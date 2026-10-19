#!/usr/bin/env bash
# Regenerates the Flight Review SBOM package (sbom/) from the current checkout.
#
# Produces, per deployable artifact: CycloneDX 1.x JSON + SPDX 2.3 JSON SBOMs,
# a grype vulnerability report, OpenVEX skeleton, human-readable inventory,
# a system-level CycloneDX manifest that links every sub-BOM, and SHA256SUMS.
#
# Requirements: docker (compose v2), syft, grype, jq, python3, git.
# Env knobs:    SKIP_BUILD=1  reuse already-built images instead of rebuilding
#               SBOM_SUPPLIER override the supplier string recorded in the BOMs
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
OUT="$REPO_ROOT/sbom"
cd "$REPO_ROOT"

for tool in docker syft grype jq python3 git; do
    command -v "$tool" >/dev/null 2>&1 || { echo "missing required tool: $tool" >&2; exit 1; }
done

GIT_SHA="$(git rev-parse HEAD)"
GIT_SHORT="$(git rev-parse --short HEAD)"
GIT_DATE="$(git log -1 --format=%cI)"
GIT_REMOTE="$(git remote get-url origin 2>/dev/null | sed -E 's#.*github.com/##; s#\.git$##')"
TS="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
SUPPLIER="${SBOM_SUPPLIER:-PX4 Autopilot Project (upstream); COG-GTM (fork maintainer)}"

export COMPOSE_PROJECT_NAME=flight_review
# Package-level BOMs only; per-file entries quadruple the size without adding
# anything an AO/ISSM reviews.
export SYFT_FILE_METADATA_SELECTION=none

APP_IMAGE="flight_review-flight_review_app:latest"
NGINX_IMAGE="flight_review-nginx:latest"
CERTBOT_IMAGE="flight_review-certbot:latest"

if [ "${SKIP_BUILD:-0}" != "1" ]; then
    echo "==> building deployable images (docker-compose.prod.yml)"
    docker compose -f docker-compose.prod.yml build
fi

