# RMF and NIST SP 800-53 Rev 5 control mapping

How this SBOM package is used at each step of the Risk Management Framework (NIST SP 800-37 Rev 2, DoDI 8510.01) and which NIST SP 800-53 Rev 5 controls it implements, supports, or exposes a gap against. "Supports" means the artifact is evidence the control is partially met or is the input the control needs; it is not a claim that the control is fully implemented. Assessment procedures are from NIST SP 800-53A Rev 5.

## 1. RMF step mapping (SP 800-37 Rev 2)

| RMF step | Task | How this package is used |
|---|---|---|
| Prepare (system level) | P-10 Asset identification; P-11 Authorization boundary | §2 of the transmittal memo and the `services` block of the browser-runtime BOM enumerate the deployable components and the external CDNs / tile services the boundary touches |
| Categorize | C-1 System description | Component list and data flows feed the SSP system description; the SBOM does not change the FIPS 199 categorization but confirms there is no cryptographic module beyond OpenSSL / pycryptodome / Python `ssl` |
| Select | S-2 Control selection, S-3 tailoring | Highlights SR, CM-8, SA-22, RA-5, SI-2 as applicable; supports tailoring-in of SR-4 enhancements |
| Implement | I-1 Control implementation | Package implements CM-8 (inventory) and SR-4 (provenance) for the software layer; `generate_sbom.sh` is the implementation mechanism |
| Assess | A-3 Assessment | Assessor can reproduce the SBOM from the recorded commit and compare `SHA256SUMS`; grype output is independent evidence for RA-5 |
| Authorize | R-2 Risk analysis, R-3 Risk response, R-4 Authorization decision | Headline results and known limitations (memo §4–5) and the disposition document give the AO the residual-risk picture; POA&M candidates are enumerated |
| Monitor | M-1 System and environment changes; M-2 Ongoing assessments; M-5 Security and privacy reporting | Regenerate on each release / base-image change; diff SBOMs to detect unauthorized component change (CM-8(3)); rescan the *same* SBOM against a fresh grype DB without rebuilding to catch newly published CVEs (RA-5(2)) |

## 2. NIST SP 800-53 Rev 5 control mapping

Legend: **I** = implemented by this package; **S** = supported / evidence provided; **G** = gap identified by this package (recommend POA&M entry).

### Configuration Management (CM)

| Control | Title | Status | Evidence in package / finding |
|---|---|---|---|
| CM-2 | Baseline Configuration | S / G | SBOM + image digests in `GENERATION_RECORD.md` constitute the software baseline for commit `ea5c16a`. **Gap:** base images referenced by floating tag (`ubuntu:noble`, `nginx:latest`, `certbot/certbot:latest`), so the baseline is not reproducible by tag alone |
| CM-2(2) | Automation support for accuracy / currency | I | `generate_sbom.sh` regenerates the baseline from source in one command |
| CM-3 | Configuration Change Control | S | Diffing successive SBOMs makes component-level change visible in review |
| CM-6 | Configuration Settings | G | `requirements.txt` pins only `bokeh`; 124 Python packages float. Recommend a lock file (`pip-compile` / `uv lock`) |
| CM-7 / CM-7(1) | Least Functionality | G | `jupyter`, `jupyterlab`, `notebook`, `pylint`, `ipykernel` and ~100 transitive packages are installed in the production app image but are not used by `serve.py`. Recommend a separate dev requirements file |
| CM-8 | System Component Inventory | I | CycloneDX / SPDX SBOMs for every deployable artifact plus `inventory/COMPONENT_INVENTORY.md`; each entry carries name, version, supplier/publisher, license, purl, CPE (where derivable) and layer location |
| CM-8(1) | Updates during installation / removal | S | Regeneration is tied to the build; recommend running it in CI on every merge |
| CM-8(2) | Automated maintenance | I | Scripted; outputs committed with the code |
| CM-8(3) | Automated unauthorized component detection | S | SBOM diff between releases is the detection mechanism; alerting is not yet wired |
| CM-8(6) | Assessed configurations / approved deviations | S | OpenVEX skeleton is the place to record approved deviations |
| CM-10 | Software Usage Restrictions | S | License for every component is recorded (SPDX identifiers where known) — see inventory; no copyleft-incompatible licence detected for a hosted web service, but legal review is outside this package |
| CM-11 | User-Installed Software | S | Image inventory shows exactly what is installed; nothing is installed at runtime |

### Risk Assessment (RA)

