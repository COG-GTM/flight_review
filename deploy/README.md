# Flight Review — container deployment package for AO / ISSM review

Kubernetes packaging of the Flight Review web application
(`COG-GTM/flight_review`), delivered alongside the SBOM / RMF package in
[`../sbom/`](../sbom/README.md). The SBOM answers *what is in the containers*;
this directory answers *how they run* — identity, privileges, network reach,
storage, resource ceilings — in a form an assessor can lint, render, diff and
apply without trusting the author.

## Contents

| Path | What it is | Audience |
|---|---|---|
| `helm/flight-review/` | Helm 3 chart: Deployment, Service, Ingress, PVC, config Secret, NetworkPolicy, ServiceAccount, optional PDB, `helm test` hook | platform team, assessor |
| `helm/flight-review/values.yaml` | Hardened defaults — every knob documented in-line | ISSM, platform team |
| `helm/flight-review/values-kind.yaml` | Local verification overlay (kind + ingress-nginx); not for production | developer |
| `k8s/00-namespace.yaml` … `03-default-deny.yaml` | Namespace with Pod Security Admission `restricted`, ResourceQuota, LimitRange, namespace-wide default-deny NetworkPolicy | platform team |
| `k8s/rendered/` | `helm template` output with default values — plain YAML for sites without Helm and for line-by-line review | assessor |
| `scripts/render.sh` | Regenerates `k8s/rendered/` | — |
| `scripts/validate.sh` | `helm lint --strict` → `kubeconform -strict` → `kube-linter`; same checks run in CI (`.github/workflows/helm.yml`) | assessor |
| `docs/05_Container_Deployment_Security_Memo.md` | Transmittal addendum: deployment boundary, what changed from the docker-compose baseline, residual risk, requested decisions | AO, ISSM |
| `docs/06_Container_Platform_Control_Mapping.md` | NIST SP 800-53 Rev 5 + Kubernetes STIG / Container Platform SRG mapping, control by control, with the exact manifest line that implements each | ISSM, ISSO, assessor |

## Hardened posture (defaults)

* **Identity** — container runs as UID/GID 10001 (`app/Dockerfile` `USER`, enforced again by `runAsNonRoot`/`runAsUser`); dedicated ServiceAccount with `automountServiceAccountToken: false`.
* **Privileges** — `allowPrivilegeEscalation: false`, `capabilities.drop: [ALL]`, `readOnlyRootFilesystem: true`, `seccompProfile: RuntimeDefault`; namespace enforces Pod Security Standard **restricted**.
* **Network** — namespace default-deny; the chart's NetworkPolicy permits only ingress from the Ingress controller on 5006 and egress to cluster DNS and public HTTPS (PX4 metadata URLs), with RFC 1918 / link-local ranges excluded. SMTP egress is opt-in with an explicit CIDR.
* **Transport** — TLS terminates at the Ingress (`ingress.tls`), replacing the compose-era `nginx:latest` + `certbot` sidecars, which are no longer in the Kubernetes boundary. `http_protocol = https` so generated links and e-mails are never cleartext.
* **Storage** — one PVC at `/opt/data` (SQLite DB, uploaded logs, cache); `/tmp` is a size-limited tmpfs; nothing else is writable.
* **Supply chain** — base image pinned by digest in `app/Dockerfile`; `image.digest` binds the running container to the SBOM in `sbom/`.
* **Capacity** — container requests/limits, namespace ResourceQuota and LimitRange; `replicaCount: 1` with `Recreate` because SQLite is single-writer.

## Deploy

```
cd ~/flight_review
docker build -t registry.example.mil/flight-review/app:2026.10 ./app
docker push registry.example.mil/flight-review/app:2026.10
kubectl apply -f deploy/k8s/00-namespace.yaml -f deploy/k8s/01-resourcequota.yaml -f deploy/k8s/02-limitrange.yaml -f deploy/k8s/03-default-deny.yaml
helm upgrade --install flight-review deploy/helm/flight-review -n flight-review --set domain=flight-review.example.mil --set image.digest=sha256:<digest from docker push>
helm test flight-review -n flight-review
```

Site-specific secrets (SMTP password, Cesium/Mapbox keys, ULge private key)
go in `secrets.*` through `--set-file` / a sealed values file, or pre-create a
Secret holding `config_user.ini` and set `secrets.existingSecret`.

## Validate (what CI and the assessor run)

```
cd ~/flight_review
./deploy/scripts/validate.sh
```

Requires `helm`, `kubeconform`, `kube-linter`. Local end-to-end verification
on `kind` is described in `docs/05_Container_Deployment_Security_Memo.md` §6.

## Relationship to docker-compose

`docker-compose*.yml`, `nginx/` and `letsencrypt/` remain for single-host
deployments and are still built by CI. The Kubernetes package is the
accreditable path; the compose path inherits only the `app/Dockerfile`
hardening (digest pin, non-root). A bind-mounted `./data` directory must now be
writable by UID 10001 (`sudo chown -R 10001:10001 data`).
