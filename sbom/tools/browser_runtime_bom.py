#!/usr/bin/env python3
"""Emit a CycloneDX BOM for the browser-side runtime of Flight Review.

syft only sees what is on disk or in the image. Flight Review also pulls JS/CSS
from public CDNs at page-load time and calls external map/imagery services.
Those are part of the authorization boundary's data flows, so they are recorded
here from the Jinja templates in app/plot_app/templates.
"""
import argparse
import hashlib
import json
import uuid
from pathlib import Path

STATIC = "app/plot_app/static"
TPL = "app/plot_app/templates"

# (name, version, purl, supplier, license, delivery, url_or_path, loaded_by, sri)
COMPONENTS = [
    ("jquery", "3.1.0", "pkg:npm/jquery@3.1.0", "OpenJS Foundation", "MIT", "cdn",
     "https://ajax.aspnetcdn.com/ajax/jQuery/jquery-3.1.0.min.js", f"{TPL}/footer.html", False),
    ("jquery", "3.7.0", "pkg:npm/jquery@3.7.0", "OpenJS Foundation", "MIT", "cdn",
     "https://cdn.datatables.net/v/bs5/jq-3.7.0/dt-2.3.4/datatables.min.js", f"{TPL}/browse.html", True),
    ("datatables.net", "2.3.4", "pkg:npm/datatables.net@2.3.4", "SpryMedia Ltd", "MIT", "cdn",
     "https://cdn.datatables.net/v/bs5/jq-3.7.0/dt-2.3.4/datatables.min.js", f"{TPL}/browse.html", True),
    ("datatables.net-bs5", "2.3.4", "pkg:npm/datatables.net-bs5@2.3.4", "SpryMedia Ltd", "MIT", "cdn",
     "https://cdn.datatables.net/2.3.4/js/dataTables.bootstrap5.js", f"{TPL}/browse.html", False),
    ("bootstrap", "5.3.8", "pkg:npm/bootstrap@5.3.8", "The Bootstrap Authors", "MIT", "cdn",
     "https://cdn.jsdelivr.net/npm/bootstrap@5.3.8/dist/js/bootstrap.bundle.min.js", f"{TPL}/footer.html", False),
    ("bootstrap", "5.3.8", "pkg:npm/bootstrap@5.3.8", "The Bootstrap Authors", "MIT", "vendored",
     f"{STATIC}/js/bootstrap.min.js", "(unreferenced copy)", None),
    ("bootstrap", "5.3.8", "pkg:npm/bootstrap@5.3.8", "The Bootstrap Authors", "MIT", "vendored",
     f"{STATIC}/css/bootstrap.min.css", "(unreferenced copy)", None),
    ("bootswatch", "5.3.8", "pkg:npm/bootswatch@5.3.8", "Thomas Park", "MIT", "cdn",
     "https://cdn.jsdelivr.net/npm/bootswatch@5.3.8/dist/yeti/bootstrap.min.css", f"{TPL}/header.html", False),
    ("chosen-js", "1.8.3", "pkg:npm/chosen-js@1.8.3", "Harvest", "MIT", "cdn",
     "https://cdnjs.cloudflare.com/ajax/libs/chosen/1.8.3/chosen.jquery.min.js", f"{TPL}/footer.html", False),
    ("@fortawesome/fontawesome-free", "6.5.1", "pkg:npm/%40fortawesome/fontawesome-free@6.5.1", "Fonticons, Inc.",
     "MIT AND CC-BY-4.0 AND OFL-1.1", "cdn",
     "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/fontawesome.min.css", f"{TPL}/header.html", False),
    ("leaflet", "1.3.4", "pkg:npm/leaflet@1.3.4", "Vladimir Agafonkin", "BSD-2-Clause", "cdn",
     "https://unpkg.com/leaflet@1.3.4/dist/leaflet.js", f"{TPL}/header.html", True),
    ("leaflet-omnivore", "0.3.1", "pkg:npm/leaflet-omnivore@0.3.1", "Mapbox", "BSD-2-Clause", "cdn",
     "https://api.tiles.mapbox.com/mapbox.js/plugins/leaflet-omnivore/v0.3.1/leaflet-omnivore.min.js",
     f"{TPL}/header.html", False),
    ("cesium", "1.123.0", "pkg:npm/cesium@1.123.0", "Cesium GS, Inc.", "Apache-2.0", "vendored",
     f"{STATIC}/cesium/Build/Cesium/Cesium.js", f"{TPL}/3d.html", None),
    ("two.js", "0.7.0", "pkg:npm/two.js@0.7.0", "Jono Brandel", "MIT", "vendored",
     f"{STATIC}/js/two.min.js", f"{TPL}/3d.html, {TPL}/radio_controller.html", None),
    ("lightbox2", "2.7.1", "pkg:npm/lightbox2@2.7.1", "Lokesh Dhakar", "MIT", "vendored",
     f"{STATIC}/js/lightbox.min.js", "(unreferenced copy)", None),
    ("pace-js", "1.0.2", "pkg:npm/pace-js@1.0.2", "HubSpot", "MIT", "vendored",
     f"{STATIC}/js/pace.min.js", f"{TPL}/footer.html", None),
    ("bootstrap-filestyle", "2.1.0", "pkg:npm/bootstrap-filestyle@2.1.0", "Markus Vinicius da Silva Lima", "MIT",
     "vendored", f"{STATIC}/js/bootstrap-filestyle.min.js", f"{TPL}/footer.html", None),
    ("popper.js", None, "pkg:npm/popper.js", "Federico Zivolo", "MIT", "vendored",
     f"{STATIC}/js/popper.min.js", "(unreferenced copy; 1.x build, version string not embedded)", None),
    ("animate.css", None, "pkg:npm/animate.css", "Daniel Eden", "MIT", "vendored",
     f"{STATIC}/css/animate.min.css", f"{TPL}/header.html (version string not embedded)", None),
]

