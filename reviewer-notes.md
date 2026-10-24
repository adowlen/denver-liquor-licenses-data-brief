# Reviewer notes - Denver liquor licenses brief (2026-10-24)

For the morning QA run. Package state: brief-draft.md, stats.json,
panel CSV, charts, and hero are final and in sync; audit PASSED on
the final build; independent verification reproduced every figure
with zero corrections.

## Claims most likely to be challenged

1. The per-resident framing itself. The headline rates (CBD 20.73,
   DIA 18.72 per 1,000 residents) divide licenses by the people who
   sleep in the neighborhood, while downtown, airport, and arena
   licenses serve visitors and workers. The brief handles this in
   Finding 3 (rates printed with counts and populations; the
   more-than-5,000-residents ranking stated separately; an explicit
   refusal of the over/under-supply reading) and gives the strongest
   alternative explanation its own paragraph. If QA wants a softer
   top line, the defensible fallback headline is the count
   concentration (28.2 percent of licenses in 5 neighborhoods with
   7.4 percent of residents), which does not depend on any rate.
2. The 28.2 percent concentration depends on the analysis population
   being ACTIVE licenses only (1,965 of 2,215 records). Including
   pending applications would move shares slightly; the choice is
   definitional (licenses in force), is stated in Finding 1, and
   pending and delinquent records are counted there rather than
   dropped silently.
3. The population denominator is new. The stack had no neighborhood
   population layer (ACS housing units only), so one was built for
   this brief with the stack's own tract-allocation method. Checks:
   tract sum equals a direct county read (718,877); 99.94 percent
   allocated; per-unit rankings agree at 0.97. A challenger would
   have to dispute the ACS itself or the allocation method the stack
   already uses, and both are disclosed in the data notes. Worth
   keeping the layer: data/neighborhood_population.csv is reusable
   by any future brief needing per-capita rates.
4. The crime correlation (0.69) is the softest number in the brief:
   ecological, all-offense (not alcohol-specific), and both sides
   plausibly index commercial land use. Finding 5 states all three
   limits and claims only shared geography. If QA is uneasy, the
   finding can be cut without touching any other figure; nothing
   else depends on it.

## Dataset-quality finding, and whom it reflects on (Section 11.3)

The placeholder-coordinate records (56, of which 27 active), the
district-0 assignments, the layer description claiming an
active-license layer while 250 records are pending or delinquent,
and the issue-date field floored at a 2012 system migration are
properties of the City and County of Denver's published layer
(Denver Department of Excise and Licenses source data, published via
Denver open data). The brief reports them as measured facts in
Findings 1 and 6 and addresses the fix to Excise and Licenses in Who
can act. No other dataset in the package carries a comparable defect:
the ACS denominators and the crime panel passed their checks.

## Checks not completed

- None blocking. One non-check, disclosed: ACS margins of error were
  not propagated into the rates (standard for this series; the
  per-unit ranking agreement at 0.97 is the robustness evidence).
- The register's daily churn means a morning re-pull will not match
  2,215 exactly; that is expected and Finding 6 pre-discloses it. QA
  should not re-pull and diff; the audit's server checks were run
  against the settled October 23 snapshot and its fresh queries
  matched at audit time.

## Surprises worth knowing

- Indian Creek has zero active licenses on 4,234 residents and 2,165
  housing units, verified two ways. It is the only zero.
- The district-0 placeholder set and the unlocated set are exactly
  the same 27 active records; the register's two missing-geography
  signals coincide perfectly, which is why the fix in Who can act is
  a single repair, not two.
- Register churn was visible in real time: the first server counter
  of the evening read 1,973 active / 85 delinquent and the settled
  pull read 1,965 / 93 (a net 8 records moving between statuses
  mid-evening, consistent with the layer's daily republication).
  All printed figures come from the settled pull.
- The bank lead's preliminary count (2,210) is close to but not the
  live figure (2,215 records; 1,965 active). The brief uses only the
  live pull, per the standards' verify-before-use rule.
