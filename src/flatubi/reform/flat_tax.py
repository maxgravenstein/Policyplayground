"""Flat income tax on a broad base (spec Section 2.2)."""

from __future__ import annotations

from policyengine_us.model_api import (
    YEAR,
    USD,
    Household,
    Person,
    TaxUnit,
    Variable,
    add,
    max_,
)

from flatubi.config import Policy
from flatubi.reform.credits import ctc_against_tax

# Taxes that the flat tax replaces. Set to true in the reform.
ABOLISH_PARAMETERS = [
    # Spec 2.2: standard and itemized deductions, all credits (EITC, CTC,
    # CDCC, education, saver's), the capital gains rate, the AMT and the NIIT
    # all live inside the federal income tax. Abolish it as a whole.
    "gov.contrib.ubi_center.flat_tax.abolish_federal_income_tax",
]
# Spec 2.2: federal payroll taxes go to zero. We zero the federal parts one
# by one, not the whole employee_payroll_tax, so that state payroll taxes
# (such as California SDI) stay at current law. Employer taxes are not in
# household net income; the budget table counts them as zero in the reform.
PAYROLL_VARIABLES = [
    "employee_social_security_tax",
    "employee_medicare_tax",
    "additional_medicare_tax",
    "self_employment_tax",
]

# Income that is in the base but not in PolicyEngine's market income.
EXTRA_SOURCES = [
    "unemployment_compensation",  # zero when unemployment is removed
    "social_security",  # spec 2.2: legacy benefits, phase1 only (else zero)
]
EMPLOYER_HEALTH = "employer_sponsored_insurance_premiums"
RETIREMENT_CONTRIBUTIONS = [
    "traditional_401k_contributions",
    "traditional_ira_contributions",
    "self_employed_pension_contributions",
]
EMPLOYER_PAYROLL = ["employer_social_security_tax", "employer_medicare_tax"]


