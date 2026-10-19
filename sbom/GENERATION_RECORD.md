# Generation record

Who/what/when for every file in this package, so a reviewer can reproduce it with `sbom/generate_sbom.sh` and compare hashes.

| Field | Value |
|---|---|
| Generated (UTC) | 2026-10-19T17:06:08Z |
| Repository | https://github.com/COG-GTM/flight_review |
| Commit | `ea5c16a3bb939f49e50296f953efac40c2456489` (2026-08-18T03:34:46+09:00) |
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
| `cyclonedx/flight_review-app-image.cdx.json` | `d78ed2dd6b3eb2f7bca414d73e527e2d13f1da529ef1cd1e9c3ff06d150bc0ed` |
| `cyclonedx/flight_review-browser-runtime.cdx.json` | `dccdd1b0b5995b31d578811b574f7b2488e643930c1c00fcca392ddc4c6f1177` |
| `cyclonedx/flight_review-certbot-image.cdx.json` | `a6bab41eb50013ca99c4ae88e582f5d6b8b0efd9bcd840831f5be9ceeec7c680` |
| `cyclonedx/flight_review-nginx-image.cdx.json` | `d9974f0c67670bf3c89506e12b699f84788042372635a3042e562fe0b9d41d4e` |
| `cyclonedx/flight_review-source.cdx.json` | `40bf196cf1971f0c49ec0cb3927f3611f1d8236a60968807fd79020edcc9f2c5` |
| `spdx/flight_review-app-image.spdx.json` | `56562b49a9cf4f64078dd3478057a3cad68fc0b6df4a9a77c7afeb5101a0bf60` |
| `spdx/flight_review-certbot-image.spdx.json` | `05f37f624975dbf68ed3b6a96d4786b4db5f3fb0d679d64fe3faaebbf39aa477` |
| `spdx/flight_review-nginx-image.spdx.json` | `439dc6bc06c215100fd04541730608b1aed6ae850377bb486301b5e94953776b` |
| `spdx/flight_review-source.spdx.json` | `372c1ba85b38d6bca0674d002c2d206b1c3c0378053c59b5e6db8cfe1d3be97b` |
| `vulnerability/flight_review-app-image.grype.json` | `0adfe87cb88d7ad27a68329d5a19c26c259c0f8a8a0e6bccb46959b6dbceb8a6` |
| `vulnerability/flight_review-browser-runtime.grype.json` | `35aafb5dd280e28255f86fff99ae546f1a4295d91c8a4477dc04f2a73fb8ee0a` |
| `vulnerability/flight_review-certbot-image.grype.json` | `38e3a72c31872660708c41b6ce409dbda70df074046afcb6a70a948c364ede10` |
| `vulnerability/flight_review-nginx-image.grype.json` | `b22f8fee676c78fbf241fddb15194cd2926c02bd4de30769bd3d9b3d3260d185` |
| `vulnerability/flight_review-source.grype.json` | `471a3ccc992e0ec9e4d061f1d9b4d16d3f4d17d8bcc1e8c62f3c28242b0052f8` |
| `vulnerability/openvex-skeleton.json` | `9c5207cd19b6b604ee217f30d678c73804b134e61d75be09e66cacc5df9a29e2` |

## Component / finding counts

| Artifact | Components (non-file) | grype matches |
|---|---:|---:|
| `flight_review-source` | 8 | 0 |
| `flight_review-app-image` | 265 | 207 |
| `flight_review-nginx-image` | 154 | 337 |
| `flight_review-certbot-image` | 1126 | 75 |
| `flight_review-browser-runtime` | 18 | 3 |
