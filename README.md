# Denver Liquor Licenses - a Machine Readable data brief

Five of Denver's 78 statistical neighborhoods (Five Points, Union Station, Highland, the Central Business District, and DIA) hold 554 of the city's 1,965 active liquor licenses, 28.2 percent, and 7.4 percent of its residents. The Central Business District records 20.7 active licenses per 1,000 residents against a citywide rate of 2.7. Register pulled October 23, 2026 (2,215 records; 1,965 active).

Part of Machine Readable: https://adowlen.github.io/machine-readable/

## Contents

- brief-draft.md - the brief (publishable text)
- stats.json - every figure used in the brief, produced by code/build_stats.py
- verification.md - Section 10 pre-flight audit record and methods checklist (AUDIT PASSED)
- verification-ledger-independent.md - the independent verifier's recomputation ledger (all figures reproduced)
- reviewer-notes.md - claims most likely challenged, checks not completed, flags
- sources.md - dataset citations and the per-figure source audit
- social-drafts.md - LinkedIn draft (held for a future Friday synthesis under the Friday-only rule; Machine Readable never posts to X)
- hero.png - hero graphic (generated illustration, headline figure composited; code/hero_composite.py)
- charts/ - chart_top_counts.png, chart_neighborhood_rates.png, chart_class_mix.png, chart_fusion_scatter.png
- data/ - neighborhood_panel_liquor.csv (the published panel), neighborhood_population.csv (ACS denominators), liquor_raw.geojson (the full register pull), raw_aggregates.json, pull_log.json, population_build_log.json, audit_output.txt, verify_independent_output.json
- code/ - pull_data.py, build_population.py, build_stats.py, audit_section10.py, verify_independent.py, charts.py, hero_composite.py

## Dependencies (match code imports)

Python standard library; requests; pandas; numpy; shapely; pyproj; matplotlib; Pillow.

## Reuse and citation

Licensed CC-BY-4.0 (see LICENSE). Cite as: Machine Readable, "Denver's liquor licenses, counted neighborhood by neighborhood" (2026), https://github.com/adowlen/denver-liquor-licenses-data-brief