def make_variables(policy: Policy) -> list[type[Variable]]:
    rate = policy.flat_rate
    individual = policy.individual_filing

    class flatubi_payroll_passthrough(Variable):
        """Employer payroll tax paid out as wages (optional, not in the spec).

        If tax.employer_payroll_to_wages is true, the employer Social
        Security and Medicare tax that the reform removes goes to the worker
        as extra pay. That pay is in the flat tax base and in market income.
        """

        value_type = float
        entity = Person
        definition_period = YEAR
        unit = USD
        label = "Employer payroll tax paid out as wages"

        def formula(person, period, parameters):
            if not (policy.employer_payroll_to_wages and policy.remove_payroll_tax):
                return 0 * person("age", period)
            return add(person, period, EMPLOYER_PAYROLL)

    class flatubi_broad_income(Variable):
        """The flat tax base for one person (spec 2.2, "No carve outs").

        = all PolicyEngine market income (gov.household.market_income_sources:
          wages before pre-tax deductions, self-employment, partnership and S
          corp, farm, rent, all interest including tax-exempt, all dividends,
          all capital gains at the wage rate, pensions, IRA and 401(k)
          distributions, alimony, estate, and other income)
        + unemployment compensation (if kept) and Social Security (phase1)
        + employer health insurance premiums (if include_employer_health)
        + employer payroll tax paid out as wages (optional)
        - pre-tax retirement contributions (only if they are not in the base)

        Wages are gross of 401(k) deferrals, so employee contributions are
        taxed when earned. The data have no employer retirement contributions.
        """

        value_type = float
        entity = Person
        definition_period = YEAR
        unit = USD
        label = "Flat tax base (broad income)"

        def formula(person, period, parameters):
            sources = list(parameters(period).gov.household.market_income_sources)
            income = add(person, period, sources + EXTRA_SOURCES)
            if policy.include_employer_health:
                income = income + person(EMPLOYER_HEALTH, period)
            if not policy.include_retirement_contributions:
                income = income - add(person, period, RETIREMENT_CONTRIBUTIONS)
            income = income + person("flatubi_payroll_passthrough", period)
            return income

    class flatubi_flat_tax(Variable):
        """Flat tax owed by one person (spec 2.2).

        One rate, tax.flat_rate, on that person's own broad income, with no
        brackets, deductions or credits. Net losses give zero tax, not a
        refund. With individual_filing false, the tax unit pools income and
        each member gets a share of the tax in proportion to positive income.
        """

        value_type = float
        entity = Person
        definition_period = YEAR
        unit = USD
        label = "Flat tax (person)"

        def formula(person, period, parameters):
            income = person("flatubi_broad_income", period)
            if individual:
                return rate * max_(income, 0)
            unit_income = person.tax_unit.sum(income)
            unit_positive = person.tax_unit.sum(max_(income, 0))
            share = max_(income, 0) / max_(person.tax_unit.project(unit_positive), 1e-9)
            return rate * max_(person.tax_unit.project(unit_income), 0) * share

    keep_eitc = "eitc" in policy.kept_credits
    keep_ctc = "ctc" in policy.kept_credits

    class flatubi_flat_tax_gross(Variable):
        """Tax-unit total of flatubi_flat_tax, before any credit."""

        value_type = float
        entity = TaxUnit
        definition_period = YEAR
        unit = USD
        label = "Flat tax before credits"

        def formula(tax_unit, period, parameters):
            return add(tax_unit, period, ["flatubi_flat_tax"])

    class flatubi_eitc(Variable):
        """Federal EITC kept against the flat tax (phase 1, user decision).

        Spec 2.5 phase1: working-age adults keep current programs. The EITC is
        kept at its current-law amount (same AGI, phase-in and phase-out) and
        is fully refundable, as today. Zero when `eitc` is removed.
        """

        value_type = float
        entity = TaxUnit
        definition_period = YEAR
        unit = USD
        label = "EITC kept against the flat tax"

        def formula(tax_unit, period, parameters):
            eitc = tax_unit("eitc", period)
            return eitc if keep_eitc else 0 * eitc

    class flatubi_ctc(Variable):
        """Federal CTC kept against the flat tax (phase 1, user decision).

        Current-law CTC amount and phase-out. The non-refundable part reduces
        the flat tax (not the abolished income tax), and the refundable part
        follows the current ACTC rule. See reform/credits.py.
        """

        value_type = float
        entity = TaxUnit
        definition_period = YEAR
        unit = USD
        label = "CTC kept against the flat tax"

        def formula(tax_unit, period, parameters):
            ctc = tax_unit("ctc", period)
            if not keep_ctc:
                return 0 * ctc
            return ctc_against_tax(
                ctc,
                tax_unit("ctc_refundable_maximum", period),
                tax_unit("ctc_phase_in", period),
                tax_unit("flatubi_flat_tax_gross", period),
            )

    class flat_tax(Variable):
        """Flat tax of the tax unit after kept credits (can be below zero).

        = flatubi_flat_tax_gross - flatubi_eitc - flatubi_ctc. Without kept
        credits this is the plain sum of flatubi_flat_tax. PolicyEngine
        subtracts `flat_tax` in household net income and in SPM resources, so
        the flat tax and the credits reach poverty and net income results.
        """

        value_type = float
        entity = TaxUnit
        definition_period = YEAR
        unit = USD
        label = "Flat tax"

        def formula(tax_unit, period, parameters):
            gross = tax_unit("flatubi_flat_tax_gross", period)
            return gross - tax_unit("flatubi_eitc", period) - tax_unit("flatubi_ctc", period)

    variables = [
        flatubi_payroll_passthrough,
        flatubi_broad_income,
        flatubi_flat_tax,
        flatubi_flat_tax_gross,
        flatubi_eitc,
        flatubi_ctc,
        flat_tax,
    ]

    if policy.employer_payroll_to_wages and policy.remove_payroll_tax:

        class household_market_income(Variable):
            """Market income plus employer payroll tax paid out as wages."""

            value_type = float
            entity = Household
            definition_period = YEAR
            unit = USD
            label = "market income"

            def formula(household, period, parameters):
                sources = list(parameters(period).gov.household.market_income_sources)
                return add(household, period, sources + ["flatubi_payroll_passthrough"])

        variables.append(household_market_income)

    return variables


def parameter_switches(policy: Policy) -> list[str]:
    return list(ABOLISH_PARAMETERS)


def payroll_variables(policy: Policy) -> list[str]:
    return list(PAYROLL_VARIABLES) if policy.remove_payroll_tax else []
