#!/usr/bin/env python3
"""Turn the raw syft/grype output in sbom/ into reviewer-facing artifacts.

Writes:
  inventory/COMPONENT_INVENTORY.md    package tables per deployable artifact
  vulnerability/SUMMARY.md            severity x fix-state matrix, Critical/High detail
  vulnerability/openvex-skeleton.json OpenVEX document with every Critical/High
                                      finding set to under_investigation for the ISSM
  flight_review-system.cdx.json       top-level CycloneDX BOM linking each sub-BOM
  GENERATION_RECORD.md                tool versions, inputs, image digests, hashes
Only the Python standard library is used.
"""
import argparse
import hashlib
import json
import uuid
from collections import Counter, defaultdict
from pathlib import Path

SEVERITIES = ["Critical", "High", "Medium", "Low", "Negligible", "Unknown"]
FIX_STATES = ["fixed", "not-fixed", "wont-fix", "unknown"]

ARTIFACT_DESCRIPTIONS = {
    "flight_review-source": "Git working tree: declared Python requirements, CI workflow actions, vendored npm metadata",
    "flight_review-app-image": "Tornado/Bokeh application container (ubuntu:noble + apt + pip), the primary deployable",
    "flight_review-nginx-image": "Reverse proxy / TLS terminator container (nginx:latest)",
    "flight_review-certbot-image": "ACME certificate renewal sidecar (certbot/certbot), production profile only",
    "flight_review-browser-runtime": "Client-side JS/CSS fetched from CDNs or served from app/plot_app/static, plus external services",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(path: Path):
    return json.loads(path.read_text())


def license_str(comp) -> str:
    out = []
    for lic in comp.get("licenses", []):
        if "expression" in lic:
            out.append(lic["expression"])
        elif "license" in lic:
            out.append(lic["license"].get("id") or lic["license"].get("name") or "")
    return ", ".join(x for x in out if x) or "-"


def ecosystem(comp) -> str:
    purl = comp.get("purl", "")
    if purl.startswith("pkg:"):
        return purl[4:].split("/")[0].split("?")[0]
    return comp.get("type", "-")


def fix_state(match) -> str:
    return (match["vulnerability"].get("fix") or {}).get("state") or "unknown"


def esc(s) -> str:
    return str(s).replace("|", "\\|")


def write_inventory(out: Path, boms: dict) -> None:
    lines = ["# Component inventory", "",
             "Human-readable view of the CycloneDX SBOMs in `cyclonedx/`. The JSON files are authoritative; "
             "this table exists so a reviewer can skim without tooling.", ""]
    lines += ["| Artifact | Components | Ecosystems |", "|---|---:|---|"]
    for name, bom in boms.items():
        comps = [c for c in bom.get("components", []) if c.get("type") != "file"]
        eco = Counter(ecosystem(c) for c in comps)
        lines.append(f"| `{name}` | {len(comps)} | {', '.join(f'{k} ({v})' for k, v in sorted(eco.items()))} |")
    lines.append("")
    for name, bom in boms.items():
        unique = {(ecosystem(c), c.get("name"), c.get("version"), c.get("purl")): c
                  for c in bom.get("components", []) if c.get("type") != "file"}
        comps = sorted(unique.values(), key=lambda c: (ecosystem(c), c.get("name", "").lower(), c.get("version", "")))
        lines += [f"## {name}", "", ARTIFACT_DESCRIPTIONS.get(name, ""), "",
                  "| Ecosystem | Name | Version | License | Supplier / publisher | purl |", "|---|---|---|---|---|---|"]
        for c in comps:
            supplier = (c.get("supplier") or {}).get("name") or c.get("publisher") or "-"
            lines.append(f"| {ecosystem(c)} | {esc(c.get('name', ''))} | {esc(c.get('version', '-') or '-')} | "
                         f"{esc(license_str(c))} | {esc(supplier)} | `{esc(c.get('purl', '-'))}` |")
        lines.append("")
    (out / "inventory" / "COMPONENT_INVENTORY.md").write_text("\n".join(lines))


def write_vuln_summary(out: Path, scans: dict, gen: dict) -> None:
    lines = ["# Vulnerability summary (grype)", "",
             f"Scanner: grype {gen['tools']['grype']}, vulnerability DB built {gen['tools']['grype_db_built']}, "
             f"run {gen['generated_at']} against the CycloneDX SBOMs in `cyclonedx/`.", "",
             "Fix state is the distro/upstream advisory state as recorded by grype: `fixed` = a patched version exists "
             "(POA&M candidate), `not-fixed` = no patch released yet, `wont-fix` = distro has declined to patch "
             "(typically minor-impact or disputed CVEs), `unknown` = no fix data.", "",
             "Severity is the scanner's view and is **not** a risk determination for this system; that adjudication "
             "belongs to the ISSM/AO using the deployment context in `docs/04_Vulnerability_Disposition.md`.", ""]

    lines += ["## Totals", "", "| Artifact | Total | Critical | High | Medium | Low | Negligible | Unknown | with fix available |",
              "|---|---:|---:|---:|---:|---:|---:|---:|---:|"]
    for name, scan in scans.items():
        matches = scan.get("matches", [])
        sev = Counter(m["vulnerability"]["severity"] for m in matches)
        fixed = sum(1 for m in matches if fix_state(m) == "fixed")
        lines.append(f"| `{name}` | {len(matches)} | " + " | ".join(str(sev.get(s, 0)) for s in SEVERITIES) + f" | {fixed} |")
    lines.append("")

    for name, scan in scans.items():
        matches = scan.get("matches", [])
        lines += [f"## {name}", ""]
        if not matches:
            lines += ["No matches.", ""]
            continue
        matrix = defaultdict(Counter)
        for m in matches:
            matrix[m["vulnerability"]["severity"]][fix_state(m)] += 1
        lines += ["| Severity | " + " | ".join(FIX_STATES) + " |", "|---|" + "---:|" * len(FIX_STATES)]
        for s in SEVERITIES:
            if matrix.get(s):
                lines.append(f"| {s} | " + " | ".join(str(matrix[s].get(f, 0)) for f in FIX_STATES) + " |")
        lines.append("")

        crit_high = [m for m in matches if m["vulnerability"]["severity"] in ("Critical", "High")]
        if crit_high:
            lines += ["### Critical / High detail", "",
                      "| Package | Version | Type | Vulnerability | Severity | Fix state | Fixed in |", "|---|---|---|---|---|---|---|"]
            seen = set()
            for m in sorted(crit_high, key=lambda m: (m["vulnerability"]["severity"] != "Critical",
                                                      m["artifact"]["name"], m["vulnerability"]["id"])):
                key = (m["artifact"]["name"], m["artifact"]["version"], m["vulnerability"]["id"])
                if key in seen:
                    continue
                seen.add(key)
                v = m["vulnerability"]
                fixed_in = ", ".join((v.get("fix") or {}).get("versions") or []) or "-"
                lines.append(f"| {m['artifact']['name']} | {m['artifact']['version']} | {m['artifact']['type']} | "
                             f"[{v['id']}]({v.get('dataSource', '')}) | {v['severity']} | {fix_state(m)} | {fixed_in} |")
            lines.append("")

        fixable = Counter()
        for m in matches:
            if fix_state(m) == "fixed":
                fixable[(m["artifact"]["name"], m["artifact"]["version"], m["artifact"]["type"])] += 1
        if fixable:
            lines += ["### Packages with a fix available (POA&M candidates)", "",
                      "| Package | Current | Type | Findings closed by upgrade |", "|---|---|---|---:|"]
            for (n, ver, typ), cnt in sorted(fixable.items(), key=lambda kv: -kv[1]):
                lines.append(f"| {n} | {ver} | {typ} | {cnt} |")
            lines.append("")
    (out / "vulnerability" / "SUMMARY.md").write_text("\n".join(lines))


def write_openvex(out: Path, scans: dict, gen: dict) -> None:
    statements = []
    seen = set()
    for name, scan in scans.items():
        for m in scan.get("matches", []):
            v = m["vulnerability"]
            if v["severity"] not in ("Critical", "High"):
                continue
            purl = m["artifact"].get("purl") or f"{m['artifact']['name']}@{m['artifact']['version']}"
            key = (v["id"], purl)
            if key in seen:
                continue
            seen.add(key)
            statements.append({
                "vulnerability": {"name": v["id"]},
                "products": [{"@id": purl}],
                "status": "under_investigation",
                "action_statement": f"ISSM to adjudicate; surfaced in SBOM {name}. Replace status with "
                                    "not_affected (with justification) / affected (with POA&M) / fixed.",
            })
    doc = {
        "@context": "https://openvex.dev/ns/v0.2.0",
        "@id": f"https://github.com/{gen['repository']}/sbom/vex/{uuid.uuid4()}",
        "author": "Flight Review system owner (skeleton generated by sbom/tools/build_reports.py; statuses not yet adjudicated)",
        "timestamp": gen["generated_at"],
        "version": 1,
        "statements": statements,
    }
    (out / "vulnerability" / "openvex-skeleton.json").write_text(json.dumps(doc, indent=2))


def write_system_bom(out: Path, boms: dict, gen: dict) -> None:
    components, deps = [], []
    for name, bom in boms.items():
        path = out / "cyclonedx" / f"{name}.cdx.json"
        meta = bom.get("metadata", {}).get("component", {})
        ref = f"sub-bom:{name}"
        components.append({
            "bom-ref": ref,
            "type": meta.get("type", "application"),
            "name": name,
            "version": meta.get("version", gen["git_commit_short"]),
            "description": ARTIFACT_DESCRIPTIONS.get(name, ""),
            "externalReferences": [{
                "type": "bom",
                "url": f"cyclonedx/{name}.cdx.json",
                "comment": f"CycloneDX serialNumber {bom.get('serialNumber', 'n/a')}; SPDX twin at spdx/{name}.spdx.json"
                           if name != "flight_review-browser-runtime" else f"CycloneDX serialNumber {bom.get('serialNumber', 'n/a')}",
                "hashes": [{"alg": "SHA-256", "content": sha256(path)}],
            }],
        })
        deps.append(ref)
    system = {
        "$schema": "http://cyclonedx.org/schema/bom-1.5.schema.json",
        "bomFormat": "CycloneDX",
        "specVersion": "1.5",
        "serialNumber": f"urn:uuid:{uuid.uuid4()}",
        "version": 1,
        "metadata": {
            "timestamp": gen["generated_at"],
            "tools": {"components": [
                {"type": "application", "name": "syft", "version": gen["tools"]["syft"], "author": "anchore"},
                {"type": "application", "name": "grype", "version": gen["tools"]["grype"], "author": "anchore"},
                {"type": "application", "name": "build_reports.py", "version": "1.0"}]},
            "supplier": {"name": gen["supplier"]},
            "component": {
                "bom-ref": "flight_review-system",
                "type": "application",
                "name": "flight_review",
                "version": gen["git_commit"],
                "description": "PX4 Flight Review web application (ULog upload, analysis, plotting) as deployed by docker-compose.prod.yml",
                "externalReferences": [{"type": "vcs", "url": f"https://github.com/{gen['repository']}"}],
            },
        },
        "components": components,
        "dependencies": [{"ref": "flight_review-system", "dependsOn": deps}],
    }
    (out / "flight_review-system.cdx.json").write_text(json.dumps(system, indent=2))


def write_generation_record(out: Path, boms: dict, scans: dict, gen: dict) -> None:
    lines = ["# Generation record", "",
             "Who/what/when for every file in this package, so a reviewer can reproduce it with "
             "`sbom/generate_sbom.sh` and compare hashes.", "",
             "| Field | Value |", "|---|---|",
             f"| Generated (UTC) | {gen['generated_at']} |",
             f"| Repository | https://github.com/{gen['repository']} |",
             f"| Commit | `{gen['git_commit']}` ({gen['git_commit_date']}) |",
             f"| Supplier recorded in BOMs | {gen['supplier']} |",
             f"| SBOM generator | syft {gen['tools']['syft']} (CycloneDX 1.x JSON, SPDX 2.3 JSON) |",
             f"| Vulnerability scanner | grype {gen['tools']['grype']}, DB built {gen['tools']['grype_db_built']} |",
             "| Browser-runtime BOM | `tools/browser_runtime_bom.py` (hand-maintained list derived from templates) |",
             "", "## Container images scanned", "",
             "| Role | Image ref | Image ID | Base image | Base digest |", "|---|---|---|---|---|"]
    for role, img in gen["images"].items():
        lines.append(f"| {role} | `{img['ref']}` | `{img['id']}` | `{img['base']}` | `{img['base_digest']}` |")
    lines += ["", "## Artifact hashes", "", "| File | SHA-256 |", "|---|---|"]
    for sub in ("cyclonedx", "spdx", "vulnerability"):
        for p in sorted((out / sub).glob("*.json")):
            lines.append(f"| `{sub}/{p.name}` | `{sha256(p)}` |")
    lines += ["", "## Component / finding counts", "", "| Artifact | Components (non-file) | grype matches |", "|---|---:|---:|"]
    for name, bom in boms.items():
        n = sum(1 for c in bom.get("components", []) if c.get("type") != "file")
        lines.append(f"| `{name}` | {n} | {len(scans.get(name, {}).get('matches', []))} |")
    lines.append("")
    (out / "GENERATION_RECORD.md").write_text("\n".join(lines))


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    out = Path(args.out)
    gen = load(out / "generation.json")

    order = list(ARTIFACT_DESCRIPTIONS)
    boms = {p.stem[:-4]: load(p) for p in (out / "cyclonedx").glob("*.cdx.json")}
    boms = {k: boms[k] for k in sorted(boms, key=lambda k: order.index(k) if k in order else 99)}
    scans = {}
    for name in boms:
        p = out / "vulnerability" / f"{name}.grype.json"
        if p.exists():
            scans[name] = load(p)

    write_inventory(out, boms)
    write_vuln_summary(out, scans, gen)
    write_openvex(out, scans, gen)
    write_system_bom(out, boms, gen)
    write_generation_record(out, boms, scans, gen)


if __name__ == "__main__":
    main()
