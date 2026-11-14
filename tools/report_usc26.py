"""Write docs/TAX_CODE_MEASURE.md from the classified Title 26 sections.

Usage: python tools/report_usc26.py outputs/tax_code/usc26_classified.csv docs/TAX_CODE_MEASURE.md
"""

import sys

import pandas as pd

from classify_usc26 import between

RELEASE = "Public Law 119-142 (November 10, 2026)"

# Areas for removed text, by section number.
AREAS = [
    ("Individual income tax: rates, filing status, deductions, exemptions, personal credits", [
        ("1", "5"), ("21", "37"), ("62", "63"), ("67", "68"), ("151", "153"), ("211", "226"), ("1301", "1301"),
    ]),
    ("Exclusions from income (carve-outs)", [
        ("101", "150"), ("529", "530A"), ("1202", "1202"),
    ]),
    ("Payroll taxes (FICA, self-employment, 3.8% investment tax, railroad, federal unemployment)", [
        ("1401", "1411"), ("3101", "3134"), ("3201", "3241"), ("3301", "3322"),
    ]),
    ("Estate, gift and generation-skipping taxes", [("2001", "2801")]),
    ("Business credits and preferences", [
        ("38", "54ZZ"), ("87", "87"), ("179D", "199A"), ("613", "613A"), ("1391", "1400Z-2"),
    ]),
]

# New text the reform adds (words): (item, low, high, basis).
ADDED = [
    ("Flat tax on individuals and the tax base (replaces sections 1, 2, 3, 62, 63)", 2000, 4000,
     "A short rate section and a base definition"),
    ("Inheritance and gift rules (replace Subtitle B, 50,431 words)", 12600, 20200,
     "25-40% of today's estate and gift law: no exemptions per heir, but caps, valuation, trusts, payment over time"),
    ("21% tax on all businesses, owner credit, franking accounts, guard rules", 8000, 15000,
     "2-3 times today's pass-through deduction (199A, 4,605 words) plus base erosion tax (59A, 2,548)"),
    ("Broker basis adjustment for taxed retained profit", 2000, 4000,
     "Like today's broker reporting (6045, 2,116 words) plus basis rules"),
    ("Employer insurance premium (replaces federal unemployment tax, 17,893 words)", 5400, 8900,
     "30-50% of today's unemployment tax chapter"),
    ("Simple automatic EITC for the transition (may sit outside Title 26)", 2000, 3000,
     "Like today's EITC section (32, 2,764 words)"),
    ("Retirement accounts: before and after the reform", 2000, 4000, "Transition rules"),
    ("Home sale gains: inflation-indexed basis", 1000, 2000, "One short section"),
]


def area_of(sec):
    for name, ranges in AREAS:
        if any(between(sec, lo, hi) for lo, hi in ranges):
            return name
    return "Other"


def fmt(n):
    return f"{n:,.0f}"


