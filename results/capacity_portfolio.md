# Model 1: capacity portfolio

All 32,768 combinations of 15 levers, 4 jurisdiction types, 16 years, 40 Monte Carlo trials per run, seed 20261111.
Scores are net value above the status quo: outcome-index points (0-100 scale) minus 10 points per 1.0 of extra annual spending as a share of the jurisdiction's own budget (lever costs plus the lock-in premium on vendor contracts). All parameters are illustrative assumptions; results show what follows from the stated assumptions, not empirical estimates.

- **Positive:** net value with stable politics, averaged over the four jurisdiction types.
- **Durable:** the same with elections every four years that can bring a hostile successor.
- **Scalable:** the lowest net value across the four jurisdiction types (stable politics).

## 1. Best portfolios by criterion

### Positive

| Rank | Portfolio | Positive | Durable | Scalable | Outcome gain | Extra spend % of budget | Levers surviving turnover % |
|---:|---|---:|---:|---:|---:|---:|---:|
| 1 | team + insourcing + funding + policy + procurement + platforms + collaboration + safeguards | 10.91 | 9.34 | 0.78 | 16.75 | 58.45 | 38.75 |
| 2 | team + insourcing + funding + policy + platforms + collaboration + safeguards | 10.89 | 9.24 | 1.27 | 16.47 | 55.82 | 40.27 |
| 3 | team + insourcing + mandate + funding + policy + platforms + collaboration + safeguards | 10.66 | 10.25 | 0.94 | 16.47 | 58.12 | 75.70 |
| 4 | team + insourcing + mandate + funding + policy + procurement + platforms + collaboration + safeguards | 10.58 | 10.14 | 0.44 | 16.50 | 59.25 | 72.92 |
| 5 | team + insourcing + funding + policy + portability + platforms + collaboration + safeguards | 10.56 | 9.03 | 0.84 | 16.40 | 58.35 | 40.16 |

Smallest portfolio reaching 90% of the best positive score: **team + insourcing + policy + platforms + collaboration + safeguards** (10.00 vs. 10.91).

### Durable

| Rank | Portfolio | Positive | Durable | Scalable | Outcome gain | Extra spend % of budget | Levers surviving turnover % |
|---:|---|---:|---:|---:|---:|---:|---:|
| 1 | team + insourcing + mandate + funding + policy + platforms + collaboration + safeguards | 10.66 | 10.25 | 0.94 | 16.47 | 58.12 | 75.70 |
| 2 | team + insourcing + mandate + funding + policy + procurement + platforms + collaboration + safeguards | 10.58 | 10.14 | 0.44 | 16.50 | 59.25 | 72.92 |
| 3 | team + insourcing + mandate + funding + policy + portability + platforms + collaboration + safeguards | 10.23 | 9.82 | 0.51 | 16.15 | 59.15 | 74.17 |
| 4 | team + insourcing + mandate + funding + policy + procurement + portability + platforms + collaboration + safeguards | 10.20 | 9.81 | 0.06 | 16.22 | 60.28 | 72.06 |
| 5 | team + insourcing + authority + mandate + funding + policy + procurement + platforms + collaboration + safeguards | 9.83 | 9.59 | -0.23 | 15.99 | 61.57 | 71.06 |

Smallest portfolio reaching 90% of the best durable score: **team + insourcing + funding + policy + platforms + collaboration + safeguards** (9.24 vs. 10.25).

### Scalable

| Rank | Portfolio | Positive | Durable | Scalable | Outcome gain | Extra spend % of budget | Levers surviving turnover % |
|---:|---|---:|---:|---:|---:|---:|---:|
| 1 | policy + platforms + collaboration | 6.00 | 5.59 | 2.79 | 8.72 | 27.26 | 28.33 |
| 2 | policy + platforms + collaboration + safeguards | 7.22 | 6.59 | 2.76 | 10.86 | 36.42 | 33.91 |
| 3 | insourcing + policy + platforms + collaboration | 6.66 | 5.23 | 2.51 | 9.16 | 24.96 | 26.72 |
| 4 | insourcing + policy + platforms + collaboration + safeguards | 7.94 | 6.35 | 2.50 | 11.36 | 34.13 | 32.62 |
| 5 | mandate + policy + platforms + collaboration | 5.77 | 5.52 | 2.46 | 8.72 | 29.55 | 70.00 |

