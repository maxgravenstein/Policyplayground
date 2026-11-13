"""Write CSV tables, charts and the single-file HTML report (spec 4.7)."""

from __future__ import annotations

import base64
import html
import io
import json
from pathlib import Path
from typing import Any

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
import yaml  # noqa: E402

from flatubi.outputs import CHANGE_BINS  # noqa: E402

# Reference palette (dataviz skill): categorical slots 1-2, diverging blue/red.
BLUE, ORANGE = "#2a78d6", "#eb6834"
RED, RED_LIGHT, GRAY, BLUE_LIGHT = "#e34948", "#f2a19f", "#d9d8d3", "#86b6ef"
INK, INK_2, MUTED, AXIS, SURFACE = "#0b0b0b", "#52514e", "#898781", "#c3c2b7", "#fcfcfb"
BIN_COLORS = {
    "Gain more than 5%": BLUE,
    "Gain less than 5%": BLUE_LIGHT,
    "No change": GRAY,
    "Lose less than 5%": RED_LIGHT,
    "Lose more than 5%": RED,
}

LIMITS = [
    ("Static.", "No change in work, saving, or migration, except the rough adjustment of the behavior module (spec 7.4), and only when it is on."),
    ("One year.", "No transition path over many years. (A separate spreadsheet model covers 2027-2070.)"),
    ("Missing income.", "Survey data under-reports high incomes and capital gains. The data have no employer retirement contributions. Inheritances are part of the design but are not in the data: they are excluded."),
    ("Corporate tax", "is an estimate outside the microsimulation: flat_rate x corporate_profit_base. The microsimulation taxes dividends and capital gains in full and does not model the shareholder credit."),
    ("No spending outside taxes and transfers.", "Defense, interest, and other federal functions are not modeled."),
    ("SSI and Medicaid interactions.", "PolicyEngine leaves `basic_income` out of SSI, SNAP and Medicaid income while it is not taxable. So the UBI does not reduce SSI or Medicaid in this model (config: ubi.counts_as_ssi_income). Under current SSI rules, a cash UBI would count as unearned income."),
    ("Employer payroll tax.", "The reform removes it, but by default the saving does not go to workers as higher pay (config: tax.employer_payroll_to_wages)."),
    ("State taxes", "stay at current law. They still use federal AGI and the federal EITC, so they do not change much. Their MTR is in the reform MTR."),
    ("Net income", "is PolicyEngine household net income plus ACA premium tax credits (cash-like). Medicaid, CHIP and Medicare are not in net income."),
]


def limits(res, tables) -> list[tuple[str, str]]:
    """LIMITS plus the items that depend on the data used."""
    meta = res.meta
    out = list(LIMITS)
    label = meta.get("dataset_label") or "Enhanced CPS 2024 (policyengine-us-data tag 1.115.3)"
    data_txt = f"{label}, survey year 2024, aged to {meta.get('year')} by PolicyEngine. Baseline totals differ from published totals; see the checks table."
    if "Enhanced CPS" in label:
        data_txt += " The 'main' copy of the Enhanced CPS on Hugging Face has $9.3T of miscellaneous income and is not used."
    out.append(("Data.", data_txt))
    if res.policy.include_employer_health and not meta.get("employer_health_in_data", True):
        out.append(("Employer health premiums.", "The config puts them in the tax base, but this dataset has no employer health premiums, so they are left out (spec 2.2: 'if the dataset has them'). The base is smaller and the revenue-neutral rate higher than with them."))
    missing = sorted(set(res.baseline.meta.get("not_computed", [])) | set(res.reform.meta.get("not_computed", [])))
    if missing:
        out.append(("Not computed.", f"{', '.join(missing)}: the simulation needed more memory than this machine has. These budget lines are blank and left out of the totals. They are programs kept at current law, so the reform changes them little."))
    checks = tables.get("aggregate_checks")
    if checks is not None and "spm_poverty_rate" in set(checks["item"]):
        gap = float(checks.set_index("item").loc["spm_poverty_rate", "gap_pct"])
        if abs(gap) > 15:
            out.append(("SPM poverty level.", "Baseline SPM poverty on this data is far from the Census rate (see the checks table). The change in poverty between baseline and reform is more reliable than the level."))
    return out


