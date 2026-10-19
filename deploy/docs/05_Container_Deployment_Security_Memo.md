# Transmittal addendum — containerized deployment of Flight Review

**To:** Authorizing Official (AO); Information System Security Manager (ISSM)
**From:** Flight Review system owner / development team (`COG-GTM/flight_review`)
**Subject:** Kubernetes deployment package (Helm chart, namespace policy, rendered manifests) for the Flight Review web application — addendum to the SBOM transmittal (`sbom/docs/01_Transmittal_Memo_AO_ISSM.md`)
**References:** NIST SP 800-53 Rev 5 / 800-53B; NIST SP 800-190 (Application Container Security Guide); DISA Kubernetes STIG; DISA Container Platform SRG; Kubernetes Pod Security Standards; DoDI 8510.01; CNCF/DoD *DevSecOps Reference Design*

## 1. Purpose

The SBOM package establishes *what* software is in each Flight Review container. This addendum establishes *how* the application container is run — the identity it executes as, the privileges it holds, the network it can reach, the storage it can write, and the ceilings on its resource use — and provides those settings as reviewable, lintable, reproducible artifacts (`deploy/`). Together the two packages are the configuration-management and system-hardening evidence for the software layer of the SSP (CM-2, CM-6, CM-7, AC-6, SC-7).

## 2. Deployment boundary (Kubernetes)

| Component | Artifact | In Kubernetes boundary? | Notes |
|---|---|---|---|
| Application container | `app/Dockerfile` → `image.repository@image.digest` | **Yes** | Tornado + Bokeh server, ULog parsing, SQLite. Runs as UID 10001, read-only root FS |
| Persistent data | `PersistentVolumeClaim` `…-data` → `/opt/data` | Yes | SQLite DB, uploaded `.ulg` files, cached PX4 metadata, overview images |
| Configuration | `Secret` `…-config` (`config_user.ini`, optional ULge PEM) | Yes | Site values; may hold SMTP password / API keys, hence a Secret not a ConfigMap |
| Ingress / TLS | `Ingress` + platform Ingress controller + TLS Secret | Platform-provided | Replaces `nginx/Dockerfile` (`nginx:latest`) and `letsencrypt/Dockerfile` (`certbot/certbot`) |
| Network policy | `NetworkPolicy` (chart) + `default-deny-all` (namespace) | Yes | Requires a CNI that enforces NetworkPolicy (Calico, Cilium, …) |
| Admission | Namespace labels `pod-security.kubernetes.io/enforce: restricted` | Platform-provided | Pod Security Admission is built into Kubernetes ≥1.25 |

**Removed from the boundary relative to `docker-compose.prod.yml`:** the `nginx` reverse-proxy container (337 grype findings, 17 Critical in the SBOM baseline — none in nginx itself but in Debian libraries it carried) and the `certbot` sidecar (75 findings, 1 Critical). TLS termination and certificate lifecycle move to the platform's accredited Ingress controller and certificate service, which are inherited controls.

External interconnections (unchanged from the SBOM memo §2): browser-side CDNs and map tile providers; server-side HTTPS to `px4-travis.s3.amazonaws.com` for airframe / parameter / event metadata, and SMTP only if enabled.

## 3. What changed, and why it matters to the risk picture

| # | Compose baseline (`docker-compose.prod.yml`) | Kubernetes package | Finding / control addressed |
|---|---|---|---|
| 1 | App ran as **root**; `FROM ubuntu:noble` floating tag | `USER 10001`; base pinned `@sha256:68ee2200…`; `runAsNonRoot`, `allowPrivilegeEscalation: false`, all capabilities dropped, seccomp `RuntimeDefault` | Scan finding *"app container runs as root with an unpinned base image"*; AC-6, CM-7, SR-4(3); K8s STIG V-242414/V-242415 (non-root, no privileged) |
| 2 | `nginx:latest` and `certbot/certbot:latest` in boundary, unpinned | Not deployed; Ingress controller is an inherited platform control | Scan finding *"unpinned nginx base image"*; SBOM gap G1; removes 412 third-party findings from the system's own inventory |
| 3 | `http_protocol = http` default → delete-token links e-mailed over cleartext | `config.httpProtocol: https` default; `ingress.tls.enabled: true` | Scan finding *"default http_protocol=http sends delete-token links over cleartext"*; SC-8, SC-8(1) |
| 4 | Writable container filesystem | `readOnlyRootFilesystem: true`; only `/opt/data` (PVC) and `/tmp` (256 Mi tmpfs) writable | CM-7(2), SI-7; limits persistence of a web-stack RCE |
| 5 | Host network namespace exposure via published `80:443`; no egress control | Default-deny namespace; explicit ingress from Ingress controller on 5006; egress limited to DNS + public HTTPS (RFC 1918 excluded); SMTP opt-in by CIDR | SC-7, SC-7(5), SC-7(8); CORA lateral-movement indicator |
| 6 | No resource limits | Container requests/limits; namespace ResourceQuota + LimitRange | SC-5, SC-6; bounds the *client-controlled upload size* DoS finding's blast radius (the finding itself remains a code fix) |
| 7 | Implicit default service identity | Dedicated ServiceAccount, `automountServiceAccountToken: false` | AC-6(10), K8s STIG V-242381/V-242383 |
| 8 | Config via bind-mounted files | Config rendered into a Secret, mode 0440, checksum-annotated for rollout | SC-28, CM-3 |
| 9 | Nothing to lint | `helm lint --strict`, `kubeconform -strict`, `kube-linter` in CI; rendered manifests committed and drift-checked | CM-3(2), CM-6(1), SA-11 |

