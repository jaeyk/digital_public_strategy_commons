"""Menu-or-package analysis (framework.md Section 5).

Functions take `f`, an array with one value per portfolio, indexed by bit mask
(bit i set = lever i adopted), measured relative to the status quo (f[0] = 0).
"""

from __future__ import annotations

import itertools
from dataclasses import dataclass

import numpy as np

ABS_TOLERANCE = 0.15
"""Interaction (in outcome points) below which a pair is treated as additive."""
REL_TOLERANCE = 0.10
"""...or below this share of the larger of the two levers' separate effects."""


def masks(n: int) -> np.ndarray:
    return np.arange(1 << n, dtype=np.int64)


def standalone(f: np.ndarray, n: int) -> np.ndarray:
    """Effect of each lever adopted alone, compared with the status quo."""
    return np.array([f[1 << i] - f[0] for i in range(n)])


def average_marginal(f: np.ndarray, n: int) -> np.ndarray:
    """Effect of adding each lever, averaged over every combination of the others."""
    all_masks = masks(n)
    out = []
    for i in range(n):
        base = all_masks[(all_masks >> i & 1) == 0]
        out.append(float(np.mean(f[base | 1 << i] - f[base])))
    return np.array(out)


@dataclass(frozen=True)
class Pair:
    i: int
    j: int
    effect_i: float
    """Average effect of adding i when j is absent."""
    effect_j: float
    interaction: float
    """Average extra effect of having both, beyond the two separate effects."""
    share_positive: float
    """Share of contexts (combinations of other levers) where the interaction is positive."""
    kind: str


def classify(a: float, b: float, interaction: float, names=("i", "j")) -> str:
    """Relationship type for a pair, using the definitions in framework.md Section 5."""
    tolerance = max(ABS_TOLERANCE, REL_TOLERANCE * max(abs(a), abs(b)))
    if abs(interaction) <= tolerance:
        return "additive"
    if interaction > 0:
        small_a, small_b = a <= 0.25 * interaction, b <= 0.25 * interaction
        if small_a and small_b:
            return "joint (works only together)"
        if small_a:
            return f"prerequisite ({names[0]} needs {names[1]})"
        if small_b:
            return f"prerequisite ({names[1]} needs {names[0]})"
        return "complementary"
    if a > 0 and b > 0 and a + b + interaction >= max(a, b):
        return "substitute"
    return "conflict"


def pairwise(f: np.ndarray, n: int, keys: tuple[str, ...]) -> list[Pair]:
    all_masks = masks(n)
    pairs = []
    for i, j in itertools.combinations(range(n), 2):
        bi, bj = 1 << i, 1 << j
        base = all_masks[(all_masks & (bi | bj)) == 0]
        a = f[base | bi] - f[base]
        b = f[base | bj] - f[base]
        inter = f[base | bi | bj] - f[base | bi] - f[base | bj] + f[base]
        a_mean, b_mean, inter_mean = float(a.mean()), float(b.mean()), float(inter.mean())
        pairs.append(Pair(i, j, a_mean, b_mean, inter_mean, float(np.mean(inter > 0)),
                          classify(a_mean, b_mean, inter_mean, (keys[i], keys[j]))))
    return pairs


def triples(f: np.ndarray, n: int) -> list[tuple[float, int, int, int]]:
    """Third-order interaction (what the trio adds beyond all pairs), averaged over contexts."""
    all_masks = masks(n)
    out = []
    for i, j, k in itertools.combinations(range(n), 3):
        bits = (1 << i, 1 << j, 1 << k)
        base = all_masks[(all_masks & sum(bits)) == 0]
        total = np.zeros(base.size)
        for size in range(4):
            for subset in itertools.combinations(bits, size):
                total += (-1) ** (3 - size) * f[base | sum(subset)]
        out.append((float(total.mean()), i, j, k))
    return sorted(out, key=lambda row: abs(row[0]), reverse=True)


def package_share(f: np.ndarray, mask: int, n: int) -> float:
    """Share of a portfolio's gain that comes from combining levers rather than from each alone."""
    gain = f[mask] - f[0]
    if abs(gain) < 1e-9:
        return float("nan")
    alone = sum(f[1 << i] - f[0] for i in range(n) if mask >> i & 1)
    return float((gain - alone) / gain)


def minimal_package(f: np.ndarray, n: int, share: float = 0.9) -> int:
    """Smallest portfolio reaching `share` of the best gain (ties broken by higher gain)."""
    target = f[0] + share * (f.max() - f[0])
    candidates = np.flatnonzero(f >= target)
    sizes = np.array([bin(int(m)).count("1") for m in candidates])
    smallest = candidates[sizes == sizes.min()]
    return int(smallest[np.argmax(f[smallest])])
