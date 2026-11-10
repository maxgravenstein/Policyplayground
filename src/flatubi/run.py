"""Run the baseline and reform microsimulations and keep the results we need.

A full run is slow (several minutes per simulation), so this module pulls
the values it needs into small pandas frames, then frees the simulation.
The baseline frames are cached on disk, because the baseline does not depend
on the reform switches.
"""

from __future__ import annotations

import gc
import hashlib
import json
import pickle
import time
from dataclasses import dataclass, field
from importlib.metadata import version
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

from flatubi.config import Policy, load_config, resolve

ROOT = Path(__file__).resolve().parents[2]

# Household-level values (summed over members where needed).
HOUSEHOLD_VARIABLES = [
    "household_net_income",
    "household_market_income",
    "household_benefits",
    "household_tax",
    "household_state_income_tax",
    "household_count_people",
    "income_tax",
    "eitc",
    "ctc",
    "employee_social_security_tax",
    "employee_medicare_tax",
    "additional_medicare_tax",
    "self_employment_tax",
    "employer_social_security_tax",
    "employer_medicare_tax",
    "flat_tax",
    "basic_income",
    "snap",
    "tanf",
    "wic",
    "housing_assistance",
    "aca_ptc",
    "unemployment_compensation",
    "social_security",
    "ssi",
    "medicaid",
    "chip",
    "medicare_cost",
    "free_school_meals",
    "reduced_price_school_meals",
    "employment_income",
    "self_employment_income",
    "spm_unit_net_income",
]
PERSON_VARIABLES = [
    "age",
    "is_disabled",
    "employment_income",
    "self_employment_income",
    "social_security",
    "ssi",
    "medicaid",
    "person_in_poverty",
    "in_deep_poverty",
    "market_income",
]
REFORM_PERSON_VARIABLES = ["flatubi_ubi", "flatubi_broad_income", "flatubi_flat_tax"]
REFORM_HOUSEHOLD_VARIABLES = ["flatubi_broad_income", "flatubi_flat_tax"]


@dataclass
class SimResult:
    """Frames for one simulation (baseline or reform)."""

    person: pd.DataFrame
    household: pd.DataFrame
    meta: dict[str, Any] = field(default_factory=dict)


@dataclass
class RunResult:
    policy: Policy
    baseline: SimResult
    reform: SimResult
    meta: dict[str, Any] = field(default_factory=dict)


def dataset_path(cfg: dict[str, Any]) -> Path:
    """Download (once) the pinned Enhanced CPS file and return its path."""
    data = cfg.get("data", {})
    if data.get("path"):
        return Path(data["path"])
    revision = str(data.get("revision", "1.115.3"))
    local_dir = ROOT / data.get("local_dir", "data") / f"ecps_{revision}"
    target = local_dir / data.get("file", "enhanced_cps_2024.h5")
    if not target.exists():
        from huggingface_hub import hf_hub_download

        hf_hub_download(
            data.get("repo", "policyengine/policyengine-us-data"),
            data.get("file", "enhanced_cps_2024.h5"),
            revision=revision,
            local_dir=local_dir,
        )
    return target


def package_versions() -> dict[str, str]:
    out = {}
    for name in ["policyengine-us", "policyengine-core", "policyengine-us-data", "flatubi"]:
        try:
            out[name] = version(name)
        except Exception:
            out[name] = "not installed"
    return out


def _calc(sim, name: str, year: int, map_to: str | None = None) -> np.ndarray:
    values = sim.calculate(name, year, map_to=map_to)
    return np.asarray(getattr(values, "values", values), dtype=float)


def extract(sim, year: int, reform: bool, log=print) -> SimResult:
    t0 = time.time()
    hh: dict[str, np.ndarray] = {
        "household_id": _calc(sim, "household_id", year),
        "weight": _calc(sim, "household_weight", year),
    }
    names = HOUSEHOLD_VARIABLES + (REFORM_HOUSEHOLD_VARIABLES if reform else [])
    for i, name in enumerate(names):
        hh[name] = _calc(sim, name, year, map_to="household")
        log(f"    [{i + 1}/{len(names)}] {name}  ({time.time() - t0:.0f}s)")
    person: dict[str, np.ndarray] = {
        "household_id": _calc(sim, "person_household_id", year),
        "weight": _calc(sim, "person_weight", year),
    }
    pnames = PERSON_VARIABLES + (REFORM_PERSON_VARIABLES if reform else [])
    for name in pnames:
        person[name] = _calc(sim, name, year, map_to="person")
    log(f"    done in {time.time() - t0:.0f}s")
    return SimResult(pd.DataFrame(person), pd.DataFrame(hh), {"seconds": time.time() - t0})


