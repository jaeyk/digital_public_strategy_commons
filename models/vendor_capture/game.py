"""Model 2 game: government commits to a portfolio, the incumbent vendor responds.

Registered with OpenSpiel as "python_dpsc_vendor_capture". It is a two-move,
perfect-information, general-sum game:

    1. Government chooses one of 128 portfolios of the seven market-facing levers.
    2. The incumbent vendor sees the portfolio and chooses a response.

Payoffs come from the shared capacity engine (models/common/engine.py), run
for the chosen jurisdiction type with the vendor's response built into the
dynamics. The government's payoff is net value (outcome gain minus weighted
spending), measured against the status quo with a lock-in vendor. The
vendor's payoff is contract revenue, which rises with lock-in and quality and
falls with competition.
"""

from __future__ import annotations

import functools

import numpy as np
import pyspiel

from models.common import engine
from models.common.jurisdictions import BY_KEY

KEYS: tuple[str, ...] = ("team", "insourcing", "procurement", "portability", "open_source", "maintenance", "entrants")
VENDOR_ACTIONS: tuple[str, ...] = engine.VENDOR_ACTIONS
GOVERNMENT, VENDOR = 0, 1
N_PORTFOLIOS = 1 << len(KEYS)

_DEFAULT_PARAMS = {"jurisdiction": "high_cap_high_mot", "years": 16, "trials": 30, "seed": 20261111,
                   "cost_weight": 10.0, "ai_shock_year": -1}

_GAME_TYPE = pyspiel.GameType(
    short_name="python_dpsc_vendor_capture",
    long_name="Digital Public Strategy Commons: vendor capture",
    dynamics=pyspiel.GameType.Dynamics.SEQUENTIAL,
    chance_mode=pyspiel.GameType.ChanceMode.DETERMINISTIC,
    information=pyspiel.GameType.Information.PERFECT_INFORMATION,
    utility=pyspiel.GameType.Utility.GENERAL_SUM,
    reward_model=pyspiel.GameType.RewardModel.TERMINAL,
    max_num_players=2,
    min_num_players=2,
    provides_information_state_string=False,
    provides_information_state_tensor=False,
    provides_observation_string=True,
    provides_observation_tensor=False,
    parameter_specification=_DEFAULT_PARAMS,
)


@functools.lru_cache(maxsize=None)
def payoff_tables(jurisdiction: str, years: int, trials: int, seed: int, cost_weight: float,
                  ai_shock_year: int = -1, baseline_ai_shock_year: int = -1):
    """(government, vendor) payoff matrices, shape (128 portfolios, 4 vendor actions).

    `ai_shock_year` = -1 means no AI shock. Government payoffs are measured against the status quo with
    a lock-in vendor and no AI shock, so games with and without the shock are directly comparable.
    """
    j = BY_KEY[jurisdiction]
    portfolios = engine.portfolio_matrix(np.arange(N_PORTFOLIOS), KEYS)
    government = np.zeros((N_PORTFOLIOS, len(VENDOR_ACTIONS)))
    vendor = np.zeros_like(government)
    ai = None if ai_shock_year < 0 else ai_shock_year
    reference = engine.simulate(portfolios[:1], j, years=years, trials=trials, seed=seed)
    baseline = (reference.outcome_gain - cost_weight * reference.spend_share)[0]
    for column, action in enumerate(VENDOR_ACTIONS):
        result = engine.simulate(portfolios, j, years=years, trials=trials, seed=seed, vendor_action=action,
                                 ai_shock_year=ai)
        government[:, column] = result.outcome_gain - cost_weight * result.spend_share
        vendor[:, column] = result.vendor_payoff
    return government - baseline, vendor


class VendorCaptureGame(pyspiel.Game):
    def __init__(self, params=None):
        params = {**_DEFAULT_PARAMS, **(params or {})}
        self.settings = params
        self.table_key = (str(params["jurisdiction"]), int(params["years"]), int(params["trials"]),
                          int(params["seed"]), float(params["cost_weight"]), int(params["ai_shock_year"]))
        self.government_payoffs, self.vendor_payoffs = payoff_tables(*self.table_key)
        both = np.concatenate([self.government_payoffs.ravel(), self.vendor_payoffs.ravel()])
        super().__init__(_GAME_TYPE, pyspiel.GameInfo(
            num_distinct_actions=N_PORTFOLIOS, max_chance_outcomes=0, num_players=2,
            min_utility=float(both.min()), max_utility=float(both.max()), utility_sum=None,
            max_game_length=2), params)

    def new_initial_state(self):
        return VendorCaptureState(self)

    def make_py_observer(self, iig_obs_type=None, params=None):
        return _Observer()


class VendorCaptureState(pyspiel.State):
    def __init__(self, game: VendorCaptureGame):
        super().__init__(game)
        # States are deep-copied when cloned, so keep a cache key rather than the game object.
        self._table_key = game.table_key
        self.portfolio: int | None = None
        self.response: int | None = None

    def current_player(self):
        if self.portfolio is None:
            return GOVERNMENT
        if self.response is None:
            return VENDOR
        return pyspiel.PlayerId.TERMINAL

    def _legal_actions(self, player):
        return list(range(N_PORTFOLIOS)) if player == GOVERNMENT else list(range(len(VENDOR_ACTIONS)))

    def _apply_action(self, action):
        if self.portfolio is None:
            self.portfolio = action
        else:
            self.response = action

    def _action_to_string(self, player, action):
        if player == GOVERNMENT:
            return " + ".join(k for bit, k in enumerate(KEYS) if action >> bit & 1) or "status quo"
        return VENDOR_ACTIONS[action]

    def is_terminal(self):
        return self.response is not None

    def returns(self):
        if not self.is_terminal():
            return [0.0, 0.0]
        government, vendor = payoff_tables(*self._table_key)
        return [float(government[self.portfolio, self.response]), float(vendor[self.portfolio, self.response])]

    def __str__(self):
        return f"portfolio={self.portfolio} response={self.response}"


class _Observer:
    """Perfect information: every player sees the full history."""

    def __init__(self):
        self.tensor = None
        self.dict = {}

    def set_from(self, state, player):
        pass

    def string_from(self, state, player):
        return str(state)


pyspiel.register_game(_GAME_TYPE, VendorCaptureGame)
