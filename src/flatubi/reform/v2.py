"""Spec v2 reform (docs/SPEC_v2.md) for one stage: phase 1, a phase 2 step, or the long run.

Each variable names the spec section it implements.
"""

from __future__ import annotations

import numpy as np
from policyengine_core.periods import instant
from policyengine_core.reforms import Reform
from policyengine_us.model_api import (
    YEAR,
    USD,
    Person,
    TaxUnit,
    Variable,
    add,
    max_,
    min_,
    where,
)

from flatubi.config_v2 import PolicyV2
from flatubi.reform.datafix import apply_data_fixes

SS_PARTS = [
    "social_security_retirement",
    "social_security_disability",
    "social_security_survivors",
    "social_security_dependents",
]
FEDERAL_PAYROLL = [
    "employee_social_security_tax",
    "employee_medicare_tax",
    "additional_medicare_tax",
    "self_employment_tax",
]
# Spec 4.2: interest on state and local bonds stays untaxed; already-taxed
# retirement money (Roth, basis) is not taxed again (taxed once).
NOT_IN_BASE = [
    "tax_exempt_interest_income",
    "tax_exempt_retirement_distributions",
    "tax_exempt_pension_income",
]
REMOVED_PROGRAM_VARIABLES = {
    "snap": ["snap"],
    "tanf": ["tanf"],
    "wic": ["wic"],
    "housing": ["housing_assistance", "spm_unit_capped_housing_subsidy"],
}
# Spec 9.2: programs that count the UBI as income (not SSI, not Medicaid),
# with the UBI variable each one counts (spec v3: programs that end at step 5
# count the working-age part only; continuing programs phase in the rest).
COUNT_UBI_LISTS = {
    "gov.usda.snap.income.sources.unearned": "flatubi_ubi_counted_end",
    "gov.usda.wic.income.sources": "flatubi_ubi_counted_end",
    "gov.usda.school_meals.income.sources": "flatubi_ubi_counted_cont",
    "gov.hud.annual_income.sources.unearned": "flatubi_ubi_counted_cont",
}
# 2026 employer share of premiums, used to impute where the data has none
# (Populace). Rough, from the KFF 2025 employer survey, uprated one year.
EMPLOYER_PREMIUM_SINGLE = 8_400.0


