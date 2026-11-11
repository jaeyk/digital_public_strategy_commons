"""Export everything the website needs from the Python models.

The website runs a JavaScript copy of the engine in the browser so people can
try their own theories of change. To keep one source of truth, every number
it uses comes from this script:

    docs/data/model.json    levers, jurisdiction types, parameters, assumed relationships, effort ratings
    docs/data/scores.bin    the model's scores for all 32,768 plans in every agency type (see write_scores)
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
        "effort": lv.EFFORT,
        "effort_reasons": {k: reason for k, (_, reason) in lv.EFFORT_REASONS.items()},
        "investment_levels": list(INVESTMENT_LEVELS),
        "defaults": {"years": 16, "ai_shock_year": cp.AI_YEAR, "trials": cp.TRIALS, "political_conditions": 2},
        "scores": write_scores(SITE_DATA / "scores.bin"),
    }


# How much a visitor can invest (time, money, and effort). Each level caps the total effort of the
# strategies they can choose (levers.EFFORT) and sets how much spending counts against benefits
# (outcome points per 1.0 of yearly spending as a share of the agency's budget): with limited
# investment, every strategy has to pay off.
INVESTMENT_LEVELS = (
    {"key": "limited", "effort_points": 4, "cost_weight": 10.0},
    {"key": "moderate", "effort_points": 7, "cost_weight": 5.0},
    {"key": "substantial", "effort_points": 11, "cost_weight": 0.0},
)
SITE_SEED = 7


SCORE_TRIALS = 40
SCORE_MEASURES = ("outcome_gain", "spend_share", "survival")


def write_scores(path: Path) -> dict:
    """Write the model's scores for every one of the 32,768 plans to a compact binary file.

    The website looks up a visitor's plan here and rebuilds the comparison group (plans of the same
    size that fit the visitor's investment, using the visitor's own effort ratings) in the browser.

    Layout: little-endian int16, value x 100, ordered [agency][condition][measure][plan], where
    agency follows JURISDICTIONS, condition is (stable, turnover), measure is SCORE_MEASURES, and
    plan is the bit mask over levers.KEYS (bit i set = lever i adopted).
    """
    masks = np.arange(1 << len(lv.KEYS))
    portfolios = engine.portfolio_matrix(masks)
    blocks = []
    for j in JURISDICTIONS:
        for turnover in (False, True):
            r = engine.simulate(portfolios, j, trials=SCORE_TRIALS, seed=SITE_SEED, turnover=turnover)
            blocks += [r.outcome_gain, r.spend_share, np.nan_to_num(r.survival, nan=0.0)]
    data = np.round(np.array(blocks) * 100).astype("<i2")
    path.write_bytes(data.tobytes())
    return {"file": path.name, "format": "int16 little-endian, value x 100", "agencies": [j.key for j in JURISDICTIONS],
            "conditions": ["stable", "turnover"], "measures": list(SCORE_MEASURES), "plans": int(masks.size),
            "trials": SCORE_TRIALS, "seed": SITE_SEED}


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
