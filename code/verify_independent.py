"""Independent verification for the Denver liquor licenses brief.

Separate implementation from code/build_stats.py: standard library only
(json, csv, statistics), no pandas, no shapely, and three figures are
recomputed from FRESH live queries against the ArcGIS service and
Census Reporter rather than from the builder's saved pull. Writes
data/verify_independent_output.json; the human-readable ledger is
verification-ledger-independent.md.
"""
import csv, json, pathlib, urllib.parse, urllib.request
from collections import Counter
from statistics import mean

ROOT = pathlib.Path(__file__).resolve().parent.parent
BASE = ("https://services1.arcgis.com/zdB7qR0BtYrg0Xpl/ArcGIS/rest/"
        "services/ODC_BUSN_LIQUORLICENSES_P/FeatureServer/27/query")
UA = {"User-Agent": "Mozilla/5.0 MachineReadable verify"}


def q(url, params):
    req = urllib.request.Request(
        url + "?" + urllib.parse.urlencode(params), headers=UA)
    with urllib.request.urlopen(req, timeout=90) as r:
        return json.loads(r.read())


def server_group(field, where):
    d = q(BASE, {"where": where, "groupByFieldsForStatistics": field,
                 "outStatistics": json.dumps([{
                     "statisticType": "count", "onStatisticField": "OBJECTID",
                     "outStatisticFieldName": "cnt"}]),
                 "resultRecordCount": 5000, "f": "json"})
    return {f["attributes"][field]: f["attributes"]["cnt"]
            for f in d["features"]}


def ranks(xs):
    order = sorted(range(len(xs)), key=lambda i: xs[i])
    r = [0.0] * len(xs)
    i = 0
    while i < len(xs):
        j = i
        while j + 1 < len(xs) and xs[order[j + 1]] == xs[order[i]]:
            j += 1
        avg = (i + j) / 2 + 1
        for k in range(i, j + 1):
            r[order[k]] = avg
        i = j + 1
    return r


def pearson(a, b):
    ma, mb = mean(a), mean(b)
    num = sum((x - ma) * (y - mb) for x, y in zip(a, b))
    den = (sum((x - ma) ** 2 for x in a) * sum((y - mb) ** 2 for y in b)) ** 0.5
    return num / den


def main():
    out = {}
    stats = json.loads((ROOT / "stats.json").read_text())

    # 1. Fresh live server counters vs stats.json
    live_status = server_group("LIC_STATUS", "1=1")
    out["live_status_counter"] = live_status
    out["status_matches_stats"] = (
        live_status == stats["status_counter"])
    live_total = q(BASE, {"where": "1=1", "returnCountOnly": "true",
                          "f": "json"})["count"]
    out["live_total"] = live_total

    # 2. Stdlib recount from the saved raw pull
    feats = json.loads((ROOT / "data" / "liquor_raw.geojson")
                       .read_text())["features"]
    props = [f["properties"] for f in feats]
    act = [p for p in props if p["LIC_STATUS"] == "LICENSE ISSUED - ACTIVE"]
    out["recount_total"] = len(props)
    out["recount_active"] = len(act)
    by_nb = Counter(p["NEIGHBORHOOD"] for p in act if p["NEIGHBORHOOD"])
    out["recount_active_with_source_neighborhood"] = sum(by_nb.values())
    out["recount_top5_by_count"] = by_nb.most_common(5)
    on = set(stats["class_group_mapping"]["on_premises"])
    off = set(stats["class_group_mapping"]["off_premises_retail"])
    groups = Counter("on" if p["LICENSES"] in on else
                     "off" if p["LICENSES"] in off else "other" for p in act)
    out["recount_groups"] = dict(groups)
    out["recount_hotel_restaurant_family"] = sum(
        1 for p in act if p["LICENSES"].startswith(
            "LIQUOR - HOTEL AND RESTAURANT"))

    # 3. Live server active-by-neighborhood vs the recount
    live_nb = server_group("NEIGHBORHOOD",
                           "LIC_STATUS='LICENSE ISSUED - ACTIVE'")
    live_nb = {k: v for k, v in live_nb.items() if k}
    out["live_vs_recount_nbhd_diffs"] = {
        k: (live_nb.get(k, 0), by_nb.get(k, 0))
        for k in set(live_nb) | set(by_nb)
        if live_nb.get(k, 0) != by_nb.get(k, 0)}

    # 4. Rates and concentration from the panel CSV, stdlib arithmetic
    panel = list(csv.DictReader(
        open(ROOT / "data" / "neighborhood_panel_liquor.csv")))
    alloc = sum(float(r["population_acs2024_5yr"]) for r in panel)
    assigned = sum(int(float(r["active_licenses"])) for r in panel)
    out["citywide_rate_recomputed"] = round(1000 * assigned / alloc, 2)
    cbd = next(r for r in panel if r["neighborhood"] == "CBD")
    out["cbd_rate_recomputed"] = round(
        1000 * float(cbd["active_licenses"])
        / float(cbd["population_acs2024_5yr"]), 2)
    by_count = sorted(panel, key=lambda r: -float(r["active_licenses"]))
    top5 = by_count[:5]
    out["top5_share_recomputed"] = round(
        100 * sum(float(r["active_licenses"]) for r in top5)
        / len(act), 1)
    out["top5_pop_share_recomputed"] = round(
        100 * sum(float(r["population_acs2024_5yr"]) for r in top5)
        / alloc, 1)
    rates = sorted(float(r["per_1000_residents"]) for r in panel)
    out["median_rate_recomputed"] = round(
        (rates[38] + rates[39]) / 2, 2) if len(rates) == 78 else None
    counts = sorted(int(float(r["active_licenses"])) for r in panel)
    n = len(counts)
    gini = ((2 * sum((i + 1) * v for i, v in enumerate(counts)))
            / (n * sum(counts)) - (n + 1) / n)
    out["gini_recomputed"] = round(gini, 3)

    # 5. Spearman by hand on the panel CSV
    fus = [r for r in panel
           if r["offense_reports_2026_window"]
           and float(r["population_acs2024_5yr"]) >= 1000]
    lr = ranks([float(r["per_1000_residents"]) for r in fus])
    orr = ranks([float(r["offenses_per_1000_residents"]) for r in fus])
    out["spearman_pop_ge_1000_recomputed"] = round(pearson(lr, orr), 3)

    # 6. County population: Census Reporter county geography direct read
    d = q("https://api.censusreporter.org/1.0/data/show/acs2024_5yr",
          {"table_ids": "B01003", "geo_ids": "05000US08031"})
    county = d["data"]["05000US08031"]["B01003"]["estimate"]["B01003001"]
    out["census_reporter_county_population"] = county
    out["tract_sum_from_build_log"] = json.loads(
        (ROOT / "data" / "population_build_log.json").read_text()
    )["county_population_tract_sum"]

    (ROOT / "data" / "verify_independent_output.json").write_text(
        json.dumps(out, indent=2))
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
