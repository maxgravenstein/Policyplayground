# Flat Tax + UBI: results summary (2026)

Static, one-year model on PolicyEngine US 2.107.4 and the Enhanced CPS 2024
(tag 1.115.3), aged to 2026. People do not change behavior. All amounts are
per year. Full tables and charts are in each folder's `report.html`.

**See also `outputs/populace/SUMMARY.md`:** the same runs on PolicyEngine's
Populace data, whose baseline is much closer to published totals (steady-state
rate 36.75%, phase 1 23.11%). Populace is the better dataset.

**Design change (2026-11-13): the steady state keeps Social Security above the
UBI.** Each beneficiary gets max(benefit - own UBI, 0) on top of the UBI, taxed
at the flat rate (switch: `steady_state.social_security_residual`). Before, the
steady state removed Social Security: revenue-neutral at 35.61%, poverty
-11.1 pp, poverty for people 65+ +0.5 pp. Phase 1 is unchanged.

## Key results

| | Steady state | Phase 1 |
|---|---|---|
| **Revenue-neutral flat rate** | **39.40%** | **22.77%** |
| Net budget effect at 38.25% | -$223B (deficit) | +$3,157B (surplus) |
| UBI cost (gross) | $4,503B | $420B |
| Social Security paid | $800B (above the UBI) | $1,785B |
| Flat tax revenue at the revenue-neutral rate | $7,004B | $4,278B |
| Net transfer (UBI minus flat tax, where positive), at the revenue-neutral rate | **$1,814B** | $333B |
| SPM poverty change at the revenue-neutral rate | **-12.6 pp** (23.7% to 11.1%) | **+6.3 pp** (23.7% to 30.0%) |
| Child poverty change | -9.7 pp | +8.9 pp |
| Poverty change, people 65+ | **-7.4 pp** | +3.0 pp |
| Deep poverty change | -4.5 pp | +1.0 pp |
| Gini (equivalized, person-weighted) | 0.460 to 0.395 | 0.460 to 0.490 |

The revenue-neutral rates come from the solver (bisection on the tax step) and
were confirmed by full reruns at that rate: net budget -$0.3B (steady state) and
+$0.6B (phase 1). Folders: `steady_state_2026/`, `phase1_2026/` (at 38.25%, with
MTRs) and `*_revenue_neutral/` (at the solved rate).

## What the numbers say

1. **Keeping Social Security above the UBI costs about 3.8 points of rate**
   (35.61% to 39.40%). It pays $800B of Social Security, and SSI rises less
   ($33B instead of $80B).
2. **Poverty for people 65+ now falls 7.4 points** instead of rising, and total
   poverty falls 12.6 points.
3. **For a retiree above the UBI, the UBI now just replaces part of Social
   Security.** Their remaining loss is tax: the flat tax on Social Security and
   pensions, with no standard deduction. On average, households of people 65+
   still lose 20% of net income.
4. **The net transfer is about $1.8 trillion.** The earlier $1.1 trillion
   estimate is still well below the model.
