"""Capacity dynamics engine shared by the models.

One jurisdiction is simulated year by year. All state variables are indices
from 0 to 1. The engine is vectorized: it runs many portfolios (rows) and many
Monte Carlo trials (columns) at once, using the same random draws for every
portfolio (common random numbers), so differences between portfolios reflect
the portfolios rather than luck.

State variables, mapped to framework.md Section 2:
    talent (T)          Talent and skills
    authority (A)       Authority and governance
    funding (F)         Funding model (stability of funding)
    policy_fit (Pf)     Policy and process fit
    infrastructure (I)  Infrastructure and reuse
    legitimacy (Lg)     Legitimacy and accountability
    portability, competition, lock_in   Market power (Section 3, constraint 1)
    quality (Q), reach (R)              Outcomes people experience

Outcome index = 0.6 * quality + 0.4 * reach, reported as the average gain over
the horizon in points (0-100 scale). Spending (lever costs plus the lock-in
premium on vendor contracts) is reported separately as a share of the
jurisdiction's budget, so models can weigh value for money.

Parameters in PARAMS are main effects. Deliberate interactions between levers
come only from models/common/relationships.py. All numbers are illustrative
assumptions for theory-building and need calibration.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from . import levers as lv
from .jurisdictions import Jurisdiction
from .relationships import strengths

PARAMS: dict[str, float] = {
    # Talent
    "team_rate": 0.14, "collab_talent": 0.04, "baseline_hiring": 0.02, "attrition": 0.08,
    # Authority and funding
    "authority_rate": 0.15, "mandate_authority": 0.05, "authority_decay": 0.05,
    "funding_base": 0.20, "funding_lever": 0.60, "funding_mandate": 0.10, "funding_adjust": 0.30,
    # Policy fit
    "policy_rate": 0.10, "rule_accretion": 0.02,
    # Infrastructure
    "platform_rate": 0.10, "collab_infra": 0.04, "infra_decay": 0.04,
    # Market
    "oss_rate": 0.10, "portability_rate": 0.10, "portability_decay": 0.04,
    "entry_rate": 0.10, "modular_competition": 0.04, "consolidation": 0.05,
    "renewal_effect": 0.30, "lev_base": 0.05, "lev_talent": 0.15, "lev_procurement": 0.35,
    "lev_portability": 0.20, "lev_competition": 0.15, "public_option_rate": 0.06,
    # Vendor contract spending (value for money): annual contract = contract_size x budget,
    # with a lock-in premium of vendor_premium x lock_in on top.
    "contract_size": 1.0, "vendor_premium": 0.40,
    # Incumbent's risk of losing the contract at renewal when government leverage is high.
    "replacement_threshold": 0.20, "replacement_rate": 0.60, "adapt_retention": 0.40,
    "acquisition_cost": 2.0,
    # In-house delivery at scale (insourcing): scope, scale, pace.
    # Staff capacity H and insourced share S are both measured as shares of the work vendors do today.
    "hire_rate_max": 0.05,          # scale: most staff capacity that can be hired per year (x hiring pipeline)
    "inhouse_attrition": 0.10,      # yearly staff loss while the programme runs
    "cut_attrition": 0.35,          # yearly staff loss after the programme is cut
    "transition_speed": 0.08,       # pace: most work that can move in-house per year
    "return_speed": 0.25,           # how fast work goes back to vendors when capacity falls
    "transition_disruption": 0.30,  # quality lost per unit of work moved, x (1 - talent)
    "inhouse_unit_cost": 0.85,      # in-house cost per unit of work, relative to the vendor's base price
    "q_inhouse": 0.03, "lev_insourcing": 0.30,
    # AI shock (scenario, not a lever). The share of AI capability the government absorbs itself
    # depends on talent, portability, shared infrastructure, and insourced delivery; the rest
    # arrives through vendors.
    "ai_ramp": 2.0, "ai_w_talent": 0.35, "ai_w_portability": 0.25, "ai_w_infra": 0.20, "ai_w_insourced": 0.20,
    "ai_productivity": 1.0,         # extra work each in-house staff unit can carry at full AI strength
    "ai_scope": 0.20,               # rise in the insourcing ceiling at full AI strength
    "q_ai_governed": 0.030, "r_ai": 0.05,            # gains when AI is absorbed by public capacity
    "q_ai_vendor": 0.012,                             # gains when AI arrives through vendors
    "ai_lock_in": 0.10, "ai_concentration": 0.06,     # dependency when AI arrives through vendors
    "ai_vendor_spend": 0.10, "ai_vendor_revenue": 0.15, "ai_risk": 0.04,
    # Legitimacy
    "safeguard_rate": 0.10, "standards_legitimacy": 0.03, "results_legitimacy": 0.05,
    "legitimacy_decay": 0.03, "legitimacy_anchor": 0.40,
    # Quality and reach
    "q_talent": 0.050, "q_infra": 0.040, "q_competition": 0.025, "q_lock_in": 0.020,
    "q_drift": 0.02, "q_anchor": 0.45, "quality_noise": 0.008,
    "r_safeguards": 0.06, "r_infra": 0.10, "r_policy": 0.04, "r_drift": 0.025,
    # Political turnover (durability)
    "renewal_period": 4, "election_period": 4, "turnover_probability": 0.5,
    "status_quo_bias": 0.15, "hostility_weight": 0.6,
}

# How hard it is to undo each lever once in place, independent of other levers.
EMBEDDEDNESS: dict[str, float] = {
    "mandate": 0.30, "open_source": 0.30, "collaboration": 0.25, "platforms": 0.20,
    "portability": 0.10, "insourcing": 0.10,
}

VENDOR_ACTIONS: tuple[str, ...] = ("lock_in", "adapt", "lowball", "acquire_entrants")

INITIAL = {"funding": 0.20, "infrastructure": 0.10, "portability": 0.10, "competition": 0.12,
           "legitimacy": 0.45, "quality": 0.50, "reach": 0.45}


@dataclass
class Result:
    outcome_gain: np.ndarray
    outcome_gain_se: np.ndarray
    final_gain: np.ndarray
    annual_cost: np.ndarray
    spend_share: np.ndarray
    """Lever spending plus vendor lock-in premium, as a share of the jurisdiction's budget per year."""
    survival: np.ndarray
    vendor_payoff: np.ndarray
    finals: dict[str, np.ndarray]
    paths: dict[str, np.ndarray] | None = None
    """Per-year means (portfolios x years) of insourced share, staff capacity, outcome gain, and AI
    absorption, when record_paths=True."""