Smallest portfolio reaching 90% of the best scalable score: **policy + platforms + collaboration** (2.79 vs. 2.79).

## 2. Best portfolio for each jurisdiction type

| Jurisdiction | Criterion | Best portfolio | Gain | Smallest at 90% | Gain |
|---|---|---|---:|---|---:|
| Well-resourced and committed | positive | team + insourcing + funding + policy + procurement + portability + entrants + open_source + platforms + collaboration + safeguards | 22.76 | team + insourcing + funding + policy + platforms + collaboration + safeguards | 21.54 |
| Well-resourced and committed | durable | team + insourcing + mandate + funding + policy + procurement + platforms + collaboration + safeguards + public_option | 21.94 | team + insourcing + mandate + funding + policy + platforms + collaboration + safeguards | 20.60 |
| Well-resourced and reluctant | positive | team + insourcing + funding + policy + procurement + platforms + collaboration + safeguards + public_option | 7.99 | team + insourcing + policy + platforms + collaboration + safeguards | 7.50 |
| Well-resourced and reluctant | durable | team + insourcing + mandate + funding + policy + procurement + platforms + collaboration + safeguards + public_option | 7.06 | team + policy + platforms + collaboration + safeguards + public_option | 6.38 |
| Small and committed | positive | team + insourcing + funding + policy + platforms + collaboration + safeguards | 12.99 | team + insourcing + policy + platforms + collaboration + safeguards | 11.79 |
| Small and committed | durable | team + insourcing + mandate + funding + policy + platforms + collaboration + safeguards | 12.30 | team + insourcing + funding + policy + platforms + collaboration + safeguards | 11.18 |
| Small and reluctant | positive | policy + platforms + collaboration | 2.79 | policy + platforms + collaboration | 2.79 |
| Small and reluctant | durable | policy + platforms + collaboration + safeguards | 3.16 | policy + platforms + collaboration | 3.09 |

## 3. Lever profiles: does each lever work alone?

*Alone* is the lever's effect when adopted by itself. *In combination* is its effect averaged over every combination of the other levers. A large gap means the lever's value depends on what it is combined with (package-like); a small gap means it works the same on any menu.

| Lever | Framework | Cost | Positive: alone | Positive: in combination | Durable: alone | Durable: in combination | Scalable: in combination |
|---|---|---:|---:|---:|---:|---:|---:|
| Core digital team | A1, A2, A3, A4, A5 | 0.12 | -0.72 | 0.94 | 0.12 | 0.97 | -0.52 |
| In-house delivery at scale (insourcing) | A6 | 0.03 | -0.48 | 0.55 | -1.18 | -0.09 | -0.31 |
| Spend controls and service standards | B1, B2, B4 | 0.03 | -0.89 | -0.59 | -0.53 | -0.38 | -0.60 |
| Legal mandate | B3 | 0.01 | -0.23 | -0.19 | -0.21 | -0.25 | -0.22 |
| Product (continuous) funding | C1, C2 | 0.04 | -0.72 | -0.01 | -0.42 | 0.05 | -0.62 |
| Policy and process simplification | D1, D2 | 0.03 | 0.93 | 2.80 | 0.93 | 2.35 | 0.98 |
| Strategic and modular procurement | E1, E2 | 0.03 | -0.20 | 0.04 | -0.02 | 0.10 | -0.34 |
| Data rights and open interfaces | E5, F3, H1 | 0.02 | -0.22 | -0.06 | -0.09 | -0.02 | -0.19 |
| New-entrant and mission-aligned vendor pipeline | E3, E4, E8, E9 | 0.05 | -0.70 | -0.38 | -0.28 | -0.22 | -0.79 |
| Open source by default | F1 | 0.04 | -0.82 | -0.41 | -0.62 | -0.42 | -0.57 |
| Funding open source maintenance | F2 | 0.04 | -0.91 | -0.54 | -0.55 | -0.40 | -0.65 |
| Shared platforms (DPI building blocks) | F4, F5 | 0.10 | 1.25 | 2.90 | 1.57 | 2.71 | 1.49 |
| Collaboration between governments | I1, I2, I3, E6 | 0.03 | 1.88 | 3.03 | 1.78 | 2.72 | 2.54 |
| Accountability and safeguards | J1, J2, J3, E7 | 0.04 | 1.20 | 1.33 | 0.99 | 1.09 | 0.29 |
| Public option | G1, G2 | 0.12 | -0.65 | -0.39 | 0.08 | -0.06 | -1.26 |

