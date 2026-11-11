"""Repeated digital public infrastructure strategy game."""

from __future__ import annotations

import argparse
import itertools
import random
from dataclasses import dataclass

import pyspiel


POLICIES = ("team", "procurement", "open_source", "startups")
VENDOR_ACTIONS = ("lock_in", "adapt")
POLICY_COSTS = {
    "team": 0.08,
    "procurement": 0.04,
    "open_source": 0.06,
    "startups": 0.08,
}
YEARS = 12
TRIALS = 500
SEED = 20261111


@dataclass(frozen=True)
class Outcome:
    public_payoff: float
    incumbent_payoff: float
    control: float
    service_quality: float
    competition: float
    portability: float
    vendor_lock_in: float
    annual_cost: float


def portfolio_name(policies: frozenset[str]) -> str:
    return "+".join(policy for policy in POLICIES if policy in policies) or "status_quo"


def simulate_trial(
    policies: frozenset[str], vendor_action: str, rng: random.Random, years: int
) -> Outcome:
    """Simulate one agency-vendor relationship; state variables are normalized to 0..1."""
    capacity = 0.15
    portability = 0.10
    competition = 0.12
    lock_in = 0.72
    quality = 0.62
    yearly = []

    for year in range(years):
        if "team" in policies:
            capacity += 0.11 * (1 - capacity)
        else:
            capacity += 0.012 * (1 - capacity)

        if "open_source" in policies:
            portability += (0.08 + 0.10 * capacity) * (1 - portability)
        else:
            portability += 0.008 * (1 - portability)

        if "startups" in policies and year >= 2:
            entry_chance = min(
                0.85,
                0.05 + 0.42 * portability + 0.18 * capacity
                + (0.14 if "procurement" in policies else 0),
            )
            if rng.random() < entry_chance:
                competition += 0.075 * (1 - competition)
        else:
            competition += 0.003 * (1 - competition)

        leverage = 0.08 + 0.16 * capacity
        if "procurement" in policies:
            leverage += 0.25 + 0.15 * portability + 0.10 * competition

        if year in (3, 7, 10):
            lock_in -= leverage * (0.11 + 0.10 * portability)
        if vendor_action == "lock_in":
            lock_in += 0.032 * (1 - lock_in)
        else:
            lock_in -= (0.018 + 0.018 * portability) * lock_in
        lock_in = min(0.98, max(0.03, lock_in))

        quality += (
            0.025 * capacity
            + (0.012 if vendor_action == "adapt" else -0.006)
            + 0.012 * competition
            - 0.010 * lock_in
            + rng.gauss(0, 0.008)
        )
        quality = min(0.98, max(0.25, quality))

        control = 0.25 * (
            capacity + portability + competition + (1 - lock_in)
        )
        yearly.append((control, quality, competition, portability, lock_in, leverage))

    means = [sum(row[index] for row in yearly) / years for index in range(6)]
    control, quality, competition, portability, lock_in, leverage = means
    policy_cost = sum(POLICY_COSTS[policy] for policy in policies)
    transaction_cost = 0.04
    cooperative_saving = 0.015
    annual_cost = transaction_cost + policy_cost - cooperative_saving

    # Cooperative purchasing lowers transaction cost, but does not affect leverage or competition.
    public_payoff = (
        45 * control + 35 * quality + 20 * competition - 40 * annual_cost
    )
    incumbent_payoff = (
        100 * (0.60 * (0.45 + 0.35 * lock_in) + 0.40 * quality)
        - 25 * competition
        - 10 * leverage
        + (4 * portability if vendor_action == "adapt" else 0)
    )
    return Outcome(
        public_payoff,
        incumbent_payoff,
        control,
        quality,
        competition,
        portability,
        lock_in,
        annual_cost,
    )


