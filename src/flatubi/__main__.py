"""Command line (spec Section 7.1).

    python -m flatubi run --config config.yaml [--scenario phase1] [--no-mtr]
    python -m flatubi solve-rate --config config.yaml
    python -m flatubi compare --configs a.yaml b.yaml
    python -m flatubi baseline-check --config config.yaml
"""

from __future__ import annotations

import argparse
import pickle
import sys
import time
from pathlib import Path

import pandas as pd

from flatubi.config import load_config
from flatubi.run import ROOT


def _log(msg: str) -> None:
    print(msg, flush=True)


def _run(cfg_path: str, scenario: str | None, mtr: bool):
    from flatubi import outputs, report, solver
    from flatubi import run as runmod

    cfg = load_config(cfg_path)
    res = runmod.run(cfg, scenario=scenario, mtr=mtr, log=_log)
    tables = outputs.all_tables(res)
    solve = solver.solve_rate(res)
    if solve.converged:
        at = outputs.with_rate(res, solve.rate)
        h = outputs.household_frame(at)
        tables["distribution_decile_at_solved_rate"] = outputs.distribution_by_decile(h)
        tables["losers_at_solved_rate"] = outputs.biggest_losers(h)
        tables["budget_at_solved_rate"] = outputs.budget_table(at)
    out_dir = ROOT / "outputs" / f"{res.policy.scenario}_{res.policy.year}"
    path = report.write_outputs(res, tables, solve, out_dir)
    with open(out_dir / "result.pkl", "wb") as f:
        pickle.dump(res, f)
    return res, tables, solve, path


def cmd_run(args) -> int:
    t = time.time()
    res, tables, solve, path = _run(args.config, args.scenario, not args.no_mtr)
    b = tables["budget"].set_index("item")
    _log("")
    _log(tables["budget"].to_string(index=False))
    _log("")
    _log(f"Net budget effect: {b.loc['Net budget effect (revenue minus spending)', 'difference']:+,.1f} B")
    _log(f"Revenue-neutral rate: {solve.rate_pct:.2f}% (converged: {solve.converged})")
    _log(f"Report: {path}  ({time.time() - t:.0f}s)")
    return 0


def _load_or_run(cfg_path: str, scenario: str | None):
    cfg = load_config(cfg_path)
    scen = scenario or cfg.get("scenario", "steady_state")
    pkl = ROOT / "outputs" / f"{scen}_{cfg.get('year', 2026)}" / "result.pkl"
    if pkl.exists():
        with open(pkl, "rb") as f:
            res = pickle.load(f)
        # Use the current config's solver, corporate and behavior settings.
        res.policy.raw = cfg
        if res.policy.flat_rate == float(cfg["tax"]["flat_rate"]):
            return res
    from flatubi import run as runmod

    return runmod.run(cfg, scenario=scenario, mtr=False, log=_log)


def cmd_solve(args) -> int:
    from flatubi import solver

    res = _load_or_run(args.config, args.scenario)
    s = solver.solve_rate(res, target=args.target)
    _log(f"Scenario {res.policy.scenario} {res.policy.year}: target {s.target_billions:,.0f} B")
    _log(f"Revenue-neutral flat rate: {s.rate_pct:.2f}%  (net budget {s.net_budget_billions:+,.2f} B, {s.steps} steps, converged {s.converged})")
    return 0 if s.converged else 1


def cmd_compare(args) -> int:
    from flatubi import outputs, solver

    rows = []
    for path in args.configs:
        res = _load_or_run(path, None)
        t = outputs.all_tables(res)
        b = t["budget"].set_index("item")
        pov = t["poverty"].set_index("group")
        s = solver.solve_rate(res)
        rows.append(
            {
                "config": path,
                "scenario": res.policy.scenario,
                "flat_rate_pct": 100 * res.policy.flat_rate,
                "net_budget_B": b.loc["Net budget effect (revenue minus spending)", "difference"],
                "revenue_neutral_rate_pct": s.rate_pct if s.converged else None,
                "net_transfer_B": b.loc["Net transfer: UBI minus flat tax, where positive", "reform"],
                "ubi_cost_B": b.loc["UBI (gross)", "reform"],
                "poverty_change_pp": pov.loc["All people", "poverty_change_pp"],
                "child_poverty_change_pp": pov.loc["Children (under 18)", "poverty_change_pp"],
                "gini_change": t["inequality"].change.iloc[0],
            }
        )
    df = pd.DataFrame(rows)
    _log(df.to_string(index=False))
    out = ROOT / "outputs" / "compare.csv"
    df.to_csv(out, index=False)
    _log(f"Wrote {out}")
    return 0


def cmd_baseline(args) -> int:
    from flatubi import outputs
    from flatubi.config import resolve
    from flatubi.run import RunResult, run_baseline

    cfg = load_config(args.config)
    pol = resolve(cfg)
    base = run_baseline(cfg, pol.year, mtr=False, log=_log)
    fake = RunResult(pol, base, base)
    _log(outputs.aggregate_checks(fake).to_string(index=False))
    return 0


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="flatubi", description="Flat tax + UBI microsimulation")
    sub = ap.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("run", help="run one scenario and write outputs/<scenario>_<year>/")
    r.add_argument("--config", default="config.yaml")
    r.add_argument("--scenario", choices=["steady_state", "phase1", "custom"])
    r.add_argument("--no-mtr", action="store_true", help="skip marginal tax rates (faster)")
    r.set_defaults(fn=cmd_run)
    s = sub.add_parser("solve-rate", help="find the revenue-neutral flat rate")
    s.add_argument("--config", default="config.yaml")
    s.add_argument("--scenario", choices=["steady_state", "phase1", "custom"])
    s.add_argument("--target", type=float, default=None, help="net budget target, $ billions")
    s.set_defaults(fn=cmd_solve)
    c = sub.add_parser("compare", help="compare several configs")
    c.add_argument("--configs", nargs="+", required=True)
    c.set_defaults(fn=cmd_compare)
    b = sub.add_parser("baseline-check", help="print baseline totals against published totals")
    b.add_argument("--config", default="config.yaml")
    b.set_defaults(fn=cmd_baseline)
    args = ap.parse_args(argv)
    return args.fn(args)


if __name__ == "__main__":
    sys.exit(main())
