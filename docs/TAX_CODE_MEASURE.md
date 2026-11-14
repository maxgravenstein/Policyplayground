# How much smaller would the tax code be?

Measured on 2026-11-14 from the official text of Title 26 (the Internal Revenue Code), current through Public Law 119-142 (November 10, 2026), published by the House Office of the Law Revision Counsel (uscode.house.gov, XML release).

## Method

- **Words of law text** in each section: heading and body only. Editorial notes, amendment histories and source credits are not law and are left out.
- Each section is classified under `docs/SPEC_v2.md` as **removed**, **changed** (stays, but is rewritten), **kept**, or **already repealed**. The rules and a reason for each are in `tools/classify_usc26.py`; the result for every section is in `outputs/tax_code/usc26_classified.csv`.
- **Changed** sections are counted as kept text. Many will shrink (for example, retirement plan and charitable rules lose their individual parts), so this is a conservative measure.
- **New text** the reform needs is estimated by comparison with similar sections today. It is a range, not a count.
- Only the statute is measured. Regulations, IRS guidance and forms are much larger and are not counted.

## The code today

- **1,763,385 words** of law text in **2,162 sections** (1,900 in force; 3,837 words in sections already repealed or reserved).

## Result

| Category | Sections | Words | Share of law in force |
|---|---|---|---|
| Removed | 277 | 328,830 | 18.7% |
| Changed | 166 | 211,651 | 12.0% |
| Kept | 1,457 | 1,219,067 | 69.3% |
| Added (estimate) | - | 35,000 to 61,100 | 2.0% to 3.5% |

**Net effect (conservative):** from 1,759,548 words in force to about 1,465,718 to 1,491,818 words: **15% to 17% smaller.**

If half of the text in changed sections also goes (a plausible outcome), the code is about **23% smaller.**

## What is removed, by area

| Area | Sections | Words |
|---|---|---|
| Business credits and preferences | 52 | 81,023 |
| Exclusions from income and tax-exempt bonds (carve-outs) | 48 | 76,255 |
| Individual income tax: rates, filing status, deductions, exemptions, personal credits | 43 | 68,027 |
| Payroll taxes (FICA, self-employment, 3.8% investment tax, railroad, federal unemployment) | 42 | 53,255 |
| Estate, gift and generation-skipping taxes | 92 | 50,270 |
| **Total removed** | **277** | **328,830** |

## Largest removed sections

| Section | Heading | Words |
|---|---|---|
| 42 | Low-income housing credit | 15,136 |
| 3121 | Definitions | 12,959 |
| 143 | Mortgage revenue bonds: qualified mortgage bond and qualified veterans’ mortgage bond | 7,735 |
| 142 | Exempt facility bond | 7,298 |
| 3306 | Definitions | 6,489 |
| 1 | Tax imposed | 5,804 |
| 148 | Arbitrage | 5,772 |
| 2032A | Valuation of certain farm, etc., real property | 5,225 |
| 1402 | Definitions | 4,858 |
| 220 | Archer MSAs | 4,671 |
| 199A | Qualified business income | 4,605 |
| 30B | Alternative motor vehicle credit | 4,600 |
| 223 | Health savings accounts | 4,228 |
| 144 | Qualified small issue bond; qualified student loan bond; qualified redevelopment bond | 4,179 |
| 1202 | Partial exclusion for gain from certain small business stock | 4,160 |

## Largest changed sections (kept, but rewritten)

| Section | Heading | Words | Change |
|---|---|---|---|
| 401 | Qualified pension, profit-sharing, and stock bonus plans | 24,995 | Qualified plans: post-reform contributions taxed when earned |
| 170 | Charitable, etc., contributions and gifts | 14,979 | Charitable contributions: individual deduction goes; business part stays |
| 408 | Individual retirement accounts | 11,122 | IRAs: post-reform contributions taxed when earned |
| 163 | Interest | 8,413 | Interest: business part stays; home mortgage and investment interest for people go |
| 404 | Deduction for contributions of an employer to an employees’ trust or annuity plan and compensation under a deferred-payment plan | 6,739 | Employer deduction for plan contributions: same change |
| 402 | Taxability of beneficiary of employees’ trust | 6,690 | Taxation of plan beneficiaries: Roth-style for post-reform money |
| 403 | Taxation of employee annuities | 3,877 | Annuity plans: same change |
| 101 | Certain death benefits | 3,863 | Life insurance proceeds: taxed as inheritance cash |
| 45Q | Credit for carbon oxide sequestration | 3,840 | Carbon capture: kept for permanent storage only |
| 457 | Deferred compensation plans of State and local governments and tax-exempt organizations | 3,731 | Government and nonprofit deferred compensation: same change |
| 1250 | Gain from dispositions of certain depreciable realty | 3,645 | Capital gains: individual rates and holding-period distinctions mostly no longer matter |
| 165 | Losses | 3,056 | Losses: business part stays; personal casualty losses go |

