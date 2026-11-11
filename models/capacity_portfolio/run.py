"""Model 1: capacity portfolio.

Simulates every combination of the 14 levers in each of the four jurisdiction
types, with and without political turnover, and scores each portfolio on the
three success criteria in framework.md Section 1:

    positive  - net value over the status quo with stable politics, averaged over jurisdiction types
    durable   - net value over the status quo when elections can bring hostile successors
    scalable  - the lowest net value across the four jurisdiction types (the floor)

Net value = outcome gain (points) - cost_weight x extra spending (share of the
jurisdiction's own budget per year, including the lock-in premium on vendor
contracts). The framework's definition of "positive" includes value for money.

It then asks whether levers work as a menu or a package (framework.md Section 5)
for each criterion, compares the results with a menu baseline where every
assumed relationship is switched off, tests whether order of adoption matters,
and checks sensitivity to relationship strengths and random seed.
"""

from __future__ import annotations

import argparse
import dataclasses

import numpy as np

from models.common import analysis, engine, levers as lv
from models.common.jurisdictions import JURISDICTIONS
from models.common.relationships import RELATIONSHIPS
from models.common.report import fmt, table, write

N = len(lv.KEYS)
ALL = analysis.masks(N)
CRITERIA = ("positive", "durable", "scalable")
SEQUENCES = (
    ("team", "procurement"), ("portability", "entrants"), ("maintenance", "open_source"),
    ("policy", "team"), ("authority", "platforms"), ("mandate", "team"), ("team", "insourcing"),
)
INSOURCING_SCENARIOS = (
    ("Informed buyer: team + procurement", ("team", "procurement")),
    ("Insourcing without a core team", ("insourcing",)),
    ("Builder: team + insourcing", ("team", "insourcing")),
    ("Builder with stable funding", ("team", "insourcing", "funding")),
    ("Builder with pooling: + funding, collaboration, platforms", ("team", "insourcing", "funding", "collaboration", "platforms")),
    ("Hybrid: team + procurement + insourcing + funding", ("team", "procurement", "insourcing", "funding")),
)
AI_YEAR = 4


def net_value(result: engine.Result, cost_weight: float) -> np.ndarray:
    """Outcome gain minus weighted extra spending, both relative to the status quo (row 0)."""
    value = result.outcome_gain - cost_weight * result.spend_share
    return value - value[0]


def evaluate(scale: float, years: int, trials: int, seed: int, cost_weight: float,
             ai_shock_year: int | None = None) -> dict:
    portfolios = engine.portfolio_matrix(ALL)
    out = {"positive_by_type": {}, "durable_by_type": {}, "raw_by_type": {}, "cost": [], "outcome": [],
           "survival": [], "lock_in": [], "insourced": []}
    for j in JURISDICTIONS:
        run = dict(years=years, trials=trials, seed=seed, relationship_scale=scale, ai_shock_year=ai_shock_year)
        stable = engine.simulate(portfolios, j, **run)
        turbulent = engine.simulate(portfolios, j, turnover=True, **run)
        out["positive_by_type"][j.key] = net_value(stable, cost_weight)
        out["durable_by_type"][j.key] = net_value(turbulent, cost_weight)
        out["raw_by_type"][j.key] = stable.outcome_gain - cost_weight * stable.spend_share
        out["lock_in"].append(stable.finals["lock_in"])
        out["insourced"].append(stable.finals["insourced"])
        out["cost"].append(stable.spend_share - stable.spend_share[0])
        out["outcome"].append(stable.outcome_gain - stable.outcome_gain[0])
        out["survival"].append(turbulent.survival)
    positive_types = np.array(list(out["positive_by_type"].values()))
    out["positive"] = positive_types.mean(axis=0)
    out["durable"] = np.array(list(out["durable_by_type"].values())).mean(axis=0)
    out["scalable"] = positive_types.min(axis=0)
    out["cost"] = np.mean(out["cost"], axis=0)
    out["outcome"] = np.mean(out["outcome"], axis=0)
    out["lock_in_by_type"] = np.array(out.pop("lock_in"))
    out["insourced_by_type"] = np.array(out.pop("insourced"))
    survival = np.array(out["survival"])
    out["survival"] = np.where(np.isnan(survival).all(axis=0), np.nan,
                               np.nansum(survival, axis=0) / np.maximum((~np.isnan(survival)).sum(axis=0), 1))
    return out