def _fig_to_data_uri(fig) -> str:
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=144, bbox_inches="tight", facecolor=SURFACE)
    plt.close(fig)
    return "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()


def _style(ax):
    ax.set_facecolor(SURFACE)
    for side in ["top", "right"]:
        ax.spines[side].set_visible(False)
    for side in ["left", "bottom"]:
        ax.spines[side].set_color(AXIS)
    ax.tick_params(colors=INK_2, labelsize=9)
    ax.yaxis.grid(True, color="#ecebe7", linewidth=0.8)
    ax.set_axisbelow(True)


def chart_decile_change(df: pd.DataFrame) -> str:
    fig, ax = plt.subplots(figsize=(7, 3.4), facecolor=SURFACE)
    _style(ax)
    colors = [BLUE if v >= 0 else RED for v in df["pct_change"]]
    ax.bar(df.decile.astype(str), df["pct_change"], color=colors, width=0.6, edgecolor=SURFACE, linewidth=2)
    for x, v in zip(df.decile.astype(str), df["pct_change"]):
        ax.annotate(f"{v:+.1f}%", (x, v), ha="center", va="bottom" if v >= 0 else "top", fontsize=8, color=INK_2, xytext=(0, 2 if v >= 0 else -2), textcoords="offset points")
    ax.axhline(0, color=AXIS, linewidth=1)
    ax.set_xlabel("Income decile (equivalized household net income, baseline)", color=INK_2, fontsize=9)
    ax.set_ylabel("Change in net income (%)", color=INK_2, fontsize=9)
    return _fig_to_data_uri(fig)


def chart_shares(df: pd.DataFrame, key: str, label: str) -> str:
    fig, ax = plt.subplots(figsize=(7, 0.42 * len(df) + 1.0), facecolor=SURFACE)
    _style(ax)
    ax.yaxis.grid(False)
    left = np.zeros(len(df))
    y = df[key].astype(str)
    for c in CHANGE_BINS:
        ax.barh(y, df[c], left=left, color=BIN_COLORS[c], edgecolor=SURFACE, linewidth=2, height=0.7, label=c)
        left += df[c].to_numpy()
    ax.invert_yaxis()
    ax.set_xlim(0, 100)
    ax.set_xlabel("Share of people (%)", color=INK_2, fontsize=9)
    ax.set_ylabel(label, color=INK_2, fontsize=9)
    ax.legend(ncol=5, fontsize=7.5, frameon=False, loc="lower center", bbox_to_anchor=(0.5, 1.0), handlelength=1)
    return _fig_to_data_uri(fig)


def chart_two_series(x, a, b, xlabel, ylabel, names=("Baseline", "Reform"), ref=None, kind="bar") -> str:
    fig, ax = plt.subplots(figsize=(7, 3.4), facecolor=SURFACE)
    _style(ax)
    xs = np.arange(len(x))
    if kind == "bar":
        w = 0.38
        ax.bar(xs - w / 2, a, w, color=BLUE, label=names[0], edgecolor=SURFACE, linewidth=2)
        ax.bar(xs + w / 2, b, w, color=ORANGE, label=names[1], edgecolor=SURFACE, linewidth=2)
        ax.set_xticks(xs, [str(v) for v in x])
    else:
        ax.plot(x, a, color=BLUE, linewidth=2, label=names[0], marker="o", markersize=4)
        ax.plot(x, b, color=ORANGE, linewidth=2, label=names[1], marker="o", markersize=4)
        ax.set_xscale("log")
    if ref is not None:
        ax.axhline(ref[0], color=MUTED, linestyle="--", linewidth=1)
        ax.annotate(ref[1], (1.0, ref[0]), xycoords=("axes fraction", "data"), fontsize=8, color=INK_2,
                    xytext=(4, 0), textcoords="offset points", va="center", ha="left")
    ax.set_xlabel(xlabel, color=INK_2, fontsize=9)
    ax.set_ylabel(ylabel, color=INK_2, fontsize=9)
    ax.legend(frameon=False, fontsize=8, ncol=2, loc="lower left", bbox_to_anchor=(0, 1.0))
    return _fig_to_data_uri(fig)