## New text the reform needs (estimate)

| Item | Words (low) | Words (high) | Basis |
|---|---|---|---|
| Flat tax on individuals and the tax base (replaces sections 1, 2, 3, 62, 63) | 2,000 | 4,000 | A short rate section and a base definition |
| Inheritance and gift rules (replace Subtitle B, 50,431 words) | 12,600 | 20,200 | 25-40% of today's estate and gift law: no exemptions per heir, but caps, valuation, trusts, payment over time |
| 21% tax on all businesses, owner credit, franking accounts, guard rules | 8,000 | 15,000 | 2-3 times today's pass-through deduction (199A, 4,605 words) plus base erosion tax (59A, 2,548) |
| Broker basis adjustment for taxed retained profit | 2,000 | 4,000 | Like today's broker reporting (6045, 2,116 words) plus basis rules |
| Employer insurance premium (replaces federal unemployment tax, 17,893 words) | 5,400 | 8,900 | 30-50% of today's unemployment tax chapter |
| Simple automatic EITC for the transition (may sit outside Title 26) | 2,000 | 3,000 | Like today's EITC section (32, 2,764 words) |
| Retirement accounts: before and after the reform | 2,000 | 4,000 | Transition rules |
| Home sale gains: inflation-indexed basis | 1,000 | 2,000 | One short section |
| **Total** | **35,000** | **61,100** | |

## By subtitle

| Subtitle | Today (words) | After (kept + changed) | Change |
|---|---|---|---|
| A. Income Taxes | 1,071,830 | 838,476 | -22% |
| B. Estate and Gift Taxes | 50,431 | 0 | -100% |
| C. Employment Taxes | 64,348 | 16,990 | -74% |
| D. Miscellaneous Excise Taxes | 104,497 | 104,038 | -0% |
| E. Alcohol, Tobacco, and Certain Other Excise Taxes | 60,044 | 59,797 | -0% |
| F. Procedure and Administration | 347,476 | 346,684 | -0% |
| G. The Joint Committee on Taxation | 1,370 | 1,370 | +0% |
| H. Financing of Presidential Election Campaigns | 10,269 | 10,252 | -0% |
| I. Trust Fund Code | 11,203 | 11,203 | +0% |
| J. Coal Industry Health Benefits | 10,006 | 10,006 | +0% |
| K. Group Health Plan Requirements | 31,911 | 31,902 | -0% |

The new text is not in this table. Most of it goes into Subtitle A (business tax, basis) and replaces Subtitle B (inheritances) and part of Subtitle C (employer premium).

## What this means

1. **The statute shrinks by about 15-25%, not by half.** About 70% of the code is business, international, retirement-plan, excise and procedure law that the reform keeps.
2. **The part that households deal with almost disappears:** brackets, filing status, deductions, personal credits, payroll and self-employment taxes, and the estate and gift taxes.
3. **The bigger saving is in compliance, not pages.** With one flat rate withheld at source and no deductions, most wage earners and retirees would not need to file a return. Returns remain for business income, capital gains and inheritances.
4. **Business complexity stays about the same.** The 21% tax on pass-throughs, the owner credit and franking accounts add text for partnerships and S corporations.
5. **Word counts are only a proxy.** A short section can be hard to apply, and a long one easy. Regulations, which are much longer than the statute, would shrink in proportion for the removed areas.

## Judgment calls to check

- **ABLE accounts for disabled people (529A):** marked changed, not removed. Under 'no carve-outs' they would go; that hurts disabled savers. A decision for you.
- **Railroad retirement tax (3201-3241):** assumed to go with the other payroll taxes. The spec does not mention it.
- **Private activity bonds (141-150):** removed, because bond interest becomes taxable. State and local governments would pay more to borrow.
- **Corporate minimum tax:** kept (only the individual AMT goes). The spec does not mention it.
- **Excise taxes, procedure, health plan rules:** kept, because the spec does not change them.
- **Exclusions (101-140):** most removed as carve-outs. A few that cover government payments (disaster relief, foster care, cost-sharing) are kept, consistent with 'government payments are not taxed'.