def portfolio_matrix(masks, keys=lv.KEYS) -> np.ndarray:
    """Boolean matrix (portfolios x all engine levers) from bit masks over `keys`."""
    masks = np.asarray(masks, dtype=np.int64)
    matrix = np.zeros((masks.size, len(lv.KEYS)), dtype=bool)
    for bit, key in enumerate(keys):
        matrix[:, lv.INDEX[key]] = (masks >> bit) & 1
    return matrix


def _gate(state, strength):
    """Prerequisite gate: 1 when the prerequisite is fully met, 1 - strength when absent."""
    return 1.0 - strength * (1.0 - state)


def simulate(
    portfolios: np.ndarray,
    jurisdiction: Jurisdiction,
    *,
    years: int = 16,
    trials: int = 40,
    seed: int = 0,
    turnover: bool = False,
    relationship_scale: float = 1.0,
    relationship_overrides: dict[str, float] | None = None,
    start_years: np.ndarray | None = None,
    vendor_action: str = "lock_in",
    params: dict[str, float] | None = None,
    ai_shock_year: int | None = None,
    ai_strength: float = 1.0,
    record_paths: bool = False,
) -> Result:
    """Simulate each portfolio (row of `portfolios`) for one jurisdiction type."""
    p = {**PARAMS, **(params or {})}
    rel = strengths(relationship_scale, relationship_overrides)
    portfolios = np.asarray(portfolios, dtype=bool)
    n_port, n_lev = portfolios.shape
    assert n_lev == len(lv.LEVERS)
    if vendor_action not in VENDOR_ACTIONS:
        raise ValueError(f"Unknown vendor action: {vendor_action}")

    rng = np.random.default_rng(seed)
    quality_noise = rng.normal(0.0, p["quality_noise"], size=(years, trials))
    turnover_draw = rng.random((years, trials)) < p["turnover_probability"]
    hostility = rng.random((years, trials))
    idiosyncratic = rng.random((years, n_lev, trials))

    start = np.where(portfolios, 0 if start_years is None else start_years, np.inf)
    start = start.T[:, :, None]  # levers x portfolios x 1
    alive = np.ones((n_lev, n_port, trials), dtype=bool)

    costs = np.array([lever.annual_cost for lever in lv.LEVERS])[:, None, None]
    shareable = np.array([lever.shareable for lever in lv.LEVERS])[:, None, None]
    fidelity = np.array([
        jurisdiction.motivation + (1 - jurisdiction.motivation) * lever.external_support
        for lever in lv.LEVERS])[:, None, None]
    embed = np.array([EMBEDDEDNESS.get(key, 0.0) for key in lv.KEYS])[:, None, None]
    ix = lv.INDEX

    def full(value):
        return np.full((n_port, trials), float(value))

    T, A = full(jurisdiction.talent0), full(jurisdiction.authority0)
    F, Pf = full(INITIAL["funding"]), full(jurisdiction.policy_fit0)
    I, Port = full(INITIAL["infrastructure"]), full(INITIAL["portability"])
    C, K = full(INITIAL["competition"]), full(jurisdiction.lock_in0)
    Lg, Q, R = full(INITIAL["legitimacy"]), full(INITIAL["quality"]), full(INITIAL["reach"])
    outcome0 = 0.6 * Q + 0.4 * R
    outcome_sum = np.zeros((n_port, trials))
    cost_sum = np.zeros((n_port, trials))
    spend_sum = np.zeros((n_port, trials))
    vendor_sum = np.zeros((n_port, trials))
    retained = np.ones((n_port, trials))  # incumbent's expected share of the contract
    H, S = full(0.0), full(0.0)  # in-house staff capacity and insourced share of vendor work
    paths = {"insourced": [], "staff": [], "outcome": [], "ai_absorbed": []} if record_paths else None
    renewal = int(p["renewal_period"])

    for t in range(years):
        on = (start <= t) & alive
        lever_cost = on * costs * np.where(shareable, 1 - rel["collaboration_cost_sharing"] * on[ix["collaboration"]], 1)
        total_cost = lever_cost.sum(axis=0)
        budget = jurisdiction.budget
        coverage = np.minimum(1.0, budget / np.maximum(total_cost, 1e-9))
        x = on * coverage[None] * fidelity
        team, authority, mandate, funding = (x[ix[k]] for k in ("team", "authority", "mandate", "funding"))
        policy, procurement, portability = (x[ix[k]] for k in ("policy", "procurement", "portability"))
        entrants, oss, maintenance = (x[ix[k]] for k in ("entrants", "open_source", "maintenance"))
        platforms, collaboration = x[ix["platforms"]], x[ix["collaboration"]]
        safeguards, public = x[ix["safeguards"]], x[ix["public_option"]]
        insourcing, insourcing_on = x[ix["insourcing"]], on[ix["insourcing"]]

        # AI shock: strength ramps up after the shock year. `absorb` is the share the government
        # absorbs with its own capacity (last year's states); the rest arrives through vendors.
        ai = 0.0
        if ai_shock_year is not None and t >= ai_shock_year:
            ai = ai_strength * (1 - np.exp(-(t - ai_shock_year + 1) / p["ai_ramp"]))
        absorb = np.clip(rel["capacity_absorbs_ai"] * (p["ai_w_talent"] * T + p["ai_w_portability"] * Port
                                                       + p["ai_w_infra"] * I + p["ai_w_insourced"] * S), 0, 1)
        captured = ai * (1 - absorb)

        # Talent and skills
        T = T + (p["baseline_hiring"] + p["team_rate"] * team + p["collab_talent"] * collaboration) * (1 - T) \
            - p["attrition"] * (1 - rel["funding_retains_talent"] * funding) * T
        # In-house delivery: scope (ceiling), scale (hiring and attrition), pace (transition speed)
        productivity = 1 + p["ai_productivity"] * ai * absorb
        ceiling = np.clip(jurisdiction.insource_ceiling + rel["pooling_extends_scope"] * (collaboration + I)
                          + p["ai_scope"] * ai * absorb, 0, 1) * insourcing_on
        hire_cap = p["hire_rate_max"] * jurisdiction.hiring_pipeline * (1 + rel["team_speeds_hiring"] * team) * insourcing
        hire = np.minimum(hire_cap, np.maximum(0, ceiling / productivity - H))
        leave = np.where(insourcing_on, p["inhouse_attrition"] * (1 - rel["funding_retains_talent"] * funding),
                         p["cut_attrition"])
        H = np.clip(H + hire - leave * H, 0, 1)
        speed = p["transition_speed"] * _gate(T, rel["core_team_gates_insourcing"])
        S_next = S + np.clip(np.minimum(H * productivity, ceiling) - S, -p["return_speed"], speed)
        S_next = np.clip(np.minimum(S_next, H * productivity), 0, 1)
        moved = np.abs(S_next - S)
        S = S_next
        vendor_share = 1 - S

        # Authority and funding stability
        A = A + (p["authority_rate"] * authority + p["mandate_authority"] * mandate) * (1 - A) \
            - p["authority_decay"] * A
        F = F + p["funding_adjust"] * (p["funding_base"] + p["funding_lever"] * funding
                                       + p["funding_mandate"] * mandate - F)
        # Policy and process fit
        Pf = Pf + p["policy_rate"] * policy * (1 - Pf) - p["rule_accretion"] * Pf
        # Infrastructure and reuse
        platform_growth = p["platform_rate"] * platforms * (1 + rel["platforms_need_authority"] * authority) \
            * (1 + rel["platforms_need_funding"] * funding)
        I = I + (platform_growth + p["collab_infra"] * collaboration) * (1 - I) - p["infra_decay"] * I
        # Portability
        oss_effect = p["oss_rate"] * oss * _gate(maintenance, rel["open_source_needs_maintenance"])
        Port = Port + (oss_effect + p["portability_rate"] * portability
                       + rel["portability_stack"] * oss * portability) * (1 - Port) \
            - p["portability_decay"] * (1 - maintenance) * Port
        # Competition
        talent_gate = _gate(T, rel["talent_gates_procurement"])
        entry = p["entry_rate"] * entrants * _gate(Port, rel["entrants_need_portability"]) \
            * (1 - rel["public_option_crowds_out_entrants"] * public)
        modular = p["modular_competition"] * procurement * talent_gate \
            * (1 - rel["cooperative_vs_modular"] * collaboration)
        extra_acquired = (0.20 * (1 - Port) * C) if vendor_action == "acquire_entrants" else 0.0
        C = C + (entry + modular) * (1 - C) - p["consolidation"] * C - extra_acquired
        # Vendor lock-in
        if vendor_action == "adapt":
            K = K - 0.02 * K
        elif vendor_action == "lowball":
            K = K + (0.01 if t < renewal else 0.07) * (1 - K)
        else:
            K = K + 0.04 * (1 - K)
        if t % renewal == renewal - 1:
            leverage = p["lev_base"] + p["lev_talent"] * T + p["lev_procurement"] * procurement * talent_gate \
                + p["lev_portability"] * Port + p["lev_competition"] * C + p["lev_insourcing"] * S
            K = K - p["renewal_effect"] * leverage * K
            loss = np.clip(leverage - p["replacement_threshold"], 0, 1) * p["replacement_rate"]
            if vendor_action == "adapt" or (vendor_action == "lowball" and t < renewal):
                loss = loss * p["adapt_retention"]
            retained = retained * (1 - loss)
        K = K + p["ai_lock_in"] * captured * (1 - rel["procurement_unbundles_ai"] * procurement * talent_gate) * (1 - K)
        C = np.clip(C - p["ai_concentration"] * captured * C, 0, 1)
        K = np.clip(K - p["public_option_rate"] * public * K, 0.02, 0.98)
        lock = K * vendor_share  # lock-in only binds on work still done by vendors
        # Outcomes
        binding = _gate(Pf, rel["policy_binding_constraint"]) * (1 - rel["lock_in_limits_change"] * lock)
        vendor_quality = {"adapt": 0.010, "lowball": -0.002}.get(vendor_action, -0.004) * vendor_share
        Q = Q + binding * (p["q_talent"] * T * (1 - rel["spend_controls_slow_teams"] * authority)
                           + p["q_infra"] * I + p["q_competition"] * C + p["q_inhouse"] * S * T
                           + p["q_ai_governed"] * ai * absorb + p["q_ai_vendor"] * captured) \
            + vendor_quality - p["q_lock_in"] * lock - p["q_drift"] * (Q - p["q_anchor"]) \
            - p["transition_disruption"] * moved * (1 - T) + quality_noise[t]
        Q = np.clip(Q, 0.05, 0.98)
        R = R + binding * (p["r_safeguards"] * safeguards + p["r_infra"] * I + p["r_policy"] * Pf
                           + p["r_ai"] * ai * absorb) * (1 - R) - p["r_drift"] * R
        Lg = Lg + (p["safeguard_rate"] * safeguards + p["standards_legitimacy"] * authority) * (1 - Lg) \
            + p["results_legitimacy"] * (Q - INITIAL["quality"]) - p["legitimacy_decay"] * (Lg - p["legitimacy_anchor"]) \
            - p["ai_risk"] * ai * (1 - rel["safeguards_contain_ai_risk"] * safeguards)
        T, A, Pf, I, Port, C, R, Lg = (np.clip(v, 0.0, 1.0) for v in (T, A, Pf, I, Port, C, R, Lg))

        outcome_sum += 0.6 * Q + 0.4 * R - outcome0
        premium = p["vendor_premium"] * K * (0.5 if vendor_action == "lowball" and t < renewal else 1.0)
        cost_sum += np.minimum(total_cost, budget)
        spend_sum += np.minimum(total_cost, budget) / budget + p["contract_size"] * (
            vendor_share * (1 + premium) + p["inhouse_unit_cost"] * H + p["ai_vendor_spend"] * captured)
        revenue = vendor_share * (0.45 + 0.35 * K + 0.15 * Q - 0.30 * C) + p["ai_vendor_revenue"] * captured
        if vendor_action == "lowball" and t < renewal:
            revenue = revenue - 0.10
        if vendor_action == "adapt":
            revenue = revenue - 0.04
        vendor_sum += retained * revenue - p["acquisition_cost"] * extra_acquired
        if record_paths:
            paths["insourced"].append(S.mean(axis=1))
            paths["staff"].append(H.mean(axis=1))
            paths["outcome"].append(100 * (0.6 * Q + 0.4 * R - outcome0).mean(axis=1))
            paths["ai_absorbed"].append((absorb * (ai > 0)).mean(axis=1) if np.ndim(absorb) else np.zeros(n_port))

        # Political turnover at the end of each term
        if turnover and t % int(p["election_period"]) == int(p["election_period"]) - 1:
            protection = (p["status_quo_bias"] + rel["mandate_protects"] * mandate
                          + rel["funding_protects"] * F + rel["legitimacy_protects"] * Lg)[None] + embed
            pressure = p["hostility_weight"] * hostility[t] + (1 - p["hostility_weight"]) * idiosyncratic[t][:, None, :]
            dismantle = turnover_draw[t][None, None, :] & (pressure > protection)
            alive &= ~(dismantle & on)

    adopted = (start[:, :, 0] < np.inf)
    alive_end = alive & (start <= years - 1)
    n_adopted = adopted.sum(axis=0)
    survival = alive_end.sum(axis=0).mean(axis=1) / np.maximum(n_adopted, 1)
    survival = np.where(n_adopted > 0, survival, np.nan)
    outcome = 100 * outcome_sum / years
    return Result(
        outcome_gain=outcome.mean(axis=1),
        outcome_gain_se=outcome.std(axis=1, ddof=1) / np.sqrt(trials) if trials > 1 else np.zeros(n_port),
        final_gain=100 * (0.6 * Q + 0.4 * R - outcome0).mean(axis=1),
        annual_cost=(cost_sum / years).mean(axis=1),
        spend_share=(spend_sum / years).mean(axis=1),
        survival=survival,
        vendor_payoff=(100 * vendor_sum / years).mean(axis=1),
        finals={name: value.mean(axis=1) for name, value in (
            ("talent", T), ("authority", A), ("funding", F), ("policy_fit", Pf), ("infrastructure", I),
            ("portability", Port), ("competition", C), ("lock_in", K), ("legitimacy", Lg),
            ("quality", Q), ("reach", R), ("insourced", S), ("staff", H))},
        paths={k: np.array(v).T for k, v in paths.items()} if record_paths else None,
    )
