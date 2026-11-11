// The model's scores for every possible plan, written by models/export_site_data.py (write_scores).
// The results page looks up the visitor's plan here and builds its comparison group in the browser,
// using the visitor's own effort ratings, so the comparison always matches what they chose.

let DATA = null;

export async function loadScores(model) {
  const buffer = await fetch(`data/${model.scores.file}`).then((r) => {
    if (!r.ok) throw new Error(`Could not load ${model.scores.file}`);
    return r.arrayBuffer();
  });
  const view = new DataView(buffer);
  const values = new Int16Array(buffer.byteLength / 2);
  for (let i = 0; i < values.length; i++) values[i] = view.getInt16(i * 2, true); // stored little-endian
  const s = model.scores;
  if (values.length !== s.agencies.length * s.conditions.length * s.measures.length * s.plans) {
    throw new Error("scores.bin does not match model.json; rerun python -m models.export_site_data");
  }
  DATA = { values, spec: s, keys: model.levers.map((l) => l.key), cache: new Map() };
}

export const maskOf = (plan) => plan.reduce((m, k) => m | (1 << DATA.keys.indexOf(k)), 0);
const keysOf = (mask) => DATA.keys.filter((_, i) => mask >> i & 1);

function raw(agency, condition, measure, mask) {
  const s = DATA.spec;
  const a = s.agencies.indexOf(agency), c = s.conditions.indexOf(condition), m = s.measures.indexOf(measure);
  return DATA.values[((a * s.conditions.length + c) * s.measures.length + m) * s.plans + mask] / 100;
}

/** Net value over doing nothing: outcome gain minus weighted extra spending (as in the Python models). */
export function value(agency, condition, mask, costWeight) {
  const v = (m) => raw(agency, condition, "outcome_gain", m) - costWeight * raw(agency, condition, "spend_share", m);
  return v(mask) - v(0);
}

export const survival = (agency, mask) => raw(agency, "turnover", "survival", mask);

/** Score of a plan for one goal. "scalable" is the score in the agency type where it works worst. */
export function goalScore(goal, agency, mask, costWeight) {
  if (goal === "positive") return value(agency, "stable", mask, costWeight);
  if (goal === "durable") return value(agency, "turnover", mask, costWeight);
  return Math.min(...DATA.spec.agencies.map((a) => value(a, "stable", mask, costWeight)));
}

export function weakestAgency(mask, costWeight) {
  return DATA.spec.agencies.reduce((best, a) => {
    const v = value(a, "stable", mask, costWeight);
    return !best || v < best.v ? { a, v } : best;
  }, null).a;
}

export const effortOfMask = (mask, effort) => keysOf(mask).reduce((sum, k) => sum + effort[k], 0);

/**
 * Median, top-tenth, and best scores among every plan with the same number of strategies that fits the
 * investment limit under the given effort ratings. Returns null if no plan of that size fits.
 */
export function comparison(goal, agency, size, limit, effort, costWeight) {
  const key = [goal, agency, size, limit, costWeight, ...DATA.keys.map((k) => effort[k])].join("|");
  if (DATA.cache.has(key)) return DATA.cache.get(key);
  const scores = [];
  for (let mask = 1; mask < DATA.spec.plans; mask++) {
    let n = 0, cost = 0;
    for (let i = 0; i < DATA.keys.length; i++) if (mask >> i & 1) { n++; cost += effort[DATA.keys[i]]; }
    if (n === size && cost <= limit) scores.push(goalScore(goal, agency, mask, costWeight));
  }
  scores.sort((x, y) => x - y);
  const q = (p) => scores[Math.min(scores.length - 1, Math.floor(p * (scores.length - 1) + 0.5))];
  const result = scores.length ? [q(0.5), q(0.9), scores[scores.length - 1]] : null;
  DATA.cache.set(key, result);
  return result;
}
