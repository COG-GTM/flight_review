# Transmittal memorandum — Software Bill of Materials, Flight Review

**To:** Authorizing Official (AO); Information System Security Manager (ISSM)
**From:** Flight Review system owner / development team (`COG-GTM/flight_review`)
**Subject:** Software Bill of Materials (SBOM) and component vulnerability baseline for the Flight Review web application, in support of RMF authorization
**Baseline:** git commit `ea5c16a3bb939f49e50296f953efac40c2456489` (2026-08-18), SBOM generated 2026-10-19T16:57Z
**References:** NIST SP 800-37 Rev 2; NIST SP 800-53 Rev 5 / 800-53B; NIST SP 800-161 Rev 1; NIST SP 800-218 (SSDF); EO 14028 §4(e) and NTIA *Minimum Elements for an SBOM* (July 2021); OMB M-22-18 / M-23-16; DoDI 8510.01; DoDI 5200.44

## 1. Purpose

This package delivers the machine-readable SBOMs, the vulnerability baseline derived from them, and the supporting narratives needed for the ISSM to assess, and the AO to accept, the supply-chain and flaw-remediation posture of Flight Review. It is intended to be filed as a system security plan (SSP) artifact under CM-8 / SR-4 and to seed the Plan of Action & Milestones (POA&M) under CA-5.

## 2. System description and authorization boundary

Flight Review is a Python 3 web application (Tornado 6.5 + Bokeh 3.8 server) that accepts PX4 ULog flight-log uploads, stores metadata in SQLite, and renders interactive analysis plots and a 3D flight replay. As deployed by `docker-compose.prod.yml` it consists of:

| Component | Image / origin | Role | In this SBOM as |
|---|---|---|---|
| Application container | `app/Dockerfile` on `ubuntu:noble` | Tornado/Bokeh app, ULog parsing, SQLite DB, upload handling | `flight_review-app-image` |
| Reverse proxy | `nginx/Dockerfile` on `nginx:latest` | TLS termination, HTTP basic-auth option, static serving | `flight_review-nginx-image` |
| Certificate sidecar | `letsencrypt/Dockerfile` on `certbot/certbot:latest` | ACME renewal via cron | `flight_review-certbot-image` |
| Browser runtime | Jinja templates in `app/plot_app/templates` | JS/CSS loaded in the user's browser from CDNs and `app/plot_app/static` | `flight_review-browser-runtime` |
| Source tree | git | Declared dependencies, CI workflow actions | `flight_review-source` |

External interconnections observed in the templates and recorded as `services` in the browser-runtime BOM: Microsoft Ajax CDN, cdnjs (Cloudflare), jsDelivr, unpkg, DataTables CDN, Google Fonts, OpenStreetMap tile servers, Mapbox (optional, key-gated), Cesium ion and Bing Maps (optional, key-gated). Outbound from the server side: SMTP (upload notification e-mail, if configured) and the ACME endpoints used by certbot.

Out of scope: the host OS and Docker engine, the SQLite data files under `data/`, keys under `app/private_key/`, and the PX4 flight controllers that produce the logs.

## 3. What was produced

| Artifact | Format | Components | Notes |
|---|---|---:|---|
| Application image SBOM | CycloneDX 1.5 JSON + SPDX 2.3 JSON | 265 | Ubuntu 24.04 OS record, 121 deb, 125 pip, 18 npm (Cesium third-party) |
| nginx image SBOM | CycloneDX + SPDX | 154 | Debian 13.7 OS record, 152 deb, 1 maven |
| certbot image SBOM | CycloneDX + SPDX | 1,126 | Alpine 3.23.5; 1,038 of the components are Rust crates compiled into the `cryptography` wheel and are reported by the Cargo auditable cataloger |
| Source-tree SBOM | CycloneDX + SPDX | 8 | `bokeh==3.8.2` (the only pinned requirement) and the GitHub Actions used by CI |
| Browser-runtime SBOM | CycloneDX 1.5 JSON | 18 libraries + 10 services | Hand-derived from templates; records CDN URL, Subresource Integrity presence, and SHA-256 of vendored files |
| System manifest | CycloneDX 1.5 JSON | 5 | Links each sub-BOM by path and SHA-256 |
| Vulnerability reports | grype JSON + table, OpenVEX skeleton | — | grype 0.120.1, DB built 2026-10-19 |
| Generation record, checksums | Markdown, `SHA256SUMS` | — | Reproducibility and integrity |