def sequencing(years: int, trials: int, seed: int, cost_weight: float, delay: int = 4) -> list[list]:
    """Does the pair's interaction depend on which lever comes first?

    Comparing raw totals would mostly measure which lever was delayed. Instead,
    the interaction is computed separately for each order, using the same
    delayed single-lever runs, so only the synergy is compared.
    """
    rows = []
    for a, b in SEQUENCES:
        ia, ib = lv.INDEX[a], lv.INDEX[b]
        # rows: none, a@0, b@0, a@delay, b@delay, a@0+b@0, a@0+b@delay, b@0+a@delay
        spec = [(), (a,), (b,), (a,), (b,), (a, b), (a, b), (a, b)]
        portfolios = engine.portfolio_matrix([lv.mask_of(keys) for keys in spec])
        starts = np.zeros(portfolios.shape)
        starts[3, ia] = starts[4, ib] = starts[6, ib] = starts[7, ia] = delay
        values = []
        for j in JURISDICTIONS:
            result = engine.simulate(portfolios, j, years=years, trials=trials, seed=seed, start_years=starts)
            values.append(net_value(result, cost_weight))
        f = np.mean(values, axis=0)
        together = f[5] - f[1] - f[2] + f[0]
        a_first = f[6] - f[1] - f[4] + f[0]
        b_first = f[7] - f[2] - f[3] + f[0]
        rows.append([f"{a} + {b}", together, a_first, b_first, a_first - b_first])
    return rows


def first_year(path: np.ndarray, threshold: float):
    hit = np.flatnonzero(path >= threshold)
    return int(hit[0]) + 1 if hit.size else None


def insourcing_study(args) -> dict:
    """Scope, scale, and pace of in-house delivery (framework.md Section 4, in-house capacity)."""
    masks = [lv.mask_of(keys) for _, keys in INSOURCING_SCENARIOS]
    counterparts = [m & ~lv.mask_of(["insourcing"]) for m in masks]
    portfolios = engine.portfolio_matrix([0, *masks, *counterparts])
    n = len(masks)
    rows, ai_rows = [], []
    for j in JURISDICTIONS:
        for ai_year, target in ((None, rows), (AI_YEAR, ai_rows)):
            run = dict(years=args.years, trials=args.trials, seed=args.seed, ai_shock_year=ai_year)
            stable = engine.simulate(portfolios, j, record_paths=True, **run)
            turbulent = engine.simulate(portfolios, j, turnover=True, **run)
            value_s, value_t = net_value(stable, args.cost_weight), net_value(turbulent, args.cost_weight)
            for k, (label, keys) in enumerate(INSOURCING_SCENARIOS):
                row_index, counterpart = 1 + k, 1 + n + k
                path = stable.paths["insourced"][row_index]
                has_insourcing = "insourcing" in keys
                dip = (stable.paths["outcome"][row_index] - stable.paths["outcome"][counterpart]).min() \
                    if has_insourcing else None
                target.append([j.name, label, 100 * stable.finals["insourced"][row_index],
                               first_year(path, 0.25) or "not reached", first_year(path, 0.50) or "not reached",
                               dip, 100 * (stable.spend_share[row_index] - stable.spend_share[0]),
                               value_s[row_index], value_t[row_index]])

    coverage = []
    pooled = engine.portfolio_matrix([lv.mask_of(INSOURCING_SCENARIOS[4][1])])
    for j in (JURISDICTIONS[0], JURISDICTIONS[2]):
        for pipeline in (1.0, 2.0):
            for ai_year in (None, AI_YEAR):
                unlimited = dataclasses.replace(j, insource_ceiling=1.0, hiring_pipeline=j.hiring_pipeline * pipeline)
                result = engine.simulate(pooled, unlimited, years=30, trials=args.trials, seed=args.seed,
                                         record_paths=True, ai_shock_year=ai_year)
                path = result.paths["insourced"][0]
                coverage.append([j.name, f"{pipeline:.0f}x", "yes" if ai_year is not None else "no",
                                 *[first_year(path, th) or "not in 30 years" for th in (0.5, 0.75, 0.9)],
                                 100 * path[-1]])

    sensitivity = []
    compare = engine.portfolio_matrix([0, lv.mask_of(INSOURCING_SCENARIOS[0][1]), lv.mask_of(INSOURCING_SCENARIOS[4][1])])
    for name, values in (("inhouse_unit_cost", (0.7, 0.85, 1.0, 1.2)), ("transition_speed", (0.04, 0.08, 0.16)),
                         ("hire_rate_max", (0.025, 0.05, 0.10))):
        for value in values:
            gaps = []
            for j in (JURISDICTIONS[0], JURISDICTIONS[2]):
                result = engine.simulate(compare, j, years=args.years, trials=args.trials, seed=args.seed,
                                         params={name: value})
                v = net_value(result, args.cost_weight)
                gaps.append(v[2] - v[1])
            sensitivity.append([name, value, *gaps])
    return {"rows": rows, "ai_rows": ai_rows, "coverage": coverage, "sensitivity": sensitivity}


