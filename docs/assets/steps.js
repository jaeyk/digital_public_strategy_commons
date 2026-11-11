// Page 1: four steps, one at a time. The choices are passed to results.html in the URL.
import { AGENCIES, GOALS, STRATEGIES, SCALE, LEVELS, WEIGHTS, EFFORT_LABELS, effortMap, investmentOf, encodeState, decodeState, listText } from "./shared.js";

const state = { agency: null, goals: [], plan: [], guess: {}, effort: {}, budget: null, weight: null, ...decodeState(location.search) };
let step = 1;
let MODEL = null;
const $ = (id) => document.getElementById(id);

const effortOf = (key) => effortMap(MODEL, state)[key];
const levelSpec = () => investmentOf(MODEL, state);
const used = () => state.plan.reduce((sum, k) => sum + effortOf(k), 0);
const fits = () => used() <= levelSpec().effort_points;

function card({ title, text, selected, onClick, role = "checkbox", extra = "", disabled = false }) {
  const b = document.createElement("button");
  b.type = "button";
  b.className = "card";
  b.setAttribute("role", role);
  b.setAttribute("aria-checked", String(selected));
  b.disabled = disabled;
  b.innerHTML = "<strong></strong><span></span>";
  b.querySelector("strong").textContent = title;
  b.querySelector("span").textContent = text;
  if (extra) b.insertAdjacentHTML("beforeend", extra);
  b.addEventListener("click", onClick);
  return b;
}

function render() {
  // Step 1: the 2 x 2 (top row = more committed; right column = more resources).
  const quad = $("agencies");
  quad.innerHTML = "";
  ["low_cap_high_mot", "high_cap_high_mot", "low_cap_low_mot", "high_cap_low_mot"].forEach((key) => {
    quad.appendChild(card({ ...AGENCIES[key], role: "radio", selected: state.agency === key,
      onClick: () => { state.agency = key; render(); } }));
  });

  // Step 2: goals and investment level.
  const goals = $("goals");
  goals.innerHTML = "";
  Object.entries(GOALS).forEach(([key, g]) => goals.appendChild(card({ ...g, selected: state.goals.includes(key),
    onClick: () => { toggle(state.goals, key); render(); } })));
  const levels = $("levels");
  levels.innerHTML = "";
  Object.entries(LEVELS).forEach(([key, l]) => levels.appendChild(card({ ...l, role: "radio", selected: state.level === key,
    onClick: () => { state.level = key; state.budget = null; state.weight = null; render(); } })));

  // Custom budget: effort dots and how much spending counts.
  const inv = levelSpec();
  const custom = state.budget != null || state.weight != null;
  $("budget-summary").textContent = custom ? "Customize your budget (in use)" : "Customize your budget";
  $("budget-range").value = String(inv.effort_points);
  $("budget-value").textContent = `${inv.effort_points} ${inv.effort_points === 1 ? "dot" : "dots"}`;
  const weights = $("weight-choices");
  weights.innerHTML = "";
  WEIGHTS.forEach((w) => {
    const b = document.createElement("button");
    b.type = "button";
    b.setAttribute("role", "radio");
    b.setAttribute("aria-checked", String(inv.cost_weight === w.value));
    b.textContent = w.title;
    b.addEventListener("click", () => { state.weight = w.value; render(); });
    weights.appendChild(b);
  });
  $("budget-reset").hidden = !custom;

  // Step 3: strategies, limited by the investment level.
  const limit = levelSpec().effort_points;
  const left = limit - used();
  $("budget").innerHTML = `<span class="budget-label">Investment used</span>
    <span class="budget-dots" aria-hidden="true">${"<i class='on'></i>".repeat(Math.min(used(), limit))}${"<i></i>".repeat(Math.max(0, left))}${used() > limit ? "<i class='over'></i>".repeat(used() - limit) : ""}</span>
    <span class="budget-text">${used() > limit ? "Your plan needs more than you can invest. Remove a strategy, or go back and choose a higher investment."
      : left === 0 ? "You have used all of your investment." : `Room for ${left} more ${left === 1 ? "dot" : "dots"} of effort.`}</span>`;
  const strategies = $("strategies");
  strategies.innerHTML = "";
  Object.entries(STRATEGIES).forEach(([key, [title, text]]) => {
    const chosen = state.plan.includes(key);
    const e = effortOf(key);
    strategies.appendChild(card({ title, text, selected: chosen, disabled: !chosen && e > left,
      extra: `<em class="effort${e >= 3 ? " heavy" : ""}"><span class="pips" aria-hidden="true">${"<i class='on'></i>".repeat(e)}${"<i></i>".repeat(4 - e)}</span>${EFFORT_LABELS[e]} effort${state.effort[key] ? " (your rating)" : ""}</em>`,
      onClick: () => { toggle(state.plan, key); render(); } }));
  });

  // Effort ratings the visitor can adjust.
  const rows = $("effort-rows");
  rows.innerHTML = "";
  Object.entries(STRATEGIES).forEach(([key, [title]]) => {
    const row = document.createElement("div");
    row.className = `effort-row${state.effort[key] ? " changed" : ""}`;
    row.innerHTML = "<div class='effort-name'><strong></strong><span></span></div><div class='effort-choices' role='radiogroup'></div>";
    row.querySelector("strong").textContent = title;
    row.querySelector("span").textContent = state.effort[key]
      ? `Our starting guess: ${EFFORT_LABELS[MODEL.effort[key]].toLowerCase()}. ${MODEL.effort_reasons[key]}`
      : MODEL.effort_reasons[key];
    row.querySelector(".effort-choices").setAttribute("aria-label", `Effort for ${title}`);
    [1, 2, 3, 4].forEach((n) => {
      const b = document.createElement("button");
      b.type = "button";
      b.setAttribute("role", "radio");
      b.setAttribute("aria-checked", String(effortOf(key) === n));
      b.innerHTML = `<span class="pips" aria-hidden="true">${"<i class='on'></i>".repeat(n)}${"<i></i>".repeat(4 - n)}</span>${EFFORT_LABELS[n]}`;
      b.addEventListener("click", () => {
        if (n === MODEL.effort[key]) delete state.effort[key]; else state.effort[key] = n;
        render();
      });
      row.querySelector(".effort-choices").appendChild(b);
    });
    rows.appendChild(row);
  });
  $("effort-reset").hidden = Object.keys(state.effort).length === 0;

  // Step 4: guesses.
  const plan = state.plan.map((k) => STRATEGIES[k][0].toLowerCase());
  $("plan-summary").textContent = state.agency && plan.length
    ? `Your plan for a ${AGENCIES[state.agency].title.toLowerCase()} agency: ${listText(plan)}.` : "";
  const guesses = $("guesses");
  guesses.innerHTML = "";
  state.goals.forEach((g) => {
    const box = document.createElement("fieldset");
    box.className = "guess";
    box.innerHTML = "<legend></legend><div class='scale'></div>";
    box.querySelector("legend").textContent = GOALS[g].title;
    SCALE.forEach((s, i) => {
      const b = document.createElement("button");
      b.type = "button";
      b.innerHTML = "<strong></strong><span></span>";
      b.querySelector("strong").textContent = s.label;
      b.querySelector("span").textContent = s.text;
      b.setAttribute("aria-pressed", String(state.guess[g] === i));
      b.addEventListener("click", () => { state.guess[g] = i; render(); });
      box.querySelector(".scale").appendChild(b);
    });
    guesses.appendChild(box);
  });

  document.querySelectorAll(".step").forEach((s) => { s.hidden = +s.dataset.step !== step; });
  document.querySelectorAll(".progress li").forEach((li) => {
    const n = +li.dataset.step;
    li.className = n === step ? "current" : n < step ? "done" : "";
    if (n === step) li.setAttribute("aria-current", "step"); else li.removeAttribute("aria-current");
  });
  $("back").hidden = step === 1;
  $("next").textContent = step === 4 ? "See my results" : "Next";
  $("next").disabled = !ready();
}

