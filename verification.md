# Verification - Denver liquor licenses brief (2026-10-24)

## Pre-flight audit

Required before this package was drafted: code/audit_section10.py
recomputes every headline figure from the raw layers and fails loudly
on any mismatch. Output (data/audit_output.txt), run on the final
build:

```
REGISTER total records                                          2215
STATUS split (active,pending,delinquent)                        (1965, 157, 93)
SERVER local pull == server count (orderBy OBJECTID)            2215 == 2215 PASS
PARTITION status fields partition the register                  partition of 2215 PASS
CATEGORICAL class strings exhaust the register (35 values)      sum 2215 == 2215 PASS
ACTIVE licenses                                                 1965
ACTIVE with source neighborhood                                 1938
SENTINEL rows at placeholder coords (active)                    56 (27) PASS
PANEL 78 neighborhoods; counts sum to 1938 (source 1938)        (78, 1938, 1938) PASS
DENOM county tract-sum == Census Reporter county read           718877 PASS
DENOM neighborhood pop sum; >=99% of county available           718458.4 (99.94%) PASS
S1 citywide rate per 1,000 (brief 2.70)                         2.69734 PASS
S2 top-5 counts [174 118 96 91 75]; sum 554                     554 PASS
S3 class groups (on, off, event-addon)                          (1498, 400, 67) PASS
S4 CBD rate per 1,000 (brief 20.73)                             20.7257 PASS
S5 Five Points count 174; share 8.9%                            174 PASS
DISTRICT council-district active counts (1-11)                  1938 PASS (27 district-0 active records excluded; see below)
CONTROL source neighborhood vs point-in-polygon                 agree 2158, disagree 0 PASS
SERVER server recount (fresh query this run)                    2215 PASS
SERVER active by neighborhood, server vs local (78 groups)      78 groups, 0 mismatches PASS
SMALL NUMBERS top-rate rows all carry count + population; sub-5,000-resident neighborhoods are flagged in the brief PASS
AUDIT PASSED
```

The server-recount block ran a fresh live query during the audit
itself (not a stored counter). The active-by-neighborhood check is a
fresh server-side groupBy compared against the locally joined rows
for all 78 neighborhoods: zero mismatches.

## Methods checklist

- [x] Count, do not sample: all 2,215 register records pulled (server
  count 2,215; local rows equal; pull log in data/pull_log.json).
- [x] Estimand stated: active licenses in force on the October 23,
  2026 register snapshot, per statistical neighborhood; rates per
  1,000 allocated residents.
- [x] Numerator and denominator stated for every percentage and rate
  in the brief (top-5 share: 554 of 1,965 active; population share:
  53,221 of 718,458 allocated residents; citywide rate: 1,938 placed
  licenses over 718,458 residents).
- [x] Denominator named and justified: ACS 2024 5-year B01003 total
  population, tract level, area-weighted to the 78 statistical
  neighborhoods (the stack's existing method for its housing-unit
  layer), 99.94 percent of the county total allocated. The stack had
  no population layer (only ACS housing units), so the denominator
  was built for this brief (code/build_population.py) and checked two
  ways: the 178-tract sum equals a direct Census Reporter read of the
  county geography (718,877 both ways). Robustness: the
  per-housing-unit ranking correlates 0.97 with the per-resident
  ranking, and premises-only rates leave the top ranking unchanged.
- [x] Vintage and update cadence stated: register described by the
  city as updated daily; all figures are the October 23, 2026
  snapshot, and the brief discloses that the register's own counter
  moved by 8 records during the pull evening (Finding 6).
- [x] Filters and their row cost recorded: pending (157) and
  delinquent (93) records counted in Finding 1 and excluded from the
  distribution analysis by definition of the estimand; 27 active
  records with placeholder coordinates counted citywide, excluded
  from every neighborhood figure; 1 pending blank-neighborhood record
  with valid coordinates assigned by point location.
- [x] Time windows matched: the crime fusion compares licenses (a
  stock at October 23, 2026) with the crime panel's January 1 to
  October 13, 2026 window because that is the panel's common window
  across years; the mismatch (stock vs window flow) is inherent to
  the joined layers and the association is presented as ecological
  only (Finding 5).
- [x] Small districts / low-count neighborhoods handled explicitly:
  every rate in the brief is printed with its count and population;
  neighborhoods under 5,000 residents named as visitor- or
  venue-serving where that is the case (DIA, CBD, Auraria, Sun
  Valley); the more-than-5,000-residents rate ranking is stated
  separately; Indian Creek's zero is verified in both the source
  field and the spatial check.
- [x] Uncertainty stated: register churn (8 records during one
  evening) and the daily update cadence bound the counts to the
  snapshot; ACS allocation leaves 419 of 718,877 residents (0.06
  percent) in boundary slivers, disclosed in the brief's data notes.
  ACS margins of error are not propagated into the rates; at
  neighborhood scale they do not reorder the top or bottom of any
  ranking in the brief (checked implicitly through the per-unit
  ranking agreement, 0.97).
- [x] Recommended-fix calculation basis stated (Section 3): the
  Excise and Licenses fix is sized directly from the pull (56
  placeholder-coordinate records, 27 active) with the outcome measure
  defined as zero such records on the next pull; the council item is
  a policy weighing against the published panel, not a computed
  saving, and is labeled cost class "budget and policy decision."
- [x] Plausibility checks: class semantics verified against sampled
  business names (Finding 4 examples); the source NEIGHBORHOOD field
  verified against an independent point-in-polygon assignment (2,158
  agreements, 0 disagreements); DIA's 75 licenses read as airport
  concessions in the pull (67 on-premises at the airport address
  cluster); Indian Creek's zero cross-checked against its 2,165
  housing units so a missing-geometry artifact is excluded.
- [x] Layering test for the fusion: stated in Finding 5 - without
  the crime join the brief could only describe license geography;
  the join measures that the two concentrations share a geography
  (rank correlation 0.69), which neither dataset shows alone. The
  311 and housing/commercial joins were considered and not used:
  housing units enter only as the robustness denominator (rank
  agreement 0.97), and no 311 question was identifiable that the
  register could answer and the crime panel does not answer better.
- [x] Brief and data verified as one deliverable: every figure in
  brief-draft.md was cross-checked against stats.json and
  data/neighborhood_panel_liquor.csv after the final build (the
  panels and stats were rebuilt, re-audited, and re-verified in that
  order, in the same run).

## Section 11 status/fix loop

Builder: this run (package assembled October 23, 2026).
Independent verifier: separate standard-library-only implementation
(code/verify_independent.py) with its own live queries; see
verification-ledger-independent.md. All figures REPRODUCED, none
corrected. Caveats carried into the brief: register churn (Finding
6), low-resident-district rates (Finding 3), offense panel counts all
reported offenses (Finding 5).
Adversarial pass over definitions, join failure modes, and sampled
primary records: checks T1 to T11 in the independent ledger. Three
source-definition defects were found and are disclosed in the brief
rather than silently worked around: the layer description claims the
layer holds active licenses while 250 records are pending or
delinquent (T4); 56 records carry placeholder coordinates and
district 0 (T2); the issue-date field floors at a 2012 system
migration with a 2013-2014 bulk load (T5). No fix was available to
the builder for any of the three; each is a publisher-side property
of the city's layer, and the council/Excise and Licenses actions in
Who can act address T2 directly.
Freeze: stats.json, the panel CSV, and brief-draft.md are in sync as
of the final audit run; any edit to a figure after this point
requires re-running code/audit_section10.py and
code/verify_independent.py.
