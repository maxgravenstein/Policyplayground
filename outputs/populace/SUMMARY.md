# Flat Tax + UBI on Populace data (2026)

Same policy and model as `outputs/SUMMARY.md`, but on PolicyEngine's Populace
dataset (build `populace-us-2024-spm-20260909`, 166,000 people) instead of the
Enhanced CPS. Static, one year. Config: `configs/populace.yaml`.

## Why Populace

Its baseline is much closer to published 2026 totals:

| Baseline total | Enhanced CPS | Populace | Published |
|---|---|---|---|
| Federal income tax | $2,161B (-21%) | **$2,595B (-6%)** | $2,751B (CBO) |
| Payroll taxes | $1,727B (-5%) | $1,714B (-6%) | $1,826B (CBO) |
| Social Security | $1,785B (+7%) | **$1,678B (+0.5%)** | about $1,670B |
| SNAP | $114B (+27%) | **$95B (+6%)** | about $90B |
| EITC | $72B | $70B | $70B (IRS) |
| SSI | $9B | **$57B** | about $60B |
| SPM poverty | 23.7% | **13.7%** | 13.1% (Census, 2025) |
| Children | 73M | 78M (+7%) | 73M |
| Housing assistance | $172B (too high) | $6B (too low) | about $60B (HUD) |
| ACA premium credits | $45B | $145B | |

## Key results

**Design change (2026-11-13): the steady state keeps Social Security above the
UBI** (max(benefit - own UBI, 0), taxed at the flat rate). The "before" column
is the steady state that removed Social Security.

| | Steady state, Populace | Steady state before, Populace | Steady state, ECPS | Phase 1, Populace | Phase 1, ECPS |
|---|---|---|---|---|---|
| **Revenue-neutral flat rate** | **36.75%** | 34.40% | 39.40% | **23.11%** | 22.77% |
| Net budget at 38.25% | +$327B | +$807B | -$223B | +$3,435B | +$3,157B |
| UBI cost | $4,507B | $4,507B | $4,503B | $600B | $420B |
| Social Security paid | $824B | $0 | $800B | $1,678B | $1,785B |
| Net transfer at the revenue-neutral rate | $1,687B | $1,907B | $1,814B | $401B | $333B |
| SPM poverty | **13.7% to 4.5% (-9.2 pp)** | 13.7% to 5.3% | 23.7% to 11.1% | **13.7% to 17.6% (+3.8 pp)** | 23.7% to 30.0% |
| Child poverty change | -9.4 pp | -9.5 pp | -9.7 pp | +7.1 pp | +8.9 pp |
| Poverty change, 65+ | **-7.0 pp** | -3.1 pp | -7.4 pp | -3.2 pp | +3.0 pp |
| Deep poverty change | -2.4 pp | -2.3 pp | -4.5 pp | -0.1 pp | +1.0 pp |
| Gini change | -0.058 | -0.045 | -0.065 | +0.021 | +0.017 |

Full reruns at the solved rates give net budgets of +$0.2B (steady state) and
-$1.0B (phase 1).

## What changes with better data and the new Social Security rule

1. **The steady state is revenue-neutral at 36.75%.** Keeping Social Security
   above the UBI costs 2.35 points (it was 34.40%). On the Enhanced CPS the
   same rule costs 3.8 points, because that data has more Social Security and
   almost no SSI.
2. **Poverty falls from 13.7% to 4.5%,** and for people 65+ by 7.0 points.
   Child poverty roughly halves.
3. **The worst losses are about half of what they were.** The worst group
   loses 25% of net income instead of 48%. Households of people 65+ still lose
   16% on average, now mostly from the flat tax on Social Security and pensions
   (today most of their Social Security is untaxed, and they get a larger
   standard deduction).
4. **Deciles 1-5 gain (4% to 78%); deciles 6-10 lose (0.5% to 12%).**
5. **Phase 1 is unchanged and still raises poverty, mostly for children
   (+7.1 points).** Working-age adults and their children lose the EITC and CTC
   and pay the flat tax from the first dollar.
