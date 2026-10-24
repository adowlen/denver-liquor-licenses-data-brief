"""Build stats.json and the neighborhood panel for the Denver liquor
licenses brief (2026-10-24).

Inputs:
- data/liquor_raw.geojson (live pull, code/pull_data.py)
- data/neighborhood_population.csv (ACS 2024 5-year B01003 population,
  area-weighted tract allocation, code/build_population.py)
- Machine Readable stack layers (read-only):
  layers/acs_neighborhood_units.parquet (ACS housing units denominator)
  layers/crime_neighborhood_panel.parquet (reported offenses panel,
  matched Jan 1-Oct 13 windows; the fusion comparison uses 2026)
  layers/neighborhoods_clean.parquet (statistical neighborhood
  polygons, for the point-in-polygon control and land areas)

Definitions:
- Analysis population for distribution: licenses with LIC_STATUS
  'LICENSE ISSUED - ACTIVE' (the register's in-force status). Pending
  (157) and delinquent (93) records are counted and disclosed, never
  folded into the density analysis.
- Neighborhood: the source NEIGHBORHOOD field. Where it is blank, the
  point-in-polygon assignment is used if the row's coordinates are
  real; rows whose coordinates are the source's placeholder values
  (two fixed points in southern California, used for some special
  events records) have no location and stay unassigned.
- Coordinates are 'valid' when inside a Denver bounding box
  (-105.15..-104.55 lon, 39.55..39.95 lat).
- License-class groups (derived; full mapping in stats.json):
  on-premises, off-premises retail, and event/add-on/administrative.
  The grouping follows the class names as filed in the register.
"""
import json, pathlib
from collections import Counter
import numpy as np
import pandas as pd
from shapely import wkb
from shapely.geometry import Point

ROOT = pathlib.Path(__file__).resolve().parent.parent
STACK = (pathlib.Path.home() / "workspace/goals/daily-civic-data-brief/"
         "hidden_files/stack/denver/layers")
ACTIVE = "LICENSE ISSUED - ACTIVE"
DENVER_BBOX = (-105.15, -104.55, 39.55, 39.95)

ON_PREMISES = {
    "LIQUOR - HOTEL AND RESTAURANT", "LIQUOR - HOTEL AND RESTAURANT AND CABARET",
    "LIQUOR - TAVERN AND CABARET", "LIQUOR - TAVERN", "LIQUOR - BEER & WINE",
    "LIQUOR - BREW PUB", "LIQUOR - CLUB", "LIQUOR - LODGING",
    "LIQUOR - ARTS", "LIQUOR - BREW PUB AND CABARET",
    "LIQUOR - ENTERTAINMENT AND CABARET",
    "LIQUOR - HOTEL AND RESTAURANT WITH OPTIONAL PREMISES AND CABARET",
    "LIQUOR - HOTEL AND RESTAURANT WITH OPTIONAL PREMISES",
    "LIQUOR - BEER & WINE AND CABARET", "LIQUOR - LODGING AND ENTERTAINMENT",
    "LIQUOR - BED & BREAKFAST", "LIQUOR - LODGING AND ENTERTAINMENT AND CABARET",
    "LIQUOR - VINTNER'S RESTAURANT", "LIQUOR - ENTERTAINMENT",
    "LIQUOR - LODGING AND CABARET", "LIQUOR - CAMPUS LIQUOR COMPLEX AND CABARET",
    "LIQUOR - CAMPUS LIQUOR COMPLEX", "LIQUOR - VINTNER'S RESTAURANT AND CABARET",
    "LIQUOR - DISTILLERY PUB", "LIQUOR - ART GALLERY",
    "LIQUOR - ART GALLERY PERMIT",
}
OFF_PREMISES = {
    "LIQUOR - FERMENTED MALT BEVERAGE", "LIQUOR - STORE",
    "LIQUOR - DRUG STORE", "LIQUOR - 3.2% BEER",
}


def class_group(cls):
    if cls in ON_PREMISES:
        return "on_premises"
    if cls in OFF_PREMISES:
        return "off_premises_retail"
    return "event_addon_admin"


