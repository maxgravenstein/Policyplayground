# Spec v2: results by stage (2026)

Model of `docs/SPEC_v2.md` on Populace data (PolicyEngine US 2.107.4), 2026
population, static (no behavior change). Each stage is a one-year snapshot of
the same population. All numbers are at each stage's **revenue-neutral flat
rate**, found by the solver. SPM poverty is recomputed exactly at that rate:
in v2 nothing but the flat tax depends on the rate, and the recomputation
matches PolicyEngine for every person at the run rate.

Full tables and charts: `outputs/v2/<stage>_2026/report.html`.

## The stages

| | Phase 1 | Step 1 | Step 2 | Step 3 | Step 4 | Step 5 (end of schedule) | Long run |
|---|---|---|---|---|---|---|---|
| **Revenue-neutral rate** | **26.03%** | **27.99%** | **30.33%** | **32.69%** | **35.01%** | **36.99%** | **34.06%** |
| Working-age UBI | $0 | $3,192 | $6,384 | $9,576 | $12,768 | $15,960 | $15,960 |
| UBI cost ($B) | 612 | 1,190 | 1,768 | 2,345 | 2,923 | 3,501 | 4,347 |
| Simple EITC ($B) | 74 | 16 | 3 | 2 | 2 | 0 | 0 |
| Social Security paid ($B) | 1,678 | 1,678 | 1,678 | 1,678 | 1,678 | 1,678 | 36 (SSDI above the UBI) |
| SNAP ($B; baseline 95) | 95 | 41 | 28 | 18 | 12 | 0 | 0 |
| Net transfer ($B) | 420 | 508 | 635 | 800 | 991 | 1,205 | 1,784 |
| SPM poverty (baseline 13.7%) | 14.9% | 15.0% | 12.3% | 9.8% | 7.2% | **6.1%** | 6.5% |
| Poverty change (pp) | +1.2 | +1.2 | -1.4 | -3.9 | -6.5 | **-7.7** | -7.3 |
| Child poverty change (pp) | +1.8 | **+5.1** | +2.4 | -1.2 | -5.4 | -6.9 | -7.4 |
| Adults 18-64 poverty change (pp) | +3.2 | +1.9 | -1.4 | -4.2 | -6.9 | -8.3 | -8.4 |
| 65+ poverty change (pp) | **-6.3** | -5.7 | -6.2 | -6.4 | -6.6 | -6.4 | -3.4 |
| Deep poverty change (pp) | -0.5 | -1.0 | -1.6 | -2.0 | -2.2 | -2.2 | -2.1 |
| Gini change | +0.008 | -0.000 | -0.014 | -0.029 | -0.043 | -0.054 | -0.038 |
| Deciles that gain on average | 1 | 1 | 3 | 4 | 5 | 5 | 4 |
| Largest average loss, deciles 6-10 | -9.4% | -8.3% | -8.5% | -9.5% | -10.4% | -11.5% | -9.8% |
| Net income change, people 65+ | -0.6% | -2.0% | -3.5% | -5.0% | -6.5% | -7.8% | -13.2% |

Step 5 is the end of the 6-year schedule (year 6): full UBI; SNAP, TANF, WIC
and the EITC gone; housing aid still open to new families; legacy Social
Security paid to everyone who gets it today. The long run is the end state
with Social Security gone (except SSDI above the UBI) and housing aid gone,
applied to today's population.

## What the numbers say

1. **The rate rises 2.0-2.4 points per step:** 26.0% in phase 1, 37.0% at
   the end of the schedule. In the long run, when legacy Social Security is
   gone, it falls to 34.1%. The rate peaks at the end of the schedule because
   the full UBI and full legacy Social Security overlap.

2. **At the end of the schedule, poverty falls from 13.7% to 6.1%.** Child
   poverty falls 6.9 points, poverty for people 65+ 6.4 points, deep poverty
   2.2 points. Inequality falls (Gini -0.054). The bottom five deciles gain on
   average (3% to 75%); the top five lose (2% to 12%).

3. **Phase 1 protects retirees, as designed.** Poverty for people 65+ falls
   6.3 points, and their average net income barely changes (-0.6%). The floors
   and the current-law Social Security tax do this: only $530B of the $1,678B
   of Social Security is taxable.

4. **Phase 1 costs working-age people.** They pay 26% from the first dollar,
   with no UBI yet. Poverty for adults 18-64 rises 3.2 points. The biggest
   losers are single workers with low and middle earnings (-12% to -17%) and
   middle-income working families (about -10% to -12%).

5. **Step 1 is the weak point: child poverty rises 5.1 points**, more than in
   phase 1. The main cause: from step 1, SNAP, school meals, housing and ACA
   credits count **all** UBI as income, including the children's $3,000 and
   the seniors' UBI that phase 1 paid without counting. A SNAP family with two
   children suddenly has $6,000 more counted income. SNAP falls from $95B to
   $41B: $37B from smaller benefits and $16B from 6.2 million households that
   lose SNAP entirely (its gross income limit). At the same time, the EITC
   offset takes away the new adult UBI from working families. Single parents
   lose 7.9% of net income on average.

6. **From step 2 on, poverty falls at every step.** By step 3 child poverty is
   below today's.

7. **Retirees with pensions and investments pay more at every step.** Their
   pensions, investment income and part of their Social Security are taxed at
   a rising rate. At the end of the schedule the biggest losers are retired
   households in the top two fifths (-15% to -17%), and higher-income
   households living on investments.