6. **Marginal rates:** in the steady state at 38.25%, 24% of workers face
   exactly the flat rate; most others also pay state income tax (about 44%).
   Phase 1 MTRs for workers in deciles 1-2 are about 57% (flat tax + SNAP and
   housing phase-outs).

## The 10 biggest losing household types (revenue-neutral rate)

### Steady state (36.75%)

| # | Who | People | Average change | Main cause |
|---|---|---|---|---|
| 1 | Retired households, fourth fifth, mainly Social Security | 3.7 M | -$27,700 (-25%) | $28,600 more tax |
| 2 | Retired households, middle fifth, mainly Social Security | 5.8 M | -$17,400 (-21%) | $19,300 more tax |
| 3 | Retired households, fourth fifth, mainly pensions and investments | 3.4 M | -$23,500 (-20%) | $32,000 more tax |
| 4 | Retired households, top fifth, mainly pensions and investments | 7.7 M | -$65,000 (-19%) | $74,800 more tax |
| 5 | Couples (one under 65), fourth fifth, mainly Social Security | 0.6 M | -$22,400 (-19%) | $28,800 more tax and $3,800 less benefits |
| 6 | Couples (one under 65), middle fifth, mainly Social Security | 2.4 M | -$12,600 (-15%) | $19,800 more tax and $3,700 less benefits |
| 7 | Couples (one under 65), top fifth, mainly pensions and investments | 6.8 M | -$53,700 (-15%) | $76,900 more tax |
| 8 | Couples (one under 65), second fifth, mainly Social Security | 2.5 M | -$8,000 (-14%) | $9,900 more tax and $6,100 less benefits |
| 9 | Households of 3+ adults, fourth fifth, mainly Social Security | 0.9 M | -$21,800 (-14%) | $37,900 more tax |
| 10 | Retired households, second fifth, mainly Social Security | 8.2 M | -$7,200 (-13%) | $9,800 more tax |

For the Social Security groups, the UBI and the Social Security cut cancel out;
what remains is the flat tax. The UBI gain is larger than the Social Security
cut only for household members who had no Social Security of their own.

**Fixes to consider:** a lower flat tax on legacy Social Security and pensions,
or an exemption for people 65+.

### Phase 1 (23.11%)

All 10 groups get most of their income from Social Security. Each loses 17% to
20% of net income, almost entirely from the flat tax on Social Security
(for example, retired households in the middle fifth: 5.8 million people,
-$16,400, of which -$18,400 is tax). Full list: `phase1_2026_revenue_neutral/losers.csv`.

## Limits specific to Populace

* **No employer health premiums in the data.** They are left out of the tax
  base (spec 2.2: "if the dataset has them"). In the Enhanced CPS they were
  $1.24T. With them, the steady-state rate would be roughly 2 points lower.
* The employer payroll pass-through sensitivity was run on the Enhanced CPS
  only (see `outputs/SUMMARY.md`: it lowers the steady-state rate by 1.5 points).
* **Medicaid was not computed.** Its simulation needs more memory than this
  15 GB machine has. The Medicaid budget line is blank in both baseline and
  reform; it is a kept program, and on the Enhanced CPS the reform changed it by
  -$1B.
* **Housing assistance is almost missing ($6B),** so the saving from removing
  it is understated by about $50B (about 0.3 points of rate).
* **ACA premium credits are $145B,** higher than on the Enhanced CPS. Removing
  them saves more.
* All other limits in `outputs/SUMMARY.md` apply: static, one year, corporate
  tax outside the microsimulation, the UBI not counted by SSI, SNAP or Medicaid,
  and the employer payroll tax saving not passed to workers.

Folders: `steady_state_2026/` and `phase1_2026/` (at 38.25%, with MTRs);
`*_revenue_neutral/` (at the solved rate, no MTRs).
