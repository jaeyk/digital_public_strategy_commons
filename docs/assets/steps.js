// Page 1: four steps, one at a time. The choices are passed to results.html in the URL.
import { AGENCIES, GOALS, STRATEGIES, SCALE, encodeState, decodeState, listText } from "./shared.js";

const state = { agency: null, goals: [], plan: [], guess: {}, ...decodeState(location.search) };
let step = 1;
const $ = (id) => document.getElementById(id);

function card({ title, text, selected, onClick, role = "checkbox" }) {
  const b = document.createElement("button");
  b.type = "button";
  b.className = "card";
  b.setAttribute("role", role);
  b.setAttribute("aria-checked", String(selected));
  b.innerHTML = "<strong></strong><span></span>";
  b.querySelector("strong").textContent = title;
  b.querySelector("span").textContent = text;
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

  const goals = $("goals");
  goals.innerHTML = "";
  Object.entries(GOALS).forEach(([key, g]) => goals.appendChild(card({ ...g, selected: state.goals.includes(key),
    onClick: () => { toggle(state.goals, key); render(); } })));

  const strategies = $("strategies");
  strategies.innerHTML = "";
  Object.entries(STRATEGIES).forEach(([key, [title, text]]) => strategies.appendChild(card({ title, text,
    selected: state.plan.includes(key), onClick: () => { toggle(state.plan, key); render(); } })));

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
      b.textContent = s.label;
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
  if (step === 3) return state.plan.length > 0;
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

render();
