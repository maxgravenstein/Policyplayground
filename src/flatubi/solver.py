"""Revenue-neutral flat rate (spec Section 4.2)."""

from __future__ import annotations

from dataclasses import dataclass

from flatubi.outputs import net_budget_effect
from flatubi.run import RunResult


@dataclass
class SolveResult:
    rate: float
    net_budget_billions: float
    target_billions: float
    steps: int
    converged: bool

    @property
    def rate_pct(self) -> float:
        return round(100 * self.rate, 2)


def solve_rate(
    res: RunResult,
    target: float | None = None,
    lo: float = 0.0,
    hi: float = 1.0,
    tol: float = 1e-5,
    max_steps: int = 60,
) -> SolveResult:
    """Find the flat_rate where the net budget effect equals `target`.

    `target` is in $ billions against current law (default: the config's
    solver.target_net_budget_billions, else 0). Bisection. Each step only
    recomputes the flat tax and the corporate line from the cached tax base
    of the run; it does not rerun the simulation. This is exact without the
    behavior module, because nothing else in the model depends on the rate
    (no program in PolicyEngine counts the flat tax). With the behavior
    module on, each step also rescales income with the new MTR.
    """
    if target is None:
        target = float(res.policy.raw.get("solver", {}).get("target_net_budget_billions", 0) or 0)

    def f(rate: float) -> float:
        return net_budget_effect(res, rate) - target

    f_lo, f_hi = f(lo), f(hi)
    if f_lo > 0 or f_hi < 0:
        bad = lo if f_lo > 0 else hi
        return SolveResult(bad, f(bad) + target, target, 0, False)
    steps = 0
    while hi - lo > tol and steps < max_steps:
        mid = (lo + hi) / 2
        if f(mid) < 0:
            lo = mid
        else:
            hi = mid
        steps += 1
    rate = (lo + hi) / 2
    return SolveResult(rate, f(rate) + target, target, steps, True)
