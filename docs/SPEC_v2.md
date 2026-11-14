# Spec v2: Flat Tax + UBI, full design

Status: design decisions as of 2026-11-14 (all proposals confirmed). This document replaces the original
spec (v1, in the first request) as the reference for the **policy**. The model
code does not yet follow it; see Section 14.

Marks used:
- **Decided**: the user chose it.
- **Proposed**: suggested, not yet confirmed. Listed again in Section 13.
- **Open**: left for later.

All dollar amounts are in 2026 dollars. "Index" means: raise each year by the
same formula as the HHS poverty guideline (consumer prices, CPI-U).

---

## 1. Purpose and principles

1. Replace the federal income tax, payroll taxes and most income-tested
   programs with one flat tax and a universal basic income (UBI).
2. **One rate, taxed once.** All personal income pays one flat rate. Business
   profit pays 21% at the business and the rest of the flat rate at the owner,
   with a credit, so it is taxed once.
3. **No carve-outs.** No deductions for people; for businesses, only credits
   that prevent double tax, reduce negative externalities, or fund research.
4. **Payments from the government are not taxed** (UBI, EITC in the transition).
   Legacy Social Security is taxed as under current law.
5. **"Higher of" rule** for earnings-based benefits that remain (Social Security
   in transition, SSDI): a person gets the higher of the benefit or their UBI.
6. **Gradual transition** on a fixed, announced schedule with a safety check.
   Old programs shrink by themselves because they count the UBI as income.
7. **Protect people who relied on the old rules:** retirees, people near
   retirement, survivors, dependents, disabled workers.
8. **Simple administration:** no tax return needed just to get the UBI; flat
   tax withheld at source; benefits paid automatically from data the
   government already has.

---

## 2. Timeline

| Period | Years after passage | What happens |
|---|---|---|
| **Phase 1** | Year 1 = the tax year after passage | Flat tax replaces income and payroll taxes. UBI for children and people 65+. Floors for Social Security beneficiaries. Simple EITC. Programs kept. |
| **Phase 2** | Years 2 to 6 | Partial UBI for adults 18-64 in five equal steps. Programs count the UBI and shrink. Employer health premiums enter the tax base in steps. |
| Safety-check delays | Up to year 8 | At most two one-year delays (Section 10). |
| **End state** | After the last step | Full UBI for all. SNAP, TANF, WIC and the EITC end. |
| Long tail | Decades | Legacy Social Security winds down (about 60 years). Housing aid: new vouchers until year 18, then attrition. |

---

## 3. Universal basic income

| Item | Rule | Status |
|---|---|---|
| Adult amount | $15,960 a year (2026 HHS poverty guideline, one person), indexed | Decided |
| Child amount | $3,000 a year, under 18, indexed | Decided |
| Adult age | 18 and over, including students living with parents | Decided |
| Phase 1 | Children: $3,000. People 65+: higher of Social Security or $15,960. Floors for survivor, dependent and SSDI beneficiaries (Section 5). Working-age adults: no UBI. | Decided |
| Phase 2 | Adults 18-64 get a partial UBI that rises in five equal steps of about $3,200 (indexed) to $15,960 | Decided |
| Tax | Not taxed | Decided |
| Phase-out | None | Decided |
| One national amount | No regional variation. States and cities work on cost of living (Section 9). | Decided |
| Eligibility | U.S. citizens, and lawful permanent residents after 5 years in qualified status (same rule as SNAP; refugees and asylees exempt from the wait) | Decided |
| Residence | Must live in the United States | Decided |
| Prison | Suspended during a prison term, as SSA does for benefits | Decided |
| Payment | Monthly, run by SSA (Treasury makes the payments) | Decided |
| Child UBI payee | The primary caregiver registered with SSA. Shared custody: split 50/50 by agreement or court order. | Decided |
| Debt collection | Child support and federal debts may be offset, as today. Private creditors may take at most 15% of each payment. | Decided |

---

## 4. Flat tax

### 4.1 Rate and unit

| Item | Rule | Status |
|---|---|---|
| Rate | One rate on all personal income. Set in law for each year of the schedule so that each step is revenue-neutral on paper. | Decided |
| Rate path (estimate only) | About 24% in phase 1, rising about 2 points per phase 2 step to the high 30s. Must be costed (Section 14). | Estimate |
| Unit | Each person on their own income (individual filing) | Decided |
| Deductions and credits | None, except: the simple EITC during the transition (Section 6) and the business tax credit (Section 8) | Decided |
| Collection | Withheld at source on wages and other payments | Decided |

