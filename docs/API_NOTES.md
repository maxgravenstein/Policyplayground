# PolicyEngine API notes

Written on 2026-11-09 for spec Section 3.1. Read again when you upgrade a package:
the PolicyEngine API changes often.

## Versions

| Package | Version |
|---|---|
| policyengine-us | 2.107.4 |
| policyengine-core | 3.34.10 |
| policyengine-us-data | 1.89.0 (installed; not used to build data) |
| Python | 3.13 |

The `policyengine.github.io` docs and `policyengine.org` were not used as the
primary source. All facts below come from reading the installed package code and
from running test households.

## Data

* `policyengine_us.system.DEFAULT_DATASET` is now the **Populace** file
  (`hf://datasets/policyengine/populace-us/populace_us_2024.h5`), not the Enhanced
  CPS. The spec asks for the Enhanced CPS, so we pass the file path ourselves.
* The Enhanced CPS is `enhanced_cps_2024.h5` in the Hugging Face model repo
  `policyengine/policyengine-us-data`.
* **Do not use the `main` copy (also tag 1.115.5).** It was promoted on
  2026-05-20 from a patch candidate and holds $9.3 trillion of
  `miscellaneous_income` and $0.8 trillion of `salt_refund_income`. With it, the
  2026 federal income tax comes out at $4.4 trillion.
* **We use tag `1.115.3`.** Its 2026 totals are plausible (income tax $2.16T,
  Social Security $1.79T, SNAP $114B). `partnership_s_corp_income` is almost zero
  in this file, which is one reason the income tax is low against CBO.
* `flatubi.run.dataset_path` downloads the file once with
  `huggingface_hub.hf_hub_download(repo, file, revision="1.115.3")`.
  The network must allow `huggingface.co` and `us.aws.cdn.hf.co`.
