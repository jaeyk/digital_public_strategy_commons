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
  positive: { title: "Better services", text: "Services work better for people, and give good value for money." },
  durable: { title: "Change that lasts", text: "Improvements survive elections, budget cuts, and staff leaving." },
  scalable: { title: "Works for everyone", text: "The approach also works for small and reluctant governments." },
};

// Step 3: strategies in plain words.
export const STRATEGIES = {
  team: ["Hire a core digital team", "A few skilled people who lead products and manage vendors."],
  insourcing: ["Bring vendor work in-house", "Grow your own staff to build and run services yourselves."],
  policy: ["Simplify the rules", "Cut paperwork and simplify the rules behind the service."],
  funding: ["Give it steady funding", "A stable yearly budget instead of one-off projects."],
  mandate: ["Put it in law", "Write the program and its goals into law."],
  authority: ["Set up central spending controls", "A central office that reviews tech spending and sets standards."],
  platforms: ["Use shared platforms", "Common tools for login, payments, and notifications."],
  collaboration: ["Team up with other governments", "Share staff, tools, and purchasing with neighbors."],
  procurement: ["Use smarter contracts", "Buy in smaller pieces and use renewals to get better deals."],
  portability: ["Own your data", "Make sure you own the data and can switch vendors."],
  entrants: ["Open the door to new vendors", "Make it easier for new and mission-driven companies to compete."],
  open_source: ["Make open source the default", "Publish and reuse code instead of buying closed products."],
  maintenance: ["Pay to maintain open source", "Fund the upkeep of the open code you depend on."],
  public_option: ["Build it as a public service", "The government builds and runs the service itself."],
  safeguards: ["Add safeguards and accountability", "Accessibility, ways to appeal, and openness about automated decisions."],
};

// Step 4 and results: one simple scale.
export const SCALE = [
  { key: "worse", label: "Worse than doing nothing" },
  { key: "little", label: "Little change" },
  { key: "some", label: "Some improvement" },
  { key: "big", label: "Big improvement" },
];

/** Turn a model score into a step on the simple scale. */
export function verdict(value) {
  if (value < -1) return 0;
  if (value < 2) return 1;
  if (value < 6) return 2;
  return 3;
}

export function encodeState(state) {
  const q = new URLSearchParams();
  q.set("agency", state.agency);
  q.set("goals", state.goals.join(","));
  q.set("plan", state.plan.join(","));
  q.set("guess", Object.entries(state.guess).map(([g, v]) => `${g}:${v}`).join(","));
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
  return {
    agency: AGENCIES[q.get("agency")] ? q.get("agency") : null,
    goals: list("goals").filter((g) => g in GOALS),
    plan: list("plan").filter((s) => s in STRATEGIES),
    guess,
  };
}

export const listText = (items) => (items.length <= 1 ? items.join("")
  : items.length === 2 ? `${items[0]} and ${items[1]}`
    : `${items.slice(0, -1).join(", ")}, and ${items[items.length - 1]}`);
