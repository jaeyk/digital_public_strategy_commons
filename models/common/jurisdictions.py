"""Jurisdiction typology for testing scalability (framework.md Section 1 and Section 6, item 5).

Capacity and motivation are crossed because the framework treats them as
different problems: a small committed city lacks resources, a large reluctant
agency lacks will. Starting values are illustrative assumptions, not estimates.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Jurisdiction:
    key: str
    name: str
    budget: float
    """Modernization budget per year, in the same units as Lever.annual_cost."""
    motivation: float
    """0..1. Scales how faithfully levers that depend on local effort are carried out."""
    talent0: float
    authority0: float
    policy_fit0: float
    lock_in0: float
    population_share: float
    """Share of all jurisdictions of this type; used by the diffusion model."""
    insource_ceiling: float
    """Scope: largest share of current vendor work this jurisdiction could realistically run itself."""
    hiring_pipeline: float
    """Scale: relative ability to recruit technical staff (labor market, pay, employer reputation)."""


JURISDICTIONS: tuple[Jurisdiction, ...] = (
    Jurisdiction("high_cap_high_mot", "Well-resourced and committed", 0.80, 0.90, 0.30, 0.35, 0.40, 0.65, 0.05, 0.60, 1.0),
    Jurisdiction("high_cap_low_mot", "Well-resourced and reluctant", 0.80, 0.40, 0.25, 0.30, 0.35, 0.72, 0.10, 0.60, 0.9),
    Jurisdiction("low_cap_high_mot", "Small and committed", 0.30, 0.90, 0.10, 0.20, 0.45, 0.70, 0.25, 0.35, 0.6),
    Jurisdiction("low_cap_low_mot", "Small and reluctant", 0.30, 0.40, 0.08, 0.15, 0.40, 0.78, 0.60, 0.35, 0.5),
)

BY_KEY: dict[str, Jurisdiction] = {j.key: j for j in JURISDICTIONS}
