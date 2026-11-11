# Model 4: scalability through diffusion

Four populations of jurisdictions (one per type, weighted by assumed share of all jurisdictions: Well-resourced and committed 5%, Well-resourced and reluctant 10%, Small and committed 25%, Small and reluctant 60%) choose among five strategy packages. Shares evolve by Boltzmann Q-learning dynamics from `open_spiel.python.egt.dynamics` (temperature 2.0, 4000 steps of 0.02). Package values come from the shared engine with political turnover (16 years, 40 trials). A jurisdiction using a shared package alone gets 25% of its value; the rest depends on how available shared platforms are, through other jurisdictions' adoption or central provision. Switching costs rise with package size and fall with motivation. All numbers are illustrative assumptions.

Packages: **status_quo** = nothing; **informed_buyer** = team + procurement + portability; **shared_adopter** = policy + portability + platforms + collaboration; **builder** = team + insourcing + funding + policy; **pooled_builder** = team + insourcing + funding + policy + platforms + collaboration.

## Without the AI shock

### Package values by jurisdiction type (net value, before network effects)

| Jurisdiction | status_quo | informed_buyer | shared_adopter | builder | pooled_builder |
|---|---:|---:|---:|---:|---:|
| Well-resourced and committed | 0.00 | 1.94 | 8.33 | 5.81 | 14.70 |
| Well-resourced and reluctant | 0.00 | 0.26 | 4.76 | 0.65 | 5.68 |
| Small and committed | 0.00 | 0.40 | 6.29 | 1.65 | 9.61 |
| Small and reluctant | 0.00 | -1.58 | 2.89 | -2.28 | 2.17 |

### Adoption and value by intervention

Cells show reform adoption (share not on the status quo) early on and in the long run, and the most common package in the long run. *Platforms available* is the long-run availability of shared platforms. *Expected value* is the share-weighted realized package value (excluding grants and penalties), so it measures what jurisdictions get from the packages themselves. *Floor* is the lowest expected value across types.

| Intervention | Well-resourced and committed | Well-resourced and reluctant | Small and committed | Small and reluctant | Platforms available | Weighted expected value | Floor |
|---|---|---|---|---|---:|---:|---:|
| none | 51% -> 94% (pooled_builder) | 21% -> 47% (status_quo) | 37% -> 81% (pooled_builder) | 15% -> 29% (status_quo) | 32% | 1.08 | 0.12 |
| shared platforms provided | 89% -> 100% (pooled_builder) | 45% -> 88% (shared_adopter) | 71% -> 98% (pooled_builder) | 29% -> 68% (shared_adopter) | 100% | 4.29 | 1.64 |
| conditional funding | 65% -> 99% (pooled_builder) | 32% -> 76% (shared_adopter) | 51% -> 95% (pooled_builder) | 24% -> 57% (status_quo) | 55% | 2.04 | 0.51 |
| standards mandate | 65% -> 99% (pooled_builder) | 32% -> 76% (shared_adopter) | 51% -> 95% (pooled_builder) | 24% -> 57% (status_quo) | 55% | 2.04 | 0.51 |
| combined | 96% -> 100% (pooled_builder) | 71% -> 98% (shared_adopter) | 88% -> 100% (pooled_builder) | 55% -> 94% (shared_adopter) | 100% | 4.76 | 2.27 |

## With the AI shock in year 4

### Package values by jurisdiction type (net value, before network effects)

| Jurisdiction | status_quo | informed_buyer | shared_adopter | builder | pooled_builder |
|---|---:|---:|---:|---:|---:|
| Well-resourced and committed | 0.00 | 2.65 | 9.62 | 8.34 | 18.00 |
| Well-resourced and reluctant | 0.00 | 0.63 | 5.56 | 1.44 | 6.98 |
| Small and committed | 0.00 | 1.18 | 7.58 | 3.95 | 13.17 |
| Small and reluctant | 0.00 | -1.17 | 3.70 | -1.63 | 3.27 |

### Adoption and value by intervention

Cells show reform adoption (share not on the status quo) early on and in the long run, and the most common package in the long run. *Platforms available* is the long-run availability of shared platforms. *Expected value* is the share-weighted realized package value (excluding grants and penalties), so it measures what jurisdictions get from the packages themselves. *Floor* is the lowest expected value across types.

| Intervention | Well-resourced and committed | Well-resourced and reluctant | Small and committed | Small and reluctant | Platforms available | Weighted expected value | Floor |
|---|---|---|---|---|---:|---:|---:|
| none | 62% -> 98% (pooled_builder) | 23% -> 55% (status_quo) | 45% -> 91% (pooled_builder) | 17% -> 35% (status_quo) | 37% | 1.96 | 0.34 |
| shared platforms provided | 95% -> 100% (pooled_builder) | 52% -> 92% (pooled_builder) | 84% -> 100% (pooled_builder) | 35% -> 77% (shared_adopter) | 100% | 6.14 | 2.55 |
| conditional funding | 75% -> 100% (pooled_builder) | 35% -> 83% (shared_adopter) | 59% -> 99% (pooled_builder) | 26% -> 65% (shared_adopter) | 63% | 3.53 | 1.12 |
| standards mandate | 75% -> 100% (pooled_builder) | 35% -> 83% (shared_adopter) | 59% -> 99% (pooled_builder) | 26% -> 65% (shared_adopter) | 63% | 3.53 | 1.12 |
| combined | 98% -> 100% (pooled_builder) | 77% -> 99% (pooled_builder) | 94% -> 100% (pooled_builder) | 61% -> 96% (shared_adopter) | 100% | 6.57 | 3.20 |

## Caveats

- Jurisdictions learn from relative payoffs; real adoption also depends on politics, vendors, and peer networks not represented here.
- Population shares, switching costs, network gains, and intervention sizes are assumptions.
- Interventions are free to the jurisdictions in this model; their cost to the higher level of government is not counted.
- Conditional funding and a standards mandate give identical results here by construction: both widen the payoff gap between reform and the status quo by the same amount. In practice they differ in who pays and in whether compliance is real or only on paper, which this model does not capture.

