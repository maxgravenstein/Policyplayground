"""Data fixes applied to BOTH baseline and reform (not policy changes)."""

from __future__ import annotations

from policyengine_core.reforms import Reform
from policyengine_us.model_api import YEAR, SPMUnit, Variable, max_


class spm_measurement_adults(Variable):
    """Adults in the SPM unit, at least 1.

    The SPM threshold code in policyengine-us 2.107 stops with
    SPMInputError when an SPM unit has no member it classes as an adult.
    Enhanced CPS 1.115.3 has a few such units (only people under 18, with no
    household head flag). We count one member as the adult so that SPM
    poverty can be computed for every unit. This changes the threshold of
    those few units only, and it is the same in baseline and reform.
    """

    value_type = int
    entity = SPMUnit
    definition_period = YEAR
    label = "Adults under SPM measurement classification (at least 1)"

    def formula(unit, period, parameters):
        age = unit.members("age", period)
        role = unit.members("is_spm_independent_minor_role", period)
        adults = unit.sum((age >= 18) | ((age >= 15) & role))
        return max_(adults, 1)


DATA_FIX_VARIABLES = [spm_measurement_adults]


def apply_data_fixes(reform: Reform) -> None:
    for variable in DATA_FIX_VARIABLES:
        reform.update_variable(variable)


class DataFix(Reform):
    """The baseline: current law plus the data fixes above."""

    def apply(self):
        apply_data_fixes(self)
