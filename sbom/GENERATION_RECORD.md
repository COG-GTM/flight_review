# Generation record

Who/what/when for every file in this package, so a reviewer can reproduce it with `sbom/generate_sbom.sh` and compare hashes.

| Field | Value |
|---|---|
| Generated (UTC) | 2026-10-19T17:12:55Z |
| Repository | https://github.com/COG-GTM/flight_review |
| Commit | `aec3f49a6ef5e230129046b8a5ed4533c4fb6e06` (2026-10-19T17:07:07+00:00) |
| Supplier recorded in BOMs | PX4 Autopilot Project (upstream); COG-GTM (fork maintainer) |
| SBOM generator | syft 1.54.1 (CycloneDX 1.x JSON, SPDX 2.3 JSON) |
| Vulnerability scanner | grype 0.120.1, DB built 2026-10-19T06:39:15Z |
| Browser-runtime BOM | `tools/browser_runtime_bom.py` (hand-maintained list derived from templates) |

## Container images scanned

| Role | Image ref | Image ID | Base image | Base digest |
|---|---|---|---|---|
| app | `flight_review-flight_review_app:latest` | `sha256:4cc9b81d407bcecf37885134e9b4e102a8b8d14196605325b66bcfc2a3a19965` | `ubuntu:noble` | `ubuntu@sha256:68ee22004a9109b44973313b02ff7b1de250f1de0f5ecb628d73f579aaff33ac` |
| nginx | `flight_review-nginx:latest` | `sha256:ba75d9d08875f79d50d52bcdbfb0845dd0ef13fcf17420cdf705bd4beacf26a1` | `nginx:latest` | `nginx@sha256:bc4cad49969aaf95eb4eecec5572846f86e59f1e8332aba36ed64b91aff8b724` |
| certbot | `flight_review-certbot:latest` | `sha256:3f89a9d6e6c9cd1b3e3df0a12d986e5058af607d7a2908566ee65a9c745a129d` | `certbot/certbot:latest` | `certbot/certbot@sha256:f70ad0adbb7e117f0fe42a63c553f28ea451edabc0148757b6efcd9735acaa20` |

## Artifact hashes

| File | SHA-256 |
|---|---|
| `cyclonedx/flight_review-app-image.cdx.json` | `96537ddc023fb0e891ce657d7126b889300b28abf015ff668c622b023af52c37` |
| `cyclonedx/flight_review-browser-runtime.cdx.json` | `ef7de7f337d744ca83dbc33b929a9431d70f43aadc00c320a322899837c18577` |
| `cyclonedx/flight_review-certbot-image.cdx.json` | `2aeec94c5cdac9a33bdd6e8fc393c367f6b60f80ab866094007b1ff585ce094f` |
| `cyclonedx/flight_review-nginx-image.cdx.json` | `42a35563f8c010f24304c7538f5ff37a68ad8b2798c8a87335fbebdc1b1589d5` |
| `cyclonedx/flight_review-source.cdx.json` | `515a32a44b74819960ea0a1173cfdc3901407e8005f1a89460adf37946b4bdf8` |
| `spdx/flight_review-app-image.spdx.json` | `ef6ec2d3223872613e1b71b946ae4b49c3496f7926d2b9950a6f3db897432b52` |
| `spdx/flight_review-certbot-image.spdx.json` | `86bef0f1aa73077506d0b5e373573390a0e34d9578a903090cc0c0e23d306a65` |
| `spdx/flight_review-nginx-image.spdx.json` | `4b0ca6e1730ccb5fce643494ec6a77aa44fda17b3c93a28888bd3cd431a584ad` |
| `spdx/flight_review-source.spdx.json` | `6a24ddbf44a78089423e3d032837d8b380dd1418edc7173ee50c2e52a8a3b962` |
| `vulnerability/flight_review-app-image.grype.json` | `1845ea599e01e492fe449ce2ee3e047b98e0388ee278618b25fd9559ac42c836` |
| `vulnerability/flight_review-browser-runtime.grype.json` | `d15f14b42a064ef3990f19fec174e170f233d820b3163641682835cc8fd587b3` |
| `vulnerability/flight_review-certbot-image.grype.json` | `5687ca145eafc775e0e9ef88d772ccda43bf039a9b1c052e07dc40cee4ad199d` |
| `vulnerability/flight_review-nginx-image.grype.json` | `0a71d4ca7dafb47b0d2086fe22b5e9bef1bad5cd4c62a290b82f1c4a461489d9` |
| `vulnerability/flight_review-source.grype.json` | `738ea2a4617813b03a90f1c5020d61cf2190e00764e295c97d3280cdf983d4a2` |
| `vulnerability/openvex-skeleton.json` | `077a90a1fae1286963aa1acd507d2950c38cf6eb941e1c5fedf4625153415511` |

## Component / finding counts

| Artifact | Components (non-file) | grype matches |
|---|---:|---:|
| `flight_review-source` | 8 | 0 |
| `flight_review-app-image` | 265 | 207 |
| `flight_review-nginx-image` | 154 | 337 |
| `flight_review-certbot-image` | 1126 | 75 |
| `flight_review-browser-runtime` | 19 | 3 |
