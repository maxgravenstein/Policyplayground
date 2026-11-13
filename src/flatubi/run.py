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
REFORM_PERSON_VARIABLES = ["flatubi_ubi", "flatubi_broad_income", "flatubi_flat_tax", "employer_sponsored_insurance_premiums"]
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
    """Return the local data file; download it once if it is missing.

    Config `data`:
      repo, file, revision   Hugging Face location (pinned revision).
      repo_type              "model" (Enhanced CPS, default) or "dataset" (Populace).
      path                   local file. Default: data/ecps_<revision>/<file>.
    """
    data = cfg.get("data", {})
    revision = str(data.get("revision", "1.115.3"))
    file = data.get("file", "enhanced_cps_2024.h5")
    if data.get("path"):
        target = Path(data["path"])
        target = target if target.is_absolute() else ROOT / target
    else:
        target = ROOT / data.get("local_dir", "data") / f"ecps_{revision}" / file
    if not target.exists():
        from huggingface_hub import hf_hub_download

        hf_hub_download(
            data.get("repo", "policyengine/policyengine-us-data"),
            file,
            revision=revision,
            repo_type=data.get("repo_type", "model"),
            local_dir=target.parent,
        )
        downloaded = target.parent / file
        if downloaded != target:
            downloaded.rename(target)
    return target


def dataset_label(cfg: dict[str, Any]) -> str:
    data = cfg.get("data", {})
    return data.get("label") or f"Enhanced CPS 2024 (policyengine-us-data {data.get('revision', '1.115.3')})"


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


# Health-cost values are slow and memory-heavy, and net income does not need
# them. They are computed in their own process (see simulate_frames).
HEAVY_HOUSEHOLD_VARIABLES = ["medicaid", "chip", "medicare_cost", "free_school_meals", "reduced_price_school_meals"]
HEAVY_PERSON_VARIABLES = ["medicaid"]


def extract(sim, year: int, reform: bool, log=print, hh_names=None, person_names=None) -> SimResult:
    t0 = time.time()
    hh: dict[str, np.ndarray] = {
        "household_id": _calc(sim, "household_id", year),
        "weight": _calc(sim, "household_weight", year),
    }
    names = hh_names if hh_names is not None else HOUSEHOLD_VARIABLES + (REFORM_HOUSEHOLD_VARIABLES if reform else [])
    for i, name in enumerate(names):
        hh[name] = _calc(sim, name, year, map_to="household")
        log(f"    [{i + 1}/{len(names)}] {name}  ({time.time() - t0:.0f}s)")
    person: dict[str, np.ndarray] = {
        "household_id": _calc(sim, "person_household_id", year),
        "weight": _calc(sim, "person_weight", year),
    }
    pnames = person_names if person_names is not None else PERSON_VARIABLES + (REFORM_PERSON_VARIABLES if reform else [])
    for name in pnames:
        person[name] = _calc(sim, name, year, map_to="person")
    log(f"    done in {time.time() - t0:.0f}s")
    return SimResult(pd.DataFrame(person), pd.DataFrame(hh), {"seconds": time.time() - t0})


MTR_DELTA = 1_000.0


def add_mtr(result: SimResult, path: Path, policy: Policy | None, year: int, isolate: bool = True, log=print) -> None:
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
    p = result.person
    wages = p.employment_income.to_numpy()
    bump = np.where(wages > 0, MTR_DELTA, 0.0)
    log("    MTR: simulate with wages + $1,000")
    net2 = _isolated(isolate, "simulate_bumped_net", str(path), policy, year, wages + bump)
    hh = result.household
    d_earn = pd.Series(bump).groupby(p.household_id.to_numpy()).sum()
    d_earn = hh.household_id.map(d_earn).fillna(0).to_numpy()
    d_net = net2 - hh.household_net_income.to_numpy()
    mtr_h = np.where(d_earn > 0, 1 - d_net / np.where(d_earn > 0, d_earn, 1), np.nan)
    hh["mtr"] = mtr_h
    by_id = pd.Series(mtr_h, index=hh.household_id.to_numpy())
    p["mtr"] = np.where(wages > 0, p.household_id.map(by_id).to_numpy(), np.nan)
    p["mtr_measured"] = wages > 0


