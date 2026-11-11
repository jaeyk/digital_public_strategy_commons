# Models

These models turn [`framework.md`](../framework.md) into simulations and games. Each answers part of one question: which strategies, alone or together, build digital state capacity that is **positive** (better outcomes and value for money), **durable** (survives political turnover), and **scalable** (works for jurisdictions with different capacity and motivation)?

The models are for building theory, not for prediction. Every number is an assumption, stated in code so it can be argued with and calibrated. A result shows what follows from the assumptions; it does not show that the assumptions are true.

## The four models

| Model | Question | Method | Framework sections | Report |
|---|---|---|---|---|
| 1. [Capacity portfolio](capacity_portfolio/run.py) | Which of the 32,768 combinations of 15 levers do best on each criterion? Do levers work as a menu or a package, and does order matter? What are the limits on scope, scale, and pace of in-house delivery? What does an AI shock change? | Vectorized Monte Carlo simulation over all portfolios, 4 jurisdiction types, with and without political turnover | 1, 2, 3, 4, 5 | [results/capacity_portfolio.md](../results/capacity_portfolio.md) |
| 2. [Vendor capture](vendor_capture/game.py) | What happens when the incumbent vendor responds strategically, including to AI? | OpenSpiel game (`python_dpsc_vendor_capture`): government commits, vendor responds; subgame-perfect equilibrium by backward induction; simultaneous-move version via `pyspiel.create_matrix_game` | 3 (market power, AI), 5 | [results/vendor_capture.md](../results/vendor_capture.md) |
| 3. [Turnover](turnover/game.py) | Which protections keep a program alive when hostile successors can cut it? | OpenSpiel game (`python_dpsc_turnover`) with chance nodes for elections and three players; backward induction | 1 (durable), 4 (in-house pace), 5 | [results/turnover.md](../results/turnover.md) |
| 4. [Diffusion](diffusion/run.py) | Do packages spread to small and reluctant jurisdictions, and which support from a higher level of government helps? | OpenSpiel evolutionary dynamics (`open_spiel.python.egt.dynamics.boltzmannq`) over four populations, with a coordination problem for shared platforms | 1 (scalable), 4 | [results/diffusion.md](../results/diffusion.md) |

Run everything with `python -m models.run_all` (about 90 seconds), or one model with, for example, `python -m models.capacity_portfolio.run --help`.

## Shared building blocks ([`common/`](common/))

| File | What it holds | Framework link |
|---|---|---|
| [`levers.py`](common/levers.py) | 15 levers, each mapped to the framework strategy IDs it stands for, with cost and how much it depends on local motivation. Lists strategies not modeled. | Section 4 |
| [`jurisdictions.py`](common/jurisdictions.py) | Four types: high or low capacity crossed with high or low motivation. Includes the in-house scope ceiling and hiring pipeline for each. | Sections 1, 6 |
| [`relationships.py`](common/relationships.py) | Every interaction deliberately built into the engine, with its type (prerequisite, complement, conflict, binding, moderator, cost sharing), strength, and the framework row it comes from. Scale to 0 for the menu baseline. | Section 5 |
| [`engine.py`](common/engine.py) | Year-by-year dynamics of the capacity dimensions, market power, in-house staff and insourced share, the AI shock, and political turnover. `PARAMS` holds main effects. | Sections 2, 3, 4 |
| [`analysis.py`](common/analysis.py) | Menu-or-package tests: pairwise classification, three-way interactions, package share, smallest effective package. | Section 5 |
| [`solvers.py`](common/solvers.py) | Backward induction over OpenSpiel game trees, and pure Nash equilibria of bimatrix games. | |

## Design rules

1. **Interactions are declared, not hidden.** Interactions that are meant to be there live in `relationships.py`. Reports mark which results come from these assumptions and which come from the model's structure (budget limits, saturation of 0-1 indices, causal chains, thresholds). Each Model 1 run also reports a menu baseline with all declared relationships switched off.
2. **Same random draws for every portfolio.** Differences between portfolios reflect the portfolios, not luck.
3. **Sensitivity is part of the result.** Model 1 reruns with relationship strengths at 0, 0.5, and 1.5 times their values, with a second seed, and with different assumptions about in-house cost, hiring, and transition speed.
4. **Criteria stay separate.** Positive, durable, and scalable are reported side by side so trade-offs stay visible.

## How the newer questions are modeled

**In-house delivery: scope, scale, pace.** The `team` lever is a core team: an informed buyer and product leader. The `insourcing` lever grows in-house staff to take over vendor work. Staff capacity grows only as fast as hiring allows (higher with a core team and hiring reform) and shrinks with attrition (lower with stable funding). Salaries are paid before work moves. Work moves in-house only as fast as experienced staff can manage, each move dents quality in proportion to inexperience, and each jurisdiction type has a ceiling on how much vendor work it could run. Pooling with other governments and shared platforms raise that ceiling. If a successor cuts the program, staff leave and work returns to vendors.

**AI shock.** AI is a scenario, not a lever. From the shock year, the share of AI capability the government absorbs depends on talent, portability, shared infrastructure, and insourced work. That share raises in-house productivity, the scope ceiling, quality, and reach. The rest arrives through vendors: some quality gain, but more lock-in, market concentration, and AI contract spending. Strategic procurement limits the bundling, and safeguards limit the damage to public trust.

## Headline results under current assumptions

These depend on assumptions that have not been calibrated. Read them as hypotheses to test.

- **Package, not menu, once in-house delivery is included.** About 70% of the best portfolio's value comes from combining levers. Insourcing without a core team loses value; with one, it is the strongest prerequisite pair in the model, and the core team should come first.
- **In-house delivery is slow and has limits.** A well-resourced, committed government reaches 50% of vendor work in about 10 years; small jurisdictions plateau around 30-40% unless they pool with others. Pace is limited by how fast work can be migrated safely, not just by hiring.
- **The AI shock deepens dependency quietly when capacity is missing.** With no response, lock-in rises 10-14 points and vendor revenue rises, while short-run net value barely changes. With capacity in place, AI raises value most for small but committed jurisdictions, and insourcing and the core team become the levers that gain most.
- **A strategic vendor changes the answer.** Committed governments that commit to team + procurement + portability get the vendor to adapt. Assuming the vendor never responds misses most of this.
- **Durability needs layered protection in polarized politics.** Protections substitute for each other when politics is supportive, but become complements when successors are likely to be hostile.
- **Scale depends on a higher level of government.** Without help, small reluctant jurisdictions mostly stay on the status quo. Providing shared platforms centrally lifts their adoption the most of the single interventions tested.

## Limitations and next steps

- Parameters need calibration from procurement records, workforce data, case studies, and practitioner interviews (framework Section 6).
- Each model simplifies: one incumbent vendor, stylized successors, four jurisdiction types, and levers that group several strategies.
- A possible extension is qualitative, multi-stakeholder simulation with generative agents, for example with Google DeepMind's Concordia library, to explore negotiations these models reduce to a few actions. It is not used here.