## 4. Menu or package?

Share of each top portfolio's gain that comes from combining levers rather than from each lever alone. 0% would be a pure menu. The menu baseline switches off every assumed relationship in `models/common/relationships.py`; what remains comes from the model's structure (budget limits, saturation of 0-1 indices, and causal chains such as talent -> procurement leverage).

| Criterion | Best (assumed relationships) | Package share % | Best (menu baseline) | Package share % |
|---|---|---:|---|---:|
| positive | team + insourcing + funding + policy + procurement + platforms + collaboration + safeguards | 71.11 | team + procurement + entrants + platforms + collaboration + safeguards | -40.78 |
| durable | team + insourcing + mandate + funding + policy + platforms + collaboration + safeguards | 65.05 | team + procurement + entrants + platforms + collaboration + safeguards | -28.59 |
| scalable | policy + platforms + collaboration | 67.80 | procurement + entrants + platforms + collaboration + safeguards | -27.81 |

### Pairwise relationships

Each pair is classified with the definitions in framework.md Section 5, from interaction effects averaged over all combinations of the other 13 levers. *Hypothesis* is the relationship assumed in the code (blank = none assumed, so any non-additive result emerged from the model's structure). *Contexts +* is the share of contexts in which the interaction is positive; values far from 0% or 100% mean the relationship depends on context. Additive pairs with no hypothesis are omitted.

| Pair | Hypothesis | Positive | Durable | Scalable | Contexts + | Menu baseline |
|---|---|---|---|---|---|---|
| team + insourcing | prerequisite; complement | prerequisite (insourcing needs team) (1.14) | prerequisite (insourcing needs team) (0.87) | joint (works only together) (0.35) | 100% | prerequisite (insourcing needs team) |
| authority + platforms | complement | prerequisite (authority needs platforms) (0.96) | prerequisite (authority needs platforms) (0.85) | prerequisite (authority needs platforms) (0.54) | 100% | additive |
| policy + platforms |  | complementary (0.94) | complementary (0.74) | complementary (0.43) | 100% | additive |
| team + public_option |  | prerequisite (public_option needs team) (0.21) | additive (0.06) | joint (works only together) (0.88) | 71% | additive |
| policy + collaboration |  | complementary (0.67) | complementary (0.57) | complementary (0.35) | 100% | additive |
| funding + platforms | complement | prerequisite (funding needs platforms) (0.64) | prerequisite (funding needs platforms) (0.60) | prerequisite (funding needs platforms) (0.40) | 100% | additive |
| collaboration + public_option |  | additive (-0.24) | additive (-0.19) | conflict (-0.59) | 22% | additive |
| insourcing + collaboration |  | complementary (0.58) | prerequisite (insourcing needs collaboration) (0.51) | prerequisite (insourcing needs collaboration) (0.27) | 100% | additive |
| team + policy |  | complementary (0.55) | complementary (0.38) | prerequisite (team needs policy) (0.18) | 100% | additive |
| insourcing + public_option |  | conflict (-0.48) | conflict (-0.35) | additive (0.10) | 1% | conflict |
| insourcing + mandate |  | additive (0.00) | joint (works only together) (0.48) | additive (0.02) | 51% | additive |
| platforms + public_option |  | additive (0.26) | additive (0.10) | prerequisite (public_option needs platforms) (0.47) | 84% | additive |
| entrants + public_option | conflict | additive (-0.03) | additive (-0.09) | joint (works only together) (0.44) | 38% | additive |
| platforms + safeguards |  | substitute (-0.40) | substitute (-0.32) | additive (-0.12) | 0% | substitute |
| platforms + collaboration |  | substitute (-0.40) | substitute (-0.34) | additive (-0.00) | 7% | substitute |
| funding + public_option |  | additive (0.08) | additive (-0.02) | joint (works only together) (0.36) | 70% | joint (works only together) |
| team + collaboration |  | additive (0.26) | additive (0.15) | prerequisite (team needs collaboration) (0.35) | 86% | substitute |
| insourcing + funding |  | prerequisite (funding needs insourcing) (0.26) | joint (works only together) (0.35) | additive (0.08) | 100% | additive |
| maintenance + public_option |  | additive (0.12) | additive (0.07) | joint (works only together) (0.34) | 83% | additive |
| team + entrants |  | additive (0.07) | additive (0.02) | joint (works only together) (0.32) | 71% | substitute |
| open_source + public_option |  | additive (0.06) | additive (0.02) | joint (works only together) (0.30) | 64% | additive |
| authority + public_option |  | additive (0.13) | additive (0.06) | joint (works only together) (0.30) | 85% | additive |
| team + funding | complement | prerequisite (funding needs team) (0.25) | prerequisite (funding needs team) (0.18) | joint (works only together) (0.29) | 99% | additive |
| insourcing + policy |  | complementary (0.28) | additive (0.19) | additive (0.03) | 100% | additive |
| mandate + policy |  | additive (-0.01) | prerequisite (mandate needs policy) (0.28) | additive (-0.00) | 22% | additive |
| team + procurement | prerequisite; moderator | prerequisite (procurement needs team) (0.26) | prerequisite (procurement needs team) (0.19) | joint (works only together) (0.28) | 99% | additive |
| entrants + collaboration |  | additive (-0.13) | additive (-0.10) | conflict (-0.27) | 29% | additive |
| safeguards + public_option |  | additive (0.10) | additive (-0.00) | prerequisite (public_option needs safeguards) (0.27) | 74% | additive |
| team + maintenance |  | additive (0.08) | additive (0.04) | joint (works only together) (0.25) | 80% | additive |
| team + open_source |  | additive (0.07) | additive (0.03) | joint (works only together) (0.24) | 74% | additive |
| team + authority | conflict | conflict (-0.23) | conflict (-0.20) | additive (0.10) | 5% | additive |
| portability + entrants | prerequisite | joint (works only together) (0.22) | joint (works only together) (0.17) | joint (works only together) (0.16) | 100% | additive |
| procurement + public_option |  | additive (-0.04) | additive (-0.06) | joint (works only together) (0.22) | 31% | conflict |
| mandate + safeguards |  | additive (0.00) | prerequisite (mandate needs safeguards) (0.20) | additive (0.02) | 48% | additive |
| team + platforms |  | additive (-0.05) | additive (-0.13) | prerequisite (team needs platforms) (0.19) | 44% | substitute |
| entrants + open_source |  | joint (works only together) (0.18) | additive (0.13) | joint (works only together) (0.17) | 100% | additive |
| open_source + maintenance | prerequisite | additive (0.13) | additive (0.10) | additive (0.13) | 100% | additive |
| procurement + collaboration | conflict | additive (-0.03) | additive (-0.02) | additive (-0.10) | 37% | additive |
| portability + open_source | complement | additive (0.05) | additive (0.05) | additive (0.08) | 82% | additive |

### Strongest three-way interactions (positive and durable)

What a trio adds beyond its pairs. Pairwise tests miss these.

| Criterion | Trio | Three-way interaction |
|---|---|---:|
| positive | team + collaboration + public_option | -0.30 |
| positive | team + insourcing + public_option | -0.28 |
| positive | policy + platforms + collaboration | -0.27 |
| positive | team + platforms + public_option | -0.25 |
| positive | team + policy + platforms | -0.25 |
| durable | team + collaboration + public_option | -0.25 |
| durable | team + insourcing + funding | 0.22 |
| durable | policy + platforms + collaboration | -0.20 |
| durable | team + policy + platforms | -0.20 |
| durable | team + insourcing + public_option | -0.18 |

## 5. Does order matter?

Interaction (positive criterion, averaged over jurisdiction types) when both levers start together, and when one starts four years before the other. Each interaction is measured against single-lever runs with the same timing, so the comparison isolates the synergy rather than the cost of delaying a bigger lever. *Order effect* is (first listed first) minus (second listed first); a positive value means the first listed lever should come first.

| Pair | Interaction: together | First listed first | Second listed first | Order effect |
|---|---:|---:|---:|---:|
| team + procurement | 0.33 | 0.20 | 0.15 | 0.04 |
| portability + entrants | 0.20 | 0.14 | 0.08 | 0.06 |
| maintenance + open_source | 0.10 | 0.04 | 0.04 | -0.00 |
| policy + team | 0.73 | 0.47 | 0.42 | 0.05 |
| authority + platforms | 0.93 | 0.52 | 0.38 | 0.14 |
| mandate + team | 0.00 | -0.00 | 0.00 | -0.00 |
| team + insourcing | 1.11 | 0.80 | 0.50 | 0.30 |

## 6. Sensitivity

Relationship strengths scaled from 0 (menu baseline) to 1.5x. *Pairs unchanged* is the share of the 105 pairs whose positive-criterion classification matches the 1.0x run.

| Strength | Criterion | Best portfolio | Score | Package share % | Pairs unchanged |
|---|---|---|---:|---:|---:|
| 0.0x | positive | team + procurement + entrants + platforms + collaboration + safeguards | 16.76 | -40.78 | 80% |
| 0.0x | durable | team + procurement + entrants + platforms + collaboration + safeguards | 16.10 | -28.59 | 80% |
| 0.0x | scalable | procurement + entrants + platforms + collaboration + safeguards | 10.27 | -27.81 | 80% |
| 0.5x | positive | team + insourcing + policy + procurement + platforms + collaboration + safeguards | 13.37 | 8.28 | 90% |
| 0.5x | durable | team + policy + procurement + platforms + collaboration + safeguards | 11.83 | -3.05 | 90% |
| 0.5x | scalable | policy + platforms + collaboration + safeguards | 5.89 | -4.94 | 90% |
| 1.0x | positive | team + insourcing + funding + policy + procurement + platforms + collaboration + safeguards | 10.91 | 71.11 | 100% |
| 1.0x | durable | team + insourcing + mandate + funding + policy + platforms + collaboration + safeguards | 10.25 | 65.05 | 100% |
| 1.0x | scalable | policy + platforms + collaboration | 2.79 | 67.80 | 100% |
| 1.5x | positive | team + insourcing + funding + policy + platforms + collaboration + safeguards | 8.15 | 144.21 | 83% |
| 1.5x | durable | team + insourcing + mandate + funding + policy + procurement + platforms + collaboration + safeguards | 7.89 | 132.85 | 83% |
| 1.5x | scalable | policy + platforms + collaboration | 0.68 | 475.50 | 83% |

Seed check (seed 20261112): overlap of the top 10 portfolios with the main run: positive 100%, durable 90%, scalable 100%.

## 7. In-house delivery: scope, scale, and pace

framework.md Section 4 asks whether an in-house team could cover everything vendors do (scope), whether it can grow large enough (scale), and whether it can do so fast enough (pace). In the engine, in-house staff capacity grows only as fast as hiring allows, shrinks with attrition, and is paid for before work moves; work moves in-house only as fast as experienced staff can manage, and each move dents service quality in proportion to inexperience. Each jurisdiction type has a ceiling on the share of vendor work it could realistically run (well-resourced 60%, small 35%), which pooling and shared platforms can raise.

*Worst transition dip* is the lowest yearly outcome of the approach minus the same portfolio without insourcing (negative = service disruption during the transition).

| Jurisdiction | Approach | Work in-house at end % | Years to 25% | Years to 50% | Worst transition dip | Extra spend % of budget | Net value (stable) | Net value (turnover) |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| Well-resourced and committed | Informed buyer: team + procurement | 0.00 | not reached | not reached | n/a | 15.51 | 1.77 | 1.86 |
| Well-resourced and committed | Insourcing without a core team | 36.66 | 8 | not reached | -1.46 | -7.43 | 0.15 | -1.33 |
| Well-resourced and committed | Builder: team + insourcing | 53.16 | 5 | 14 | -1.05 | 3.25 | 3.28 | 1.21 |
| Well-resourced and committed | Builder with stable funding | 57.64 | 5 | 10 | -0.96 | 6.37 | 4.16 | 2.29 |
| Well-resourced and committed | Builder with pooling: + funding, collaboration, platforms | 70.65 | 5 | 10 | -0.78 | 8.71 | 11.54 | 8.90 |
| Well-resourced and committed | Hybrid: team + procurement + insourcing + funding | 57.64 | 5 | 10 | -0.97 | 8.79 | 4.74 | 2.90 |
| Well-resourced and reluctant | Informed buyer: team + procurement | 0.00 | not reached | not reached | n/a | 17.34 | -0.21 | 0.25 |
| Well-resourced and reluctant | Insourcing without a core team | 14.66 | not reached | not reached | -0.62 | -1.03 | -0.16 | -0.71 |
| Well-resourced and reluctant | Builder: team + insourcing | 17.60 | not reached | not reached | -0.56 | 12.72 | -0.02 | -0.34 |
| Well-resourced and reluctant | Builder with stable funding | 19.89 | not reached | not reached | -0.56 | 17.21 | -0.27 | -0.43 |
| Well-resourced and reluctant | Builder with pooling: + funding, collaboration, platforms | 19.89 | not reached | not reached | -0.47 | 20.84 | 4.28 | 3.66 |
| Well-resourced and reluctant | Hybrid: team + procurement + insourcing + funding | 19.89 | not reached | not reached | -0.57 | 20.06 | -0.22 | -0.32 |
| Small and committed | Informed buyer: team + procurement | 0.00 | not reached | not reached | n/a | 46.63 | -0.79 | 0.58 |
| Small and committed | Insourcing without a core team | 22.00 | not reached | not reached | -1.20 | 2.93 | -0.95 | -1.65 |
| Small and committed | Builder: team + insourcing | 31.90 | 10 | not reached | -0.95 | 39.30 | -0.40 | -0.44 |
| Small and committed | Builder with stable funding | 33.94 | 8 | not reached | -0.97 | 51.20 | -0.81 | -0.73 |
| Small and committed | Builder with pooling: + funding, collaboration, platforms | 42.39 | 8 | not reached | -0.79 | 60.44 | 5.86 | 5.22 |
| Small and committed | Hybrid: team + procurement + insourcing + funding | 33.94 | 8 | not reached | -0.98 | 59.31 | -0.73 | -0.48 |
| Small and reluctant | Informed buyer: team + procurement | 0.00 | not reached | not reached | n/a | 48.54 | -3.10 | -1.33 |
| Small and reluctant | Insourcing without a core team | 8.15 | not reached | not reached | -0.44 | 7.23 | -0.96 | -1.02 |
| Small and reluctant | Builder: team + insourcing | 9.78 | not reached | not reached | -0.40 | 46.28 | -3.23 | -1.93 |
| Small and reluctant | Builder with stable funding | 11.05 | not reached | not reached | -0.41 | 59.30 | -4.39 | -2.78 |
| Small and reluctant | Builder with pooling: + funding, collaboration, platforms | 11.05 | not reached | not reached | -0.34 | 69.14 | -0.32 | 0.85 |
| Small and reluctant | Hybrid: team + procurement + insourcing + funding | 11.05 | not reached | not reached | -0.41 | 68.36 | -4.98 | -3.07 |

### Could it cover everything, and how fast?

The pooled builder approach with the scope ceiling removed (100% of vendor work allowed), run for 30 years, with normal and doubled hiring capacity, and with and without the AI shock.

| Jurisdiction | Hiring capacity | AI shock | Years to 50% | Years to 75% | Years to 90% | In-house after 30 years % |
|---|---|---|---:|---:|---:|---:|
| Well-resourced and committed | 1x | no | 10 | 18 | 26 | 94.79 |
| Well-resourced and committed | 1x | yes | 9 | 13 | 15 | 94.79 |
| Well-resourced and committed | 2x | no | 9 | 13 | 15 | 94.79 |
| Well-resourced and committed | 2x | yes | 9 | 13 | 15 | 94.79 |
| Small and committed | 1x | no | 22 | not in 30 years | not in 30 years | 58.14 |
| Small and committed | 1x | yes | 12 | 20 | 27 | 94.83 |
| Small and committed | 2x | no | 9 | 14 | 18 | 94.79 |
| Small and committed | 2x | yes | 9 | 13 | 15 | 94.79 |

### Sensitivity: when does building beat buying well?

Net value of the pooled builder approach minus the informed-buyer approach, as one assumption varies. Positive values favor building in-house.

| Assumption | Value | Well-resourced and committed | Small and committed |
|---|---:|---:|---:|
| inhouse_unit_cost | 0.70 | 10.42 | 7.03 |
| inhouse_unit_cost | 0.85 | 9.78 | 6.64 |
| inhouse_unit_cost | 1.00 | 9.13 | 6.26 |
| inhouse_unit_cost | 1.20 | 8.28 | 5.75 |
| transition_speed | 0.04 | 6.23 | 6.08 |
| transition_speed | 0.08 | 9.78 | 6.64 |
| transition_speed | 0.16 | 9.93 | 6.64 |
| hire_rate_max | 0.03 | 7.33 | 5.10 |
| hire_rate_max | 0.05 | 9.78 | 6.64 |
| hire_rate_max | 0.10 | 9.06 | 8.10 |

## 8. The AI shock

AI arrives in year 4 and ramps up over about two years. The share the government absorbs with its own capacity (talent, portability, shared infrastructure, insourced work) raises productivity, quality, reach, and the in-house scope ceiling. The rest arrives through vendors: some quality gain, but more lock-in, market concentration, and AI contract spending, reduced by strategic procurement. Without safeguards, AI also erodes legitimacy. *AI effect* is net value with the shock minus net value without it, for the same portfolio.

| Jurisdiction | AI effect on status quo | Lock-in at end with AI % | Lock-in at end without AI % | AI effect on best AI-era portfolio | Best AI-era portfolio |
|---|---:|---:|---:|---:|---|
| Well-resourced and committed | -0.17 | 87.87 | 74.11 | 3.87 | team + insourcing + funding + policy + procurement + portability + entrants + open_source + platforms + collaboration + safeguards |
| Well-resourced and reluctant | -0.17 | 89.24 | 77.48 | 2.65 | team + insourcing + funding + policy + procurement + portability + open_source + platforms + collaboration + safeguards |
| Small and committed | -0.13 | 89.38 | 77.12 | 5.03 | team + insourcing + funding + policy + platforms + collaboration + safeguards |
| Small and reluctant | -0.10 | 90.81 | 80.89 | 0.88 | insourcing + policy + platforms + collaboration |

### Which levers matter more once AI arrives?

Average effect of adding each lever (positive criterion), with and without the AI shock.

| Lever | Without AI | With AI | Change |
|---|---:|---:|---:|
| In-house delivery at scale (insourcing) | 0.55 | 1.62 | 1.08 |
| Core digital team | 0.94 | 1.56 | 0.62 |
| Policy and process simplification | 2.80 | 3.39 | 0.59 |
| Data rights and open interfaces | -0.06 | 0.38 | 0.43 |
| Collaboration between governments | 3.03 | 3.47 | 0.43 |
| Open source by default | -0.41 | -0.18 | 0.23 |
| Shared platforms (DPI building blocks) | 2.90 | 3.08 | 0.18 |
| Product (continuous) funding | -0.01 | 0.07 | 0.08 |
| Funding open source maintenance | -0.54 | -0.47 | 0.07 |
| Strategic and modular procurement | 0.04 | 0.08 | 0.04 |
| Spend controls and service standards | -0.59 | -0.59 | -0.00 |
| Legal mandate | -0.19 | -0.20 | -0.01 |
| New-entrant and mission-aligned vendor pipeline | -0.38 | -0.50 | -0.12 |
| Accountability and safeguards | 1.33 | 1.19 | -0.14 |
| Public option | -0.39 | -0.63 | -0.25 |

### Does AI widen or narrow the gap between jurisdictions?

Gap between the best achievable net value in the strongest and weakest jurisdiction type: 19.97 without AI, 23.30 with AI. Scalable floor (best lowest-type value): 2.79 without AI, 3.50 with AI. Status quo outcome change from AI by type: Well-resourced and committed -0.17, Well-resourced and reluctant -0.17, Small and committed -0.13, Small and reluctant -0.10.

## Caveats

- Every parameter, relationship strength, and jurisdiction profile is an assumption to be calibrated with evidence and practitioner input. The model shows the consequences of these assumptions; it cannot confirm them.
- Relationships labeled with a hypothesis were put in deliberately. Non-additive results without a hypothesis come from structure, mainly the budget limit (which makes costly levers substitutes in small jurisdictions) and causal chains between state variables.
- Levers group several framework strategies (see `models/common/levers.py`), so effects within a group, such as fellowships versus permanent teams, cannot be separated.
- Vendor behavior is fixed at 'lock-in' here. Model 2 lets the vendor respond strategically.
- In-house scope ceilings, hiring capacity, transition speed, and in-house unit cost are assumptions with large effects; Section 7 shows how results move with them.
- The AI shock is one stylized scenario (timing, strength, and how capacity absorbs it are all assumptions), not a forecast.
- Turnover is a reduced-form rule. Model 3 treats the successor's decision as a strategic choice.

