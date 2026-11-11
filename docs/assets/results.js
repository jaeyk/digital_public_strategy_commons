// Page 2: look up the model's guess for the visitor's plan, compare it with their guess, and explain the gap
// in plain words. Scores come from docs/data/scores.bin, written by the Python models.
import { AGENCIES, GOALS, STRATEGIES, SCALE, LEVELS, WEIGHTS, SHORT_NAMES, RELATIONS, EFFORT_LABELS, effortMap, investmentOf, verdict, decodeState, encodeState, listText } from "./shared.js";
import { loadScores, maskOf, goalScore, survival, weakestAgency, comparison, effortOfMask } from "./scores.js";

const $ = (id) => document.getElementById(id);
const name = (k) => STRATEGIES[k][0].toLowerCase();

// Plain-language explanations of the relationships assumed in the model (models/common/relationships.py).
const PAIRS = [
  {
    need: "insourcing", partner: "team", missing: "Bringing work in-house is slow and disruptive without a core team to plan it.",
    present: "Your core team can plan the move in-house, so services are not disrupted."
  },
  {
    need: "procurement", partner: "team", missing: "Smarter contracts need skilled people to manage them. Without a core team they achieve little.",
    present: "Your core team has the skills to make smarter contracts work."
  },
  {
    need: "entrants", partner: "portability", missing: "New vendors struggle to compete unless you own your data and can switch.",
    present: "Owning your data means new vendors can actually win work."
  },
  {
    need: "open_source", partner: "maintenance", missing: "Open source code that nobody maintains does little to reduce dependence on vendors.",
    present: "Paying for maintenance keeps your open source code useful."
  },
  {
    need: "platforms", partner: "collaboration", missing: "Shared platforms pay off more when other governments use them too.",
    present: "Teaming up with other governments makes shared platforms cheaper and more useful."
  },
  {
    need: "platforms", partner: "funding", missing: "Shared platforms need steady funding to keep improving.",
    present: "Steady funding keeps your shared platforms improving."
  },
  {
    need: "insourcing", partner: "collaboration", small: true, missing: "A small agency can only run so much on its own. Pooling staff with other governments lets it do more.",
    present: "Pooling with other governments lets a small agency run more itself."
  },
];
const CONFLICTS = [
  { a: "entrants", b: "public_option", text: "Building the service yourself leaves less room for new vendors, so these two pull against each other." },
  { a: "authority", b: "team", text: "Central spending controls can slow down a product team that needs to move quickly." },
];

let MODEL, state, agency;

function scores(levers, goals = state.goals) {
  const mask = maskOf(levers);
  const w = investmentOf(MODEL, state).cost_weight;
  const out = {};
  for (const g of goals) out[g] = goalScore(g, agency.key, mask, w);
  if (goals.includes("durable")) out.survival = levers.length ? survival(agency.key, mask) : null;
  if (goals.includes("scalable")) out.weakest = MODEL.jurisdictions.find((j) => j.key === weakestAgency(mask, w));
  return out;
}

function planCost(levers, j) {
  const shared = levers.includes("collaboration");
  const total = MODEL.levers.filter((l) => levers.includes(l.key))
    .reduce((sum, l) => sum + l.annual_cost * (l.shareable && shared ? 0.6 : 1), 0);
  return total / j.budget;
}

