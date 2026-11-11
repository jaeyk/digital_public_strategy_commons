"""Model 4: scalability through diffusion across many jurisdictions.

Uses OpenSpiel's evolutionary game theory module (open_spiel.python.egt) to
ask whether strategy packages spread to jurisdictions of every type
(framework.md Section 1, "scalable"). There is one population per
jurisdiction type. Each population is a share distribution over five
packages, and shares evolve by Boltzmann Q-learning dynamics
(selection plus exploration):

    status_quo
    informed_buyer        team + procurement + portability
    shared_adopter        policy + portability + platforms + collaboration
    builder               team + insourcing + funding + policy
    pooled_builder        team + insourcing + funding + policy + platforms + collaboration

Fitness of a package for a jurisdiction type =
    its net value under political turnover (from the shared engine, so it reflects capacity and motivation),
    where the value of shared packages is scaled by how available shared platforms are: a jurisdiction
    acting alone gets only a fraction, and availability grows as other jurisdictions adopt them or when a
    higher level of government provides them (a coordination problem)
  - a switching cost that is higher for larger packages and less motivated jurisdictions
  + any support from a higher level of government.

Interventions by a higher level of government compared:
    none
    shared platforms provided   - central provision lowers the cost and effort of shared packages
    conditional funding         - a grant for adopting any reform package
    standards mandate           - a penalty for staying with the status quo
    combined                    - all three
"""

from __future__ import annotations

import argparse

import numpy as np
from open_spiel.python.egt import dynamics

from models.common import engine, levers as lv
from models.common.jurisdictions import JURISDICTIONS
from models.common.report import fmt, table, write

PACKAGES: dict[str, tuple[str, ...]] = {
    "status_quo": (),
    "informed_buyer": ("team", "procurement", "portability"),
    "shared_adopter": ("policy", "portability", "platforms", "collaboration"),
    "builder": ("team", "insourcing", "funding", "policy"),
    "pooled_builder": ("team", "insourcing", "funding", "policy", "platforms", "collaboration"),
}
SHARED = np.array([("platforms" in keys) for keys in PACKAGES.values()], dtype=float)
REFORM = np.array([bool(keys) for keys in PACKAGES.values()], dtype=float)
SIZE = np.array([len(keys) for keys in PACKAGES.values()], dtype=float)

INTERVENTIONS = {
    "none": {},
    "shared platforms provided": {"provision": 1.0, "shared_switch_discount": 0.5},
    "conditional funding": {"grant": 2.0},
    "standards mandate": {"status_quo_penalty": 2.0},
    "combined": {"provision": 1.0, "shared_switch_discount": 0.5, "grant": 2.0, "status_quo_penalty": 2.0},
}
SOLO_SHARE = 0.25      # share of a shared package's value a jurisdiction gets when platforms are unavailable
SWITCH_COST = 1.0      # per lever in the package, scaled by (1.5 - motivation)
TEMPERATURE = 2.0      # higher = noisier, more boundedly rational adoption
STEPS, DT = 4000, 0.02
EARLY_STEP = 40        # snapshot of adoption early on, to show pace


def package_values(args, ai_shock_year=None) -> np.ndarray:
    """Net value of each package (rows: jurisdiction types) under political turnover."""
    portfolios = engine.portfolio_matrix([lv.mask_of(keys) for keys in PACKAGES.values()])
    values = []
    for j in JURISDICTIONS:
        r = engine.simulate(portfolios, j, years=args.years, trials=args.trials, seed=args.seed, turnover=True,
                            ai_shock_year=ai_shock_year)
        v = r.outcome_gain - args.cost_weight * r.spend_share
        values.append(v - v[0])
    return np.array(values)


def availability(state: np.ndarray, intervention: dict) -> float:
    weights = np.array([j.population_share for j in JURISDICTIONS])
    return max(intervention.get("provision", 0.0), float(weights @ (state @ SHARED)))


def realized_values(values: np.ndarray, available: float) -> np.ndarray:
    """Package values once shared platforms are only partly available."""
    scale = SOLO_SHARE + (1 - SOLO_SHARE) * available
    return values * np.where(SHARED > 0, scale, 1.0)


def simulate_diffusion(values: np.ndarray, intervention: dict) -> dict:
    motivation = np.array([j.motivation for j in JURISDICTIONS])
    n_pop, n_pkg = values.shape
    state = np.full((n_pop, n_pkg), 0.02)
    state[:, 0] = 1 - 0.02 * (n_pkg - 1)
    discount = 1 - intervention.get("shared_switch_discount", 0.0) * SHARED
    early = None
    for step in range(STEPS):
        realized = realized_values(values, availability(state, intervention))
        for k in range(n_pop):
            fitness = (realized[k] - SWITCH_COST * SIZE * discount * (1.5 - motivation[k])
                       + intervention.get("grant", 0.0) * REFORM
                       - intervention.get("status_quo_penalty", 0.0) * (1 - REFORM))
            state[k] = state[k] + DT * dynamics.boltzmannq(state[k], fitness, TEMPERATURE)
            state[k] = np.clip(state[k], 1e-9, None)
            state[k] /= state[k].sum()
        if step + 1 == EARLY_STEP:
            early = state.copy()
    available = availability(state, intervention)
    return {"state": state, "early": early, "available": available,
            "realized": realized_values(values, available)}


