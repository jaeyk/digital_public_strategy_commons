# Digital Public Strategy Commons (DPSC)

How can governments build the capacity to deliver good digital services: human-centered, durable, and able to scale across agencies, without becoming captured by vendors? DPSC turns the strategies people propose into explicit models that anyone can try, question, and improve.

Civic tech needs more and better theories of change: written down, plural because different cases need different models, and tested continually. This repository is an open commons for doing that. Every assumption is in plain text, every model is open, and you can challenge them without writing code.

> **All of these models are wrong.** They are useful only as thought experiments: ways to make assumptions explicit and question them. None of their results are predictions or empirical estimates.

- **Website:** [jaeyk.github.io/digital_public_strategy_commons](https://jaeyk.github.io/digital_public_strategy_commons/)
- **Questions or suggestions:** [jaekim@unc.edu](mailto:jaekim@unc.edu)
- **Contribute:** [CONTRIBUTING.md](CONTRIBUTING.md)

## Contents

- [Start here: try the website](#start-here-try-the-website)
- [How the model works, in brief](#how-the-model-works-in-brief)
- [Ways to contribute](#ways-to-contribute)
- [Repository map](#repository-map)
- [Developer setup](#developer-setup)
- [How the pieces fit together](#how-the-pieces-fit-together)
- [Where to change things](#where-to-change-things)
- [The four research models](#the-four-research-models)
- [The original prototype](#the-original-prototype)
- [Troubleshooting](#troubleshooting)
- [Developer and license](#developer-and-license)

## Start here: try the website

The [website](https://jaeyk.github.io/digital_public_strategy_commons/) is the quickest way to understand the project. It takes about five minutes and shows no numbers or technical detail.

The site walks you through five steps: four to build a plan on the first page, and your results on the second.

1. **Your agency.** Pick the closest of four types on a 2 by 2 grid: small or well-resourced, with committed or reluctant leadership.
2. **Your goals and your investment.** Choose one or more goals:
   - **Human-centered delivery:** services work well for the people who use them and give good value for money.
   - **Durable change:** improvements survive elections, budget cuts, and staff leaving.
   - **Scales across agencies:** the approach also works in other agencies, including small ones and ones with reluctant leaders.

   Then choose how much you can invest (time, money, and effort): limited, moderate, or substantial. Budgets and priorities differ by agency, so you can also set your own: how many effort dots you can spend, and how much spending should count against results.
3. **Your strategies.** Choose from 15 strategies. Each shows how much time, money, and political effort it takes, from light to very heavy (passing a law and renegotiating vendor contracts are the heaviest), and your investment level limits how many fit. Effort differs between agencies, so you can change any rating to fit yours.
4. **Your guess.** For each goal, guess how your plan compares with other plans of the same size: *it backfires*, *below average*, *above average*, or *among the best*.
5. **Your results.** For each goal, the page shows your guess next to the model's guess, then explains in plain words what works and what holds the plan back. It suggests one change that would help most: add a strategy, drop one, or swap one. You can switch the investment level to see how much the answer depends on it. The page ends with a map of how the 15 levers connect: which strategies need others, which work better together, and which pull against each other.

## How the model works, in brief

- **15 policy levers** a government can use, such as hiring a core digital team, simplifying rules, using shared platforms, passing a law, or owning its data. They group about 40 strategies described in [`framework.md`](framework.md).
- **32,768 possible portfolios:** every combination of the 15 levers.
- **4 kinds of agencies:** the 2 by 2 of resources and commitment.
- **Two political conditions:** stable, or elections every four years that can bring a hostile government that cuts programs.
- **About 10.5 million simulations:** each portfolio is simulated over 16 years, in each kind of agency and political condition, 40 times.
- **22 assumed interactions** between strategies, for example "smarter contracts need a skilled core team to manage them" or "shared platforms pay off more when other governments use them too." Each one is written down in [`models/common/relationships.py`](models/common/relationships.py) with the part of the framework it comes from.

A plan's score is how much it improves outcomes for people over the 16 years, compared with doing nothing. Both your guess and the model's are guesses, not predictions: the model's guess only shows what follows from its written-down assumptions. The website turns scores into plain verdicts by comparing each plan with every other plan of the same size that fits the same investment. "It backfires" means the plan does worse than doing nothing.

The concepts behind all this, including the goals, the kinds of capacity, the obstacles, in-house capacity (scope, scale, and pace), and the AI shock, are in [`framework.md`](framework.md).

## Ways to contribute

**No coding needed.** The models improve when people with experience in government, vendors, and communities say what is wrong or missing.

- Try the website and email [jaekim@unc.edu](mailto:jaekim@unc.edu) with questions or suggestions.
- Use a short form on GitHub (free account needed):
  - [Challenge an assumption](https://github.com/jaeyk/digital_public_strategy_commons/issues/new?template=challenge-assumption.yml)
  - [Share a case or evidence](https://github.com/jaeyk/digital_public_strategy_commons/issues/new?template=share-evidence.yml)
  - [Suggest a strategy](https://github.com/jaeyk/digital_public_strategy_commons/issues/new?template=suggest-strategy.yml)
  - [Write a theory of change](https://github.com/jaeyk/digital_public_strategy_commons/issues/new?template=theory-of-change.yml)

**With code.** Follow [Developer setup](#developer-setup) below, then see [CONTRIBUTING.md](CONTRIBUTING.md) for the workflow and principles.

## Repository map

| Path | What it is |
|---|---|
| [`framework.md`](framework.md) | The concepts the models formalize: goals, capacity, strategies, hypothesized relationships, open questions, and verified references. Start here to understand the ideas. |
| [`models/`](models/) | Python models. [`models/README.md`](models/README.md) explains each one. |
| [`models/common/`](models/common/) | Shared building blocks: levers, agency types, assumed relationships, the simulation engine, and analysis tools. |
| [`results/`](results/) | Reports written by the four research models. |
| [`docs/`](docs/) | The website, published with GitHub Pages: plain HTML, CSS, and JavaScript, no build step. |
| [`docs/data/`](docs/data/) | Model data the website reads: `model.json` (levers, agency types, relationships, effort ratings), `scores.bin` (the model's scores for all 32,768 plans), and `parity.json` (engine test cases). Generated from the Python code; do not edit by hand. |
| [`tests/`](tests/) | Python tests, plus a Node test that checks the website's engine matches the Python engine. |
| [`.github/`](.github/) | Contribution forms and automated checks. |
| [`preview_website.sh`](preview_website.sh), [`update_website.sh`](update_website.sh) | Preview the website locally; publish an update. |
| [`simulate.py`](simulate.py), [`results.md`](results.md) | The original four-strategy prototype and its report. |

## Developer setup

You need **Python 3.11 or newer** (3.12 recommended; OpenSpiel 2.0.2 does not support older versions) and, for the website check, **Node.js**.

```sh
git clone https://github.com/jaeyk/digital_public_strategy_commons.git
cd digital_public_strategy_commons
python3.12 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.txt
```

Common tasks:

```sh
python -m unittest discover tests      # Python tests (a few seconds)
node tests/site_engine.test.mjs        # website engine matches the Python engine
python -m models.run_all               # rerun all four models and rewrite results/ (about 90 seconds)
python -m models.run_all --quick       # same, with fewer trials
python -m models.export_site_data      # regenerate docs/data/ for the website
./preview_website.sh                   # serve the website at http://localhost:8000
./preview_website.sh 9000              # use another port (also --port 9000)
./preview_website.sh --rebuild         # regenerate data and run the engine check first
./preview_website.sh --force           # take over the port without asking
./update_website.sh                    # regenerate, run all checks, show changes, ask, then commit and push
./update_website.sh "Message"          # same, with your own commit message
```

Each model can also be run on its own, for example `python -m models.capacity_portfolio.run --help`.

## How the pieces fit together

```
framework.md                 concepts and hypotheses
      |
models/common/               Python source of truth: levers, agency types, relationships, engine
      |                \
models/*/run.py         models/export_site_data.py
      |                       |
results/*.md            docs/data/model.json, parity.json
                              |
                        docs/assets/engine.js   (JavaScript copy of the engine)
                              |
                        docs/index.html, results.html   (the website)
```

- **Python is the source of truth.** Every number the website uses comes from [`models/export_site_data.py`](models/export_site_data.py). It writes `docs/data/model.json` (levers, agency types, parameters, relationships, effort ratings, investment levels) and `docs/data/scores.bin`, the model's scores for all 32,768 plans in every agency type, with and without hostile elections. The results page looks up the visitor's plan in `scores.bin` and builds its comparison group in the browser from the visitor's own effort ratings.
- **The website runs the model in the browser** with [`docs/assets/engine.js`](docs/assets/engine.js), a line-by-line JavaScript copy of [`models/common/engine.py`](models/common/engine.py). [`tests/site_engine.test.mjs`](tests/site_engine.test.mjs) checks the two agree on 192 test cases.
- **Automated checks** ([`.github/workflows/checks.yml`](.github/workflows/checks.yml)) run the tests on every push and pull request, and fail if `docs/data/` is out of date with the models.
- **Publishing:** GitHub Pages serves the `docs/` folder on `main` (Settings > Pages > Deploy from a branch > `main` > `/docs`). The live site updates a minute or two after a push.

## Where to change things

| To change... | Edit | Then |
|---|---|---|
| A strategy's definition, cost, or default effort rating (`EFFORT_REASONS`) | [`models/common/levers.py`](models/common/levers.py) | Export data; update its plain wording in `docs/assets/shared.js` |
| An assumed interaction between strategies | [`models/common/relationships.py`](models/common/relationships.py) | Export data; update the matching explanation in `docs/assets/results.js` |
| A main-effect parameter (hiring speed, lock-in, AI, ...) | `PARAMS` in [`models/common/engine.py`](models/common/engine.py) | Export data |
| The engine's equations | [`models/common/engine.py`](models/common/engine.py) **and** [`docs/assets/engine.js`](docs/assets/engine.js) | Export data; the Node test fails until they agree |
| Agency types (budgets, motivation, scope ceilings) | [`models/common/jurisdictions.py`](models/common/jurisdictions.py) | Export data |
| Investment levels (effort limit, how much spending counts) | `INVESTMENT_LEVELS` in [`models/export_site_data.py`](models/export_site_data.py) | Export data; wording in `LEVELS`, custom spending options in `WEIGHTS`, both in `docs/assets/shared.js` |
| The relationship map on the results page | `RELATIONS` and `SHORT_NAMES` in [`docs/assets/shared.js`](docs/assets/shared.js) (keys match `models/common/relationships.py`) | Preview |
| Website wording: agency types, goals, strategies, verdict labels | [`docs/assets/shared.js`](docs/assets/shared.js) | Preview |
| Website explanations of results | [`docs/assets/results.js`](docs/assets/results.js) | Preview |
| Page layout and style | [`docs/index.html`](docs/index.html), [`docs/results.html`](docs/results.html), [`docs/assets/style.css`](docs/assets/style.css) | Preview. Colors and type follow the [Figma design file](https://www.figma.com/design/w8Biv8YcYbj64TuvpHlq02) (Atkinson Hyperlegible Next; colors pass WCAG AA in light and dark mode) |
| Concepts, strategies, or hypotheses | [`framework.md`](framework.md) | Update the models if the change should be modeled |

"Export data" means `python -m models.export_site_data`; `./update_website.sh` does it for you. After changing models, also run `python -m models.run_all` to refresh the reports in `results/`.

## The four research models

The website uses the shared engine directly. Four fuller models, built on the same engine and on Google DeepMind's [OpenSpiel](https://github.com/google-deepmind/open_spiel), explore specific questions and write reports to [`results/`](results/):

| Model | Question | Report |
|---|---|---|
| [Capacity portfolio](models/capacity_portfolio/run.py) | Which combinations do best on each goal? Do strategies work as a menu or a package? How far and how fast can in-house delivery go? What does an AI shock change? | [results/capacity_portfolio.md](results/capacity_portfolio.md) |
| [Vendor capture](models/vendor_capture/game.py) | What happens when the incumbent vendor responds strategically, including to AI? (OpenSpiel game) | [results/vendor_capture.md](results/vendor_capture.md) |
| [Turnover](models/turnover/game.py) | Which protections keep a program alive when hostile successors can cut it? (OpenSpiel game) | [results/turnover.md](results/turnover.md) |
| [Diffusion](models/diffusion/run.py) | Do strategies spread to small and reluctant agencies, and what help from above works? (OpenSpiel evolutionary dynamics) | [results/diffusion.md](results/diffusion.md) |

[`models/README.md`](models/README.md) describes the design rules and each model in more detail.

## The original prototype

[`simulate.py`](simulate.py) is the project's first model, kept for reference: a government chooses among four strategies (in-house team, strategic procurement, open source, and a startup pipeline) over 12 years, and an incumbent vendor responds by keeping lock-in or adapting. It writes [`results.md`](results.md). Run it with `python simulate.py` (options: `--years`, `--trials`, `--seed`). The vendor capture model extends it.

## Troubleshooting

- **`ensurepip` is unavailable when creating the virtual environment:** install your system's `python3.12-venv` package, or install dependencies into a folder and point Python at it: `python3.12 -m pip install --target /tmp/dpsc-deps -r requirements.txt`, then prefix commands with `PYTHONPATH=/tmp/dpsc-deps`.
- **`No matching distribution found for open_spiel`:** your Python is older than 3.11.
- **"Address already in use" when previewing:** `./preview_website.sh` stops an earlier preview server on the same port automatically. If another program holds the port, it asks before stopping it; use `--force` to skip the question, or pick another port.
- **The website shows "could not load":** open it through `./preview_website.sh`, not by double-clicking the HTML file. Browsers block loading data from local files.
- **The automated check says `docs/data` is out of date:** run `python -m models.export_site_data` and commit the result.

## Developer and license

Developed by [Jae Yeon Kim](https://jaeyk.github.io/) ([jaekim@unc.edu](mailto:jaekim@unc.edu)).

- **Code** (the models, the website code, the tests, and the scripts) is released under the [MIT License](LICENSE).
- **Written content** (`framework.md`, the reports in `results/`, the documentation, and the text of the website) is released under the [Creative Commons Attribution 4.0 International License (CC BY 4.0)](LICENSE-CONTENT). You may share and adapt it with attribution to Jae Yeon Kim and a link to this repository.
