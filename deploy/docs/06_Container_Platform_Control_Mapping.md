# Container platform control mapping — NIST SP 800-53 Rev 5, Kubernetes STIG, Container Platform SRG

Which controls the deployment package in `deploy/` implements (**I**), supports with evidence (**S**), or leaves as an inherited platform control (**P**) or gap (**G**). Assessment procedures are from SP 800-53A Rev 5. STIG identifiers are DISA Kubernetes STIG (V2) rule IDs where the requirement applies to workload manifests rather than the control plane; CP-SRG = Container Platform SRG. File references are to this repository.

## 1. Access control / least privilege

| Control | Title | Status | Implementation / evidence |
|---|---|---|---|
| AC-3 | Access Enforcement | S | Namespace isolation; Pod Security Admission `restricted` (`deploy/k8s/00-namespace.yaml`) rejects any manifest that escalates privilege |
| AC-6 | Least Privilege | I | `app/Dockerfile` `USER 10001:10001`; `podSecurityContext.runAsNonRoot/runAsUser/runAsGroup` and `containerSecurityContext` (`values.yaml`, rendered in `deployment.yaml`). K8s STIG V-242414 (non-root), V-242415 (no privileged), CP-SRG SRG-APP-000342 |
| AC-6(2) | Non-privileged access for non-security functions | I | No `privileged`, `hostPID`, `hostNetwork`, `hostIPC`, host paths; `capabilities.drop: [ALL]` |
| AC-6(10) | Prohibit non-privileged users from executing privileged functions | I | `allowPrivilegeEscalation: false`; `automountServiceAccountToken: false` on both ServiceAccount and Pod — the app has no API-server identity to abuse. K8s STIG V-242381 |
| AC-17 / AC-17(2) | Remote Access / cryptographic protection | I / P | Only path in is the Ingress; TLS at Ingress (`ingress.tls`), certificate supplied by the platform |

## 2. Configuration management

| Control | Title | Status | Implementation / evidence |
|---|---|---|---|
| CM-2 | Baseline Configuration | I | The chart + `values.yaml` + `deploy/k8s/*.yaml` *is* the configuration baseline; rendered copy in `deploy/k8s/rendered/` is drift-checked by `validate.sh`. Image bound by `image.digest` to the SBOM in `sbom/GENERATION_RECORD.md` |
| CM-2(2) | Automation support | I | `render.sh`, `validate.sh`, CI workflow `.github/workflows/helm.yml` |
| CM-3 / CM-3(2) | Change control / test, validate, document | I | Every chart change is a reviewed PR; CI lint + schema + policy checks must pass; `checksum/config` annotation forces a controlled rollout when configuration changes |
| CM-5 | Access Restrictions for Change | P | Cluster RBAC on the namespace is a platform control; the chart requests no RBAC objects |
| CM-6 / CM-6(1) | Configuration Settings / automated enforcement | I | Hardened defaults in `values.yaml`; PSA `restricted`, LimitRange and ResourceQuota enforce them even if a values override drops them. Remaining gap: Python package pinning (SBOM gap G2) |
| CM-7 / CM-7(1) | Least Functionality | I / G | Single process (`run.sh` → `serve.py`); no shell service, no extra ports. Gap: dev tooling in the image (SBOM gap G3) |
| CM-7(2) | Prevent program execution | S | `readOnlyRootFilesystem: true`; `/tmp` is `noexec`-equivalent tmpfs by platform default; `PYTHONDONTWRITEBYTECODE=1` |
| CM-8 | System Component Inventory | S | SBOM package in `sbom/`; chart `annotations.flightreview.cog-gtm.io/sbom` links the two |
| CM-14 | Signed Components | G / P | Digest pinning only; signature verification (cosign policy) is a platform admission control |

## 3. System and communications protection

