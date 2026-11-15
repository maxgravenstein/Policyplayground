"""Single-household tests for the spec v3 changes (docs/SPEC_v3.md)."""

from __future__ import annotations

import copy
from functools import lru_cache

import numpy as np
import pytest

from conftest import ROOT, YEAR, situation

U = 15960
PT = 1.0765  # wages with the employer payroll tax paid out as wages (v3 config), below the wage cap


@lru_cache(maxsize=None)
def system(config: str, scenario: str):
    from policyengine_us import CountryTaxBenefitSystem

    from flatubi.config import load_config, resolve
    from flatubi.reform.v2 import build_reform_v2

    pol = resolve(load_config(ROOT / "configs" / config), scenario)
    return build_reform_v2(pol)(CountryTaxBenefitSystem()), pol


def run(people, config, scenario):
    from policyengine_us import Simulation

    tbs, pol = system(config, scenario)
    sim = Simulation(situation=copy.deepcopy(situation(people)), tax_benefit_system=tbs)
    return (lambda v: np.asarray(sim.calculate(v, YEAR), float)), pol


def test_phase1_earnings_exemption():
    r, pol = run({"a": {"age": 30, "employment_income": 30000}}, "v3.yaml", "v3_phase1")
    assert r("flatubi_earnings_exemption")[0] == pytest.approx(16100)
    assert r("flatubi_flat_tax")[0] == pytest.approx(pol.flat_rate * (30000 * PT - 16100))


def test_exemption_covers_self_employment_and_not_65_plus():
    r, _ = run({"a": {"age": 40, "self_employment_income": 10000}}, "v3.yaml", "v3_phase1")
    assert r("flatubi_earnings_exemption")[0] == pytest.approx(10000)
    assert r("flatubi_flat_tax")[0] == pytest.approx(0)
    r, _ = run({"a": {"age": 70, "employment_income": 30000}}, "v3.yaml", "v3_phase1")
    assert r("flatubi_earnings_exemption")[0] == 0


def test_exemption_shrinks_by_step():
    r, _ = run({"a": {"age": 30, "employment_income": 30000}}, "v3.yaml", "v3_step2")
    assert r("flatubi_earnings_exemption")[0] == pytest.approx(16100 * 0.6)
    r, _ = run({"a": {"age": 30, "employment_income": 30000}}, "v3.yaml", "v3_step5")
    assert r("flatubi_earnings_exemption")[0] == 0


def test_social_security_rule_uses_earnings_before_exemption():
    # Age 63, already receiving: $20,000 wages + $20,000 Social Security.
    people = {"a": {"age": 63, "employment_income": 20000, "social_security_retirement": 20000}}
    r, _ = run(people, "v3.yaml", "v3_phase1")
    # Provisional income = 21,530 (wages with pass-through) + 10,000 = 31,530
    # -> 50% x 6,530 = 3,265 taxable.
    assert r("flatubi_taxable_social_security")[0] == pytest.approx(0.5 * (20000 * PT + 10000 - 25000))


def test_eitc_offset_is_half_of_partial_ubi():
    people = {"p": {"age": 30, "employment_income": 20000}, "c1": {"age": 4}, "c2": {"age": 7}}
    r1, _ = run(people, "v3.yaml", "v3_phase1")
    r3, _ = run(people, "v3.yaml", "v3_step1")
    assert r3("flatubi_simple_eitc")[0] == pytest.approx(max(r1("flatubi_simple_eitc")[0] - 0.5 * U / 5, 0))


def test_snap_counts_only_working_age_ubi_in_v3():
    people = {"p": {"age": 30, "employment_income": 20000}, "c1": {"age": 4}, "c2": {"age": 7}}
    r2, _ = run(people, "v2.yaml", "v2_step1")
    r3, _ = run(people, "v3.yaml", "v3_step1")
    assert r3("flatubi_ubi_counted_end").sum() == pytest.approx(U / 5)  # parent only, not the children
    assert r3("snap").sum() > r2("snap").sum()
    # Continuing programs count 20% of the child UBI at step 1.
    assert r3("flatubi_ubi_counted_cont").sum() == pytest.approx(U / 5 + 0.2 * 6000)


def test_employer_payroll_tax_paid_as_wages():
    # $50,000 wages: employer tax 7.65% = $3,825 goes to the worker as pay.
    r, pol = run({"a": {"age": 30, "employment_income_before_lsr": 50000}}, "v3.yaml", "v3_step5")
    assert pol.payroll_to_wages
    assert r("flatubi_payroll_passthrough")[0] == pytest.approx(3825)
    assert r("employment_income")[0] == pytest.approx(53825)
    assert r("flatubi_flat_tax")[0] == pytest.approx(pol.flat_rate * 53825)
    # Off in the v2 config, to keep the published v2 results.
    r, pol = run({"a": {"age": 30, "employment_income_before_lsr": 50000}}, "v2.yaml", "v2_step5")
    assert not pol.payroll_to_wages
    assert r("employment_income")[0] == pytest.approx(50000)


def test_payroll_passthrough_respects_wage_cap():
    r, _ = run({"a": {"age": 45, "employment_income_before_lsr": 400000}}, "v3.yaml", "v3_step5")
    from policyengine_us import CountryTaxBenefitSystem

    cap = CountryTaxBenefitSystem().parameters(f"{YEAR}-01-01").gov.irs.payroll.social_security.cap
    assert r("flatubi_payroll_passthrough")[0] == pytest.approx(0.062 * cap + 0.0145 * 400000)