MTR_DELTA = 1_000.0


def add_mtr(result: SimResult, path: Path, reform_cls, year: int, log=print) -> None:
    """Effective marginal tax rate on earnings, by a second simulation.

    PolicyEngine's `marginal_tax_rate` variable copies the whole simulation
    and needs more memory than this machine has. Instead we run the
    simulation again with every worker's wages raised by MTR_DELTA at once,
    and set for each household:

        MTR = 1 - (change in household net income) / (change in earnings)

    Every worker in the household gets that MTR. People with no wages have
    no MTR. This is close to the per-person MTR for one-earner households;
    for two-earner households it is the average of the two.
    """
    from policyengine_us import Microsimulation

    p = result.person
    wages = p.employment_income.to_numpy()
    bump = np.where(wages > 0, MTR_DELTA, 0.0)
    log("    MTR: simulate with wages + $1,000")
    sim = Microsimulation(dataset=str(path), reform=reform_cls)
    sim.set_input("employment_income_before_lsr", year, wages + bump)
    net2 = _calc(sim, "household_net_income", year, map_to="household")
    del sim
    gc.collect()
    hh = result.household
    d_earn = pd.Series(bump).groupby(p.household_id.to_numpy()).sum()
    d_earn = hh.household_id.map(d_earn).fillna(0).to_numpy()
    d_net = net2 - hh.household_net_income.to_numpy()
    mtr_h = np.where(d_earn > 0, 1 - d_net / np.where(d_earn > 0, d_earn, 1), np.nan)
    hh["mtr"] = mtr_h
    by_id = pd.Series(mtr_h, index=hh.household_id.to_numpy())
    p["mtr"] = np.where(wages > 0, p.household_id.map(by_id).to_numpy(), np.nan)
    p["mtr_measured"] = wages > 0


def _baseline_cache_key(path: Path, year: int, mtr: bool) -> str:
    info = {
        "data": str(path),
        "size": path.stat().st_size,
        "year": year,
        "mtr": mtr,
        "versions": package_versions(),
        "variables": HOUSEHOLD_VARIABLES + PERSON_VARIABLES,
        "schema": 4,
    }
    return hashlib.sha1(json.dumps(info, sort_keys=True).encode()).hexdigest()[:12]


def run_baseline(cfg: dict[str, Any], year: int, mtr: bool = True, log=print) -> SimResult:
    from policyengine_us import Microsimulation

    path = dataset_path(cfg)
    cache_dir = ROOT / "outputs" / ".cache"
    cache_dir.mkdir(parents=True, exist_ok=True)
    cache = cache_dir / f"baseline_{year}_{_baseline_cache_key(path, year, mtr)}.pkl"
    if cache.exists():
        log(f"  baseline: from cache {cache.name}")
        with open(cache, "rb") as f:
            return pickle.load(f)
    from flatubi.reform.datafix import DataFix

    log("  baseline: simulate current law")
    sim = Microsimulation(dataset=str(path), reform=DataFix)
    result = extract(sim, year, reform=False, log=log)
    del sim
    gc.collect()
    if mtr:
        add_mtr(result, path, DataFix, year, log=log)
    with open(cache, "wb") as f:
        pickle.dump(result, f)
    return result


def run_reform(cfg: dict[str, Any], policy: Policy, mtr: bool = True, log=print) -> SimResult:
    from policyengine_us import Microsimulation

    from flatubi.reform import build_reform

    path = dataset_path(cfg)
    log(f"  reform: simulate {policy.scenario}")
    reform_cls = build_reform(policy)
    sim = Microsimulation(dataset=str(path), reform=reform_cls)
    result = extract(sim, policy.year, reform=True, log=log)
    del sim
    gc.collect()
    if mtr:
        add_mtr(result, path, reform_cls, policy.year, log=log)
    return result


def run(cfg: dict[str, Any] | str | Path, scenario: str | None = None, mtr: bool = True, log=print) -> RunResult:
    if not isinstance(cfg, dict):
        cfg = load_config(cfg)
    policy = resolve(cfg, scenario)
    t0 = time.time()
    baseline = run_baseline(cfg, policy.year, mtr=mtr, log=log)
    reform = run_reform(cfg, policy, mtr=mtr, log=log)
    meta = {
        "versions": package_versions(),
        "dataset": str(dataset_path(cfg).relative_to(ROOT)) if str(dataset_path(cfg)).startswith(str(ROOT)) else str(dataset_path(cfg)),
        "data_revision": str(cfg.get("data", {}).get("revision", "")),
        "data_year": 2024,
        "year": policy.year,
        "seconds": round(time.time() - t0),
        "mtr": mtr,
    }
    return RunResult(policy, baseline, reform, meta)
