// Shared plain-language content and helpers for the two pages.

export const REPO = "https://github.com/jaeyk/digital_public_strategy_commons";
export const EMAIL = "jaekim@unc.edu";

// Step 1: the 2 x 2. Rows: commitment (high on top). Columns: resources (limited, then ample).
export const AGENCIES = {
  low_cap_high_mot: { title: "Small and committed", text: "Eager to change, but few people and little money." },
  high_cap_high_mot: { title: "Well-resourced and committed", text: "Eager to change, with people and money to do it." },
  low_cap_low_mot: { title: "Small and reluctant", text: "Few resources, and leaders who are not pushing for change." },
  high_cap_low_mot: { title: "Well-resourced and reluctant", text: "Has resources, but leaders who are not pushing for change." },
};

// Step 2: goals, matching the framework's three success criteria.
export const GOALS = {
  positive: { title: "Human-centered delivery", text: "Services work well for the people who use them, reach those who need them, and give good value for money." },
  durable: { title: "Durable change", text: "Improvements survive elections, budget cuts, and staff leaving." },
  scalable: { title: "Scales across agencies", text: "The approach also works in other agencies, including small ones and ones with reluctant leaders." },
};

// Step 3: strategies in plain words.
export const STRATEGIES = {
  team: ["Hire a core digital team", "A few skilled people who lead products and manage vendors."],
  insourcing: ["Bring vendor work in-house", "Grow your own staff to build and run services yourselves."],
  policy: ["Simplify the rules", "Cut paperwork and simplify the rules behind the service."],
  funding: ["Give it steady funding", "A stable yearly budget instead of one-off projects."],
  mandate: ["Pass a law", "Write the program and its goals into legislation. Takes a majority, a coalition, and time."],
  authority: ["Set up central spending controls", "A central office that reviews tech spending and sets standards."],
  platforms: ["Use shared platforms", "Common tools for login, payments, and notifications."],
  collaboration: ["Team up with other governments", "Share staff, tools, and purchasing with neighbors."],
  procurement: ["Use smarter contracts", "Buy in smaller pieces and use renewals to get better deals."],
  portability: ["Own your data", "Negotiate contracts so you own your data and can switch vendors. Often has to wait for renewal."],
  entrants: ["Open the door to new vendors", "Make it easier for new and mission-driven companies to compete."],
  open_source: ["Make open source the default", "Publish and reuse code instead of buying closed products."],
  maintenance: ["Pay to maintain open source", "Fund the upkeep of the open code you depend on."],
  public_option: ["Build it as a public service", "The government builds and runs the service itself."],
  safeguards: ["Add safeguards and accountability", "Accessibility, ways to appeal, and openness about automated decisions."],
};

// Step 2 (second question): how much can you invest? Effort limits and how much spending counts
// come from docs/data/model.json (benchmarks.levels); only the words live here.
export const LEVELS = {
  limited: { title: "Limited", text: "Little time, money, or staff to spare. Room for only a few strategies, and each has to pay off." },
  moderate: { title: "Moderate", text: "Some room to invest. Results matter most, but the investment counts too." },
  substantial: { title: "Substantial", text: "Real time, money, and staff to commit. Room for many strategies." },
};
export const DEFAULT_LEVEL = "moderate";

// Step 4 and results: where a plan stands among other plans with the same number of strategies.
export const SCALE = [
  { key: "backfires", label: "It backfires", text: "Worse than doing nothing." },
  { key: "below", label: "Below average", text: "Weaker than most plans of its size." },
  { key: "above", label: "Above average", text: "Better than most plans of its size." },
  { key: "best", label: "Among the best", text: "In the top tenth of plans of its size." },
];

/**
 * Grade a score. cut = [median, top-tenth, best] for plans of the same size
 * (from docs/data/model.json benchmarks). "It backfires" is judged on the plan's own score.
 */
export function verdict(value, cut) {
  if (!cut) return value < -1 ? 0 : 1;
  if (value < -1) return 0;
  if (value >= cut[1]) return 3;
  if (value >= cut[0]) return 2;
  return 1;
}

export function encodeState(state) {
  const q = new URLSearchParams();
  q.set("agency", state.agency);
  q.set("goals", state.goals.join(","));
  q.set("plan", state.plan.join(","));
  q.set("guess", Object.entries(state.guess).map(([g, v]) => `${g}:${v}`).join(","));
  q.set("level", state.level ?? DEFAULT_LEVEL);
  // Only effort ratings the visitor changed from the defaults are stored.
  const custom = Object.entries(state.effort || {}).map(([k, v]) => `${k}:${v}`).join(",");
  if (custom) q.set("effort", custom);
  if (state.budget != null) q.set("budget", String(state.budget));
  if (state.weight != null) q.set("weight", String(state.weight));
  return q.toString();
}

export function decodeState(search) {
  const q = new URLSearchParams(search);
  const list = (k) => (q.get(k) || "").split(",").filter(Boolean);
  const guess = {};
  list("guess").forEach((pair) => {
    const [g, v] = pair.split(":");
    if (g in GOALS && SCALE[+v]) guess[g] = +v;
  });
  const effort = {};
  list("effort").forEach((pair) => {
    const [k, v] = pair.split(":");
    if (k in STRATEGIES && [1, 2, 3, 4].includes(+v)) effort[k] = +v;
  });
  const budget = q.has("budget") && /^\d+$/.test(q.get("budget")) ? Math.min(30, Math.max(1, +q.get("budget"))) : null;
  const weight = q.has("weight") && WEIGHTS.some((w) => w.value === +q.get("weight")) ? +q.get("weight") : null;
  return {
    level: LEVELS[q.get("level")] ? q.get("level") : DEFAULT_LEVEL,
    agency: AGENCIES[q.get("agency")] ? q.get("agency") : null,
    goals: list("goals").filter((g) => g in GOALS),
    plan: list("plan").filter((s) => s in STRATEGIES),
    guess,
    effort,
    budget,
    weight,
  };
}

