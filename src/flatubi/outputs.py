"""Tables from a RunResult: budget, distribution, poverty, MTR, losers, checks.

All money is in dollars per year, except budget tables (billions).
"""

from __future__ import annotations

import copy
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
import yaml

from flatubi.run import RunResult

BILLION = 1e9
AGE_GROUPS = [(0, 18, "Under 18"), (18, 30, "18-29"), (30, 50, "30-49"), (50, 65, "50-64"), (65, 200, "65+")]
HOUSEHOLD_TYPES = ["Single", "Couple", "Single parent", "Couple with children", "65+ household", "Other (3+ adults)"]
CHANGE_BINS = ["Gain more than 5%", "Gain less than 5%", "No change", "Lose less than 5%", "Lose more than 5%"]
NO_CHANGE = 0.001  # |change| below 0.1% of net income counts as no change
FEDERAL_PAYROLL = [
    "employee_social_security_tax",
    "employee_medicare_tax",
    "additional_medicare_tax",
    "self_employment_tax",
]
EMPLOYER_PAYROLL = ["employer_social_security_tax", "employer_medicare_tax"]
REMOVABLE_BENEFITS = ["snap", "tanf", "wic", "housing_assistance", "unemployment_compensation", "aca_ptc"]


# --------------------------------------------------------------------------
# Rate changes without a new simulation
# --------------------------------------------------------------------------


def flat_tax_base(res: RunResult) -> float:
    """Sum of w x (flat tax per unit of rate), in dollars. Linear in the rate."""
    r0 = res.policy.flat_rate
    p = res.reform.person
    if r0 > 0:
        return float((p.weight * p.flatubi_flat_tax).sum() / r0)
    return float((p.weight * p.flatubi_broad_income.clip(lower=0)).sum())


def behavior_factors(res: RunResult, rate: float) -> np.ndarray:
    """Spec 7.4: scale income by ((1 - new MTR) / (1 - old MTR)) ^ elasticity.

    Rough. Uses the measured MTRs of each person; people without a measured
    MTR keep their income. The new MTR moves one for one with the rate.
    """
    b = res.policy.raw.get("behavior", {})
    p = res.reform.person
    if "mtr" not in p or "mtr" not in res.baseline.person:
        return np.ones(len(p))
    old = res.baseline.person["mtr"].to_numpy()
    new = p["mtr"].to_numpy() + (rate - res.policy.flat_rate) * (p.flatubi_broad_income > 0)
    measured = res.baseline.person.get("mtr_measured", pd.Series(True, index=p.index)).to_numpy()
    ratio = np.clip(1 - new, 0.05, None) / np.clip(1 - old, 0.05, None)
    high = p.flatubi_broad_income.to_numpy() > float(b.get("high_income_threshold", 200000))
    e = np.where(high, float(b.get("elasticity_high_income", 0.5)), float(b.get("elasticity_low_income", 0.25)))
    factor = np.clip(ratio, 0.25, 4) ** e
    return np.where(measured, factor, 1.0)


def flat_tax_revenue(res: RunResult, rate: float, behavior: bool | None = None) -> float:
    """Flat tax revenue (dollars) at `rate`. Recomputes the tax only."""
    if behavior is None:
        behavior = bool(res.policy.raw.get("behavior", {}).get("enabled", False))
    if not behavior:
        return rate * flat_tax_base(res)
    p = res.reform.person
    if res.policy.individual_filing:
        base = (p.flatubi_broad_income * behavior_factors(res, rate)).clip(lower=0)
        return float(rate * (p.weight * base).sum())
    return rate * flat_tax_base(res)  # pooled units: no behavior adjustment