def mtr_curve(m: pd.DataFrame, rate: float) -> str:
    edges = np.geomspace(1000, 1_000_000, 25)
    m = m[(m.earnings >= edges[0]) & (m.earnings < edges[-1])].copy()
    m["bin"] = pd.cut(m.earnings, edges)
    g = m.groupby("bin", observed=True).apply(
        lambda d: pd.Series(
            {
                "x": np.sqrt(d.name.left * d.name.right),
                "b": 100 * (d.mtr_b * d.weight).sum() / d.weight.sum(),
                "r": 100 * (d.mtr_r * d.weight).sum() / d.weight.sum(),
            }
        ),
        include_groups=False,
    )
    return chart_two_series(
        g.x.to_numpy(), g.b.to_numpy(), g.r.to_numpy(),
        "Annual earnings of the worker ($, log scale)", "Average MTR (%)",
        ref=(100 * rate, f"flat rate {100 * rate:.2f}%"), kind="line",
    )


# --------------------------------------------------------------------------


INT_COLUMNS = {"decile", "quintile", "rank", "records"}
HEADER_WORDS = {
    "people_m": "people (m)",
    "households_m": "households (m)",
    "workers_m": "workers (m)",
    "avg_change_per_household": "avg change per household ($)",
    "avg_household_change": "avg household change ($)",
    "avg_change": "avg change ($)",
    "avg_baseline_net": "avg baseline net income ($)",
    "pct_change": "change (%)",
    "gap_pct": "gap (%)",
    "share_pct": "share (%)",
    "share_losing_5pct": "losing >5% (%)",
    "share_housing": "housing (%)",
    "share_snap": "SNAP (%)",
    "d_ubi": "UBI ($)",
    "d_federal_tax": "federal tax ($)",
    "d_social_security": "Social Security ($)",
    "d_removed_benefits": "removed benefits ($)",
    "d_state_tax": "state tax ($)",
    "d_other": "other ($)",
    "change_pp": "change (pp)",
    "poverty_change_pp": "poverty change (pp)",
    "deep_poverty_change_pp": "deep poverty change (pp)",
    "main_source": "main income",
}


def _header(col) -> str:
    col = str(col)
    return HEADER_WORDS.get(col, col.replace("_", " "))


def _fmt_table(df: pd.DataFrame, money: set[str] = frozenset(), pct: set[str] = frozenset(), digits: int = 1) -> str:
    def fmt(col, v):
        if col in INT_COLUMNS and isinstance(v, (int, float, np.number)) and not pd.isna(v):
            return f"{int(v)}"
        if isinstance(v, (float, np.floating)):
            if np.isnan(v):
                return ""
            if col in money:
                return f"{v:,.0f}"
            if col in pct:
                return f"{v:.1f}"
            return f"{v:,.{digits}f}"
        return html.escape(str(v))

    head = "".join(f"<th>{html.escape(_header(c))}</th>" for c in df.columns)
    rows = []
    for _, r in df.iterrows():
        cells = "".join(
            f"<td class='{'num' if isinstance(r[c], (int, float, np.number)) else 'txt'}'>{fmt(c, r[c])}</td>" for c in df.columns
        )
        cls = " class='total'" if str(r.iloc[0]) in ("Total",) or "Net budget" in str(r.get("item", "")) else ""
        rows.append(f"<tr{cls}>{cells}</tr>")
    return f"<div class='tw'><table><thead><tr>{head}</tr></thead><tbody>{''.join(rows)}</tbody></table></div>"


