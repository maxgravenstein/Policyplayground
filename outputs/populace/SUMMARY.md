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

| | Steady state, Populace | Steady state, ECPS | Phase 1, Populace | Phase 1, ECPS |
|---|---|---|---|---|
| **Revenue-neutral flat rate** | **34.40%** | 35.61% | **23.11%** | 22.77% |
| Net budget at 38.25% | +$807B | +$491B | +$3,435B | +$3,157B |
| UBI cost | $4,507B | $4,503B | $600B | $420B |
| Net transfer at the revenue-neutral rate | $1,907B | $2,058B | $401B | $333B |
| SPM poverty | **13.7% to 5.3% (-8.5 pp)** | 23.7% to 12.6% (-11.1 pp) | **13.7% to 17.6% (+3.8 pp)** | 23.7% to 30.0% (+6.3 pp) |
| Child poverty change | -9.5 pp | -10.7 pp | +7.1 pp | +8.9 pp |
| Poverty change, 65+ | **-3.1 pp** | +0.5 pp | -3.2 pp | +3.0 pp |
| Deep poverty change | -2.3 pp | -4.3 pp | -0.1 pp | +1.0 pp |
| Gini change | -0.045 | -0.050 | +0.021 | +0.017 |

Full reruns at the solved rates give net budgets of -$0.6B (steady state) and
-$1.0B (phase 1).

## What changes with better data

1. **The steady-state rate falls by 1.2 points, to 34.40%.** The tax base is
   larger, but baseline income tax is also higher, so the gain is smaller than
   expected. Employer health premiums are not in Populace, which takes about
   $1.2T out of the base (see limits).
2. **Poverty levels are now usable.** The steady state cuts SPM poverty from
   13.7% to 5.3%.
3. **People 65+ do better than on the Enhanced CPS.** With SSI now in the data,
   SSI rises $47B when Social Security goes, and poverty for people 65+ falls 3.1
   points. Their average household still loses 15% of net income.
4. **The steady-state pattern is the same.** Deciles 1-5 gain (1% to 79%),
   deciles 6-10 lose (3% to 10%). All 10 biggest losing groups get most of their
   income from Social Security, or are retirees who lose it.
5. **Phase 1 still raises poverty, mostly for children (+7.1 points).** Working-
   age adults and their children lose the EITC and CTC and pay the flat tax from
   the first dollar. On average only the bottom and top deciles gain.
6. **Phase 1 MTRs** for workers in deciles 1-2 are about 57% at 38.25%
   (flat tax + SNAP and housing phase-outs).

## The 10 biggest losing household types (revenue-neutral rate)

### Steady state (34.40%)

| # | Who | People | Average change | Main cause |
|---|---|---|---|---|
| 1 | Retired households, fourth fifth, mainly Social Security | 3.7 M | -$53,400 (-48%) | Lose $71,400 Social Security; UBI +$29,700 |
| 2 | Couples (one under 65), fourth fifth, mainly Social Security | 0.6 M | -$49,800 (-43%) | Lose $66,900 Social Security; UBI +$31,900 |
| 3 | Retired households, middle fifth, mainly Social Security | 5.8 M | -$34,800 (-43%) | Lose $59,900 Social Security; UBI +$30,600 |
| 4 | Couples (one under 65), middle fifth, mainly Social Security | 2.4 M | -$31,600 (-38%) | Lose $53,400 Social Security |
| 5 | Couples (one under 65), second fifth, mainly Social Security | 2.5 M | -$18,800 (-32%) | Lose $45,200 Social Security and $6,100 of other benefits |
| 6 | Households of 3+ adults, fourth fifth, mainly Social Security | 0.9 M | -$48,400 (-30%) | Lose $85,100 Social Security |
| 7 | Retired households, second fifth, mainly Social Security | 8.2 M | -$16,200 (-29%) | Lose $48,500 Social Security; SSI +$4,500 |
| 8 | Retired households, fourth fifth, mainly pensions and investments | 3.4 M | -$29,700 (-25%) | Lose $32,500 Social Security, $24,900 more tax |
| 9 | Households of 3+ adults, middle fifth, mainly Social Security | 2.2 M | -$21,400 (-20%) | Lose $64,300 Social Security |
| 10 | Retired households, top fifth, mainly pensions and investments | 7.7 M | -$67,100 (-20%) | $59,200 more tax and $35,600 less Social Security |

### Phase 1 (23.11%)

All 10 groups get most of their income from Social Security. Each loses 17% to
20% of net income, almost entirely from the flat tax on Social Security
(for example, retired households in the middle fifth: 5.8 million people,
-$16,400, of which -$18,400 is tax). Full list: `phase1_2026_revenue_neutral/losers.csv`.

## Limits specific to Populace

* **No employer health premiums in the data.** They are left out of the tax
  base (spec 2.2: "if the dataset has them"). In the Enhanced CPS they were
  $1.24T. With them, the steady-state rate would be roughly 2 points lower.
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
