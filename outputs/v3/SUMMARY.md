# Spec v3: results by stage (2026)

Model of `docs/SPEC_v3.md` on Populace data (PolicyEngine US 2.107.4), 2026
population, static (no behavior change). Each stage is a one-year snapshot of
the same population. All numbers are at each stage's **revenue-neutral flat
rate**, found by the solver.

Phase 1 and steps 1-4 are new v3 runs (`outputs/v3/`). Step 5 and the long run
have the same rules in v2 and v3 (no exemption, all UBI counted, SNAP, WIC and
the EITC gone), so they come from the v2 runs (`outputs/v2/`).

Full tables and charts: `outputs/v3/<stage>_2026/report.html`.

## What v3 changes

1. **Earnings exemption** for people 18-64: the first $16,100 of wages and
   self-employment income is not taxed. It falls 20% per step and is $0 at
   step 5.
2. **EITC offset at half:** in steps 1-4 the EITC falls by half of the adults'
   partial UBI (v2: all of it).
3. **Programs count the UBI in two parts.** SNAP and WIC count only the
   working-age UBI. School meals, housing aid and ACA credits count the
   working-age UBI plus 20% per step of the child and senior UBI.

## The stages

| | Phase 1 | Step 1 | Step 2 | Step 3 | Step 4 | Step 5 (end of schedule) | Long run |
|---|---|---|---|---|---|---|---|
| **Revenue-neutral rate, v3** | **29.76%** | **31.45%** | **33.06%** | **34.61%** | **36.05%** | **36.99%** | **34.06%** |
| Rate, v2 | 26.03% | 27.99% | 30.33% | 32.69% | 35.01% | 36.99% | 34.06% |
| Working-age UBI | $0 | $3,192 | $6,384 | $9,576 | $12,768 | $15,960 | $15,960 |
| Earnings exemption per person | $16,100 | $12,880 | $9,660 | $6,440 | $3,220 | $0 | $0 |
| Earnings exempted ($B) | 2,464 | 2,006 | 1,529 | 1,036 | 526 | 0 | 0 |
| UBI cost ($B) | 612 | 1,190 | 1,768 | 2,345 | 2,923 | 3,501 | 4,347 |
| Simple EITC ($B) | 74 | 37 | 17 | 8 | 4 | 0 | 0 |
| SNAP ($B; baseline 95) | 95 | 73 | 55 | 41 | 32 | 0 | 0 |
| Net transfer ($B) | 414 | 553 | 709 | 872 | 1,036 | 1,205 | 1,784 |
| **SPM poverty, v3** (baseline 13.7%) | **11.2%** | **9.8%** | **8.2%** | **6.9%** | **5.8%** | **6.1%** | **6.5%** |
| SPM poverty, v2 | 14.9% | 15.0% | 12.3% | 9.8% | 7.2% | 6.1% | 6.5% |
| Child poverty change (pp) | -3.9 | -4.6 | -5.8 | -7.1 | -8.6 | -6.9 | -7.4 |
| Adults 18-64 poverty change (pp) | -0.9 | -2.9 | -4.9 | -6.6 | -7.9 | -8.3 | -8.4 |
| 65+ poverty change (pp) | -6.2 | -6.6 | -7.1 | -7.3 | -7.3 | -6.4 | -3.4 |
| Deep poverty change (pp) | -1.2 | -1.6 | -2.0 | -2.2 | -2.3 | -2.2 | -2.1 |
| Gini change | -0.013 | -0.022 | -0.032 | -0.041 | -0.050 | -0.054 | -0.038 |
| Deciles that gain on average | 2 | 4 | 4 | 5 | 5 | 5 | 4 |
| Net income change, people 65+ | -3.0% | -4.1% | -5.1% | -6.1% | -7.1% | -7.8% | -13.2% |

The full table, made by `tools/summary_v2.py outputs/v3 outputs/v2`, is in
`outputs/v3/stages.md`.

## What the numbers say

1. **Poverty now falls at every stage.** In v2, poverty rose in phase 1
   (14.9%) and step 1 (15.0%). In v3 it is 11.2% in phase 1 and falls each
   step, to 5.8% at step 4. Child poverty falls 3.9 points in phase 1 (v2:
   rose 1.8) and 4.6 points at step 1 (v2: rose 5.1).

2. **The cost is a higher rate early.** The phase 1 rate is 29.8%, 3.7 points
   above v2. The gap closes step by step as the exemption shrinks: 3.5 points
   at step 1, 1.9 at step 3, 1.0 at step 4, 0 at step 5. The rate rises 1.4-1.7
   points per step to step 4 and 0.9 points at step 5 (v2: 2.0-2.4). This is the smoother path that spec v3
   wanted.