CSS = """
:root{--bg:#f6f5f2;--surface:#fcfcfb;--ink:#0b0b0b;--ink2:#52514e;--muted:#898781;--line:#e4e3de;--accent:#2a78d6;--warn:#b25f00;--card:#ffffff}
@media (prefers-color-scheme: dark){:root:not([data-theme="light"]){--bg:#121211;--surface:#1a1a19;--ink:#f0efec;--ink2:#c3c2b7;--muted:#898781;--line:#383835;--accent:#3987e5;--warn:#e0a040;--card:#1a1a19}}
:root[data-theme="dark"]{--bg:#121211;--surface:#1a1a19;--ink:#f0efec;--ink2:#c3c2b7;--muted:#898781;--line:#383835;--accent:#3987e5;--warn:#e0a040;--card:#1a1a19}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);font:15px/1.5 system-ui,-apple-system,Segoe UI,Roboto,sans-serif}
main{max-width:1040px;margin:0 auto;padding:24px 16px 64px}
h1{font-size:26px;margin:0 0 4px}h2{font-size:19px;margin:36px 0 8px;border-bottom:1px solid var(--line);padding-bottom:4px}
h3{font-size:15px;margin:20px 0 6px}
p.sub{color:var(--ink2);margin:0 0 16px}
.kpis{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:12px;margin:16px 0}
.kpi{background:var(--card);border:1px solid var(--line);border-radius:8px;padding:12px 14px}
.kpi .v{font-size:24px;font-weight:600;font-variant-numeric:tabular-nums}.kpi .l{color:var(--ink2);font-size:13px}
.tw{overflow-x:auto;background:var(--card);border:1px solid var(--line);border-radius:8px;margin:8px 0}
table{border-collapse:collapse;width:100%;font-size:13px;font-variant-numeric:tabular-nums}
th{text-align:left;color:var(--ink2);font-weight:600;padding:6px 8px;border-bottom:1px solid var(--line);white-space:nowrap}
td{padding:5px 8px;border-bottom:1px solid var(--line)}td.num{text-align:right;white-space:nowrap}
tr.total td{font-weight:600}
.chart{background:#fcfcfb;border:1px solid var(--line);border-radius:8px;padding:8px;margin:8px 0}
.chart img{width:100%;max-width:760px;height:auto;display:block;margin:0 auto}
.note{color:var(--ink2);font-size:13px}
.flag{color:var(--warn);font-weight:600}
pre{background:var(--card);border:1px solid var(--line);border-radius:8px;padding:12px;overflow-x:auto;font-size:12px}
ul.limits li{margin:4px 0}
.loser{background:var(--card);border:1px solid var(--line);border-radius:8px;padding:10px 12px;margin:8px 0}
.loser b{font-variant-numeric:tabular-nums}
"""


def write_outputs(res, tables: dict[str, Any], solve, out_dir: Path) -> Path:
    out_dir.mkdir(parents=True, exist_ok=True)
    for name, df in tables.items():
        if isinstance(df, pd.DataFrame):
            df.to_csv(out_dir / f"{name}.csv", index=False)
    summary = {
        "scenario": res.policy.scenario,
        "year": res.policy.year,
        "flat_rate": res.policy.flat_rate,
        "revenue_neutral_rate": solve.rate if solve else None,
        "solver_converged": solve.converged if solve else None,
        "net_budget_billions": float(tables["budget"].set_index("item").loc["Net budget effect (revenue minus spending)", "difference"]),
        "net_transfer_billions": float(tables["budget"].set_index("item").loc["Net transfer: UBI minus flat tax, where positive", "reform"]),
        "meta": res.meta,
    }
    (out_dir / "summary.json").write_text(json.dumps(summary, indent=2, default=str))
    path = out_dir / "report.html"
    path.write_text(render_html(res, tables, solve))
    return path


