"""Assumed relationships between strategies (framework.md Section 5).

In a simulation, complementarity is an assumption, not a finding: interaction
effects appear only if the equations contain them. Every interaction the
engine encodes on purpose is listed here, with its type, strength, and the
framework row it comes from. Setting `scale=0` turns all of them off, which
gives the "menu" baseline. Interactions that remain in the menu baseline come
from the model's structure (budget limits, bounded 0..1 state variables, and
causal chains), and the reports say so.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Relationship:
    key: str
    kind: str
    levers: tuple[str, ...]
    strength: float
    framework_row: str
    how_encoded: str


RELATIONSHIPS: tuple[Relationship, ...] = (
    Relationship(
        "talent_gates_procurement", "prerequisite", ("team", "procurement"), 0.80,
        "In-house talent -> strategic procurement, modular contracting, contract rights",
        "Procurement leverage and modular competition are multiplied by 1 - s*(1 - talent)."),
    Relationship(
        "open_source_needs_maintenance", "prerequisite", ("maintenance", "open_source"), 0.60,
        "Open source + maintenance funding",
        "Open source's portability effect is multiplied by 1 - s*(1 - maintenance intensity)."),
    Relationship(
        "portability_stack", "complement", ("open_source", "portability"), 0.10,
        "Open source + data rights + open APIs",
        "Extra portability growth of s * open_source * portability."),
    Relationship(
        "funding_retains_talent", "complement", ("funding", "team"), 0.50,
        "Digital team + legal mandate + continuous funding (durability)",
        "Stable funding cuts staff attrition by s * funding intensity."),
    Relationship(
        "mandate_protects", "complement", ("mandate",), 0.35,
        "Digital team + legal mandate + continuous funding (durability)",
        "Adds s * mandate intensity to every lever's protection against a hostile successor."),
    Relationship(
        "funding_protects", "complement", ("funding",), 0.25,
        "Digital team + legal mandate + continuous funding (durability)",
        "Adds s * funding stability to every lever's protection against a hostile successor."),
    Relationship(
        "legitimacy_protects", "complement", ("safeguards",), 0.25,
        "Success criterion 'durable': who would defend it?",
        "Adds s * public legitimacy to every lever's protection against a hostile successor."),
    Relationship(
        "policy_binding_constraint", "binding", ("policy",), 0.80,
        "Policy simplification -> any delivery strategy",
        "Quality and reach gains are multiplied by 1 - s*(1 - policy fit)."),
    Relationship(
        "lock_in_limits_change", "binding", ("procurement", "portability", "entrants", "public_option"), 0.40,
        "Constraint 1 (market power): vendors control the systems needed to change services",
        "Quality and reach gains are multiplied by 1 - s * lock-in, so reducing lock-in raises the return to other levers."),
    Relationship(
        "platforms_need_authority", "complement", ("platforms", "authority"), 0.60,
        "Shared platforms + central authority + funding",
        "Platform growth is multiplied by 1 + s * authority intensity."),
    Relationship(
        "platforms_need_funding", "complement", ("platforms", "funding"), 0.40,
        "Shared platforms + central authority + funding",
        "Platform growth is multiplied by 1 + s * funding intensity."),
    Relationship(
        "entrants_need_portability", "prerequisite", ("portability", "entrants"), 0.70,
        "Startup pipeline + portability",
        "New-entrant competition is multiplied by 1 - s*(1 - portability)."),
    Relationship(
        "public_option_crowds_out_entrants", "conflict", ("public_option", "entrants"), 0.50,
        "Startup pipeline vs. public option",
        "New-entrant competition is multiplied by 1 - s * public option intensity."),
    Relationship(
        "spend_controls_slow_teams", "conflict", ("authority", "team"), 0.20,
        "Spend controls vs. agency autonomy for product teams",
        "Talent's contribution to quality is multiplied by 1 - s * authority intensity."),
    Relationship(
        "cooperative_vs_modular", "conflict", ("collaboration", "procurement"), 0.30,
        "Cooperative purchasing vs. modular contracting",
        "Modular procurement's competition effect is multiplied by 1 - s * collaboration intensity."),
    Relationship(
        "core_team_gates_insourcing", "prerequisite", ("team", "insourcing"), 0.70,
        "In-house capacity: pace (moving work in-house needs experienced staff to manage migration)",
        "The speed at which work can move in-house is multiplied by 1 - s*(1 - talent)."),
    Relationship(
        "team_speeds_hiring", "complement", ("team", "insourcing"), 0.50,
        "In-house capacity: scale (hiring reform and a credible core team speed recruitment)",
        "The maximum hiring rate is multiplied by 1 + s * team intensity."),
    Relationship(
        "pooling_extends_scope", "complement", ("insourcing", "collaboration", "platforms"), 0.15,
        "In-house capacity: scope (pooled teams and shared platforms let small jurisdictions run more)",
        "The insourcing ceiling rises by s * collaboration intensity + s * shared infrastructure."),
    Relationship(
        "capacity_absorbs_ai", "moderator", ("team", "insourcing", "portability", "platforms"), 1.00,
        "AI shock: whether AI strengthens the state or the vendor depends on how it is built or procured",
        "Share of AI capability absorbed by public capacity = s * (weighted talent, portability, shared "
        "infrastructure, insourced share); the rest arrives through vendors and deepens dependency."),
    Relationship(
        "procurement_unbundles_ai", "moderator", ("procurement", "team"), 0.60,
        "AI shock: large, fast AI procurement deepens dependency unless contracts are unbundled",
        "AI-driven lock-in growth is multiplied by 1 - s * procurement intensity * talent gate."),
    Relationship(
        "safeguards_contain_ai_risk", "moderator", ("safeguards",), 0.70,
        "AI shock: errors and opaque automated decisions erode trust",
        "The AI hit to legitimacy is multiplied by 1 - s * safeguards intensity."),
    Relationship(
        "collaboration_cost_sharing", "cost_sharing", ("collaboration",), 0.40,
        "Success criterion 'scalable': pooled capacity for small jurisdictions",
        "Cuts the cost of shareable levers (team, insourcing, open source, maintenance, platforms) by s."),
)

NOT_ENCODED: dict[str, str] = {
    "Digital team vs. fellowships": "Fellowships are folded into the team lever, so the pair cannot be separated.",
}


def strengths(scale: float = 1.0, overrides: dict[str, float] | None = None) -> dict[str, float]:
    """Strength of each relationship, multiplied by `scale` (0 = menu baseline)."""
    values = {r.key: r.strength * scale for r in RELATIONSHIPS}
    for key, value in (overrides or {}).items():
        if key not in values:
            raise KeyError(f"Unknown relationship: {key}")
        values[key] = value
    return values
