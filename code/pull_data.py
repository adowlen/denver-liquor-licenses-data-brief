"""Pull the full Denver liquor license register from the live ArcGIS service.

Source: ODC_BUSN_LIQUORLICENSES_P, FeatureServer layer 27 (id resolved at
pull time from the service root), City and County of Denver Open Data
Catalog, published from Denver Excise and Licenses records.
https://services1.arcgis.com/zdB7qR0BtYrg0Xpl/ArcGIS/rest/services/ODC_BUSN_LIQUORLICENSES_P/FeatureServer

The register is small (about 2,200 rows), so the pull is a full row pull
with geometry, paginated by OBJECTID, saved verbatim to
data/liquor_raw.geojson. Server-side counters (status, license class,
neighborhood, status x neighborhood for active licenses) are saved to
data/raw_aggregates.json so the Section 10 audit and the independent
verification pass can compare server aggregates against the local pull.
"""
import json, pathlib, urllib.parse, urllib.request
from collections import Counter

ROOT = ("https://services1.arcgis.com/zdB7qR0BtYrg0Xpl/ArcGIS/rest/services/"
        "ODC_BUSN_LIQUORLICENSES_P/FeatureServer")
PAGE = 1000


def q(url, params):
    full = url + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(full, headers={"User-Agent": "MachineReadable pull"})
    with urllib.request.urlopen(req, timeout=90) as r:
        return json.loads(r.read())


def resolve_layer():
    d = q(ROOT, {"f": "json"})
    for lyr in d.get("layers", []):
        if lyr["name"] == "BUSN_LIQUORLICENSES_P":
            return lyr["id"]
    raise SystemExit("BUSN_LIQUORLICENSES_P layer not found in service root")


def count(base, where):
    return q(base + "/query", {"where": where, "returnCountOnly": "true",
                               "f": "json"})["count"]


def group(base, field, where="1=1"):
    d = q(base + "/query",
          {"where": where, "groupByFieldsForStatistics": field,
           "outStatistics": json.dumps([{"statisticType": "count",
                                         "onStatisticField": "OBJECTID",
                                         "outStatisticFieldName": "cnt"}]),
           "orderByFields": "cnt DESC", "resultRecordCount": 5000, "f": "json"})
    out = [[f["attributes"][field], f["attributes"]["cnt"]]
           for f in d.get("features", [])]
    return out


def main():
    root = pathlib.Path(__file__).resolve().parent.parent
    lid = resolve_layer()
    base = f"{ROOT}/{lid}"
    meta = q(base, {"f": "json"})
    total = count(base, "1=1")
    feats, offset = [], 0
    while True:
        d = q(base + "/query",
              {"where": "1=1", "outFields": "*", "returnGeometry": "true",
               "outSR": 4326, "orderByFields": "OBJECTID ASC",
               "resultOffset": offset, "resultRecordCount": PAGE, "f": "geojson"})
        batch = d.get("features", [])
        feats.extend(batch)
        if len(batch) < PAGE:
            break
        offset += PAGE
    assert len(feats) == total, (len(feats), total)
    (root / "data" / "liquor_raw.geojson").write_text(
        json.dumps({"type": "FeatureCollection", "features": feats}))
    status = group(base, "LIC_STATUS")
    classes = group(base, "LICENSES")
    agg = {
        "layer_id": lid,
        "service_last_edit_ms": (meta.get("editingInfo") or {}).get("lastEditDate"),
        "total_records": total,
        "pulled_records": len(feats),
        "status_counter": status,
        "license_class_counter": classes,
        "neighborhood_counter_all": group(base, "NEIGHBORHOOD"),
        "active_count": count(base, "LIC_STATUS='LICENSE ISSUED - ACTIVE'"),
        "active_by_neighborhood": group(
            base, "NEIGHBORHOOD", "LIC_STATUS='LICENSE ISSUED - ACTIVE'"),
        "active_by_class": group(
            base, "LICENSES", "LIC_STATUS='LICENSE ISSUED - ACTIVE'"),
        "active_by_council_dist": group(
            base, "COUNCIL_DIST", "LIC_STATUS='LICENSE ISSUED - ACTIVE'"),
    }
    (root / "data" / "raw_aggregates.json").write_text(json.dumps(agg, indent=2))
    (root / "data" / "pull_log.json").write_text(json.dumps({
        "dataset": "ODC_BUSN_LIQUORLICENSES_P",
        "layer_id_resolved": lid,
        "service_url": base,
        "total_records": total, "pulled_records": len(feats),
        "status_counter_local": Counter(
            f["properties"]["LIC_STATUS"] for f in feats).most_common(),
        "service_last_edit_ms": agg["service_last_edit_ms"],
    }, indent=2))
    print("layer", lid, "total", total, "pulled", len(feats))
    print("status", status)


if __name__ == "__main__":
    main()
