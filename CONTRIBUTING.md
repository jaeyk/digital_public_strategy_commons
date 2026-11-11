# Contributing

This project is a commons: a shared, open set of theories of change for building government's digital capacity. It improves when people with different experience test it. You do not need to write code to help.

## Ways to contribute without code

Each of these opens a short form on GitHub. You need a free GitHub account.

| If you want to... | Use this form |
|---|---|
| Say a number or relationship in the models is wrong | [Challenge an assumption](https://github.com/jaeyk/digital_public_strategy_commons/issues/new?template=challenge-assumption.yml) |
| Tell us what happened when a government tried a strategy | [Share a case or evidence](https://github.com/jaeyk/digital_public_strategy_commons/issues/new?template=share-evidence.yml) |
| Add a missing strategy or improve a description | [Suggest a strategy](https://github.com/jaeyk/digital_public_strategy_commons/issues/new?template=suggest-strategy.yml) |
| Describe a path that fits a particular kind of agency or place | [Write a theory of change](https://github.com/jaeyk/digital_public_strategy_commons/issues/new?template=theory-of-change.yml) |

The easiest starting point is the [website](https://jaeyk.github.io/digital_public_strategy_commons/). Try a plan, compare your guess with the model, and if the result or its reasons seem wrong to you, tell us why. You can also email [jaekim@unc.edu](mailto:jaekim@unc.edu).

Keep in mind that all of these models are wrong; they are thought experiments. The most useful contributions show where an assumption breaks down and why.

Some tips:

- Plain language is ideal. Say what you think and why.
- Say whether your view comes from direct experience, observation, research, or a hunch. All are useful; knowing which helps.
- Do not share confidential information or anything that identifies a private person.

## What happens to your contribution

1. A maintainer reads it and may ask follow-up questions in the issue.
2. If it changes the framework, [`framework.md`](framework.md) is updated, with credit.
3. If it changes the models, the assumption is changed in code, the models are rerun, and the website is updated. The issue links to the change, so every step stays visible.

## For developers and researchers

The project has four layers. Each one is plain text you can read:

- [`framework.md`](framework.md): the concepts, strategies, and hypotheses.
- [`models/`](models/): Python models built on [OpenSpiel](https://github.com/google-deepmind/open_spiel). Assumed relationships live in [`models/common/relationships.py`](models/common/relationships.py) and main parameters in [`models/common/engine.py`](models/common/engine.py). See [`models/README.md`](models/README.md).
- [`results/`](results/): the reports the models write.
- [`docs/`](docs/): the two-page website, published with GitHub Pages. It is plain HTML, CSS, and JavaScript with no build step. [`docs/assets/engine.js`](docs/assets/engine.js) is a JavaScript copy of the Python engine; all its numbers come from [`docs/data/`](docs/data/), which is exported from the Python code. The plain-language reasons shown to visitors are in [`docs/assets/results.js`](docs/assets/results.js); if you change a relationship in the model, update its explanation there too.

### Setup

```sh
python3.12 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.txt
```

### After changing a model

```sh
python -m models.run_all               # rerun the models and reports (about 90 seconds)
python -m models.export_site_data      # refresh the website's data
python -m unittest discover tests      # Python tests
node tests/site_engine.test.mjs        # check the website engine still matches Python
./preview_website.sh                      # look at the website at http://localhost:8000
```

If you change the engine's equations, change both `models/common/engine.py` and `docs/assets/engine.js`; the Node test will fail until they agree. Pull requests run these checks automatically.

### Principles

- **Declare assumptions.** Every deliberate interaction between strategies goes in `relationships.py`, with the framework row it comes from.
- **Keep the menu baseline.** Results should show what comes from assumptions and what comes from the model's structure.
- **Plain language first.** Anything a non-technical reader sees should be understandable without the code.
- **Verify sources.** References must be complete and checked against publisher or library records.

## License

By contributing, you agree that code contributions are released under the [MIT License](LICENSE) and written contributions under [CC BY 4.0](LICENSE-CONTENT).
