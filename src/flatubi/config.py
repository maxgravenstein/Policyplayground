"""Load config.yaml and turn a scenario name into a full set of switches."""

from __future__ import annotations

import copy
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml

ALL_REMOVABLE = [
    "snap",
    "tanf",
    "wic",
    "housing",
    "eitc",
    "ctc",
    "aca_ptc",
    "unemployment",
    "social_security",
]
ALL_KEEPABLE = ["medicaid", "chip", "ssi", "medicare", "school_meals"]
SCENARIOS = ("steady_state", "phase1", "custom")


@dataclass
class Policy:
    """The resolved switches for one run. The reform code reads only this."""

    year: int
    scenario: str
    ubi_adult: float
    ubi_child: float
    min_age_adult: int
    ubi_min_age: int | None  # None: every adult. 65 in phase1.
    ubi_counts_as_ssi_income: bool
    flat_rate: float
    individual_filing: bool
    remove_payroll_tax: bool
    include_employer_health: bool
    include_retirement_contributions: bool
    employer_payroll_to_wages: bool
    programs_removed: list[str]
    programs_kept: list[str]
    social_security_offset: bool
    social_security_residual: bool  # steady state: keep Social Security above the UBI
    raw: dict[str, Any] = field(repr=False, default_factory=dict)

    def removes(self, program: str) -> bool:
        return program in self.programs_removed


def load_config(path: str | Path) -> dict[str, Any]:
    with open(path) as f:
        cfg = yaml.safe_load(f)
    cfg.setdefault("_path", str(path))
    return cfg


def resolve(cfg: dict[str, Any], scenario: str | None = None) -> Policy:
    """Apply the scenario rules of spec Section 2.5 to the config switches.

    steady_state: the config as written, with UBI for every adult. With
        steady_state.social_security_residual (default true), Social Security
        is kept above the UBI: each beneficiary gets max(benefit - own UBI, 0)
        on top of the UBI. Otherwise Social Security is removed.
    phase1: UBI only for children and people at or above phase1_min_age.
        Social Security is kept and offset against the UBI. Working-age
        adults keep the current programs, so only the federal tax credits
        (EITC, CTC) go, because the flat tax replaces the income tax.
    custom: every switch exactly as written in the config.
    """
    cfg = copy.deepcopy(cfg)
    scenario = scenario or cfg.get("scenario", "steady_state")
    if scenario not in SCENARIOS:
        raise ValueError(f"Unknown scenario {scenario!r}. Use one of {SCENARIOS}.")
    ubi = cfg.get("ubi", {})
    tax = cfg.get("tax", {})
    removed = list(cfg.get("programs_removed", ALL_REMOVABLE))
    kept = list(cfg.get("programs_kept", ALL_KEEPABLE))
    unknown = set(removed) - set(ALL_REMOVABLE)
    if unknown:
        raise ValueError(f"Unknown programs in programs_removed: {sorted(unknown)}")
    ubi_min_age = None
    ss_offset = False

    ss_residual = False
    if scenario == "steady_state":
        ss_residual = bool(cfg.get("steady_state", {}).get("social_security_residual", True))
        if ss_residual:
            removed = [p for p in removed if p != "social_security"]
        elif "social_security" not in removed:
            removed.append("social_security")
    elif scenario == "phase1":
        ubi_min_age = int(ubi.get("phase1_min_age", 65))
        removed = [p for p in removed if p in ("eitc", "ctc")]
        ss_offset = bool(cfg.get("phase1", {}).get("social_security_offset", True))
    else:  # custom
        if cfg.get("custom", {}).get("ubi_min_age") is not None:
            ubi_min_age = int(cfg["custom"]["ubi_min_age"])
        ss_offset = bool(cfg.get("phase1", {}).get("social_security_offset", False))
        ss_residual = bool(cfg.get("custom", {}).get("social_security_residual", False))
        if ss_residual and ss_offset:
            raise ValueError("custom: use social_security_offset or social_security_residual, not both.")
        if ss_residual:
            removed = [p for p in removed if p != "social_security"]
        if ss_offset and "social_security" in removed:
            raise ValueError(
                "custom: social_security_offset needs Social Security kept. "
                "Remove 'social_security' from programs_removed."
            )

    return Policy(
        year=int(cfg.get("year", 2026)),
        scenario=scenario,
        ubi_adult=float(ubi.get("adult_annual", 15960)),
        ubi_child=float(ubi.get("child_annual", 3000)),
        min_age_adult=int(ubi.get("min_age_adult", 18)),
        ubi_min_age=ubi_min_age,
        ubi_counts_as_ssi_income=bool(ubi.get("counts_as_ssi_income", False)),
        flat_rate=float(tax.get("flat_rate", 0.3825)),
        individual_filing=bool(tax.get("individual_filing", True)),
        remove_payroll_tax=bool(tax.get("remove_payroll_tax", True)),
        include_employer_health=bool(tax.get("include_employer_health_in_base", True)),
        include_retirement_contributions=bool(
            tax.get("include_retirement_contributions_in_base", True)
        ),
        employer_payroll_to_wages=bool(tax.get("employer_payroll_to_wages", False)),
        programs_removed=removed,
        programs_kept=kept,
        social_security_offset=ss_offset,
        social_security_residual=ss_residual,
        raw=cfg,
    )
