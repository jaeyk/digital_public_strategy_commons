# Model 3: durability under political turnover (OpenSpiel game)

OpenSpiel game `python_dpsc_turnover`: a reform government chooses protections for its program; two elections follow; after each, a new government (if power changes hands) with low, medium, or high hostility chooses to keep, scale back, or dismantle the program. Solved by backward induction over the full game tree (subgame-perfect equilibrium). All payoff numbers are illustrative assumptions.

Protections (political cost to the reformer / added cost to a successor of cutting the whole program): **mandate** 1.0 / 3.0; **budget_line** 0.8 / 1.5; **constituency** 0.8 / 2.5; **embedding** 1.2 / 2.0.

## 1. Equilibrium protections by political scenario

| Scenario | Equilibrium protections | Program surviving % | Reformer value | Surviving with no protections % | Surviving with all protections % |
|---|---|---:|---:|---:|---:|
| Supportive politics | mandate | 75.20 | 12.11 | 36.00 | 94.18 |
| Contested politics | mandate + budget_line + constituency | 88.28 | 11.50 | 25.00 | 88.28 |
| Polarized politics | mandate + budget_line + constituency | 76.28 | 10.53 | 25.00 | 76.28 |
| Polarized, unfinished insourcing | mandate + budget_line + constituency | 76.28 | 9.58 | 25.00 | 76.28 |

## 2. Survival for every package of protections

Expected share of the program still running after two elections.

| Protections | Supportive politics | Contested politics | Polarized politics | Polarized, unfinished insourcing |
|---|---:|---:|---:|---:|
| no protections | 36.00 | 25.00 | 25.00 | 25.00 |
| mandate | 75.20 | 61.25 | 41.69 | 41.69 |
| budget_line | 48.00 | 35.00 | 28.75 | 28.75 |
| mandate + budget_line | 76.18 | 62.78 | 42.81 | 42.81 |
| constituency | 64.00 | 49.00 | 33.06 | 33.06 |
| mandate + constituency | 81.40 | 72.62 | 60.69 | 60.69 |
| budget_line + constituency | 76.18 | 62.78 | 42.81 | 42.81 |
| mandate + budget_line + constituency | 94.18 | 88.28 | 76.28 | 76.28 |
| embedding | 50.00 | 37.00 | 29.03 | 29.03 |
| mandate + embedding | 76.18 | 62.78 | 42.81 | 42.81 |
| budget_line + embedding | 75.20 | 61.25 | 41.69 | 41.69 |
| mandate + budget_line + embedding | 94.00 | 87.50 | 72.50 | 72.50 |
| constituency + embedding | 76.18 | 62.78 | 42.81 | 42.81 |
| mandate + constituency + embedding | 94.18 | 88.28 | 76.28 | 76.28 |
| budget_line + constituency + embedding | 94.00 | 87.50 | 72.50 | 72.50 |
| mandate + budget_line + constituency + embedding | 94.18 | 88.28 | 76.28 | 76.28 |

## 3. Do protections work as a menu or a package?

Pairwise relationships between protections for program survival (percentage points), from interaction effects averaged over the other two protections. Successors cut when their gain exceeds their cost, so protections act through thresholds: one protection may be useless alone but decisive together with another. That produces complementarity without any interaction being assumed.

| Scenario | Pair | Relationship | Interaction (points) |
|---|---|---|---:|
| Supportive politics | mandate + budget_line | substitute | -8.91 |
| Supportive politics | mandate + constituency | substitute | -14.70 |
| Supportive politics | mandate + embedding | substitute | -9.91 |
| Supportive politics | budget_line + constituency | substitute | -3.31 |
| Supportive politics | budget_line + embedding | complementary | 5.72 |
| Supportive politics | constituency + embedding | substitute | -4.31 |
| Contested politics | mandate + budget_line | substitute | -7.71 |
| Contested politics | mandate + constituency | substitute | -10.16 |
| Contested politics | mandate + embedding | substitute | -8.71 |
| Contested politics | budget_line + constituency | additive | -1.59 |
| Contested politics | budget_line + embedding | complementary | 8.18 |
| Contested politics | constituency + embedding | substitute | -2.59 |
| Polarized politics | mandate + budget_line | substitute | -2.36 |
| Polarized politics | mandate + constituency | complementary | 5.75 |
| Polarized politics | mandate + embedding | substitute | -2.50 |
| Polarized politics | budget_line + constituency | complementary | 1.95 |
| Polarized politics | budget_line + embedding | complementary | 10.45 |
| Polarized politics | constituency + embedding | additive | 1.81 |
| Polarized, unfinished insourcing | mandate + budget_line | substitute | -2.36 |
| Polarized, unfinished insourcing | mandate + constituency | complementary | 5.75 |
| Polarized, unfinished insourcing | mandate + embedding | substitute | -2.50 |
| Polarized, unfinished insourcing | budget_line + constituency | complementary | 1.95 |
| Polarized, unfinished insourcing | budget_line + embedding | complementary | 10.45 |
| Polarized, unfinished insourcing | constituency + embedding | additive | 1.81 |

## Caveats

- Protections, costs, and hostility levels are stylized. Real successors also face courts, unions, vendors, and the media.
- Successors are assumed to see the protections and the program's state (perfect information).
- 'Unfinished insourcing' adds a public loss when the program is cut, standing for work returning to vendors on worse terms; Model 1 Section 7 shows how long transitions take.

