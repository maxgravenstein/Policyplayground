"""Spec v2 stages (docs/SPEC_v2.md) as resolved switches."""

from __future__ import annotations

import copy
from dataclasses import dataclass, field
from typing import Any

V2_SCENARIOS = (
    "v2_phase1",
    "v2_step1",
    "v2_step2",
    "v2_step3",
    "v2_step4",
    "v2_step5",
    "v2_longrun",
)


@dataclass
class PolicyV2:
    year: int
    scenario: str
    step: int                      # 0 = phase 1, 1..5 = phase 2 steps, 5 = end of schedule
    longrun: bool
    ubi_adult: float
    ubi_child: float
    min_age_adult: int
    senior_age: int
    working_age_ubi: float         # partial UBI for adults 18-64 without Social Security
    eligible_statuses: list[str]
    flat_rate: float
    business_rate: float
    employer_health_share: float
    employer_health_total: float
    employer_health_ratio: float
    ss_thresholds: tuple[float, float]
    ss_rule: str                   # "floor" (higher of benefit or UBI) or "ssdi_only"
    eitc_rule: str                 # "simple", "offset" or "none"
    programs_count_ubi: bool
    programs_removed: list[str]
    ui_factor: float
    ssi_limits: tuple[float, float]
    raw: dict[str, Any] = field(repr=False, default_factory=dict)

    # Attributes the shared output code reads.
    spec = "v2"
    individual_filing = True
    remove_payroll_tax = True
    include_employer_health = True
    social_security_offset = True
    social_security_residual = False
    ubi_min_age = None
    programs_kept = ["medicaid", "chip", "ssi", "medicare", "school_meals"]

    def removes(self, program: str) -> bool:
        return program in self.programs_removed

    @property
    def kept_credits(self) -> list[str]:
        return []


def resolve_v2(cfg: dict[str, Any], scenario: str | None = None) -> PolicyV2:
    cfg = copy.deepcopy(cfg)
    scenario = scenario or cfg.get("scenario", "v2_phase1")
    if scenario not in V2_SCENARIOS:
        raise ValueError(f"Unknown v2 scenario {scenario!r}. Use one of {V2_SCENARIOS}.")
    ubi = cfg.get("ubi", {})
    tax = cfg.get("tax", {})
    steps = int(ubi.get("steps", 5))
    adult = float(ubi.get("adult_annual", 15960))
    longrun = scenario == "v2_longrun"
    step = 0 if scenario == "v2_phase1" else (steps if longrun else int(scenario.removeprefix("v2_step")))

    if step == 0:
        eitc_rule, count, removed, ui = "simple", False, [], 1.0
    elif step < steps:
        eitc_rule, count, removed, ui = "offset", True, [], 1.0
    else:
        # End of the schedule: SNAP, TANF, WIC and the EITC end; unemployment
        # becomes the short top-up. Housing aid continues (new vouchers until
        # year 18). In the long run housing aid is gone too.
        eitc_rule, count, removed = "none", True, ["snap", "tanf", "wic"]
        ui = float(cfg.get("unemployment", {}).get("topup_factor", 0.5))
        if longrun:
            removed = removed + ["housing"]

    rates = tax.get("flat_rate_by_scenario", {})
    ssi = cfg.get("ssi", {})
    th = tax.get("social_security_thresholds", [25000, 34000])
    return PolicyV2(
        year=int(cfg.get("year", 2026)),
        scenario=scenario,
        step=step,
        longrun=longrun,
        ubi_adult=adult,
        ubi_child=float(ubi.get("child_annual", 3000)),
        min_age_adult=int(ubi.get("min_age_adult", 18)),
        senior_age=int(ubi.get("senior_age", 65)),
        working_age_ubi=adult * step / steps,
        eligible_statuses=list(ubi.get("eligible_statuses", ["CITIZEN", "LEGAL_PERMANENT_RESIDENT"])),
        flat_rate=float(rates.get(scenario, tax.get("flat_rate", 0.30))),
        business_rate=float(tax.get("business_rate", 0.21)),
        employer_health_share=min(step / steps, 1.0),
        employer_health_total=float(tax.get("employer_health_total_billions", 1240)) * 1e9,
        employer_health_ratio=float(tax.get("employer_health_family_to_single", 2.6)),
        ss_thresholds=(float(th[0]), float(th[1])),
        ss_rule="ssdi_only" if longrun else "floor",
        eitc_rule=eitc_rule,
        programs_count_ubi=count,
        programs_removed=removed,
        ui_factor=ui,
        ssi_limits=(float(ssi.get("asset_limit_individual", 6000)), float(ssi.get("asset_limit_couple", 9000))),
        raw=cfg,
    )