| Control | Title | Status | Evidence / finding |
|---|---|---|---|
| RA-3(1) | Supply Chain Risk Assessment | S | Supplier / origin of every component, CDN providers and tile services identified for C-SCRM review (SP 800-161 Rev 1) |
| RA-5 | Vulnerability Monitoring and Scanning | I | grype 0.120.1 against DB built 2026-10-19; results per artifact in `vulnerability/` |
| RA-5(2) | Update vulnerabilities to be scanned | I | `grype db update` runs every generation; the stored SBOMs can be rescanned without rebuilding |
| RA-5(3) | Breadth / depth of coverage | S | OS packages, language packages (pip, npm, cargo-auditable), binaries (python), browser-side libraries |
| RA-5(5) | Privileged access | n/a | Image scanning needs no credentials to the system |
| RA-5(11) | Public disclosure program | — | Not addressed by this package |
| RA-7 | Risk Response | S | POA&M candidate tables in `vulnerability/SUMMARY.md` §"Packages with a fix available" |

### System and Services Acquisition (SA)

| Control | Title | Status | Evidence / finding |
|---|---|---|---|
| SA-4(5) | System, component, service configurations | S | SBOM documents the as-built configuration of each container |
| SA-8 | Security and Privacy Engineering Principles | S | Supports "least common mechanism / minimization" review (see CM-7 gap) |
| SA-9 | External System Services | S / G | Browser-runtime BOM lists 11 external services. **Gap:** 6 of 8 CDN-delivered scripts/styles are loaded without Subresource Integrity, so an external CDN compromise would execute in users' browsers (also SI-7) |
| SA-10 | Developer Configuration Management | S / G | Commit, Dockerfiles and compose files are the CM record. **Gap:** CI workflow uses `actions/checkout@master` and `ad-m/github-push-action@master` (mutable refs) — pin to commit SHAs |
| SA-11 | Developer Testing and Evaluation | S | CI runs pylint and a docker build; no SAST/DAST evidence is in this package (the companion Devin code scan covers SAST) |
| SA-15(7) | Automated vulnerability analysis | S | grype step in `generate_sbom.sh`; recommend running in CI with `--fail-on high` once the baseline is adjudicated |
| SA-22 | Unsupported System Components | G | `jquery 3.1.0` (2016; current 3.7.x), `leaflet 1.3.4` (2018; 1.9.x current), vendored `popper.js 1.x` (superseded by @popperjs/core 2.x in 2020), `lightbox2 2.7.1`, `pace 1.0.2` (unmaintained). Python 3.12, nginx 1.31, Ubuntu 24.04 LTS, Debian 13 are supported |

### System and Information Integrity (SI)

| Control | Title | Status | Evidence / finding |
|---|---|---|---|
| SI-2 | Flaw Remediation | S | Fix-available tables give the exact upgrade targets; distro `not-fixed` / `wont-fix` states are recorded so the ISSM can distinguish actionable from non-actionable findings |
| SI-2(2) | Automated flaw remediation status | S | Rescanning the committed SBOM reports status without rebuilding |
| SI-2(3) | Time to remediate / benchmarks | — | Dates of first detection are not tracked yet; start from this baseline |
| SI-5 | Security Alerts, Advisories, Directives | S | purls / CPEs allow the SBOM to be matched against new advisories (e.g., with a continuous SBOM monitor) |
| SI-7 | Software, Firmware, Information Integrity | S / G | SHA-256 of every vendored browser asset is in the BOM; `SHA256SUMS` covers the package. **Gaps:** SBOMs are not signed; CDN assets mostly lack SRI (see SA-9) |

### Supply Chain Risk Management (SR)

| Control | Title | Status | Evidence / finding |
|---|---|---|---|
| SR-2 | Supply Chain Risk Management Plan | S | Component / supplier inventory is the input to the plan |
| SR-3 | Supply Chain Controls and Processes | S / G | Package identifies the acquisition channels (Docker Hub, Ubuntu/Debian/Alpine archives, PyPI, npm CDNs). **Gap:** no digest pinning or mirror / allow-list policy for these channels |
| SR-4 | Provenance | I | SBOM with supplier, version, unique identifiers (purl, CPE), image digests and build commit for every component — the core provenance record |
| SR-4(1) | Identity | S | Each component uniquely identified by purl; recommend signing SBOMs to bind identity to the build |
| SR-4(2) | Track and trace | S | Layer IDs in the CycloneDX properties show which Dockerfile step introduced each package |
| SR-4(3) | Validate as genuine and not altered | G | No signature verification of base images or packages is enforced (apt/pip do verify repository signatures / hashes during build, but images are pulled by tag) |
| SR-5 | Acquisition Strategies, Tools, Methods | S | Inventory of sources supports a decision to use an internal registry / mirror |
| SR-6 | Supplier Assessments and Reviews | S | Supplier / publisher column in the inventory identifies who to assess |
| SR-8 | Notification Agreements | S | Supplier list identifies whose advisories to subscribe to (Ubuntu USN, Debian DSA, Alpine, PyPA, nginx, Bokeh) |
| SR-10 | Inspection of Systems or Components | S | SBOM is the reference for inspecting a running container (`syft` the live image and diff) |
| SR-11 | Component Authenticity | G | Same as SR-4(3) |
| SR-12 | Component Disposal | n/a | — |

