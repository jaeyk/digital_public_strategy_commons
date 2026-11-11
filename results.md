# Digital Public Strategy Commons: simulation report

OpenSpiel matrix game; 12 annual rounds, 500 Monte Carlo trials per action pair, seed 20261111.
Payoffs and state indices are illustrative model units, not empirical estimates.

## Results

Government commits to a policy portfolio; the incumbent then chooses the response that maximizes its own payoff.
The ranking below reports government payoff against that modeled best response.
OpenSpiel stores the payoff matrix; this leader-follower calculation is not a simultaneous Nash-equilibrium solution.

| Rank | Policy portfolio | Incumbent response | Government payoff | Control | Quality | Competition | Portability | Vendor lock-in | Annual cost |
|---:|---|---|---:|---:|---:|---:|---:|---:|---:|
| 1 | team+procurement+open_source+startups | adapt | 41.78 | 47.76 | 75.48 | 26.38 | 57.92 | 50.09 | 0.28 |
| 2 | team+open_source | adapt | 41.47 | 42.78 | 74.50 | 13.70 | 57.92 | 57.35 | 0.17 |
| 3 | team+open_source+startups | adapt | 41.41 | 45.10 | 75.16 | 23.01 | 57.92 | 57.35 | 0.24 |
| 4 | team+procurement+open_source | adapt | 40.77 | 44.53 | 74.83 | 13.70 | 57.92 | 50.33 | 0.21 |
| 5 | team | adapt | 38.61 | 31.14 | 74.44 | 13.70 | 14.55 | 60.52 | 0.10 |
| 6 | open_source | adapt | 38.13 | 31.86 | 69.86 | 13.70 | 51.32 | 58.94 | 0.09 |
| 7 | procurement+open_source+startups | adapt | 37.64 | 36.16 | 70.68 | 24.16 | 51.32 | 52.17 | 0.21 |
| 8 | team+procurement | adapt | 37.57 | 32.23 | 74.64 | 13.70 | 14.55 | 56.16 | 0.15 |

### Strongest standalone strategies

| Policy | Government payoff vs. incumbent best response |
|---|---:|
| team | 38.61 |
| open_source | 38.13 |
| procurement | 35.08 |
| startups | 33.84 |

### Pairwise complementarity

Interactions are averaged over the other two policy choices and both incumbent actions. Positive values indicate complementarity in this payoff model; negative values indicate diminishing returns or conflict.

| Policy pair | Interaction effect |
|---|---:|
| open_source + startups | 1.41 |
| procurement + startups | 1.16 |
| team + open_source | 0.93 |
| team + startups | 0.63 |
| procurement + open_source | 0.20 |
| team + procurement | -0.04 |

## Interpretation and caveats

The best modeled portfolio is **team+procurement+open_source+startups** (government payoff 41.78), under incumbent response(s): adapt.
The strongest modeled pairwise complementarity is **open_source + startups** (1.41); the most substitutive pair is **team + procurement** (-0.04).

This is a theory-building model, not a causal estimate. Probabilities, costs, lags, and payoff weights are explicit assumptions to be calibrated with procurement data and practitioner input. The model omits agency heterogeneity, multi-vendor bargaining, political turnover, and cross-agency spillovers. Cooperative purchasing is represented only as a transaction-cost saving; it does not increase bargaining power. Open-source portability, team capacity, procurement leverage, and startup entry are separate state variables so their interactions can be inspected.

## Reproduce

Install the dependencies in `requirements.txt`, then run `python simulate.py`. Adjust `--years`, `--trials`, and `--seed` to explore assumptions.
