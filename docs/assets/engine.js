// A line-by-line JavaScript port of models/common/engine.py, so the website can run
// the model in the browser. Every number comes from docs/data/model.json, which
// models/export_site_data.py writes from the Python code. tests/site_engine.test.mjs
// checks that this file reproduces the Python engine exactly on deterministic cases.
// If you change the engine, change both files and rerun the export and the test.

export function strengths(model, scale = 1, overrides = {}) {
  const values = {};
  for (const r of model.relationships) values[r.key] = r.strength * scale;
  for (const [key, value] of Object.entries(overrides)) {
    if (!(key in values)) throw new Error(`Unknown relationship: ${key}`);
    values[key] = value;
  }
  return values;
}

// Small seeded random number generator (mulberry32) so results are reproducible.
function mulberry32(seed) {
  let a = seed >>> 0;
  return () => {
    a = (a + 0x6d2b79f5) >>> 0;
    let t = a;
    t = Math.imul(t ^ (t >>> 15), t | 1);
    t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

function draws(seed, years, trials, nLevers, p) {
  const rand = mulberry32(seed);
  const normal = () => {
    const u = Math.max(rand(), 1e-12);
    return Math.sqrt(-2 * Math.log(u)) * Math.cos(2 * Math.PI * rand());
  };
  const grid = (fn) => Array.from({ length: years }, () => Array.from({ length: trials }, fn));
  return {
    noise: grid(() => normal() * p.quality_noise),
    turnover: grid(() => rand() < p.turnover_probability),
    hostility: grid(() => rand()),
    idiosyncratic: Array.from({ length: years }, () =>
      Array.from({ length: nLevers }, () => Array.from({ length: trials }, () => rand()))),
  };
}

const clip = (v, lo, hi) => Math.min(hi, Math.max(lo, v));
const gate = (state, strength) => 1 - strength * (1 - state);

/**
 * Simulate one portfolio for one jurisdiction type.
 * options: { levers: [keys], jurisdiction: key or object, years, trials, seed, turnover,
 *            relationshipScale, relationshipOverrides, vendorAction, params, aiShockYear,
 *            aiStrength, startYears: {key: year} }
 */
export function simulate(model, options = {}) {
  const {
    levers = [], years = 16, trials = 30, seed = 1, turnover = false, relationshipScale = 1,
    relationshipOverrides = {}, vendorAction = "lock_in", params = {}, aiShockYear = null,
    aiStrength = 1, startYears = {},
  } = options;
  const j = typeof options.jurisdiction === "string"
    ? model.jurisdictions.find((x) => x.key === options.jurisdiction)
    : options.jurisdiction || model.jurisdictions[0];
  const p = { ...model.params, ...params };
  const rel = strengths(model, relationshipScale, relationshipOverrides);
  const keys = model.levers.map((l) => l.key);
  const ix = Object.fromEntries(keys.map((k, i) => [k, i]));
  const nLev = keys.length;
  const selected = new Set(levers);
  const start = keys.map((k) => (selected.has(k) ? (startYears[k] ?? 0) : Infinity));
  const cost = model.levers.map((l) => l.annual_cost);
  const shareable = model.levers.map((l) => l.shareable);
  const fidelity = model.levers.map((l) => j.motivation + (1 - j.motivation) * l.external_support);
  const embed = keys.map((k) => model.embeddedness[k] ?? 0);
  const init = model.initial;
  const renewal = Math.round(p.renewal_period);
  const election = Math.round(p.election_period);
  const rnd = draws(seed, years, trials, nLev, p);

  const sums = { outcome: 0, spend: 0, vendor: 0, survival: 0 };
  const finalsSum = {};
  const pathSum = { outcome: [], insourced: [], staff: [], lock_in: [], ai_absorbed: [] };
  for (const name of Object.keys(pathSum)) pathSum[name] = new Array(years).fill(0);
  const nAdopted = start.filter((s) => s < Infinity).length;

  for (let n = 0; n < trials; n++) {
    let T = j.talent0, A = j.authority0, F = init.funding, Pf = j.policy_fit0;
    let I = init.infrastructure, Port = init.portability, C = init.competition, K = j.lock_in0;
    let Lg = init.legitimacy, Q = init.quality, R = init.reach, H = 0, S = 0, retained = 1;
    const outcome0 = 0.6 * Q + 0.4 * R;
    let outcomeSum = 0, spendSum = 0, vendorSum = 0;
    const alive = new Array(nLev).fill(true);

    for (let t = 0; t < years; t++) {
      const on = keys.map((_, l) => start[l] <= t && alive[l]);
      const collabOn = on[ix.collaboration] ? 1 : 0;
      let total = 0;
      for (let l = 0; l < nLev; l++) {
        if (on[l]) total += cost[l] * (shareable[l] ? 1 - rel.collaboration_cost_sharing * collabOn : 1);
      }
      const budget = j.budget;
      const coverage = Math.min(1, budget / Math.max(total, 1e-9));
      const x = keys.map((_, l) => (on[l] ? coverage * fidelity[l] : 0));
      const v = (k) => x[ix[k]];
      const team = v("team"), authority = v("authority"), mandate = v("mandate"), funding = v("funding");
      const policy = v("policy"), procurement = v("procurement"), portability = v("portability");
      const entrants = v("entrants"), oss = v("open_source"), maintenance = v("maintenance");
      const platforms = v("platforms"), collaboration = v("collaboration");
      const safeguards = v("safeguards"), pub = v("public_option");
      const insourcing = v("insourcing"), insourcingOn = on[ix.insourcing] ? 1 : 0;

      // AI shock: absorbed share uses last year's states; the rest arrives through vendors.
      let ai = 0;
      if (aiShockYear !== null && aiShockYear !== undefined && t >= aiShockYear) {
        ai = aiStrength * (1 - Math.exp(-(t - aiShockYear + 1) / p.ai_ramp));
      }
      const absorb = clip(rel.capacity_absorbs_ai * (p.ai_w_talent * T + p.ai_w_portability * Port
        + p.ai_w_infra * I + p.ai_w_insourced * S), 0, 1);
      const captured = ai * (1 - absorb);

      // Talent and skills
      T = T + (p.baseline_hiring + p.team_rate * team + p.collab_talent * collaboration) * (1 - T)
        - p.attrition * (1 - rel.funding_retains_talent * funding) * T;
      // In-house delivery: scope, scale, pace
      const productivity = 1 + p.ai_productivity * ai * absorb;
      const ceiling = clip(j.insource_ceiling + rel.pooling_extends_scope * (collaboration + I)
        + p.ai_scope * ai * absorb, 0, 1) * insourcingOn;
      const hireCap = p.hire_rate_max * j.hiring_pipeline * (1 + rel.team_speeds_hiring * team) * insourcing;
      const hire = Math.min(hireCap, Math.max(0, ceiling / productivity - H));
      const leave = insourcingOn ? p.inhouse_attrition * (1 - rel.funding_retains_talent * funding) : p.cut_attrition;
      H = clip(H + hire - leave * H, 0, 1);
      const speed = p.transition_speed * gate(T, rel.core_team_gates_insourcing);
      let Snext = S + clip(Math.min(H * productivity, ceiling) - S, -p.return_speed, speed);
      Snext = clip(Math.min(Snext, H * productivity), 0, 1);
      const moved = Math.abs(Snext - S);
      S = Snext;
      const vendorShare = 1 - S;

      // Authority and funding stability
      A = A + (p.authority_rate * authority + p.mandate_authority * mandate) * (1 - A) - p.authority_decay * A;
      F = F + p.funding_adjust * (p.funding_base + p.funding_lever * funding + p.funding_mandate * mandate - F);
      // Policy and process fit
      Pf = Pf + p.policy_rate * policy * (1 - Pf) - p.rule_accretion * Pf;
      // Infrastructure and reuse
      const platformGrowth = p.platform_rate * platforms * (1 + rel.platforms_need_authority * authority)
        * (1 + rel.platforms_need_funding * funding);
      I = I + (platformGrowth + p.collab_infra * collaboration) * (1 - I) - p.infra_decay * I;
      // Portability
      const ossEffect = p.oss_rate * oss * gate(maintenance, rel.open_source_needs_maintenance);
      Port = Port + (ossEffect + p.portability_rate * portability + rel.portability_stack * oss * portability) * (1 - Port)
        - p.portability_decay * (1 - maintenance) * Port;
      // Competition
      const talentGate = gate(T, rel.talent_gates_procurement);
      const entry = p.entry_rate * entrants * gate(Port, rel.entrants_need_portability)
        * (1 - rel.public_option_crowds_out_entrants * pub);
      const modular = p.modular_competition * procurement * talentGate * (1 - rel.cooperative_vs_modular * collaboration);
      const extraAcquired = vendorAction === "acquire_entrants" ? 0.20 * (1 - Port) * C : 0;
      C = C + (entry + modular) * (1 - C) - p.consolidation * C - extraAcquired;
      // Vendor lock-in
      if (vendorAction === "adapt") K = K - 0.02 * K;
      else if (vendorAction === "lowball") K = K + (t < renewal ? 0.01 : 0.07) * (1 - K);
      else K = K + 0.04 * (1 - K);
      if (t % renewal === renewal - 1) {
        const leverage = p.lev_base + p.lev_talent * T + p.lev_procurement * procurement * talentGate
          + p.lev_portability * Port + p.lev_competition * C + p.lev_insourcing * S;
        K = K - p.renewal_effect * leverage * K;
        let loss = clip(leverage - p.replacement_threshold, 0, 1) * p.replacement_rate;
        if (vendorAction === "adapt" || (vendorAction === "lowball" && t < renewal)) loss *= p.adapt_retention;
        retained *= 1 - loss;
      }
      K = K + p.ai_lock_in * captured * (1 - rel.procurement_unbundles_ai * procurement * talentGate) * (1 - K);
      C = clip(C - p.ai_concentration * captured * C, 0, 1);
      K = clip(K - p.public_option_rate * pub * K, 0.02, 0.98);
      const lock = K * vendorShare;
      // Outcomes
      const binding = gate(Pf, rel.policy_binding_constraint) * (1 - rel.lock_in_limits_change * lock);
      const vendorQuality = ({ adapt: 0.010, lowball: -0.002 }[vendorAction] ?? -0.004) * vendorShare;
      Q = Q + binding * (p.q_talent * T * (1 - rel.spend_controls_slow_teams * authority) + p.q_infra * I
        + p.q_competition * C + p.q_inhouse * S * T + p.q_ai_governed * ai * absorb + p.q_ai_vendor * captured)
        + vendorQuality - p.q_lock_in * lock - p.q_drift * (Q - p.q_anchor)
        - p.transition_disruption * moved * (1 - T) + rnd.noise[t][n];
      Q = clip(Q, 0.05, 0.98);
      R = R + binding * (p.r_safeguards * safeguards + p.r_infra * I + p.r_policy * Pf + p.r_ai * ai * absorb) * (1 - R)
        - p.r_drift * R;
      Lg = Lg + (p.safeguard_rate * safeguards + p.standards_legitimacy * authority) * (1 - Lg)
        + p.results_legitimacy * (Q - init.quality) - p.legitimacy_decay * (Lg - p.legitimacy_anchor)
        - p.ai_risk * ai * (1 - rel.safeguards_contain_ai_risk * safeguards);
      T = clip(T, 0, 1); A = clip(A, 0, 1); Pf = clip(Pf, 0, 1); I = clip(I, 0, 1);
      Port = clip(Port, 0, 1); C = clip(C, 0, 1); R = clip(R, 0, 1); Lg = clip(Lg, 0, 1);

      outcomeSum += 0.6 * Q + 0.4 * R - outcome0;
      const premium = p.vendor_premium * K * (vendorAction === "lowball" && t < renewal ? 0.5 : 1);
      spendSum += Math.min(total, budget) / budget + p.contract_size
        * (vendorShare * (1 + premium) + p.inhouse_unit_cost * H + p.ai_vendor_spend * captured);
      let revenue = vendorShare * (0.45 + 0.35 * K + 0.15 * Q - 0.30 * C) + p.ai_vendor_revenue * captured;
      if (vendorAction === "lowball" && t < renewal) revenue -= 0.10;
      if (vendorAction === "adapt") revenue -= 0.04;
      vendorSum += retained * revenue - p.acquisition_cost * extraAcquired;

      pathSum.outcome[t] += 100 * (0.6 * Q + 0.4 * R - outcome0);
      pathSum.insourced[t] += S;
      pathSum.staff[t] += H;
      pathSum.lock_in[t] += K;
      pathSum.ai_absorbed[t] += ai > 0 ? absorb : 0;

      // Political turnover at the end of each term
      if (turnover && t % election === election - 1) {
        const protection = p.status_quo_bias + rel.mandate_protects * mandate + rel.funding_protects * F
          + rel.legitimacy_protects * Lg;
        for (let l = 0; l < nLev; l++) {
          const pressure = p.hostility_weight * rnd.hostility[t][n] + (1 - p.hostility_weight) * rnd.idiosyncratic[t][l][n];
          if (rnd.turnover[t][n] && on[l] && pressure > protection + embed[l]) alive[l] = false;
        }
      }
    }

    sums.outcome += (100 * outcomeSum) / years;
    sums.spend += spendSum / years;
    sums.vendor += (100 * vendorSum) / years;
    if (nAdopted > 0) {
      sums.survival += keys.filter((_, l) => start[l] <= years - 1 && alive[l]).length / nAdopted;
    }
    const finals = { talent: T, authority: A, funding: F, policy_fit: Pf, infrastructure: I, portability: Port,
      competition: C, lock_in: K, legitimacy: Lg, quality: Q, reach: R, insourced: S, staff: H };
    for (const [name, value] of Object.entries(finals)) finalsSum[name] = (finalsSum[name] ?? 0) + value;
  }

  const mean = (x) => x / trials;
  return {
    outcomeGain: mean(sums.outcome),
    spendShare: mean(sums.spend),
    vendorPayoff: mean(sums.vendor),
    survival: nAdopted > 0 ? mean(sums.survival) : null,
    finals: Object.fromEntries(Object.entries(finalsSum).map(([k, s]) => [k, mean(s)])),
    paths: Object.fromEntries(Object.entries(pathSum).map(([k, arr]) => [k, arr.map(mean)])),
  };
}

/**
 * Net value of a portfolio over the status quo, matching models/capacity_portfolio/run.py:
 * outcome gain minus cost_weight x extra spending (share of the jurisdiction's own budget).
 */
export function netValue(model, options = {}) {
  const w = options.costWeight ?? model.defaults.cost_weight;
  const run = simulate(model, options);
  const base = simulate(model, { ...options, levers: [], startYears: {} });
  return {
    value: run.outcomeGain - w * run.spendShare - (base.outcomeGain - w * base.spendShare),
    outcome: run.outcomeGain - base.outcomeGain,
    spend: run.spendShare - base.spendShare,
    run,
    base,
  };
}
