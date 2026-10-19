#!/usr/bin/env bash
# Static validation an assessor can re-run: helm lint, schema validation of the
# rendered manifests (kubeconform), and policy lint (kube-linter). Exit code is
# non-zero on any failure. KUBE_VERSION selects the API schemas.
set -euo pipefail
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
CHART="$REPO_ROOT/deploy/helm/flight-review"
KUBE_VERSION="${KUBE_VERSION:-1.32.0}"
TMP="$(mktemp -d)"; trap 'rm -rf "$TMP"' EXIT

for tool in helm kubeconform kube-linter; do
    command -v "$tool" >/dev/null 2>&1 || { echo "missing required tool: $tool" >&2; exit 1; }
done

echo "==> helm lint"
helm lint --strict "$CHART"
helm lint --strict "$CHART" -f "$CHART/values-kind.yaml"

echo "==> helm template (default values)"
helm template flight-review "$CHART" -n flight-review > "$TMP/default.yaml"
echo "==> helm template (kind overlay)"
helm template flight-review "$CHART" -n flight-review -f "$CHART/values-kind.yaml" > "$TMP/kind.yaml"

echo "==> kubeconform (Kubernetes $KUBE_VERSION, strict)"
kubeconform -strict -summary -kubernetes-version "$KUBE_VERSION" \
    "$TMP/default.yaml" "$TMP/kind.yaml" "$REPO_ROOT"/deploy/k8s/0*.yaml

echo "==> kube-linter"
kube-linter lint "$TMP/default.yaml" "$REPO_ROOT"/deploy/k8s/0*.yaml

if [ -d "$REPO_ROOT/deploy/k8s/rendered" ]; then
    echo "==> rendered manifests are current"
    # Compare ignoring the generation comment header.
    RENDER_TMP="$(mktemp -d)"
    OUT_BACKUP="$REPO_ROOT/deploy/k8s/rendered"
    cp -r "$OUT_BACKUP" "$RENDER_TMP/committed"
    "$REPO_ROOT/deploy/scripts/render.sh" >/dev/null
    if ! diff -r -q -x README.md "$RENDER_TMP/committed" "$OUT_BACKUP" >/dev/null; then
        echo "deploy/k8s/rendered is stale — run deploy/scripts/render.sh and commit" >&2
        rm -rf "$OUT_BACKUP"; mv "$RENDER_TMP/committed" "$OUT_BACKUP"
        exit 1
    fi
    rm -rf "$OUT_BACKUP"; mv "$RENDER_TMP/committed" "$OUT_BACKUP"
    rm -rf "$RENDER_TMP"
fi
echo "OK"
