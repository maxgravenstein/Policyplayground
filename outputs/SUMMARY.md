# Flat Tax + UBI: results summary (2026)

Static, one-year model on PolicyEngine US 2.107.4 and the Enhanced CPS 2024
(tag 1.115.3), aged to 2026. People do not change behavior. All amounts are
per year. Full tables and charts are in each folder's `report.html`.

## Key results

| | Steady state | Phase 1 |
|---|---|---|
| **Revenue-neutral flat rate** | **35.61%** | **22.77%** |
| Net budget effect at 38.25% | +$491B (surplus) | +$3,157B (surplus) |
| UBI cost (gross) | $4,503B | $420B |
| Flat tax revenue at the revenue-neutral rate | $6,050B | $4,278B |
| Net transfer (UBI minus flat tax, where positive), at the revenue-neutral rate | **$2,058B** | $333B |
| Net transfer at 38.25% | $2,009B | $311B |
| SPM poverty change at the revenue-neutral rate | **-11.1 pp** (23.7% to 12.6%) | **+6.3 pp** (23.7% to 30.0%) |
| Child poverty change | -10.7 pp | +8.9 pp |
| Poverty change, people 65+ | +0.5 pp | +3.0 pp |
| Deep poverty change | -4.3 pp | +1.0 pp |
| Gini (equivalized, person-weighted) | 0.460 to 0.410 | 0.460 to 0.490 |

The revenue-neutral rates come from the solver (bisection on the tax step) and
were confirmed by full reruns at that rate: net budget +$0.2B (steady state) and
+$0.6B (phase 1). Folders: `steady_state_2026/`, `phase1_2026/` (at 38.25%, with
MTRs) and `*_revenue_neutral/` (at the solved rate).

## What the numbers say

1. **Steady state pays for itself below 38.25%.** At 35.61% it is
   revenue-neutral against current law, including $570B of corporate tax at the
   flat rate (outside the microsimulation).
2. **The net transfer is about $2.1 trillion, not $1.1 trillion.** The earlier
   estimate is about half of what the model finds. The model has 268 million
   adults and 73 million children; the UBI alone costs $4.5 trillion.
3. **Steady state cuts poverty by about 11 points.** The bottom three deciles
   gain 20% to 188% of net income. Deciles 7 to 10 lose 7% to 12%.
4. **People 65+ lose the most.** On average their households lose about $20,000
   (20% of net income). Poverty for people 65+ does not fall. Every one of the 10
   biggest losing groups in the steady state gets most of its income from Social
   Security, or is 65+ and loses Social Security.
5. **Phase 1 as designed raises poverty.** Working-age adults get no UBI but
   pay the flat tax from the first dollar and lose the EITC and CTC. At the
   revenue-neutral 22.77%, poverty rises 6.3 points. On average only the
   bottom decile (children's UBI) and the top decile (lower tax) gain.
6. **Phase 1 taxes Social Security in full.** The offset gives each retiree
   max(Social Security, UBI) before tax, then the flat tax takes 22.77% of the
   Social Security. Retirees whose benefit is above the UBI lose the tax.
7. **Phase 1 MTRs are high for low earners who keep SNAP and housing:**
   about 70% at 38.25% (flat tax + benefit phase-out). In the steady state, 26% of workers
   face exactly the flat rate; most others also pay state income tax
   (reform MTR about 44%).

## The 10 biggest losing household types

Groups are household type x baseline income fifth x main income source, with at
least 0.5 million people. Ranked by the average % loss of net income, at the
revenue-neutral rate. Amounts are per household per year.

### Steady state (35.61%)

| # | Who | People | Average change | Main cause |
|---|---|---|---|---|
| 1 | Retired households (all adults 65+), top income fifth, living mainly on Social Security | 2.0 M | -$79,400 (-54%) | Lose $96,900 of Social Security; UBI pays back $31,900 |
| 2 | Retired households, fourth fifth, mainly Social Security | 3.7 M | -$39,400 (-51%) | Lose $52,800 of Social Security; UBI +$20,800 |
| 3 | Single adults under 65 (mostly SSDI), bottom fifth | 1.5 M | -$3,900 (-50%) | Lose $14,500 SSDI and $5,200 of SNAP and housing; UBI +$16,000. 29% have housing aid, 50% SNAP |
| 4 | Single adults under 65 on SSDI, second fifth | 2.6 M | -$15,000 (-48%) | Lose $30,700 SSDI; UBI +$16,000 |
| 5 | Single adults under 65 on SSDI, middle fifth | 1.3 M | -$19,000 (-46%) | Lose $29,900 SSDI and $3,100 more tax; 34% have housing aid |
| 6 | Retired households, middle fifth, mainly Social Security | 7.3 M | -$18,500 (-37%) | Lose $38,100 of Social Security; UBI +$20,800; SSI +$3,200 |
| 7 | Retired households, fourth fifth, mainly pensions and investments | 3.1 M | -$23,000 (-29%) | Lose $29,500 Social Security and pay $14,300 more tax |
| 8 | Couples without children (one under 65), middle fifth, mainly Social Security | 1.1 M | -$16,300 (-27%) | Lose $46,100 Social Security; UBI +$31,900 |
| 9 | Retired households, fourth fifth, still working | 3.0 M | -$21,000 (-26%) | Lose $27,600 Social Security and pay $16,100 more tax |
| 10 | Retired households, top fifth, mainly pensions and investments | 7.6 M | -$64,900 (-25%) | Lose $49,600 Social Security and pay $39,500 more tax |

**Fix to consider:** the loss of Social Security above the UBI. A transition
credit for accrued benefits, or a higher UBI for 65+ and for disabled people,
would target groups 1 to 10. SSDI recipients (groups 3 to 5) also lose SNAP and
housing aid.

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

PASSTHROUGH_RESULTS

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
  $60B). When Social Security goes, SSI rises by $70B. With full SSI data, both
  numbers would be larger.
* **Housing assistance is $172B in the model**, about three times HUD rental
  aid. The saving from removing it is overstated.
* The UBI does not count as income for SSI, SNAP or Medicaid (PolicyEngine
  default). Corporate tax is outside the microsimulation. Inheritances are not
  in the data. No behavior change. One year only.
* The Enhanced CPS file on the Hugging Face `main` branch is faulty ($9.3T of
  miscellaneous income). We use tag 1.115.3. See `docs/API_NOTES.md`.
