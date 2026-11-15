# Spec v3: Flat Tax + UBI, full design

Status: design decisions as of 2026-11-15. This document replaces spec v2
(`docs/SPEC_v2.md`, kept for reference) as the reference for the **policy**.
Changes from v2 are marked **(v3)**. The model follows v2; the v3 changes are
not yet modeled (Section 14).

Marks used:
- **Decided**: the user chose it.
- **Proposed**: suggested, not yet confirmed. Listed again in Section 13.
- **Open**: left for later.

All dollar amounts are in 2026 dollars. "Index" means: raise each year by the
same formula as the HHS poverty guideline (consumer prices, CPI-U).

## Changes from v2

The v2 model results (`outputs/v2/SUMMARY.md`) showed three problems: child
poverty rose 5.1 points at step 1, low- and middle-income single workers lost
12-17% in phase 1, and the flat rate peaked at 37% at the end of the schedule.

| # | Change | Sections |
|---|---|---|
| 1 | Programs that end at step 5 (SNAP, TANF, WIC) count only the new working-age UBI. Programs that continue count the working-age UBI, and phase in the child and senior UBI at 20% per step. | 9.1, 9.2 |
| 2 | Phase 2 EITC: reduced by **half** of the partial UBI of the tax unit's adults, instead of "higher of". | 6 |
| 3 | Phase 1: the EITC for workers without children stays at today's amounts. An expansion was considered and dropped once the earnings exemption (6) was added. | 6 |
| 4 | Inheritance revenue and the savings from the 5-year wait are not counted in the rate schedule. They are a cushion against behavior risk. | 10, 14 |
| 5 | The OASDI and Medicare HI trust funds are drawn down to hold the flat rate at a **35% ceiling** from step 4 while the reserves last (about year 11-12). The extra debt and its interest are stated. The safety check uses the planned drawdown. | 5.2, 10, 10a |
| 6 | **Transitional earnings exemption:** the first $16,100 of each working-age person's wages and self-employment earnings is not taxed in phase 1; the exemption shrinks 20% per step as the partial UBI grows, and ends at step 5. This removes most of the phase 1 squeeze on workers. | 4.7, 6 |

---

## 1. Purpose and principles

1. Replace the federal income tax, payroll taxes and most income-tested
   programs with one flat tax and a universal basic income (UBI).
2. **One rate, taxed once.** All personal income pays one flat rate. Business
   profit pays 21% at the business and the rest of the flat rate at the owner,
   with a credit, so it is taxed once.
