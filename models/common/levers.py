"""Strategy levers used by the models, mapped to framework.md Section 4.

The framework lists about 40 strategies. The models group them into 15 levers
so that every combination (2**15 = 32,768 portfolios) can be simulated. Each
lever records which framework strategies it stands for, so the grouping can be
reviewed and changed.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Lever:
    key: str
    name: str
    framework_ids: tuple[str, ...]
    annual_cost: float
    """Share of a reference modernization budget used each year (model units)."""
    external_support: float
    """0 = delivered entirely by the jurisdiction, so it depends fully on local
    motivation; 1 = works like a default that others provide."""
    shareable: bool
    """True if collaboration between governments can share its cost."""
    description: str


LEVERS: tuple[Lever, ...] = (
    Lever("team", "Core digital team", ("A1", "A2", "A3", "A4", "A5"), 0.12, 0.0, True,
          "A core of skilled staff who lead products, oversee vendors, and act as an informed buyer; includes "
          "fellowships, hiring reform, upskilling, and product operating model. It does not by itself take over "
          "vendor work; that is the insourcing lever."),
    Lever("insourcing", "In-house delivery at scale (insourcing)", ("A6",), 0.03, 0.0, True,
          "Growing in-house staff to build and run work vendors do now. Programme overhead only; salaries are "
          "charged separately by the engine in proportion to in-house staff capacity."),
    Lever("authority", "Spend controls and service standards", ("B1", "B2", "B4"), 0.03, 0.0, False,
          "A central body that can approve or block spending and set service standards."),
    Lever("mandate", "Legal mandate (legislation)", ("B3",), 0.01, 0.0, False,
          "Digital duties and institutions written into law through legislation. Costs little to run but takes heavy political effort to pass (see EFFORT)."),
    Lever("funding", "Product (continuous) funding", ("C1", "C2"), 0.04, 0.0, False,
          "Stable annual funding for teams and services, including central modernization funds."),
    Lever("policy", "Policy and process simplification", ("D1", "D2"), 0.03, 0.0, False,
          "Simpler rules and fewer procedural barriers, with implementers involved in writing policy."),
    Lever("procurement", "Strategic and modular procurement", ("E1", "E2"), 0.03, 0.0, False,
          "Using awards and renewals for leverage, and splitting contracts into replaceable pieces."),
    Lever("portability", "Data rights and open interfaces", ("E5", "F3", "H1"), 0.02, 0.3, False,
          "Government ownership of data and documentation, open APIs, and interoperability mandates."),
    Lever("entrants", "New-entrant and mission-aligned vendor pipeline", ("E3", "E4", "E8", "E9"), 0.05, 0.0, False,
          "Marketplaces, challenge-based buying, startup pipelines, and public-benefit vendors."),
    Lever("open_source", "Open source by default", ("F1",), 0.04, 0.0, True,
          "Releasing and reusing public code."),
    Lever("maintenance", "Funding open source maintenance", ("F2",), 0.04, 0.0, True,
          "Paying for upkeep of the code public services depend on."),
    Lever("platforms", "Shared platforms (DPI building blocks)", ("F4", "F5"), 0.10, 0.5, True,
          "Common identity, payments, notifications, and data exchange, including digital public goods."),
    Lever("collaboration", "Collaboration between governments", ("I1", "I2", "I3", "E6"), 0.03, 0.5, False,
          "Jointly owned infrastructure, consortia, peer networks, and cooperative purchasing."),
    Lever("safeguards", "Accountability and safeguards", ("J1", "J2", "J3", "E7"), 0.04, 0.0, False,
          "Algorithm registers, impact assessments, accessibility, redress, and open contracting."),
    Lever("public_option", "Public option", ("G1", "G2"), 0.12, 0.0, False,
          "Government builds and runs the service or infrastructure itself."),
)

# Time, money, and effort each lever takes (1 = light, 2 = medium, 3 = heavy, 4 = very heavy), used for the website's
# investment limit. This is a separate judgment from annual_cost, which only counts budget spending in
# the engine: some levers cost little money but take years of political work.
EFFORT_REASONS: dict[str, tuple[int, str]] = {
    "team": (3, "Recruiting, paying, and keeping skilled staff."),
    "insourcing": (3, "Years of hiring and migrating work off vendor systems."),
    "authority": (2, "Setting up a central office and getting agencies to follow it."),
    "mandate": (4, "Legislation: building a majority and a coalition, often over more than one session."),
    "funding": (2, "Winning a stable budget line, and defending it every year."),
    "policy": (2, "Reviewing and rewriting rules, often with lawyers and policy staff."),
    "procurement": (2, "Redesigning contracts and building the skills to manage them."),
    "portability": (4, "Contract negotiation with entrenched vendors: often waits for renewal and can mean legal disputes."),
    "entrants": (2, "Running marketplaces and challenges, and supporting new vendors."),
    "open_source": (2, "Changing how code is bought, written, and published."),
    "maintenance": (1, "Mostly a steady budget line for upkeep."),
    "platforms": (3, "Building and running shared services many agencies depend on."),
    "collaboration": (2, "Agreeing on shared governance and budgets with other governments."),
    "safeguards": (2, "Registers, assessments, accessibility work, and ways to appeal."),
    "public_option": (3, "Building and running the whole service yourself."),
}
EFFORT: dict[str, int] = {key: level for key, (level, _) in EFFORT_REASONS.items()}
assert set(EFFORT) == {lever.key for lever in LEVERS}, "every lever needs an effort rating"

NOT_MODELED: dict[str, str] = {
    "H2": "Competition enforcement is usually outside the control of the jurisdiction delivering services.",
    "I4": "Civil society and civic tech capacity is external and hard to represent as a government choice.",
}

KEYS: tuple[str, ...] = tuple(lever.key for lever in LEVERS)
INDEX: dict[str, int] = {key: index for index, key in enumerate(KEYS)}
BY_KEY: dict[str, Lever] = {lever.key: lever for lever in LEVERS}


def mask_of(keys) -> int:
    """Bit mask for a set of lever keys (bit i = LEVERS[i])."""
    mask = 0
    for key in keys:
        mask |= 1 << INDEX[key]
    return mask


def keys_of(mask: int, keys: tuple[str, ...] = KEYS) -> tuple[str, ...]:
    return tuple(key for bit, key in enumerate(keys) if mask >> bit & 1)


def label(mask: int, keys: tuple[str, ...] = KEYS) -> str:
    return " + ".join(keys_of(mask, keys)) or "status quo"