5. **Deciles 1-4 gain (3% to 189%); deciles 5-10 lose (2% to 14%).**
6. **Phase 1 as designed raises poverty.** Working-age adults get no UBI but
   pay the flat tax from the first dollar and lose the EITC and CTC. At the
   revenue-neutral 22.77%, poverty rises 6.3 points. On average only the
   bottom decile (children's UBI) and the top decile (lower tax) gain.
7. **Phase 1 taxes Social Security in full.** The offset gives each retiree
   max(Social Security, UBI) before tax, then the flat tax takes 22.77% of the
   Social Security.
8. **Marginal rates.** In the steady state, 26% of workers face exactly the
   flat rate; most others also pay state income tax (reform MTR about 44% at
   38.25%). Phase 1 MTRs for low earners who keep SNAP and housing are about 70%.

## The 10 biggest losing household types

Groups are household type x baseline income fifth x main income source, with at
least 0.5 million people. Ranked by the average % loss of net income, at the
revenue-neutral rate. Amounts are per household per year.

### Steady state (39.40%)

| # | Who | People | Average change | Main cause |
|---|---|---|---|---|
| 1 | Single adults under 65 on SSDI, bottom fifth | 1.5 M | -$3,100 (-40%) | SSDI is mostly below the UBI, so the UBI replaces it; they also lose $5,200 of SNAP and housing. 29% have housing aid, 50% SNAP |
| 2 | Retired households (all adults 65+), top fifth, mainly Social Security | 2.0 M | -$42,200 (-29%) | $42,400 more tax (flat tax on Social Security above the UBI and other income) |
| 3 | Retired households, fourth fifth, mainly Social Security | 3.7 M | -$21,600 (-28%) | $20,700 more tax |
| 4 | Single adults under 65 on SSDI, middle fifth | 1.3 M | -$11,000 (-27%) | $8,900 more tax and $2,600 less benefits. 34% have housing aid |
| 5 | Retired households, fourth fifth, mainly pensions and investments | 3.1 M | -$19,000 (-24%) | $20,800 more tax |
| 6 | Single parents, second fifth, living mainly on benefits | 1.4 M | -$9,100 (-24%) | Lose $19,500 of SNAP and housing aid (all of them have both); UBI +$19,700; $9,200 more tax |
| 7 | Retired households, top fifth, mainly pensions and investments | 7.6 M | -$59,200 (-23%) | $61,300 more tax |
| 8 | Retired households, middle fifth, mainly Social Security | 7.3 M | -$11,000 (-22%) | $11,700 more tax |
| 9 | Retired households, fourth fifth, still working | 3.0 M | -$16,800 (-21%) | $22,800 more tax |
| 10 | Single adults under 65 on SSDI, second fifth | 2.6 M | -$6,400 (-20%) | $6,100 more tax |

For every Social Security group, the UBI and the Social Security cut cancel
out (the cut equals the UBI). The loss that remains is the flat tax.

**Fixes to consider:** a lower tax on legacy Social Security (or none); and
for SSDI recipients and families on housing aid, the loss of SNAP and housing.

### Phase 1 (22.77%)

| # | Who | People | Average change | Main cause |
|---|---|---|---|---|
| 1 | Single adults under 65, bottom fifth, small pension or investment income | 1.0 M | -$1,800 (-42%) | Flat tax on income that is untaxed today |
| 2 | Single adults under 65 on SSDI, bottom fifth | 1.5 M | -$2,400 (-31%) | Flat tax on SSDI; no UBI under 65 |
| 3 | Working couples, bottom fifth | 6.0 M | -$2,900 (-26%) | Lose EITC and pay flat tax from the first dollar ($4,200 more tax) |
| 4 | Couples on Social Security, bottom fifth | 3.6 M | -$5,200 (-25%) | Flat tax on Social Security |
| 5 | Couples on Social Security, middle fifth | 1.1 M | -$14,000 (-23%) | Flat tax on Social Security |
| 6 | Single adults under 65 on SSDI, second fifth | 2.6 M | -$7,200 (-23%) | Flat tax on SSDI |
| 7 | Couples on Social Security, second fifth | 2.9 M | -$9,500 (-22%) | Flat tax on Social Security |
| 8 | Households of 3+ adults on Social Security, second fifth | 2.1 M | -$11,500 (-22%) | Flat tax on Social Security |
| 9 | Retired households, middle fifth, mainly Social Security | 7.3 M | -$10,800 (-22%) | Flat tax on Social Security; UBI top-up only $500 |
| 10 | Single adults under 65 on SSDI, middle fifth | 1.3 M | -$8,700 (-21%) | Flat tax on SSDI |

**Fix to consider:** in phase 1, either do not tax legacy Social Security, or
give the offset after tax. Low-wage working adults need the UBI (or a credit)
in phase 1, because they lose the EITC and the standard deduction.

## Sensitivity: employer payroll tax

The reform removes $779B of employer payroll tax. By default this saving does
not reach anyone in the model, so it lowers revenue without raising any
household's income. With `tax.employer_payroll_to_wages: true`, the saving is
paid out as wages and taxed. See `*_payroll_to_wages/`.

| | Steady state | Phase 1 |
|---|---|---|
| Revenue-neutral rate, default (no pass-through) | 39.40% | 22.77% |
| Revenue-neutral rate, with pass-through | **37.88%** | **21.93%** |
| Change in net income at that rate, deciles 1-6 | +2% to +196% | -10% to +26% |
| Change in net income at that rate, deciles 7-10 | -1% to -9% | -4% to +8% |

With pass-through, deciles 1-6 gain in the steady state, and the losses at the
top fall from 7-14% to 1-9%. Phase 1 still
makes most deciles worse off. (Poverty in these folders is at 38.25%, the run
rate.)

## Baseline checks and limits

| Baseline total (2026) | Model | Published | Gap |
|---|---|---|---|
| Federal income tax | $2,161B | $2,751B (CBO) | **-21%** |
| Payroll taxes | $1,727B | $1,826B (CBO) | -5% |
| Social Security | $1,785B | about $1,670B (Trustees) | +7% |
| SNAP | $114B | about $90B | **+27%** |
| EITC | $72B | $70B (IRS) | +3% |
| Adults / children | 268M / 73M | 270M / 73M | -1% / +1% |
| SPM poverty | 23.7% | 13.1% (Census, 2025) | **+81%** |

* **The baseline income tax is 21% low.** The data have almost no partnership
  and S-corp income and too little top income. So the flat tax base is too
  small, and the true revenue-neutral rate is probably lower.
* **SPM poverty is too high in the baseline.** The change in poverty is more
  reliable than the level.
* **SSI for disabled people is almost zero in the data** ($9B against about
  $60B). In the steady state SSI rises by $33B. With full SSI data, this would
  be larger.
* **Housing assistance is $172B in the model**, about three times HUD rental
  aid. The saving from removing it is overstated.
* The UBI does not count as income for SSI, SNAP or Medicaid (PolicyEngine
  default). Corporate tax is outside the microsimulation. Inheritances are not
  in the data. No behavior change. One year only.
* The Enhanced CPS file on the Hugging Face `main` branch is faulty ($9.3T of
  miscellaneous income). We use tag 1.115.3. See `docs/API_NOTES.md`.
