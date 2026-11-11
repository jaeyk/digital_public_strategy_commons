"""Model 3 game: durability under political turnover.

Registered with OpenSpiel as "python_dpsc_turnover". A perfect-information,
general-sum game with chance nodes and three players:

    player 0  reform government, which chooses protections for its program
    player 1  government after election 1 (if power changes hands)
    player 2  government after election 2 (if power changes hands)

Sequence:
    1. The reformer chooses any combination of four protections:
         mandate        - put the program in law (repeal needs legislation)
         budget_line    - give it its own stable budget line
         constituency   - build visible users and stakeholders who will defend it (safeguards, results)
         embedding      - embed it in shared platforms and partnerships others depend on
    2. Election 1 (chance): the program's supporters stay in power, or a successor
       takes over with low, medium, or high hostility to the program.
    3. A successor chooses to keep, scale back, or dismantle the program.
    4. Election 2 (chance) and successor decision, as above.

Payoffs:
    reformer   public value of the program over three terms, minus the political
               cost of the protections. Optionally, reversing an unfinished
               insourcing transition destroys extra value (work returns to vendors
               on worse terms).
    successor  ideological gain and budget savings from cutting, minus the
               political, legal, and practical cost of cutting, which the
               protections raise.

The successor's decision is a strategic choice here, unlike the reduced-form
dismantling rule in the shared engine.
"""

from __future__ import annotations

import numpy as np
import pyspiel

PROTECTIONS: tuple[str, ...] = ("mandate", "budget_line", "constituency", "embedding")
DECISIONS: tuple[str, ...] = ("keep", "scale_back", "dismantle")
HOSTILITY: tuple[str, ...] = ("low", "medium", "high")
HOSTILITY_LEVEL = {"low": 0.1, "medium": 0.5, "high": 1.0}
N_PACKAGES = 1 << len(PROTECTIONS)

# Political cost to the reformer of each protection, and how much each raises a
# successor's cost of cutting the whole program.
PROTECTION_COST = {"mandate": 1.0, "budget_line": 0.8, "constituency": 0.8, "embedding": 1.2}
DETERRENCE = {"mandate": 3.0, "budget_line": 1.5, "constituency": 2.5, "embedding": 2.0}

_DEFAULT_PARAMS = {
    "program_value": 5.0,       # public value per term of the full program
    "continuity": 0.5,          # probability the program's supporters keep power at an election
    "p_low": 0.4, "p_medium": 0.35, "p_high": 0.25,   # hostility of a new government
    "savings": 1.5,             # budget savings from cutting the full program
    "ideology": 6.0,            # ideological gain from cutting, at maximum hostility
    "base_cut_cost": 0.5,       # disruption cost of cutting with no protections
    "scale_back_cost_share": 0.35,
    "reversal_cost": 0.0,       # extra public value lost when cutting (e.g. unfinished insourcing)
}

_GAME_TYPE = pyspiel.GameType(
    short_name="python_dpsc_turnover",
    long_name="Digital Public Strategy Commons: durability under turnover",
    dynamics=pyspiel.GameType.Dynamics.SEQUENTIAL,
    chance_mode=pyspiel.GameType.ChanceMode.EXPLICIT_STOCHASTIC,
    information=pyspiel.GameType.Information.PERFECT_INFORMATION,
    utility=pyspiel.GameType.Utility.GENERAL_SUM,
    reward_model=pyspiel.GameType.RewardModel.TERMINAL,
    max_num_players=3,
    min_num_players=3,
    provides_information_state_string=False,
    provides_information_state_tensor=False,
    provides_observation_string=True,
    provides_observation_tensor=False,
    parameter_specification=_DEFAULT_PARAMS,
)

CONTINUE = 0  # chance outcome: supporters keep power; 1..3 = new government with hostility low..high


def package_name(mask: int) -> str:
    return " + ".join(p for bit, p in enumerate(PROTECTIONS) if mask >> bit & 1) or "no protections"


def deterrence(mask: int) -> float:
    return sum(DETERRENCE[p] for bit, p in enumerate(PROTECTIONS) if mask >> bit & 1)