def main():
    raw = json.loads((ROOT / "data" / "liquor_raw.geojson").read_text())
    feats = raw["features"]
    nb = pd.read_parquet(STACK / "neighborhoods_clean.parquet")
    nb["geometry"] = nb["geometry_wkb"].apply(wkb.loads)
    polys = dict(zip(nb["NBHD_NAME"], nb["geometry"]))

    rows = []
    agree = disagree = 0
    disagree_rows = []
    for f in feats:
        p = f["properties"]
        lon, lat = f["geometry"]["coordinates"]
        valid = (DENVER_BBOX[0] < lon < DENVER_BBOX[1]
                 and DENVER_BBOX[2] < lat < DENVER_BBOX[3])
        spatial = None
        if valid:
            pt = Point(lon, lat)
            for name, poly in polys.items():
                if poly.contains(pt):
                    spatial = name
                    break
        src = p["NEIGHBORHOOD"] or None
        if src and spatial:
            if src == spatial:
                agree += 1
            else:
                disagree += 1
                disagree_rows.append((p["BFN"], src, spatial))
        final = src or spatial
        rows.append({
            "bfn": p["BFN"], "class": p["LICENSES"], "status": p["LIC_STATUS"],
            "group": class_group(p["LICENSES"]),
            "src_neighborhood": src, "spatial_neighborhood": spatial,
            "neighborhood": final, "valid_coords": valid,
            "council_dist": p["COUNCIL_DIST"],
            "issue_ms": p["ORIGINAL_ISSUE_DATE"],
        })
    df = pd.DataFrame(rows)
    total = len(df)
    status_counter = Counter(df["status"])
    class_counter_all = Counter(df["class"])
    act = df[df["status"] == ACTIVE].copy()
    n_active = len(act)
    class_counter_active = Counter(act["class"])
    group_counter_active = Counter(act["group"])

    # ---- neighborhood panel
    pop = pd.read_csv(ROOT / "data" / "neighborhood_population.csv")
    units = pd.read_parquet(STACK / "acs_neighborhood_units.parquet")
    units = units.rename(columns={"acs_units_2020_2024": "housing_units"})
    crime = pd.read_parquet(STACK / "crime_neighborhood_panel.parquet")
    crime26 = crime[crime["window_year"] == 2026][
        ["neighborhood", "reports"]].rename(
        columns={"reports": "offense_reports_2026_window"})
    panel = pop.merge(units[["neighborhood", "housing_units"]],
                      on="neighborhood", how="left")
    cnt = act.groupby("neighborhood").size().rename("active_licenses")
    onc = act[act["group"] == "on_premises"].groupby(
        "neighborhood").size().rename("on_premises")
    offc = act[act["group"] == "off_premises_retail"].groupby(
        "neighborhood").size().rename("off_premises_retail")
    panel = (panel.set_index("neighborhood")
             .join(cnt).join(onc).join(offc)
             .join(crime26.set_index("neighborhood"))
             .fillna({"active_licenses": 0, "on_premises": 0,
                      "off_premises_retail": 0})
             .reset_index())
    panel["share_of_city_active_pct"] = (
        100 * panel["active_licenses"] / n_active).round(2)
    panel["per_1000_residents"] = (
        1000 * panel["active_licenses"]
        / panel["population_acs2024_5yr"]).round(2)
    panel["per_1000_units"] = (
        1000 * panel["active_licenses"] / panel["housing_units"]).round(2)
    panel["per_sq_mi"] = (
        panel["active_licenses"] / panel["area_sq_mi"]).round(2)
    panel["offenses_per_1000_residents"] = (
        1000 * panel["offense_reports_2026_window"]
        / panel["population_acs2024_5yr"]).round(2)
    panel = panel.sort_values("active_licenses", ascending=False)
    panel.to_csv(ROOT / "data" / "neighborhood_panel_liquor.csv", index=False)

    known = act[act["neighborhood"].notna()]
    alloc_pop = float(pop["population_acs2024_5yr"].sum())
    citywide_rate = 1000 * len(known) / alloc_pop

    def top(df_, col, n=10):
        d = df_.sort_values(col, ascending=False).head(n)
        return [[r.neighborhood, int(r.active_licenses),
                 float(getattr(r, "population_acs2024_5yr")),
                 float(getattr(r, col))] for r in d.itertuples()]

    top5 = panel.head(5)
    top10 = panel.head(10)
    conc = {
        "top5_count_share_pct": round(
            100 * top5["active_licenses"].sum() / n_active, 1),
        "top5_population_share_pct": round(
            100 * top5["population_acs2024_5yr"].sum() / alloc_pop, 1),
        "top10_count_share_pct": round(
            100 * top10["active_licenses"].sum() / n_active, 1),
        "top10_population_share_pct": round(
            100 * top10["population_acs2024_5yr"].sum() / alloc_pop, 1),
        "neighborhoods_with_zero_active": int(
            (panel["active_licenses"] == 0).sum()),
        "median_active_per_neighborhood": float(
            panel["active_licenses"].median()),
        "neighborhoods_at_or_below_5_active": int(
            (panel["active_licenses"] <= 5).sum()),
    }
    # Gini across the 78 neighborhoods (counts, unweighted)
    x = np.sort(panel["active_licenses"].to_numpy(dtype=float))
    n = len(x)
    gini = float((2 * np.arange(1, n + 1) * x).sum() / (n * x.sum())
                 - (n + 1) / n) if x.sum() else 0.0

    # ---- fusion: licenses vs reported offenses (2026 matched window)
    fus = panel.dropna(subset=["offense_reports_2026_window"]).copy()
    fus_big = fus[fus["population_acs2024_5yr"] >= 1000]
    def spearman(a, b):
        ra = pd.Series(a).rank().to_numpy()
        rb = pd.Series(b).rank().to_numpy()
        return float(np.corrcoef(ra, rb)[0, 1])
    fusion = {
        "spearman_all_neighborhoods": round(spearman(
            fus["per_1000_residents"],
            fus["offenses_per_1000_residents"]), 3),
        "spearman_pop_ge_1000": round(spearman(
            fus_big["per_1000_residents"],
            fus_big["offenses_per_1000_residents"]), 3),
        "n_neighborhoods": int(len(fus_big)),
        "top_quartile_both": sorted(
            fus_big[
                (fus_big["per_1000_residents"]
                 >= fus_big["per_1000_residents"].quantile(0.75))
                & (fus_big["offenses_per_1000_residents"]
                   >= fus_big["offenses_per_1000_residents"].quantile(0.75))
            ]["neighborhood"].tolist()),
        "license_rate_vs_unit_rate_rank_corr": round(spearman(
            panel["per_1000_residents"], panel["per_1000_units"]), 3),
    }

    # issue-date record (register migrated 2012-2014; see verification)
    from datetime import datetime, timezone
    def yr(ms):
        return (datetime.fromtimestamp(ms / 1000, timezone.utc).year
                if pd.notna(ms) else None)
    yrs = [y for y in (yr(ms) for ms in act["issue_ms"]) if y]
    issue = {
        "active_with_issue_date": len(yrs),
        "min_year": min(yrs), "max_year": max(yrs),
        "issued_2020_or_later": int(sum(1 for y in yrs if y >= 2020)),
        "issued_2020_or_later_pct": round(
            100 * sum(1 for y in yrs if y >= 2020) / len(yrs), 1),
        "bulk_load_2013_2014_all_statuses": int(sum(
            1 for ms in df["issue_ms"] if yr(ms) in (2013, 2014))),
    }

    stats = {
        "source_pull_date": "2026-10-23",
        "source_dataset": ("ODC_BUSN_LIQUORLICENSES_P (Denver Open Data, "
                           "ArcGIS FeatureServer layer 27)"),
        "total_records": total,
        "status_counter": dict(status_counter),
        "active_licenses": n_active,
        "active_with_neighborhood": int(len(known)),
        "active_without_neighborhood": int(n_active - len(known)),
        "active_placeholder_coords": int(
            ((act["valid_coords"] == False)).sum()),  # noqa: E712
        "class_counter_all": dict(class_counter_all.most_common()),
        "class_counter_active": dict(class_counter_active.most_common()),
        "class_groups_active": dict(group_counter_active),
        "class_group_mapping": {
            "on_premises": sorted(ON_PREMISES),
            "off_premises_retail": sorted(OFF_PREMISES),
            "event_addon_admin": "all remaining classes as filed",
        },
        "hotel_restaurant_family_active": int(sum(
            v for k, v in class_counter_active.items()
            if k.startswith("LIQUOR - HOTEL AND RESTAURANT"))),
        "neighborhood_control": {
            "source_vs_spatial_agree": agree,
            "source_vs_spatial_disagree": disagree,
            "disagreements": disagree_rows[:20],
        },
        "allocated_population": alloc_pop,
        "citywide_active_per_1000_residents": round(citywide_rate, 2),
        "concentration": conc,
        "gini_neighborhood_counts": round(gini, 3),
        "top_by_count": top(panel, "active_licenses"),
        "top_by_per_1000_residents": top(panel, "per_1000_residents"),
        "top_by_per_sq_mi": top(panel, "per_sq_mi"),
        "bottom_by_per_1000_residents": [
            [r.neighborhood, int(r.active_licenses),
             float(r.population_acs2024_5yr),
             float(r.per_1000_residents)]
            for r in panel.sort_values("per_1000_residents").head(8)
            .itertuples()],
        "council_district_active": dict(Counter(
            act["council_dist"].astype(str)).most_common()),
        "council_district_zero_records": int(
            (act["council_dist"].astype(str) == "0").sum()),
        "district_zero_all_unlocated": bool((
            act.loc[act["council_dist"].astype(str) == "0",
                    "valid_coords"] == False).all()),  # noqa: E712
        "median_per_1000_residents": round(float(
            panel["per_1000_residents"].median()), 2),
        "low_count_group": {
            "neighborhoods_at_or_below_5_active": int(
                (panel["active_licenses"] <= 5).sum()),
            "their_active_licenses": int(
                panel.loc[panel["active_licenses"] <= 5,
                          "active_licenses"].sum()),
            "their_population_share_pct": round(100 * panel.loc[
                panel["active_licenses"] <= 5,
                "population_acs2024_5yr"].sum() / alloc_pop, 1),
        },
        "group_shares_active_pct": {
            k: round(100 * v / n_active, 1)
            for k, v in group_counter_active.items()},
        "five_points_share_pct": round(100 * float(panel.loc[
            panel["neighborhood"] == "Five Points",
            "active_licenses"].iloc[0]) / n_active, 1),
        "fusion_crime": fusion,
        "top10_by_count": [
            [r.neighborhood, int(r.active_licenses),
             float(r.share_of_city_active_pct)]
            for r in panel.head(10).itertuples()],
        "offense_reports_2026_window_total": int(
            panel["offense_reports_2026_window"].sum()),
        "citywide_offenses_per_1000_residents_2026_window": round(
            1000 * panel["offense_reports_2026_window"].sum()
            / alloc_pop, 1),
        "named_neighborhood_splits": {
            r.neighborhood: {
                "active": int(r.active_licenses),
                "on_premises": int(r.on_premises),
                "off_premises_retail": int(r.off_premises_retail),
                "offenses_per_1000_residents": float(
                    r.offenses_per_1000_residents),
            } for r in panel.itertuples()
            if r.neighborhood in ("Five Points", "Union Station", "CBD",
                                  "DIA", "Highland", "Cherry Creek",
                                  "Montbello")},
        "issue_date_record": issue,
    }
    (ROOT / "stats.json").write_text(json.dumps(stats, indent=2))
    print("active", n_active, "known nbhd", len(known),
          "agree", agree, "disagree", disagree)
    print("citywide per 1000:", round(citywide_rate, 2))
    print("top count:", top(panel, "active_licenses", 5))
    print("top rate:", top(panel, "per_1000_residents", 8))
    print("concentration:", conc, "gini:", round(gini, 3))
    print("fusion:", fusion)


if __name__ == "__main__":
    main()
