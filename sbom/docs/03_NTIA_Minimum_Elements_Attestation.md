# NTIA Minimum Elements attestation

Element-by-element statement against *The Minimum Elements for a Software Bill of Materials (SBOM)*, NTIA, July 2021 (issued under EO 14028 §4(f)), with notes on the additional baseline attributes in CISA's 2025 *Minimum Elements* update where this package already provides them. Applies to every SBOM in `cyclonedx/` and `spdx/` for commit `ea5c16a3bb939f49e50296f953efac40c2456489`.

## 1. Data fields

| NTIA element | Requirement | Status | Where / how |
|---|---|---|---|
| Supplier name | Name of the entity that creates, defines, and identifies components | **Met with caveat** | Component level: `publisher` (deb/apk maintainer) or `author` (PyPI metadata) as discovered by syft; SPDX `supplier`/`originator` where package metadata provides it; browser-runtime BOM carries an explicit `supplier` per library. Described-artifact level: `metadata.supplier` = "PX4 Autopilot Project (upstream); COG-GTM (fork maintainer)". **Caveat:** for packages whose metadata lacks an author (some pip wheels) the field is absent rather than guessed |
| Component name | Designation assigned by the original supplier | **Met** | `name` on every component, as published in the package database / index |
| Version of the component | Identifier used by the supplier to specify a change from a previously identified version | **Met** | `version` on every component; two vendored browser assets (`popper.js`, `animate.css`) embed no version string and are flagged `flight_review:version_unverified=true` rather than given an invented version |
| Other unique identifiers | Other identifiers used to identify a component or serve as a look-up key | **Met** | Package URL (`purl`) on every catalogued component; CPE 2.3 where syft can derive one; image IDs and base-image digests for containers; SHA-256 for vendored browser files and for each sub-BOM in the system manifest |
| Dependency relationship | Characterizing the relationship that an upstream component X is included in software Y | **Met** | CycloneDX `dependencies` graph (syft emits package-to-package relationships where the ecosystem metadata exposes them, and container → package containment); SPDX `relationships` (`CONTAINS`, `DEPENDS_ON`, `DESCRIBES`); system manifest expresses system → artifact → sub-BOM |
| Author of SBOM data | Name of the entity that creates the SBOM data | **Met** | CycloneDX `metadata.tools` (syft 1.54.1; `browser_runtime_bom.py`; `build_reports.py`), SPDX `creationInfo.creators` (Tool: syft, Organization: supplier string); `GENERATION_RECORD.md` names the generating repository commit and run |
| Timestamp | Record of the date and time of the SBOM data assembly | **Met** | `metadata.timestamp` / `creationInfo.created` on every BOM, UTC |

## 2. Automation support

| Requirement | Status | Where / how |
|---|---|---|
| Machine-readable, in one of SPDX, CycloneDX, or SWID | **Met (two formats)** | SPDX 2.3 JSON and CycloneDX 1.5 JSON for every artifact catalogued by syft; CycloneDX 1.5 for the browser-runtime and system manifest. Schema references are embedded (`$schema`, `spdxVersion`) |
| Automatic generation | **Met** | `generate_sbom.sh` builds, catalogues, scans, and writes checksums without manual steps; only the browser-runtime list is maintained by hand (and is generated from that list by script) |

## 3. Practices and processes

| Requirement | Status | Where / how |
|---|---|---|
| Frequency — new SBOM with each new build/release or when a component changes | **Process defined, not yet enforced** | `README.md` instructs regeneration per release and on base-image / requirements change; recommend adding `generate_sbom.sh` to CI so this is automatic (CM-8(2)) |
| Depth — all top-level components and their transitive dependencies | **Met for server side; met for client side at the library level** | Container scans capture the full installed closure (OS + language packages + compiled-in Rust crates via cargo-auditable). Browser-runtime BOM lists each delivered library; the internal dependencies of bundled CDN files (e.g. what `bootstrap.bundle.min.js` includes) are not enumerated |
| Known unknowns — state explicitly where the dependency graph is not fully enumerated | **Met** | This section; the `version_unverified` property; the unpinned-tag caveat in the transmittal memo §5 |
| Distribution and delivery — available in a timely fashion with appropriate access | **Met** | Committed to the repository under `sbom/` with the code it describes; delivered to AO/ISSM as a zip + PDF; `SHA256SUMS` for integrity on receipt |
| Access control — terms for who may see the SBOM | **Met (open)** | Repository is the access-control boundary; no sensitive data (keys, data files) is included |
| Accommodation of mistakes — tolerance for errors and omissions | **Met** | Reproducible generation from a recorded commit; corrections are a regeneration plus commit; CycloneDX `serialNumber`/`version` allow superseding a BOM |

## 4. Additional attributes (CISA *Minimum Elements* 2025 update and *Framing* 3rd ed.)

| Attribute | Status | Where |
|---|---|---|
| Component hash | **Partial** | SHA-256 for vendored browser assets, container images, and each sub-BOM. Per-package hashes for deb/apk/pip are not exposed by the package databases syft reads; per-file hashes were deliberately excluded to keep the BOMs reviewable (`SYFT_FILE_METADATA_SELECTION=none`) and can be enabled on request |
| License | **Met where declared** | `licenses` on components where package metadata declares one; SPDX identifiers used when recognised |
| Tool name | **Met** | `metadata.tools` / `creators` |
| Generation context | **Met** | Build-time cataloguing of the as-built image (not source-only, not runtime-observed), recorded in `GENERATION_RECORD.md` |
| Primary component / described artifact | **Met** | `metadata.component` in each CycloneDX BOM; `documentDescribes` in SPDX; system manifest ties them together |

## 5. Statement

The SBOMs in this package were generated automatically from the repository at the recorded commit using the tools and versions listed in `GENERATION_RECORD.md`, contain the NTIA minimum data fields for every component the catalogers could identify, and state their known unknowns above. They have not been independently verified by a third party and are not cryptographically signed; integrity on hand-off is provided by `SHA256SUMS`.
