"""Model 3: durability under political turnover (OpenSpiel game).

Solves "python_dpsc_turnover" by backward induction for several political
scenarios and reports:

- which protections the reform government chooses in equilibrium;
- the expected share of the program still running after two elections for
  every package of protections;
- whether protections work as a menu or a package for durability
  (framework.md Section 5);
- how the answer changes for an unfinished insourcing transition, where
  reversal sends work back to vendors on worse terms (framework.md Section 4,
  in-house capacity: pace).
"""

from __future__ import annotations

import argparse

import numpy as np
import pyspiel

from models.common import analysis
from models.common.report import fmt, table, write
from models.common.solvers import backward_induction
from models.turnover import game as tg

SCENARIOS = {
    "Supportive politics": {"continuity": 0.6, "p_low": 0.5, "p_medium": 0.35, "p_high": 0.15},
    "Contested politics": {"continuity": 0.5, "p_low": 0.4, "p_medium": 0.35, "p_high": 0.25},
    "Polarized politics": {"continuity": 0.5, "p_low": 0.15, "p_medium": 0.3, "p_high": 0.55},
    "Polarized, unfinished insourcing": {"continuity": 0.5, "p_low": 0.15, "p_medium": 0.3, "p_high": 0.55,
                                          "reversal_cost": 4.0},
}


def expected_survival(game, package: int) -> tuple[float, float]:
    """Expected program level after two elections and reformer value, when the reformer picks `package`."""
    state = game.new_initial_state()
    state.apply_action(package)
    values, plan = backward_induction(state)

    def level(s):
        if s.is_terminal():
            return s.levels[-1]
        if s.is_chance_node():
            return sum(p * level(s.child(a)) for a, p in s.chance_outcomes())
        return level(s.child(plan[s.history_str()]))

    return level(state), values[0]


def analyse(params: dict) -> dict:
    game = pyspiel.load_game("python_dpsc_turnover", params)
    values, plan = backward_induction(game.new_initial_state())
    survival, value = np.zeros(tg.N_PACKAGES), np.zeros(tg.N_PACKAGES)
    for package in range(tg.N_PACKAGES):
        survival[package], value[package] = expected_survival(game, package)
    return {"choice": plan[""], "values": values, "survival": survival, "value": value}


def build_report(results: dict) -> list[str]:
    lines = [
        "# Model 3: durability under political turnover (OpenSpiel game)",
        "",
        "OpenSpiel game `python_dpsc_turnover`: a reform government chooses protections for its program; two "
        "elections follow; after each, a new government (if power changes hands) with low, medium, or high "
        "hostility chooses to keep, scale back, or dismantle the program. Solved by backward induction over the "
        "full game tree (subgame-perfect equilibrium). All payoff numbers are illustrative assumptions.",
        "",
        "Protections (political cost to the reformer / added cost to a successor of cutting the whole program): "
        + "; ".join(f"**{p}** {tg.PROTECTION_COST[p]} / {tg.DETERRENCE[p]}" for p in tg.PROTECTIONS) + ".",
        "",
        "## 1. Equilibrium protections by political scenario",
        "",
    ]
    rows = []
    for name, r in results.items():
        choice = r["choice"]
        rows.append([name, tg.package_name(choice), 100 * r["survival"][choice], r["values"][0],
                     100 * r["survival"][0], 100 * r["survival"][-1]])
    lines += table(["Scenario", "Equilibrium protections", "Program surviving %", "Reformer value",
                    "Surviving with no protections %", "Surviving with all protections %"], rows,
                   ["---", "---", "---:", "---:", "---:", "---:"])

    lines += ["", "## 2. Survival for every package of protections", "",
              "Expected share of the program still running after two elections.", ""]
    names = list(results)
    rows = [[tg.package_name(m), *[100 * results[n]["survival"][m] for n in names]] for m in range(tg.N_PACKAGES)]
    lines += table(["Protections", *names], rows, ["---"] + ["---:"] * len(names))

    lines += ["", "## 3. Do protections work as a menu or a package?", "",
              "Pairwise relationships between protections for program survival (percentage points), from "
              "interaction effects averaged over the other two protections. Successors cut when their gain "
              "exceeds their cost, so protections act through thresholds: one protection may be useless alone "
              "but decisive together with another. That produces complementarity without any interaction "
              "being assumed.", ""]
    rows = []
    for name, r in results.items():
        f = 100 * (r["survival"] - r["survival"][0])
        for pair in analysis.pairwise(f, len(tg.PROTECTIONS), tg.PROTECTIONS):
            rows.append([name, f"{tg.PROTECTIONS[pair.i]} + {tg.PROTECTIONS[pair.j]}", pair.kind, pair.interaction])
    lines += table(["Scenario", "Pair", "Relationship", "Interaction (points)"], rows, ["---", "---", "---", "---:"])

    lines += ["", "## Caveats", "",
              "- Protections, costs, and hostility levels are stylized. Real successors also face courts, "
              "unions, vendors, and the media.",
              "- Successors are assumed to see the protections and the program's state (perfect information).",
              "- 'Unfinished insourcing' adds a public loss when the program is cut, standing for work returning "
              "to vendors on worse terms; Model 1 Section 7 shows how long transitions take.",
              ""]
    return lines


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--output", default="turnover.md")
    args = parser.parse_args(argv)
    results = {name: analyse(params) for name, params in SCENARIOS.items()}
    path = write(args.output, build_report(results))
    print(f"Wrote {path}")
    return results


if __name__ == "__main__":
    main()