3. **No carve-outs.** No deductions for people (except the temporary earnings
   exemption of Section 4.7, which ends at step 5); for businesses, only credits
   that prevent double tax, reduce negative externalities, or fund research.
   Exceptions kept on purpose: 529-like savings accounts (education, ABLE,
   Coverdell, children's accounts) and tax-exempt state and local bonds.
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
| **Phase 1** | Year 1 = the tax year after passage | Flat tax replaces income and payroll taxes. UBI for children and people 65+. Floors for Social Security beneficiaries. Simple EITC (today's amounts, including the small childless EITC). Earnings exemption of $16,100 per worker **(v3)**. Programs kept. |
| **Phase 2** | Years 2 to 6 | Partial UBI for adults 18-64 in five equal steps. Programs count the new UBI and shrink; continuing programs phase in counting of the child and senior UBI **(v3)**. EITC reduced by half of the partial UBI **(v3)**. Earnings exemption shrinks 20% per step **(v3)**. Employer health premiums enter the tax base in steps. |
| Rate ceiling **(v3)** | From step 4 while the trust funds last (about year 11-12) | Flat rate held at 35% by drawing down the OASDI and Medicare HI trust funds (Section 10a). |
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
| Deductions and credits | None, except: the simple EITC during the transition (Section 6), the transitional earnings exemption (Section 4.7, v3) and the business tax credit (Section 8) | Decided |
| Collection | Withheld at source on wages and other payments | Decided |

### 4.2 Tax base

Taxed at the flat rate:
- wages and salaries, including 401(k) and other pre-tax deferrals
- self-employment income; owner payouts from businesses (Section 8)
- all interest, **except** interest on state and local bonds, which stays
  tax-exempt (decided 2026-11-14)
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

Kept as today (decided 2026-11-14):
- **529-like savings accounts:** education savings plans (529), ABLE accounts
  for disabled people (529A), Coverdell education savings accounts (530), and
  the children's accounts (530A). Earnings and qualified withdrawals stay
  untaxed. Contributions are made from income that was already taxed.
- **Tax-exempt bonds:** interest on state and local bonds stays tax-exempt,
  with today's private activity bond rules.

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

### 4.7 Transitional earnings exemption (v3)

Phase 1 removes today's standard deduction and lower brackets from working-age
adults one year before their UBI starts. The exemption replaces them with a
deduction for earnings that shrinks as the UBI grows. **Decided** (2026-11-15).

| Item | Rule | Status |
|---|---|---|
| Who | Each person aged 18-64 (individual, like the flat tax) | Decided |
| What is exempt | Earnings only: wages and net self-employment earnings, the same rule for both. Not investment income, pensions or Social Security. | Decided |
| Amount, phase 1 | **$16,100** (about today's standard deduction for a single filer), indexed | Decided |
| Phase 2 | Shrinks 20% per step as the partial UBI rises 20% per step: about $12,900 at step 1, $9,700 at step 2, $6,400 at step 3, $3,200 at step 4, **$0 from step 5** | Decided |
| How it works | The flat tax applies to earnings above the exemption. It is not refundable: it can only reduce the tax on earnings to zero. | Decided |
| Social Security tax rule | "Other income" in Section 5.3 uses earnings **before** the exemption, as current law uses income before the standard deduction | Decided |
| Withholding, wages | The primary employer applies the exemption monthly (like a W-4 today). Other employers withhold at the flat rate. An automatic year-end adjustment from wage reports settles people with several jobs; no return needed. | Decided |
| Self-employed | Applied in quarterly estimated payments, settled at year end | Decided |

Worker support grows at every step, so no step is a cliff:

| | Phase 1 | Step 1 | Step 2 | Step 3 | Step 4 | Step 5 |
|---|---|---|---|---|---|---|
| Earnings exemption | $16,100 | $12,900 | $9,700 | $6,400 | $3,200 | $0 |
| Partial UBI | $0 | $3,192 | $6,384 | $9,576 | $12,768 | $15,960 |

Estimated effect (not modeled): costs about $620B in phase 1, falling to $0 at
step 5. The phase 1 rate rises from about 26% to about 29%, and the rate path
rises more gently to the 35% ceiling. A single worker without children,
compared with today (corrected 2026-11-15):

| Earnings | Phase 1 without the exemption (26%) | With the exemption (29%) |
|---|---|---|
| $10,000 | about -$1,800 | about +$770 |
| $15,000 | about -$2,500 | about +$1,150 |
| $20,000 | about -$3,300 | about +$790 |
| $30,000 | about -$4,100 | about -$320 |
| $50,000 | about -$5,400 | about -$2,200 |

Workers up to about $25,000 gain; the remaining losses are around
$40,000-60,000 (about -4% to -6%) and are mostly covered at step 1.
Higher-income households and retirees with investment income pay the higher
phase 1 rate without the exemption.

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
| Funding | The Social Security (OASDI) trust fund pays legacy benefits first, on the drawdown schedule of Section 10a; then general revenue | Decided (v3: schedule) |
| End state | Social Security is removed; only legacy benefits remain, ending as recipients die (about 60 years) | Decided |

Note: the earned part ramps up by itself with years paid in, so older workers
get more without a separate age ramp.

**Debt (v3):** the trust fund holds Treasury bonds. Redeeming them means
Treasury borrows from the public. Drawing down the reserves (about $2.4
trillion) raises federal debt held by the public by about the same amount,
and adds roughly $90-100 billion a year of interest paid to the public (at
about 4%). Section 10a.

### 5.2a Railroad retirement

Rail workers are not in Social Security. The Railroad Retirement Board pays
two tiers. **Decided** (2026-11-14):

| Part | Rule | Status |
|---|---|---|
| Railroad retirement payroll taxes (Tier 1 and Tier 2, sections 3201-3241) | Removed, with the other payroll taxes | Decided |
| **Tier 1** (the Social Security equivalent) | Follows the Social Security rules in this section: phase 1 floors, current-law taxation, wind-down | Decided |
| **Tier 2** (an extra pension for rail service) | Becomes a **private industry pension** | Decided |
| Tier 2 already earned | Protected. Paid first from the National Railroad Retirement Investment Trust, then as a pension obligation of the industry plan. | Decided |
| Tier 2 for future rail service | Earned in the private industry plan, funded by employer and worker contributions outside the tax code, like any private pension | Decided |
| Tax on Tier 2 payments | Taxed at the flat rate when paid, like other pensions | Decided |
| "Higher of" rule | Only Tier 1 counts as Social Security; Tier 2 is a pension and is not offset by the UBI | Decided |

Open details: who takes over the trust fund and its governance, and pension
insurance for the new plan (for example, coverage by the Pension Benefit
Guaranty Corporation). See Section 13.

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
| EITC for workers without children, phase 1 **(v3)** | Today's childless EITC, kept as is and paid automatically (maximum about $650). No expansion: with the earnings exemption, single workers up to about $25,000 already gain against today. | Decided |
| EITC, phase 2 **(v3)** | Net EITC = max(simple EITC - 0.5 x the partial UBI of all adults 18-64 in the tax unit, 0). Each step adds about $3,192 of UBI per adult and removes only half of it from the EITC, so working families gain about $1,600 per adult per step. A single parent's EITC reaches zero around step 4; a couple's around step 3. | Decided |
| EITC, end state | Gone. No cliff: the step 5 UBI increase is larger than any EITC left after step 4. | Decided |

**Phase 1 single workers (v3).** Without a deduction or lower bracket, single
workers without children would pay the flat rate from the first dollar and
lose 12-17% in phase 1 (v2 model). The **transitional earnings exemption**
(Section 4.7) removes most of this loss: workers up to about $25,000 gain,
and the remaining losses (around $40,000-60,000, about -4% to -6%) are mostly
covered at step 1. Considered and not adopted:
- an expanded childless EITC (the 2021 expansion raised for inflation:
  maximum about $1,800, zero at about $25,700; about $15-20B a year).
  Dropped (2026-11-15): with the exemption it would only add to gains, and
  dropping it keeps the phase 1 EITC identical to today's;
- accepting the squeeze until step 1;
- a low-earner credit refunding the flat tax on the first $15,000 of wages,
  phased out by $35,000 (about $60-100B a year);
- a middle-earner credit phased out between $25,000 and $60,000 (about
  $150-200B; adds about 11 points to the marginal rate in that range);
- a 6-step schedule that starts the partial UBI in phase 1 (about $310B,
  +1.5 points; pays non-workers, who lose nothing in phase 1).

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


### 8.3a Corporate minimum tax

The corporate minimum tax on large companies' book income stays as today. Only
the individual AMT is removed. **Decided** (2026-11-14).

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
| SNAP | Kept | Counts the new working-age UBI only **(v3)**, shrinks | Ends |
| TANF | Kept | Counts the new working-age UBI only **(v3)**, shrinks | Ends |
| WIC | Kept | Counts the new working-age UBI only **(v3)** | Ends |
| Housing aid | Kept | Counts the working-age UBI; child and senior UBI phased in 20% per step **(v3)** (rent = 30% of income) | New vouchers until **year 18 after passage**, then attrition |
| ACA premium credits | Kept | Count the working-age UBI; child and senior UBI phased in 20% per step **(v3)** | **Kept, counting the UBI** |
| Unemployment insurance | Kept | Becomes the short top-up (7.4) | Short top-up |
| EITC | Simple automatic version, today's amounts | Reduced by half of the partial UBI **(v3)** | Ends |
| CTC | Removed | - | - |
| Social Security | Kept with floors, taxed as current law | Wind-down | Legacy only |
| SSDI | Floor | Above the UBI | Above the UBI, permanent |
| SSI | Kept, no UBI counting, higher asset limit | Same | Same |
| Medicaid, CHIP | Kept; Medicaid does not count the UBI | Same | Same |
| Medicare | Everyone 65+, no work requirement | Same | Same |
| School meals | Kept | Count the working-age UBI; child and senior UBI phased in 20% per step **(v3)** | Kept, counting the UBI |
| Other income-tested programs (child care help, Head Start, LIHEAP, Pell grants and similar) | Kept | Same as school meals **(v3)** | Kept, counting the UBI |

### 9.2 Rules

| Item | Rule | Status |
|---|---|---|
| Programs that count the UBI as income | All income-tested programs, **except** SSI and Medicaid | Decided |
| How much they count **(v3)** | Two parts of the UBI are treated differently. **Working-age UBI** (the partial UBI of adults 18-64 from phase 2): counted in full from step 1. **Child and senior UBI** (the child UBI, the UBI of people 65+, and the UBI floors of survivor, dependent and SSDI beneficiaries, all paid from phase 1): programs that **end at step 5** (SNAP, TANF, WIC) never count it; programs that **continue** count 20% at step 1, 40% at step 2, 60% at step 3, 80% at step 4 and 100% from step 5. | Decided |
| Why **(v3)** | In the v2 model, counting the child and senior UBI all at once at step 1 cut SNAP from $95B to $41B and raised child poverty 5.1 points. | - |
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
| Safety check baseline **(v3)** | The plan the check compares against includes the planned trust fund drawdown (Section 10a), so planned deficits do not trigger the brake | Decided |
| Revenue not counted **(v3)** | The rate schedule does not count inheritance revenue, or the savings from the 5-year wait for permanent residents. That money lowers the deficit and counts in the safety check's margin: it is a cushion against behavior risk (work, capital gains, profit shifting; estimated at 1-4 points of rate). | Decided |

### 10a. Rate smoothing with the trust funds (v3)

| Item | Rule | Status |
|---|---|---|
| Ceiling | The flat rate is set at no more than **35%** from step 4, while the reserves last | Decided |
| Source | Draw down the OASDI trust fund (about $2.4 trillion at passage) and the Medicare HI trust fund (roughly $200-300 billion), which lose their payroll taxes | Decided |
| How long (estimate) | At the end of the schedule one point of rate is worth about $210B a year. Holding 35% instead of about 37% costs about $400B a year. The reserves last until about **year 11-12**. To be confirmed with the multi-year spreadsheet. | Estimate |
| After the reserves run out | The ceiling ends; the rate is set for revenue neutrality. Legacy benefits shrink slowly and workers who retire during the transition add new legacy benefits (UBI + 40%), so the rate may stay above 35% for some years. | Decided |
| Debt | Federal debt held by the public rises by about the amount drawn down (about $2.4-2.7 trillion), with roughly $90-100 billion a year of extra interest paid to the public. The law states this. | Decided |
| Not possible | A permanent 34% ceiling: at about $600B a year it would exhaust the reserves around year 9 | - |

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

## 12. Estimates and model results

### 12.1 Model results for v2 (Populace data, static, 2026 population)

From `outputs/v2/SUMMARY.md`. Revenue-neutral flat rate by stage:

| Phase 1 | Step 1 | Step 2 | Step 3 | Step 4 | Step 5 (end of schedule) | Long run |
|---|---|---|---|---|---|---|
| 26.03% | 27.99% | 30.33% | 32.69% | 35.01% | 36.99% | 34.06% |

SPM poverty (baseline 13.7%): 14.9% in phase 1, 15.0% at step 1, 6.1% at the
end of the schedule, 6.5% in the long run.

### 12.2 Estimated effect of the v3 changes (not modeled)

| Change | Estimate |
|---|---|
| Child and senior UBI not counted by SNAP, TANF, WIC; phased in elsewhere | SNAP stays larger in steps 1-4 (about $30-40B at step 1); about +0.15-0.2 points of rate at step 1 |
| 50% EITC offset | EITC about $40B at step 1 instead of $16B, then falling fast; about +0.1 point at step 1 |
| Childless EITC expansion | Dropped; would have cost about $15-20B a year |
| Trust fund ceiling | Holds 35% from step 4 to about year 11-12; debt +$2.4-2.7T; interest +$90-100B a year |
| Transitional earnings exemption | About $620B in phase 1 (phase 1 rate about 26% to 29%), falling 20% per step to $0 at step 5 |

### 12.3 Estimates from the v2 discussion

These are rough figures from the design discussion, kept for reference.

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

Left for later:
1. Cost-of-living fund details (9.3).
2. Public housing buildings (9.2).
3. SSI marriage penalty (7.2).
4. Unemployment top-up: exact cap, trigger and start date (7.4).
5. Tier 2 railroad pension: who takes over the trust fund, its governance,
   and pension insurance for the new private plan (5.2a).
6. How the affordable housing money is split among states (today's
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
  fund drawdown and the 35% ceiling (Section 10a). These belong to the
  spreadsheet model (2027-2070).
- **Inheritance revenue (v3):** not modeled and, by Section 10, not counted in
  the rate schedule. It is kept as a cushion against behavior risk.
- State responses and the cost-of-living fund.
- The business credit in detail (who owns which shares); the model can only
  approximate it with a share of dividends.
- Medicaid totals on Populace data on a 15 GB machine.
- Business tax credits and preferences (Section 8.4): PolicyEngine models
  household taxes, not business returns. Their effect enters only as an
  estimate.

### 14.3 Status of the model

The v2 model (`src/flatubi/reform/v2.py`, `configs/v2.yaml`) implements spec
v2 for phase 1, the five phase 2 steps and the long run, except: TANF, child
care, Head Start and LIHEAP counting the UBI; SSDI family members and taper;
the 5-year wait; Medicare for everyone 65+. Employer health premiums are
imputed on Populace.

### 14.4 Code changes needed for v3

| Area | v2 model | v3 |
|---|---|---|
| Programs counting the UBI | All UBI counted in SNAP, school meals, WIC, housing and ACA from step 1 | Split the UBI into working-age and child/senior parts. SNAP and WIC count the working-age part only; school meals, housing and ACA count the working-age part plus 20% x step of the child/senior part |
| Phase 2 EITC | max(EITC - adults' partial UBI, 0) | max(EITC - 0.5 x adults' partial UBI, 0) |
| Childless EITC, phase 1 | Today's childless EITC (PolicyEngine) | No change |
| Earnings exemption | None | Per person 18-64: subtract min(earnings, exemption) from the flat tax base; exemption = $16,100 x (1 - step/5); earnings = wages + net self-employment income |
| Rate ceiling | Not modeled | Outside the one-year model: report each stage's gap to 35% as the planned trust fund drawdown |

### 14.5 Original order of work

1. Update the reform code and config to this spec.
2. Run phase 1, the five phase 2 steps and the end state on Populace data.
3. Solve the revenue-neutral rate for each, and write a new summary with the
   rate path, poverty, distribution and biggest losers for each phase.