def build_game(years: int, trials: int, seed: int):
    portfolios = [
        frozenset(policy for bit, policy in enumerate(POLICIES) if mask & (1 << bit))
        for mask in range(1 << len(POLICIES))
    ]
    government_payoffs = []
    incumbent_payoffs = []
    details = {}

    for portfolio_index, policies in enumerate(portfolios):
        government_row = []
        incumbent_row = []
        for vendor_index, vendor_action in enumerate(VENDOR_ACTIONS):
            outcomes = [
                simulate_trial(
                    policies,
                    vendor_action,
                    random.Random(seed + trial * 997 + portfolio_index * 31 + vendor_index),
                    years,
                )
                for trial in range(trials)
            ]
            government_row.append(
                sum(outcome.public_payoff for outcome in outcomes) / trials
            )
            incumbent_row.append(
                sum(outcome.incumbent_payoff for outcome in outcomes) / trials
            )
            details[(policies, vendor_action)] = {
                field: sum(getattr(outcome, field) for outcome in outcomes) / trials
                for field in Outcome.__dataclass_fields__
            }
        government_payoffs.append(government_row)
        incumbent_payoffs.append(incumbent_row)

    game = pyspiel.create_matrix_game(
        "digital_public_strategy_commons",
        "Government policy portfolio vs incumbent response",
        [portfolio_name(policies) for policies in portfolios],
        list(VENDOR_ACTIONS),
        government_payoffs,
        incumbent_payoffs,
    )
    return game, portfolios, government_payoffs, incumbent_payoffs, details


def best_response_results(portfolios, government_payoffs, incumbent_payoffs):
    results = []
    for index, policies in enumerate(portfolios):
        vendor_best = max(incumbent_payoffs[index])
        best_responses = [
            action
            for action, payoff in zip(VENDOR_ACTIONS, incumbent_payoffs[index])
            if abs(payoff - vendor_best) < 1e-9
        ]
        public_value = sum(
            government_payoffs[index][VENDOR_ACTIONS.index(action)]
            for action in best_responses
        ) / len(best_responses)
        results.append((public_value, policies, best_responses))
    return sorted(results, key=lambda row: row[0], reverse=True)


def interaction_effects(portfolios, government_payoffs):
    values = {
        policies: sum(government_payoffs[index]) / len(VENDOR_ACTIONS)
        for index, policies in enumerate(portfolios)
    }
    effects = []
    for left, right in itertools.combinations(POLICIES, 2):
        context_effects = []
        others = [policy for policy in POLICIES if policy not in (left, right)]
        for mask in range(1 << len(others)):
            context = frozenset(
                policy for bit, policy in enumerate(others) if mask & (1 << bit)
            )
            context_effects.append(
                values[context | {left, right}]
                - values[context | {left}]
                - values[context | {right}]
                + values[context]
            )
        effects.append((sum(context_effects) / len(context_effects), left, right))
    return sorted(effects, reverse=True)