def with_rate(res: RunResult, rate: float) -> RunResult:
    """A copy of the result with the flat tax recomputed at `rate`.

    Net income moves by the change in flat tax. Poverty flags are NOT
    recomputed (SPM resources need the full simulation), so poverty tables
    from this copy describe the rate of the original run.
    """
    out = copy.copy(res)
    out.reform = copy.copy(res.reform)
    r0 = res.policy.flat_rate
    scale = rate / r0 if r0 > 0 else None
    hh = res.reform.household.copy()
    pp = res.reform.person.copy()
    new_hh_tax = hh.flat_tax * scale if scale is not None else rate * hh.flatubi_broad_income.clip(lower=0)
    new_p_tax = pp.flatubi_flat_tax * scale if scale is not None else rate * pp.flatubi_broad_income.clip(lower=0)
    hh["household_net_income"] = hh.household_net_income - (new_hh_tax - hh.flat_tax)
    hh["household_tax"] = hh.household_tax + (new_hh_tax - hh.flat_tax)
    hh["flat_tax"] = new_hh_tax
    hh["flatubi_flat_tax"] = new_hh_tax
    pp["flatubi_flat_tax"] = new_p_tax
    out.reform.household = hh
    out.reform.person = pp
    out.policy = copy.copy(res.policy)
    out.policy.flat_rate = rate
    out.meta = dict(res.meta, rate_override=rate, poverty_at_rate=r0)
    return out


# --------------------------------------------------------------------------
# Budget (spec 4.1)
# --------------------------------------------------------------------------


def _total(frame: pd.DataFrame, cols) -> float:
    """Weighted total; NaN if the values were not computed (out of memory)."""
    cols = [cols] if isinstance(cols, str) else list(cols)
    if frame[cols].isna().all().all():
        return float("nan")
    return float((frame[cols].sum(axis=1) * frame.weight).sum())


def corporate_rows(res: RunResult) -> tuple[float, float]:
    c = res.policy.raw.get("corporate", {})
    base = float(c.get("profit_base_billions", 1600)) * BILLION
    if c.get("baseline_revenue_billions") not in (None, ""):
        baseline = float(c["baseline_revenue_billions"]) * BILLION
    else:
        baseline = float(c.get("baseline_rate", 0.21)) * base
    return baseline, res.policy.flat_rate * base


def budget_table(res: RunResult) -> pd.DataFrame:
    """Federal budget lines in $ billions: baseline, reform, difference."""
    b, r = res.baseline.household, res.reform.household
    pol = res.policy
    corp_b, corp_r = corporate_rows(res)
    flat_r = flat_tax_revenue(res, pol.flat_rate)
    payroll_r = _total(r, FEDERAL_PAYROLL) + (0.0 if pol.remove_payroll_tax else _total(r, EMPLOYER_PAYROLL))
    rows = [
        ("Revenue", "Federal income tax", _total(b, "income_tax"), _total(r, "income_tax")),
        ("Revenue", "Payroll taxes (employee, employer, self-employment)", _total(b, FEDERAL_PAYROLL + EMPLOYER_PAYROLL), payroll_r),
        ("Revenue", "Flat tax", 0.0, flat_r),
        ("Revenue", "Corporate tax (outside the microsimulation)", corp_b, corp_r),
    ]
    spending = [
        ("UBI (gross)", "basic_income"),
        ("SNAP", "snap"),
        ("TANF", "tanf"),
        ("WIC", "wic"),
        ("Housing assistance", "housing_assistance"),
        ("ACA premium tax credits", "aca_ptc"),
        ("Unemployment insurance", "unemployment_compensation"),
        ("Social Security", "social_security"),
        ("SSI", "ssi"),
        ("Medicaid", "medicaid"),
        ("CHIP", "chip"),
        ("Medicare", "medicare_cost"),
        ("School meals", ["free_school_meals", "reduced_price_school_meals"]),
    ]
    for label, cols in spending:
        rows.append(("Spending", label, _total(b, cols), _total(r, cols)))
    df = pd.DataFrame(rows, columns=["group", "item", "baseline", "reform"])
    rev = df[df.group == "Revenue"][["baseline", "reform"]].sum()
    spend = df[df.group == "Spending"][["baseline", "reform"]].sum()
    total_rows = [
        ("Total", "Total revenue", rev.baseline, rev.reform),
        ("Total", "Total spending", spend.baseline, spend.reform),
        ("Total", "Net budget effect (revenue minus spending)", rev.baseline - spend.baseline, rev.reform - spend.reform),
    ]
    eitc_r = 0.0  # federal income tax is abolished in every scenario
    memo = [
        ("Memo", "EITC (inside federal income tax)", _total(b, "eitc"), eitc_r),
        ("Memo", "CTC (inside federal income tax)", _total(b, "ctc"), 0.0),
        ("Memo", "State and local income tax (not in net budget)", _total(b, "household_state_income_tax"), _total(r, "household_state_income_tax")),
        ("Memo", "Net transfer: UBI minus flat tax, where positive", 0.0, net_transfer(res)),
    ]
    df = pd.concat([df, pd.DataFrame(total_rows + memo, columns=df.columns)], ignore_index=True)
    df[["baseline", "reform"]] = df[["baseline", "reform"]] / BILLION
    df["difference"] = df.reform - df.baseline
    return df.round(1)


