"""Model 2: vendor capture as an OpenSpiel game.

For each jurisdiction type, loads "python_dpsc_vendor_capture" from OpenSpiel
and computes:

- the subgame-perfect equilibrium (government commits, vendor responds), by
  backward induction over the OpenSpiel game tree;
- pure-strategy Nash equilibria of the simultaneous-move version, built with
  pyspiel.create_matrix_game, to measure the value of commitment;
- the cost of assuming the vendor never changes behavior (Model 1's assumption);
- whether the market levers act as a menu or a package once the vendor
  responds strategically (framework.md Section 5);
- how an AI shock shifts power between government and vendor (framework.md Section 3).
"""

from __future__ import annotations

import argparse

import numpy as np
import pyspiel

from models.common import analysis, levers as lv
from models.common.jurisdictions import JURISDICTIONS
from models.common.report import fmt, table, write
from models.common.solvers import backward_induction, pure_nash
from models.vendor_capture import game as vc

N = len(vc.KEYS)


def name(mask: int) -> str:
    return lv.label(int(mask), vc.KEYS)


def solve(jurisdiction: str, args, ai_shock_year: int = -1) -> dict:
    params = {"jurisdiction": jurisdiction, "years": args.years, "trials": args.trials, "seed": args.seed,
              "cost_weight": args.cost_weight, "ai_shock_year": ai_shock_year}
    game = pyspiel.load_game("python_dpsc_vendor_capture", params)
    values, plan = backward_induction(game.new_initial_state())
    portfolio = plan[""]
    state = game.new_initial_state()
    state.apply_action(portfolio)
    response = plan[state.history_str()]

    government, vendor = game.government_payoffs, game.vendor_payoffs
    best_response = np.array([plan[f"{m}"] for m in range(vc.N_PORTFOLIOS)])
    strategic = government[np.arange(vc.N_PORTFOLIOS), best_response]

    matrix_game = pyspiel.create_matrix_game(
        "dpsc_vendor_capture_simultaneous", "Simultaneous-move vendor capture",
        [name(m) for m in range(vc.N_PORTFOLIOS)], list(vc.VENDOR_ACTIONS), government.tolist(), vendor.tolist())
    row = np.array([[matrix_game.player_utility(0, i, j) for j in range(len(vc.VENDOR_ACTIONS))]
                    for i in range(vc.N_PORTFOLIOS)])
    col = np.array([[matrix_game.player_utility(1, i, j) for j in range(len(vc.VENDOR_ACTIONS))]
                    for i in range(vc.N_PORTFOLIOS)])
    nash = pure_nash(row, col)

    naive = int(np.argmax(government[:, 0]))
    return {
        "values": values, "portfolio": portfolio, "response": response, "best_response": best_response,
        "strategic": strategic, "fixed": government[:, 0], "nash": nash, "government": government,
        "vendor": vendor, "naive": naive,
    }