### 4.2 Tax base

Taxed at the flat rate:
- wages and salaries, including 401(k) and other pre-tax deferrals
- self-employment income; owner payouts from businesses (Section 8)
- all interest, including today's tax-exempt interest
- dividends (with the business credit, Section 8)
- capital gains, at the same rate as wages (gains on shares only above the
  company's taxed retained profit, Section 8.3)
- pensions and withdrawals from pre-reform retirement balances (4.3)
- rent and all other income
- **employer-paid health insurance premiums**, phased in: 20% of the premium at
  phase 2 step 1, 40% at step 2, and so on, 100% from the last step. Employers
  already report the cost on the W-2.
- Social Security in phase 1 and legacy benefits: only the taxable part under
  current-law rules (Section 5.3)

Not taxed: the UBI, SSI, the EITC, and other government payments listed as
untaxed in this spec.

### 4.3 Retirement accounts

| Money | Rule | Status |
|---|---|---|
| Saved before the reform (never taxed) | Taxed at the flat rate when withdrawn, as today | Decided |
| Saved after the reform | Taxed when earned (going in); withdrawals tax-free (like a Roth account) | Decided |

### 4.4 Losses

Net losses carry forward without limit and offset any income in later years.
No carryback. Losses stay with the person. **Decided.**

### 4.5 Home sales

The home sale exclusion ($250,000 / $500,000) is removed. On a primary home,
only the gain above inflation is taxed: the purchase price and improvements
are indexed to the sale date with the UBI index. **Decided.**

### 4.6 Payroll taxes

Employee and employer Social Security and Medicare taxes and self-employment
tax are removed. Replaced by the employer insurance premium (Section 7.3) and
the flat tax. **Decided.**

---

## 5. Social Security

### 5.1 Phase 1

| Who | Rule | Status |
|---|---|---|
| People 65+ on Social Security | Higher of benefit or UBI: UBI top-up = max($15,960 - benefit, 0) | Decided |
| Survivor and dependent beneficiaries, any age | Higher of benefit or own UBI (children $3,000, adults $15,960) | Decided |
| SSDI beneficiaries, any age | Same floor: higher of benefit or $15,960 | Decided |
| Early retirement, 62-64, already receiving benefits at passage | Same floor: higher of benefit or $15,960 | Decided |
| Early retirement, 62-64, claiming after passage | Benefit as today; no floor until 65 (avoids early claiming just to get the floor) | Decided |
| Tax | Current-law rules, per person (5.3) | Decided |

### 5.2 Wind-down (no new benefits earned after the reform)

The payroll tax ends, so nobody earns new Social Security after the reform.

| Group | Rule | Status |
|---|---|---|
| Already receiving retirement, survivor or dependent benefits | Higher of benefit or UBI, for life | Decided |
| Workers who paid in, **age 57+ at passage** | At retirement: the more of (a) higher of earned benefit or UBI, or (b) UBI + 40% of the earned part | Decided |
| Workers who paid in, **under 57 at passage** | At retirement: UBI + 40% of the earned part | Decided |
| New workers | UBI only | Decided |
| Earned part | Current-law benefit x (years of covered work before the reform / 35) | Decided |
| Funding | The Social Security trust fund pays legacy benefits first; then general revenue | Decided |
| End state | Social Security is removed; only legacy benefits remain, ending as recipients die (about 60 years) | Decided |

Note: the earned part ramps up by itself with years paid in, so older workers
get more without a separate age ramp.

### 5.3 Tax on Social Security (phase 1 and legacy benefits)

For each person separately (spouses do not combine):

1. Other income = the person's flat tax base without Social Security.
2. Provisional income = other income + 50% of the person's Social Security.
3. Taxable part:
   - provisional income up to $25,000: none
   - $25,000 to $34,000: the lesser of 50% of Social Security, or 50% of
     (provisional income - $25,000)
   - above $34,000: the lesser of 85% of Social Security, or
     85% of (provisional income - $34,000) + the lesser of $4,500 or 50% of
     Social Security
4. The taxable part is taxed at the flat rate.
5. No senior deduction.
6. The $25,000 and $34,000 thresholds start at today's values and are indexed.

**Decided.** Note: "other income" is broader than today's AGI (it includes
employer health premiums and pre-tax deferrals), so some people have slightly
more Social Security taxed than today.