def net_budget_effect(res: RunResult, rate: float | None = None) -> float:
    """Reform minus baseline (revenue minus spending), $ billions."""
    rate = res.policy.flat_rate if rate is None else rate
    t = budget_table(res)
    at = t.set_index("item")
    base_effect = at.loc["Net budget effect (revenue minus spending)", "difference"]
    # Move the two rate-dependent lines from the run rate to `rate`.
    r0 = res.policy.flat_rate
    c = res.policy.raw.get("corporate", {})
    corp_base = float(c.get("profit_base_billions", 1600))
    d_flat = (flat_tax_revenue(res, rate) - flat_tax_revenue(res, r0)) / BILLION
    d_corp = (rate - r0) * corp_base
    return float(base_effect + d_flat + d_corp)


def net_transfer(res: RunResult) -> float:
    """Spec 4.1: UBI minus flat tax per person, summed where positive ($)."""
    p = res.reform.person
    net = p.flatubi_ubi - p.flatubi_flat_tax
    return float((p.weight * net.clip(lower=0)).sum())


# --------------------------------------------------------------------------
# Household frame used by the distribution tables
# --------------------------------------------------------------------------


def _weighted_quantile_bins(values, weights, n) -> np.ndarray:
    order = np.argsort(values, kind="stable")
    cum = np.cumsum(weights[order])
    cum = cum / cum[-1]
    bins = np.empty(len(values), dtype=int)
    bins[order] = np.minimum((cum * n - 1e-12).astype(int) + 1, n)
    return bins


def household_frame(res: RunResult) -> pd.DataFrame:
    b, r = res.baseline.household, res.reform.household
    if not np.array_equal(b.household_id.to_numpy(), r.household_id.to_numpy()):
        raise ValueError("Baseline and reform households are not in the same order.")
    count_ptc = bool(res.policy.raw.get("distribution", {}).get("count_aca_ptc_as_income", True))
    h = pd.DataFrame({"household_id": b.household_id, "weight": b.weight})
    h["size"] = b.household_count_people.clip(lower=1)
    h["net_b"] = b.household_net_income + (b.aca_ptc if count_ptc else 0)
    h["net_r"] = r.household_net_income + (r.aca_ptc if count_ptc else 0)
    h["change"] = h.net_r - h.net_b
    h["rel_change"] = h.change / np.maximum(h.net_b, 1)
    h["equiv_b"] = h.net_b / np.sqrt(h["size"])
    h["equiv_r"] = h.net_r / np.sqrt(h["size"])
    h["person_weight"] = h.weight * h["size"]
    h["decile"] = _weighted_quantile_bins(h.equiv_b.to_numpy(), h.person_weight.to_numpy(), 10)
    h["quintile"] = (h.decile + 1) // 2

    # Household type from member ages.
    p = res.baseline.person
    ages = p.groupby("household_id").age
    counts = pd.DataFrame(
        {
            "adults": p.assign(x=p.age >= 18).groupby("household_id").x.sum(),
            "children": p.assign(x=p.age < 18).groupby("household_id").x.sum(),
            "seniors": p.assign(x=p.age >= 65).groupby("household_id").x.sum(),
            "max_age": ages.max(),
        }
    )
    h = h.merge(counts, left_on="household_id", right_index=True, how="left")
    conditions = [
        (h.children == 0) & (h.adults > 0) & (h.seniors == h.adults),
        (h.children == 0) & (h.adults == 1),
        (h.children == 0) & (h.adults == 2),
        (h.children > 0) & (h.adults == 1),
        (h.children > 0) & (h.adults == 2),
    ]
    h["type"] = np.select(
        conditions,
        ["65+ household", "Single", "Couple", "Single parent", "Couple with children"],
        default="Other (3+ adults)",
    )

    # Parts of the change, for the losers table.
    fed_cols = ["income_tax", "flat_tax"] + FEDERAL_PAYROLL
    h["d_ubi"] = r.basic_income - b.basic_income
    h["d_federal_tax"] = -(r[fed_cols].sum(axis=1) - b[fed_cols].sum(axis=1))
    h["d_social_security"] = r.social_security - b.social_security
    ben = [c for c in REMOVABLE_BENEFITS if count_ptc or c != "aca_ptc"]
    h["d_removed_benefits"] = r[ben].sum(axis=1) - b[ben].sum(axis=1)
    h["d_state_tax"] = -(r.household_state_income_tax - b.household_state_income_tax)
    h["d_other"] = h.change - h[["d_ubi", "d_federal_tax", "d_social_security", "d_removed_benefits", "d_state_tax"]].sum(axis=1)

    # Main income source in the baseline.
    earnings = b.employment_income + b.self_employment_income
    sources = pd.DataFrame(
        {
            "earnings": earnings,
            "Social Security": b.social_security,
            "pensions and investments": b.household_market_income - earnings,
            "benefits": b[["ssi", "snap", "tanf", "housing_assistance", "wic", "unemployment_compensation"]].sum(axis=1),
        }
    )
    main = sources.idxmax(axis=1)
    h["main_source"] = np.where(sources.max(axis=1) <= 0, "no income", main)
    h["gets_housing"] = b.housing_assistance > 0
    h["gets_snap"] = b.snap > 0
    h["gets_ssi"] = b.ssi > 0
    h["net_market"] = b.household_market_income
    return h