# --------------------------------------------------------------------------
# Each simulation runs in its own process
# --------------------------------------------------------------------------
# A PolicyEngine simulation on Populace needs about 13 GB. Python does not give
# all of that memory back when the simulation is deleted, so two simulations
# in one process do not fit on a 15 GB machine. Each simulation therefore runs
# in a fresh process that returns only the small result frames and then exits.


def _reform_class(policy: Policy | None):
    if policy is None:
        from flatubi.reform.datafix import DataFix

        return DataFix
    from flatubi.reform import build_reform

    return build_reform(policy)


def simulate_part(path: str, policy: Policy | None, year: int, hh_names: list, person_names: list) -> SimResult:
    """One simulation computing only the given variables."""
    from policyengine_us import Microsimulation

    sim = Microsimulation(dataset=path, reform=_reform_class(policy))
    return extract(sim, year, reform=policy is not None, hh_names=hh_names, person_names=person_names)


def simulate_frames(path: str, policy: Policy | None, year: int, isolate: bool = True) -> SimResult:
    """Baseline (policy None) or reform frames, from two simulations.

    The first computes net income, taxes, benefits and poverty; the second
    the heavy health-cost values. Each runs in its own process if `isolate`.
    """
    reform = policy is not None
    hh_all = HOUSEHOLD_VARIABLES + (REFORM_HOUSEHOLD_VARIABLES if reform else [])
    p_all = PERSON_VARIABLES + (REFORM_PERSON_VARIABLES if reform else [])
    hh_light = [v for v in hh_all if v not in HEAVY_HOUSEHOLD_VARIABLES]
    p_light = [v for v in p_all if v not in HEAVY_PERSON_VARIABLES]
    main = _isolated(isolate, "simulate_part", path, policy, year, hh_light, p_light)
    main.meta["not_computed"] = []
    groups = [
        (["medicaid"], ["medicaid"]),
        (["chip"], []),
        (["medicare_cost"], []),
        (["free_school_meals", "reduced_price_school_meals"], []),
    ]
    for hh_group, p_group in groups:
        print(f"    health-cost values: {', '.join(hh_group)} (own simulation)", flush=True)
        try:
            part = _isolated(isolate, "simulate_part", path, policy, year, hh_group, p_group)
        except ChildOutOfMemory as e:
            print(f"    NOT COMPUTED: {e}", flush=True)
            for c in hh_group:
                main.household[c] = np.nan
            for c in p_group:
                main.person[c] = np.nan
            main.meta["not_computed"] += hh_group
            continue
        if not np.array_equal(main.household.household_id.to_numpy(), part.household.household_id.to_numpy()):
            raise ValueError("The simulations returned households in a different order.")
        for c in hh_group:
            main.household[c] = part.household[c].to_numpy()
        for c in p_group:
            main.person[c] = part.person[c].to_numpy()
    return main


def simulate_bumped_net(path: str, policy: Policy | None, year: int, wages: np.ndarray) -> np.ndarray:
    """Household net income with wages set to `wages` (for the MTR)."""
    from policyengine_us import Microsimulation

    sim = Microsimulation(dataset=path, reform=_reform_class(policy))
    sim.set_input("employment_income_before_lsr", year, wages)
    return _calc(sim, "household_net_income", year, map_to="household")


def _child_to_file(fn_name: str, args: tuple, out: str) -> None:
    result = globals()[fn_name](*args)
    with open(out, "wb") as f:
        pickle.dump(result, f)


class ChildOutOfMemory(RuntimeError):
    pass


MIN_FREE_GB = 0.8


def _mem_available_gb() -> float:
    try:
        with open("/proc/meminfo") as f:
            for line in f:
                if line.startswith("MemAvailable:"):
                    return int(line.split()[1]) / 1e6
    except OSError:
        pass
    return float("inf")


