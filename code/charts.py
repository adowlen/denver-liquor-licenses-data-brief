"""Data charts for the Denver liquor licenses brief. Brand palette:
dark charcoal background, amber + teal bars, white text."""
import json, pathlib
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

root = pathlib.Path(__file__).resolve().parent.parent
s = json.loads((root / "stats.json").read_text())
panel = pd.read_csv(root / "data" / "neighborhood_panel_liquor.csv")
BG, AMBER, TEAL, FG = "#1c1c1e", "#e8a33d", "#2a9d8f", "#f2f2f2"
plt.rcParams.update({"figure.facecolor": BG, "axes.facecolor": BG,
                     "text.color": FG, "axes.labelcolor": FG,
                     "xtick.color": FG, "ytick.color": FG,
                     "axes.edgecolor": "#555555", "font.size": 10})

# 1. Highest licenses per 1,000 residents (counts printed on each bar)
rows = s["top_by_per_1000_residents"][:8][::-1]
fig, ax = plt.subplots(figsize=(8.2, 4.8))
ax.barh([r[0] for r in rows], [r[3] for r in rows], color=AMBER)
for i, r in enumerate(rows):
    ax.text(r[3] + 0.5, i, f"{r[3]}  ({r[1]:.0f} licenses, {r[2]:,.0f} residents)",
            va="center", fontsize=9)
ax.set_xlim(0, 30)
ax.set_xlabel("Active liquor licenses per 1,000 residents (ACS 2024 5-year population)")
ax.set_title(f"Highest license density per resident, by neighborhood\n"
             f"Citywide: {s['citywide_active_per_1000_residents']} per 1,000 residents",
             loc="left", fontsize=11)
fig.tight_layout(); fig.savefig(root / "charts" / "chart_neighborhood_rates.png", dpi=200)
plt.close(fig)

# 2. Largest counts by neighborhood
p = panel.sort_values("active_licenses", ascending=False).head(10).iloc[::-1]
fig, ax = plt.subplots(figsize=(8.2, 5.0))
ax.barh(p["neighborhood"], p["active_licenses"], color=TEAL)
for i, (c, share) in enumerate(zip(p["active_licenses"], p["share_of_city_active_pct"])):
    ax.text(c + 3, i, f"{c:.0f}  ({share}% of all active)", va="center", fontsize=9)
ax.set_xlim(0, 205)
ax.set_xlabel("Active liquor licenses")
ax.set_title("Most active liquor licenses, by neighborhood\n"
             "1,965 active licenses citywide; 27 carry no neighborhood (see brief)",
             loc="left", fontsize=11)
fig.tight_layout(); fig.savefig(root / "charts" / "chart_top_counts.png", dpi=200)
plt.close(fig)

# 3. License classes among active licenses (top classes, as filed)
cc = list(s["class_counter_active"].items())[:8][::-1]
labels = [k.replace("LIQUOR - ", "").title() for k, _ in cc]
fig, ax = plt.subplots(figsize=(8.2, 4.6))
ax.barh(labels, [v for _, v in cc], color=AMBER)
for i, (_, v) in enumerate(cc):
    ax.text(v + 18, i, f"{v:,}", va="center", fontsize=9)
ax.set_xlim(0, 860)
ax.set_xlabel("Active licenses")
ax.set_title("Largest license classes among active licenses (class names as filed)",
             loc="left", fontsize=11)
fig.tight_layout(); fig.savefig(root / "charts" / "chart_class_mix.png", dpi=200)
plt.close(fig)

# 4. Fusion scatter: license density vs reported-offense density
f = panel[(panel["population_acs2024_5yr"] >= 1000)
          & panel["offense_reports_2026_window"].notna()]
fig, ax = plt.subplots(figsize=(8.2, 5.2))
ax.scatter(f["per_1000_residents"], f["offenses_per_1000_residents"],
           s=26, color=TEAL, alpha=0.85, edgecolor="none")
for name in ["CBD", "Five Points", "Union Station", "DIA", "Capitol Hill",
             "Montbello", "Indian Creek"]:
    r = f[f["neighborhood"] == name]
    if len(r):
        r = r.iloc[0]
        ax.annotate(name, (r["per_1000_residents"],
                           r["offenses_per_1000_residents"]),
                    textcoords="offset points", xytext=(6, 4), fontsize=8.5)
ax.set_xlabel("Active liquor licenses per 1,000 residents")
ax.set_ylabel("Reported offenses per 1,000 residents\n(Jan 1-Oct 13, 2026 window, Denver crime data)")
ax.set_title("License density and reported-offense density, by neighborhood\n"
             "Rank correlation 0.69 across 77 neighborhoods (population 1,000+)",
             loc="left", fontsize=11)
fig.tight_layout(); fig.savefig(root / "charts" / "chart_fusion_scatter.png", dpi=200)
plt.close(fig)
print("charts done")