# External services the browser (or Cesium) contacts at runtime: these are
# system interconnections for the boundary diagram, not software components.
SERVICES = [
    ("Google Fonts", "https://fonts.googleapis.com", "Web font CSS (Play)", f"{TPL}/header.html"),
    ("Microsoft Ajax CDN", "https://ajax.aspnetcdn.com", "jQuery delivery", f"{TPL}/footer.html"),
    ("cdnjs (Cloudflare)", "https://cdnjs.cloudflare.com", "chosen, font-awesome delivery", f"{TPL}/header.html"),
    ("jsDelivr", "https://cdn.jsdelivr.net", "bootstrap, bootswatch delivery", f"{TPL}/header.html"),
    ("unpkg", "https://unpkg.com", "leaflet delivery", f"{TPL}/header.html"),
    ("DataTables CDN", "https://cdn.datatables.net", "datatables + jQuery 3.7.0 delivery", f"{TPL}/browse.html"),
    ("Mapbox CDN", "https://api.tiles.mapbox.com", "leaflet-omnivore delivery (protocol-relative URL in header.html)",
     f"{TPL}/header.html"),
    ("Mapbox Tiles API", "https://api.mapbox.com", "Map imagery (when mapbox_api_access_token configured)", f"{TPL}/index.html"),
    ("OpenStreetMap tile servers", "https://tile.openstreetmap.org", "Map imagery (default)", f"{TPL}/index.html"),
    ("Cesium ion", "https://api.cesium.com", "3D terrain/imagery (when cesium_api_key configured)", f"{TPL}/3d.html"),
    ("Bing Maps (via Cesium)", "https://dev.virtualearth.net", "Aerial imagery (when cesium_enable_bing_aerial)", f"{TPL}/3d.html"),
]


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", required=True)
    ap.add_argument("--timestamp", required=True)
    ap.add_argument("--version", required=True)
    ap.add_argument("--supplier", required=True)
    args = ap.parse_args()
    repo = Path(args.repo)

    components = []
    for i, (name, ver, purl, supplier, lic, delivery, ref, loaded_by, sri) in enumerate(COMPONENTS):
        comp = {
            "bom-ref": f"browser-{i}-{name.replace('@', '').replace('/', '-')}",
            "type": "library",
            "name": name,
            "supplier": {"name": supplier},
            "licenses": [{"expression": lic}] if " AND " in lic else [{"license": {"id": lic}}],
            "purl": purl,
            "properties": [
                {"name": "flight_review:delivery", "value": delivery},
                {"name": "flight_review:loaded_by", "value": loaded_by},
                {"name": "flight_review:language", "value": "javascript/css"},
            ],
        }
        if ver:
            comp["version"] = ver
        else:
            comp["properties"].append({"name": "flight_review:version_unverified", "value": "true"})
        if delivery == "cdn":
            comp["externalReferences"] = [{"type": "distribution", "url": ref}]
            comp["properties"].append({"name": "flight_review:subresource_integrity", "value": "present" if sri else "absent"})
        else:
            p = repo / ref
            comp["properties"].append({"name": "flight_review:path", "value": ref})
            if p.exists():
                comp["hashes"] = [{"alg": "SHA-256", "content": sha256(p)}]
        components.append(comp)

    services = []
    for i, (name, url, desc, loaded_by) in enumerate(SERVICES):
        services.append({
            "bom-ref": f"service-{i}",
            "name": name,
            "description": desc,
            "endpoints": [url],
            "authenticated": False,
            "x-trust-boundary": True,
            "data": [{"flow": "bi-directional", "classification": "public / unclassified map tiles and static assets"}],
            "properties": [{"name": "flight_review:loaded_by", "value": loaded_by}],
        })

    bom = {
        "$schema": "http://cyclonedx.org/schema/bom-1.5.schema.json",
        "bomFormat": "CycloneDX",
        "specVersion": "1.5",
        "serialNumber": f"urn:uuid:{uuid.uuid4()}",
        "version": 1,
        "metadata": {
            "timestamp": args.timestamp,
            "tools": {"components": [{"type": "application", "name": "browser_runtime_bom.py", "version": "1.0",
                                      "description": "hand-maintained inventory derived from app/plot_app/templates"}]},
            "component": {
                "bom-ref": "flight_review-browser-runtime",
                "type": "application",
                "name": "flight_review-browser-runtime",
                "version": args.version,
                "supplier": {"name": args.supplier},
                "description": "Client-side JavaScript/CSS loaded by the Flight Review web UI, from CDNs and vendored static files",
            },
        },
        "components": components,
        "services": services,
        "dependencies": [{"ref": "flight_review-browser-runtime",
                          "dependsOn": [c["bom-ref"] for c in components] + [s["bom-ref"] for s in services]}],
    }
    print(json.dumps(bom, indent=2))


if __name__ == "__main__":
    main()