def encoded_pairs() -> dict[frozenset, str]:
    pairs = {}
    for r in RELATIONSHIPS:
        if len(r.levers) == 2:
            key = frozenset(r.levers)
            pairs[key] = f"{pairs[key]}; {r.kind}" if key in pairs else r.kind
    return pairs


def build_report(full: dict, menu: dict, sensitivity: dict, seed_check: dict, seq_rows, insourcing: dict,
                 ai: dict, args) -> list[str]:
    lines = [
        "# Model 1: capacity portfolio",
        "",
        f"All {len(ALL):,} combinations of {N} levers, {len(JURISDICTIONS)} jurisdiction types, "
        f"{args.years} years, {args.trials} Monte Carlo trials per run, seed {args.seed}.",
        "Scores are net value above the status quo: outcome-index points (0-100 scale) minus "
        f"{fmt(args.cost_weight, 0)} points per 1.0 of extra annual spending as a share of the jurisdiction's own "
        "budget (lever costs plus the lock-in premium on vendor contracts). All parameters are illustrative "
        "assumptions; results show what follows from the stated assumptions, not empirical estimates.",
        "",
        "- **Positive:** net value with stable politics, averaged over the four jurisdiction types.",
        "- **Durable:** the same with elections every four years that can bring a hostile successor.",
        "- **Scalable:** the lowest net value across the four jurisdiction types (stable politics).",
        "",
        "## 1. Best portfolios by criterion",
        "",
    ]
    for criterion in CRITERIA:
        f = full[criterion]
        order = np.argsort(f)[::-1][:5]
        lines += [f"### {criterion.capitalize()}", ""]
        rows = [[rank + 1, lv.label(int(m)), full["positive"][m], full["durable"][m], full["scalable"][m],
                 full["outcome"][m], 100 * full["cost"][m], 100 * full["survival"][m]]
                for rank, m in enumerate(order)]
        lines += table(["Rank", "Portfolio", "Positive", "Durable", "Scalable", "Outcome gain",
                        "Extra spend % of budget", "Levers surviving turnover %"], rows,
                       ["---:", "---", "---:", "---:", "---:", "---:", "---:", "---:"])
        minimal = analysis.minimal_package(f, N)
        lines += ["", f"Smallest portfolio reaching 90% of the best {criterion} score: **{lv.label(minimal)}** "
                      f"({fmt(f[minimal])} vs. {fmt(f.max())}).", ""]

    lines += ["## 2. Best portfolio for each jurisdiction type", ""]
    rows = []
    for j in JURISDICTIONS:
        for criterion in ("positive", "durable"):
            f = full[f"{criterion}_by_type"][j.key]
            best, minimal = int(np.argmax(f)), analysis.minimal_package(f, N)
            rows.append([j.name, criterion, lv.label(best), f[best], lv.label(minimal), f[minimal]])
    lines += table(["Jurisdiction", "Criterion", "Best portfolio", "Gain", "Smallest at 90%", "Gain"], rows,
                   ["---", "---", "---", "---:", "---", "---:"])

    lines += ["", "## 3. Lever profiles: does each lever work alone?", "",
              "*Alone* is the lever's effect when adopted by itself. *In combination* is its effect averaged over "
              "every combination of the other levers. A large gap means the lever's value depends on what it is "
              "combined with (package-like); a small gap means it works the same on any menu.", ""]
    alone_p, avg_p = analysis.standalone(full["positive"], N), analysis.average_marginal(full["positive"], N)
    alone_d, avg_d = analysis.standalone(full["durable"], N), analysis.average_marginal(full["durable"], N)
    avg_s = analysis.average_marginal(full["scalable"], N)
    rows = [[lever.name, ", ".join(lever.framework_ids), lever.annual_cost, alone_p[i], avg_p[i], alone_d[i],
             avg_d[i], avg_s[i]] for i, lever in enumerate(lv.LEVERS)]
    lines += table(["Lever", "Framework", "Cost", "Positive: alone", "Positive: in combination",
                    "Durable: alone", "Durable: in combination", "Scalable: in combination"], rows,
                   ["---", "---", "---:", "---:", "---:", "---:", "---:", "---:"])

    lines += ["", "## 4. Menu or package?", "",
              "Share of each top portfolio's gain that comes from combining levers rather than from each lever "
              "alone. 0% would be a pure menu. The menu baseline switches off every assumed relationship in "
              "`models/common/relationships.py`; what remains comes from the model's structure (budget limits, "
              "saturation of 0-1 indices, and causal chains such as talent -> procurement leverage).", ""]
    rows = []
    for criterion in CRITERIA:
        best_full, best_menu = int(np.argmax(full[criterion])), int(np.argmax(menu[criterion]))
        rows.append([criterion, lv.label(best_full), 100 * analysis.package_share(full[criterion], best_full, N),
                     lv.label(best_menu), 100 * analysis.package_share(menu[criterion], best_menu, N)])
    lines += table(["Criterion", "Best (assumed relationships)", "Package share %", "Best (menu baseline)",
                    "Package share %"], rows, ["---", "---", "---:", "---", "---:"])

    lines += ["", "### Pairwise relationships", "",
              "Each pair is classified with the definitions in framework.md Section 5, from interaction effects "
              "averaged over all combinations of the other 13 levers. *Hypothesis* is the relationship assumed "
              "in the code (blank = none assumed, so any non-additive result emerged from the model's structure). "
              "*Contexts +* is the share of contexts in which the interaction is positive; values far from 0% "
              "or 100% mean the relationship depends on context. Additive pairs with no hypothesis are omitted.", ""]
    hypotheses = encoded_pairs()
    pair_sets = {c: analysis.pairwise(full[c], N, lv.KEYS) for c in CRITERIA}
    menu_pairs = analysis.pairwise(menu["positive"], N, lv.KEYS)
    rows = []
    for index, pair in enumerate(pair_sets["positive"]):
        names = frozenset((lv.KEYS[pair.i], lv.KEYS[pair.j]))
        kinds = [pair_sets[c][index].kind for c in CRITERIA]
        if names not in hypotheses and all(k == "additive" for k in kinds):
            continue
        rows.append((max(abs(pair_sets[c][index].interaction) for c in CRITERIA), [
            f"{lv.KEYS[pair.i]} + {lv.KEYS[pair.j]}", hypotheses.get(names, ""),
            *[f"{pair_sets[c][index].kind} ({fmt(pair_sets[c][index].interaction)})" for c in CRITERIA],
            f"{100 * pair.share_positive:.0f}%", menu_pairs[index].kind]))
    rows = [row for _, row in sorted(rows, key=lambda r: r[0], reverse=True)]
    lines += table(["Pair", "Hypothesis", "Positive", "Durable", "Scalable", "Contexts +", "Menu baseline"], rows)

    lines += ["", "### Strongest three-way interactions (positive and durable)", "",
              "What a trio adds beyond its pairs. Pairwise tests miss these.", ""]
    rows = []
    for criterion in ("positive", "durable"):
        for value, i, j, k in analysis.triples(full[criterion], N)[:5]:
            rows.append([criterion, f"{lv.KEYS[i]} + {lv.KEYS[j]} + {lv.KEYS[k]}", value])
    lines += table(["Criterion", "Trio", "Three-way interaction"], rows, ["---", "---", "---:"])

    lines += ["", "## 5. Does order matter?", "",
              "Interaction (positive criterion, averaged over jurisdiction types) when both levers start "
              "together, and when one starts four years before the other. Each interaction is measured against "
              "single-lever runs with the same timing, so the comparison isolates the synergy rather than the "
              "cost of delaying a bigger lever. *Order effect* is (first listed first) minus (second listed "
              "first); a positive value means the first listed lever should come first.", ""]
    lines += table(["Pair", "Interaction: together", "First listed first", "Second listed first", "Order effect"],
                   seq_rows, ["---", "---:", "---:", "---:", "---:"])

    lines += ["", "## 6. Sensitivity", "",
              "Relationship strengths scaled from 0 (menu baseline) to 1.5x. *Pairs unchanged* is the share of "
              "the 105 pairs whose positive-criterion classification matches the 1.0x run.", ""]
    base_kinds = [p.kind for p in pair_sets["positive"]]
    rows = []
    for scale, result in sorted(sensitivity.items()):
        kinds = [p.kind for p in analysis.pairwise(result["positive"], N, lv.KEYS)]
        for criterion in CRITERIA:
            best = int(np.argmax(result[criterion]))
            rows.append([f"{scale}x", criterion, lv.label(best), result[criterion][best],
                         100 * analysis.package_share(result[criterion], best, N),
                         f"{100 * np.mean([a == b for a, b in zip(kinds, base_kinds)]):.0f}%"])
    lines += table(["Strength", "Criterion", "Best portfolio", "Score", "Package share %", "Pairs unchanged"], rows,
                   ["---", "---", "---", "---:", "---:", "---:"])
    lines += ["", f"Seed check (seed {args.seed + 1}): overlap of the top 10 portfolios with the main run: " + ", ".join(
        f"{c} {len(set(np.argsort(full[c])[::-1][:10]) & set(np.argsort(seed_check[c])[::-1][:10])) * 10}%"
        for c in CRITERIA) + "."]

    lines += insourcing_section(insourcing, args)
    lines += ai_section(full, ai, args)

    lines += ["", "## Caveats", "",
              "- Every parameter, relationship strength, and jurisdiction profile is an assumption to be "
              "calibrated with evidence and practitioner input. The model shows the consequences of these "
              "assumptions; it cannot confirm them.",
              "- Relationships labeled with a hypothesis were put in deliberately. Non-additive results without "
              "a hypothesis come from structure, mainly the budget limit (which makes costly levers substitutes "
              "in small jurisdictions) and causal chains between state variables.",
              "- Levers group several framework strategies (see `models/common/levers.py`), so effects within a "
              "group, such as fellowships versus permanent teams, cannot be separated.",
              "- Vendor behavior is fixed at 'lock-in' here. Model 2 lets the vendor respond strategically.",
              "- In-house scope ceilings, hiring capacity, transition speed, and in-house unit cost are assumptions "
              "with large effects; Section 7 shows how results move with them.",
              "- The AI shock is one stylized scenario (timing, strength, and how capacity absorbs it are all "
              "assumptions), not a forecast.",
              "- Turnover is a reduced-form rule. Model 3 treats the successor's decision as a strategic choice.",
              ""]
    return lines