// How much spending counts against results (outcome points per 1.0 of yearly spending as a share of budget).
export const WEIGHTS = [
  { value: 0, title: "Not at all" },
  { value: 5, title: "Somewhat" },
  { value: 10, title: "A lot" },
  { value: 20, title: "Very much" },
];
/** The visitor's investment: the chosen level, with any custom budget or spending weight on top. */
export function investmentOf(model, state) {
  const level = model.investment_levels.find((l) => l.key === state.level);
  return { effort_points: state.budget ?? level.effort_points, cost_weight: state.weight ?? level.cost_weight };
}

// Effort scale shown to visitors (1-4 dots).
export const EFFORT_LABELS = ["", "Light", "Medium", "Heavy", "Very heavy"];
/** Effort ratings in use: the model's defaults with the visitor's changes on top. */
export const effortMap = (model, state) => ({ ...model.effort, ...(state.effort || {}) });

export const listText = (items) => (items.length <= 1 ? items.join("")
  : items.length === 2 ? `${items[0]} and ${items[1]}`
    : `${items.slice(0, -1).join(", ")}, and ${items[items.length - 1]}`);

// The relationships between levers, in plain words, for the map on the results page. Keys match
// models/common/relationships.py; the map only shows keys that exist in docs/data/model.json.
// kind: "needs" (first lever needs the second), "together" (works better together),
// "against" (pulls against each other), or "all" (shapes every other lever).
export const SHORT_NAMES = {
  team: "Core team", insourcing: "In-house work", collaboration: "Teaming up", platforms: "Shared platforms",
  authority: "Spending controls", funding: "Steady funding", mandate: "Pass a law", safeguards: "Safeguards",
  policy: "Simpler rules", procurement: "Smarter contracts", portability: "Own your data", entrants: "New vendors",
  public_option: "Public service", open_source: "Open source", maintenance: "Maintain open source",
};
export const RELATIONS = {
  talent_gates_procurement: { kind: "needs", edges: [["procurement", "team"]], text: "Smarter contracts need a core team that can manage them." },
  core_team_gates_insourcing: { kind: "needs", edges: [["insourcing", "team"]], text: "Bringing work in-house needs a core team to plan the move." },
  open_source_needs_maintenance: { kind: "needs", edges: [["open_source", "maintenance"]], text: "Open source code needs paid maintenance to stay useful." },
  entrants_need_portability: { kind: "needs", edges: [["entrants", "portability"]], text: "New vendors can only compete if you own your data and can switch." },
  team_speeds_hiring: { kind: "together", edges: [["team", "insourcing"]], text: "A core team makes it easier to hire the staff needed to bring work in-house." },
  funding_retains_talent: { kind: "together", edges: [["funding", "team"]], text: "Steady funding keeps skilled staff from leaving." },
  portability_stack: { kind: "together", edges: [["open_source", "portability"]], text: "Open source does more when you also own your data and interfaces." },
  platforms_need_authority: { kind: "together", edges: [["platforms", "authority"]], text: "Shared platforms spread faster with central standards behind them." },
  platforms_need_funding: { kind: "together", edges: [["platforms", "funding"]], text: "Shared platforms need steady funding to keep improving." },
  pooling_extends_scope: { kind: "together", edges: [["insourcing", "collaboration"], ["insourcing", "platforms"]], text: "Teaming up and shared platforms let an agency run more work in-house." },
  collaboration_cost_sharing: { kind: "together", edges: [["collaboration", "team"], ["collaboration", "platforms"], ["collaboration", "open_source"], ["collaboration", "maintenance"]], text: "Teaming up with other governments shares the cost of staff, platforms, and open source." },
  public_option_crowds_out_entrants: { kind: "against", edges: [["public_option", "entrants"]], text: "Building the service yourself leaves less room for new vendors." },
  spend_controls_slow_teams: { kind: "against", edges: [["authority", "team"]], text: "Central spending controls can slow down a product team." },
  cooperative_vs_modular: { kind: "against", edges: [["collaboration", "procurement"]], text: "Buying jointly with others works against splitting contracts into small pieces." },
  policy_binding_constraint: { kind: "all", lever: "policy", text: "Simpler rules let every other strategy pay off. Complicated rules hold them all back." },
  mandate_protects: { kind: "all", lever: "mandate", text: "Once passed, a law makes every other strategy harder for a new government to cut." },
  funding_protects: { kind: "all", lever: "funding", text: "Steady funding makes every other strategy harder to cut." },
  legitimacy_protects: { kind: "all", lever: "safeguards", text: "Safeguards build public trust, and people defend programs they trust." },
  lock_in_limits_change: { kind: "all", levers: ["procurement", "portability", "entrants", "public_option"], text: "Vendor lock-in holds back every improvement. Smarter contracts, owning your data, new vendors, and building it yourself loosen the vendor's grip." },
};