mkdir -p "$OUT/cyclonedx" "$OUT/spdx" "$OUT/vulnerability" "$OUT/inventory"
rm -f "$OUT"/cyclonedx/*.json "$OUT"/spdx/*.json "$OUT"/vulnerability/*.json "$OUT"/vulnerability/*.txt "$OUT"/inventory/*.md

scan() {
    local name="$1" target="$2" version="$3"; shift 3
    echo "==> syft $name ($target)"
    syft scan "$target" "$@" \
        --source-name "$name" --source-version "$version" \
        -o "cyclonedx-json@1.5=$OUT/cyclonedx/$name.cdx.json" \
        -o "spdx-json=$OUT/spdx/$name.spdx.json" -q
    # syft's --source-supplier stamps every third-party component with the same
    # supplier, which misstates the NTIA "supplier" element; set it on the
    # described artifact only and leave component publishers as discovered.
    local tmp="$OUT/cyclonedx/$name.cdx.json.tmp"
    jq --arg s "$SUPPLIER" '.metadata.supplier = {name: $s} | .metadata.component.supplier = {name: $s}' \
        "$OUT/cyclonedx/$name.cdx.json" > "$tmp" && mv "$tmp" "$OUT/cyclonedx/$name.cdx.json"
    tmp="$OUT/spdx/$name.spdx.json.tmp"
    jq --arg s "$SUPPLIER" '.creationInfo.creators += ["Organization: " + $s]' \
        "$OUT/spdx/$name.spdx.json" > "$tmp" && mv "$tmp" "$OUT/spdx/$name.spdx.json"
}

scan flight_review-source "dir:$REPO_ROOT" "$GIT_SHORT" \
    --exclude './.venv/**' --exclude './data/**' --exclude './screenshots/**' \
    --exclude './letsencrypt/**' --exclude './app/private_key/**' --exclude './sbom/**'
scan flight_review-app-image     "docker:$APP_IMAGE"     "$GIT_SHORT"
scan flight_review-nginx-image   "docker:$NGINX_IMAGE"   "$GIT_SHORT"
scan flight_review-certbot-image "docker:$CERTBOT_IMAGE" "$GIT_SHORT"

echo "==> browser-runtime BOM (CDN-delivered + vendored JS/CSS, external services)"
python3 "$OUT/tools/browser_runtime_bom.py" --repo "$REPO_ROOT" --timestamp "$TS" \
    --version "$GIT_SHORT" --supplier "$SUPPLIER" \
    > "$OUT/cyclonedx/flight_review-browser-runtime.cdx.json"

echo "==> grype"
grype db update -q >/dev/null 2>&1 || echo "warning: grype db update failed, using cached db" >&2
for bom in "$OUT"/cyclonedx/*.cdx.json; do
    name="$(basename "$bom" .cdx.json)"
    grype "sbom:$bom" -o json --file "$OUT/vulnerability/$name.grype.json" -q
    grype "sbom:$bom" -o table --file "$OUT/vulnerability/$name.grype.txt" -q || true
done

image_id() { docker image inspect --format '{{.Id}}' "$1"; }
base_digest() { docker image inspect --format '{{index .RepoDigests 0}}' "$1" 2>/dev/null || echo "n/a"; }
# Base-image digests are only meaningful when resolved right after the build
# that consumed them. With SKIP_BUILD=1 the local base tags may have moved on,
# so carry the digest forward from the previous record if it describes the
# same image ID, and otherwise say so rather than report a current tag.
PREV="$OUT/generation.json"
base_for() {
    local key="$1" image="$2" tag="$3"
    if [ "${SKIP_BUILD:-0}" != "1" ]; then base_digest "$tag"; return; fi
    if [ -f "$PREV" ] && [ "$(jq -r --arg k "$key" '.images[$k].id // ""' "$PREV")" = "$(image_id "$image")" ]; then
        jq -r --arg k "$key" '.images[$k].base_digest' "$PREV"; return
    fi
    echo "n/a (image reused with SKIP_BUILD=1; base provenance not recorded at build time)"
}
APP_BASE="$(base_for app "$APP_IMAGE" ubuntu:noble)"
NGINX_BASE="$(base_for nginx "$NGINX_IMAGE" nginx:latest)"
CERTBOT_BASE="$(base_for certbot "$CERTBOT_IMAGE" certbot/certbot:latest)"

jq -n \
    --arg ts "$TS" --arg sha "$GIT_SHA" --arg short "$GIT_SHORT" --arg gitdate "$GIT_DATE" \
    --arg repo "$GIT_REMOTE" --arg supplier "$SUPPLIER" \
    --arg syft "$(syft version -o json | jq -r .version)" \
    --arg grype "$(grype version -o json | jq -r .version)" \
    --arg grypedb "$(grype db status -o json 2>/dev/null | jq -r '.built // .Built // "unknown"')" \
    --arg app_id "$(image_id "$APP_IMAGE")" --arg nginx_id "$(image_id "$NGINX_IMAGE")" \
    --arg certbot_id "$(image_id "$CERTBOT_IMAGE")" \
    --arg ubuntu "$APP_BASE" --arg nginx_base "$NGINX_BASE" --arg certbot_base "$CERTBOT_BASE" \
    --argjson rebuilt "$([ "${SKIP_BUILD:-0}" != "1" ] && echo true || echo false)" \
    '{generated_at:$ts, repository:$repo, git_commit:$sha, git_commit_short:$short, git_commit_date:$gitdate,
      supplier:$supplier, images_rebuilt:$rebuilt,
      tools:{syft:$syft, grype:$grype, grype_db_built:$grypedb},
      images:{app:{ref:"'"$APP_IMAGE"'", id:$app_id, base:"ubuntu:noble", base_digest:$ubuntu},
              nginx:{ref:"'"$NGINX_IMAGE"'", id:$nginx_id, base:"nginx:latest", base_digest:$nginx_base},
              certbot:{ref:"'"$CERTBOT_IMAGE"'", id:$certbot_id, base:"certbot/certbot:latest", base_digest:$certbot_base}}}' \
    > "$OUT/generation.json"

echo "==> reports, system manifest, OpenVEX skeleton"
python3 "$OUT/tools/build_reports.py" --out "$OUT"

echo "==> checksums"
(cd "$OUT" && find . -type f ! -name 'SHA256SUMS*' ! -path './tools/*' ! -path './dist/*' | sort | xargs sha256sum > SHA256SUMS.tmp && mv SHA256SUMS.tmp SHA256SUMS)

echo "done: $OUT"
