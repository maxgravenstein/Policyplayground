"""Social Security above the UBI (steady state, user decision 2026-11-13)."""

from __future__ import annotations

from policyengine_us.model_api import YEAR, USD, Person, Variable, add, max_

COMPONENTS = [
    "social_security_retirement",
    "social_security_disability",
    "social_security_survivors",
    "social_security_dependents",
]


def make_variables() -> list[type[Variable]]:
    class social_security(Variable):
        """Social Security minus the person's own UBI, not below zero.

        Each beneficiary keeps the part of today's benefit that is above the
        UBI, so Social Security + UBI = max(social_security, UBI). This covers
        retirement, disability (SSDI), survivor and dependent benefits. A child
        on survivor or dependent benefits is offset by the child UBI.

        Every program that reads `social_security` (SSI and SNAP income, state
        taxes, the flat tax base) sees the reduced amount. The four parts
        underneath keep their current-law values; only HUD rules read them,
        and housing aid is removed in the steady state.
        """

        value_type = float
        entity = Person
        definition_period = YEAR
        unit = USD
        label = "Social Security above the UBI"

        def formula(person, period, parameters):
            full = add(person, period, COMPONENTS)
            return max_(full - person("flatubi_ubi", period), 0)

    return [social_security]