/** Plain reasons for a goal's result. Each reason is {text, helps}. */
function reasons(goal, plan, result) {
  const has = (k) => plan.includes(k);
  const small = agency.budget < 0.5;
  const out = [];
  PAIRS.forEach((p) => {
    if (p.small && !small) return;
    if (has(p.need) && !has(p.partner)) out.push({ text: p.missing, helps: false });
    if (has(p.need) && has(p.partner)) out.push({ text: p.present, helps: true });
  });
  CONFLICTS.forEach((c) => { if (has(c.a) && has(c.b)) out.push({ text: c.text, helps: false }); });
  if (goal !== "durable") {
    out.push(has("policy")
      ? { text: "Simpler rules let your other strategies pay off.", helps: true }
      : { text: "Complicated rules limit how much any technology can improve services. Simplifying them makes every other strategy work better.", helps: false });
  }
  if (planCost(plan, agency) > 1) {
    out.push({ text: "Your plan needs more investment than this kind of agency can afford, so every part is spread thin. Fewer, well-chosen strategies may do better.", helps: false });
  }
  if (agency.motivation < 0.6) out.push({ text: "Reluctant leadership means strategies are carried out half-heartedly, so gains are smaller.", helps: false });
  if (has("insourcing")) out.push({ text: "Bringing work in-house takes years, so much of the benefit arrives late.", helps: false });

  if (goal === "durable") {
    const s = result.survival ?? 1;
    out.unshift({
      text: s >= 0.75 ? "Most of your strategies are likely to survive a hostile new government."
        : s >= 0.4 ? "Some of your strategies are likely to be cut by a hostile new government."
          : "Many of your strategies are likely to be cut by a hostile new government.", helps: s >= 0.75
    });
    if (!has("mandate") && !has("funding")) out.push({ text: "Nothing protects your plan from being cut. Passing a law or giving it steady funding helps it survive.", helps: false });
    if (has("mandate")) out.push({ text: "Once passed, a law makes your plan much harder to undo.", helps: true });
    if (has("funding")) out.push({ text: "Steady funding makes your plan harder to cut and keeps staff from leaving.", helps: true });
    if (has("safeguards")) out.push({ text: "Services people trust have defenders when budgets are cut.", helps: true });
    else if (s < 0.75) out.push({ text: "People who trust a service will defend it. Safeguards help build that trust.", helps: false });
    if (has("insourcing")) out.push({ text: "A half-finished move in-house is easy to reverse, and the work goes back to vendors.", helps: false });
  }
  if (goal === "scalable" && result.weakest) {
    const w = result.weakest;
    const why = w.budget < 0.5
      ? "Small agencies cannot afford big teams. Shared platforms and teaming up lower the investment needed."
      : "Reluctant agencies carry out plans half-heartedly. Shared tools that work by default help most.";
    out.unshift({ text: `Your plan works least well for ${w.name.toLowerCase()} agencies. ${why}`, helps: false });
  }
  return out;
}

function meter(guess, model) {
  const row = document.createElement("div");
  row.className = "meter";
  SCALE.forEach((s, i) => {
    const cell = document.createElement("div");
    cell.className = `meter-cell v-${s.key}`;
    if (i === model) cell.classList.add("model");
    if (i === guess) cell.classList.add("guess");
    cell.innerHTML = "<span class='meter-label'></span><span class='badges'></span>";
    cell.querySelector(".meter-label").textContent = s.label;
    const badges = cell.querySelector(".badges");
    if (i === guess) badges.insertAdjacentHTML("beforeend", "<span class='badge you'>Your guess</span>");
    if (i === model) badges.insertAdjacentHTML("beforeend", "<span class='badge model'>Model’s guess</span>");
    row.appendChild(cell);
  });
  return row;
}

const levelSpec = (key) => MODEL.investment_levels.find((l) => l.key === key);
const customBudget = () => state.budget != null || state.weight != null;
/** Short description of the investment for comparison sentences. */
const investmentText = () => {
  if (!customBudget()) return `a ${LEVELS[state.level].title.toLowerCase()} investment`;
  const inv = investmentOf(MODEL, state);
  return `your budget of ${inv.effort_points} effort dots`;
};
const effort = () => effortMap(MODEL, state);
const effortOf = (plan) => effortOfMask(maskOf(plan), effort());

/** Median, top-tenth, and best scores of plans with `size` strategies that fit the same investment. */
function cutFor(goal, size) {
  const inv = investmentOf(MODEL, state);
  return comparison(goal, agency.key, size, inv.effort_points, effort(), inv.cost_weight);
}