def _watch_memory(proc) -> None:
    """Wait for the child; stop it before the kernel's out-of-memory killer acts.

    The kernel may kill other processes too (in a cloud session, the session
    itself), so we stop the child first when free memory gets low.
    """
    while proc.is_alive():
        proc.join(timeout=1.0)
        if proc.is_alive() and _mem_available_gb() < MIN_FREE_GB:
            proc.kill()
            proc.join()
            proc._stopped_for_memory = True


def _isolated(isolate: bool, fn_name: str, *args):
    """Run globals()[fn_name](*args), in a fresh process if `isolate`.

    The child writes its result to a temporary file and exits, so all of
    its memory goes back to the system. If the child dies (for example, the
    kernel kills it for lack of memory: exit code -9), this raises.
    """
    if not isolate:
        out = globals()[fn_name](*args)
        gc.collect()
        return out
    import multiprocessing as mp
    import tempfile

    with tempfile.TemporaryDirectory() as tmp:
        out = Path(tmp) / "result.pkl"
        proc = mp.get_context("spawn").Process(target=_child_to_file, args=(fn_name, args, str(out)))
        proc.start()
        _watch_memory(proc)
        if getattr(proc, "_stopped_for_memory", False):
            raise ChildOutOfMemory(f"{fn_name}: stopped, the machine was almost out of memory")
        if proc.exitcode == -9:
            raise ChildOutOfMemory(f"{fn_name}: killed by the system, out of memory")
        if proc.exitcode != 0 or not out.exists():
            hint = " (killed: probably out of memory)" if proc.exitcode == -9 else ""
            raise RuntimeError(f"{fn_name} failed in its process, exit code {proc.exitcode}{hint}")
        with open(out, "rb") as f:
            return pickle.load(f)


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


def _isolate(cfg: dict[str, Any]) -> bool:
    return bool(cfg.get("run", {}).get("isolate_simulations", True))


def run_baseline(cfg: dict[str, Any], year: int, mtr: bool = True, log=print) -> SimResult:
    path = dataset_path(cfg)
    cache_dir = ROOT / "outputs" / ".cache"
    cache_dir.mkdir(parents=True, exist_ok=True)
    cache = cache_dir / f"baseline_{year}_{_baseline_cache_key(path, year, mtr)}.pkl"
    if cache.exists():
        log(f"  baseline: from cache {cache.name}")
        with open(cache, "rb") as f:
            return pickle.load(f)
    log("  baseline: simulate current law")
    result = simulate_frames(str(path), None, year, _isolate(cfg))
    if mtr:
        add_mtr(result, path, None, year, isolate=_isolate(cfg), log=log)
    with open(cache, "wb") as f:
        pickle.dump(result, f)
    return result


def run_reform(cfg: dict[str, Any], policy: Policy, mtr: bool = True, log=print) -> SimResult:
    path = dataset_path(cfg)
    log(f"  reform: simulate {policy.scenario}")
    result = simulate_frames(str(path), policy, policy.year, _isolate(cfg))
    if mtr:
        add_mtr(result, path, policy, policy.year, isolate=_isolate(cfg), log=log)
    return result


def run(cfg: dict[str, Any] | str | Path, scenario: str | None = None, mtr: bool = True, log=print) -> RunResult:
    if not isinstance(cfg, dict):
        cfg = load_config(cfg)
    policy = resolve(cfg, scenario)
    t0 = time.time()
    log(f"  data: {dataset_label(cfg)}")
    baseline = run_baseline(cfg, policy.year, mtr=mtr, log=log)
    reform = run_reform(cfg, policy, mtr=mtr, log=log)
    path = dataset_path(cfg)
    meta = {
        "versions": package_versions(),
        "dataset": str(path.relative_to(ROOT)) if str(path).startswith(str(ROOT)) else str(path),
        "dataset_label": dataset_label(cfg),
        "data_revision": str(cfg.get("data", {}).get("revision", "")),
        "data_year": 2024,
        "year": policy.year,
        "seconds": round(time.time() - t0),
        "mtr": mtr,
        "employer_health_in_data": bool(
            "employer_sponsored_insurance_premiums" in reform.person
            and (reform.person.employer_sponsored_insurance_premiums * reform.person.weight).sum() > 0
        ),
    }
    return RunResult(policy, baseline, reform, meta)
