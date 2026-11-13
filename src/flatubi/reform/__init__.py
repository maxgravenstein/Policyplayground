"""Build one PolicyEngine Reform class from a resolved Policy.

The pieces are applied in the build order of spec Section 10: UBI, program
removal, payroll tax removal, flat tax on the broad base, individual filing.
"""

from __future__ import annotations

from policyengine_core.periods import instant
from policyengine_core.reforms import Reform

from flatubi.config import Policy


def build_reform(policy: Policy) -> type[Reform]:
    # Imported here so that `flatubi.reform.phase1` can be imported by ubi.py.
    from flatubi.reform import flat_tax, programs, ubi
    from flatubi.reform.datafix import apply_data_fixes

    new_variables = ubi.make_variables(policy) + flat_tax.make_variables(policy)
    if policy.social_security_residual:
        from flatubi.reform import social_security

        new_variables += social_security.make_variables()
    neutralized = programs.variables_to_neutralize(policy) + flat_tax.payroll_variables(policy)
    switches = flat_tax.parameter_switches(policy)
    start = instant(f"{policy.year - 1}-01-01")
    stop = instant(f"{policy.year + 1}-12-31")

    def modify(parameters):
        for path in switches:
            parameters.get_child(path).update(start=start, stop=stop, value=True)
        if policy.removes("housing"):
            # Also takes housing out of the household benefit lists.
            parameters.get_child("gov.hud.abolition").update(start=start, stop=stop, value=True)
        if policy.ubi_counts_as_ssi_income:
            node = parameters.get_child("gov.ssa.ssi.income.sources.unearned")
            sources = list(node(f"{policy.year}-01-01"))
            node.update(start=start, stop=stop, value=sources + ["flatubi_ubi"])
        return parameters

    class FlatTaxUBI(Reform):
        def apply(self):
            apply_data_fixes(self)
            for variable in new_variables:
                if variable.__name__ in self.variables:
                    self.update_variable(variable)
                else:
                    self.add_variable(variable)
            for name in neutralized:
                self.neutralize_variable(name)
            self.modify_parameters(modify)

    FlatTaxUBI.__name__ = f"FlatTaxUBI_{policy.scenario}"
    return FlatTaxUBI
