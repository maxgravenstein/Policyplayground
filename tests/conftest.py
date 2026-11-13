"""Shared helpers for the tests.

Building a PolicyEngine tax-benefit system takes about a minute, so each
system is built once per test session and reused for every household.
"""

from __future__ import annotations

import copy
from functools import lru_cache
from pathlib import Path

import pytest

from flatubi.config import load_config, resolve

YEAR = 2026
ROOT = Path(__file__).resolve().parents[1]


def base_config() -> dict:
    return load_config(ROOT / "config.yaml")


@lru_cache(maxsize=None)
def _system(key: str):
    from policyengine_us import CountryTaxBenefitSystem

    from flatubi.reform import build_reform

    if key == "baseline":
        from flatubi.reform.datafix import DataFix

        return DataFix(CountryTaxBenefitSystem())
    scenario, _, variant = key.partition(":")
    cfg = base_config()
    if variant == "zero":
        cfg["tax"]["flat_rate"] = 0.0
        cfg["ubi"]["adult_annual"] = 0
        cfg["ubi"]["child_annual"] = 0
    if variant == "passthrough":
        cfg["tax"]["employer_payroll_to_wages"] = True
    if variant == "no_ss":
        cfg.setdefault("steady_state", {})["social_security_residual"] = False
    if variant == "ssi_counts":
        cfg["ubi"]["counts_as_ssi_income"] = True
    return build_reform(resolve(cfg, scenario))(CountryTaxBenefitSystem())


def situation(people: dict, state: str = "TX") -> dict:
    """One household = one tax unit = one SPM unit. Couples are married."""
    names = list(people)
    adults = [n for n in names if people[n]["age"] >= 18]
    return {
        "people": {n: {k: {YEAR: v} for k, v in p.items()} for n, p in people.items()},
        "tax_units": {"tu": {"members": names}},
        "spm_units": {"spm": {"members": names}},
        "families": {"fam": {"members": names}},
        "marital_units": {f"mu_{n}": {"members": [n]} for n in names if n not in adults[:2]}
        | ({"mu": {"members": adults[:2]}} if adults else {}),
        "households": {"hh": {"members": names, "state_name": {YEAR: state}}},
    }


class Household:
    """Run one household under baseline and a reform system."""

    def __init__(self, people: dict, system: str = "steady_state", state: str = "TX"):
        from policyengine_us import Simulation

        sit = situation(people, state)
        self.base = Simulation(situation=copy.deepcopy(sit), tax_benefit_system=_system("baseline"))
        self.ref = Simulation(situation=copy.deepcopy(sit), tax_benefit_system=_system(system))

    def b(self, var):
        return self.base.calculate(var, YEAR)

    def r(self, var):
        return self.ref.calculate(var, YEAR)


@pytest.fixture
def household():
    return Household