### Other controls touched

| Control | Status | Note |
|---|---|---|
| CA-5 Plan of Action and Milestones | S | POA&M candidates: see `docs/04_Vulnerability_Disposition.md` §4 |
| CA-7 Continuous Monitoring | S | Regeneration cadence recommendation in `README.md` |
| SC-7 Boundary Protection | S | External services in the browser-runtime BOM define outbound flows for the boundary diagram |
| SC-13 Cryptographic Protection | S | Cryptographic components present: OpenSSL (Debian/Alpine/Ubuntu), `pycryptodome 4.1.0` (ULge encrypted-log support), `cryptography` (certbot). None is FIPS 140-validated as packaged; relevant if the system must meet SC-13 with validated modules |
| PM-30 Supply Chain Risk Management Strategy | S | Organization-level; this package is one system's input |

## 3. Cross-walk to other frameworks the AO may ask about

| Framework | Relevant requirement | How met |
|---|---|---|
| EO 14028 §4(e)(vii) / NTIA Minimum Elements (July 2021) | Provide a purchaser an SBOM with the data fields, automation support, and practices | See `docs/03_NTIA_Minimum_Elements_Attestation.md` |
| OMB M-22-18 / M-23-16 | Agencies may require SBOMs from software producers; secure software attestation | SBOM available in two standard formats; attestation form (CISA Secure Software Development Attestation) is outside this package |
| NIST SP 800-218 SSDF v1.1 | PS.3.2 (provenance data / SBOM), PW.4.1 (acquire well-secured components), RV.1.1 (gather vulnerability information) | PS.3.2 met by this package; PW.4.1 and RV.1.1 evidenced by the inventory and grype output |
| NIST SP 800-161 Rev 1 (C-SCRM) | Component inventory, supplier identification, vulnerability management in the supply chain | Inventory, supplier column, external-service list |
| DoDI 5200.44 (Trusted Systems and Networks) | Criticality analysis and supply-chain risk management for critical components | Component inventory is the starting point for criticality analysis |
| CISA SBOM guidance (*Framing Software Component Transparency*, 3rd ed. 2024; *Minimum Elements* 2025 update) | Baseline attributes including hashes, license, dependency relationships, tool name, generation context | CycloneDX output carries hashes (vendored assets, images), licenses, dependency graph, tool metadata |

## 4. Gaps summary (recommended POA&M entries)

| # | Gap | Controls | Suggested milestone |
|---|---|---|---|
| G1 | Base images pulled by floating tag | CM-2, CM-6, SR-3, SR-4(3), SR-11 | Pin `FROM` lines to `@sha256:` digests recorded in `GENERATION_RECORD.md`; add a renovate/dependabot rule |
| G2 | Python dependencies unpinned beyond `bokeh` | CM-6, SR-3 | Generate `requirements.lock` with hashes (`pip-compile --generate-hashes`) and install with `--require-hashes` |
| G3 | Dev tooling (jupyter, pylint) in production image | CM-7, SA-8, SA-15(7) | Split `requirements-dev.txt`; rebuild; expect the app image finding count to drop materially |
| G4 | CDN scripts without Subresource Integrity | SA-9, SI-7 | Add `integrity=` attributes or vendor the assets; already done for DataTables and Leaflet |
| G5 | End-of-life browser libraries (jQuery 3.1.0, leaflet 1.3.4, popper.js 1.x) | SA-22, SI-2 | Upgrade jQuery to 3.7.x (also closes 3 CVEs), leaflet to 1.9.x; remove the unreferenced vendored copies |
| G6 | CI actions pinned to `master` | SA-10, SR-3 | Pin to commit SHAs |
| G7 | SBOMs unsigned | SR-4(1), SI-7 | Sign in CI (cosign attest) and verify at deploy |
| G8 | nginx 1.31.7 unpatched CVEs (3 Critical, 1 High) | SI-2, RA-5 | Track Debian/nginx advisories; rebuild on fixed `nginx` tag; consider `nginx:stable` instead of mainline `latest` |
| G9 | certbot image Python 3.14.7 Critical | SI-2 | Rebuild on current `certbot/certbot` tag (fix in 3.14.8) |