def insourcing_section(study: dict, args) -> list[str]:
    headers = ["Jurisdiction", "Approach", "Work in-house at end %", "Years to 25%", "Years to 50%",
               "Worst transition dip", "Extra spend % of budget", "Net value (stable)", "Net value (turnover)"]
    align = ["---", "---", "---:", "---:", "---:", "---:", "---:", "---:", "---:"]
    lines = ["", "## 7. In-house delivery: scope, scale, and pace", "",
             "framework.md Section 4 asks whether an in-house team could cover everything vendors do (scope), "
             "whether it can grow large enough (scale), and whether it can do so fast enough (pace). In the "
             "engine, in-house staff capacity grows only as fast as hiring allows, shrinks with attrition, and is "
             "paid for before work moves; work moves in-house only as fast as experienced staff can manage, and "
             "each move dents service quality in proportion to inexperience. Each jurisdiction type has a ceiling "
             "on the share of vendor work it could realistically run (well-resourced 60%, small 35%), which "
             "pooling and shared platforms can raise.",
             "",
             "*Worst transition dip* is the lowest yearly outcome of the approach minus the same portfolio without "
             "insourcing (negative = service disruption during the transition).", ""]
    lines += table(headers, study["rows"], align)
    lines += ["", "### Could it cover everything, and how fast?", "",
              "The pooled builder approach with the scope ceiling removed (100% of vendor work allowed), run for "
              "30 years, with normal and doubled hiring capacity, and with and without the AI shock.", ""]
    lines += table(["Jurisdiction", "Hiring capacity", "AI shock", "Years to 50%", "Years to 75%", "Years to 90%",
                    "In-house after 30 years %"], study["coverage"], ["---", "---", "---", "---:", "---:", "---:", "---:"])
    lines += ["", "### Sensitivity: when does building beat buying well?", "",
              "Net value of the pooled builder approach minus the informed-buyer approach, as one assumption "
              "varies. Positive values favor building in-house.", ""]
    lines += table(["Assumption", "Value", "Well-resourced and committed", "Small and committed"],
                   study["sensitivity"], ["---", "---:", "---:", "---:"])
    return lines


