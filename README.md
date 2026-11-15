# flatubi: Flat Tax + UBI microsimulation

This tool tests a Flat Tax + UBI design against current law on household
survey data, with [PolicyEngine US](https://github.com/PolicyEngine/policyengine-us)
(version 2.107.4). For each stage of the design it answers these questions:

1. **Budget:** how much does the system cost and collect in one year?
2. **Distribution:** who gains and who loses, by income decile, age and
   household type?
3. **Poverty:** how do SPM poverty, deep poverty and the Gini change?
4. **Rate:** what flat tax rate makes the stage revenue-neutral?

The model is **static and annual**: each stage is a one-year snapshot of the
2026 population, and people do not change behavior.

## Results

| Spec | Results | Data |
|---|---|---|
| **v3 (current)** | [`outputs/v3/SUMMARY.md`](outputs/v3/SUMMARY.md) | Populace |
| v2 | [`outputs/v2/SUMMARY.md`](outputs/v2/SUMMARY.md) | Populace |
| Original spec | [`outputs/SUMMARY.md`](outputs/SUMMARY.md) and [`outputs/populace/SUMMARY.md`](outputs/populace/SUMMARY.md) | Enhanced CPS and Populace |

The v3 runs pay the employer payroll tax that the reform removes to workers
as higher wages. The v2 runs do not (see "Employer payroll tax" below).

## The design (spec v3)

The current design is [`docs/SPEC_v3.md`](docs/SPEC_v3.md). Spec v2 is
[`docs/SPEC_v2.md`](docs/SPEC_v2.md). In short:

| Part | Rule |
|---|---|
| Flat tax | One rate on each person's income, with no brackets. The only deductions and credits are the simple EITC and the earnings exemption during the transition, and the business tax credit. It replaces federal income tax and payroll taxes. |
| UBI | $15,960 per adult (18+) and $3,000 per child, not taxed, no phase-out |
| Phase 1 | UBI for children and people 65+. Floors for Social Security beneficiaries. Simple EITC. The first $16,100 of each working-age person's earnings is not taxed. Programs are kept. |
| Phase 2 (steps 1-5) | Adults 18-64 get a partial UBI that rises in five equal steps. The earnings exemption falls 20% per step. Programs count the new UBI. |
| End state (step 5) | Full UBI for all. SNAP, TANF, WIC and the EITC end. |
| Long run | Legacy Social Security has almost ended ($36B a year against $1,678B today). |
| Business tax | 21% on all businesses; owners get a credit for it on dividends |
| Programs kept | SSI, Medicaid, CHIP, Medicare, school meals, housing aid (counting the UBI), ACA credits (counting the UBI) |

[`docs/TAX_CODE_MEASURE.md`](docs/TAX_CODE_MEASURE.md) measures how much of the
Internal Revenue Code the design removes (scripts `tools/*usc26.py`).

### Employer payroll tax

The reform ends the employer part of Social Security and Medicare tax. With
`tax.employer_payroll_to_wages: true`, the model pays that saving to each
worker as higher wages ($786B in 2026). This follows CBO, JCT and Treasury,
which assume that workers carry this tax today in lower pay. In the v2 and v3
model, the higher wages are taxed and count as earnings for benefits and
poverty. In the original-spec model, they are added only to the flat tax base.

| Model | Default | Set in |
|---|---|---|
| Spec v2 and v3 (`src/flatubi/reform/v2.py`) | true | `configs/v3.yaml`: true. `configs/v2.yaml`: false, to keep the published v2 results. |
| Original spec (`config.yaml`) | false | `configs/*_payroll_to_wages.yaml` turn it on |

## Set up

```bash
python3 -m venv .venv && . .venv/bin/activate
pip install -e ".[dev]"
```

The first run downloads the data from Hugging Face. The network must allow
`huggingface.co` and `us.aws.cdn.hf.co`.

| Data | Used by | File | Size |
|---|---|---|---|
| Populace US 2024 | `configs/v3.yaml`, `configs/v2.yaml`, `configs/populace.yaml` | `data/populace/populace_us_2024.h5` | 789 MB |
| Enhanced CPS 2024 (tag 1.115.3) | `config.yaml` | `data/ecps_1.115.3/enhanced_cps_2024.h5` | 106 MB |

A Populace run needs about 13 GB of RAM per simulation. Each simulation runs
in its own process (`run.isolate_simulations`), so that memory is given back
between simulations. Medicaid is not computed on Populace
(`run.skip_medicaid`), because it needs more than 15 GB.

## Use

```bash
# Spec v3, one stage: v3_phase1, v3_step1 ... v3_step5, v3_longrun
python -m flatubi run --config configs/v3.yaml --scenario v3_phase1
python -m flatubi run --config configs/v3.yaml --scenario v3_step3 --no-mtr   # faster, no MTR tables

# Spec v2, one stage: v2_phase1 ... v2_step5, v2_longrun
python -m flatubi run --config configs/v2.yaml --scenario v2_step3

# Rebuild the tables and report from the saved run (no new simulation)
python -m flatubi report --config configs/v3.yaml --scenario v3_step3

# Stage comparison table
python tools/summary_v2.py outputs/v3 > outputs/v3/stages.md

# Original spec (scenarios steady_state, phase1, custom)
python -m flatubi run --config config.yaml --scenario phase1
python -m flatubi solve-rate --config config.yaml           # uses the saved run
python -m flatubi compare --configs a.yaml b.yaml
python -m flatubi baseline-check --config config.yaml       # baseline totals against published totals
python -m flatubi run --config config.yaml --flat-rate 0.33 --output-name test   # one-off rate
```

For spec v2 and v3, the run finds the revenue-neutral rate and computes all
tables at that rate. The rate in the config is only a starting guess.

On Populace, with 4 CPUs, a stage takes about 25 minutes with or without
MTR tables. The first run takes about an hour, because it also computes the
baseline. The baseline is cached in `outputs/.cache/` after that.

Each run writes `<output_dir>/<scenario>_<year>/` (for v3:
`outputs/v3/v3_step3_2026/`):

| File | What |
|---|---|
| `report.html` | All tables and charts, config, versions, limits |
| `budget.csv` | Budget table, $ billions |
| `budget_at_run_rate.csv` | v2 and v3: the budget at the starting rate |
| `*_at_solved_rate.csv` | Original spec: the main tables at the revenue-neutral rate |
| `distribution_*.csv` | By decile, age group and household type |
| `poverty.csv`, `inequality.csv` | SPM poverty, deep poverty, Gini |
| `mtr_decile.csv`, `mtr_not_flat.csv` | Marginal tax rates (not with `--no-mtr`) |
| `losers.csv` | The household groups that lose the most |
| `aggregate_checks.csv`, `reform_checks.csv` | Baseline totals against published totals, and reform checks |
| `summary.json` | Key numbers |
| `result.pkl` | The saved run (not in git) |

In v2 and v3 runs, the marginal tax rate is the share of one more dollar of
the employer's cost of pay that the worker does not keep. It includes
employee and employer payroll taxes, in the baseline and in the reform.

## Tests

```bash
pytest tests/test_v3.py           # 8 single-household tests of the v3 rules
pytest tests/test_v2.py           # 11 single-household tests of the v2 rules
pytest tests/test_households.py   # 17 single-household tests of the original spec
pytest tests/test_outputs.py      # 7 tests of the output tables on a made-up population, seconds
pytest tests/test_aggregates.py   # 8 tests on saved original-spec runs (outputs/<scenario>_2026/result.pkl); skip if missing
FLATUBI_FULL=1 pytest tests/test_aggregates.py   # also the zero-rate check (one more full run)
```

The household tests take some minutes each, because each tax-benefit system
takes about a minute to build. Run one test file at a time, and not while a
full simulation runs: together they can use more than 15 GB of RAM.

## Code

```
config.yaml          original spec, Enhanced CPS
configs/
  v3.yaml            spec v3 stages, Populace
  v2.yaml            spec v2 stages, Populace
  populace.yaml      original spec, Populace
  *_revenue_neutral.yaml, *_payroll_to_wages.yaml   original spec, extra runs
src/flatubi/
  __main__.py        command line
  config.py          original spec: config -> resolved switches per scenario
  config_v2.py       spec v2 and v3: config -> resolved switches per stage
  run.py             baseline and reform microsimulations -> small frames, MTR
  outputs.py         budget, distribution, poverty, MTR, losers, checks
  solver.py          revenue-neutral rate
  report.py          CSV files, charts, report.html
  published.yaml     published totals for the baseline check
  reform/
    v2.py            spec v2 and v3 reform (all stages)
    ubi.py           original spec: UBI
    flat_tax.py      original spec: flat tax, individual filing
    programs.py      original spec: programs removed and kept
    phase1.py        original spec: Social Security offset in phase 1
    social_security.py   original spec: Social Security above the UBI
    datafix.py       data fix used in baseline and reform
tools/
  summary_v2.py      stage comparison table for v2 and v3
  *_usc26.py         tax code measure
tests/
notebooks/explore.ipynb
docs/
  SPEC_v3.md, SPEC_v2.md   policy design
  API_NOTES.md       PolicyEngine API, parameter paths, data problems found
  TAX_CODE_MEASURE.md
```

The original spec is not in the repository. Section numbers in the comments
of the original-spec code (for example "5.2 check") refer to it.

## Limits

See the "Limits" section of each report and of each SUMMARY.md, and
`docs/API_NOTES.md`. The main ones:
- The model is static and covers one year. The multi-year path (Social
  Security wind-down, trust fund drawdown) is outside it.
- Survey data under-reports top incomes.
- The data has no inheritances.
- Business tax is outside the microsimulation.
- Medicaid is not computed on Populace.
- Populace has no employer health premiums, so the v2 and v3 configs
  impute them.
