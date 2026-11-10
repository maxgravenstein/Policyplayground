"""Programs removed or kept (spec Sections 2.3 and 2.4)."""

from __future__ import annotations

from flatubi.config import ALL_KEEPABLE, Policy

# PolicyEngine variables set to zero for each program name in the config.
REMOVED_PROGRAM_VARIABLES = {
    "snap": ["snap"],
    "tanf": ["tanf"],
    "wic": ["wic"],
    "housing": ["housing_assistance", "spm_unit_capped_housing_subsidy"],
    # Federal EITC and CTC go with the federal income tax (spec 2.2). State
    # credits that copy the federal EITC still use the federal formula, so
    # we do not set the `eitc` or `ctc` variables to zero.
    "eitc": [],
    "ctc": [],
    "aca_ptc": ["aca_ptc"],
    "unemployment": ["unemployment_compensation"],
    "social_security": [
        "social_security_retirement",
        "social_security_disability",
        "social_security_survivors",
        "social_security_dependents",
    ],
}

# Spec 2.4: kept at current law. If a name is left out of programs_kept, the
# program is set to zero too (the school meals switch the spec asks for).
KEPT_PROGRAM_VARIABLES = {
    "medicaid": ["medicaid"],
    "chip": ["chip"],
    "ssi": ["ssi"],
    "medicare": ["medicare_cost"],
    "school_meals": ["free_school_meals", "reduced_price_school_meals"],
}


def variables_to_neutralize(policy: Policy) -> list[str]:
    names: list[str] = []
    for program in policy.programs_removed:
        names += REMOVED_PROGRAM_VARIABLES[program]
    for program in ALL_KEEPABLE:
        if program not in policy.programs_kept:
            names += KEPT_PROGRAM_VARIABLES[program]
    return names
