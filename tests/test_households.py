"""Single-household tests (spec Section 5.1).

Every household lives in Texas, which has no state income tax, so the
expected values are exact.
"""

from __future__ import annotations

import numpy as np
import pytest

UBI_ADULT = 15960
UBI_CHILD = 3000
RATE = 0.3825
FEDERAL_PAYROLL = ["employee_social_security_tax", "employee_medicare_tax", "additional_medicare_tax", "self_employment_tax"]


def total(sim_fn, var):
    return float(np.sum(sim_fn(var)))


def test_single_no_income(household):
    h = household({"a": {"age": 30}})
    assert total(h.r, "household_net_income") == pytest.approx(UBI_ADULT)
    assert total(h.r, "flat_tax") == 0
    assert total(h.r, "household_tax") == 0


def test_single_wages_50k(household):
    h = household({"a": {"age": 30, "employment_income": 50_000}})
    assert total(h.r, "flat_tax") == pytest.approx(19_125)
    assert total(h.r, "household_net_income") == pytest.approx(46_835)
    for var in FEDERAL_PAYROLL + ["employee_payroll_tax"]:
        assert total(h.r, var) == 0, var
    assert total(h.r, "income_tax") == 0
    # Baseline does charge payroll tax.
    assert total(h.b, "employee_payroll_tax") > 0


def test_capital_gains_taxed_like_wages(household):
    wages = household({"a": {"age": 30, "employment_income": 50_000}})
    gains = household({"a": {"age": 30, "long_term_capital_gains": 50_000}})
    assert total(gains.r, "flat_tax") == pytest.approx(total(wages.r, "flat_tax"))
    assert total(gains.r, "flat_tax") == pytest.approx(19_125)
    # Current law taxes the two differently.
    assert total(gains.b, "income_tax") != pytest.approx(total(wages.b, "income_tax"))


def test_couple_individual_filing(household):
    h = household({"a": {"age": 40, "employment_income": 100_000}, "b": {"age": 40}})
    assert total(h.r, "basic_income") == pytest.approx(2 * UBI_ADULT)
    tax = h.r("flatubi_flat_tax")
    assert float(tax[0]) == pytest.approx(38_250)
    assert float(tax[1]) == 0
    assert total(h.r, "flat_tax") == pytest.approx(38_250)
    assert total(h.r, "household_net_income") == pytest.approx(100_000 - 38_250 + 2 * UBI_ADULT)


def test_single_parent_two_children(household):
    h = household(
        {
            "p": {"age": 25, "employment_income": 20_000},
            "c1": {"age": 4},
            "c2": {"age": 7},
        }
    )
    assert total(h.r, "basic_income") == pytest.approx(UBI_ADULT + 2 * UBI_CHILD)
    # No EITC and no CTC reach the family in the reform.
    assert total(h.r, "income_tax_refundable_credits_in_force") == 0
    assert total(h.r, "household_refundable_tax_credits") == 0
    assert total(h.r, "income_tax") == 0
    # They had both under current law.
    assert total(h.b, "eitc") > 0
    assert total(h.b, "refundable_ctc") > 0
    assert total(h.r, "flat_tax") == pytest.approx(RATE * 20_000)


def test_retiree_steady_state(household):
    h = household({"a": {"age": 70, "social_security_retirement": 24_000}})
    assert total(h.b, "social_security") == pytest.approx(24_000)
    assert total(h.r, "social_security") == 0
    assert total(h.r, "basic_income") == pytest.approx(UBI_ADULT)
    assert total(h.r, "flat_tax") == 0  # UBI is not taxable
    # Medicare kept.
    assert total(h.r, "medicare_cost") == pytest.approx(total(h.b, "medicare_cost"))
    assert total(h.r, "medicare_cost") > 0


@pytest.mark.parametrize("ss, expected", [(24_000, 24_000), (12_000, UBI_ADULT)])
def test_retiree_phase1_offset(household, ss, expected):
    h = household({"a": {"age": 70, "social_security_retirement": ss}}, system="phase1")
    received = total(h.r, "social_security") + total(h.r, "flatubi_ubi")
    assert received == pytest.approx(expected)
    assert total(h.r, "social_security") == pytest.approx(ss)  # offset, not cut


def test_phase1_working_age_no_ubi(household):
    h = household({"a": {"age": 40, "employment_income": 30_000}, "c": {"age": 5}}, system="phase1")
    ubi = h.r("flatubi_ubi")
    assert float(ubi[0]) == 0
    assert float(ubi[1]) == pytest.approx(UBI_CHILD)


def test_ssi_adult_keeps_ssi(household):
    h = household({"a": {"age": 40, "is_disabled": True, "meets_ssi_disability_criteria": True}})
    ssi_base = total(h.b, "ssi")
    assert ssi_base > 0
    assert total(h.r, "ssi") == pytest.approx(ssi_base)  # UBI not counted
    assert total(h.r, "basic_income") == pytest.approx(UBI_ADULT)
    assert total(h.r, "household_net_income") == pytest.approx(ssi_base + UBI_ADULT)


def test_ssi_counts_ubi_switch(household):
    """With ubi.counts_as_ssi_income, SSI treats the UBI as unearned income."""
    h = household({"a": {"age": 40, "is_disabled": True, "meets_ssi_disability_criteria": True}}, system="steady_state:ssi_counts")
    # $15,960 a year is above the federal SSI rate, so SSI goes to zero.
    assert total(h.r, "ssi") == 0
    assert total(h.r, "basic_income") == pytest.approx(UBI_ADULT)


def test_zero_rate_zero_ubi_equals_baseline_minus_removed(household):
    """Spec 5.3, one household: with flat_rate = 0 and UBI = 0, the reform is
    the baseline minus the removed programs and taxes."""
    h = household(
        {
            "p": {"age": 30, "employment_income": 22_000, "unemployment_compensation": 3_000},
            "c": {"age": 3},
        },
        system="steady_state:zero",
    )
    removed_benefits = ["snap", "tanf", "wic", "housing_assistance", "unemployment_compensation", "social_security"]
    expected = (
        total(h.b, "household_net_income")
        + total(h.b, "income_tax")
        + sum(total(h.b, v) for v in FEDERAL_PAYROLL)
        - sum(total(h.b, v) for v in removed_benefits)
    )
    assert total(h.r, "household_net_income") == pytest.approx(expected, abs=1)


def test_employer_payroll_passthrough_switch(household):
    """Optional: employer payroll tax paid out as wages and taxed (not in the spec)."""
    h = household({"a": {"age": 30, "employment_income": 50_000}}, system="steady_state:passthrough")
    employer = total(h.b, "employer_social_security_tax") + total(h.b, "employer_medicare_tax")
    assert employer == pytest.approx(0.0765 * 50_000)
    assert total(h.r, "flat_tax") == pytest.approx(RATE * (50_000 + employer))
    assert total(h.r, "household_net_income") == pytest.approx((50_000 + employer) * (1 - RATE) + UBI_ADULT)