def render_html(res, tables, solve) -> str:
    pol = res.policy
    b = tables["budget"].set_index("item")
    net = b.loc["Net budget effect (revenue minus spending)", "difference"]
    transfer = b.loc["Net transfer: UBI minus flat tax, where positive", "reform"]
    pov = tables["poverty"].set_index("group")
    behavior = bool(pol.raw.get("behavior", {}).get("enabled", False))
    label = " (with rough behavior adjustment)" if behavior else ""
    scen_txt = {
        "steady_state": "Steady state: UBI for all ages, flat tax, programs removed, " + ("Social Security kept only above the UBI (max of benefit minus UBI, or zero)." if getattr(pol, "social_security_residual", False) else "Social Security removed."),
        "phase1": f"Phase 1: UBI for children and people {pol.ubi_min_age}+, Social Security offset (max of SS and UBI), working-age programs kept, flat tax for all.",
        "custom": "Custom: every switch as set in the config.",
    }[pol.scenario]

    kpis = [
        (f"{net:+,.0f} B", f"Net budget effect at {100 * pol.flat_rate:.2f}%{label}"),
        (f"{solve.rate_pct:.2f}%" if solve and solve.converged else "no solution in 0-100%", "Revenue-neutral flat rate"),
        (f"{transfer:,.0f} B", "Net transfer (UBI minus flat tax, where positive)"),
        (f"{pov.loc['All people', 'poverty_change_pp']:+.1f} pp", f"SPM poverty: {pov.loc['All people', 'poverty_baseline']:.1f}% to {pov.loc['All people', 'poverty_reform']:.1f}%"),
    ]
    kpi_html = "".join(f"<div class='kpi'><div class='v'>{v}</div><div class='l'>{html.escape(l)}</div></div>" for v, l in kpis)

    budget = tables["budget"].rename(columns={"baseline": "baseline ($B)", "reform": "reform ($B)", "difference": "difference ($B)"})
    dd = tables["distribution_decile"]
    da = tables["distribution_age"]
    dt = tables["distribution_type"]
    money = {"avg_change_per_household", "avg_household_change", "avg_change", "avg_baseline_net"}

    parts = [
        f"<h1>Flat Tax + UBI: {html.escape(pol.scenario)}, {pol.year}</h1>",
        f"<p class='sub'>{html.escape(scen_txt)} Static, one-year model: people do not change behavior{' except for the rough adjustment in the behavior module' if behavior else ''}.</p>",
        f"<div class='kpis'>{kpi_html}</div>",
        "<h2>1. Budget</h2>",
        "<p class='note'>Federal budget lines in $ billions per year. Net budget effect = revenue minus spending in the table. Medicaid, CHIP and Medicare are PolicyEngine cost estimates. EITC and CTC are inside the federal income tax line; they are shown as memo lines only.</p>",
        _fmt_table(budget),
        "<h2>2. Revenue-neutral rate</h2>",
    ]
    if solve:
        parts.append(
            f"<p>The flat rate that makes the net budget effect equal <b>{solve.target_billions:,.0f} B</b> is "
            f"<b>{solve.rate_pct:.2f}%</b> ({'converged' if solve.converged else 'NOT converged'}, {solve.steps} bisection steps, "
            f"net budget at that rate {solve.net_budget_billions:+,.1f} B). Each step recomputes the flat tax and the corporate line only.</p>"
        )
    if "distribution_decile_at_solved_rate" in tables:
        parts.append("<h3>Distribution by decile at the revenue-neutral rate</h3>")
        parts.append(_fmt_table(tables["distribution_decile_at_solved_rate"], money=money))
    parts += [
        "<h2>3. Distribution</h2>",
        "<h3>Average change in net income by decile</h3>",
        f"<div class='chart'><img alt='Change in net income by decile' src='{chart_decile_change(dd)}'></div>",
        f"<div class='chart'><img alt='Winners and losers by decile' src='{chart_shares(dd, 'decile', 'Decile')}'></div>",
        _fmt_table(dd, money=money),
        "<h3>By age group</h3>",
        f"<div class='chart'><img alt='Winners and losers by age' src='{chart_shares(da, 'age_group', 'Age group')}'></div>",
        _fmt_table(da, money=money),
        "<h3>By household type</h3>",
        f"<div class='chart'><img alt='Winners and losers by household type' src='{chart_shares(dt, 'type', 'Household type')}'></div>",
        _fmt_table(dt, money=money),
        "<p class='note'>Deciles are by baseline equivalized household net income (net income / sqrt(household size)), with equal numbers of people. Shares are of people, using their household's change. 'No change' = change smaller than 0.1% of net income.</p>",
        "<h2>4. Poverty and inequality</h2>",
    ]
    pt = tables["poverty"]
    parts.append(
        f"<div class='chart'><img alt='SPM poverty' src='{chart_two_series(pt.group.str.replace(' (', chr(10) + '(', regex=False), pt.poverty_baseline, pt.poverty_reform, '', 'SPM poverty rate (%)')}'></div>"
    )
    if res.meta.get("rate_override"):
        parts.append("<p class='flag'>Poverty is at the run rate, not at the override rate.</p>")
    parts += [_fmt_table(pt), _fmt_table(tables["inequality"], digits=4)]

    parts.append("<h2>5. Marginal tax rates</h2>")
    if "mtr_decile" in tables:
        md = tables["mtr_decile"]
        m = tables["_frames"]["mtr"]
        parts += [
            "<p class='note'>Effective MTR on earnings for workers with wages: we rerun the simulation with every worker's wages $1,000 higher, and MTR = 1 - (change in household net income) / (change in household wages). All workers in a household share that MTR. Includes federal, state and payroll taxes and the phase-out of benefits counted in net income. Medicaid is not in net income, so Medicaid cliffs do not show.</p>",
            f"<div class='chart'><img alt='MTR by decile' src='{chart_two_series(md.decile, md.mtr_baseline, md.mtr_reform, 'Income decile', 'Average MTR (%)', ref=(100 * pol.flat_rate, 'flat rate'))}'></div>",
            _fmt_table(md),
            "<h3>MTR curve by earnings</h3>",
            f"<div class='chart'><img alt='MTR curve' src='{mtr_curve(m, pol.flat_rate)}'></div>",
            "<h3>Where the reform MTR is not the flat rate (more than 1 pp away)</h3>",
            _fmt_table(tables["mtr_not_flat"]),
        ]
    else:
        parts.append("<p>MTRs were not computed in this run (--no-mtr).</p>")

    parts.append("<h2>6. Biggest losers</h2>")
    parts.append("<p class='note'>Groups = household type x baseline income fifth x main income source, with at least 0.5 million people and 30 sample households. Ranked by average % change in net income. Amounts are per household per year.</p>")
    for r in tables["losers"].itertuples():
        parts.append(f"<div class='loser'><b>{r.rank}.</b> {html.escape(r.description)}</div>")
    lt = tables["losers"].drop(columns=["description"])
    parts.append(_fmt_table(lt, money=money | {"d_ubi", "d_federal_tax", "d_social_security", "d_removed_benefits", "d_state_tax", "d_other"}))

    parts.append("<h2>7. Checks</h2><h3>Baseline totals against published totals (spec 5.2)</h3>")
    ac = tables["aggregate_checks"]
    parts.append(_fmt_table(ac))
    flagged = ac[ac.flag != ""].item.tolist()
    if flagged:
        parts.append(f"<p class='flag'>Gap above 15%: {', '.join(flagged)}.</p>")
    parts.append("<h3>Reform checks (spec 5.3)</h3>")
    parts.append(_fmt_table(tables["reform_checks"]))

    parts.append("<h2>8. Limits</h2><ul class='limits'>")
    parts += [f"<li><b>{html.escape(a)}</b> {html.escape(t)}</li>" for a, t in limits(res, tables)]
    parts.append("</ul>")

    meta = res.meta
    cfg = {k: v for k, v in pol.raw.items() if not k.startswith("_")}
    parts += [
        "<h2>9. Run details</h2>",
        f"<p class='note'>Packages: {html.escape(', '.join(f'{k} {v}' for k, v in meta.get('versions', {}).items()))}. "
        f"Data: {html.escape(str(meta.get('dataset_label') or meta.get('dataset')))}, file {html.escape(str(meta.get('dataset')))} (revision {html.escape(str(meta.get('data_revision')))}, survey year {meta.get('data_year')}), "
        f"model year {meta.get('year')}. Run time {meta.get('seconds')} s.</p>",
        "<h3>Config used</h3>",
        f"<pre>{html.escape(yaml.safe_dump(cfg, sort_keys=False))}</pre>",
        "<h3>Resolved switches</h3>",
        f"<pre>ubi_min_age: {pol.ubi_min_age}\nprograms_removed: {pol.programs_removed}\nprograms_kept: {pol.programs_kept}\nsocial_security_offset: {pol.social_security_offset}</pre>",
    ]
    body = "\n".join(parts)
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Flat Tax UBI Report</title><style>{CSS}</style></head><body><main>{body}</main></body></html>"""