---

## 6. Earned income and child credits

| Item | Rule | Status |
|---|---|---|
| CTC | Removed from phase 1. The child UBI ($3,000) replaces it. | Decided |
| EITC, phase 1 | **Simple automatic EITC**: same purpose and similar amounts as today; earnings from employer wage reports; children from the child UBI register; phase-out on earnings only; paid automatically; no tax return. Not taxed. | Decided |
| EITC, phase 2 | Each family gets the higher of its simple EITC or the partial UBI its adults receive. The EITC disappears as the UBI grows. | Decided |
| EITC, end state | Gone | Decided |

---

## 7. Disability and unemployment

### 7.1 SSDI (permanent, above the UBI)

| Item | Rule | Status |
|---|---|---|
| Benefit | Higher of the SSDI benefit (today's formula) or the UBI. In practice: UBI + max(SSDI - $15,960, 0). | Decided |
| New cases | Continue after the reform. SSA keeps earnings records from employer wage reports. | Decided |
| Duration | For life (does not stop at 65) | Decided |
| Work | The earnings cliff is replaced by a 50% taper: the part above the UBI falls 50 cents per dollar earned | Decided |
| Family members | Higher of their auxiliary benefit or their own UBI | Decided |
| Disability test | Today's SSA test | Decided |
| Funding | Employer insurance premium (7.3) | Decided |

### 7.2 SSI

| Item | Rule | Status |
|---|---|---|
| Kept | Yes | Decided |
| Counts the UBI | No | Decided |
| Asset limit | $6,000 single, $9,000 couple (from $2,000 / $3,000), then indexed | Decided |
| Marriage penalty (couple = 1.5 x single) | Not addressed | Open |

### 7.3 Employer insurance premium

| Item | Rule | Status |
|---|---|---|
| What it funds | SSDI above the UBI, and the unemployment top-up | Decided |
| Who pays | All employers, including nonprofits and governments, on wages. Self-employed people pay it on their own earnings and are covered. | Decided |
| Who sets it | Set in law, the same way as the business tax rate | Decided |
| Unemployment part | Varies by employer: higher for employers who lay off more workers | Decided |
| Size (estimate) | About 0.3% of wages for SSDI and 0.2-0.3% for unemployment | Estimate |

### 7.4 Unemployment top-up

| Item | Rule | Status |
|---|---|---|
| Amount | 50% of lost wages, capped (for example at half the median wage) | Decided |
| Duration | 13 weeks; automatically up to 26 weeks when unemployment is high | Decided |
| Who runs it | States, under one federal standard | Decided |
| Funding | Employer insurance premium (7.3) | Decided |
| When it replaces today's unemployment insurance | By the end of phase 2; exact timing not set | Open |
| Exact cap and high-unemployment trigger | Not set | Open |

---

## 8. Business taxation

### 8.1 Rate and credit

| Item | Rule | Status |
|---|---|---|
| Business rate | **21%, fixed**, on the profit of **all businesses** (C-corporations, S-corporations, partnerships, and sole businesses unless they use the simple option below) | Decided |
| Owner credit | When profit is paid to owners, the owner counts the profit before business tax as income, pays the flat rate, and gets a credit for the 21% paid. Total: the flat rate, once. | Decided |
| Example | $100 profit, $21 business tax, $79 paid out. At a 36.75% flat rate the owner pays $36.75 - $21 = $15.75. Total $36.75. | - |

### 8.2 Guard rules

| Rule | Status |
|---|---|
| Owners who work in the business must take a reasonable salary, taxed at the flat rate | Decided |
| Personal use of business money, and loans to owners, count as payouts | Decided |
| Interest, dividends and rents earned inside a business pay the flat rate at once | Decided |
| Simple option: sole owners and very small businesses skip the business tax and pay the flat rate on their profit directly | Decided |

### 8.3 Details

| Item | Proposal | Status |
|---|---|---|
| Credit only for tax actually paid | Each business tracks the U.S. tax it paid and can attach credits to payouts only up to that amount (a "franking account", as in Australia) | Decided |
| Unused credit | Refunded | Decided |
| Foreign owners and tax-free retirement accounts | No credit; the 21% is final | Decided |
| Capital gains on shares | No double tax: each year, brokers add the company's taxed retained profit per share to the shareholder's cost basis; on sale, only the gain above that is taxed. Companies report taxed retained profit per share. | Decided |
| Small business limit for the simple option | Sole owners, and businesses with up to about $1 million revenue, indexed | Decided |
| Reasonable salary safe rule | An owner who pays themselves at least the lower of the business profit or about twice the median wage is not challenged; above that, a market-salary test (as for S-corporations today) | Decided |
| Full expensing | Not added; today's depreciation rules stay | Decided |


### 8.4 Business tax credits and preferences

Rule: remove business tax credits and preferences, except credits that
prevent double tax, credits that significantly reduce negative externalities
(pollution, emissions), and research credits (positive externality).
**Decided** (2026-11-14).

| Credit or preference | Rule | Status |
|---|---|---|
| Foreign tax credit | **Keep** (prevents double tax on profit earned abroad) | Decided |
| Owner credit for the 21% business tax | **Keep** (Section 8.1) | Decided |
| Research and development credit | **Keep** (research benefits others: a positive externality) | Decided |
| Orphan drug credit (research on rare diseases) | **Keep**, with the R&D credit | Decided |
| Clean electricity production and investment credits (45Y, 48E) | **Keep** | Decided |
| Nuclear production credit (45U) | **Keep** | Decided |
| Carbon capture credit (45Q) | **Keep for permanent storage only**; no credit when the CO2 is used to produce more oil | Decided |
| Clean fuel production credit (45Z) | Keep only if it pays on measured lifecycle emissions; otherwise remove | Decided |
| Advanced manufacturing credit (45X) | Remove (industrial policy) | Decided |
| Energy-efficient building credits and deductions (45L, 179D), any remaining vehicle credits | Remove | Decided |
| Fossil fuel preferences: percentage depletion (oil, gas, coal), immediate write-off of drilling costs, enhanced oil recovery credit, marginal well credit | Remove (they increase a negative externality) | Decided |
| Work Opportunity Credit, New Markets credit, empowerment zones, Indian employment credit, historic rehabilitation credit, employer child care credit, paid leave credit, disabled access credit, small business health care credit, tip (FICA) credit | Remove | Decided |
| Low-Income Housing Tax Credit | **Remove from the tax code.** The same amount each year (about $14 billion, indexed) goes to the states' cost-of-living funds, restricted to affordable housing (Section 9.3). | Decided |
| Carbon fee (a charge per ton of CO2, with the revenue used to lower the flat rate or paid out with the UBI) | Not now; a possible later reform | Decided |
| New credits in future | Must meet the same test: reduce a negative externality, or fund research | Decided |

---

## 9. Programs

### 9.1 Summary by phase

| Program | Phase 1 | Phase 2 | End state |
|---|---|---|---|
| SNAP | Kept | Counts the UBI, shrinks | Ends |
| TANF | Kept | Counts the UBI, shrinks (mostly gone early) | Ends |
| WIC | Kept | Counts the UBI | Ends |
| Housing aid | Kept | Counts the UBI (rent = 30% of income) | New vouchers until **year 18 after passage**, then attrition |
| ACA premium credits | Kept | Count the UBI | **Kept, counting the UBI** |
| Unemployment insurance | Kept | Becomes the short top-up (7.4) | Short top-up |
| EITC | Simple automatic version | Higher of EITC or partial UBI | Ends |
| CTC | Removed | - | - |
| Social Security | Kept with floors, taxed as current law | Wind-down | Legacy only |
| SSDI | Floor | Above the UBI | Above the UBI, permanent |
| SSI | Kept, no UBI counting, higher asset limit | Same | Same |
| Medicaid, CHIP | Kept; Medicaid does not count the UBI | Same | Same |
| Medicare | Everyone 65+, no work requirement | Same | Same |
| School meals | Kept | Count the UBI | Kept, counting the UBI |
| Other income-tested programs (child care help, Head Start, LIHEAP, Pell grants and similar) | Kept | Count the UBI | Kept, counting the UBI |

### 9.2 Rules

| Item | Rule | Status |
|---|---|---|
| Programs that count the UBI as income | All income-tested programs, **except** SSI and Medicaid | Decided |
| Medicaid | Does not count the UBI (avoids the 138% of poverty cliff) | Decided |
| Medicare | For everyone 65+, no 40-quarter work requirement | Decided |
| Medicare for noncitizens | Same eligibility as the UBI (citizens and qualified residents). Noncitizens already on Medicare at passage keep it. | Decided |
| ACA credits | Kept permanently, counting the UBI (option A). A Medicaid buy-in with a sliding premium is a possible later reform. | Decided |
| Housing aid | Last new voucher in year 18 after passage; current families keep vouchers while eligible | Decided |
| Public housing buildings | Plan needed (sell, convert, or keep as low-rent housing) | Open |

Known effects of counting the UBI: most UBI families lose free school meals
(limit 130% of poverty) and Head Start (limit 100% of poverty) at the full UBI,
except in schools that serve free meals to all pupils.

### 9.3 States

| Item | Rule | Status |
|---|---|---|
| State income taxes | States define their own base; they may adopt the federal flat tax base | Decided |
| State savings from programs that shrink (TANF required spending, SNAP admin and cost share, and similar) | States keep the savings in a **cost-of-living fund** with restricted spending | Decided |
| Federal money for affordable housing | The amount of the removed Low-Income Housing Tax Credit (about $14 billion a year, indexed) goes to the cost-of-living funds, restricted to affordable housing (Section 8.4) | Decided |
| Allowed uses, duration and reporting of the fund | Later | Open |
| State EITCs built on the federal EITC | States redesign them | Decided (states decide) |
| Medicaid and CHIP cost-sharing | Unchanged | Decided |

---

## 10. Phase 2 schedule and safety check

| Item | Rule | Status |
|---|---|---|
| Steps | Five equal steps, years 2 to 6, each about $3,200 of adult UBI (indexed) | Decided |
| Rate path | The flat rate for each year is set in law with the schedule | Decided |
| Measure | The actual net budget effect of the whole system in the last completed fiscal year, compared with the plan | Decided |
| Data | Treasury actuals (about 3 months after the fiscal year ends) | Decided |
| Who certifies | CBO | Decided |
| Business cycle | Use CBO's cyclically adjusted figures, so a recession alone does not stop the UBI | Decided |
| Trigger | Shortfall above 0.5% of GDP: the next step waits one year. A smaller shortfall gives a half step. | Decided |
| Limits | At most two delays (latest end: year 8). A good year does not speed up the schedule. | Decided |

---

## 11. Inheritances and gifts

| Item | Rule | Status |
|---|---|---|
| Estate tax | Repealed, with its rules | Decided |
| What heirs pay tax on | Cash and investments received: bank accounts, stocks, bonds, funds, crypto, life insurance payouts, investment real estate, second homes, business and farm interests | Decided |
| Rate | The flat rate, paid by the heir | Decided |
| Exempt: primary home | Up to $1 million per estate, indexed. Value above the cap is taxed, with payment over time. | Decided |
| Exempt: personal items | Furniture, heirlooms, jewelry, cars: up to $100,000 per estate, indexed. Art, collectibles and gold count toward this cap. | Decided |
| Exemption per heir | None | Decided |
| Between spouses | Exempt (gifts and at death) | Decided |
| To charity | Exempt | Decided |
| Family businesses and farms | Taxed, with payment over 10-15 years at the Treasury interest rate; no valuation discounts | Decided |
| Inherited retirement accounts | Taxed once: pre-reform balances are taxed as income when the heir withdraws them, not as inheritance; post-reform (already taxed) balances are taxed as inheritance | Decided |
| Gifts during life | Recipient pays the flat tax on cash and investment gifts above **$19,000 per recipient per year**, indexed. Tuition and medical bills paid directly are exempt. | Decided |
| Step-up | Kept for assets taxed at inheritance (taxed once, at transfer). Exempt items keep the original cost (carryover basis); the gain is taxed once when the heir sells. | Decided |
| Valuation | Clear rules; no discounts for minority shares | Decided |
| Trusts | Look-through: the beneficiary pays when they receive money | Decided |

Note: this is much broader than today's estate tax (about $15 million exempt
per person). Revenue could be large, but the data has no inheritances, so the
model cannot estimate it.