| Control | Title | Status | Implementation / evidence |
|---|---|---|---|
| SC-5 | Denial-of-Service Protection | S | Container `resources.limits`; `ResourceQuota` (`01-resourcequota.yaml`), `LimitRange` (`02-limitrange.yaml`); Ingress `proxy-body-size: 100m`; `/tmp` size-limited. Application-level upload-size fix tracked separately |
| SC-6 | Resource Availability | I | Requests/limits and quota as above; `startupProbe` prevents restart loops during cold start |
| SC-7 | Boundary Protection | I | `03-default-deny.yaml` denies all ingress/egress in the namespace; chart `networkpolicy.yaml` permits only Ingress-controller → app:5006, app → kube-dns:53, app → public HTTPS:443 (RFC 1918, 172.16/12, 169.254/16 excluded). K8s STIG V-242417 (namespaces), CP-SRG SRG-APP-000038 |
| SC-7(5) | Deny by default / allow by exception | I | Same |
| SC-7(8) | Route traffic to authenticated proxy servers | S | Egress CIDRs are values; sites with an egress proxy narrow `networkPolicy.egress.https.cidrs` |
| SC-8 / SC-8(1) | Transmission Confidentiality and Integrity | I / P | `config.httpProtocol: https` makes every generated link (including delete-token e-mails) HTTPS; TLS at Ingress. In-cluster hop Ingress → pod is plaintext — mesh/mTLS is a platform option |
| SC-12 / SC-13 | Key management / cryptographic protection | P | Certificates from the platform's certificate service (cert-manager or enterprise CA). ULge private key, if used, is mounted read-only from the config Secret (mode 0440) |
| SC-28 / SC-28(1) | Protection of Information at Rest | S / P | Configuration in a Secret (encrypted at rest if the cluster enables EncryptionConfiguration — platform); PVC encryption is the storage class's property |
| SC-39 | Process Isolation | I | seccomp `RuntimeDefault`; dropped capabilities; no host namespaces. K8s STIG V-242435 |

## 4. System and information integrity / audit

| Control | Title | Status | Implementation / evidence |
|---|---|---|---|
| SI-2 | Flaw Remediation | S | Rebuilding the image and bumping `image.digest` is the remediation mechanism; SBOM rescan per `sbom/README.md` |
| SI-4 | System Monitoring | P | Liveness/readiness/startup probes emit events; container stdout is collected by the platform logging stack. K8s STIG V-242402 (audit) is control-plane |
| SI-7 / SI-7(1) | Software, Firmware, and Information Integrity | S | Immutable, digest-pinned image; read-only root FS means any runtime change to the application tree fails rather than persisting |
| SI-10 | Information Input Validation | G | Application-level (XSS, upload size findings) — not a deployment control |
| AU-2 / AU-12 | Event logging | S / P | Tornado access log to stdout; Ingress controller access log carries client IP (`X-Forwarded-For` honoured via `--use-xheaders`) |

## 5. Supply chain

| Control | Title | Status | Implementation / evidence |
|---|---|---|---|
| SR-3 | Supply Chain Controls and Processes | S | `image.repository` points at the accredited registry; `imagePullSecrets` supported; no public-registry references in the chart |
| SR-4 / SR-4(3) | Provenance / validate as genuine | I / G | Base image digest-pinned in `app/Dockerfile`; deployed image digest-pinned via `image.digest`. Gap: signature verification (see CM-14) |
| SR-11 | Component Authenticity | G / P | As CM-14 |
| SA-10 | Developer Configuration Management | I | Chart versioned (`Chart.yaml` `version`), reviewed via PR, validated in CI |
| SA-11 | Developer Testing and Evaluation | I | `helm test` hook (`templates/tests/test-connection.yaml`) runs a non-root, read-only probe inside the cluster; static validation in CI |

## 6. NIST SP 800-190 container-specific risks

| 800-190 § | Risk | Countermeasure here |
|---|---|---|
| 3.1 Image risks | Vulnerabilities, configuration defects, embedded secrets, untrusted images | SBOM + grype baseline (`sbom/`); non-root `USER`; no secrets in the image (config is a mounted Secret); digest pinning |
| 3.2 Registry risks | Insecure connections, stale images | `image.repository` = accredited registry; digest pin makes staleness explicit |
| 3.3 Orchestrator risks | Unbounded admin access, poor network separation, mixed sensitivity workloads | Dedicated namespace; no RBAC requested; default-deny NetworkPolicy; PSA `restricted` |
| 3.4 Container risks | Runtime vulnerabilities, unbounded network access, insecure runtime config, rogue containers | seccomp; capabilities dropped; read-only FS; egress policy; probes |
| 3.5 Host OS risks | Shared kernel, large attack surface | Inherited; no host namespaces or host paths requested |

## 7. Gaps summary (POA&M candidates added by this package)

| # | Gap | Controls | Suggested milestone |
|---|---|---|---|
| K1 | No image signature verification at admission | CM-14, SR-4(1), SR-11 | Sign in CI (`cosign sign`), enforce with Kyverno/Sigstore policy-controller |
| K2 | In-cluster hop Ingress → pod is plaintext | SC-8 | Service mesh mTLS or Ingress backend TLS, per platform standard |
| K3 | Broad public-HTTPS egress | SC-7(8) | Route PX4 metadata URLs via egress proxy; narrow CIDRs |
| K4 | Single replica | CP-9/CP-10 | Only if the system's availability categorization requires it; needs a non-SQLite data layer |
| K5 | No Content-Security-Policy for CDN assets | SA-9, SI-7 | Add CSP at the Ingress once the CDN allow-list is decided (ties to SBOM gaps G4/G5) |
