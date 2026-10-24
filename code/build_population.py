"""Build the neighborhood population denominator for the liquor brief.

Method: identical to the one the Machine Readable stack used for its
housing-unit denominator (layers/acs_neighborhood_units.parquet), applied
to population instead of units.

- Values: US Census Bureau ACS 2024 5-year estimates, table B01003
  (total population), tract level, read from Census Reporter
  (release acs2024_5yr) for all tracts in Denver County (05000US08031).
  The Census API itself now requires a key; Census Reporter serves the
  same published ACS table.
- Geometries: census tract polygons from the Census Bureau TIGERweb
  service (tigerWMS_Current, Census Tracts layer 8), and Denver
  statistical neighborhood polygons from the stack layer
  stack/denver/layers/neighborhoods_clean.parquet.
- Allocation: each tract's population is distributed to neighborhoods
  in proportion to land-area overlap (area weighting), computed in
  EPSG:26913 (UTM zone 13N, meters). The allocated share of the county
  total is printed and logged; the unallocated remainder is boundary
  slivers, the same behavior recorded for the units layer (99.94%).

Output: data/neighborhood_population.csv and
data/population_build_log.json.
"""
import json, pathlib
import requests
import pandas as pd
from shapely import wkb
from shapely.geometry import shape
from shapely.ops import unary_union

ROOT = pathlib.Path(__file__).resolve().parent.parent
STACK = (pathlib.Path.home() / "workspace/goals/daily-civic-data-brief/"
         "hidden_files/stack/denver/layers")
UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) MachineReadable research"}
CRS = "EPSG:26913"


def tract_population():
    u = ("https://api.censusreporter.org/1.0/data/show/acs2024_5yr"
         "?table_ids=B01003&geo_ids=140|05000US08031")
    d = requests.get(u, timeout=90, headers=UA).json()
    out = {}
    for geoid, vals in d["data"].items():
        # Census Reporter ids look like 14000US08031000102; TIGERweb
        # GEOID is the bare 08031000102. Normalize to the bare GEOID.
        out[geoid.split("US")[-1]] = vals["B01003"]["estimate"]["B01003001"]
    return out


def tract_geometries():
    base = ("https://tigerweb.geo.census.gov/arcgis/rest/services/"
            "TIGERweb/tigerWMS_Current/MapServer/8/query")
    feats, offset = [], 0
    while True:
        r = requests.get(base, params={
            "where": "STATE='08' AND COUNTY='031'", "outFields": "GEOID",
            "returnGeometry": "true", "outSR": 4326, "f": "geojson",
            "resultOffset": offset, "resultRecordCount": 200}, timeout=90,
            headers=UA)
        d = r.json()
        batch = d.get("features", [])
        feats.extend(batch)
        if len(batch) < 200:
            break
        offset += 200
    return {f["properties"]["GEOID"]: shape(f["geometry"]) for f in feats}


def main():
    pop = tract_population()
    geoms = tract_geometries()
    assert set(pop) == set(geoms), (len(pop), len(geoms))
    tracts = pd.DataFrame(
        [{"geoid": g, "pop": pop[g], "geometry": geoms[g]} for g in pop])
    nb = pd.read_parquet(STACK / "neighborhoods_clean.parquet")
    nb["geometry"] = nb["geometry_wkb"].apply(wkb.loads)
    # Project with pyproj + shapely.ops.transform (no geopandas needed).
    from pyproj import Transformer
    tr = Transformer.from_crs("EPSG:4326", CRS, always_xy=True)
    from shapely.ops import transform as shp_transform
    tracts["geom_p"] = tracts["geometry"].apply(lambda g: shp_transform(tr.transform, g))
    nb["geom_p"] = nb["geometry"].apply(lambda g: shp_transform(tr.transform, g))
    tracts["area"] = tracts["geom_p"].apply(lambda g: g.area)
    nb["area_m2"] = nb["geom_p"].apply(lambda g: g.area)

    alloc = {name: 0.0 for name in nb["NBHD_NAME"]}
    allocated_pop = 0.0
    for t in tracts.itertuples():
        hits = nb[[g.intersects(t.geom_p) for g in nb["geom_p"]]]
        for n in hits.itertuples():
            inter = t.geom_p.intersection(n.geom_p).area
            if inter > 0:
                share = t.pop * inter / t.area
                alloc[n.NBHD_NAME] += share
                allocated_pop += share
    county_total = float(sum(pop.values()))
    units = pd.read_parquet(STACK / "acs_neighborhood_units.parquet")
    slug = dict(zip(units["neighborhood"], units["neighborhood_slug"]))
    rows = []
    for n in nb.itertuples():
        rows.append({
            "neighborhood": n.NBHD_NAME,
            "neighborhood_slug": slug.get(n.NBHD_NAME),
            "population_acs2024_5yr": round(alloc[n.NBHD_NAME], 1),
            "area_sq_mi": round(n.area_m2 / 2589988.11, 3),
        })
    out = pd.DataFrame(rows).sort_values("neighborhood")
    out.to_csv(ROOT / "data" / "neighborhood_population.csv", index=False)
    log = {
        "tracts": len(pop),
        "county_population_tract_sum": county_total,
        "allocated_population": round(allocated_pop, 1),
        "allocated_share_pct": round(100 * allocated_pop / county_total, 2),
        "neighborhoods": len(out),
        "neighborhoods_missing_slug": int(out["neighborhood_slug"].isna().sum()),
        "smallest_population_neighborhoods": out.nsmallest(
            5, "population_acs2024_5yr")[["neighborhood",
            "population_acs2024_5yr"]].values.tolist(),
    }
    (ROOT / "data" / "population_build_log.json").write_text(
        json.dumps(log, indent=2))
    print(json.dumps(log, indent=2))


if __name__ == "__main__":
    main()