**Not changed by this package (code-level findings from the security scan remain open and are tracked separately):** reflected XSS on `/browse?search=`, stored XSS via `ver_sw_branch`, unauthenticated `/error_label` update, client-controlled `expected_size`, delete token in GET query string. Items 3–6 above reduce the impact or exposure of several of them but do not close them.

## 4. Residual risk and known limitations

1. **Single replica / SQLite.** `replicaCount: 1` with `Recreate`; availability depends on the platform rescheduling the pod and re-attaching the PVC. An HA data layer is out of scope for this package.
2. **Python dependencies still float** (SBOM gap G2) and dev tooling (`jupyter`, `pylint`) is still in the image (gap G3). The deployment package does not change the image contents; those are tracked POA&M items.
3. **Browser-side risk is untouched** — CDN scripts without SRI, EOL jQuery/leaflet (gaps G4/G5). Content-Security-Policy can be added at the Ingress controller as a compensating control; not included here because the correct policy depends on which CDNs the site permits.
4. **NetworkPolicy is only as good as the CNI.** `kind`'s default CNI does not enforce it; the policy was validated structurally and applied, not enforced, in local verification (§6). Production clusters must run an enforcing CNI.
5. **Egress to public HTTPS is broad** (`0.0.0.0/0` minus private ranges) because the PX4 metadata hosts are on a CDN with changing addresses. Sites with an egress proxy should route the three `config.*Url` values through it and narrow `networkPolicy.egress.https.cidrs`.
6. **Ingress annotations are controller-specific.** Defaults target ingress-nginx; other controllers need equivalent body-size / websocket timeout settings.
7. **Image provenance.** The chart binds to a digest but does not verify a signature; cosign/Sigstore policy admission is a platform-level control (SR-4(1), SR-11).

## 5. Requested decisions

| # | Decision | Recommendation |
|---|---|---|
| D1 | Accept the Kubernetes package as the authorized deployment configuration, superseding `docker-compose.prod.yml` for production | Accept |
| D2 | Accept residual risks 1–7 with the listed compensating controls / POA&M entries | Accept with POA&M for 2, 3, 7 |
| D3 | Direct that `image.digest` be mandatory in every environment's values file | Direct |
| D4 | Direct that `deploy/scripts/validate.sh` and `sbom/generate_sbom.sh` run on every release candidate | Direct |

## 6. Verification record

Static: `deploy/scripts/validate.sh` — `helm lint --strict` (default and kind values), `kubeconform -strict -kubernetes-version 1.32.0` on every rendered resource and namespace manifest, `kube-linter` default checks — all clean at the commit this package was delivered in.

Dynamic (developer workstation, `kind` v0.27 / Kubernetes v1.32.2): hardened image built from `app/Dockerfile`, namespace manifests applied, chart installed with `values-kind.yaml`, Pod admitted under the `restricted` Pod Security Standard and passed its readiness probe. A PX4 `.ulg` was uploaded via `kubectl port-forward` to the Service and its plot page rendered 29 plot sections with no internal error. Pod inspection confirmed UID 10001, empty capability sets (`CapEff`/`CapBnd` = 0), read-only root filesystem (`touch /opt/service/x` → "Read-only file system"), and writable `/opt/data` only (`logs.sqlite`, `log_files/`, `cache/` created there).

Outstanding: the Ingress object and `helm test` hook were schema-validated but not exercised live (the ingress-nginx controller did not schedule on the single-node kind cluster); NetworkPolicy enforcement on a production CNI; TLS at the Ingress.