function renderGoal(goal, result, used) {
  const value = result[goal];
  const cut = cutFor(goal, state.plan.length);
  const model = verdict(value, cut);
  const guess = state.guess[goal];
  const box = document.createElement("section");
  box.className = "result";
  const gap = model - guess;
  const headline = gap === 0 ? "Your guess matches the model’s guess."
    : gap > 0 ? "The model’s guess is more optimistic than yours." : "The model’s guess is less optimistic than yours.";
  box.innerHTML = `<h2></h2><p class="goal-text"></p><p class="basis"></p><p class="headline"></p><div class="why"></div>`;
  box.querySelector("h2").textContent = GOALS[goal].title;
  box.querySelector(".goal-text").textContent = GOALS[goal].text;
  const n = state.plan.length;
  box.querySelector(".basis").textContent = goal === "scalable"
    ? `Compared with every other plan of ${n} ${n === 1 ? "strategy" : "strategies"} that fits ${investmentText()}${Object.keys(state.effort).length ? " using your effort ratings" : ""}, judged by the kind of agency where it works worst.`
    : `Compared with every other plan of ${n} ${n === 1 ? "strategy" : "strategies"} that fits ${investmentText()}${Object.keys(state.effort).length ? " using your effort ratings" : ""}, for a ${AGENCIES[state.agency].title.toLowerCase()} agency.`;
  box.insertBefore(meter(guess, model), box.querySelector(".headline"));
  box.querySelector(".headline").textContent = headline;

  const all = reasons(goal, state.plan, result).filter((r) => !used.has(r.text));
  if (cut && cut[2] < 3) {
    all.unshift({
      text: goal === "scalable"
        ? "Even the best plans of this size help the hardest-pressed agencies only a little."
        : "Even the best plans of this size only help a little for this kind of agency.", helps: false
    });
  }
  if (model >= 2 && !all.some((r) => r.helps)) {
    all.unshift({ text: "Your choices hold up better than most combinations of the same size.", helps: true });
  }
  // Show at most three reasons, leading with the ones that explain the direction of the gap.
  const helps = all.filter((r) => r.helps), hurts = all.filter((r) => !r.helps);
  const takeHelps = gap > 0 ? Math.min(helps.length, 2) : Math.min(helps.length, 1);
  const picked = [...helps.slice(0, takeHelps), ...hurts.slice(0, 3 - takeHelps)];
  const why = box.querySelector(".why");
  [["What works", picked.filter((r) => r.helps), "helps"], ["What holds it back", picked.filter((r) => !r.helps), "hurts"]]
    .forEach(([title, items, cls]) => {
      if (!items.length) return;
      why.insertAdjacentHTML("beforeend", `<h3>${title}</h3><ul class="reasons"></ul>`);
      const ul = why.lastElementChild;
      items.forEach((r) => {
        used.add(r.text);
        const li = document.createElement("li");
        li.className = cls;
        li.textContent = r.text;
        ul.appendChild(li);
      });
    });
  return box;
}

function renderSuggestion(current) {
  const goals = state.goals;
  const avg = (s) => goals.reduce((sum, g) => sum + s[g], 0) / goals.length;
  const base = avg(current);
  const limit = investmentOf(MODEL, state).effort_points;
  const fits = (plan) => effortOf(plan) <= limit;
  // Candidate changes that stay within the investment: add one strategy, drop one, or swap one for another.
  const candidates = [];
  Object.keys(STRATEGIES).filter((k) => !state.plan.includes(k)).forEach((k) => {
    if (fits([...state.plan, k])) candidates.push({ plan: [...state.plan, k], add: k });
    state.plan.forEach((out) => {
      const plan = [...state.plan.filter((x) => x !== out), k];
      if (fits(plan)) candidates.push({ plan, add: k, drop: out });
    });
  });
  if (state.plan.length > 1) state.plan.forEach((out) => candidates.push({ plan: state.plan.filter((x) => x !== out), drop: out }));
  let best = null;
  candidates.forEach((c) => {
    const s = scores(c.plan);
    const gain = avg(s) - base;
    if (!best || gain > best.gain) best = { ...c, s, gain };
  });
  const box = $("suggestion");
  if (!best || best.gain < 0.5) {
    box.innerHTML = "<h2>What could make your plan stronger?</h2><p>The model does not find a single change within your investment that clearly helps. Your plan is already close to the best it finds for this agency and these goals.</p>";
    box.hidden = false;
    return;
  }
  const title = (k) => STRATEGIES[k][0];
  const pair = best.add && PAIRS.find((p) => (p.partner === best.add && best.plan.includes(p.need)) || (p.need === best.add && best.plan.includes(p.partner)));
  const action = best.add && best.drop ? `Swap "${title(best.drop).toLowerCase()}" for "${title(best.add).toLowerCase()}".`
    : best.add ? `${title(best.add)}.` : `Drop "${title(best.drop).toLowerCase()}".`;
  const why = best.add ? (pair ? pair.present : STRATEGIES[best.add][1])
    : "For this agency it needs more investment than it returns, and dropping it frees time and money.";
  // Say in plain words which goals the change helps; grades are not compared, because the plan can change size.
  const changes = goals.map((g) => {
    const d = best.s[g] - current[g];
    const effect = d > 2 ? "clearly better" : d > 0.3 ? "a little better" : d < -0.3 ? "a little worse" : "about the same";
    return `<li><strong>${GOALS[g].title}:</strong> ${effect}</li>`;
  }).join("");
  box.innerHTML = `<h2>What could make your plan stronger?</h2>
    <p><strong>${action}</strong> ${why}</p><ul>${changes}</ul>
    <a class="button" href="results.html?${encodeState({ ...state, plan: best.plan })}">See results with this change</a>`;
  box.hidden = false;
}

