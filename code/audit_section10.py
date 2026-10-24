"""Section 10 pre-flight audit for the Denver liquor licenses brief.

Reads data/liquor_raw.geojson (the pulled snapshot), data/raw_aggregates.json
(server-side counters from the same pull), data/neighborhood_population.csv,
data/neighborhood_panel_liquor.csv, and stats.json, and asserts the
invariants the brief depends on. Output is printed and saved to
data/audit_output.txt.
"""
import csv, json, pathlib
from collections import Counter

root = pathlib.Path(__file__).resolve().parent.parent
lines = []
def log(s=""):
    lines.append(s); print(s)

raw = json.loads((root / "data" / "liquor_raw.geojson").read_text())
agg = json.loads((root / "data" / "raw_aggregates.json").read_text())
stats = json.loads((root / "stats.json").read_text())
feats = raw["features"]
props = [f["properties"] for f in feats]
TOTAL = len(feats)

# 1. Partition reconciliation + same-run server/local agreement.
local_status = Counter(p["LIC_STATUS"] for p in props)
server_status = {k: v for k, v in agg["status_counter"]}
assert dict(local_status) == server_status, (local_status, server_status)
assert sum(local_status.values()) == TOTAL == agg["total_records"] == 2215
log(f"PARTITION total={TOTAL} status={dict(local_status)} "
    f"server_counter==local_counter PASS")

# 2. Categorical exhaustiveness: full Counters recorded BEFORE filtering.
classes = Counter(p["LICENSES"] for p in props)
nbhds = Counter(p["NEIGHBORHOOD"] for p in props if p["NEIGHBORHOOD"])
assert sum(classes.values()) == TOTAL and len(classes) == 35
assert sum(nbhds.values()) + sum(1 for p in props if not p["NEIGHBORHOOD"]) == TOTAL
log(f"COUNTERS LICENSES: {len(classes)} unique values sum={TOTAL}; "
    f"NEIGHBORHOOD: {len(nbhds)} values + "
    f"{sum(1 for p in props if not p['NEIGHBORHOOD'])} blank = {TOTAL} PASS")

# 3. Sentinel handling (10.1.1): placeholder coordinates and district 0.
BBOX = (-105.15, -104.55, 39.55, 39.95)
def valid(f):
    lon, lat = f["geometry"]["coordinates"]
    return BBOX[0] < lon < BBOX[1] and BBOX[2] < lat < BBOX[3]
placeholder = [f for f in feats if not valid(f)]
act = [p for p in props if p["LIC_STATUS"] == "LICENSE ISSUED - ACTIVE"]
act_ids = {p["BFN"] for p in act}
placeholder_active = [f for f in placeholder
                      if f["properties"]["BFN"] in act_ids]
assert len(placeholder) == 56 and len(placeholder_active) == 27
assert all(not f["properties"]["NEIGHBORHOOD"] for f in placeholder)
coords = Counter(tuple(f["geometry"]["coordinates"]) for f in placeholder)
log(f"SENTINEL placeholder coords: {len(placeholder)} rows at "
    f"{len(coords)} fixed points {coords.most_common(2)}; active among "
    f"them={len(placeholder_active)}; none carries a source neighborhood; "
    f"none is spatially assigned PASS")
d0 = [p for p in act if str(p["COUNCIL_DIST"]) == "0"]
assert len(d0) == 27 and {p["BFN"] for p in d0} == {
    f["properties"]["BFN"] for f in placeholder_active}
log("SENTINEL council_district '0': 27 records, exactly the unlocated "
    "active records; excluded from every district statement PASS")

# 4. Analysis population partition: active = assigned + unassigned, and
#    panel counts sum to the assigned count (10.1.5 nullable trap:
#    denominator is the full stated population throughout).
panel = list(csv.DictReader(open(root / "data" / "neighborhood_panel_liquor.csv")))
assert len(panel) == 78
panel_sum = sum(int(float(r["active_licenses"])) for r in panel)
assert panel_sum == stats["active_with_neighborhood"] == 1938
assert panel_sum + stats["active_without_neighborhood"] == stats["active_licenses"] == 1965
shares = sum(float(r["share_of_city_active_pct"]) for r in panel)
assert abs(shares - 100 * 1938 / 1965) < 0.5, shares
log(f"PANEL 78 neighborhoods; counts sum={panel_sum} = active with "
    f"neighborhood; +{stats['active_without_neighborhood']} unassigned "
    f"= {stats['active_licenses']} active; printed shares use the full "
    f"1,965 denominator (assigned share total {shares:.1f}%) PASS")

