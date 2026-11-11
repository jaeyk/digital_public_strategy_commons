// Page 2: run the model on the visitor's plan, compare it with their guess, and explain the gap in plain words.
import { simulate } from "./engine.js";
import { AGENCIES, GOALS, STRATEGIES, SCALE, verdict, decodeState, encodeState, listText } from "./shared.js";

const $ = (id) => document.getElementById(id);
const name = (k) => STRATEGIES[k][0].toLowerCase();

// Plain-language explanations of the relationships assumed in the model (models/common/relationships.py).
const PAIRS = [
  { need: "insourcing", partner: "team", missing: "Bringing work in-house is slow and disruptive without a core team to plan it.",
    present: "Your core team can plan the move in-house, so services are not disrupted." },
  { need: "procurement", partner: "team", missing: "Smarter contracts need skilled people to manage them. Without a core team they achieve little.",
    present: "Your core team has the skills to make smarter contracts work." },
  { need: "entrants", partner: "portability", missing: "New vendors struggle to compete unless you own your data and can switch.",
    present: "Owning your data means new vendors can actually win work." },
  { need: "open_source", partner: "maintenance", missing: "Open source code that nobody maintains does little to reduce dependence on vendors.",
    present: "Paying for maintenance keeps your open source code useful." },
  { need: "platforms", partner: "collaboration", missing: "Shared platforms pay off more when other governments use them too.",
    present: "Teaming up with other governments makes shared platforms cheaper and more useful." },
  { need: "platforms", partner: "funding", missing: "Shared platforms need steady funding to keep improving.",
    present: "Steady funding keeps your shared platforms improving." },
  { need: "insourcing", partner: "collaboration", small: true, missing: "A small agency can only run so much on its own. Pooling staff with other governments lets it do more.",
    present: "Pooling with other governments lets a small agency run more itself." },
];
const CONFLICTS = [
  { a: "entrants", b: "public_option", text: "Building the service yourself leaves less room for new vendors, so these two pull against each other." },
  { a: "authority", b: "team", text: "Central spending controls can slow down a product team that needs to move quickly." },
];

let MODEL, state, agency;

function run(levers, jurisdiction, turnover) {
  const opts = { jurisdiction, turnover, trials: turnover ? 60 : 12, seed: 7 };
  const w = MODEL.defaults.cost_weight;
  const plan = simulate(MODEL, { ...opts, levers });
  const base = simulate(MODEL, { ...opts, levers: [] });
  return { value: plan.outcomeGain - w * plan.spendShare - (base.outcomeGain - w * base.spendShare), plan };
}

function scores(levers, goals = state.goals) {
  const out = {};
  if (goals.includes("positive")) out.positive = run(levers, agency.key, false).value;
  if (goals.includes("durable")) {
    const r = run(levers, agency.key, true);
    out.durable = r.value;
    out.survival = r.plan.survival;
  }
  if (goals.includes("scalable")) {
    const byType = MODEL.jurisdictions.map((j) => ({ j, v: run(levers, j.key, false).value }));
    const weakest = byType.reduce((a, b) => (b.v < a.v ? b : a));
    out.scalable = weakest.v;
    out.weakest = weakest.j;
  }
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
    out.push({ text: "Your plan costs more than this kind of agency can afford, so every part is spread thin. Fewer, well-chosen strategies may do better.", helps: false });
  }
  if (agency.motivation < 0.6) out.push({ text: "Reluctant leadership means strategies are carried out half-heartedly, so gains are smaller.", helps: false });
  if (has("insourcing")) out.push({ text: "Bringing work in-house takes years, so much of the benefit arrives late.", helps: false });

  if (goal === "durable") {
    const s = result.survival ?? 1;
    out.unshift({ text: s >= 0.75 ? "Most of your strategies are likely to survive a hostile new government."
      : s >= 0.4 ? "Some of your strategies are likely to be cut by a hostile new government."
        : "Many of your strategies are likely to be cut by a hostile new government.", helps: s >= 0.75 });
    if (!has("mandate") && !has("funding")) out.push({ text: "Nothing protects your plan from being cut. Putting it in law or giving it steady funding helps it survive.", helps: false });
    if (has("mandate")) out.push({ text: "Putting it in law makes your plan much harder to undo.", helps: true });
    if (has("funding")) out.push({ text: "Steady funding makes your plan harder to cut and keeps staff from leaving.", helps: true });
    if (has("safeguards")) out.push({ text: "Services people trust have defenders when budgets are cut.", helps: true });
    else if (s < 0.75) out.push({ text: "People who trust a service will defend it. Safeguards help build that trust.", helps: false });
    if (has("insourcing")) out.push({ text: "A half-finished move in-house is easy to reverse, and the work goes back to vendors.", helps: false });
  }
  if (goal === "scalable" && result.weakest) {
    const w = result.weakest;
    const why = w.budget < 0.5
      ? "Small agencies cannot afford big teams. Shared platforms and teaming up lower the cost."
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
    cell.className = "meter-cell";
    if (i === model) cell.classList.add("model");
    if (i === guess) cell.classList.add("guess");
    cell.innerHTML = "<span class='meter-label'></span><span class='badges'></span>";
    cell.querySelector(".meter-label").textContent = s.label;
    const badges = cell.querySelector(".badges");
    if (i === guess) badges.insertAdjacentHTML("beforeend", "<span class='badge you'>Your guess</span>");
    if (i === model) badges.insertAdjacentHTML("beforeend", "<span class='badge model'>Model</span>");
    row.appendChild(cell);
  });
  return row;
}