def main(src, out):
    d = pd.read_csv(src, dtype=str)
    d["words"] = d.words.astype(int)
    total = d.words.sum()
    in_force = d[d.category != "repealed"]
    by_cat = d.groupby("category").agg(sections=("section", "count"), words=("words", "sum"))
    removed = d[d.category == "removed"].copy()
    removed["area"] = removed.section.map(area_of)
    by_area = removed.groupby("area").agg(sections=("section", "count"), words=("words", "sum")).sort_values("words", ascending=False)
    add_lo = sum(a[1] for a in ADDED)
    add_hi = sum(a[2] for a in ADDED)
    rem = by_cat.loc["removed", "words"]
    chg = by_cat.loc["changed", "words"]
    kept = by_cat.loc["kept", "words"]
    rep = by_cat.loc["repealed", "words"]
    base = total - rep
    new_lo = kept + chg + add_lo
    new_hi = kept + chg + add_hi
    new_lo_half = kept + chg / 2 + add_lo

    sub = d.groupby(["subtitle", "subtitle_heading"]).words.sum()
    sub_after = d[d.category.isin(["kept", "changed"])].groupby(["subtitle", "subtitle_heading"]).words.sum()

    L = []
    L.append("# How much smaller would the tax code be?\n")
    L.append(f"Measured on 2026-11-14 from the official text of Title 26 (the Internal Revenue Code), "
             f"current through {RELEASE}, published by the House Office of the Law Revision Counsel "
             "(uscode.house.gov, XML release).\n")
    L.append("## Method\n")
    L.append("- **Words of law text** in each section: heading and body only. Editorial notes, amendment "
             "histories and source credits are not law and are left out.")
    L.append("- Each section is classified under `docs/SPEC_v2.md` as **removed**, **changed** (stays, but is "
             "rewritten), **kept**, or **already repealed**. The rules and a reason for each are in "
             "`tools/classify_usc26.py`; the result for every section is in "
             "`outputs/tax_code/usc26_classified.csv`.")
    L.append("- **Changed** sections are counted as kept text. Many will shrink (for example, retirement plan "
             "and charitable rules lose their individual parts), so this is a conservative measure.")
    L.append("- **New text** the reform needs is estimated by comparison with similar sections today. It is a "
             "range, not a count.")
    L.append("- Only the statute is measured. Regulations, IRS guidance and forms are much larger and are not "
             "counted.\n")

    L.append("## The code today\n")
    L.append(f"- **{fmt(total)} words** of law text in **{len(d):,} sections** "
             f"({len(in_force):,} in force; {fmt(rep)} words in sections already repealed or reserved).\n")

    L.append("## Result\n")
    L.append("| Category | Sections | Words | Share of law in force |")
    L.append("|---|---|---|---|")
    for cat in ["removed", "changed", "kept"]:
        L.append(f"| {cat.capitalize()} | {by_cat.loc[cat, 'sections']:,} | {fmt(by_cat.loc[cat, 'words'])} | {100 * by_cat.loc[cat, 'words'] / base:.1f}% |")
    L.append(f"| Added (estimate) | - | {fmt(add_lo)} to {fmt(add_hi)} | {100 * add_lo / base:.1f}% to {100 * add_hi / base:.1f}% |")
    L.append("")
    L.append(f"**Net effect (conservative):** from {fmt(base)} words in force to about "
             f"{fmt(new_lo)} to {fmt(new_hi)} words: **{100 * (1 - new_hi / base):.0f}% to "
             f"{100 * (1 - new_lo / base):.0f}% smaller.**\n")
    L.append(f"If half of the text in changed sections also goes (a plausible outcome), the code is about "
             f"**{100 * (1 - new_lo_half / base):.0f}% smaller.**\n")

    L.append("## What is removed, by area\n")
    L.append("| Area | Sections | Words |")
    L.append("|---|---|---|")
    for area, r in by_area.iterrows():
        L.append(f"| {area} | {r.sections:,} | {fmt(r.words)} |")
    L.append(f"| **Total removed** | **{by_area.sections.sum():,}** | **{fmt(by_area.words.sum())}** |\n")

    L.append("## Largest removed sections\n")
    L.append("| Section | Heading | Words |")
    L.append("|---|---|---|")
    for _, r in removed.sort_values("words", ascending=False).head(15).iterrows():
        L.append(f"| {r.section} | {r.heading} | {fmt(r.words)} |")
    L.append("")

    L.append("## Largest changed sections (kept, but rewritten)\n")
    L.append("| Section | Heading | Words | Change |")
    L.append("|---|---|---|---|")
    for _, r in d[d.category == "changed"].sort_values("words", ascending=False).head(12).iterrows():
        L.append(f"| {r.section} | {r.heading} | {fmt(r.words)} | {r.reason} |")
    L.append("")

    L.append("## New text the reform needs (estimate)\n")
    L.append("| Item | Words (low) | Words (high) | Basis |")
    L.append("|---|---|---|---|")
    for item, lo, hi, basis in ADDED:
        L.append(f"| {item} | {fmt(lo)} | {fmt(hi)} | {basis} |")
    L.append(f"| **Total** | **{fmt(add_lo)}** | **{fmt(add_hi)}** | |\n")

    L.append("## By subtitle\n")
    L.append("| Subtitle | Today (words) | After (kept + changed) | Change |")
    L.append("|---|---|---|---|")
    for (s, h), w in sub.items():
        a = sub_after.get((s, h), 0)
        L.append(f"| {s}. {h} | {fmt(w)} | {fmt(a)} | {100 * (a - w) / w:+.0f}% |")
    L.append("\nThe new text is not in this table. Most of it goes into Subtitle A (business tax, basis) and "
             "replaces Subtitle B (inheritances) and part of Subtitle C (employer premium).\n")

    L.append("## What this means\n")
    L.append(f"1. **The statute shrinks by about {100 * (1 - new_hi / base):.0f}-{100 * (1 - new_lo_half / base):.0f}%, "
             f"not by half.** About {100 * kept / base:.0f}% of the code is business, international, "
             "retirement-plan, excise and procedure law that the reform keeps.")
    L.append("2. **The part that households deal with almost disappears:** brackets, filing status, "
             "deductions, personal credits, payroll and self-employment taxes, and the estate and gift taxes.")
    L.append("3. **The bigger saving is in compliance, not pages.** With one flat rate withheld at source and "
             "no deductions, most wage earners and retirees would not need to file a return. Returns remain for "
             "business income, capital gains and inheritances.")
    L.append("4. **Business complexity stays about the same.** The 21% tax on pass-throughs, the owner credit "
             "and franking accounts add text for partnerships and S corporations.")
    L.append("5. **Word counts are only a proxy.** A short section can be hard to apply, and a long one easy. "
             "Regulations, which are much longer than the statute, would shrink in proportion for the removed "
             "areas.\n")

    L.append("## Decisions applied (2026-11-14)\n")
    L.append("- **Kept:** ABLE accounts (529A), education savings plans (529), Coverdell accounts (530) and the "
             "children's accounts (530A), with their tax benefits.")
    L.append("- **Kept:** tax-exempt interest on state and local bonds (103) and the private activity bond rules "
             "(141-150).")
    L.append("- **Kept:** the corporate minimum tax. Only the individual AMT goes.")
    L.append("- **Removed:** the railroad retirement payroll tax (3201-3241).\n")
    L.append("## Other judgment calls\n")
    L.append("- **Excise taxes, procedure, health plan rules:** kept, because the spec does not change them.")
    L.append("- **Exclusions (101-140):** most removed as carve-outs. A few that cover government payments "
             "(disaster relief, foster care, cost-sharing) are kept, consistent with 'government payments are "
             "not taxed'.\n")
    with open(out, "w") as f:
        f.write("\n".join(L))
    print("\n".join(L[:40]))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
