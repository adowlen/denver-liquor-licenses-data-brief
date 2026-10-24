# Independent verification ledger - Denver liquor licenses brief (2026-10-24)

Verifier method (independent of the builder): standard-library-only
recomputation (code/verify_independent.py; json, csv, statistics; no
pandas, no shapely) from the saved raw pull, plus fresh live queries
against the ArcGIS service and Census Reporter made during the
verification pass itself. Output: data/verify_independent_output.json.

## Figures: all REPRODUCED, none corrected

| Figure | Builder | Independent | Verdict |
|---|---|---|---|
| Register records | 2,215 | 2,215 (stdlib recount; fresh live count) | REPRODUCED |
| Status split (active / pending / delinquent) | 1,965 / 157 / 93 | 1,965 / 157 / 93 (fresh live server groupBy) | REPRODUCED |
| Active with a neighborhood | 1,938 | 1,938 (stdlib count of source field) | REPRODUCED |
| Top 5 by count | Five Points 174, Union Station 118, Highland 96, CBD 91, DIA 75 | identical (stdlib Counter; and fresh live server groupBy, zero diffs across all 78 neighborhoods) | REPRODUCED |
| Class groups (on / off / event-add-on) | 1,498 / 400 / 67 | 1,498 / 400 / 67 (stdlib, mapping from stats.json) | REPRODUCED |
| Hotel and restaurant family | 963 | 963 | REPRODUCED |
| Citywide rate per 1,000 residents | 2.70 | 2.70 (recomputed from panel CSV) | REPRODUCED |
| CBD rate per 1,000 residents | 20.73 | 20.73 | REPRODUCED |
| Top-5 license share / population share | 28.2% / 7.4% | 28.2% / 7.4% | REPRODUCED |
| Median neighborhood rate | 2.07 | 2.07 (hand sorted) | REPRODUCED |
| Gini of neighborhood counts | 0.50 | 0.500 | REPRODUCED |
| Spearman, licenses vs offenses (pop 1,000+) | 0.685 | 0.685 (hand ranks, averaged ties) | REPRODUCED |
| County population (tract sum) | 718,877 | 718,877 (Census Reporter county geography read directly, equals the 178-tract sum) | REPRODUCED |

## Traps examined (adversarial pass over source definitions and samples)

- T1 Register churn: the builder's first server counter of the evening
  read ACTIVE 1,973 / DELINQUENT 85; the settled pull and every later
  read (including this pass) read 1,965 / 93. Mechanism: the layer is
  republished daily from Excise and Licenses records and was mid-edit
  during the first query. Treatment: brief Finding 6 discloses the
  snapshot nature and the 8-record move; all printed figures come from
  the single settled pull, which the audit re-checked server-to-local.
- T2 Placeholder coordinates: 56 records sit at 4 fixed points outside
  Colorado (35 at one point); 27 are active. All 56 carry no source
  neighborhood and council district 0. Mechanism (from the layer
  description): the city overlays Excise and Licenses data with
  districts and neighborhoods; these records are the overlay's
  unplaced residue, and most are special events licenses (48 of 56).
  Treatment: counted citywide only; the audit asserts none was
  spatially assigned and district 0 is excluded from district claims.
- T3 Class-name semantics: 'LIQUOR - STORE' could be misread. Sampled
  rows are retail liquor stores (Tom & Jerry's Liquor Store,
  Sportsman Liquor, Sir Fredericks Liquors). 'FERMENTED MALT
  BEVERAGE' sampled rows are grocery and convenience stores (King
  Soopers, 7-Eleven, Circle K). 'TASTINGS' holders are liquor-store
  LLCs (an add-on permit). 'SPECIAL EVENTS' holders are nonprofits
  and venues (Denver Botanic Gardens). The brief's grouping follows
  these contents, and Finding 4 names examples so readers can check.
- T4 The layer description says the layer contains points "where an
  active liquor license issued," yet 250 of 2,215 records are PENDING
  or DELINQUENT. Treatment: the brief defines its population by the
  status field itself and prints all three status counts (Finding 1).
- T5 ORIGINAL_ISSUE_DATE floor: no date before 2012-04-30 and 960
  records dated 2013-2014 (43.3 percent) - a system bulk load, not a
  licensing boom. Treatment: Finding 6 refuses vintage claims and
  prints the one bounded statement the field supports (dates in 2020
  or later postdate the migration).
- T6 End dates: 3 active records carry an END_DATE before the pull
  date (two special-events nonprofits, one lodge). Treatment: status
  field governs; disclosed in Finding 6.
- T7 Small-population rates: Auraria (705 residents), Sun Valley
  (1,201), DIA (4,007), CBD (4,390), and Civic Center (4,289) rates
  are computed against small residential bases while their licenses
  serve visitors, travelers, and venue crowds. Treatment: every rate
  in the brief is printed with its count and population, the
  more-than-5,000-residents ranking is stated separately, and Finding
  3 refuses the over/under-supply reading.
- T8 Geography control: the source NEIGHBORHOOD field against an
  independent point-in-polygon assignment agreed on all 2,158 records
  carrying both (0 disagreements), so the neighborhood geography is
  not a join artifact. Indian Creek's zero is real in both the source
  field and the spatial check.
- T9 Denominator choice: per-resident vs per-housing-unit rankings
  correlate at 0.97, so the headline pattern is not an artifact of
  choosing residents. Population allocation itself allocated 99.94
  percent of the county total; the unallocated 419 residents are
  boundary slivers, disclosed in the brief's data notes.
- T10 Fusion scope: the offense panel counts ALL reported offenses
  (48,268 in the 2026 matched window), not alcohol-involved offenses,
  and the association is ecological. Treatment: Finding 5 states both
  limits in the finding itself and makes no causal or directional
  claim; the strongest alternative (shared commercial land use) is
  printed in What this might mean.
- T11 Duplicate records: zero duplicate BFN values in the pull; the
  register is one row per license record, so no dedupe decision was
  needed. Multiple licenses at one address are real (premises plus
  add-on permits) and are why the brief counts licenses, not
  storefronts (Finding 1).

No open finding. Every figure in the brief traces to stats.json or
the panel CSV, both rebuilt and re-audited after the final build.
