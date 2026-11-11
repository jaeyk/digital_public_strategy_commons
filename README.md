# Civic Tech Digital Public Strategy Commons

How can governments build more effective and responsible digital public infrastructure without becoming captured by vendors? This repository turns public-interest technology strategies into explicit, inspectable games and simulations.

Civic tech needs more and better theories of change: written down, plural because different cases need different models, and tested continually. This project is an open commons for doing that. Every assumption is in plain text, every model is open, and anyone can challenge them without writing code.

**All of these models are wrong.** They are useful only as thought experiments: ways to make assumptions explicit and question them. None of their results are predictions or empirical estimates.

**Website:** [jaeyk.github.io/digital_public_strategy_commons](https://jaeyk.github.io/digital_public_strategy_commons/) is two simple pages. Visitors pick their agency type on a 2 by 2 grid, choose goals and strategies, guess how well their plan will do, and then compare their guess with what the model suggests, with plain-language reasons and one suggested change. No numbers or technical detail are shown.

**Contribute:** see [CONTRIBUTING.md](CONTRIBUTING.md). Forms for challenging an assumption, sharing a case, suggesting a strategy, or writing a theory of change need no coding.

## Contents

- [`framework.md`](framework.md) sets out the concepts the models formalize: the success criteria (positive, durable, scalable), the dimensions of digital state capacity, a taxonomy of about 40 strategies, the scope, scale, and pace of in-house capacity, the AI shock, and hypotheses about whether strategies work as a menu or a package.
- [`models/`](models/) contains four models built on a shared simulation engine and [OpenSpiel](https://github.com/google-deepmind/open_spiel). See [`models/README.md`](models/README.md).
- [`results/`](results/) holds the reports the models write.
- [`docs/`](docs/) is the website, published with GitHub Pages: plain HTML, CSS, and JavaScript with no build step. `index.html` holds the four choice steps and `results.html` the results. The pages run a JavaScript copy of the Python engine ([`docs/assets/engine.js`](docs/assets/engine.js)), whose numbers are exported from the Python code by `models/export_site_data.py`; a test checks that the two engines agree. The plain-language explanations on the results page are in [`docs/assets/results.js`](docs/assets/results.js) and mirror the relationships in `models/common/relationships.py`.
- [`simulate.py`](simulate.py) is the original four-strategy prototype, described below. Model 2 in `models/vendor_capture` extends it.

## Run the models

```sh
python3.12 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.txt
python -m models.run_all            # about 90 seconds; add --quick for a fast check
python -m unittest discover tests
```

## Preview the website

```sh
./preview_site.sh             # serves docs/ at http://localhost:8000
./preview_site.sh --rebuild   # first re-export the model data and check the JavaScript engine (needs Node.js)
```

To publish, enable GitHub Pages for this repository with source "Deploy from a branch", branch `main`, folder `/docs`.

## First model (prototype)

[`simulate.py`](simulate.py) models a government choosing a portfolio of four strategies over a 12-year relationship with an incumbent vendor:

- **In-house public-interest technology team:** grows government technical capacity.
- **Strategic procurement:** builds negotiation leverage, especially at contract awards and renewals.
- **Open source:** increases portability and reduces switching barriers.
- **Responsible tech startup (vendor) pipeline:** creates delayed entry and competition, with entry more likely when government has capacity, open standards, and procurement access.

The incumbent responds by preserving lock-in or adapting. The 16 government portfolios and two vendor responses are represented as an OpenSpiel payoff matrix. Each payoff is estimated from repeated stochastic runs; the report evaluates government commitment followed by the incumbent's payoff-maximizing response. This is a leader-follower scenario analysis, not a simultaneous Nash-equilibrium solution. The report also estimates pairwise interaction effects. Positive interaction means the pair's combined effect exceeds the sum of its separate effects in the model; it does not establish real-world causality.

Cooperative purchasing is represented only as a reduction in administrative transaction cost. It does not create bargaining leverage or competition. The report lists all parameter values in code and explicitly treats findings as hypotheses for calibration, not empirical estimates.

## Run the prototype

Use Python 3.12 and install the pinned dependencies in a virtual environment:

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

## Developer

Developed by [Jae Yeon Kim](https://jaeyk.github.io/) ([jaekim@unc.edu](mailto:jaekim@unc.edu)).

## License

- **Code** (the models, the website code, the tests, and the scripts) is released under the [MIT License](LICENSE).
- **Written content** (`framework.md`, the reports in `results/`, the documentation, and the text of the website) is released under the [Creative Commons Attribution 4.0 International License (CC BY 4.0)](LICENSE-CONTENT). You may share and adapt it with attribution to Jae Yeon Kim and a link to this repository.
