"""Equilibrium solvers that work on OpenSpiel game objects."""

from __future__ import annotations

import itertools

import numpy as np
import pyspiel


def backward_induction(state: pyspiel.State) -> tuple[np.ndarray, dict[str, int]]:
    """Subgame-perfect equilibrium of a perfect-information game with chance nodes.

    Returns the expected returns from `state` and the equilibrium action at
    every decision node, keyed by `state.history_str()`. Each player maximizes
    their own expected return. Ties go to the lowest action id, so games
    should list the "do nothing" action first.
    """
    plan: dict[str, int] = {}

    def solve(s: pyspiel.State) -> np.ndarray:
        if s.is_terminal():
            return np.array(s.returns())
        if s.is_chance_node():
            return sum(prob * solve(s.child(action)) for action, prob in s.chance_outcomes())
        player = s.current_player()
        best_action, best_value = None, None
        for action in s.legal_actions():
            value = solve(s.child(action))
            if best_value is None or value[player] > best_value[player] + 1e-12:
                best_action, best_value = action, value
        plan[s.history_str()] = best_action
        return best_value

    return solve(state), plan


def pure_nash(row: np.ndarray, col: np.ndarray, tol: float = 1e-9) -> list[tuple[int, int]]:
    """All pure-strategy Nash equilibria of a bimatrix game."""
    row_best = row >= row.max(axis=0, keepdims=True) - tol
    col_best = col >= col.max(axis=1, keepdims=True) - tol
    return [(i, j) for i, j in itertools.product(range(row.shape[0]), range(row.shape[1]))
            if row_best[i, j] and col_best[i, j]]