3. **The single-worker squeeze is mostly fixed.** In v2 phase 1, single
   workers in the bottom three fifths lost 12-17% of net income. In v3 only
   the middle fifth is in the list of biggest losers, at -8%. Single parents
   now gain 1.4% on average in phase 1 (v2: -3.7%). Marginal tax rates in the
   bottom decile are 32% in phase 1 (v2: 42%; today 22%).

4. **Retirees pay for much of the exemption.** The exemption is for people
   18-64 only, so people 65+ get no exemption but pay the higher rate on
   pensions, investments and taxable Social Security. In phase 1, households
   of people 65+ lose 3.9% of net income (v2: 0.5%). Their poverty still falls
   6.2 points, because the floors protect low-income retirees. The losses fall
   on retirees in the fourth and top fifths.

5. **There is a new bump at step 5.** Poverty rises from 5.8% at step 4 to
   6.1% at step 5, and child poverty rises 1.7 points. Single parents go from
   -0.9% to -3.6% of net income. At step 5 four things happen at once: SNAP
   ($32B) and WIC end, the last $3,220 of exemption goes, the EITC ends, and
   all child and senior UBI counts in the continuing programs. In v2 this
   step was a smooth drop because SNAP was already small ($12B at step 4).

6. **The trust fund ceiling (spec 10a) has less to do.** The rate is above
   35% only at step 4 (by 1.1 points) and step 5 (by 2.0 points). One point of
   rate is about $200B a year at these stages, so the drawdown is about $210B
   at step 4 and $415B at step 5, then less each year as legacy Social
   Security shrinks.

## Biggest losers (average loss of net income, revenue-neutral rate)

**Phase 1 (29.76%)**

| # | Who | People | Change |
|---|---|---|---|
| 1 | Couples with children, fourth fifth, mainly pensions and investments | 2.6 M | -$22,900 (-13%) |
| 2 | Couples, fourth fifth, mainly pensions and investments | 2.4 M | -$15,800 (-12%) |
| 3 | Retired households, fourth fifth, mainly Social Security | 3.7 M | -$13,100 (-12%) |
| 4 | Couples with children, middle fifth, mainly pensions and investments | 2.1 M | -$13,700 (-11%) |
| 5 | 3+ adults, fourth fifth, mainly pensions and investments | 5.7 M | -$18,500 (-11%) |

**Step 1 (31.45%)**

| # | Who | People | Change |
|---|---|---|---|
| 1 | Couples with children, fourth fifth, mainly pensions and investments | 2.6 M | -$22,700 (-13%) |
| 2 | Retired households, fourth fifth, mainly Social Security | 3.7 M | -$14,300 (-13%) |
| 3 | Couples, fourth fifth, mainly pensions and investments | 2.4 M | -$15,000 (-11%) |
| 4 | Retired households, fourth fifth, mainly pensions and investments | 3.4 M | -$12,400 (-11%) |
| 5 | Couples with children, middle fifth, mainly pensions and investments | 2.1 M | -$12,500 (-10%) |

**Step 4 (36.05%)**

| # | Who | People | Change |
|---|---|---|---|
| 1 | Retired households, fourth fifth, mainly Social Security | 3.7 M | -$17,900 (-16%) |
| 2 | Retired households, top fifth, mainly pensions and investments | 7.7 M | -$49,800 (-15%) |
| 3 | Retired households, fourth fifth, mainly pensions and investments | 3.4 M | -$17,300 (-15%) |
| 4 | Couples, top fifth, mainly pensions and investments | 6.8 M | -$49,100 (-13%) |
| 5 | Couples with children, fourth fifth, mainly pensions and investments | 2.6 M | -$21,900 (-13%) |

Step 5 and the long run: see `outputs/v2/SUMMARY.md`. In v3 no group of
low-income workers or low-income families is in the top five at any stage.
All of the biggest losers are middle- and upper-income households that live
mainly on pensions, investments or Social Security.

## Design issues the numbers show

1. **The step 5 bump.** Options:
   - End SNAP and WIC one step later (year 7), or cut them in two steps.
   - Keep a small part of the exemption at step 5 and end it at year 7.
   - Make the last UBI step a little larger for children.
2. **Retirees with middle and upper incomes carry more of the early cost.**
   This is the result of the exemption for 18-64 only. A lower phase 1 rate
   for pension income would move the cost back to workers.

## Approximations and limits

The same as v2 (see `outputs/v2/SUMMARY.md`): employer health premiums
imputed; Medicaid not computed; no 5-year wait, inheritances, SSDI family
members or SSDI taper; TANF, child care, Head Start and LIHEAP do not count
the UBI; business tax and employer insurance premium outside the
microsimulation; static, one year, no trust fund in the model. Marginal tax
rates are computed for phase 1 only; steps 1-4 ran without them.