8. **The long run shows the end state on today's population.** Households of
   people 65+ lose 13% of net income on average, but their poverty still falls
   3.4 points, because SSI catches retirees with no other income. Note: in the
   real long run, today's retirees have legacy benefits for life, and future
   retirees will have paid no payroll tax. The long run therefore overstates
   the loss for any real person.

9. **Marginal tax rates** (all taxes, including state, at the run rates): at
   the end of the schedule about 41-43% in every decile (today 22-37%); in the
   long run about 38-40%. In phase 1 the top two deciles' rate falls to about
   31%.

## Biggest losers (average loss of net income, revenue-neutral rate)

**Phase 1 (26.03%)**

| # | Who | People | Change |
|---|---|---|---|
| 1 | Single adults under 65, bottom fifth, living on earnings | 3.0 M | -$2,600 (-17%) |
| 2 | Single adults under 65, second fifth, earnings | 2.3 M | -$5,500 (-13%) |
| 3 | Couples with children, fourth fifth, mainly pensions and investments | 2.6 M | -$20,700 (-12%) |
| 4 | Single adults under 65, middle fifth, earnings | 1.9 M | -$6,800 (-12%) |
| 5 | Couples without children, middle fifth, earnings | 8.4 M | -$9,500 (-11%) |

**Step 1 (27.99%)**

| # | Who | People | Change |
|---|---|---|---|
| 1 | Couples with children, fourth fifth, mainly pensions and investments | 2.6 M | -$20,400 (-12%) |
| 2 | Single parents, second fifth, earnings | 2.5 M | -$6,000 (-11%) |
| 3 | Couples with children, middle fifth, mainly pensions and investments | 2.1 M | -$14,000 (-11%) |
| 4 | Retired households, fourth fifth, mainly Social Security | 3.7 M | -$12,300 (-11%) |
| 5 | Single parents, bottom fifth, earnings | 12.6 M | -$4,000 (-10%) |

**Step 5, end of schedule (36.99%)**

| # | Who | People | Change |
|---|---|---|---|
| 1 | Retired households, fourth fifth, mainly Social Security | 3.7 M | -$18,800 (-17%) |
| 2 | Retired households, top fifth, mainly pensions and investments | 7.7 M | -$53,700 (-16%) |
| 3 | Retired households, fourth fifth, mainly pensions and investments | 3.4 M | -$18,400 (-16%) |
| 4 | Couples, top fifth, mainly pensions and investments | 6.8 M | -$51,700 (-14%) |
| 5 | Couples with children, top fifth, mainly pensions and investments | 5.7 M | -$54,600 (-12%) |

In all of these groups the loss is tax: the flat tax on pensions, investment
income, part of Social Security and (from step 1) employer health premiums.

**Long run (34.06%)**: the ten biggest losers are again Social Security
households (-15% to -46%), because the long run removes Social Security from
today's retirees. See point 8.

## Design issues the numbers show

1. **Step 1 hurts low-income families with children.** Options:
   - Programs start counting the UBI with the working-age UBI only, and count
     the child and senior UBI gradually over the steps.
   - Offset the EITC by only part of the partial UBI (for example half).
   - Make the first step larger, so the UBI clears the EITC and SNAP losses
     at once.
2. **Working-age adults lose in phase 1.** A small working-age UBI or an
   earnings exemption in phase 1 would help; both cost rate.
3. **The rate peaks at 37% at the end of the schedule**, while legacy Social
   Security is still large. Using the Social Security trust fund to pay legacy
   benefits (spec 5.2) would lower the flat rate needed in those years. The
   model does not include the trust fund.

## How v2 compares with the original spec (v1, Populace)

| | v1 | v2 |
|---|---|---|
| Phase 1 rate | 23.11% | 26.03% |
| Phase 1 poverty change | +3.8 pp | +1.2 pp |
| Phase 1, 65+ poverty change | -3.2 pp | -6.3 pp |
| End state rate | 34.40% (Social Security removed) | 34.06% long run; 36.99% at the end of the schedule |
| End state poverty | 13.7% to 5.3% | 13.7% to 6.5% (long run), 6.1% (end of schedule) |

Main reasons for the differences: v2 taxes Social Security only as current law
does, adds floors and the simple EITC, credits the 21% business tax on
dividends and keeps bond interest untaxed (all raise the rate); it limits the
UBI to citizens and qualified residents and adds employer health premiums to
the base (both lower it); and it keeps ACA credits and SSI, which catch more
people.

## Approximations and limits

- **Data:** Populace has no employer health premiums. They are imputed for
  workers with employer coverage and scaled to the 2026 national total of
  $1,240B. Medicaid cannot be computed on this machine; its line is blank.
- **Not in the data:** the 5-year wait for permanent residents (all are
  eligible), inheritances and gifts, retained profit in pass-through
  businesses, capital gains basis adjustment, loss carry-forward, home-sale
  indexing, SSDI family members and the SSDI work taper.
- **Simplified:** the simple EITC uses PolicyEngine's EITC formula with full
  take-up; the unemployment top-up is half of today's benefit; TANF, child
  care, Head Start and LIHEAP do not yet count the UBI.
- **Outside the microsimulation:** the business tax ($336B at 21%, unchanged)
  and the employer insurance premium (set equal to SSDI above the UBI and the
  unemployment top-up).
- **Static:** no change in work, saving, or realizations; one year; no trust
  fund; no state responses.