def protection_cost(mask: int) -> float:
    return sum(PROTECTION_COST[p] for bit, p in enumerate(PROTECTIONS) if mask >> bit & 1)


class TurnoverGame(pyspiel.Game):
    def __init__(self, params=None):
        self.settings = {**_DEFAULT_PARAMS, **(params or {})}
        total = self.settings["p_low"] + self.settings["p_medium"] + self.settings["p_high"]
        if abs(total - 1) > 1e-9:
            raise ValueError("p_low + p_medium + p_high must equal 1")
        super().__init__(_GAME_TYPE, pyspiel.GameInfo(
            num_distinct_actions=N_PACKAGES, max_chance_outcomes=4, num_players=3,
            min_utility=-100.0, max_utility=100.0, utility_sum=None, max_game_length=5), self.settings)

    def new_initial_state(self):
        return TurnoverState(self)

    def make_py_observer(self, iig_obs_type=None, params=None):
        return _Observer()


class TurnoverState(pyspiel.State):
    def __init__(self, game: TurnoverGame):
        super().__init__(game)
        self.s = dict(game.settings)
        self.package: int | None = None
        self.level = 1.0            # share of the program still running
        self.levels = []            # program level in terms 2 and 3
        self.election = 0           # elections held so far
        self.pending: str | None = None   # hostility of a successor waiting to decide
        self.successor_payoff = [0.0, 0.0]
        self.public_loss = 0.0

    def current_player(self):
        if self.package is None:
            return 0
        if self.pending is not None:
            return self.election  # player 1 after election 1, player 2 after election 2
        if self.election < 2:
            return pyspiel.PlayerId.CHANCE
        return pyspiel.PlayerId.TERMINAL

    def chance_outcomes(self):
        s = self.s
        changed = 1 - s["continuity"]
        return [(CONTINUE, s["continuity"]), (1, changed * s["p_low"]), (2, changed * s["p_medium"]),
                (3, changed * s["p_high"])]

    def _legal_actions(self, player):
        if player == 0:
            return list(range(N_PACKAGES))
        return list(range(len(DECISIONS)))

    def _apply_action(self, action):
        if self.package is None:
            self.package = action
        elif self.is_chance_node():
            self.election += 1
            if action == CONTINUE:
                self.levels.append(self.level)
            else:
                self.pending = HOSTILITY[action - 1]
        else:
            self._decide(DECISIONS[action])

    def _decide(self, decision: str):
        s, h = self.s, HOSTILITY_LEVEL[self.pending]
        new_level = {"keep": self.level, "scale_back": min(self.level, 0.5), "dismantle": 0.0}[decision]
        cut = self.level - new_level
        if cut > 0:
            full_cut_cost = s["base_cut_cost"] + deterrence(self.package)
            share = s["scale_back_cost_share"] if decision == "scale_back" else 1.0
            gain = cut * (s["savings"] + h * s["ideology"])
            # Protections make cutting costlier the more of the program survives to defend it.
            self.successor_payoff[self.election - 1] += gain - share * full_cut_cost * self.level
            self.public_loss += cut * s["reversal_cost"]
        self.level = new_level
        self.levels.append(self.level)
        self.pending = None

    def _action_to_string(self, player, action):
        if player == pyspiel.PlayerId.CHANCE:
            return "supporters stay" if action == CONTINUE else f"{HOSTILITY[action - 1]}-hostility successor"
        if player == 0:
            return package_name(action)
        return DECISIONS[action]

    def is_terminal(self):
        return self.package is not None and self.election == 2 and self.pending is None

    def returns(self):
        if not self.is_terminal():
            return [0.0, 0.0, 0.0]
        value = self.s["program_value"] * (1 + sum(self.levels))
        reformer = value - protection_cost(self.package) - self.public_loss
        return [reformer, *self.successor_payoff]

    def __str__(self):
        return f"package={self.package} levels={self.levels} pending={self.pending}"


class _Observer:
    def __init__(self):
        self.tensor = None
        self.dict = {}

    def set_from(self, state, player):
        pass

    def string_from(self, state, player):
        return str(state)


pyspiel.register_game(_GAME_TYPE, TurnoverGame)