def ai_section(full: dict, ai: dict, args) -> list[str]:
    lines = ["", f"## 8. The AI shock", "",
             f"AI arrives in year {AI_YEAR} and ramps up over about two years. The share the government absorbs "
             "with its own capacity (talent, portability, shared infrastructure, insourced work) raises "
             "productivity, quality, reach, and the in-house scope ceiling. The rest arrives through vendors: "
             "some quality gain, but more lock-in, market concentration, and AI contract spending, reduced by "
             "strategic procurement. Without safeguards, AI also erodes legitimacy. *AI effect* is net value with "
             "the shock minus net value without it, for the same portfolio.", ""]
    rows = []
    for index, j in enumerate(JURISDICTIONS):
        effect = ai["raw_by_type"][j.key] - full["raw_by_type"][j.key]
        best_ai = int(np.argmax(ai["positive_by_type"][j.key]))
        rows.append([j.name, effect[0], 100 * ai["lock_in_by_type"][index][0],
                     100 * full["lock_in_by_type"][index][0], effect[best_ai], lv.label(best_ai)])
    lines += table(["Jurisdiction", "AI effect on status quo", "Lock-in at end with AI %",
                    "Lock-in at end without AI %", "AI effect on best AI-era portfolio", "Best AI-era portfolio"],
                   rows, ["---", "---:", "---:", "---:", "---:", "---"])
    lines += ["", "### Which levers matter more once AI arrives?", "",
              "Average effect of adding each lever (positive criterion), with and without the AI shock.", ""]
    with_ai, without = analysis.average_marginal(ai["positive"], N), analysis.average_marginal(full["positive"], N)
    order = np.argsort(with_ai - without)[::-1]
    lines += table(["Lever", "Without AI", "With AI", "Change"],
                   [[lv.LEVERS[i].name, without[i], with_ai[i], with_ai[i] - without[i]] for i in order],
                   ["---", "---:", "---:", "---:"])
    gap = lambda r: max(r["positive_by_type"][j.key].max() for j in JURISDICTIONS) - \
        min(r["positive_by_type"][j.key].max() for j in JURISDICTIONS)
    lines += ["", "### Does AI widen or narrow the gap between jurisdictions?", "",
              f"Gap between the best achievable net value in the strongest and weakest jurisdiction type: "
              f"{fmt(gap(full))} without AI, {fmt(gap(ai))} with AI. Scalable floor (best lowest-type value): "
              f"{fmt(full['scalable'].max())} without AI, {fmt(ai['scalable'].max())} with AI. Status quo outcome "
              "change from AI by type: " + ", ".join(
                  f"{j.name} {fmt(ai['raw_by_type'][j.key][0] - full['raw_by_type'][j.key][0])}" for j in JURISDICTIONS)
              + "."]
    return lines


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--years", type=int, default=16)
    parser.add_argument("--trials", type=int, default=40)
    parser.add_argument("--seed", type=int, default=20261111)
    parser.add_argument("--cost-weight", type=float, default=10.0,
                        help="outcome points per 1.0 of extra annual spending (share of own budget)")
    parser.add_argument("--output", default="capacity_portfolio.md")
    args = parser.parse_args(argv)

    run = dict(years=args.years, trials=args.trials, cost_weight=args.cost_weight)
    full = evaluate(1.0, seed=args.seed, **run)
    sensitivity = {scale: evaluate(scale, seed=args.seed, **run) for scale in (0.0, 0.5, 1.5)}
    sensitivity[1.0] = full
    seed_check = evaluate(1.0, seed=args.seed + 1, **run)
    seq_rows = sequencing(args.years, args.trials, args.seed, args.cost_weight)
    insourcing = insourcing_study(args)
    ai = evaluate(1.0, seed=args.seed, ai_shock_year=AI_YEAR, **run)
    path = write(args.output, build_report(full, sensitivity[0.0], sensitivity, seed_check, seq_rows, insourcing,
                                           ai, args))
    print(f"Wrote {path}")
    return full


if __name__ == "__main__":
    main()