def build_reform_v2(p: PolicyV2) -> type[Reform]:
    U, C, P = p.ubi_adult, p.ubi_child, p.working_age_ubi
    adult_age, senior_age = p.min_age_adult, p.senior_age
    full_ubi_all_adults = p.longrun or P >= U
    br = p.business_rate
    t1, t2 = p.ss_thresholds
    impute_health = bool(p.raw.get("tax", {}).get("impute_employer_health", True))
    # Scale so that the imputed national total matches the $1.24T 2026 total
    # in the Enhanced CPS (about the national-accounts figure).
    impute_scale = float(p.raw.get("tax", {}).get("employer_health_impute_scale", 1.0))
    single_premium = EMPLOYER_PREMIUM_SINGLE * impute_scale
    family_premium = single_premium * p.employer_health_ratio

    class flatubi_ubi_eligible(Variable):
        """Spec 3: citizens and qualified residents. The 5-year wait for
        permanent residents is not in the data."""

        value_type = bool
        entity = Person
        definition_period = YEAR
        label = "Eligible for the UBI"

        def formula(person, period, parameters):
            status = person("immigration_status", period).decode_to_str()
            return np.isin(status, p.eligible_statuses)

    class flatubi_ss_full(Variable):
        """Today's Social Security benefit (all four parts)."""

        value_type = float
        entity = Person
        definition_period = YEAR
        unit = USD
        label = "Social Security before the reform"

        def formula(person, period, parameters):
            return add(person, period, SS_PARTS)

    class flatubi_ubi(Variable):
        """UBI paid to one person (spec 3 and 5.1).

        Children: child amount. Adults 65+: full amount. Adults 18-64: the
        partial phase 2 amount (zero in phase 1, full at the end).
        Floor (phase 1 to the end of the schedule): anyone with Social
        Security gets the higher of the benefit or their full UBI, so the UBI
        is cut by the benefit. In the long run Social Security is gone except
        SSDI above the UBI, so the UBI is not cut.
        """

        value_type = float
        entity = Person
        definition_period = YEAR
        unit = USD
        label = "UBI payment"

        def formula(person, period, parameters):
            age = person("age", period)
            eligible = person("flatubi_ubi_eligible", period)
            is_adult = age >= adult_age
            full = where(is_adult, U, C)
            if full_ubi_all_adults:
                amount = full
            else:
                amount = where(is_adult, where(age >= senior_age, U, P), C)
            if p.ss_rule == "floor":
                ss = person("flatubi_ss_full", period)
                amount = where(ss > 0, max_(full - ss, 0), amount)
            return eligible * amount

    class basic_income(Variable):
        """Tax-unit total of flatubi_ubi (enters net income and SPM resources)."""

        value_type = float
        entity = TaxUnit
        definition_period = YEAR
        unit = USD
        label = "basic income"

        def formula(tax_unit, period, parameters):
            return add(tax_unit, period, ["flatubi_ubi"])

    class flatubi_ubi_working(Variable):
        """Spec v3 9.2: the working-age part of the UBI: the partial (or full)
        UBI of adults 18-64 who get it as working-age adults, not as a
        Social Security floor."""

        value_type = float
        entity = Person
        definition_period = YEAR
        unit = USD
        label = "Working-age part of the UBI"

        def formula(person, period, parameters):
            age = person("age", period)
            working = (age >= adult_age) & (age < senior_age)
            if p.ss_rule == "floor":
                working = working & (person("flatubi_ss_full", period) <= 0)
            return working * person("flatubi_ubi", period)

    class flatubi_ubi_counted_end(Variable):
        """UBI counted by programs that end at step 5 (SNAP, WIC).
        v2: all UBI. v3: only the working-age part."""

        value_type = float
        entity = Person
        definition_period = YEAR
        unit = USD
        label = "UBI counted by SNAP and WIC"

        def formula(person, period, parameters):
            if p.count_split:
                return person("flatubi_ubi_working", period)
            return person("flatubi_ubi", period)

    class flatubi_ubi_counted_cont(Variable):
        """UBI counted by programs that continue (school meals, housing, ACA).
        v2: all UBI. v3: the working-age part plus count_share (20% per step)
        of the child and senior UBI."""

        value_type = float
        entity = Person
        definition_period = YEAR
        unit = USD
        label = "UBI counted by continuing programs"

        def formula(person, period, parameters):
            ubi = person("flatubi_ubi", period)
            if not p.count_split:
                return ubi
            working = person("flatubi_ubi_working", period)
            return working + p.count_share * (ubi - working)

    class flatubi_payroll_passthrough(Variable):
        """Employer payroll tax paid out as wages (incidence assumption).

        The reform ends the employer Social Security and Medicare tax. CBO,
        JCT and Treasury assume workers bear that tax through lower pay, so
        the saving goes to each worker as higher wages: today's employer tax
        on the worker's wages before the change. Config:
        tax.employer_payroll_to_wages (default true)."""

        value_type = float
        entity = Person
        definition_period = YEAR
        unit = USD
        label = "Employer payroll tax paid out as wages"

        def formula(person, period, parameters):
            if not p.payroll_to_wages:
                return 0 * person("age", period)
            wages = person("employment_income_before_lsr", period) + person(
                "employment_income_behavioral_response", period
            )
            gross = max_(0, wages - person("fica_pre_tax_contributions", period))
            pay = parameters(period).gov.irs.payroll
            return pay.social_security.rate.employer * min_(pay.social_security.cap, gross) + (
                pay.medicare.rate.employer * gross
            )

    class employment_income(Variable):
        """Wages including the employer payroll tax paid out as wages."""

        value_type = float
        entity = Person
        definition_period = YEAR
        unit = USD
        label = "employment income"

        def formula(person, period, parameters):
            return add(
                person,
                period,
                [
                    "employment_income_before_lsr",
                    "employment_income_behavioral_response",
                    "flatubi_payroll_passthrough",
                ],
            )

    class flatubi_earnings_exemption(Variable):
        """Spec v3 4.7: transitional earnings exemption, ages 18-64: wages and
        net self-employment earnings up to the stage's exemption amount."""

        value_type = float
        entity = Person
        definition_period = YEAR
        unit = USD
        label = "Transitional earnings exemption"

        def formula(person, period, parameters):
            age = person("age", period)
            if p.earnings_exemption <= 0:
                return 0 * age
            earnings = person("employment_income", period) + max_(
                person("self_employment_income", period) + person("sstb_self_employment_income", period), 0
            )
            working = (age >= adult_age) & (age < senior_age)
            return working * min_(max_(earnings, 0), p.earnings_exemption)

    class flatubi_employer_health(Variable):
        """Spec 4.2: employer health premiums in the base, phased in by step.

        Populace has no premiums: workers with employer coverage get the
        average employer share (single, or family if their tax unit has
        more than one person)."""

        value_type = float
        entity = Person
        definition_period = YEAR
        unit = USD
        label = "Employer health premiums in the flat tax base"

        def formula(person, period, parameters):
            data = person("employer_sponsored_insurance_premiums", period)
            if impute_health:
                holder = person("has_esi", period) & (person("employment_income", period) > 0)
                size = person.tax_unit.nb_persons()
                imputed = holder * where(size > 1, family_premium, single_premium)
                data = where(data > 0, data, imputed)
            return p.employer_health_share * data

    class total_unemployment_compensation(Variable):
        """Spec 7.4: at the end of the schedule, unemployment becomes a short
        top-up (about half of today's benefit, rough)."""

        value_type = float
        entity = Person
        definition_period = YEAR
        unit = USD
        label = "total unemployment compensation"

        def formula(person, period, parameters):
            reported = person("unemployment_compensation", period)
            modeled = person("modeled_state_unemployment_compensation", period)
            return p.ui_factor * where(reported != 0, reported, modeled)

    class flatubi_dividend_credit(Variable):
        """Spec 8.1: owner credit for the 21% business tax on dividends.
        Qualified dividends stand for dividends from taxed U.S. companies."""

        value_type = float
        entity = Person
        definition_period = YEAR
        unit = USD
        label = "Credit for business tax on dividends"

        def formula(person, period, parameters):
            return person("qualified_dividend_income", period) * br / (1 - br)

    class flatubi_base_ex_ss(Variable):
        """Spec 4.2: the flat tax base without Social Security.

        Market income, minus tax-exempt bond interest and already-taxed
        retirement money, plus dividends grossed up for the business tax,
        employer health premiums (phased in) and unemployment benefits."""

        value_type = float
        entity = Person
        definition_period = YEAR
        unit = USD
        label = "Flat tax base before Social Security"

        def formula(person, period, parameters):
            sources = list(parameters(period).gov.household.market_income_sources)
            base = add(person, period, sources) - add(person, period, NOT_IN_BASE)
            base = base + person("flatubi_dividend_credit", period)  # gross-up
            base = base + person("flatubi_employer_health", period)
            base = base + person("total_unemployment_compensation", period)
            return base

    class flatubi_taxable_social_security(Variable):
        """Spec 5.3: taxable part of Social Security, current-law rule, per person."""

        value_type = float
        entity = Person
        definition_period = YEAR
        unit = USD
        label = "Taxable Social Security (per person)"

        def formula(person, period, parameters):
            ss = person("social_security", period)
            other = person("flatubi_base_ex_ss", period)
            pi = other + 0.5 * ss
            tier1 = min_(0.5 * ss, 0.5 * max_(pi - t1, 0))
            tier2 = min_(0.85 * ss, 0.85 * max_(pi - t2, 0) + min_(0.5 * (t2 - t1), 0.5 * ss))
            return where(pi > t2, tier2, tier1)

    class flatubi_broad_income(Variable):
        """Spec 4.2: the full flat tax base for one person."""

        value_type = float
        entity = Person
        definition_period = YEAR
        unit = USD
        label = "Flat tax base"

        def formula(person, period, parameters):
            return (
                person("flatubi_base_ex_ss", period)
                + person("flatubi_taxable_social_security", period)
                - person("flatubi_earnings_exemption", period)
            )

    class flatubi_flat_tax(Variable):
        """Spec 4.1: flat rate on the person's base, minus the dividend credit
        (refundable). Net losses give no tax (carry-forward is not modeled)."""

        value_type = float
        entity = Person
        definition_period = YEAR
        unit = USD
        label = "Flat tax (person)"

        def formula(person, period, parameters):
            base = person("flatubi_broad_income", period)
            return p.flat_rate * max_(base, 0) - person("flatubi_dividend_credit", period)

    class flatubi_simple_eitc(Variable):
        """Spec 6: simple automatic EITC (phase 1); in phase 2 the higher of
        the EITC or the partial UBI of the working-age adults; then gone."""

        value_type = float
        entity = TaxUnit
        definition_period = YEAR
        unit = USD
        label = "Simple automatic EITC"

        def formula(tax_unit, period, parameters):
            if p.eitc_rule == "none":
                return 0 * tax_unit("eitc_maximum", period)
            eligible = tax_unit("eitc_eligible", period)
            amount = min_(
                tax_unit("eitc_phased_in", period),
                max_(0, tax_unit("eitc_maximum", period) - tax_unit("eitc_reduction", period)),
            )
            amount = eligible * amount
            if p.eitc_rule == "offset":
                person = tax_unit.members
                if p.count_split:
                    # v3: reduced by half of the adults' working-age UBI.
                    partial = tax_unit.sum(person("flatubi_ubi_working", period))
                else:
                    age = person("age", period)
                    working = (age >= adult_age) & (age < senior_age)
                    partial = tax_unit.sum(person("flatubi_ubi", period) * working)
                amount = max_(amount - p.eitc_offset_share * partial, 0)
            return amount

    class flat_tax(Variable):
        """Tax unit: flat tax of all members minus the simple EITC. Enters
        household net income and SPM resources."""

        value_type = float
        entity = TaxUnit
        definition_period = YEAR
        unit = USD
        label = "Flat tax"

        def formula(tax_unit, period, parameters):
            return add(tax_unit, period, ["flatubi_flat_tax"]) - tax_unit("flatubi_simple_eitc", period)

    variables = [
        flatubi_ubi_eligible,
        flatubi_ss_full,
        flatubi_ubi,
        basic_income,
        flatubi_ubi_working,
        flatubi_ubi_counted_end,
        flatubi_ubi_counted_cont,
        flatubi_earnings_exemption,
        flatubi_employer_health,
        total_unemployment_compensation,
        flatubi_dividend_credit,
        flatubi_base_ex_ss,
        flatubi_taxable_social_security,
        flatubi_broad_income,
        flatubi_flat_tax,
        flatubi_simple_eitc,
        flat_tax,
        flatubi_payroll_passthrough,
    ]
    if p.payroll_to_wages:
        variables.append(employment_income)

    if p.programs_count_ubi:

        class aca_magi(Variable):
            """Spec 9.2: ACA credits count the UBI (Medicaid does not)."""

            value_type = float
            entity = TaxUnit
            definition_period = YEAR
            unit = USD
            label = "ACA-related modified AGI for this tax unit"

            def formula(tax_unit, period, parameters):
                return tax_unit("medicaid_magi", period) + add(tax_unit, period, ["flatubi_ubi_counted_cont"])

        variables.append(aca_magi)

    if p.ss_rule == "ssdi_only":

        class social_security(Variable):
            """Spec 7.1 long run: only SSDI above the UBI remains. Retirement,
            survivor and dependent benefits are gone."""

            value_type = float
            entity = Person
            definition_period = YEAR
            unit = USD
            label = "Social Security (SSDI above the UBI)"

            def formula(person, period, parameters):
                ssdi = person("social_security_disability", period)
                return max_(ssdi - person("flatubi_ubi", period), 0)

        variables.append(social_security)

    neutralize = list(FEDERAL_PAYROLL)
    for program in p.programs_removed:
        neutralize += REMOVED_PROGRAM_VARIABLES[program]

    start = instant(f"{p.year - 1}-01-01")
    stop = instant(f"{p.year + 1}-12-31")

    def modify(parameters):
        parameters.get_child("gov.contrib.ubi_center.flat_tax.abolish_federal_income_tax").update(
            start=start, stop=stop, value=True
        )
        if p.removes("housing"):
            parameters.get_child("gov.hud.abolition").update(start=start, stop=stop, value=True)
        parameters.get_child("gov.ssa.ssi.eligibility.resources.limit.individual").update(
            start=start, stop=stop, value=p.ssi_limits[0]
        )
        parameters.get_child("gov.ssa.ssi.eligibility.resources.limit.couple").update(
            start=start, stop=stop, value=p.ssi_limits[1]
        )
        if p.programs_count_ubi:
            for path, var in COUNT_UBI_LISTS.items():
                node = parameters.get_child(path)
                sources = list(node(f"{p.year}-01-01"))
                if var not in sources:
                    node.update(start=start, stop=stop, value=sources + [var])
        return parameters

    class FlatTaxUBIv2(Reform):
        def apply(self):
            apply_data_fixes(self)
            for variable in variables:
                if variable.__name__ in self.variables:
                    self.update_variable(variable)
                else:
                    self.add_variable(variable)
            for name in neutralize:
                self.neutralize_variable(name)
            self.modify_parameters(modify)

    FlatTaxUBIv2.__name__ = f"FlatTaxUBIv2_{p.scenario}"
    return FlatTaxUBIv2
