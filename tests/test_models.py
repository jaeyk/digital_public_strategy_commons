"""Tests for the models package. Run with: python -m unittest discover tests"""

from __future__ import annotations

import unittest

import numpy as np
import pyspiel

from models.common import analysis, engine, levers as lv
from models.common.jurisdictions import JURISDICTIONS
from models.common.solvers import backward_induction, pure_nash
from models.diffusion import run as diffusion
from models.turnover import game as turnover_game
from models.vendor_capture import game as vendor_game


class AnalysisTest(unittest.TestCase):
    def test_additive_function_has_no_interactions(self):
        weights = np.array([1.0, 2.0, 3.0])
        f = np.array([sum(w for bit, w in enumerate(weights) if m >> bit & 1) for m in range(8)])
        for pair in analysis.pairwise(f, 3, ("a", "b", "c")):
            self.assertEqual(pair.kind, "additive")
            self.assertAlmostEqual(pair.interaction, 0.0)
        self.assertAlmostEqual(analysis.package_share(f, 7, 3), 0.0)

    def test_relationship_types(self):
        self.assertEqual(analysis.classify(2.0, 2.0, 1.5), "complementary")
        self.assertEqual(analysis.classify(0.0, 2.0, 2.0, ("a", "b")), "prerequisite (a needs b)")
        self.assertEqual(analysis.classify(0.0, 0.0, 2.0), "joint (works only together)")
        self.assertEqual(analysis.classify(2.0, 2.0, -1.0), "substitute")
        self.assertEqual(analysis.classify(2.0, 2.0, -3.0), "conflict")

    def test_third_order_interaction_detected(self):
        f = np.array([1.0 if m == 7 else 0.0 for m in range(8)])
        value, *_ = analysis.triples(f, 3)[0]
        self.assertAlmostEqual(value, 1.0)


class EngineTest(unittest.TestCase):
    def setUp(self):
        self.portfolios = engine.portfolio_matrix(np.arange(0, 1 << len(lv.KEYS), 997))

    def test_states_stay_in_bounds_and_runs_reproduce(self):
        for j in JURISDICTIONS:
            a = engine.simulate(self.portfolios, j, trials=5, seed=1, turnover=True, ai_shock_year=4)
            b = engine.simulate(self.portfolios, j, trials=5, seed=1, turnover=True, ai_shock_year=4)
            np.testing.assert_allclose(a.outcome_gain, b.outcome_gain)
            for name, values in a.finals.items():
                self.assertTrue(np.all((values >= 0) & (values <= 1)), name)

    def test_no_insourcing_means_nothing_moves_in_house(self):
        mask = lv.mask_of(["team", "procurement"])
        result = engine.simulate(engine.portfolio_matrix([mask]), JURISDICTIONS[0], trials=3, record_paths=True)
        self.assertEqual(result.paths["insourced"].max(), 0.0)

    def test_insourcing_respects_scope_ceiling_without_pooling(self):
        j = JURISDICTIONS[2]
        mask = lv.mask_of(["team", "insourcing", "funding"])
        result = engine.simulate(engine.portfolio_matrix([mask]), j, years=40, trials=3)
        self.assertLessEqual(result.finals["insourced"][0], j.insource_ceiling + 0.02)

    def test_capacity_absorbs_more_ai_than_status_quo(self):
        masks = [0, lv.mask_of(["team", "insourcing", "portability", "platforms", "funding"])]
        result = engine.simulate(engine.portfolio_matrix(masks), JURISDICTIONS[0], trials=3, ai_shock_year=2,
                                 record_paths=True)
        absorbed = result.paths["ai_absorbed"][:, -1]
        self.assertGreater(absorbed[1], absorbed[0])


class GamesTest(unittest.TestCase):
    def test_vendor_game_equilibrium_matches_brute_force(self):
        game = pyspiel.load_game("python_dpsc_vendor_capture", {"trials": 3})
        values, plan = backward_induction(game.new_initial_state())
        government, vendor = game.government_payoffs, game.vendor_payoffs
        responses = vendor.argmax(axis=1)  # argmax picks the lowest id on ties, like the solver
        induced = government[np.arange(vendor_game.N_PORTFOLIOS), responses]
        self.assertAlmostEqual(values[0], induced.max())
        self.assertEqual(plan[""], int(np.argmax(induced)))

    def test_pure_nash_on_known_game(self):
        row = np.array([[3.0, 0.0], [5.0, 1.0]])
        self.assertEqual(pure_nash(row, row.T), [(1, 1)])

    def test_turnover_game_protections_raise_survival(self):
        from models.turnover.run import expected_survival
        game = pyspiel.load_game("python_dpsc_turnover")
        none, _ = expected_survival(game, 0)
        everything, _ = expected_survival(game, turnover_game.N_PACKAGES - 1)
        self.assertGreater(everything, none)
        state = game.new_initial_state()
        state.apply_action(0)
        self.assertAlmostEqual(sum(p for _, p in state.chance_outcomes()), 1.0)


class SiteScoresTest(unittest.TestCase):
    def test_scores_file_matches_engine(self):
        """docs/data/scores.bin holds the engine's scores for every plan, in the documented layout."""
        import json
        from pathlib import Path
        root = Path(__file__).resolve().parents[1] / "docs" / "data"
        spec = json.loads((root / "model.json").read_text())["scores"]
        data = np.frombuffer((root / spec["file"]).read_bytes(), dtype="<i2")
        n_measures, n_conditions = len(spec["measures"]), len(spec["conditions"])
        self.assertEqual(data.size, len(spec["agencies"]) * n_conditions * n_measures * spec["plans"])
        j = JURISDICTIONS[0]
        masks = [0, lv.mask_of(["team", "policy"]), (1 << len(lv.KEYS)) - 1]
        result = engine.simulate(engine.portfolio_matrix(masks), j, trials=spec["trials"], seed=spec["seed"])
        for row, mask in enumerate(masks):
            self.assertAlmostEqual(data[mask] / 100, result.outcome_gain[row], delta=0.006)  # stable, outcome_gain
            self.assertAlmostEqual(data[spec["plans"] + mask] / 100, result.spend_share[row], delta=0.006)


class DiffusionTest(unittest.TestCase):
    def test_shares_stay_on_simplex(self):
        values = np.tile(np.array([0.0, 1.0, 3.0, 2.0, 4.0]), (len(JURISDICTIONS), 1))
        result = diffusion.simulate_diffusion(values, diffusion.INTERVENTIONS["combined"])
        np.testing.assert_allclose(result["state"].sum(axis=1), 1.0)
        self.assertTrue(np.all(result["state"] >= 0))


if __name__ == "__main__":
    unittest.main()
