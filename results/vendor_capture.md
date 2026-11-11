# Model 2: vendor capture (OpenSpiel game)

OpenSpiel game `python_dpsc_vendor_capture`: the government commits to one of 128 portfolios of 7 market-facing levers (team, insourcing, procurement, portability, open_source, maintenance, entrants); the incumbent vendor sees it and chooses lock_in, adapt, lowball, acquire_entrants. Payoffs come from the shared capacity engine (16 years, 30 trials, seed 20261111). Government payoff is net value against the status quo with a lock-in vendor (outcome points minus 10 x extra spending as a share of budget). Vendor payoff is contract revenue, which rises with lock-in and quality, falls with competition, and shrinks when the vendor loses contracts at renewal to a government with leverage.

Vendor responses:

- **lock_in:** entrench, so lock-in grows; service quality slips slightly.
- **adapt:** invest in quality and openness; lock-in falls; lower risk of losing the contract at renewal.
- **lowball:** low prices and low lock-in early, then raise lock-in after the first renewal.
- **acquire_entrants:** buy up new competitors, unless portability makes switching easy.

## 1. Equilibrium by jurisdiction type

*Equilibrium* is the subgame-perfect equilibrium from backward induction over the OpenSpiel game tree. *If vendor assumed fixed* is the portfolio that is best when the vendor is assumed always to lock in (Model 1's assumption), and what the government actually gets once the vendor responds to it.

| Jurisdiction | Equilibrium portfolio | Vendor response | Government | Vendor | If vendor assumed fixed | Actual response | Government gets |
|---|---|---|---:|---:|---|---|---:|
| Well-resourced and committed | team + procurement + portability + entrants | adapt | 10.89 | 47.31 | team + insourcing + procurement + portability + entrants | adapt | 10.23 |
| Well-resourced and reluctant | status quo | acquire_entrants | -0.22 | 75.64 | team + insourcing + procurement | acquire_entrants | -0.28 |
| Small and committed | team + procurement + portability | adapt | 7.69 | 55.03 | status quo | acquire_entrants | -0.26 |
| Small and reluctant | status quo | acquire_entrants | -0.24 | 76.96 | status quo | acquire_entrants | -0.24 |

## 2. Value of commitment

Pure-strategy Nash equilibria of the simultaneous-move version (pyspiel.create_matrix_game), where the government cannot commit before the vendor acts. *Value of commitment* is the equilibrium government payoff above the best simultaneous-move equilibrium.

| Jurisdiction | Pure equilibria | Best for government | Vendor | Government | Value of commitment |
|---|---:|---|---|---:|---:|
| Well-resourced and committed | 1 | team + procurement + portability + entrants | adapt | 10.89 | 0.00 |
| Well-resourced and reluctant | 1 | status quo | acquire_entrants | -0.22 | 0.00 |
| Small and committed | 1 | status quo | acquire_entrants | -0.26 | 7.94 |
| Small and reluctant | 1 | status quo | acquire_entrants | -0.24 | 0.00 |

## 3. Which portfolios make the vendor adapt?

Number of the 128 portfolios that lead to each vendor response, and the smallest portfolios that lead the vendor to adapt.

| Jurisdiction | lock_in | adapt | lowball | acquire_entrants | Smallest portfolios inducing adapt |
|---|---:|---:|---:|---:|---|
| Well-resourced and committed | 52 | 20 | 17 | 39 | team + procurement + portability; team + procurement + portability + entrants; team + procurement + portability + open_source |
| Well-resourced and reluctant | 16 | 0 | 0 | 112 | none |
| Small and committed | 41 | 21 | 16 | 50 | team + procurement + portability; team + procurement + portability + entrants; team + procurement + portability + open_source |
| Small and reluctant | 15 | 0 | 0 | 113 | none |

## 4. Menu or package, once the vendor responds

Pairwise relationships among the market levers, averaged over the other five levers, when the vendor is held at lock-in versus when it responds strategically. Strategic response can create complementarity: a vendor may adapt only when the government holds several levers at once.

### Well-resourced and committed

| Pair | Vendor fixed at lock-in | Vendor responds |
|---|---|---|
| team + insourcing | prerequisite (insourcing needs team) (2.10) | prerequisite (insourcing needs team) (1.12) |
| team + procurement | complementary (0.36) | prerequisite (procurement needs team) (4.98) |
| team + portability | additive (-0.00) | prerequisite (portability needs team) (2.29) |
| team + open_source | additive (-0.00) | prerequisite (open_source needs team) (0.62) |
| team + maintenance | additive (-0.00) | prerequisite (maintenance needs team) (0.84) |
| insourcing + procurement | substitute (-0.20) | conflict (-1.33) |
| insourcing + portability | additive (-0.09) | substitute (-0.45) |
| insourcing + open_source | additive (-0.07) | substitute (-0.16) |
| insourcing + maintenance | additive (-0.03) | conflict (-0.15) |
| procurement + portability | additive (-0.03) | prerequisite (portability needs procurement) (2.90) |
| procurement + open_source | additive (-0.02) | prerequisite (open_source needs procurement) (1.09) |
| procurement + maintenance | additive (-0.01) | prerequisite (maintenance needs procurement) (0.90) |
| portability + open_source | additive (0.01) | conflict (-0.69) |
| portability + maintenance | additive (-0.03) | conflict (-0.96) |
| portability + entrants | prerequisite (portability needs entrants) (0.30) | complementary (0.28) |
| open_source + maintenance | additive (0.13) | joint (works only together) (1.05) |
| open_source + entrants | prerequisite (open_source needs entrants) (0.21) | additive (0.13) |

### Well-resourced and reluctant

| Pair | Vendor fixed at lock-in | Vendor responds |
|---|---|---|
| team + insourcing | joint (works only together) (0.40) | joint (works only together) (0.45) |

### Small and committed

| Pair | Vendor fixed at lock-in | Vendor responds |
|---|---|---|
| team + insourcing | joint (works only together) (1.49) | prerequisite (insourcing needs team) (1.16) |
| team + procurement | joint (works only together) (0.51) | joint (works only together) (6.14) |
| team + portability | additive (0.01) | prerequisite (portability needs team) (2.18) |
| team + open_source | additive (0.02) | prerequisite (open_source needs team) (0.84) |
| team + maintenance | additive (0.01) | prerequisite (maintenance needs team) (0.57) |
| insourcing + procurement | additive (-0.11) | conflict (-0.46) |
| insourcing + portability | additive (-0.05) | conflict (-0.59) |
| insourcing + maintenance | additive (-0.00) | conflict (-0.24) |
| procurement + portability | additive (-0.02) | prerequisite (portability needs procurement) (2.62) |
| procurement + open_source | additive (-0.01) | prerequisite (open_source needs procurement) (1.29) |
| procurement + maintenance | additive (0.01) | prerequisite (maintenance needs procurement) (0.81) |
| procurement + entrants | additive (-0.07) | conflict (-0.32) |
| portability + open_source | additive (0.02) | conflict (-0.88) |
| portability + maintenance | additive (-0.03) | conflict (-0.60) |
| portability + entrants | joint (works only together) (0.32) | prerequisite (entrants needs portability) (0.52) |
| open_source + maintenance | joint (works only together) (0.16) | joint (works only together) (0.96) |
| open_source + entrants | joint (works only together) (0.24) | additive (0.06) |
| maintenance + entrants | additive (0.09) | joint (works only together) (0.22) |

### Small and reluctant

| Pair | Vendor fixed at lock-in | Vendor responds |
|---|---|---|
| team + insourcing | joint (works only together) (0.28) | joint (works only together) (0.29) |

## 5. The AI shock and vendor power

The same game with an AI shock in year 4. Payoffs for both games are measured against the same no-AI status quo, so they can be compared directly. *Vendor at status quo* shows how much AI strengthens the incumbent when the government does nothing (the dependency path).

| Jurisdiction | Vendor at status quo, no AI | Vendor at status quo, AI | Equilibrium, no AI | Response | Government | Equilibrium, AI | Response | Government |
|---|---:|---:|---|---|---:|---|---|---:|
| Well-resourced and committed | 74.16 | 85.31 | team + procurement + portability + entrants | adapt | 10.89 | team + insourcing + procurement + portability + open_source + entrants | adapt | 12.81 |
| Well-resourced and reluctant | 75.64 | 86.48 | status quo | acquire_entrants | -0.22 | team + insourcing + procurement + portability | acquire_entrants | 0.68 |
| Small and committed | 75.22 | 86.39 | team + procurement + portability | adapt | 7.69 | team + procurement + portability | adapt | 8.52 |
| Small and reluctant | 76.96 | 87.73 | status quo | acquire_entrants | -0.24 | status quo | acquire_entrants | -0.30 |

Government payoff of each lever's best portfolio with and without the lever, under AI (equilibrium vendor response): how much the government loses in the AI era by giving up each lever.

| Jurisdiction | team | insourcing | procurement | portability | open_source | maintenance | entrants |
|---|---:|---:|---:|---:|---:|---:|---:|
| Well-resourced and committed | 3.33 | 1.10 | 6.22 | 0.76 | 0.11 | 0.00 | 0.28 |
| Well-resourced and reluctant | 0.65 | 0.82 | 0.00 | 0.33 | 0.00 | 0.00 | 0.00 |
| Small and committed | 2.10 | 0.00 | 7.02 | 0.11 | 0.00 | 0.00 | 0.00 |
| Small and reluctant | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |

## Caveats

- The vendor is a single incumbent with four stylized responses; real markets have several vendors, and responses can change over the contract.
- Payoffs are Monte Carlo averages from the shared engine, so the game inherits its assumptions.
- Ties in the equilibrium are broken toward the lowest action id (status quo for the government, lock-in for the vendor).
- Mixed-strategy equilibria of the simultaneous game are not computed (OpenSpiel's solvers for these need the optional nashpy or lrsnash packages).

