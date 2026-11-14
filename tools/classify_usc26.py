"""Classify each section of Title 26 under spec v2 (docs/SPEC_v2.md).

Usage: python tools/classify_usc26.py outputs/tax_code/usc26_sections.csv outputs/tax_code/usc26_classified.csv

Categories:
  removed   the section goes away under spec v2
  changed   the section stays but is rewritten (counted as kept text)
  kept      the section stays as it is
  repealed  already repealed, omitted, reserved or renumbered today

These are judgment calls at the level of whole sections. Each rule has a
reason. A section that is mostly kept but loses a part (for example, the
individual parts of section 163 or 164) is "changed".
"""

import csv
import re
import sys


def key(sec: str):
    """Sort and compare section numbers like '45Z', '1400Z-2', '59A'."""
    sec = sec.replace("\u2013", "-").replace("\u2014", "-")
    m = re.match(r"(\d+)([A-Z]*)(?:-(\d+))?", sec)
    if not m:
        return (10**9, sec, 0)
    return (int(m.group(1)), m.group(2), int(m.group(3) or 0))


def between(sec, lo, hi):
    return key(lo) <= key(sec) <= key(hi)


# Section-level rules: (category, reason). Checked first.
SECTION_RULES = {
    # Subchapter A, part I: tax on individuals
    "1": ("removed", "Brackets, capital gains rates, kiddie tax: replaced by one flat rate (new text)"),
    "2": ("removed", "Filing status definitions (head of household, surviving spouse)"),
    "3": ("removed", "Tax tables"),
    "5": ("removed", "Cross references for individuals"),
    # Credits kept
    "27": ("kept", "Foreign tax credit (cross reference)"),
    "31": ("kept", "Credit for tax withheld on wages (needed for withholding)"),
    "33": ("kept", "Tax withheld at source on nonresident aliens"),
    "34": ("kept", "Certain uses of fuels (excise refund mechanism)"),
    "36B": ("kept", "ACA premium tax credit (kept, counting the UBI)"),
    "32": ("removed", "EITC: replaced by the simple automatic EITC during the transition (new text), then gone"),
    "38": ("kept", "General business credit (framework for kept credits)"),
    "39": ("kept", "Carryback and carryforward of unused credits"),
    "40B": ("changed", "Sustainable aviation fuel credit: kept only on measured lifecycle emissions, like 45Z"),
    "41": ("kept", "Research credit (positive externality)"),
    "45": ("kept", "Renewable electricity production credit (clean energy)"),
    "45C": ("kept", "Orphan drug credit (research)"),
    "45J": ("kept", "Advanced nuclear power production credit (clean energy)"),
    "45Q": ("changed", "Carbon capture: kept for permanent storage only"),
    "45U": ("kept", "Zero-emission nuclear production credit"),
    "45V": ("kept", "Clean hydrogen credit (paid by lifecycle emissions)"),
    "45Y": ("kept", "Clean electricity production credit"),
    "45Z": ("changed", "Clean fuel credit: kept only on measured lifecycle emissions"),
    "46": ("kept", "Amount of investment credit (rules for kept credits)"),
    "48": ("kept", "Energy credit"),
    "48E": ("kept", "Clean electricity investment credit"),
    "49": ("kept", "At-risk rules for investment credit"),
    "50": ("kept", "Other rules for investment credit"),
    "53": ("changed", "Minimum tax credit: individual AMT removed, corporate minimum tax stays (decided 2026-11-14)"),
    "59A": ("kept", "Base erosion tax (international)"),
    # Subchapter B
    "61": ("changed", "Gross income: becomes the flat tax base"),
    "62": ("removed", "Adjusted gross income (concept not needed)"),
    "63": ("removed", "Taxable income for individuals (standard deduction)"),
    "67": ("removed", "2% floor on miscellaneous itemized deductions"),
    "68": ("removed", "Overall limit on itemized deductions"),
    "86": ("changed", "Social Security: current-law taxation kept, per person, indexed thresholds"),
    "87": ("removed", "Alcohol fuel credit inclusion"),
    "101": ("changed", "Life insurance proceeds: taxed as inheritance cash"),
    "102": ("changed", "Gifts and inheritances: now taxed under the new inheritance rules"),
    "103": ("kept", "Interest on state and local bonds stays tax-exempt (decided 2026-11-14)"),
    "108": ("kept", "Discharge of debt (insolvency rules)"),
    "109": ("kept", "Lessee improvements"),
    "110": ("kept", "Lessee construction allowances"),
    "111": ("kept", "Recovery of tax benefit items"),
    "115": ("kept", "Income of states and municipalities"),
    "118": ("kept", "Contributions to capital of a corporation"),
    "122": ("kept", "Reduced military retirement pay (government payment)"),
    "126": ("kept", "Government cost-sharing payments"),
    "131": ("kept", "Foster care payments (government payment)"),
    "139": ("kept", "Disaster relief payments (government payment)"),
    "140": ("kept", "Cross references"),
    "163": ("changed", "Interest: business part stays; home mortgage and investment interest for people go"),
    "164": ("changed", "Taxes: business part stays; state and local tax deduction for people goes"),
    "165": ("changed", "Losses: business part stays; personal casualty losses go"),
    "170": ("changed", "Charitable contributions: individual deduction goes; business part stays"),
    "172": ("changed", "Net operating loss: unlimited carryforward against all income"),
    "179D": ("removed", "Energy-efficient commercial building deduction"),
    "181": ("removed", "Film and TV production expensing (special preference)"),
    "190": ("removed", "Architectural barrier removal deduction (special preference)"),
    "193": ("removed", "Tertiary injectants (fossil fuel preference)"),
    "199A": ("removed", "Pass-through income deduction: replaced by the 21% business tax with credit"),
    "263": ("changed", "Capital expenditures: immediate write-off of drilling costs removed"),
    "401": ("changed", "Qualified plans: post-reform contributions taxed when earned"),
    "402": ("changed", "Taxation of plan beneficiaries: Roth-style for post-reform money"),
    "403": ("changed", "Annuity plans: same change"),
    "404": ("changed", "Employer deduction for plan contributions: same change"),
    "408": ("changed", "IRAs: post-reform contributions taxed when earned"),
    "457": ("changed", "Government and nonprofit deferred compensation: same change"),
    "530A": ("kept", "Trump accounts for children: kept with other 529-like accounts (decided 2026-11-14)"),
    "529": ("kept", "Education savings plans: kept (decided 2026-11-14)"),
    "529A": ("kept", "ABLE accounts for disabled people: kept (decided 2026-11-14)"),
    "530": ("kept", "Coverdell education savings accounts: kept with 529-like accounts (decided 2026-11-14)"),
    "613": ("removed", "Percentage depletion (fossil fuel preference)"),
    "613A": ("removed", "Percentage depletion for oil and gas"),
    "1014": ("kept", "Step-up at death: kept for assets taxed at inheritance"),
    "1015": ("changed", "Basis of gifts: carryover only for exempt items"),
    "1202": ("removed", "Exclusion of gain on small business stock (carve-out)"),
    "1211": ("changed", "Capital losses: unlimited offset and carryforward"),
    "1212": ("changed", "Capital loss carryover: same"),
    "1301": ("removed", "Farm income averaging (not needed with one flat rate)"),
}