// ---------- Map of how the levers connect ----------
// Arranged so related levers sit near each other around the circle.
const RING = ["team", "insourcing", "collaboration", "platforms", "authority", "funding", "mandate", "safeguards",
  "policy", "public_option", "entrants", "portability", "procurement", "maintenance", "open_source"];
const KIND_LABEL = { needs: "Needs", neededBy: "Needed by", together: "Works better with", against: "Pulls against" };

function networkEdges() {
  // One entry per pair of levers; a pair can carry several relationships.
  const known = new Set(MODEL.relationships.map((r) => r.key));
  const pairs = new Map();
  for (const [key, rel] of Object.entries(RELATIONS)) {
    if (!known.has(key) || rel.kind === "all") continue;
    for (const [a, b] of rel.edges) {
      const id = [a, b].sort().join("|");
      if (!pairs.has(id)) pairs.set(id, { a, b, items: [] });
      pairs.get(id).items.push({ kind: rel.kind, from: a, to: b, text: rel.text });
    }
  }
  // The line style follows the strongest relationship in the pair: needs, then pulls against, then together.
  for (const p of pairs.values()) {
    p.kind = ["needs", "against", "together"].find((k) => p.items.some((i) => i.kind === k));
    const need = p.items.find((i) => i.kind === "needs");
    if (need) { p.a = need.from; p.b = need.to; }
  }
  return [...pairs.values()];
}

function renderNetwork() {
  const svgNS = "http://www.w3.org/2000/svg";
  const W = 900, H = 640, cx = W / 2, cy = H / 2, R = 245;
  const pos = Object.fromEntries(RING.map((k, i) => {
    const angle = -Math.PI / 2 + (2 * Math.PI * i) / RING.length;
    return [k, { x: cx + R * Math.cos(angle), y: cy + R * Math.sin(angle), angle }];
  }));
  const edges = networkEdges();
  const el = (tag, attrs, parent) => {
    const n = document.createElementNS(svgNS, tag);
    for (const [k, v] of Object.entries(attrs)) n.setAttribute(k, v);
    if (parent) parent.appendChild(n);
    return n;
  };
  const svg = el("svg", { viewBox: `0 0 ${W} ${H}`, role: "group", "aria-label": "Map of how the 15 levers connect" });
  const defs = el("defs", {}, svg);
  const marker = el("marker", { id: "arrow-needs", viewBox: "0 0 10 10", refX: "9", refY: "5", markerWidth: "7", markerHeight: "7", orient: "auto-start-reverse" }, defs);
  el("path", { d: "M0 0 L10 5 L0 10 Z", class: "arrow needs" }, marker);
  const edgeLayer = el("g", {}, svg);
  const nodeLayer = el("g", {}, svg);
  const lines = edges.map((e) => {
    const p1 = pos[e.a], p2 = pos[e.b];
    // Stop the line short of the target node so the arrowhead stays visible.
    const dx = p2.x - p1.x, dy = p2.y - p1.y, len = Math.hypot(dx, dy);
    const line = el("line", { x1: p1.x + (dx / len) * 16, y1: p1.y + (dy / len) * 16, x2: p2.x - (dx / len) * 18, y2: p2.y - (dy / len) * 18,
      class: `edge ${e.kind}`, ...(e.kind === "needs" ? { "marker-end": "url(#arrow-needs)" } : {}) }, edgeLayer);
    return { e, line };
  });
  const nodes = RING.map((k) => {
    const p = pos[k];
    const g = el("g", { class: `node${state.plan.includes(k) ? " in-plan" : ""}`, tabindex: "0", role: "button",
      "aria-label": `${STRATEGIES[k][0]}${state.plan.includes(k) ? " (in your plan)" : ""}` }, nodeLayer);
    el("circle", { cx: p.x, cy: p.y, r: 13 }, g);
    const lx = cx + (R + 24) * Math.cos(p.angle), ly = cy + (R + 24) * Math.sin(p.angle) + (Math.sin(p.angle) > 0.9 ? 8 : Math.sin(p.angle) < -0.9 ? -6 : 0);
    const cos = Math.cos(p.angle);
    const t = el("text", { x: lx, y: ly + 6, "text-anchor": Math.abs(cos) < 0.05 ? "middle" : cos > 0 ? "start" : "end" }, g);
    t.textContent = SHORT_NAMES[k];
    g.addEventListener("mouseenter", () => select(k));
    g.addEventListener("focus", () => select(k));
    g.addEventListener("click", () => select(k));
    g.addEventListener("keydown", (ev) => { if (ev.key === "Enter" || ev.key === " ") { ev.preventDefault(); select(k); } });
    return { k, g };
  });
  const graph = $("network-graph");
  graph.innerHTML = "";
  graph.appendChild(svg);

  function select(k) {
    nodes.forEach((n) => n.g.classList.toggle("selected", n.k === k));
    const linked = new Set([k]);
    lines.forEach(({ e, line }) => {
      const on = e.a === k || e.b === k;
      line.classList.toggle("dim", !on);
      line.classList.toggle("lit", on);
      if (on) { linked.add(e.a); linked.add(e.b); }
    });
    nodes.forEach((n) => n.g.classList.toggle("dim", !linked.has(n.k)));
    const groups = { needs: [], neededBy: [], together: [], against: [] };
    edges.filter((e) => e.a === k || e.b === k).forEach((e) => e.items.forEach((i) => {
      const other = i.from === k ? i.to : i.from;
      groups[i.kind === "needs" && i.from !== k ? "neededBy" : i.kind].push({ other, text: i.text });
    }));
    const wide = Object.values(RELATIONS).filter((r) => r.kind === "all" && (r.lever === k || (r.levers || []).includes(k)));
    const panel = $("network-panel");
    const title = `<h3>${STRATEGIES[k][0]}${state.plan.includes(k) ? " <span class='in-plan-tag'>in your plan</span>" : ""}</h3>`;
    const sections = Object.entries(groups).filter(([, items]) => items.length).map(([kind, items]) =>
      `<p class="panel-kind ${kind}">${KIND_LABEL[kind]}</p><ul>${items.map((i) => `<li><strong>${SHORT_NAMES[i.other]}:</strong> ${i.text}</li>`).join("")}</ul>`).join("");
    const wideText = wide.map((r) => `<p class="panel-all">${r.text}</p>`).join("");
    panel.innerHTML = title + (sections || wideText ? sections + wideText : "<p>This lever works mostly on its own in the model.</p>");
  }
  select(state.plan.find((k) => RING.includes(k)) || RING[0]);

  $("network-all").innerHTML = Object.entries(RELATIONS)
    .filter(([key, r]) => r.kind === "all" && MODEL.relationships.some((m) => m.key === key))
    .map(([, r]) => `<li>${r.text}</li>`).join("");
  $("network").hidden = false;
}

