# Sources - Denver liquor licenses brief (2026-10-24)

Every figure in the brief traces to one of the sources below. Derived
figures are labeled derived and state their inputs.

## Register figures (counts, statuses, classes, districts)

- Source: City and County of Denver open data, ODC_BUSN_LIQUORLICENSES_P
  ("business liquor licenses"), ArcGIS FeatureServer layer 27,
  services1.arcgis.com/zdB7qR0BtYrg0Xpl. Catalog:
  opendata-geospatialdenver.hub.arcgis.com.
- What it is: the city's published liquor license register, described
  in its layer metadata as "updated daily by overlying Denver Excise
  and License liquor license data with police and council districts,
  as well as census tracts."
- Pull: October 23, 2026, full layer, 2,215 records
  (data/liquor_raw.geojson; pull record in data/pull_log.json;
  server-side counters in data/raw_aggregates.json).
- Figures taken directly: status counts (1,965 active, 157 pending,
  93 delinquent); class counter (35 class strings); council-district
  counts including the placeholder district 0; ORIGINAL_ISSUE_DATE
  record (floor 2012-04-30; 960 records dated 2013-2014; 619 active
  licenses dated 2020 or later); END_DATE check (3 active records
  past their end date).
- Derived: the three-way class grouping (on-premises 1,498;
  off-premises retail 400; event and add-on 67) and the hotel and
  restaurant family (963) are derived from the class names as filed;
  the mapping is printed in stats.json (class_groups) and was checked
  against sampled business names (verification ledger T3).

## Neighborhood assignment

- Source: the register's own NEIGHBORHOOD field (city overlay), with
  the city's statistical neighborhood polygons (Machine Readable
  stack layer neighborhoods_clean.parquet, sourced from Denver open
  data) as the independent control.
- Figures: 1,938 active licenses carry a neighborhood. Control:
  point-in-polygon on every record with valid coordinates agreed
  with the source field on all 2,158 records (0 disagreements).
  56 records carry placeholder coordinates at 4 fixed points outside
  Colorado and no neighborhood (27 of them active); 1 pending record
  with a blank source neighborhood and valid coordinates was assigned
  by point location.

## Population denominators (per-resident rates, population shares)

- Source: US Census Bureau, ACS 2024 5-year estimates, table B01003
  (total population), census-tract level for Denver County (178
  tracts), read through Census Reporter's API on October 23, 2026.
  The Census Bureau's own API endpoint required a key during this
  build and was not used; Census Reporter serves the same ACS
  release.
- Tract geometries: US Census Bureau TIGERweb (tigerWMS_Current,
  census tracts layer).
- Derived: tract population allocated to the 78 statistical
  neighborhoods in proportion to land-area overlap (EPSG:26913),
  the same method as the stack's housing-unit layer. County total
  718,877 (tract sum, equal to Census Reporter's direct county
  read); allocated 718,458 (99.94 percent). Build record:
  data/population_build_log.json; denominators:
  data/neighborhood_population.csv; code: code/build_population.py.
- Figures taken from this layer: every per-1,000-residents rate;
  the top-5 population share (7.4 percent: 53,221 of 718,458);
  the top-10 share (18.3 percent); the 12 low-count neighborhoods'
  population share (11.0 percent).

## Housing-unit denominators (robustness check only)

- Source: Machine Readable stack layer acs_neighborhood_units.parquet
  (ACS B25001 total housing units, same tract-allocation method,
  built for the September 29, 2026 housing brief).
- Figure: rank correlation between licenses per 1,000 residents and
  per 1,000 housing units across neighborhoods = 0.97 (printed as a
  robustness statement in Finding 3, not as a headline figure).

## Crime fusion (Finding 5)

- Source: Machine Readable stack layer crime_neighborhood_panel.parquet,
  derived from Denver open data reported offenses
  (ODC_CRIME_OFFENSES_P), matched January 1 to October 13 windows by
  year; this brief uses the 2026 window (48,268 reports across the
  78 neighborhoods).
- Derived: offenses per 1,000 residents on the same ACS population
  base as the license rates; Spearman rank correlation 0.69 (77
  neighborhoods with at least 1,000 residents) and 0.70 (all 78);
  the 13-neighborhood top-quartile overlap list; citywide offense
  rate 67.2 per 1,000 residents in the window.
- Scope limit (in the brief): the panel counts all reported offenses,
  not alcohol-involved offenses; the association is ecological.

## Areas (per-square-mile figures)

- Source: statistical neighborhood polygon areas (EPSG:26913)
  from the stack's neighborhoods_clean.parquet.
- Derived: active licenses per square mile (Union Station 269,
  CBD 211, North Capitol Hill 102, Civic Center 102, Five Points 99,
  DIA 1.8 over 42.3 square miles).

## Not used

- 311 data: no question was identified that 311 records could
  answer about license distribution beyond what the crime panel
  already measures; not joined (layering test, verification.md).
- The bank lead's preliminary count (2,210 licenses) was not used;
  the live pull counted 2,215 records, of which 1,965 active.
