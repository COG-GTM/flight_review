#!/usr/bin/env python3
"""Render the reviewer-facing Markdown in sbom/ into one PDF for hand-off.

Usage: python3 sbom/tools/render_pdf.py --out sbom/dist/Flight_Review_SBOM_Package.pdf
Needs the `markdown` package and `wkhtmltopdf` on PATH; both are optional for
generate_sbom.sh, which is why this is a separate step.
"""
import argparse
import subprocess
import tempfile
from pathlib import Path

import markdown

ORDER = [
    "README.md",
    "docs/01_Transmittal_Memo_AO_ISSM.md",
    "docs/02_RMF_Control_Mapping.md",
    "docs/03_NTIA_Minimum_Elements_Attestation.md",
    "docs/04_Vulnerability_Disposition.md",
    "vulnerability/SUMMARY.md",
    "GENERATION_RECORD.md",
    "inventory/COMPONENT_INVENTORY.md",
]

CSS = """
body { font-family: Helvetica, Arial, sans-serif; font-size: 10.5pt; line-height: 1.35; margin: 0 24px; color: #111; }
h1 { font-size: 20pt; border-bottom: 2px solid #1f3a5f; padding-bottom: 4px; margin-top: 28px; page-break-before: always; }
h1:first-of-type { page-break-before: avoid; }
h2 { font-size: 14pt; color: #1f3a5f; margin-top: 22px; }
h3 { font-size: 11.5pt; margin-top: 16px; }
table { border-collapse: collapse; width: 100%; margin: 8px 0 14px; font-size: 8.5pt; page-break-inside: auto; }
th, td { border: 1px solid #bbb; padding: 3px 5px; text-align: left; vertical-align: top; word-break: break-word; }
th { background: #e9eef5; }
tr { page-break-inside: avoid; }
code { font-family: Menlo, Consolas, monospace; font-size: 8.5pt; background: #f3f3f3; padding: 0 2px; }
pre { background: #f3f3f3; padding: 8px; font-size: 8.5pt; white-space: pre-wrap; }
blockquote { border-left: 3px solid #1f3a5f; margin: 8px 0; padding: 2px 10px; color: #333; }
.cover { text-align: center; margin-top: 180px; }
.cover h1 { border: none; font-size: 26pt; page-break-before: avoid; }
.cover p { font-size: 12pt; }
"""


def main() -> None:
    """Concatenate the Markdown in ORDER and print the PDF path."""
    ap = argparse.ArgumentParser()
    ap.add_argument("--sbom-dir", default=str(Path(__file__).resolve().parents[1]))
    ap.add_argument("--out", required=True)
    ap.add_argument("--title", default="Flight Review — Software Bill of Materials Package")
    ap.add_argument("--subtitle", default="Prepared for Authorizing Official and ISSM review (RMF / NIST SP 800-53 Rev 5)")
    args = ap.parse_args()
    sbom_dir = Path(args.sbom_dir)

    md = markdown.Markdown(extensions=["tables", "fenced_code", "toc"])
    parts = [f'<div class="cover"><h1>{args.title}</h1><p>{args.subtitle}</p></div>']
    for rel in ORDER:
        p = sbom_dir / rel
        if not p.exists():
            continue
        parts.append(md.reset().convert(p.read_text()))
    html = f"<html><head><meta charset='utf-8'><style>{CSS}</style></head><body>{''.join(parts)}</body></html>"

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False) as fh:
        fh.write(html)
        tmp = fh.name
    subprocess.run(["wkhtmltopdf", "--quiet", "--enable-local-file-access", "-s", "Letter",
                    "-T", "15mm", "-B", "15mm", "-L", "12mm", "-R", "12mm", tmp, str(out)], check=True)
    print(out)


if __name__ == "__main__":
    main()