# Range rules: (lo, hi, category, reason). Checked in order after section rules.
RANGE_RULES = [
    # Subtitle A, chapter 1, subchapter A
    ("11", "15", "kept", "Corporate tax (21%) and rate-change rules"),
    ("21", "26", "removed", "Nonrefundable personal credits (child care, elderly, adoption, CTC, education, saver's, home energy)"),
    ("27", "30D", "removed", "Other personal credits (vehicles, refueling property)"),
    ("31", "37", "removed", "Refundable personal credits not kept"),
    ("38", "45Z", "removed", "Business credits removed under spec v2 Section 8.4"),
    ("46", "50", "removed", "Investment credits removed (rehabilitation, advanced coal, gasification, advanced energy projects, chips manufacturing)"),
    ("51", "52", "removed", "Work Opportunity Credit"),
    ("54", "54ZZ", "removed", "Tax credit bonds"),
    ("55", "59", "changed", "AMT: individual AMT removed; corporate minimum tax stays"),
    # Subchapter B
    ("64", "66", "kept", "Ordinary income and loss; community income"),
    ("71", "91", "kept", "Items included in gross income"),
    ("101", "140", "removed", "Exclusions from gross income: carve-outs under 'no carve-outs' (employer health phased in, fringe benefits, home sale exclusion, tax-exempt interest, scholarships, and others)"),
    ("141", "150", "kept", "Private activity bond rules: kept with tax-exempt bonds (decided 2026-11-14)"),
    ("151", "153", "removed", "Personal exemptions and dependents"),
    ("161", "199A", "kept", "Business deductions"),
    ("211", "226", "removed", "Additional itemized deductions for individuals (medical, IRA, student loans, HSA, tips, overtime, and others)"),
    ("241", "250", "kept", "Special deductions for corporations"),
    ("261", "280H", "kept", "Items not deductible (business rules)"),
    ("281", "281", "kept", "Terminal railroad corporations"),
    ("291", "291", "kept", "Corporate preference items"),
    # Subchapters C to T
    ("301", "385", "kept", "Corporate distributions and adjustments"),
    ("401", "436", "kept", "Deferred compensation and plan funding rules"),
    ("441", "483", "kept", "Accounting periods and methods"),
    ("501", "530", "kept", "Exempt organizations"),
    ("531", "565", "kept", "Accumulated earnings and personal holding company taxes (used by the guard rules)"),
    ("581", "597", "kept", "Banking institutions"),
    ("611", "638", "kept", "Natural resources"),
    ("641", "692", "changed", "Estates and trusts: look-through rules for inheritances"),
    ("701", "777", "changed", "Partnerships: 21% business tax and owner credit"),
    ("801", "848", "kept", "Insurance companies"),
    ("851", "860L", "kept", "Mutual funds and REITs"),
    ("861", "999", "kept", "International rules (including the foreign tax credit)"),
    ("1001", "1092", "kept", "Gain or loss on disposition (basis rules)"),
    ("1201", "1298", "changed", "Capital gains: individual rates and holding-period distinctions mostly no longer matter"),
    ("1301", "1351", "kept", "Readjustment of tax between years"),
    ("1352", "1359", "kept", "International shipping tonnage tax"),
    ("1361", "1379", "changed", "S corporations: 21% business tax and owner credit"),
    ("1381", "1388", "kept", "Cooperatives"),
    ("1391", "1397F", "removed", "Empowerment zones"),
    ("1398", "1399", "kept", "Bankruptcy cases"),
    ("1400", "1400U-3", "removed", "Place-based zones and expired regional incentives"),
    ("1400Z-1", "1400Z-2", "removed", "Opportunity zones"),
    # Subtitle A, other chapters
    ("1401", "1403", "removed", "Self-employment tax"),
    ("1411", "1411", "removed", "Net investment income tax (3.8%)"),
    ("1441", "1465", "kept", "Withholding on nonresident aliens and foreign corporations"),
    ("1471", "1474", "kept", "FATCA reporting"),
    ("1501", "1564", "kept", "Consolidated returns and controlled groups"),
    # Subtitle B
    ("2001", "2801", "removed", "Estate, gift and generation-skipping taxes and special valuation: replaced by the inheritance and gift rules (new text)"),
    # Subtitle C
    ("3101", "3128", "removed", "FICA: Social Security and Medicare payroll taxes"),
    ("3201", "3241", "removed", "Railroad retirement payroll tax (decided 2026-11-14)"),
    ("3301", "3311", "removed", "Federal unemployment tax: replaced by the employer insurance premium (new text)"),
    ("3131", "3134", "removed", "COVID-era payroll tax credits for leave and retention"),
    ("3321", "3322", "removed", "Railroad unemployment repayment tax"),
    ("3401", "3456", "kept", "Income tax withholding at source"),
    ("3501", "3512", "changed", "General employment tax rules: now for the employer premium"),
    # Subtitles D to K
    ("4001", "5000C", "kept", "Excise taxes (not part of the reform)"),
    ("5001", "5891", "kept", "Alcohol and tobacco taxes"),
    ("6001", "7874", "kept", "Procedure and administration"),
    ("8001", "8023", "kept", "Joint Committee on Taxation"),
    ("9001", "9042", "kept", "Presidential election campaign financing"),
    ("9500", "9602", "kept", "Trust funds"),
    ("9701", "9722", "kept", "Coal industry health benefits"),
    ("9801", "9834", "kept", "Group health plan requirements"),
]


def classify(row):
    sec = row["section"]
    if row["status"] in ("repealed", "omitted", "reserved", "renumbered") or row["heading"].strip().startswith(("Repealed", "Omitted", "Reserved")):
        return "repealed", "Already repealed, omitted, reserved or renumbered"
    if sec in SECTION_RULES:
        return SECTION_RULES[sec]
    for lo, hi, cat, why in RANGE_RULES:
        if between(sec, lo, hi):
            return cat, why
    return "kept", "No rule: kept by default"


def main(src, out):
    with open(src) as f:
        rows = list(csv.DictReader(f))
    for r in rows:
        r["category"], r["reason"] = classify(r)
    with open(out, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    unmatched = [r["section"] for r in rows if r["reason"].startswith("No rule")]
    print(f"classified {len(rows)} sections; {len(unmatched)} with no rule: {unmatched[:20]}")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