def build_report(scenarios: dict, args) -> list[str]:
    weights = np.array([j.population_share for j in JURISDICTIONS])
    names = list(PACKAGES)
    lines = [
        "# Model 4: scalability through diffusion",
        "",
        "Four populations of jurisdictions (one per type, weighted by assumed share of all jurisdictions: "
        + ", ".join(f"{j.name} {100 * j.population_share:.0f}%" for j in JURISDICTIONS)
        + ") choose among five strategy packages. Shares evolve by Boltzmann Q-learning dynamics from "
        "`open_spiel.python.egt.dynamics` (temperature "
        f"{TEMPERATURE}, {STEPS} steps of {DT}). Package values come from the shared engine with political "
        f"turnover ({args.years} years, {args.trials} trials). A jurisdiction using a shared package alone gets "
        f"{100 * SOLO_SHARE:.0f}% of its value; the rest depends on how available shared platforms are, through "
        "other jurisdictions' adoption or central provision. Switching costs rise with package size and fall "
        "with motivation. All numbers are illustrative assumptions.",
        "",
        "Packages: " + "; ".join(f"**{k}** = {' + '.join(v) or 'nothing'}" for k, v in PACKAGES.items()) + ".",
        "",
    ]
    for scenario, data in scenarios.items():
        values = data["values"]
        lines += [f"## {scenario}", "", "### Package values by jurisdiction type (net value, before network effects)", ""]
        lines += table(["Jurisdiction", *names], [[j.name, *values[k]] for k, j in enumerate(JURISDICTIONS)],
                       ["---"] + ["---:"] * len(names))
        lines += ["", "### Adoption and value by intervention", "",
                  "Cells show reform adoption (share not on the status quo) early on and in the long run, and the "
                  "most common package in the long run. *Platforms available* is the long-run availability of "
                  "shared platforms. *Expected value* is the share-weighted realized package value (excluding "
                  "grants and penalties), so it measures what jurisdictions get from the packages themselves. "
                  "*Floor* is the lowest expected value across types.", ""]
        rows = []
        for intervention, result in data["states"].items():
            state, early = result["state"], result["early"]
            expected = (state * result["realized"]).sum(axis=1)
            top = [names[int(np.argmax(state[k]))] for k in range(len(JURISDICTIONS))]
            rows.append([intervention, *[f"{100 * (1 - early[k, 0]):.0f}% -> {100 * (1 - state[k, 0]):.0f}% ({top[k]})"
                                         for k in range(len(JURISDICTIONS))],
                         f"{100 * result['available']:.0f}%", float(weights @ expected), float(expected.min())])
        lines += table(["Intervention", *[j.name for j in JURISDICTIONS], "Platforms available",
                        "Weighted expected value", "Floor"], rows,
                       ["---"] + ["---"] * len(JURISDICTIONS) + ["---:", "---:", "---:"])
        lines.append("")
    lines += ["## Caveats", "",
              "- Jurisdictions learn from relative payoffs; real adoption also depends on politics, vendors, and "
              "peer networks not represented here.",
              "- Population shares, switching costs, network gains, and intervention sizes are assumptions.",
              "- Interventions are free to the jurisdictions in this model; their cost to the higher level of "
              "government is not counted.",
              "- Conditional funding and a standards mandate give identical results here by construction: both "
              "widen the payoff gap between reform and the status quo by the same amount. In practice they differ "
              "in who pays and in whether compliance is real or only on paper, which this model does not capture.",
              ""]
    return lines


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--years", type=int, default=16)
    parser.add_argument("--trials", type=int, default=40)
    parser.add_argument("--seed", type=int, default=20261111)
    parser.add_argument("--cost-weight", type=float, default=10.0)
    parser.add_argument("--ai-year", type=int, default=4)
    parser.add_argument("--output", default="diffusion.md")
    args = parser.parse_args(argv)
    scenarios = {}
    for scenario, ai in (("Without the AI shock", None), (f"With the AI shock in year {args.ai_year}", args.ai_year)):
        values = package_values(args, ai)
        scenarios[scenario] = {"values": values,
                               "states": {name: simulate_diffusion(values, spec) for name, spec in INTERVENTIONS.items()}}
    path = write(args.output, build_report(scenarios, args))
    print(f"Wrote {path}")
    return scenarios


if __name__ == "__main__":
    main()
