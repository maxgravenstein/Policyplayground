"""Single-household tests for spec v2 (docs/SPEC_v2.md).

Texas households (no state income tax). Rates are the config's starting
rates for each stage, so expected values are exact.
"""

from __future__ import annotations

import copy
from functools import lru_cache

import numpy as np
import pytest

from conftest import ROOT, YEAR, situation

U, C = 15960, 3000


@lru_cache(maxsize=None)
def system(scenario: str):
    from policyengine_us import CountryTaxBenefitSystem

    from flatubi.config import load_config, resolve
    from flatubi.reform.v2 import build_reform_v2

    pol = resolve(load_config(ROOT / "configs" / "v2.yaml"), scenario)
    return build_reform_v2(pol)(CountryTaxBenefitSystem()), pol


def run(people, scenario):
    from policyengine_us import Simulation

    tbs, pol = system(scenario)
    sim = Simulation(situation=copy.deepcopy(situation(people)), tax_benefit_system=tbs)
    return (lambda v: np.asarray(sim.calculate(v, YEAR), float)), pol


def test_phase1_retiree_floor_and_current_law_tax():
    # $12,000 Social Security + $30,000 pension: provisional income $36,000.
    r, pol = run({"a": {"age": 70, "social_security_retirement": 12000, "taxable_private_pension_income": 30000}}, "v2_phase1")
    assert r("flatubi_ubi")[0] == pytest.approx(U - 12000)  # higher of benefit or UBI
    # Above $34,000: min(85% x 12,000, 85% x 2,000 + min(4,500, 6,000)) = 6,200
    assert r("flatubi_taxable_social_security")[0] == pytest.approx(6200)
    assert r("flatubi_flat_tax")[0] == pytest.approx(pol.flat_rate * (30000 + 6200))


def test_phase1_low_income_retiree_untaxed():
    r, _ = run({"a": {"age": 70, "social_security_retirement": 24000}}, "v2_phase1")
    assert r("flatubi_taxable_social_security")[0] == 0  # provisional income $12,000 < $25,000
    assert r("flatubi_ubi")[0] == 0
    assert r("social_security")[0] == pytest.approx(24000)


def test_phase1_working_adult_no_ubi_simple_eitc():
    r, pol = run({"p": {"age": 30, "employment_income": 20000}, "c1": {"age": 4}, "c2": {"age": 7}}, "v2_phase1")
    ubi = r("flatubi_ubi")
    assert ubi[0] == 0 and ubi[1] == C and ubi[2] == C
    assert r("flatubi_simple_eitc")[0] > 0  # automatic, no tax return
    assert r("flat_tax")[0] == pytest.approx(pol.flat_rate * 20000 - r("flatubi_simple_eitc")[0])


@pytest.mark.parametrize(
    "person, ubi",
    [
        ({"age": 50, "social_security_disability": 10000}, U - 10000),  # SSDI floor
        ({"age": 63, "social_security_retirement": 9000}, U - 9000),  # early retiree already receiving
    ],
)
def test_phase1_floors_under_65(person, ubi):
    r, _ = run({"a": person}, "v2_phase1")
    assert r("flatubi_ubi")[0] == pytest.approx(ubi)


def test_phase1_child_survivor_higher_of():
    r, _ = run({"g": {"age": 40}, "c": {"age": 10, "social_security_survivors": 10000}}, "v2_phase1")
    assert r("flatubi_ubi")[1] == 0  # benefit is higher than the child UBI


def test_noncitizen_without_status_gets_no_ubi():
    r, pol = run({"a": {"age": 70, "immigration_status_str": "UNDOCUMENTED"}}, "v2_phase1")
    assert r("flatubi_ubi")[0] == 0


def test_dividend_credit_and_muni_interest():
    r, pol = run({"a": {"age": 40, "qualified_dividend_income": 10000, "tax_exempt_interest_income": 5000}}, "v2_phase1")
    gross = 10000 / (1 - pol.business_rate)
    assert r("flatubi_broad_income")[0] == pytest.approx(gross)  # muni interest not in base
    # Business tax + owner tax = flat rate on the pre-tax profit, once.
    owner_tax = r("flatubi_flat_tax")[0]
    assert owner_tax + pol.business_rate * gross == pytest.approx(pol.flat_rate * gross)


def test_step3_partial_ubi_and_eitc_offset():
    r, pol = run({"p": {"age": 30, "employment_income": 20000}, "c1": {"age": 4}, "c2": {"age": 7}}, "v2_step3")
    assert r("flatubi_ubi")[0] == pytest.approx(U * 3 / 5)
    assert r("flatubi_simple_eitc")[0] == 0  # EITC about $7,300 < partial UBI $9,576


def test_step3_snap_counts_ubi():
    people = {"p": {"age": 30, "employment_income": 20000}, "c1": {"age": 4}, "c2": {"age": 7}}
    r1, _ = run(people, "v2_phase1")
    r3, _ = run(people, "v2_step3")
    assert r3("snap").sum() < r1("snap").sum()


def test_longrun_social_security_gone_except_ssdi_above_ubi():
    r, _ = run({"a": {"age": 70, "social_security_retirement": 24000}}, "v2_longrun")
    assert r("social_security")[0] == 0
    assert r("flatubi_ubi")[0] == U
    r, _ = run({"a": {"age": 50, "social_security_disability": 20000}}, "v2_longrun")
    assert r("social_security")[0] == pytest.approx(20000 - U)
    assert r("flatubi_ubi")[0] == U
