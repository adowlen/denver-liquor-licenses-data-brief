# Denver's liquor licenses, counted neighborhood by neighborhood

**One-line finding:** Five of Denver's 78 statistical neighborhoods (Five Points, Union Station, Highland, the Central Business District, and DIA) hold 554 of the city's 1,965 active liquor licenses, 28.2 percent, and 7.4 percent of its residents; the Central Business District records 20.7 active licenses per 1,000 residents against a citywide rate of 2.7.

Source: City and County of Denver open data, liquor license register (ODC_BUSN_LIQUORLICENSES_P), 2,215 records pulled October 23, 2026. The register is published from Denver Department of Excise and Licenses records and is described by the city as updated daily. Population is the US Census Bureau's ACS 2024 5-year estimate (table B01003), allocated from census tracts to the city's 78 statistical neighborhoods by land-area share; the method and its checks are in the verification file.

## Finding 1: The register holds 2,215 records; 1,965 are licenses in force

The register's status field divides the 2,215 records into 1,965 LICENSE ISSUED - ACTIVE (88.7 percent), 157 PENDING (7.1 percent), and 93 DELINQUENT (4.2 percent). Every distribution figure in this brief is computed on the 1,965 in-force licenses. Pending records are applications the register does not yet show as issued, and delinquent records are issued licenses the register flags as delinquent; both groups are counted here and excluded from the density analysis.

Of the 1,965 active licenses, 1,938 carry one of the 78 statistical neighborhoods. The remaining 27 cannot be placed: their records carry placeholder coordinates (fixed points located outside Colorado) and council district 0, and no neighborhood. They are counted in citywide totals and in no neighborhood figure. Finding 6 returns to them.

The register's 35 license-class strings group, by the class names as filed, into three kinds of record. On-premises classes (hotel and restaurant, tavern, beer and wine, brew pub, club, arts, lodging, entertainment, and their cabaret and optional-premises variants) hold 1,498 active licenses, 76.2 percent. Off-premises retail classes (fermented malt beverage, retail store, drug store, 3.2 percent beer) hold 400, 20.4 percent. The remaining 67 active records, 3.4 percent, are event and add-on permits rather than premises: 35 special events licenses and 32 tastings permits. License counts in this brief are therefore counts of licenses in force, not counts of storefronts. The full class counter and the grouping are printed in stats.json.

## Finding 2: Five neighborhoods hold 28.2 percent of the licenses and 7.4 percent of the residents

Active licenses by neighborhood, highest counts (share of all 1,965 active licenses printed with each count):

- Five Points: 174 (8.9 percent)
- Union Station: 118 (6.0 percent)
- Highland: 96 (4.9 percent)
- Central Business District: 91 (4.6 percent)
- DIA: 75 (3.8 percent)

Together these five hold 554 licenses, 28.2 percent of the citywide total, on a combined population of 53,221 residents, 7.4 percent of the 718,458 residents allocated to neighborhoods. Extending the list: the ten highest-count neighborhoods (adding Central Park 68, Speer 67, Capitol Hill 58, Cherry Creek 56, and Berkeley 50) hold 853 licenses, 43.4 percent, and 18.3 percent of residents. The median neighborhood holds 17.5 active licenses, and the Gini coefficient of license counts across the 78 neighborhoods is 0.50.

At the other end, one neighborhood records no active license at all: Indian Creek, with 4,234 residents and 2,165 housing units. Twelve neighborhoods hold five or fewer active licenses (among them Barnum West with 1, Wellshire with 1, Fort Logan with 2, and Hilltop with 3); together they hold 41 licenses, 2.1 percent of the total, and 11.0 percent of the city's residents.

On the council-district geography the register itself carries, District 10 holds 412 active licenses, 21.0 percent of the total, followed by District 9 with 267 and District 1 with 253. District figures exclude the 27 records that carry the placeholder district value 0 (Finding 1).

## Finding 3: Per resident, the CBD carries 7.7 times the citywide license density

Dividing placed licenses by residents gives a citywide rate of 2.70 active licenses per 1,000 residents (1,938 licenses over 718,458 allocated residents). The median neighborhood rate is 2.07. The highest rates, with the counts and populations each rate rests on:

- Central Business District: 20.73 per 1,000 residents (91 licenses, 4,390 residents)
- DIA: 18.72 (75 licenses, 4,007 residents)
- Union Station: 11.90 (118 licenses, 9,920 residents)
- Auraria: 9.93 (7 licenses, 705 residents)
- Sun Valley: 9.16 (11 licenses, 1,201 residents)
- Highland: 8.57 (96 licenses, 11,208 residents)
- Cherry Creek: 7.96 (56 licenses, 7,040 residents)
- Five Points: 7.34 (174 licenses, 23,698 residents)