Generation method: deployable images were built from the repository Dockerfiles with `docker compose -f docker-compose.prod.yml build`; **syft 1.54.1** catalogued each image and the source tree; **grype 0.120.1** matched every SBOM against its vulnerability database (NVD, GitHub Security Advisories, Ubuntu/Debian/Alpine trackers). Both tools are open-source, widely used in federal pipelines, and the exact invocation is in `generate_sbom.sh`.

## 4. Headline results (scanner view, not yet adjudicated)

| Artifact | Findings | Critical | High | Fix available |
|---|---:|---:|---:|---:|
| Application image | 207 | 0 | 3 | 10 |
| nginx image | 337 | 17 | 96 | 6 |
| certbot image | 75 | 1 | 27 | 20 |
| Browser runtime | 3 | 0 | 0 | 3 |
| Source tree | 0 | 0 | 0 | 0 |

Interpretation (detail and rationale in `docs/04_Vulnerability_Disposition.md`):

* **Application image — no Critical.** The 3 Highs are the Ubuntu-packaged `setuptools 68.1.2` and `wheel 0.42.0` build tools, which have upstream fixes and are not used at runtime. 186 of the 207 findings are Ubuntu `not-fixed`/`wont-fix` entries against `python3.12`, `glibc`, `pcre2`, `gnutls` and friends — the normal Ubuntu 24.04 LTS backlog at this date.
* **nginx image — the 17 Criticals are not nginx.** 14 are Debian `wont-fix` CVEs in `curl`/`libcurl4t64`/`libtiff6`/`libxml2` that the official `nginx:latest` image carries; the proxy does not invoke these libraries in this deployment. The remaining 3 are unpatched CVEs in `nginx 1.31.7` (Debian trixie build) and are the item that most warrants ISSM attention and an upstream-tracking POA&M entry.
* **certbot image — 1 Critical** in the bundled Python 3.14.7 interpreter, fixed in 3.14.8; 20 findings close by rebuilding on a newer `certbot/certbot` tag. The sidecar has no inbound exposure.
* **Browser runtime** — `jQuery 3.1.0` (3 Mediums, fixed in 3.5.0) is loaded from Microsoft's CDN without Subresource Integrity; `leaflet 1.3.4` and the vendored `popper.js 1.x` are end-of-life lines (SA-22).

## 5. Known limitations the AO should weigh

1. **Unpinned supply chain.** Base images are pulled by floating tag and `requirements.txt` pins only `bokeh`. The SBOM therefore describes *this* build; a rebuild tomorrow may differ. Mitigation requested: pin base images by digest and adopt a lock file (CM-2, CM-6, SR-3, SR-4(3)).
2. **Development tooling in the production image.** `jupyter`, `jupyterlab`, `pylint` and ~100 transitive packages ship in the application container but are not needed to serve the application. They enlarge the attack surface and the finding count (CM-7, SA-15(7)).
3. **Browser-runtime BOM is hand-derived.** It is complete for the templates at this commit but is not produced by an automated cataloger; it must be re-reviewed when templates change.
4. **Severities are scanner severities.** No finding has yet been marked `not_affected` or `affected`; the OpenVEX skeleton lists every Critical/High as `under_investigation` for the ISSM to adjudicate.
5. **SBOMs are not yet signed.** Integrity is provided by `SHA256SUMS` and the hashes in the system manifest. Recommended follow-on: attach the SBOMs as signed attestations to the images (e.g., cosign/in-toto) in CI (SR-4(1), SI-7).
6. **Companion code-level findings.** A separate Devin security code scan of the same commit reported 8 open findings (2 Critical XSS, 2 Medium access-control / resource-exhaustion, 4 Low). Those are application-code weaknesses, outside SBOM scope, and are being tracked for remediation separately; they should appear on the same POA&M.

## 6. Decisions requested

* **ISSM:** accept this package as the CM-8 component inventory and SR-4 provenance baseline for the stated commit; adjudicate the Critical/High findings using the OpenVEX skeleton; open POA&M items for the fix-available upgrades and the nginx 1.31.7 CVEs.
* **AO:** acknowledge the residual risk described in §4–5 pending POA&M closure, and direct that the SBOM be regenerated and re-filed with each release (CA-7, CM-8(2)).

## 7. Points of contact

System owner / developer: `COG-GTM/flight_review` maintainers (GitHub). Upstream: PX4 Autopilot Project (`PX4/flight_review`, BSD-3-Clause).
