"""Aggregate checks (spec Sections 5.2 and 5.3).

These need the full microdata. They use the saved result of
`python -m flatubi run` (outputs/<scenario>_2026/result.pkl) when it exists,
and skip otherwise. Set FLATUBI_FULL=1 to also run the slow zero-rate check,
which runs one more full simulation (about 5 minutes).
"""

from __future__ import annotations

import copy
import os
import pickle
from pathlib import Path

import numpy as np
import pytest

from flatubi import outputs, solver

ROOT = Path(__file__).resolve().parents[1]


def saved(scenario: str):
    path = ROOT / "outputs" / f"{scenario}_2026" / "result.pkl"
    if not path.exists():
        pytest.skip(f"no saved run for {scenario}; run `python -m flatubi run --scenario {scenario}` first")
    with open(path, "rb") as f:
        return pickle.load(f)


@pytest.mark.slow
@pytest.mark.parametrize("scenario", ["steady_state", "phase1"])
def test_baseline_totals_reported(scenario):
    """5.2: every total is reported with its gap. A gap does not fail the run."""
    res = saved(scenario)
    table = outputs.aggregate_checks(res)
    expected = {"federal_income_tax", "payroll_taxes", "social_security", "snap", "eitc", "adults", "children", "spm_poverty_rate"}
    assert set(table["item"]) == expected
    assert table["model"].notna().all()
    assert table["published"].notna().all()
    big = table[table.gap_pct.abs() > 15]
    assert (big.flag == "GAP > 15%").all()


@pytest.mark.slow
def test_ubi_cost_matches_head_count():
    """5.3: total UBI = adults x adult UBI + children x child UBI, within 1%."""
    res = saved("steady_state")
    check = outputs.reform_checks(res)
    assert abs(check.gap_pct.iloc[0]) <= 1


@pytest.mark.slow
def test_phase1_ubi_never_above_head_count():
    res = saved("phase1")
    p = res.reform.person
    pol = res.policy
    cap = np.where(p.age >= pol.ubi_min_age, pol.ubi_adult, np.where(p.age < 18, pol.ubi_child, 0))
    assert (p.flatubi_ubi.to_numpy() <= cap + 1e-6).all()
    assert (p.flatubi_ubi.to_numpy() >= 0).all()


@pytest.mark.slow
@pytest.mark.parametrize("scenario", ["steady_state", "phase1"])
def test_solver_hits_target(scenario):
    res = saved(scenario)
    s = solver.solve_rate(res, target=0)
    assert s.converged
    assert abs(s.net_budget_billions) < 1.0
    assert 0 < s.rate < 1


@pytest.mark.slow
def test_rate_rescaling_is_linear():
    """The solver's shortcut: flat tax revenue is linear in the rate."""
    res = saved("steady_state")
    r0 = res.policy.flat_rate
    a = outputs.flat_tax_revenue(res, r0, behavior=False)
    b = outputs.flat_tax_revenue(res, r0 / 2, behavior=False)
    assert b == pytest.approx(a / 2)
    p = res.reform.person
    assert a == pytest.approx(float((p.weight * p.flatubi_flat_tax).sum()), rel=1e-9)


@pytest.mark.slow
@pytest.mark.skipif(os.environ.get("FLATUBI_FULL") != "1", reason="set FLATUBI_FULL=1 (runs a full simulation)")
def test_zero_rate_zero_ubi_aggregate():
    """5.3: with flat_rate = 0 and UBI = 0, reform = baseline minus the removed
    programs and taxes (in total net income)."""
    from flatubi import run as runmod
    from flatubi.config import load_config, resolve

    cfg = load_config(ROOT / "config.yaml")
    cfg = copy.deepcopy(cfg)
    cfg["tax"]["flat_rate"] = 0.0
    cfg["ubi"]["adult_annual"] = 0
    cfg["ubi"]["child_annual"] = 0
    res = runmod.run(cfg, scenario="steady_state", mtr=False, log=lambda *_: None)
    b, r = res.baseline.household, res.reform.household
    w = b.weight

    def tot(frame, cols):
        return float((frame[cols].sum(axis=1) * w).sum())

    removed = ["snap", "tanf", "wic", "housing_assistance", "unemployment_compensation"]
    if not res.policy.social_security_residual:  # with UBI = 0 the residual is all of it
        removed.append("social_security")
    taxes = ["income_tax"] + outputs.FEDERAL_PAYROLL
    expected = tot(b, ["household_net_income"]) + tot(b, taxes) - tot(b, removed)
    actual = tot(r, ["household_net_income"])
    # Removing programs changes SSI and state taxes, so allow a small gap and
    # report it.
    gap = (actual - expected) / expected
    print(f"zero-rate gap: {100 * gap:.2f}% (SSI change {(tot(r, ['ssi']) - tot(b, ['ssi'])) / 1e9:+.1f} B)")
    assert abs(gap) < 0.02
