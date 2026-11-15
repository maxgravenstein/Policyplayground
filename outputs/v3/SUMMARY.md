# Spec v3: results by stage (2026)

Model of `docs/SPEC_v3.md` on Populace data (PolicyEngine US 2.107.4), 2026
population, static (no behavior change). Each stage is a one-year snapshot of
the same population. All numbers are at each stage's **revenue-neutral flat
rate**, found by the solver.

All seven stages are v3 runs (`outputs/v3/`). Full tables and charts:
`outputs/v3/<stage>_2026/report.html`. The full stage table, made by
`python tools/summary_v2.py outputs/v3`, is in `outputs/v3/stages.md`.

## What v3 changes

1. **Earnings exemption** for people 18-64: the first $16,100 of wages and
   self-employment income is not taxed. It falls 20% per step and is $0 at
   step 5.
2. **EITC offset at half:** in steps 1-4 the EITC falls by half of the adults'
   partial UBI (v2: all of it).
3. **Programs count the UBI in two parts.** SNAP and WIC count only the
   working-age UBI. School meals, housing aid and ACA credits count the
   working-age UBI plus 20% per step of the child and senior UBI.

## Employer payroll tax goes to workers as pay

The reform ends the employer part of Social Security and Medicare tax
(6.2% up to the wage cap, plus 1.45%). These runs pay all of it to the worker
as higher wages: $786B a year. This is the usual assumption of CBO, JCT and
Treasury: workers carry the employer payroll tax today, in lower pay.

- The higher pay is in the flat tax base, in state income tax, and in the
  earnings that benefits and poverty measures use.
- Earlier runs kept the employer saving out of household income. Then
  households lost about $790B in total at a revenue-neutral rate, because the
  saving went to nobody.
- Marginal tax rates now use the employer's cost of one more dollar of pay as
  the base, in the baseline and in the reform. So the baseline rates include
  the employer payroll tax, and they are higher than in earlier outputs.
- `configs/v2.yaml` turns pass-through off, so `outputs/v2/` stays as
  published.

## The stages

| | Phase 1 | Step 1 | Step 2 | Step 3 | Step 4 | Step 5 (end of schedule) | Long run |
|---|---|---|---|---|---|---|---|
| **Revenue-neutral rate** | **28.39%** | **30.06%** | **31.67%** | **33.22%** | **34.66%** | **35.62%** | **32.78%** |
| Rate before pass-through | 29.76% | 31.45% | 33.06% | 34.61% | 36.05% | 36.99% | 34.06% |
| Working-age UBI | $0 | $3,192 | $6,384 | $9,576 | $12,768 | $15,960 | $15,960 |
| Earnings exemption per person | $16,100 | $12,880 | $9,660 | $6,440 | $3,220 | $0 | $0 |
| UBI cost ($B) | 612 | 1,190 | 1,768 | 2,345 | 2,923 | 3,501 | 4,347 |
| Simple EITC ($B) | 68 | 34 | 16 | 8 | 4 | 0 | 0 |
| SNAP ($B; baseline 95) | 88 | 68 | 52 | 39 | 30 | 0 | 0 |
| **SPM poverty** (baseline 13.7%) | **10.1%** | **8.7%** | **7.4%** | **6.2%** | **5.0%** | **5.3%** | **5.7%** |
| Poverty before pass-through | 11.2% | 9.8% | 8.2% | 6.9% | 5.8% | 6.1% | 6.5% |
| Child poverty change (pp) | -5.2 | -5.9 | -7.1 | -8.3 | -9.8 | -8.5 | -8.9 |
| Adults 18-64 poverty change (pp) | -2.2 | -4.1 | -5.9 | -7.4 | -8.7 | -9.0 | -9.1 |
| 65+ poverty change (pp) | -6.5 | -6.9 | -7.2 | -7.3 | -7.4 | -6.5 | -3.6 |
| Deep poverty change (pp) | -1.3 | -1.6 | -2.1 | -2.3 | -2.4 | -2.2 | -2.2 |
| Gini change | -0.011 | -0.021 | -0.030 | -0.039 | -0.048 | -0.052 | -0.036 |
| Deciles that gain on average | 4 | 5 | 5 | 6 | 6 | 6 | 5 |

The long run has almost no legacy Social Security ($36B against $1,678B
today). Its losses for retirees come from that, as in v2.

## Who gains and who loses

**Net income change by decile** (deciles of income per person, baseline):

