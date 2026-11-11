"""Small helpers for writing Markdown reports."""

from __future__ import annotations

import math
from pathlib import Path

RESULTS_DIR = Path(__file__).resolve().parents[2] / "results"


def fmt(value, digits: int = 2) -> str:
    if value is None or (isinstance(value, float) and math.isnan(value)):
        return "n/a"
    if isinstance(value, float):
        return f"{value:.{digits}f}"
    return str(value)


def table(headers, rows, align=None) -> list[str]:
    align = align or ["---"] * len(headers)
    lines = ["| " + " | ".join(headers) + " |", "|" + "|".join(align) + "|"]
    lines += ["| " + " | ".join(fmt(cell) for cell in row) + " |" for row in rows]
    return lines


def write(name: str, lines: list[str]) -> Path:
    RESULTS_DIR.mkdir(exist_ok=True)
    path = RESULTS_DIR / name
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path