The top of this ranking is dominated by neighborhoods whose licenses mostly serve people who do not live in them, and the populations printed above are what make that visible: DIA's 75 licenses are airport concessions; Auraria's 7 include Ball Arena, Elitch Gardens, Meow Wolf, and Metropolitan State University of Denver; the CBD and Union Station serve the downtown workforce and visitors. A per-resident rate in these neighborhoods measures licenses against the people who sleep there, not the people the licenses serve, and this brief does not treat it as a measure of over- or under-supply. Among neighborhoods with more than 5,000 residents, the highest rates are Union Station (11.90), Highland (8.57), Cherry Creek (7.96), and Five Points (7.34), each between 2.7 and 4.4 times the citywide rate.

Measured per square mile instead, the order changes in one instructive place: Union Station records 269 active licenses per square mile and the CBD 211, followed by North Capitol Hill (102), Civic Center (102), and Five Points (99), while DIA falls to 1.8 per square mile across its 42.3 square miles. Ranking neighborhoods by licenses per 1,000 housing units instead of per 1,000 residents produces nearly the same ordering as the per-resident ranking (rank correlation 0.97), so the pattern does not depend on which residential denominator is chosen.

## Finding 4: Half the licenses in force are hotel and restaurant licenses

The largest class in the register is LIQUOR - HOTEL AND RESTAURANT with 739 active licenses. With its cabaret variant (211) and its optional-premises variants (13), the hotel and restaurant family holds 963 of the 1,965 active licenses, 49.0 percent. Taverns hold 294 (Tavern 129, Tavern and Cabaret 165), and Beer and Wine licenses 93.