async function main() {
  state = decodeState(location.search);
  if (!state.agency || !state.goals.length || !state.plan.length || !state.goals.every((g) => g in state.guess)) {
    $("summary").innerHTML = "Your choices were not found. <a href='index.html'>Start here</a>.";
    return;
  }
  MODEL = await fetch("data/model.json").then((r) => r.json());
  await loadScores(MODEL);
  agency = MODEL.jurisdictions.find((j) => j.key === state.agency);
  $("summary").textContent = `For a ${AGENCIES[state.agency].title.toLowerCase()} agency, your plan is to ${listText(state.plan.map(name))}.`;
  $("edit-plan").href = `index.html?${encodeState(state)}`;
  const sw = $("cost-switch");
  sw.innerHTML = "<span>Investment:</span>";
  const need = effortOf(state.plan);
  if (customBudget()) {
    const inv = investmentOf(MODEL, state);
    const span = document.createElement("a");
    span.href = `results.html?${encodeState(state)}`;
    span.setAttribute("aria-current", "true");
    span.textContent = `your budget: ${inv.effort_points} dots, spending counts ${WEIGHTS.find((x) => x.value === inv.cost_weight)?.title.toLowerCase() ?? "custom"}`;
    sw.appendChild(span);
  }
  Object.entries(LEVELS).forEach(([key, l]) => {
    if (need > levelSpec(key).effort_points) {
      sw.insertAdjacentHTML("beforeend", `<span class="too-small" title="Your plan needs more than this level allows">${l.title.toLowerCase()} (too little for this plan)</span>`);
      return;
    }
    const a = document.createElement("a");
    a.href = `results.html?${encodeState({ ...state, level: key, budget: null, weight: null })}`;
    a.textContent = l.title.toLowerCase();
    a.setAttribute("aria-current", String(!customBudget() && key === state.level));
    sw.appendChild(a);
  });
  sw.insertAdjacentHTML("beforeend", "<span class='small'>Switch to see how much your results depend on it.</span>");
  // Let the page paint before running the model.
  await new Promise((r) => setTimeout(r, 30));
  const current = scores(state.plan);
  const used = new Set();
  state.goals.forEach((g) => $("results").appendChild(renderGoal(g, current, used)));
  renderSuggestion(current);
  renderNetwork();
}

main().catch((error) => {
  console.error(error);
  $("summary").textContent = `Something went wrong loading the model (${error.message}). If you opened this file directly, run ./preview_website.sh instead.`;
});