def render_report(game, portfolios, government_payoffs, incumbent_payoffs, details,
                  years, trials, seed):
    # Exercise the OpenSpiel game state and ensure its stored payoff matches the simulation.
    state = game.new_initial_state()
    state.apply_actions([0, 0])
    assert abs(state.returns()[0] - government_payoffs[0][0]) < 1e-9

    ranked = best_response_results(portfolios, government_payoffs, incumbent_payoffs)
    interactions = interaction_effects(portfolios, government_payoffs)
    singles = [row for row in ranked if len(row[1]) == 1]
    top_value, top_policies, top_responses = ranked[0]
    top_details = [details[(top_policies, action)] for action in top_responses]
    fmt = lambda value: f"{value:.2f}"

    lines = [
        "# Digital Public Strategy Commons: simulation report",
        "",
        f"OpenSpiel matrix game; {years} annual rounds, {trials} Monte Carlo trials per action pair, seed {seed}.",
        "Payoffs and state indices are illustrative model units, not empirical estimates.",
        "",
        "## Results",
        "",
        "Government commits to a policy portfolio; the incumbent then chooses the response that maximizes its own payoff.",
        "The ranking below reports government payoff against that modeled best response.",
        "OpenSpiel stores the payoff matrix; this leader-follower calculation is not a simultaneous Nash-equilibrium solution.",
        "",
        "| Rank | Policy portfolio | Incumbent response | Government payoff | Control | Quality | Competition | Portability | Vendor lock-in | Annual cost |",
        "|---:|---|---|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for rank, (value, policies, responses) in enumerate(ranked[:8], start=1):
        outcomes = [details[(policies, action)] for action in responses]
        average = lambda key: sum(row[key] for row in outcomes) / len(outcomes)
        lines.append(
            f"| {rank} | {portfolio_name(policies)} | {', '.join(responses)} | {fmt(value)} | "
            f"{fmt(100 * average('control'))} | {fmt(100 * average('service_quality'))} | "
            f"{fmt(100 * average('competition'))} | {fmt(100 * average('portability'))} | "
            f"{fmt(100 * average('vendor_lock_in'))} | {fmt(average('annual_cost'))} |"
        )

    lines.extend(["", "### Strongest standalone strategies", "", "| Policy | Government payoff vs. incumbent best response |", "|---|---:|"])
    for value, policies, _ in sorted(singles, key=lambda row: row[0], reverse=True):
        lines.append(f"| {portfolio_name(policies)} | {fmt(value)} |")

    lines.extend(["", "### Pairwise complementarity", "", "Interactions are averaged over the other two policy choices and both incumbent actions. Positive values indicate complementarity in this payoff model; negative values indicate diminishing returns or conflict.", "", "| Policy pair | Interaction effect |", "|---|---:|"])
    for effect, left, right in interactions:
        lines.append(f"| {left} + {right} | {fmt(effect)} |")

    lines.extend([
        "",
        "## Interpretation and caveats",
        "",
        f"The best modeled portfolio is **{portfolio_name(top_policies)}** (government payoff {fmt(top_value)}), under incumbent response(s): {', '.join(top_responses)}.",
        f"The strongest modeled pairwise complementarity is **{interactions[0][1]} + {interactions[0][2]}** ({fmt(interactions[0][0])}); the most substitutive pair is **{interactions[-1][1]} + {interactions[-1][2]}** ({fmt(interactions[-1][0])}).",
        "",
        "This is a theory-building model, not a causal estimate. Probabilities, costs, lags, and payoff weights are explicit assumptions to be calibrated with procurement data and practitioner input. The model omits agency heterogeneity, multi-vendor bargaining, political turnover, and cross-agency spillovers. Cooperative purchasing is represented only as a transaction-cost saving; it does not increase bargaining power. Open-source portability, team capacity, procurement leverage, and startup entry are separate state variables so their interactions can be inspected.",
        "",
        "## Reproduce",
        "",
        "Install the dependencies in `requirements.txt`, then run `python simulate.py`. Adjust `--years`, `--trials`, and `--seed` to explore assumptions.",
        "",
    ])
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--years", type=int, default=YEARS)
    parser.add_argument("--trials", type=int, default=TRIALS)
    parser.add_argument("--seed", type=int, default=SEED)
    parser.add_argument("--output", default="results.md")
    args = parser.parse_args()
    if args.years < 1 or args.trials < 1:
        parser.error("--years and --trials must be positive")

    game, portfolios, government_payoffs, incumbent_payoffs, details = build_game(
        args.years, args.trials, args.seed
    )
    report = render_report(
        game, portfolios, government_payoffs, incumbent_payoffs, details,
        args.years, args.trials, args.seed,
    )
    with open(args.output, "w", encoding="utf-8") as report_file:
        report_file.write(report)
        print(f"Wrote {args.output} from {len(portfolios)} government portfolios "
            f"and {len(VENDOR_ACTIONS)} incumbent actions.")


if __name__ == "__main__":
    main()