---

## 12. Estimates from the discussion (not model results)

These are rough figures from the design discussion. Section 14 replaces them
with model results.

| Item | Estimate |
|---|---|
| Phase 1 rate, with Social Security taxed as current law | about 24% |
| End-state rate, before behavior | high 30s |
| Behavior (work, capital gains, profit shifting) | could add 1-4 points to the rate |
| Business rate at 21% with credit, vs business rate = flat rate | about 1.5 points higher personal rate, static |
| Citizens plus qualified residents only | lowers the rate, perhaps about 1.5 points |
| ACA credits kept | about 0.5-0.7 points |
| Employer health premiums in the base (at 100%) | about 2 points lower rate |
| Simple EITC | about $70B a year, declining in phase 2 |
| SSDI above the UBI | about $25-40B a year |
| Employer insurance premium | about 0.5-0.6% of wages |
| Removing business credits and fossil fuel preferences (Section 8.4) | saves roughly $70-100B a year, about 0.3-0.5 points of rate |

Earlier model results (for reference, on the original spec): phase 1
revenue-neutral at 23.11% and steady state at 34.40% (Populace data, Social
Security removed in the steady state).

---

## 13. Open items

All proposals are decided (2026-11-14). Left for later:
1. Cost-of-living fund details (9.3).
2. Public housing buildings (9.2).
3. SSI marriage penalty (7.2).
4. Unemployment top-up: exact cap, trigger and start date (7.4).
5. How the affordable housing money is split among states (today's
   Low-Income Housing Tax Credit formula, per person, is the simple default)
   (8.4, 9.3).