* **Populace** (`hf://datasets/policyengine/populace-us/populace_us_2024.h5`,
  revision `populace-us-2024-spm-20260909`, 827 MB) is the default dataset of
  policyengine-us 2.107.4. Config: `configs/populace.yaml`, outputs in
  `outputs/populace/`.
  * Layout: one PyTables table per entity (166,321 people, 57,240 households),
    not one array per variable. `Microsimulation(dataset=path)` reads it as is.
  * One simulation peaks at about 13.1 GB, so only one fits at a time on 15 GB.
    `flatubi.run` runs each simulation in a fresh process
    (`multiprocessing` "spawn", one task per process).
  * It has **no `employer_sponsored_insurance_premiums`**, so employer health
    premiums are not in the flat tax base on Populace (spec 2.2: "if the
    dataset has them"). In the Enhanced CPS they were $1.24T in 2026.
  * Its 2026 baseline is much closer to published totals: income tax $2,595B,
    Social Security $1,678B, SNAP $95B, SSI $57B, EITC $70B, SPM poverty 13.7%.
    Housing assistance is too low ($6B).
* The data year is 2024. PolicyEngine ages it to 2026 with its own uprating.

## (a) Run a microsimulation on the Enhanced CPS

```python
from policyengine_us import Microsimulation
sim = Microsimulation(dataset="data/ecps_1.115.3/enhanced_cps_2024.h5")
sim.calculate("household_net_income", 2026)                 # weighted MicroSeries
sim.calculate("income_tax", 2026, map_to="household")         # sum to households
```

About 4 minutes for the first full calculation on 4 CPUs, 6-8 GB RAM.

**Do not call `marginal_tax_rate` on the full data on a 15 GB machine.** It copies
the simulation into a branch and the process is killed for lack of memory. We
compute the MTR with a second simulation instead (`flatubi.run.add_mtr`): set
`employment_income_before_lsr` to wages + $1,000 for every worker with
`sim.set_input(...)` before any calculation, and compare household net income.

## (b) Apply a reform from a parameter dictionary

```python
from policyengine_core.reforms import Reform
r = Reform.from_dict({"gov.contrib.ubi_center.flat_tax.abolish_federal_income_tax":
                      {"2026-01-01.2100-12-31": True}}, country_id="us")
```

In this project we set parameters inside a `Reform.apply` with
`self.modify_parameters(fn)` and `parameter.update(start=..., stop=..., value=...)`.

## (c) Custom reform in code

```python
class R(Reform):
    def apply(self):
        self.update_variable(MyVariable)   # replace an existing variable
        self.add_variable(NewVariable)     # add a new one
        self.neutralize_variable("snap")   # always returns 0, ignores inputs
        self.modify_parameters(fn)
```

For single households, build the system once and reuse it (a reform system
takes about 50 seconds to build):

```python
from policyengine_us import CountryTaxBenefitSystem, Simulation
tbs = R(CountryTaxBenefitSystem())
Simulation(situation=situation, tax_benefit_system=tbs)
```

## Parameter search (spec 3.2)

| Lead | Found | Used? |
|---|---|---|
| `gov.contrib.ubi_center.basic_income.*` | `amount.person.by_age` (age brackets), `amount.person.flat`, `phase_out.*`, `taxable` | No. We replace the `basic_income` formula with the sum of our person variable `flatubi_ubi`, because phase1 needs a per-person Social Security offset. We keep `taxable = false`. |
| `gov.contrib.ubi_center.flat_tax.rate.gross_income`, `.rate.agi` | Flat tax on `positive_gross_income` or AGI of the **tax unit** | No. The base is too narrow (no employer health, no tax-exempt interest) and it is per tax unit. We replace the `flat_tax` formula. |
| `gov.contrib.ubi_center.flat_tax.abolish_federal_income_tax` | Sets `income_tax`, `income_tax_before_refundable_credits` and the refundable credits in net income to 0 | **Yes.** Removes brackets, deductions, all federal credits, the capital gains rate, AMT and NIIT in one switch. |
| `gov.contrib.ubi_center.flat_tax.abolish_payroll_tax` | Zeroes `employee_payroll_tax`, which **includes state payroll tax** (e.g. CA SDI) | No. We neutralize the federal parts instead: `employee_social_security_tax`, `employee_medicare_tax`, `additional_medicare_tax`, `self_employment_tax`. |
| `gov.contrib.ubi_center.flat_tax.abolish_self_emp_tax` | Zeroes `self_employment_tax` | No (neutralized directly). |
| `gov.abolitions.<variable>` | Created at run time for every computed variable by `add_abolition_parameters` | No. `neutralize_variable` also covers input variables such as `unemployment_compensation` and the Social Security parts. |
| `gov.hud.abolition` | Takes housing out of the benefit lists | **Yes**, with `housing_assistance` and `spm_unit_capped_housing_subsidy` neutralized. |
| `gov.ssa.ssi.income.sources.unearned` | List of SSI unearned income sources | **Yes**, only when `ubi.counts_as_ssi_income: true` (we append `flatubi_ubi`). |
| `gov.irs.payroll.*`, `gov.irs.capital_gains.*`, `gov.irs.deductions.*`, `gov.irs.credits.*` | Present | Not needed: the whole federal income tax and the federal payroll taxes are switched off. |

## How the pieces reach net income and poverty

* `household_net_income = household_market_income + household_benefits + household_refundable_tax_credits - household_tax_before_refundable_credits - household_health_costs`.
* `basic_income` is in `household_benefits` and in `spm_unit_benefits` (SPM resources).
* `flat_tax` is in `household_tax_before_refundable_credits` and in `spm_unit_taxes`.
* `aca_ptc` is **not** in household net income by default
  (`gov.simulation.include_health_benefits_in_net_income = false`). Our report
  adds `aca_ptc` to net income in both baseline and reform
  (`distribution.count_aca_ptc_as_income`, default true).
* Employer payroll taxes are not in household net income. The budget table counts
  them; in the reform they are 0.

## How programs count the UBI (spec 5.1, SSI test)

* `basic_income` is added to AGI, to Medicaid MAGI and to some MAGI tests only if
  `gov.contrib.ubi_center.basic_income.taxable` is true. It is false here.
* `ssi_unearned_income` adds the list `gov.ssa.ssi.income.sources.unearned`, which
  does not contain `basic_income`. **Result: SSI does not count the UBI.** The SSI
  test household (age 40, disabled, no income, Texas) gets the same SSI in the
  reform as in the baseline ($11,928 in 2026), plus the full UBI.
* With `ubi.counts_as_ssi_income: true`, the UBI ($15,960) is above the federal
  SSI rate, so SSI goes to zero for that household.
* SNAP unearned income does not list `basic_income` either. This matters only in
  phase1, where SNAP is kept.

## Things that surprised us

* `meets_ssi_disability_criteria` is an input with no formula, and the Enhanced
  CPS does not supply it. So SSI for disabled people under 65 is almost zero on
  this data (baseline SSI about $9B, against about $60B in reality). A test
  household must set it to `True` to get SSI.
* When the reform removes Social Security, poor retirees become eligible for
  SSI (aged). Example: age 70, $24,000 Social Security, no other income: the
  reform pays the $15,960 UBI plus about $12,600 of SSI and Texas supplement.
* Some SPM units in the data have no member that the SPM code (the new
  `spm_calculator` package) counts as an adult, and `person_in_poverty` then stops
  with `SPMInputError`. `flatubi/reform/datafix.py` sets the adult count to at
  least 1. The same fix runs in baseline and reform.
* PolicyEngine's `marginal_tax_rate` is measured only for the adults with the
  highest market income in each household (`marginal_tax_rate_computed`). Our own
  MTR is per household (all workers bumped at once). Both use
  `household_net_income`, so they include state taxes and benefit phase-outs, but
  not Medicaid.
* Baseline SPM poverty on this data is 23.7% for 2026, against 13.1% from the
  Census for 2025. SPM thresholds look right (median $44,600 for 4 people); the
  gap is in resources: `spm_unit_net_income` ($12.8T) is about $1.2T below market
  income + benefits - taxes - child care, which points to large medical
  out-of-pocket costs. We report the level as a flagged gap and use the change.
* Baseline totals against published totals: income tax -21% (low
  partnership/S-corp income in this file), SNAP +27%, housing assistance $172B
  (HUD rental aid is nearer $60B), SSI $9B (about $60B in reality).
* Neutralizing an input variable prints a warning each time a situation sets it.
  That is expected.
