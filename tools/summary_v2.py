"""Collect the stage results into one comparison table (Markdown).

Usage: python tools/summary_v2.py outputs/v2 > outputs/v2/stages.md
       python tools/summary_v2.py outputs/v3 > outputs/v3/stages.md
With several directories, for each stage the first directory that has a
result for it is used.
"""

import json
import sys
from pathlib import Path

import pandas as pd

STAGES = [
    ("phase1", "Phase 1"),
    ("step1", "Step 1"),
    ("step2", "Step 2"),
    ("step3", "Step 3"),
    ("step4", "Step 4"),
    ("step5", "Step 5 (end of schedule)"),
    ("longrun", "Long run"),
]


def load(roots: list[Path], stage: str):
    found = [d for root in roots for d in sorted(root.glob(f"v*_{stage}_2026")) if (d / "summary.json").exists()]
    if not found:
        return None
    d = found[0]
    s = json.load(open(d / "summary.json"))
    b = pd.read_csv(d / "budget.csv").set_index("item")
    pov = pd.read_csv(d / "poverty.csv").set_index("group")
    ineq = pd.read_csv(d / "inequality.csv")
    dec = pd.read_csv(d / "distribution_decile.csv")
    age = pd.read_csv(d / "distribution_age.csv").set_index("age_group")
    return {
        "rate": 100 * s["revenue_neutral_rate"],
        "ubi": b.loc["UBI (gross)", "reform"],
        "eitc": b.loc["Simple EITC", "reform"],
        "ss": b.loc["Social Security", "reform"],
        "snap": b.loc["SNAP", "reform"],
        "transfer": b.loc["Net transfer: UBI minus flat tax, where positive", "reform"],
        "pov": pov.loc["All people", "poverty_reform"],
        "pov_ch": pov.loc["All people", "poverty_change_pp"],
        "child_ch": pov.loc["Children (under 18)", "poverty_change_pp"],
        "adult_ch": pov.loc["Adults (18-64)", "poverty_change_pp"],
        "senior_ch": pov.loc["People 65+", "poverty_change_pp"],
        "deep_ch": pov.loc["All people", "deep_poverty_change_pp"],
        "gini": ineq.change.iloc[0],
        "dec_lo": dec["pct_change"].iloc[:5].min(),
        "dec_hi_loss": dec["pct_change"].iloc[5:].min(),
        "gain_deciles": int((dec["pct_change"] > 0).sum()),
        "senior_pct": age.loc["65+", "pct_change"],
        "base_pov": pov.loc["All people", "poverty_baseline"],
        "exempt": b.loc["Earnings exemption (removed from the flat tax base)", "reform"]
        if "Earnings exemption (removed from the flat tax base)" in b.index
        else 0.0,
    }


def main(roots):
    roots = [Path(r) for r in roots]
    rows = [(label, load(roots, sc)) for sc, label in STAGES]
    rows = [(l, r) for l, r in rows if r]
    cols = [l for l, _ in rows]
    lines = ["| | " + " | ".join(cols) + " |", "|---|" + "---|" * len(cols)]

    def add(name, key, fmt):
        lines.append(f"| {name} | " + " | ".join(fmt(r[key]) for _, r in rows) + " |")

    add("**Revenue-neutral rate**", "rate", lambda v: f"**{v:.2f}%**")
    add("UBI cost ($B)", "ubi", lambda v: f"{v:,.0f}")
    add("Earnings exempted from the flat tax ($B)", "exempt", lambda v: f"{v:,.0f}")
    add("Simple EITC ($B)", "eitc", lambda v: f"{v:,.0f}")
    add("Social Security paid ($B)", "ss", lambda v: f"{v:,.0f}")
    add("SNAP ($B)", "snap", lambda v: f"{v:,.0f}")
    add("Net transfer ($B)", "transfer", lambda v: f"{v:,.0f}")
    add(f"SPM poverty (baseline {rows[0][1]['base_pov']:.1f}%)", "pov", lambda v: f"{v:.1f}%")
    add("Poverty change (pp)", "pov_ch", lambda v: f"{v:+.1f}")
    add("Child poverty change (pp)", "child_ch", lambda v: f"{v:+.1f}")
    add("Adults 18-64 poverty change (pp)", "adult_ch", lambda v: f"{v:+.1f}")
    add("65+ poverty change (pp)", "senior_ch", lambda v: f"{v:+.1f}")
    add("Deep poverty change (pp)", "deep_ch", lambda v: f"{v:+.1f}")
    add("Gini change", "gini", lambda v: f"{v:+.3f}")
    add("Deciles that gain on average (of 10)", "gain_deciles", lambda v: f"{v}")
    add("Largest average loss, deciles 6-10", "dec_hi_loss", lambda v: f"{v:.1f}%")
    add("Change for people 65+ (net income)", "senior_pct", lambda v: f"{v:+.1f}%")
    print("\n".join(lines))


if __name__ == "__main__":
    main(sys.argv[1:])
