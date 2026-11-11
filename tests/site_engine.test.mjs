// Checks that the website's JavaScript engine (docs/assets/engine.js) reproduces the Python
// engine on the deterministic cases in docs/data/parity.json.
// Run: node tests/site_engine.test.mjs   (after: python -m models.export_site_data)
import { readFileSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { dirname, join } from "node:path";
import { simulate } from "../docs/assets/engine.js";

const root = join(dirname(fileURLToPath(import.meta.url)), "..");
const model = JSON.parse(readFileSync(join(root, "docs/data/model.json"), "utf8"));
const cases = JSON.parse(readFileSync(join(root, "docs/data/parity.json"), "utf8"));
const TOLERANCE = 2e-3; // exported values are rounded to 4 decimal places

let failures = 0;
for (const c of cases) {
  const r = simulate(model, {
    levers: c.levers, jurisdiction: c.jurisdiction, vendorAction: c.vendor_action,
    aiShockYear: c.ai_shock_year, years: 16, trials: 1, params: { quality_noise: 0 },
  });
  const checks = [["outcome_gain", r.outcomeGain, c.outcome_gain], ["spend_share", r.spendShare, c.spend_share],
    ["vendor_payoff", r.vendorPayoff, c.vendor_payoff],
    ...Object.entries(c.finals).map(([k, v]) => [`finals.${k}`, r.finals[k], v]),
    ...c.outcome_path.map((v, t) => [`outcome_path[${t}]`, r.paths.outcome[t], v])];
  for (const [name, got, want] of checks) {
    if (Math.abs(got - want) > TOLERANCE) {
      failures++;
      if (failures <= 10) {
        console.error(`MISMATCH ${c.jurisdiction} ${c.vendor_action} ai=${c.ai_shock_year} [${c.levers}] ${name}: js=${got} py=${want}`);
      }
    }
  }
}
if (failures) {
  console.error(`${failures} mismatches across ${cases.length} cases`);
  process.exit(1);
}
console.log(`OK: JavaScript engine matches Python on ${cases.length} cases`);