Off-premises retail is two classes of near-equal size: Fermented Malt Beverage, 201 active licenses, the class under which the register lists grocery and convenience stores (King Soopers, 7-Eleven, and Circle K locations appear under it), and Store, 192, the class under which retail liquor stores are listed (Tom & Jerry's Liquor Store and Sportsman Liquor among them). Drug store and 3.2 percent beer classes together hold 7.

The mix tilts further toward on-premises in the highest-count neighborhoods: Five Points holds 152 on-premises and 19 off-premises licenses of its 174; Union Station 114 and 4 of 118; the CBD 85 and 4 of 91; DIA 67 and 8 of 75. Citywide, off-premises retail is 20.4 percent of active licenses; in these four neighborhoods it is between 3 and 11 percent.

## Finding 5: License density and reported-offense density occupy much the same geography

Joining the license panel to the Machine Readable crime panel (reported offenses by neighborhood, matched January 1 to October 13 window, 2026; 48,268 reports) on the same ACS population base: the rank correlation between a neighborhood's active licenses per 1,000 residents and its reported offenses per 1,000 residents is 0.69 across the 77 neighborhoods with at least 1,000 residents (0.70 across all 78). Thirteen neighborhoods sit in the top quartile of both densities: Baker, Capitol Hill, City Park West, Civic Center, the CBD, DIA, Elyria Swansea, Five Points, Lincoln Park, North Capitol Hill, Overland, Sun Valley, and Union Station.

The offense rates carry the same small-denominator behavior as the license rates: the CBD records 327 reported offenses per 1,000 residents in the window and DIA 429, against a citywide 67.2, while Montbello, with 18 licenses (0.56 per 1,000 residents), records 31.2. This is a neighborhood-level association between two densities. The offense panel counts all reported offenses, not alcohol-involved offenses, and this brief makes no claim that licenses cause reports, that reports attract licenses, or in which direction any relationship runs. Without the join, the license data alone could not show that the two concentrations share a geography; with it, that much is measured, and no more than that is claimed.

## Finding 6: The register cannot date a license before 2012, place 27 of its own records, or sit still for a day

Three limits of the source bound what this brief can say.

First, currency. The register is republished from Excise and Licenses records daily, and it moved during this analysis: a server count on the evening of October 23, 2026 first read 1,973 active and 85 delinquent records, and minutes later the settled pull read 1,965 and 93, the figures this brief uses and which two further reads the same evening confirmed. Counts in this brief are an October 23, 2026 snapshot of a register that changes daily.

Second, placement. 56 records carry placeholder coordinates at four fixed points outside Colorado (35 of them at a single point); 27 of those records are active licenses, and they are the same 27 records that carry council district 0 and no neighborhood. The brief counts them citywide and nowhere else. Three further active records carry an end date earlier than the pull date; the brief follows the register's status field for them, as for every record.

Third, vintage. The register's ORIGINAL_ISSUE_DATE field holds no date before April 30, 2012, and 960 records (43.3 percent of the register) are dated 2013 or 2014, the signature of a bulk load into a newer licensing system. The field therefore cannot say which of Denver's licensed premises are genuinely old: a license first issued decades ago and a license first issued in 2013 can carry the same recorded date. What the field can support is one bounded statement: 619 active licenses, 31.5 percent, carry original issue dates in 2020 or later, after the bulk-load years, and those records postdate the register's migration.

## What this might mean

One reading of these figures is that Denver's licensing outcomes have accumulated into a steeply uneven geography: a resident of Five Points or Highland lives in a neighborhood with roughly three times the citywide license density, a resident of Indian Creek or Barnum West in one with effectively none, and any public process that weighs a new license against neighborhood conditions is starting from baselines that differ by an order of magnitude depending on where the application lands.

The strongest alternative explanation is that licenses follow commercial land use, zoning capacity, foot traffic, and daytime population rather than residents, so a per-resident ranking mostly re-describes where Denver allows commerce: on that reading the CBD, DIA, and Auraria figures measure the mismatch between where licenses may cluster and where people sleep, and say nothing by themselves about harm, benefit, or whether any neighborhood carries too many licenses. The offense association in Finding 5 admits the same alternative: both densities may simply index the same commercial districts, with no direct relationship between them. The counts, shares, and rates above are consistent with both readings; the register alone cannot choose between them.

## Who can act

- **Denver Department of Excise and Licenses** controls the register and the license record. Concrete actions within its existing work: repair or correctly place the 56 placeholder-coordinate records so every in-force license is publicly locatable (27 active licenses currently have no neighborhood and district 0), and publish definitions for the register's 35 license-class strings alongside the dataset. Cost class: low-cost operational change. Outcome measure: the next register pull carries zero active records with placeholder coordinates, and this brief's panel can be rebuilt with all 1,965 active licenses placed.
- **Denver City Council**, in the 2027 budget cycle (hearing October 26, amendment vote November 2, passage November 9, 2026), controls the local licensing code and the Excise and Licenses budget. Concrete action: where licensing policy turns on neighborhood conditions, weigh it against a neighborhood baseline like the panel published with this brief (counts, per-resident and per-unit rates for all 78 neighborhoods) rather than citywide averages, which describe no actual neighborhood: the citywide rate is 2.70 per 1,000 residents and the CBD rate is 20.73. Cost class: budget and policy decision. Outcome measure: the same panel rebuilt on a later register pull shows whether the top-five share (28.2 percent) and the count of zero- and near-zero-license neighborhoods moved.
- **Residents and neighborhood organizations** are heard in Denver's license application process, where the Department of Excise and Licenses takes neighborhood input on new licenses. Concrete action: bring the baseline for the neighborhood in question (its current count and rates, from the data file published with this brief) rather than impressions of it. Cost class: low-cost operational change. Outcome measure: hearing records that cite the neighborhood's measured baseline, checkable against the panel.

## Data notes

- Snapshot: all register figures are from the pull of October 23, 2026 (2,215 records). The register changes daily; a later pull will differ in detail. During the pull window the register's own status counter moved by 8 records (Finding 6); the row pull, the server counters taken with it, and two later verification reads agree exactly, and the audit records all four reads.
- Neighborhood assignment uses the register's own NEIGHBORHOOD field, which the city overlays onto its Excise and Licenses data. As a control, every record that also carries valid coordinates (2,158 records) was independently assigned by point location against the city's statistical neighborhood polygons: the two assignments agree on all 2,158. One pending record with a blank source neighborhood and valid coordinates was assigned by its point location. Records with placeholder coordinates were never spatially assigned.
- Population denominators are ACS 2024 5-year estimates (table B01003, total population), read at census-tract level and allocated to statistical neighborhoods in proportion to land-area overlap, the same method the Machine Readable stack uses for its housing-unit denominator: 718,458 of the county's 718,877 residents allocated (99.94 percent); the remainder is boundary slivers. Housing-unit denominators are the stack's ACS B25001 layer built by the same method. Rates use allocated neighborhood populations throughout.
- License-class groups are derived from the class names as filed; the full mapping is in stats.json. Examples named in Finding 4 (King Soopers, 7-Eleven, Circle K, Tom & Jerry's Liquor Store, Sportsman Liquor) are register rows read directly from the pull, named to show what the two largest off-premises classes contain.
- The offense panel is the Machine Readable stack layer derived from Denver reported-offense data (ODC_CRIME_OFFENSES_P), matched January 1 to October 13 windows; this brief uses the 2026 window (48,268 reports). It counts all reported offenses; it is not an alcohol-specific measure.
- Reproduction: code/pull_data.py records the full register pull and the server-side counters; code/build_population.py builds the population denominator; code/build_stats.py builds stats.json and data/neighborhood_panel_liquor.csv; code/audit_section10.py records the pre-flight audit (output in data/audit_output.txt); code/verify_independent.py is the independent recomputation behind verification-ledger-independent.md; code/charts.py draws the charts.

*Machine Readable is a civic data project by Alex Dowlen. Briefs state measured facts from public data, with methods in the open. Corrections are welcome and will be reflected in the repository.*
