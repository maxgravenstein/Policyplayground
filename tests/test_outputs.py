"""Fast tests of the output tables on a small made-up population (no simulation)."""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from flatubi import outputs, report, solver
from flatubi.config import load_config, resolve
from flatubi.run import HOUSEHOLD_VARIABLES, PERSON_VARIABLES, RunResult, SimResult

from conftest import ROOT


def fake_result(n_households: int = 400, seed: int = 0) -> RunResult:
    rng = np.random.default_rng(seed)
    cfg = load_config(ROOT / "config.yaml")
    pol = resolve(cfg, "steady_state")
    people = []
    for h in range(n_households):
        kind = rng.integers(0, 5)
        ages = {0: [30], 1: [40, 38], 2: [28, 5], 3: [45, 44, 10, 8], 4: [72, 70]}[kind]
        for a in ages:
            wage = 0.0 if a < 18 or a >= 65 else float(rng.lognormal(10.3, 1.0))
            ss = 20_000.0 if a >= 65 else 0.0
            people.append((h, a, wage, ss))
    p = pd.DataFrame(people, columns=["household_id", "age", "employment_income", "social_security"])
    p["weight"] = 100_000.0
    for c in PERSON_VARIABLES:
        if c not in p:
            p[c] = 0.0
    p["market_income"] = p.employment_income
    hb = pd.DataFrame({"household_id": np.arange(n_households), "weight": 100_000.0})
    g = p.groupby("household_id")
    for c in HOUSEHOLD_VARIABLES:
        hb[c] = 0.0
    hb["household_count_people"] = g.size().to_numpy()
    hb["employment_income"] = g.employment_income.sum().to_numpy()
    hb["household_market_income"] = hb.employment_income
    hb["social_security"] = g.social_security.sum().to_numpy()
    hb["income_tax"] = 0.15 * hb.employment_income
    hb["employee_social_security_tax"] = 0.062 * hb.employment_income
    hb["employer_social_security_tax"] = 0.062 * hb.employment_income
    hb["snap"] = np.where(hb.employment_income < 20_000, 3_000.0, 0.0)
    hb["household_net_income"] = (
        hb.household_market_income + hb.social_security + hb.snap - hb.income_tax - hb.employee_social_security_tax
    )
    # Reform.
    pr = p.copy()
    pr["flatubi_ubi"] = np.where(pr.age >= 18, pol.ubi_adult, pol.ubi_child)
    pr["flatubi_broad_income"] = pr.employment_income
    pr["flatubi_flat_tax"] = pol.flat_rate * pr.flatubi_broad_income
    pr["social_security"] = 0.0
    hr = hb.copy()
    gr = pr.groupby("household_id")
    hr["basic_income"] = gr.flatubi_ubi.sum().to_numpy()
    hr["flat_tax"] = gr.flatubi_flat_tax.sum().to_numpy()
    hr["flatubi_flat_tax"] = hr.flat_tax
    hr["flatubi_broad_income"] = gr.flatubi_broad_income.sum().to_numpy()
    for c in ["income_tax", "employee_social_security_tax", "snap", "social_security"]:
        hr[c] = 0.0
    hr["household_net_income"] = hr.household_market_income + hr.basic_income - hr.flat_tax
    # Poverty and MTR.
    p["person_in_poverty"] = p.household_id.map(hb.set_index("household_id").household_net_income < 15_000).astype(float)
    pr["person_in_poverty"] = pr.household_id.map(hr.set_index("household_id").household_net_income < 15_000).astype(float)
    p["mtr"] = np.where(p.employment_income > 0, 0.30, np.nan)
    pr["mtr"] = np.where(pr.employment_income > 0, pol.flat_rate, np.nan)
    p["mtr_measured"] = p.employment_income > 0
    pr["mtr_measured"] = p.mtr_measured
    meta = {"versions": {}, "dataset": "fake", "data_revision": "", "data_year": 2024, "year": 2026, "seconds": 0}
    return RunResult(pol, SimResult(p, hb), SimResult(pr, hr), meta)


@pytest.fixture(scope="module")
def res():
    return fake_result()


def test_all_tables_build(res):
    t = outputs.all_tables(res)
    for name in ["budget", "distribution_decile", "distribution_age", "distribution_type", "poverty", "inequality", "losers", "mtr_decile", "mtr_not_flat"]:
        assert isinstance(t[name], pd.DataFrame) and len(t[name]) > 0, name
    assert list(t["distribution_decile"].decile) == list(range(1, 11))


def test_budget_lines(res):
    b = outputs.budget_table(res).set_index("item")
    ubi = b.loc["UBI (gross)", "reform"]
    p = res.reform.person
    assert ubi == pytest.approx((p.weight * p.flatubi_ubi).sum() / 1e9, abs=0.1)
    assert b.loc["Federal income tax", "reform"] == 0
    assert b.loc["Payroll taxes (employee, employer, self-employment)", "reform"] == 0
    assert b.loc["Corporate tax (outside the microsimulation)", "reform"] == pytest.approx(0.3825 * 1600, abs=0.1)
    net = b.loc["Net budget effect (revenue minus spending)"]
    rev = b[b.group == "Revenue"][["baseline", "reform"]].sum()
    spend = b[b.group == "Spending"][["baseline", "reform"]].sum()
    assert net.difference == pytest.approx((rev.reform - spend.reform) - (rev.baseline - spend.baseline), abs=0.3)


def test_net_transfer(res):
    p = res.reform.person
    expected = (p.weight * (p.flatubi_ubi - p.flatubi_flat_tax).clip(lower=0)).sum()
    assert outputs.net_transfer(res) == pytest.approx(expected)


def test_solver_and_with_rate(res):
    s = solver.solve_rate(res, target=0)
    assert s.converged
    assert abs(s.net_budget_billions) < 0.05
    at = outputs.with_rate(res, s.rate)
    assert outputs.budget_table(at).set_index("item").loc["Net budget effect (revenue minus spending)", "difference"] == pytest.approx(0, abs=0.2)


def test_gini_bounds():
    assert outputs.gini([1, 1, 1, 1], [1, 1, 1, 1]) == pytest.approx(0, abs=1e-9)
    assert outputs.gini([0, 0, 0, 100], [1, 1, 1, 1]) == pytest.approx(0.75, abs=1e-9)


def test_household_types(res):
    h = outputs.household_frame(res)
    assert set(h.type) <= set(outputs.HOUSEHOLD_TYPES)
    assert {"Single", "Couple", "Single parent", "Couple with children", "65+ household"} <= set(h.type)


def test_report_renders(res, tmp_path):
    t = outputs.all_tables(res)
    s = solver.solve_rate(res)
    path = report.write_outputs(res, t, s, tmp_path)
    text = path.read_text()
    assert "Limits" in text and "Revenue-neutral" in text
    assert (tmp_path / "budget.csv").exists()