function toggle(list, key) {
  const i = list.indexOf(key);
  if (i >= 0) list.splice(i, 1); else list.push(key);
}

function ready() {
  if (step === 1) return !!state.agency;
  if (step === 2) return state.goals.length > 0;
  if (step === 3) return state.plan.length > 0 && fits();
  return state.goals.every((g) => g in state.guess);
}

$("next").addEventListener("click", () => {
  if (!ready()) return;
  if (step === 4) {
    location.href = `results.html?${encodeState(state)}`;
    return;
  }
  step += 1;
  render();
  window.scrollTo({ top: 0, behavior: "smooth" });
});
$("back").addEventListener("click", () => { step = Math.max(1, step - 1); render(); });
$("effort-reset").addEventListener("click", () => { state.effort = {}; render(); });
$("budget-range").addEventListener("input", (e) => { state.budget = +e.target.value; render(); });
$("budget-reset").addEventListener("click", () => { state.budget = null; state.weight = null; render(); });

// The expandable note listing every lever in plain words (same list as step 3).
const leverEntries = Object.values(STRATEGIES);
$("levers-summary").textContent = `What are the ${leverEntries.length} policy levers?`;
leverEntries.forEach(([title, text]) => {
  const li = document.createElement("li");
  li.innerHTML = "<strong></strong> ";
  li.querySelector("strong").textContent = title;
  li.append(document.createTextNode(text));
  $("levers-list").appendChild(li);
});

// Load the model (effort ratings, investment levels, counts), then show the steps.
fetch("data/model.json").then((r) => r.json()).then((model) => {
  MODEL = model;
  const levers = model.levers.length;
  const portfolios = 2 ** levers;
  const d = model.defaults;
  const runs = portfolios * model.jurisdictions.length * d.political_conditions * d.trials;
  const n = (x) => x.toLocaleString("en-US");
  const millions = runs >= 1e6 ? `about ${(runs / 1e6).toFixed(1)} million` : n(runs);
  $("method").innerHTML = `<strong>How it works:</strong> we describe <strong>${levers} policy levers</strong> a government can use and combine them into <strong>${n(portfolios)} possible portfolios</strong>. Each portfolio is simulated over ${d.years} years in ${model.jurisdictions.length} kinds of agencies, with and without hostile elections, ${d.trials} times each: <strong>${millions} simulations</strong>, based on <strong>${model.relationships.length} assumed interactions</strong> between strategies.`;
  render();
}).catch((error) => {
  console.error(error);
  $("method").textContent = "The model could not load. If you opened this file directly, run ./preview_website.sh instead.";
});