def _change_bins(rel: pd.Series) -> pd.Series:
    return pd.cut(
        rel,
        [-np.inf, -0.05, -NO_CHANGE, NO_CHANGE, 0.05, np.inf],
        labels=CHANGE_BINS[::-1],
        right=False,
    )


def _shares(df: pd.DataFrame, weight: str) -> pd.Series:
    bins = _change_bins(df.rel_change)
    w = df[weight].groupby(bins, observed=False).sum()
    return (w / w.sum()).reindex(CHANGE_BINS).fillna(0)


def distribution_by(h: pd.DataFrame, key: str, order=None) -> pd.DataFrame:
    rows = []
    for value, g in h.groupby(key, observed=True):
        s = _shares(g, "person_weight")
        rows.append(
            {
                key: value,
                "people_m": g.person_weight.sum() / 1e6,
                "households_m": g.weight.sum() / 1e6,
                "avg_change_per_household": (g.change * g.weight).sum() / g.weight.sum(),
                "pct_change": 100 * (g.change * g.weight).sum() / (g.net_b * g.weight).sum(),
                **{c: 100 * s[c] for c in CHANGE_BINS},
            }
        )
    out = pd.DataFrame(rows)
    if order is not None:
        out = out.set_index(key).reindex([o for o in order if o in set(out[key])]).reset_index()
    return out


def distribution_by_decile(h):
    return distribution_by(h, "decile", order=list(range(1, 11)))


def distribution_by_type(h):
    return distribution_by(h, "type", order=HOUSEHOLD_TYPES)


def person_frame(res: RunResult, h: pd.DataFrame) -> pd.DataFrame:
    p = res.baseline.person[["household_id", "weight", "age"]].copy()
    p["age_group"] = pd.cut(p.age, [a for a, _, _ in AGE_GROUPS] + [200], labels=[l for _, _, l in AGE_GROUPS], right=False)
    p = p.merge(h[["household_id", "change", "rel_change", "net_b", "decile", "size"]], on="household_id", how="left")
    p["poverty_b"] = res.baseline.person.person_in_poverty.to_numpy() > 0
    p["poverty_r"] = res.reform.person.person_in_poverty.to_numpy() > 0
    p["deep_b"] = res.baseline.person.in_deep_poverty.to_numpy() > 0
    p["deep_r"] = res.reform.person.in_deep_poverty.to_numpy() > 0
    return p