| Decile | Phase 1 | Step 1 | Step 2 | Step 3 | Step 4 | Step 5 | Long run |
|---|---|---|---|---|---|---|---|
| 1 | +34.2% | +43.1% | +53.5% | +64.7% | +75.3% | +78.5% | +81.0% |
| 2 | +9.5% | +11.8% | +14.7% | +18.3% | +22.1% | +24.0% | +25.3% |
| 3 | +3.6% | +6.6% | +9.7% | +12.8% | +15.8% | +18.2% | +16.1% |
| 4 | +1.8% | +4.1% | +6.3% | +8.4% | +10.1% | +11.7% | +6.1% |
| 5 | -0.3% | +1.5% | +3.2% | +4.8% | +6.2% | +7.6% | +3.2% |
| 6 | -2.2% | -1.2% | -0.4% | +0.5% | +1.3% | +2.3% | -0.8% |
| 7 | -3.0% | -2.4% | -1.8% | -1.4% | -1.1% | -0.5% | -2.3% |
| 8 | -3.0% | -2.9% | -2.8% | -2.9% | -3.0% | -2.7% | -2.8% |
| 9 | -3.3% | -3.9% | -4.6% | -5.3% | -6.0% | -6.3% | -4.9% |
| 10 | -0.2% | -1.9% | -3.6% | -5.3% | -6.8% | -7.8% | -5.0% |

**Net income change by family type:**

| Family type | Phase 1 | Step 1 | Step 2 | Step 3 | Step 4 | Step 5 | Long run |
|---|---|---|---|---|---|---|---|
| Single | +1.2% | +1.4% | +1.6% | +1.8% | +1.9% | +2.3% | +5.2% |
| Couple | -0.8% | -0.9% | -1.1% | -1.4% | -1.7% | -1.7% | -0.6% |
| Single parent | +4.4% | +3.6% | +3.1% | +2.6% | +2.8% | +0.4% | +1.4% |
| Couple with children | +0.6% | +0.5% | +0.5% | +0.5% | +0.6% | +0.7% | +4.0% |
| 65+ household | -2.0% | -3.6% | -5.2% | -6.7% | -8.1% | -9.5% | -16.7% |
| 3+ adults | 0.0% | +1.2% | +2.3% | +3.4% | +4.4% | +5.6% | +6.9% |

**65+ households by income fifth** (change in net income; in brackets, the
share of people who lose more than 5%):

| Fifth | Phase 1 | Step 1 | Step 4 | Step 5 |
|---|---|---|---|---|
| Bottom | +55% (2%) | +54% (2%) | +51% (3%) | +41% (8%) |
| Second | +4% (10%) | +3% (12%) | +2% (16%) | +1% (19%) |
| Middle | -3% (43%) | -3% (45%) | -7% (51%) | -8% (52%) |
| Fourth | -8% (71%) | -8% (72%) | -13% (79%) | -15% (82%) |
| Top | -5% (63%) | -6% (67%) | -13% (87%) | -15% (92%) |

**People in the bottom half (deciles 1-5) who lose more than 5%:** 14.4 M in
phase 1, 8.1 M at step 1, 11.7 M at step 4, 15.9 M at step 5 (of about 173 M).

## What the numbers say

1. **Pass-through lowers the rate by about 1.4 points at every stage.** Phase
   1 is 28.4% (before: 29.8%). Step 4 is 34.7% (before: 36.1%) and step 5 is
   35.6% (before: 37.0%). The extra pay widens the tax base, so the same
   revenue needs a lower rate.

2. **Poverty falls about 1 point more at every stage.** It is 10.1% in phase 1
   and 5.0% at step 4. Child poverty falls 5.2 points in phase 1 and 9.8
   points at step 4.

3. **The bottom half gains on average from step 1.** In phase 1, deciles 1-4
   gain and decile 5 loses 0.3%. From step 1, deciles 1-5 gain. From step 3,
   decile 6 also gains.

4. **Five of six family types do not lose on average, at every stage.** Only
   65+ households lose on average. Couples without children lose a little
   (-0.8% to -1.7%). Households of 3+ adults are even in
   phase 1 and gain from step 1.

5. **Retirees in the middle and upper fifths carry the cost.** People 65+ get
   no exemption and almost no pass-through, but they pay the flat rate on pensions,
   investments and taxable Social Security. 65+ households in the bottom two
   fifths gain. In the middle fifth they lose 3% in phase 1 and 8% at step 5;
   in the top two fifths 5-15%. Their poverty still falls 6.5-7.4 points to
   step 4.

6. **The step 5 bump is smaller but still there.** Poverty rises from 5.0% at
   step 4 to 5.3% at step 5, and child poverty rises 1.3 points. Single
   parents go from +2.8% to +0.4% of net income. At step 5, SNAP ($30B) and
   WIC end, the last $3,220 of exemption goes, the EITC ends, and all child
   and senior UBI counts in the continuing programs.

7. **The 35% ceiling (spec 10a) is needed only at step 5.** Step 4 is below
   35%. Step 5 is above it by 0.6 points. One point of rate is about $215B a
   year at step 5, so the drawdown is about $135B in that year, then less
   each year as legacy Social Security shrinks.

