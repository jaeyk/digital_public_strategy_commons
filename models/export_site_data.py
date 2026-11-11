"""Export everything the website needs from the Python models.

The website runs a JavaScript copy of the engine in the browser so people can
try their own theories of change. To keep one source of truth, every number
it uses comes from this script:

    docs/data/model.json    levers, jurisdiction types, parameters, and assumed relationships
    docs/data/parity.json   deterministic test cases; tests/site_engine.test.mjs checks that
                            the JavaScript engine reproduces them

Run after changing any model:  python -m models.export_site_data
"""

from __future__ import annotations

import argparse
import dataclasses
import json
from pathlib import Path

import numpy as np

from models.capacity_portfolio import run as cp
from models.common import engine, levers as lv
from models.common.jurisdictions import JURISDICTIONS
from models.common.relationships import RELATIONSHIPS

SITE_DATA = Path(__file__).resolve().parents[1] / "docs" / "data"


def clean(value):
    """Make numpy values JSON-safe and round floats to keep files small."""
    if isinstance(value, dict):
        return {str(k): clean(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [clean(v) for v in value]
    if isinstance(value, np.ndarray):
        return clean(value.tolist())
    if isinstance(value, (np.floating, float)):
        return None if np.isnan(value) else round(float(value), 4)
    if isinstance(value, np.integer):
        return int(value)
    return value


def model_spec() -> dict:
    return {
        "levers": [dataclasses.asdict(lever) for lever in lv.LEVERS],
        "not_modeled": lv.NOT_MODELED,
        "jurisdictions": [dataclasses.asdict(j) for j in JURISDICTIONS],
        "params": engine.PARAMS,
        "embeddedness": engine.EMBEDDEDNESS,
        "initial": engine.INITIAL,
        "vendor_actions": list(engine.VENDOR_ACTIONS),
        "relationships": [dataclasses.asdict(r) for r in RELATIONSHIPS],
        "defaults": {"years": 16, "cost_weight": 10.0, "ai_shock_year": cp.AI_YEAR},
    }


PARITY_PORTFOLIOS = (
    (), ("team",), ("team", "insourcing", "funding"), ("procurement", "portability", "entrants", "open_source"),
    ("team", "insourcing", "funding", "policy", "platforms", "collaboration", "safeguards"),
    tuple(lv.KEYS),
)


def parity_cases() -> list[dict]:
    cases = []
    portfolios = engine.portfolio_matrix([lv.mask_of(keys) for keys in PARITY_PORTFOLIOS])
    for j in JURISDICTIONS:
        for vendor_action in engine.VENDOR_ACTIONS:
            for ai in (None, 4):
                result = engine.simulate(portfolios, j, years=16, trials=1, seed=0, vendor_action=vendor_action,
                                         ai_shock_year=ai, params={"quality_noise": 0.0}, record_paths=True)
                for k, keys in enumerate(PARITY_PORTFOLIOS):
                    cases.append({
                        "jurisdiction": j.key, "vendor_action": vendor_action, "ai_shock_year": ai,
                        "levers": list(keys), "outcome_gain": result.outcome_gain[k],
                        "spend_share": result.spend_share[k], "vendor_payoff": result.vendor_payoff[k],
                        "finals": {name: values[k] for name, values in result.finals.items()},
                        "outcome_path": result.paths["outcome"][k],
                    })
    return cases


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.parse_args(argv)
    SITE_DATA.mkdir(parents=True, exist_ok=True)

    files = {"model.json": model_spec(), "parity.json": parity_cases()}
    for name, content in files.items():
        path = SITE_DATA / name
        path.write_text(json.dumps(clean(content), separators=(",", ":")), encoding="utf-8")
        print(f"Wrote {path} ({path.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    main()