def distribution_by_age(p: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for value, g in p.groupby("age_group", observed=True):
        bins = _change_bins(g.rel_change)
        w = g.weight.groupby(bins, observed=False).sum()
        s = (w / w.sum()).reindex(CHANGE_BINS).fillna(0)
        rows.append(
            {
                "age_group": value,
                "people_m": g.weight.sum() / 1e6,
                "avg_household_change": (g.change * g.weight).sum() / g.weight.sum(),
                "pct_change": 100 * (g.change * g.weight).sum() / (g.net_b * g.weight).sum(),
                **{c: 100 * s[c] for c in CHANGE_BINS},
            }
        )
    return pd.DataFrame(rows)


# --------------------------------------------------------------------------
# Poverty and inequality (spec 4.4)
# --------------------------------------------------------------------------


def poverty_table(p: pd.DataFrame) -> pd.DataFrame:
    groups = {
        "All people": p.age >= 0,
        "Children (under 18)": p.age < 18,
        "Adults (18-64)": (p.age >= 18) & (p.age < 65),
        "People 65+": p.age >= 65,
    }
    rows = []
    for name, mask in groups.items():
        g = p[mask]
        w = g.weight.sum()
        rows.append(
            {
                "group": name,
                "poverty_baseline": 100 * (g.weight * g.poverty_b).sum() / w,
                "poverty_reform": 100 * (g.weight * g.poverty_r).sum() / w,
                "deep_poverty_baseline": 100 * (g.weight * g.deep_b).sum() / w,
                "deep_poverty_reform": 100 * (g.weight * g.deep_r).sum() / w,
            }
        )
    df = pd.DataFrame(rows)
    df["poverty_change_pp"] = df.poverty_reform - df.poverty_baseline
    df["deep_poverty_change_pp"] = df.deep_poverty_reform - df.deep_poverty_baseline
    return df


def gini(values, weights) -> float:
    v = np.clip(np.asarray(values, float), 0, None)
    w = np.asarray(weights, float)
    order = np.argsort(v)
    v, w = v[order], w[order]
    cw = np.cumsum(w)
    cvw = np.cumsum(v * w)
    total_w, total_vw = cw[-1], cvw[-1]
    # Area under the Lorenz curve by the trapezoid rule.
    lorenz = cvw / total_vw
    prev = np.concatenate([[0], lorenz[:-1]])
    area = np.sum((lorenz + prev) * w) / (2 * total_w)
    return float(1 - 2 * area)


def inequality_table(h: pd.DataFrame) -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "measure": "Gini, equivalized household net income (person-weighted)",
                "baseline": gini(h.equiv_b, h.person_weight),
                "reform": gini(h.equiv_r, h.person_weight),
            },
            {
                "measure": "Gini, household net income (household-weighted)",
                "baseline": gini(h.net_b, h.weight),
                "reform": gini(h.net_r, h.weight),
            },
        ]
    ).assign(change=lambda d: d.reform - d.baseline)


# --------------------------------------------------------------------------
# Marginal tax rates (spec 4.5)
# --------------------------------------------------------------------------


def mtr_frame(res: RunResult, h: pd.DataFrame) -> pd.DataFrame | None:
    b, r = res.baseline.person, res.reform.person
    if "mtr" not in b or "mtr" not in r:
        return None
    m = pd.DataFrame(
        {
            "household_id": b.household_id,
            "weight": b.weight,
            "earnings": b.employment_income + b.self_employment_income,
            "mtr_b": b.mtr.clip(-1, 1.5),
            "mtr_r": r.mtr.clip(-1, 1.5) + (res.policy.flat_rate - res.meta.get("poverty_at_rate", res.policy.flat_rate)) * (r.flatubi_broad_income > 0),
            "measured": b.get("mtr_measured", pd.Series(True, index=b.index)).astype(bool),
            "ssi_r": r.ssi,
            "medicaid_r": r.medicaid,
        }
    )
    m = m.merge(h[["household_id", "decile"]], on="household_id", how="left")
    rh = res.reform.household.set_index("household_id")
    kept = rh[["snap", "tanf", "wic", "housing_assistance"]].sum(axis=1)
    m["kept_means_tested"] = m.household_id.map(kept).fillna(0).to_numpy() > 0
    m["state_tax"] = m.household_id.map(rh.household_state_income_tax).fillna(0).to_numpy() > 0
    m = m[m.measured & (m.earnings > 0)]
    return m


