"""Universal basic income (spec Section 2.1, and the age limit of 2.5 phase1)."""

from __future__ import annotations

from policyengine_us.model_api import (
    YEAR,
    USD,
    Person,
    TaxUnit,
    Variable,
    add,
    where,
)

from flatubi.config import Policy
from flatubi.reform import phase1


def make_variables(policy: Policy) -> list[type[Variable]]:
    adult_amount = policy.ubi_adult
    child_amount = policy.ubi_child
    adult_age = policy.min_age_adult
    min_age = policy.ubi_min_age

    class flatubi_ubi(Variable):
        """UBI paid to one person.

        Spec 2.1: each adult (age >= min_age_adult) gets ubi.adult_annual and
        each child gets ubi.child_annual. No phase-out. Not taxable.
        Spec 2.5 phase1: adults get the UBI only at age >= phase1_min_age, and
        the Social Security offset applies (see reform/phase1.py).
        """

        value_type = float
        entity = Person
        definition_period = YEAR
        unit = USD
        label = "Flat-tax UBI payment"

        def formula(person, period, parameters):
            age = person("age", period)
            is_adult = age >= adult_age
            adult_eligible = is_adult if min_age is None else age >= min_age
            amount = where(
                is_adult,
                where(adult_eligible, adult_amount, 0.0),
                child_amount,
            )
            if policy.social_security_offset:
                amount = phase1.offset_ubi(person, period, amount, is_adult & adult_eligible)
            return amount

    class basic_income(Variable):
        """Tax-unit total of flatubi_ubi.

        PolicyEngine already counts `basic_income` in household benefits and
        SPM resources, and leaves it out of AGI and of SNAP, SSI and Medicaid
        income while gov.contrib.ubi_center.basic_income.taxable is false.
        Spec 2.1: the UBI is not taxable income.
        """

        value_type = float
        entity = TaxUnit
        definition_period = YEAR
        unit = USD
        label = "basic income"

        def formula(tax_unit, period, parameters):
            return add(tax_unit, period, ["flatubi_ubi"])

    return [flatubi_ubi, basic_income]