---

## 14. Modeling plan and gaps

### 14.1 What the microsimulation can test

One-year snapshots (2026 population, static):
- Phase 1.
- Each of the five phase 2 steps (partial adult UBI; programs counting the UBI;
  EITC offset; employer health premiums 20-100%).
- The end state.

### 14.2 What it cannot test

- Inheritances and gifts (not in the data).
- Behavior: work, capital gains realizations, profit shifting, owners
  relabeling pay as profit.
- The multi-year path: Social Security wind-down, housing attrition, the trust
  fund. These belong to the spreadsheet model (2027-2070).
- State responses and the cost-of-living fund.
- The business credit in detail (who owns which shares); the model can only
  approximate it with a share of dividends.
- Medicaid totals on Populace data on a 15 GB machine.
- Business tax credits and preferences (Section 8.4): PolicyEngine models
  household taxes, not business returns. Their effect enters only as an
  estimate.

### 14.3 Code changes needed to match this spec

| Area | Code today | Needed |
|---|---|---|
| Steady state Social Security | `steady_state.social_security_residual: true` (kept above the UBI) | Removed (`false`), plus legacy and SSDI-above-UBI rules |
| Phase 1 Social Security tax | 100% of Social Security in the flat tax base | Current-law taxable part, per person, $25,000 / $34,000 |
| Phase 1 floors | Only people 65+ | Also survivor, dependent and SSDI beneficiaries of any age |
| EITC | Removed with the income tax | Simple EITC in phase 1; offset by partial UBI in phase 2 |
| SSI asset limit | PolicyEngine current law | $6,000 / $9,000 |
| ACA credits | Removed in the steady state | Kept, counting the UBI |
| Programs counting the UBI | PolicyEngine leaves `basic_income` out of all program income | Count it in SNAP, TANF, housing, WIC, ACA credits, school meals and others; not in SSI or Medicaid |
| Eligibility | Everyone | Citizens and qualified residents after 5 years (data has immigration status) |
| Employer health premiums | In the base at 100% (Enhanced CPS only; Populace has none) | Phased in by step; needs an imputation for Populace |
| Business tax | Corporate line = flat rate x $1.6T; dividends fully taxed | 21% x profit base; credit on dividends |
| Phase 2 | Not modeled | Five partial-UBI steps as scenarios |
| Unemployment | Kept or removed | Short top-up (approximate) |
| SSDI | Removed with Social Security in the steady state | Above the UBI, with family floors |
| Employer insurance premium | None | Revenue line |
| Medicare | PolicyEngine eligibility | Everyone 65+ (small effect) |
| Capital gains basis adjustment for retained business profit | None | Cannot be modeled with the data; note as a limit |

### 14.4 Order of work (when asked)

1. Update the reform code and config to this spec.
2. Run phase 1, the five phase 2 steps and the end state on Populace data.
3. Solve the revenue-neutral rate for each, and write a new summary with the
   rate path, poverty, distribution and biggest losers for each phase.
