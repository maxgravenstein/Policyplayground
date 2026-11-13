# flatubi: Flat Tax + UBI microsimulation

This tool tests one policy system against current law on real household data
(Enhanced CPS), with [PolicyEngine US](https://github.com/PolicyEngine/policyengine-us).
It answers three questions:

1. **Budget:** how much does the system cost and collect in one year?
2. **Distribution:** who gains and who loses, by income, age and household type?
3. **Rate:** what flat tax rate makes the system revenue-neutral?

The model is **static and annual**. People do not change behavior, unless you
turn on the rough behavior module (`behavior.enabled`).

The results of the last runs are in [`outputs/SUMMARY.md`](outputs/SUMMARY.md).

## The policy

| Part | Default |
|---|---|
| UBI | $15,960 per adult (18+), $3,000 per child. Not taxable. No phase-out. |
| Flat tax | 38.25% on each person's own income. No brackets, deductions or credits. Capital gains at the same rate. Employer health premiums in the base. |
| Taxes removed | Federal income tax (with EITC, CTC and all credits), federal payroll and self-employment taxes |
| Programs removed | SNAP, TANF, WIC, housing assistance, ACA premium credits, unemployment insurance, Social Security (steady state) |
| Programs kept | Medicaid, CHIP, SSI, Medicare, school meals |
| Corporate tax | flat_rate x $1.6T profits, outside the microsimulation |

Every number is in [`config.yaml`](config.yaml).

### Scenarios

* `steady_state`: the full system.
* `phase1`: UBI only for children and people 65+. Social Security is kept and
  offset: each beneficiary 65+ gets max(Social Security, UBI). Working-age
  adults keep SNAP, TANF, WIC, housing, UI and ACA credits. Flat tax for all.
* `custom`: every switch exactly as in the config. Add `custom: {ubi_min_age: 65}`
  for an age limit.

## Set up

```bash
python3 -m venv .venv && . .venv/bin/activate
pip install -e ".[dev]"
```

The first run downloads `enhanced_cps_2024.h5` (108 MB, tag 1.115.3) from
Hugging Face into `data/`. The network must allow `huggingface.co` and
`us.aws.cdn.hf.co`. A run needs about 8 GB of RAM.

## Use

```bash
python -m flatubi run --config config.yaml                  # scenario from the config
python -m flatubi run --config config.yaml --scenario phase1
python -m flatubi run --config config.yaml --no-mtr         # faster, no MTR tables
python -m flatubi solve-rate --config config.yaml           # uses the saved run
python -m flatubi compare --configs a.yaml b.yaml
python -m flatubi baseline-check --config config.yaml       # 5.2 totals only
python -m flatubi report --scenario phase1                  # rebuild report from the saved run
python -m flatubi run --config configs/populace.yaml --scenario phase1   # Populace data
python -m flatubi run --config config.yaml --flat-rate 0.33 --output-name test   # one-off rate
```

A run takes about 15 minutes on 4 CPUs (9 with `--no-mtr`) (the baseline part is cached after the
first run). Each run writes `outputs/<scenario>_<year>/`:

| File | What |
|---|---|
| `report.html` | All tables and charts, config, versions, limits |
| `budget.csv` | Budget table, $ billions |
| `distribution_*.csv` | By decile, age group and household type |
| `poverty.csv`, `inequality.csv` | SPM poverty, deep poverty, Gini |
| `mtr_decile.csv`, `mtr_not_flat.csv` | Marginal tax rates |
| `losers.csv` | The 10 household groups that lose the most |
| `*_at_solved_rate.csv` | The same tables at the revenue-neutral rate |
| `aggregate_checks.csv`, `reform_checks.csv` | Spec 5.2 and 5.3 checks |
| `summary.json` | Key numbers |

### Two datasets

| | Enhanced CPS (`config.yaml`) | Populace (`configs/populace.yaml`) |
|---|---|---|
| Spec | yes (Section 3.1) | PolicyEngine's default dataset now |
| People in file | 101,000 | 166,000 |
| Memory per simulation | 8-11 GB | about 13 GB |
| Baseline income tax vs CBO | -21% | -6% |
| SSI, SNAP, SPM poverty | far off | close |
| Employer health premiums | yes | **no** (left out of the base) |
| Outputs | `outputs/` | `outputs/populace/` |

Each simulation runs in its own process (`run.isolate_simulations`), so that
memory is given back between simulations. Populace does not fit otherwise.

`configs/` holds the extra runs used in the summary: each scenario at its
revenue-neutral rate, and each scenario with the employer payroll tax paid out
as wages. Set `output_name` in a config to write to `outputs/<output_name>/`.

The notebook [`notebooks/explore.ipynb`](notebooks/explore.ipynb) loads a
config, runs it and shows the main tables.

## Tests

```bash
pytest tests/test_households.py          # 13 single-household tests, about 5 minutes
pytest tests/test_outputs.py             # output tables on a made-up population, 2 seconds
pytest tests/test_aggregates.py          # uses the saved runs in outputs/
FLATUBI_FULL=1 pytest tests/test_aggregates.py   # also the zero-rate check (one more full run)
```

Run the tests when no full simulation runs at the same time: two together can
use more than 15 GB of RAM.

## Code

```
config.yaml
src/flatubi/
  __main__.py        command line
  config.py          config -> resolved switches per scenario
  run.py             baseline and reform microsimulations -> small frames
  outputs.py         budget, distribution, poverty, MTR, losers, checks
  solver.py          revenue-neutral rate (bisection, tax step only)
  report.py          CSV files, charts, report.html
  published.yaml     published totals for the 5.2 check
  reform/
    ubi.py           UBI (2.1)
    flat_tax.py      broad base, flat tax, individual filing (2.2)
    programs.py      programs removed and kept (2.3, 2.4)
    phase1.py        Social Security offset (2.5)
    datafix.py       data fix used in baseline and reform
tests/
notebooks/explore.ipynb
docs/API_NOTES.md    PolicyEngine API, parameter paths, data problems found
```

The spec puts the project in a folder `flatubi/`. Here the repository root is
that folder.

## Limits

See the "Limits" section of each report and `docs/API_NOTES.md`. The main ones:
static, one year, survey data under-reports top incomes, no inheritances in the
data, corporate tax is outside the microsimulation, and PolicyEngine's SSI for
disabled people is almost zero on this data.