def build_report(results: dict, ai_results: dict, args) -> list[str]:
    lines = [
        "# Model 2: vendor capture (OpenSpiel game)",
        "",
        f"OpenSpiel game `python_dpsc_vendor_capture`: the government commits to one of {vc.N_PORTFOLIOS} "
        f"portfolios of {N} market-facing levers ({', '.join(vc.KEYS)}); the incumbent vendor sees it and "
        f"chooses {', '.join(vc.VENDOR_ACTIONS)}. Payoffs come from the shared capacity engine "
        f"({args.years} years, {args.trials} trials, seed {args.seed}). Government payoff is net value against "
        "the status quo with a lock-in vendor (outcome points minus "
        f"{fmt(args.cost_weight, 0)} x extra spending as a share of budget). Vendor payoff is contract revenue, "
        "which rises with lock-in and quality, falls with competition, and shrinks when the vendor loses "
        "contracts at renewal to a government with leverage.",
        "",
        "Vendor responses:",
        "",
        "- **lock_in:** entrench, so lock-in grows; service quality slips slightly.",
        "- **adapt:** invest in quality and openness; lock-in falls; lower risk of losing the contract at renewal.",
        "- **lowball:** low prices and low lock-in early, then raise lock-in after the first renewal.",
        "- **acquire_entrants:** buy up new competitors, unless portability makes switching easy.",
        "",
        "## 1. Equilibrium by jurisdiction type",
        "",
        "*Equilibrium* is the subgame-perfect equilibrium from backward induction over the OpenSpiel game tree. "
        "*If vendor assumed fixed* is the portfolio that is best when the vendor is assumed always to lock in "
        "(Model 1's assumption), and what the government actually gets once the vendor responds to it.",
        "",
    ]
    rows = []
    for j in JURISDICTIONS:
        r = results[j.key]
        naive = r["naive"]
        rows.append([j.name, name(r["portfolio"]), vc.VENDOR_ACTIONS[r["response"]], r["values"][0], r["values"][1],
                     name(naive), vc.VENDOR_ACTIONS[r["best_response"][naive]], r["strategic"][naive]])
    lines += table(["Jurisdiction", "Equilibrium portfolio", "Vendor response", "Government", "Vendor",
                    "If vendor assumed fixed", "Actual response", "Government gets"], rows,
                   ["---", "---", "---", "---:", "---:", "---", "---", "---:"])

    lines += ["", "## 2. Value of commitment", "",
              "Pure-strategy Nash equilibria of the simultaneous-move version (pyspiel.create_matrix_game), "
              "where the government cannot commit before the vendor acts. *Value of commitment* is the "
              "equilibrium government payoff above the best simultaneous-move equilibrium.", ""]
    rows = []
    for j in JURISDICTIONS:
        r = results[j.key]
        if r["nash"]:
            best = max(r["nash"], key=lambda cell: r["government"][cell])
            rows.append([j.name, len(r["nash"]), name(best[0]), vc.VENDOR_ACTIONS[best[1]],
                         r["government"][best], r["values"][0] - r["government"][best]])
        else:
            rows.append([j.name, 0, "none in pure strategies", "", None, None])
    lines += table(["Jurisdiction", "Pure equilibria", "Best for government", "Vendor", "Government",
                    "Value of commitment"], rows, ["---", "---:", "---", "---", "---:", "---:"])

    lines += ["", "## 3. Which portfolios make the vendor adapt?", "",
              f"Number of the {vc.N_PORTFOLIOS} portfolios that lead to each vendor response, and the smallest portfolios that "
              "lead the vendor to adapt.", ""]
    rows = []
    for j in JURISDICTIONS:
        r = results[j.key]
        counts = [int(np.sum(r["best_response"] == a)) for a in range(len(vc.VENDOR_ACTIONS))]
        adapting = [m for m in range(vc.N_PORTFOLIOS) if r["best_response"][m] == vc.VENDOR_ACTIONS.index("adapt")]
        smallest = sorted(adapting, key=lambda m: (bin(m).count("1"), -r["strategic"][m]))[:3]
        rows.append([j.name, *counts, "; ".join(name(m) for m in smallest) or "none"])
    lines += table(["Jurisdiction", *vc.VENDOR_ACTIONS, "Smallest portfolios inducing adapt"], rows,
                   ["---", "---:", "---:", "---:", "---:", "---"])

    lines += ["", "## 4. Menu or package, once the vendor responds", "",
              "Pairwise relationships among the market levers, averaged over the other five levers, when the "
              "vendor is held at lock-in versus when it responds strategically. Strategic response can create "
              "complementarity: a vendor may adapt only when the government holds several levers at once.", ""]
    for j in JURISDICTIONS:
        r = results[j.key]
        fixed = analysis.pairwise(r["fixed"] - r["fixed"][0], N, vc.KEYS)
        strategic = analysis.pairwise(r["strategic"] - r["strategic"][0], N, vc.KEYS)
        rows = [[f"{vc.KEYS[a.i]} + {vc.KEYS[a.j]}", f"{a.kind} ({fmt(a.interaction)})",
                 f"{b.kind} ({fmt(b.interaction)})"]
                for a, b in zip(fixed, strategic) if a.kind != "additive" or b.kind != "additive"]
        lines += [f"### {j.name}", ""]
        lines += table(["Pair", "Vendor fixed at lock-in", "Vendor responds"], rows) if rows else \
            ["All pairs additive under both assumptions."]
        lines.append("")

    lines += ["## 5. The AI shock and vendor power", "",
              f"The same game with an AI shock in year {args.ai_year}. Payoffs for both games are measured "
              "against the same no-AI status quo, so they can be compared directly. *Vendor at status quo* shows "
              "how much AI strengthens the incumbent when the government does nothing (the dependency path).", ""]
    rows = []
    for j in JURISDICTIONS:
        base, ai = results[j.key], ai_results[j.key]
        rows.append([j.name, base["vendor"][0].max(), ai["vendor"][0].max(),
                     name(base["portfolio"]), vc.VENDOR_ACTIONS[base["response"]], base["values"][0],
                     name(ai["portfolio"]), vc.VENDOR_ACTIONS[ai["response"]], ai["values"][0]])
    lines += table(["Jurisdiction", "Vendor at status quo, no AI", "Vendor at status quo, AI",
                    "Equilibrium, no AI", "Response", "Government", "Equilibrium, AI", "Response", "Government"],
                   rows, ["---", "---:", "---:", "---", "---", "---:", "---", "---", "---:"])
    lines += ["", "Government payoff of each lever's best portfolio with and without the lever, under AI "
              "(equilibrium vendor response): how much the government loses in the AI era by giving up each lever.", ""]
    rows = []
    for j in JURISDICTIONS:
        strategic = ai_results[j.key]["strategic"]
        best = strategic.max()
        losses = []
        for bit, key in enumerate(vc.KEYS):
            without = max(strategic[m] for m in range(vc.N_PORTFOLIOS) if not m >> bit & 1)
            losses.append(best - without)
        rows.append([j.name, *losses])
    lines += table(["Jurisdiction", *vc.KEYS], rows, ["---"] + ["---:"] * N)
    lines.append("")

    lines += ["## Caveats", "",
              "- The vendor is a single incumbent with four stylized responses; real markets have several "
              "vendors, and responses can change over the contract.",
              "- Payoffs are Monte Carlo averages from the shared engine, so the game inherits its assumptions.",
              "- Ties in the equilibrium are broken toward the lowest action id (status quo for the government, "
              "lock-in for the vendor).",
              "- Mixed-strategy equilibria of the simultaneous game are not computed (OpenSpiel's solvers for "
              "these need the optional nashpy or lrsnash packages).",
              ""]
    return lines


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--years", type=int, default=16)
    parser.add_argument("--trials", type=int, default=30)
    parser.add_argument("--seed", type=int, default=20261111)
    parser.add_argument("--cost-weight", type=float, default=10.0)
    parser.add_argument("--ai-year", type=int, default=4)
    parser.add_argument("--output", default="vendor_capture.md")
    args = parser.parse_args(argv)
    results = {j.key: solve(j.key, args) for j in JURISDICTIONS}
    ai_results = {j.key: solve(j.key, args, args.ai_year) for j in JURISDICTIONS}
    path = write(args.output, build_report(results, ai_results, args))
    print(f"Wrote {path}")
    return results


if __name__ == "__main__":
    main()