function renderGoal(goal, result, used) {
  const value = result[goal];
  const model = verdict(value);
  const guess = state.guess[goal];
  const box = document.createElement("section");
  box.className = "result";
  const gap = model - guess;
  const headline = gap === 0 ? "Your guess matches the model."
    : gap > 0 ? "The model is more optimistic than you were." : "The model is less optimistic than you were.";
  box.innerHTML = `<h2></h2><p class="goal-text"></p><p class="headline"></p><h3>Why</h3><ul class="reasons"></ul>`;
  box.querySelector("h2").textContent = GOALS[goal].title;
  box.querySelector(".goal-text").textContent = GOALS[goal].text;
  box.insertBefore(meter(guess, model), box.querySelector(".headline"));
  box.querySelector(".headline").textContent = headline;
  // Lead with the reasons that explain the direction of the gap.
  const all = reasons(goal, state.plan, result).filter((r) => !used.has(r.text));
  const lead = gap < 0 ? all.filter((r) => !r.helps) : gap > 0 ? all.filter((r) => r.helps) : all;
  const picked = [...lead, ...all.filter((r) => !lead.includes(r))].slice(0, 3);
  picked.forEach((r) => {
    used.add(r.text);
    const li = document.createElement("li");
    li.className = r.helps ? "helps" : "hurts";
    li.textContent = r.text;
    box.querySelector(".reasons").appendChild(li);
  });
  if (!picked.length) box.querySelector(".reasons").innerHTML = "<li>Your strategies mostly add up on their own here, without strong effects on each other.</li>";
  return box;
}

function renderSuggestion(current) {
  const goals = state.goals;
  const avg = (s) => goals.reduce((sum, g) => sum + s[g], 0) / goals.length;
  const base = avg(current);
  let best = null;
  Object.keys(STRATEGIES).filter((k) => !state.plan.includes(k)).forEach((k) => {
    const s = scores([...state.plan, k]);
    const gain = avg(s) - base;
    if (!best || gain > best.gain) best = { k, s, gain, add: true };
  });
  if (state.plan.length > 1) {
    state.plan.forEach((k) => {
      const s = scores(state.plan.filter((x) => x !== k));
      const gain = avg(s) - base;
      if (gain > (best?.gain ?? 0)) best = { k, s, gain, add: false };
    });
  }
  const box = $("suggestion");
  if (!best || best.gain < 0.5) {
    box.innerHTML = "<h2>What could make your plan stronger?</h2><p>The model does not find a single change that clearly helps. Your plan is already close to the best it finds for this agency and these goals.</p>";
    box.hidden = false;
    return;
  }
  const plan = best.add ? [...state.plan, best.k] : state.plan.filter((x) => x !== best.k);
  const pair = PAIRS.find((p) => best.add && ((p.partner === best.k && state.plan.includes(p.need)) || (p.need === best.k && state.plan.includes(p.partner))));
  const why = best.add ? (pair ? pair.present : STRATEGIES[best.k][1]) : "For this agency it costs more than it adds.";
  const changes = goals.map((g) => {
    const before = SCALE[verdict(current[g])].label, after = SCALE[verdict(best.s[g])].label;
    return `<li><strong>${GOALS[g].title}:</strong> ${before === after ? `${after} (stronger)` : `${before} &rarr; ${after}`}</li>`;
  }).join("");
  box.innerHTML = `<h2>What could make your plan stronger?</h2>
    <p><strong>${best.add ? "Add" : "Drop"}: ${STRATEGIES[best.k][0]}.</strong> ${why}</p><ul>${changes}</ul>
    <a class="button" href="results.html?${encodeState({ ...state, plan })}">See results with this change</a>`;
  box.hidden = false;
}

async function main() {
  state = decodeState(location.search);
  if (!state.agency || !state.goals.length || !state.plan.length || !state.goals.every((g) => g in state.guess)) {
    $("summary").innerHTML = "Your choices were not found. <a href='index.html'>Start here</a>.";
    return;
  }
  MODEL = await fetch("data/model.json").then((r) => r.json());
  agency = MODEL.jurisdictions.find((j) => j.key === state.agency);
  $("summary").textContent = `For a ${AGENCIES[state.agency].title.toLowerCase()} agency, your plan is to ${listText(state.plan.map(name))}.`;
  $("edit-plan").href = `index.html?${encodeState(state)}`;
  // Let the page paint before running the model.
  await new Promise((r) => setTimeout(r, 30));
  const current = scores(state.plan);
  const used = new Set();
  state.goals.forEach((g) => $("results").appendChild(renderGoal(g, current, used)));
  renderSuggestion(current);
}

main().catch((error) => {
  console.error(error);
  $("summary").textContent = `Something went wrong loading the model (${error.message}). If you opened this file directly, run ./preview_site.sh instead.`;
});