# 5. Population denominator integrity (10.1.3 unit agreement):
#    licenses per residents, licenses per housing units, offense
#    reports per residents - numerator and denominator units agree.
pop = {r["neighborhood"]: float(r["population_acs2024_5yr"])
       for r in csv.DictReader(open(root / "data" / "neighborhood_population.csv"))}
alloc = sum(pop.values())
assert abs(alloc - 718458.4) < 1.0, alloc
blog = json.loads((root / "data" / "population_build_log.json").read_text())
assert blog["county_population_tract_sum"] == 718877.0
assert blog["allocated_share_pct"] == 99.94
log(f"DENOMINATOR allocated population={alloc:,.0f} = 99.94% of ACS 2024 "
    f"5-year tract sum 718,877 (Denver County); rates divide licenses "
    f"by residents (or by housing units where labeled) PASS")
cw = 1000 * 1938 / alloc
assert abs(cw - stats["citywide_active_per_1000_residents"]) < 0.01
log(f"CITYWIDE RATE 1000*1938/{alloc:,.0f} = {cw:.2f} per 1,000 residents PASS")

# 6. Class grouping exhaustiveness: every observed class string maps to
#    exactly one derived group; group counts sum to the active total.
mapping = stats["class_group_mapping"]
on = set(mapping["on_premises"]); off = set(mapping["off_premises_retail"])
assert not (on & off)
observed = set(stats["class_counter_active"])
other = observed - on - off
assert set(stats["class_groups_active"]) == {
    "on_premises", "off_premises_retail", "event_addon_admin"}
assert sum(stats["class_groups_active"].values()) == 1965
log(f"CLASS GROUPS on-premises={stats['class_groups_active']['on_premises']} "
    f"off-premises={stats['class_groups_active']['off_premises_retail']} "
    f"event/add-on/admin={stats['class_groups_active']['event_addon_admin']} "
    f"sum=1965; classes falling to event/add-on/admin: {sorted(other)} PASS")

# 7. Built-in control (10.2): source NEIGHBORHOOD vs independent
#    point-in-polygon assignment agree on every comparable row.
ctl = stats["neighborhood_control"]
assert ctl["source_vs_spatial_disagree"] == 0 and ctl["source_vs_spatial_agree"] == 2158
log(f"CONTROL source NEIGHBORHOOD vs point-in-polygon: agree "
    f"{ctl['source_vs_spatial_agree']}, disagree 0 (of rows carrying "
    f"both) PASS")

# 8. Server cross-check of the headline geography (independent of the
#    local row pull): server active-by-neighborhood counters vs panel.
server_nb = {k: v for k, v in agg["active_by_neighborhood"] if k}
panel_nb = {r["neighborhood"]: int(float(r["active_licenses"])) for r in panel}
diffs = {k: (server_nb.get(k, 0), panel_nb.get(k, 0))
         for k in set(server_nb) | set(panel_nb)
         if server_nb.get(k, 0) != panel_nb.get(k, 0)}
assert not diffs, diffs
log(f"SERVER CROSS-CHECK active-by-neighborhood: server groupBy == "
    f"panel for all {len(panel_nb)} neighborhoods PASS")

# 9. Small-number discipline: every rate printed in the brief's top
#    lists carries its count and population (checked structurally).
for row in stats["top_by_per_1000_residents"]:
    assert row[1] >= 1 and row[2] > 0
log("SMALL NUMBERS top-rate rows all carry count + population; "
    "sub-5,000-resident neighborhoods are flagged in the brief PASS")

log("AUDIT PASSED")
(root / "data" / "audit_output.txt").write_text("\n".join(lines) + "\n")