def mtr_by_decile(m: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for d, g in m.groupby("decile"):
        w = g.weight
        rows.append(
            {
                "decile": d,
                "workers_m": w.sum() / 1e6,
                "mtr_baseline": 100 * (g.mtr_b * w).sum() / w.sum(),
                "mtr_reform": 100 * (g.mtr_r * w).sum() / w.sum(),
            }
        )
    return pd.DataFrame(rows).assign(change_pp=lambda d: d.mtr_reform - d.mtr_baseline)


def mtr_not_flat(m: pd.DataFrame, rate: float, tolerance: float = 0.01) -> pd.DataFrame:
    """Where the reform MTR is not equal to flat_rate, and why."""
    off = (m.mtr_r - rate).abs() > tolerance
    reason = np.select(
        [m.ssi_r > 0, m.kept_means_tested, m.state_tax],
        ["On SSI", "Kept SNAP, TANF, WIC or housing (phase1)", "State income tax only"],
        default="Other",
    )
    df = pd.DataFrame({"reason": np.where(off, reason, "MTR = flat rate"), "weight": m.weight, "mtr_r": m.mtr_r})
    out = df.groupby("reason").apply(
        lambda g: pd.Series(
            {
                "workers_m": g.weight.sum() / 1e6,
                "share_pct": 100 * g.weight.sum() / df.weight.sum(),
                "avg_mtr_reform": 100 * (g.mtr_r * g.weight).sum() / g.weight.sum(),
            }
        ),
        include_groups=False,
    )
    return out.reset_index().sort_values("workers_m", ascending=False)


# --------------------------------------------------------------------------
# Biggest losers (spec 4.6)
# --------------------------------------------------------------------------

QUINTILE_WORDS = {1: "bottom fifth", 2: "second fifth", 3: "middle fifth", 4: "fourth fifth", 5: "top fifth"}
PART_WORDS = {
    "d_ubi": "UBI",
    "d_federal_tax": "federal tax (income + payroll + flat tax)",
    "d_social_security": "Social Security",
    "d_removed_benefits": "SNAP, TANF, WIC, housing, UI and ACA credits",
    "d_state_tax": "state income tax",
    "d_other": "other (SSI and other benefits)",
}
TYPE_WORDS = {
    "Single": "single adults under 65",
    "Couple": "couples without children",
    "Single parent": "single parents",
    "Couple with children": "couples with children",
    "65+ household": "households where all adults are 65+",
    "Other (3+ adults)": "households with 3 or more adults",
}


def biggest_losers(h: pd.DataFrame, n: int = 10, min_people_m: float = 0.5, min_records: int = 30) -> pd.DataFrame:
    keys = ["type", "quintile", "main_source"]
    rows = []
    for (t, q, s), g in h.groupby(keys):
        if len(g) < min_records or g.person_weight.sum() / 1e6 < min_people_m:
            continue
        w = g.weight
        row = {
            "type": t,
            "quintile": q,
            "main_source": s,
            "people_m": g.person_weight.sum() / 1e6,
            "records": len(g),
            "avg_baseline_net": (g.net_b * w).sum() / w.sum(),
            "avg_change": (g.change * w).sum() / w.sum(),
            "pct_change": 100 * (g.change * w).sum() / (g.net_b * w).sum(),
            "share_losing_5pct": 100 * (g.person_weight * (g.rel_change < -0.05)).sum() / g.person_weight.sum(),
            "share_housing": 100 * (w * g.gets_housing).sum() / w.sum(),
            "share_snap": 100 * (w * g.gets_snap).sum() / w.sum(),
        }
        for part in PART_WORDS:
            row[part] = (g[part] * w).sum() / w.sum()
        rows.append(row)
    if not rows:
        return pd.DataFrame(columns=["rank", "type", "quintile", "main_source", "people_m", "avg_change", "pct_change", "description"])
    df = pd.DataFrame(rows).sort_values("pct_change").head(n).reset_index(drop=True)
    df.insert(0, "rank", range(1, len(df) + 1))
    df["description"] = [describe_group(r) for r in df.itertuples()]
    return df


def describe_group(r) -> str:
    parts = {k: getattr(r, k) for k in PART_WORDS}
    losses = sorted([(v, k) for k, v in parts.items() if v < 0])
    gains = sorted([(v, k) for k, v in parts.items() if v > 0], reverse=True)
    loss_txt = ", ".join(f"{PART_WORDS[k]} ${-v:,.0f}" for v, k in losses[:2]) or "none"
    gain_txt = ", ".join(f"{PART_WORDS[k]} +${v:,.0f}" for v, k in gains[:2]) or "none"
    extra = []
    if r.share_housing >= 25:
        extra.append(f"{r.share_housing:.0f}% get housing assistance")
    if r.share_snap >= 25:
        extra.append(f"{r.share_snap:.0f}% get SNAP")
    extra_txt = f" In this group, {' and '.join(extra)} today." if extra else ""
    return (
        f"{TYPE_WORDS.get(r.type, r.type).capitalize()} in the {QUINTILE_WORDS[r.quintile]} of income, "
        f"whose main income is {r.main_source} ({r.people_m:.1f} million people). "
        f"They lose ${-r.avg_change:,.0f} a year on average ({r.pct_change:.1f}% of net income). "
        f"Main losses: {loss_txt}. Main gains: {gain_txt}.{extra_txt}"
    )


# --------------------------------------------------------------------------
# Checks (spec 5.2 and 5.3)
# --------------------------------------------------------------------------


def aggregate_checks(res: RunResult) -> pd.DataFrame:
    published = yaml.safe_load(open(Path(__file__).with_name("published.yaml")))
    pub = published.get(res.policy.year) or published.get(str(res.policy.year)) or {}
    b = res.baseline.household
    p = res.baseline.person
    model = {
        "federal_income_tax": _total(b, "income_tax") / BILLION,
        "payroll_taxes": _total(b, FEDERAL_PAYROLL + EMPLOYER_PAYROLL) / BILLION,
        "social_security": _total(b, "social_security") / BILLION,
        "snap": _total(b, "snap") / BILLION,
        "eitc": _total(b, "eitc") / BILLION,
        "adults": float((p.weight * (p.age >= 18)).sum() / 1e6),
        "children": float((p.weight * (p.age < 18)).sum() / 1e6),
        "spm_poverty_rate": float(100 * (p.weight * (p.person_in_poverty > 0)).sum() / p.weight.sum()),
    }
    rows = []
    for key, value in model.items():
        ref = pub.get(key, {})
        target = ref.get("value")
        gap = (value - target) / target * 100 if target else np.nan
        rows.append(
            {
                "item": key,
                "unit": ref.get("unit", "$ billions"),
                "model": value,
                "published": target,
                "gap_pct": gap,
                "flag": "GAP > 15%" if target and abs(gap) > 15 else "",
                "source": ref.get("source", ""),
            }
        )
    return pd.DataFrame(rows)


def reform_checks(res: RunResult) -> pd.DataFrame:
    p = res.reform.person
    pol = res.policy
    adult = p.age >= pol.min_age_adult
    if pol.ubi_min_age is not None:
        eligible_adults = p.age >= pol.ubi_min_age
    else:
        eligible_adults = adult
    expected = float((p.weight * (eligible_adults * pol.ubi_adult + (~adult) * pol.ubi_child)).sum())
    actual = float((p.weight * p.flatubi_ubi).sum())
    rows = [
        {
            "check": "Total UBI = adults x adult UBI + children x child UBI (within 1%)",
            "expected_billions": expected / BILLION,
            "model_billions": actual / BILLION,
            "gap_pct": 100 * (actual - expected) / expected if expected else 0.0,
        }
    ]
    df = pd.DataFrame(rows)
    note = "pass" if pol.social_security_offset else ("pass" if abs(df.gap_pct.iloc[0]) <= 1 else "FAIL")
    if pol.social_security_offset:
        note = "n/a: phase1 offset cuts the UBI of Social Security beneficiaries"
    df["result"] = note
    return df


def all_tables(res: RunResult) -> dict[str, Any]:
    h = household_frame(res)
    p = person_frame(res, h)
    m = mtr_frame(res, h)
    tables = {
        "budget": budget_table(res),
        "distribution_decile": distribution_by_decile(h),
        "distribution_age": distribution_by_age(p),
        "distribution_type": distribution_by_type(h),
        "poverty": poverty_table(p),
        "inequality": inequality_table(h),
        "losers": biggest_losers(h),
        "aggregate_checks": aggregate_checks(res),
        "reform_checks": reform_checks(res),
    }
    if m is not None:
        tables["mtr_decile"] = mtr_by_decile(m)
        tables["mtr_not_flat"] = mtr_not_flat(m, res.policy.flat_rate)
    tables["_frames"] = {"household": h, "person": p, "mtr": m}
    return tables
