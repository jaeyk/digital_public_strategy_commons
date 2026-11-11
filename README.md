# Digital Public Strategy Commons

How can governments build more effective and responsible digital public infrastructure without becoming captured by vendors? This repository turns public-interest technology strategies into explicit, inspectable games and simulations.

## First model

[`simulate.py`](simulate.py) models a government choosing a portfolio of four strategies over a 12-year relationship with an incumbent vendor:

- **In-house public-interest technology team:** grows government technical capacity.
- **Strategic procurement:** builds negotiation leverage, especially at contract awards and renewals.
- **Open source:** increases portability and reduces switching barriers.
- **Responsible startup pipeline:** creates delayed entry and competition, with entry more likely when government has capacity, open standards, and procurement access.

The incumbent responds by preserving lock-in or adapting. The 16 government portfolios and two vendor responses are represented as an OpenSpiel payoff matrix. Each payoff is estimated from repeated stochastic runs; the report evaluates government commitment followed by the incumbent's payoff-maximizing response. This is a leader-follower scenario analysis, not a simultaneous Nash-equilibrium solution. The report also estimates pairwise interaction effects. Positive interaction means the pair's combined effect exceeds the sum of its separate effects in the model; it does not establish real-world causality.

Cooperative purchasing is represented only as a reduction in administrative transaction cost. It does not create bargaining leverage or competition. The report lists all parameter values in code and explicitly treats findings as hypotheses for calibration, not empirical estimates.

## Run

Use Python 3.12 and install the pinned dependency in a virtual environment:

```sh
python3.12 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.txt
python simulate.py
```

The default run writes [`results.md`](results.md). Change the horizon, trial count, or random seed with `--years`, `--trials`, and `--seed`. Smaller trial counts are useful for quick experiments; compare multiple seeds and calibrate costs, probabilities, and payoff weights before treating rankings as policy guidance.

If Python reports that `ensurepip` is unavailable when creating the virtual environment, install the OS package `python3.12-venv`. As a no-venv alternative, install into a temporary target and set the import path:

```sh
python3.12 -m pip install --target /tmp/dpi-deps -r requirements.txt
PYTHONPATH=/tmp/dpi-deps python3.12 simulate.py
```