8. **Marginal tax rates.** On the employer-cost base, workers in the bottom
   decile face 33% in phase 1 (today: 28%) and 40% at step 5. At step 5 every
   decile faces about 40-41%: the 35.6% flat rate plus state income tax.
   Today the rates go from 28% to 41%.

## Biggest losers (average loss of net income, revenue-neutral rate)

**Phase 1 (28.39%)**

| # | Who | People | Change |
|---|---|---|---|
| 1 | Retired households, fourth fifth, mainly Social Security | 3.7 M | -$12,000 (-10.7%) |
| 2 | Couples with children, fourth fifth, mainly pensions and investments | 2.6 M | -$18,000 (-10.4%) |
| 3 | Couples, fourth fifth, mainly pensions and investments | 2.4 M | -$12,700 (-9.7%) |
| 4 | Couples with children, middle fifth, mainly pensions and investments | 2.1 M | -$10,700 (-8.4%) |
| 5 | 3+ adults, fourth fifth, mainly pensions and investments | 5.7 M | -$14,000 (-8.0%) |

**Step 1 (30.06%)**

| # | Who | People | Change |
|---|---|---|---|
| 1 | Retired households, fourth fifth, mainly Social Security | 3.7 M | -$13,200 (-11.8%) |
| 2 | Couples with children, fourth fifth, mainly pensions and investments | 2.6 M | -$17,700 (-10.3%) |
| 3 | Retired households, fourth fifth, mainly pensions and investments | 3.4 M | -$10,800 (-9.2%) |
| 4 | Couples, fourth fifth, mainly pensions and investments | 2.4 M | -$11,800 (-9.1%) |
| 5 | Retired households, top fifth, mainly pensions and investments | 7.7 M | -$25,200 (-7.5%) |

**Step 4 (34.66%)**

| # | Who | People | Change |
|---|---|---|---|
| 1 | Retired households, fourth fifth, mainly Social Security | 3.7 M | -$16,800 (-15.0%) |
| 2 | Retired households, fourth fifth, mainly pensions and investments | 3.4 M | -$15,700 (-13.3%) |
| 3 | Retired households, top fifth, mainly pensions and investments | 7.7 M | -$43,500 (-13.0%) |
| 4 | Couples, top fifth, mainly pensions and investments | 6.8 M | -$38,900 (-10.6%) |
| 5 | Couples with children, fourth fifth, mainly pensions and investments | 2.6 M | -$16,900 (-9.8%) |

**Step 5 (35.62%)**

| # | Who | People | Change |
|---|---|---|---|
| 1 | Retired households, fourth fifth, mainly Social Security | 3.7 M | -$17,800 (-15.8%) |
| 2 | Retired households, fourth fifth, mainly pensions and investments | 3.4 M | -$16,900 (-14.3%) |
| 3 | Retired households, top fifth, mainly pensions and investments | 7.7 M | -$47,500 (-14.2%) |
| 4 | Couples, top fifth, mainly pensions and investments | 6.8 M | -$41,700 (-11.3%) |
| 5 | Couples with children, fourth fifth, mainly pensions and investments | 2.6 M | -$16,100 (-9.3%) |

**Long run (32.78%):** all five biggest losers are households that live
mainly on Social Security, in the second to fourth fifths. They lose 29-45%,
because legacy Social Security is gone in this snapshot (as in v2).

No group of low-income workers or low-income families is in the top five at
any stage.

## Design issues the numbers show

1. **The step 5 bump.** Options:
   - End SNAP and WIC one step later (year 7), or cut them in two steps.
   - Keep a small part of the exemption at step 5 and end it at year 7.
   - Make the last UBI step a little larger for children.
2. **Retirees in the middle and upper fifths.** They pay for much of the
   exemption, because it is for people 18-64 only and they get no
   pass-through. A means-tested senior exemption, or a lower early rate on
   pension income, would move some of the cost back to workers.
3. **Bottom-half losers.** 8-16 M people in deciles 1-5 still lose more than
   5%, even when their decile gains on average. Spec work on who they are is
   still open.

## Approximations and limits

The same as v2 (see `outputs/v2/SUMMARY.md`): employer health premiums
imputed; Medicaid not computed; no 5-year wait, inheritances, SSDI family
members or SSDI taper; TANF, child care, Head Start and LIHEAP do not count
the UBI; business tax and employer insurance premium outside the
microsimulation; static, one year, no trust fund in the model.

Pass-through is full and at once. In practice, pay may adjust over some
years. State income tax rises about $39B a year, because states tax the
higher pay; this is not in the federal budget.

Marginal tax rates are computed for phase 1, step 5 and the long run only;
steps 1-4 ran without them.
