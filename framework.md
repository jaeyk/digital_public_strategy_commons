# Framework: Building State Capacity for Digital Services and Infrastructure

Status: draft for review. This document fixes the concepts, strategies, and mechanisms before they are turned into models. Models in this repository should cite the section of this document they formalize, and should say what they leave out.

## 1. The question

How can governments build and keep the capacity to deliver effective and responsible digital public services and infrastructure?

Vendor capture is one important part of this question, but not all of it. A government can escape vendor lock-in and still fail. Rules may be too complex to implement, funding may come in one-off projects, no one may have authority to stop bad spending, or its systems may lose public trust. The framework therefore treats capture as one of several constraints.

### What success means

We judge strategies, and combinations of strategies, against three criteria. A strategy that does well on one but badly on another is not a complete answer.

| Criterion | Definition | Questions to ask of a strategy | Possible indicators |
|---|---|---|---|
| **Positive (outcome-oriented)** | Improves what people actually experience: services that work, reach the people entitled to them, are fair and safe, and give value for money | Does it change outcomes for users, or only inputs and processes? | Completion and take-up rates, time to receive a benefit, error and exclusion rates, cost per transaction, user satisfaction, complaints and appeals |
| **Durable** | Benefits survive political turnover, budget cuts, leadership departures, and changes of vendor | What happens to it after an election or the departure of its champion? Who would defend it? | Survival through changes of government, staff retention, stability of funding, whether it has a legal basis, whether services keep running through transitions |
| **Scalable** | Works across jurisdictions with different capacity (large national governments to small cities) and different motivation (committed reformers to reluctant adopters) | Does it need a large budget, rare talent, or a strong champion? Can a low-capacity or low-motivation jurisdiction still benefit? | Adoption by small or low-capacity jurisdictions, cost to adopt, adoption without dedicated champions, reuse of shared components |

Two points follow from these criteria:

- **Outcomes, not activity.** Building a team, publishing code, or holding a competitive tender are means. They count only to the extent they lead to better outcomes, either directly or through durability and scale. Adopting reforms in form without these effects is the "isomorphic mimicry" problem discussed in Section 5.
- **Scaling across motivation is different from scaling across capacity.** A small but committed city lacks resources. A large but reluctant agency lacks will. Strategies that help the first (shared platforms, consortia, pooled talent) may not help the second, which may need defaults, standards, conditions attached to funding, or regulation that make the good option the easy or required one.

### Tensions between the criteria

The three criteria can pull against each other:

- **Durability vs. adaptability.** Legal mandates and entrenched institutions protect good reforms, but they can also lock in bad designs. Protecting the capacity to improve is different from protecting one particular arrangement.
- **Outcomes vs. scale.** The most effective strategies often need rare talent and strong leaders (for example, an elite central digital team). These are hard to copy in thousands of smaller jurisdictions.
- **Speed vs. durability.** Reforms driven by a champion can move fast but often depend on that person. Building broad coalitions is slower but more likely to survive.
- **Central authority vs. local motivation.** Strong central controls can raise the floor for reluctant jurisdictions, but they can also produce resistance or box-ticking compliance.

## 2. What "state capacity" means here

Digital state capacity is the government's sustained ability to decide what to build, build or buy it well, operate and improve it over time, and remain accountable for it. We break it into six dimensions. A strategy can strengthen one dimension while leaving others untouched.

| Dimension | Question it answers | Signs it is weak |
|---|---|---|
| **Talent and skills** | Do public servants have the technical, product, design, and data skills to make and judge decisions? | Contractors write requirements and grade their own work; key staff leave |
| **Authority and governance** | Who can set standards, stop bad spending, and make decisions across agencies? | Every agency buys separately; no one can say no to a failing project |
| **Funding model** | Is money tied to ongoing services or to one-off projects? | Large capital projects, then neglect; no budget for maintenance |
| **Policy and process fit** | Can the rules be implemented as written? Are implementers allowed to make trade-offs? | Complex eligibility rules and compliance culture drive cost and failure |
| **Infrastructure and reuse** | Are there shared components (identity, payments, data exchange) and standards that services can build on? | Every service rebuilds the same functions; data cannot move between systems |
| **Legitimacy and accountability** | Do the public and oversight bodies trust the services, and can people get redress when things go wrong? | Opaque algorithms, exclusion of some users, no appeal route |

A seventh concern applies to all six: **durability**. Capacity decays when staff leave, leadership changes, or funding is cut. A strategy that builds capacity quickly but cannot survive a change of government may be worth less than a slower, more durable one.

## 3. Four constraints strategies respond to, and a shock

Strategies differ mainly in which constraint they are trying to relax.

1. **Market power.** The government depends on a small number of vendors who control the systems, the data, or the knowledge needed to change them.
2. **Internal rules and processes.** Policy complexity, procurement and hiring rules, budget structure, and oversight culture make good delivery hard, whoever does the work.
3. **Fragmentation.** Agencies and levels of government each build, buy, and staff separately, so they cannot share costs or learning.
4. **Legitimacy.** Services must be fair, safe, accessible, and accountable. If they are not, political support for digital investment is lost.

### A shock that cuts both ways: AI

AI is not a strategy, but it changes the context every strategy works in. It can push a government in two opposite directions, and which way it goes depends on how AI is built or procured.

- **The dependency path.** AI arrives as large, fast, bundled contracts with a few vendors that control the models, data pipelines, and integration. Procurement gets faster and larger, which deepens dependency: lock-in rises, the market concentrates, and the government loses the ability to inspect, change, or replace what it relies on. Services may improve in the short run, but the state becomes less able to steer them.
- **The capacity path.** The government has the talent, open interfaces, shared platforms, and in-house delivery to absorb AI itself. AI then raises the productivity of public staff, widens what an in-house team can realistically run, and lets small jurisdictions do more with shared tools. The state becomes more efficient and more scalable.
- **What decides the path.** The capacity the government already has when the shock arrives (talent, portability, shared infrastructure, insourced delivery), whether AI contracts are unbundled and competed (strategic and modular procurement), and whether safeguards contain the risk of errors and opaque automated decisions that erode trust.

The same shock can therefore widen or narrow the gap between strong and weak jurisdictions. It also raises the cost of waiting: capacity built before the shock decides who captures its benefits.

## 4. Strategy taxonomy

Each strategy is described by its mechanism, the capacity dimensions it mainly affects, the constraint it targets, and well-known examples. Examples illustrate the idea and do not show that it works.

### A. Building in-house capability

| Strategy | Mechanism | Dimensions | Constraint | Examples |
|---|---|---|---|---|
| A1. Central or agency digital service team | Skilled staff build, buy, and oversee services directly | Talent | Market power, internal rules | UK GDS, US Digital Service, 18F (closed 2025), Canadian Digital Service |
| A2. Talent pipelines and fellowships | Bring outside technologists into government for fixed terms | Talent | Market power | Presidential Innovation Fellows, TechCongress, Code for America fellowships |
| A3. Hiring and pay reform | Change hiring rules so government can recruit and keep technical staff | Talent, durability | Internal rules | Subject-matter-expert hiring assessments (US), digital job families |
| A4. Upskilling existing staff | Train the current workforce in digital, product, and data skills | Talent, durability | Internal rules | Digital academies and civil-service schools |
| A5. Product operating model | Organize around product ownership, user research, and iterative delivery, not projects and specifications | Talent, policy fit | Internal rules | Government service manuals and digital service playbooks |
| A6. Insourcing delivery at scale | Grow in-house engineering and operations staff to build and run work that vendors do now | Talent, infrastructure | Market power | In-house builds of central platforms, such as GOV.UK by the UK Government Digital Service |

### B. Governance and authority

| Strategy | Mechanism | Dimensions | Constraint | Examples |
|---|---|---|---|---|
| B1. Spend controls | A central body approves or blocks technology spending above a threshold | Authority | Fragmentation, market power | UK GDS spend controls |
| B2. Service standards and assessments | Services must meet a published standard before launch | Authority, legitimacy | Internal rules | UK Service Standard, Australia Digital Service Standard |
| B3. Legal mandates | Put digital duties and institutions into law so they survive leadership changes | Authority, durability | Internal rules | US 21st Century IDEA Act, Estonia's once-only principle |
| B4. CIO / CDO authority | Give technology leaders real budget and decision rights | Authority | Fragmentation | US FITARA |

### C. Funding

| Strategy | Mechanism | Dimensions | Constraint | Examples |
|---|---|---|---|---|
| C1. Product (continuous) funding | Fund teams and services every year, not one-off projects | Funding, durability | Internal rules | Agile funding pilots |
| C2. Revolving or central modernization funds | Central fund lends or grants for modernization, often with conditions | Funding, authority | Internal rules, fragmentation | US Technology Modernization Fund |

### D. Policy and process reform

| Strategy | Mechanism | Dimensions | Constraint | Examples |
|---|---|---|---|---|
| D1. Simplifying policy for delivery | Reduce rule complexity; involve implementers when policy is written | Policy fit | Internal rules | Argument in Pahlka, *Recoding America* (2023) |
| D2. Reducing procedural burden | Reform oversight, compliance, and approval processes that discourage sensible risk | Policy fit | Internal rules | Paperwork and authority-to-operate reform |

### E. Procurement and market shaping

| Strategy | Mechanism | Dimensions | Constraint | Examples |
|---|---|---|---|---|
| E1. Strategic procurement | Use contract awards and renewals to gain leverage | Talent (needs it), authority | Market power | Competitive re-bids, performance terms |
| E2. Modular contracting | Split large contracts into smaller, replaceable pieces | Infrastructure | Market power | Modular procurement guidance |
| E3. Digital marketplaces and agile vehicles | Make it easy for smaller suppliers to sell to government | — | Market power, fragmentation | UK Digital Marketplace / G-Cloud |
| E4. Challenge-based procurement | Buy solutions to stated problems instead of specifications | — | Market power | SBIR-style programs, GovTech challenge funds |
| E5. Contract data and IP rights | Require government ownership of data, documentation, and interfaces | Infrastructure | Market power | Data-rights and open-API clauses |
| E6. Cooperative purchasing | Several governments buy together | — | Fragmentation | Joint purchasing agreements |
| E7. Open contracting | Publish procurement data so it can be scrutinized | Legitimacy | Market power, legitimacy | Open Contracting Data Standard |
| E8. Startup and new-entrant pipeline | Lower barriers to entry for new vendors | — | Market power | GovTech accelerators |
| E9. Mission-aligned vendors | Favor or help create vendors whose ownership or charter ties them to public benefit | — | Market power, legitimacy | Public benefit corporations, steward ownership |

### F. Open and shared infrastructure

| Strategy | Mechanism | Dimensions | Constraint | Examples |
|---|---|---|---|---|
| F1. Open source by default | Release and reuse public code | Infrastructure | Market power | "Public Money, Public Code" |
| F2. Funding open source maintenance | Pay for upkeep of code that public services depend on | Infrastructure, durability | Market power | Germany's Sovereign Tech Agency, government OSPOs |
| F3. Open standards and APIs | Require interoperable interfaces so components can be replaced | Infrastructure | Market power, fragmentation | Open standards policies |
| F4. Shared platforms / DPI building blocks | Build common identity, payment, notification, and data-exchange components once | Infrastructure | Fragmentation | X-Road, India Stack, MOSIP, Login.gov, GOV.UK Notify, GovStack |
| F5. Digital public goods | Adopt or contribute to openly licensed software that other countries share | Infrastructure | Market power, fragmentation | Digital Public Goods Alliance |

### G. Public provision

| Strategy | Mechanism | Dimensions | Constraint | Examples |
|---|---|---|---|---|
| G1. Public option | Government builds and runs a service itself, alongside or instead of private offerings | Talent, infrastructure | Market power | IRS Direct File (ended 2025) |
| G2. Public or sovereign compute and cloud | Publicly owned or controlled computing infrastructure | Infrastructure | Market power | NAIRR, CalCompute, EU sovereign cloud initiatives |

### H. Regulation

| Strategy | Mechanism | Dimensions | Constraint | Examples |
|---|---|---|---|---|
| H1. Interoperability and portability mandates | Legally require vendors to support data export and interoperability | Infrastructure | Market power | EU Digital Markets Act |
| H2. Competition enforcement | Use antitrust law against anti-competitive conduct in the government market | — | Market power | Antitrust action |

### I. Collaboration

| Strategy | Mechanism | Dimensions | Constraint | Examples |
|---|---|---|---|---|
| I1. Jointly owned infrastructure between governments | Several governments co-own and govern shared systems | Infrastructure, durability | Fragmentation | Nordic Institute for Interoperability Solutions (X-Road) |
| I2. Shared code and consortia among subnational governments | States or cities pool development of common systems | Talent, infrastructure | Fragmentation | Multi-state system consortia |
| I3. Peer networks | Governments share practice and staff learning | Talent | Fragmentation | Digital Nations |
| I4. Civil society and civic tech | Volunteers, NGOs, and participatory processes add capacity and legitimacy | Talent, legitimacy | Legitimacy | g0v and vTaiwan (Taiwan); Code for America brigades (ended 2023) |

### J. Accountability and safeguards

| Strategy | Mechanism | Dimensions | Constraint | Examples |
|---|---|---|---|---|
| J1. Algorithm and system registers | Publish what automated systems are used and how | Legitimacy | Legitimacy | Amsterdam and Helsinki algorithm registers |
| J2. Impact assessments and audits | Assess risks to rights, privacy, and fairness before and during use | Legitimacy | Legitimacy | Algorithmic impact assessments |
| J3. Accessibility, inclusion, and redress | Ensure everyone can use services and can appeal decisions | Legitimacy | Legitimacy | Accessibility law, non-digital fallback channels |

### In-house capacity: scope, scale, and pace

An in-house team is not a single choice. Building one raises three questions that the strategies above do not answer by themselves.

1. **Scope: could the team cover everything vendors do?** Probably not, and it may not need to. Vendor work ranges from commodity services (hosting, standard software) to specialized products and peak-load or specialist work that is costly to staff permanently. The realistic question is which part of the work the government should own and run, which part it should buy, and whether it can still switch suppliers for the part it buys. Possible roles for in-house staff run along a spectrum:
   - **Informed buyer:** a small team that writes requirements, oversees vendors, and holds them to account (mainly A1, E1).
   - **Product owner:** in-house product leadership with vendors doing much of the building (A1, A5).
   - **Builder and operator:** in-house staff build and run core services (A6).
   Smaller jurisdictions face a lower ceiling on scope. Pooling staff with other governments (I2) and using shared platforms (F4) can raise it.
2. **Scale: can the team grow large enough?** Growth is limited by hiring rules and speed, pay compared with the private sector, the local labor market, attrition, and budgets. Salaries are a recurring operating cost, while vendor contracts are often funded differently, so moving work in-house can be harder to fund even when it is cheaper overall. During a transition the government pays for staff before work has moved, so it pays twice for a while.
3. **Pace: can it happen fast enough?** Hiring, building, and migrating off legacy systems take years. A transition that moves work faster than experienced staff can manage risks service disruption. Multi-year transitions also have to survive changes of government; if a successor cuts the program, work goes back to vendors, often on worse terms.

These questions interact with the success criteria. Scope and scale bear on whether insourcing is **scalable**, pace and exposure to turnover bear on whether it is **durable**, and transition risk bears on whether it is **positive** in the short run. They also interact with AI (Section 3): AI may raise how much work each staff member can carry, but only if the government absorbs it rather than buying it as a bundled service.

## 5. Menu or package?

A central question for this project is whether these strategies work as a **menu**, where a government can pick any subset and each adds its own value, or as a **package**, where some only work, or work much better, together. The answer matters for advice. If strategies form a menu, a government can start with whatever is cheapest or most politically feasible. If they form a package, adopting only part of it may waste money, or look like reform without delivering any. Andrews, Pritchett, and Woolcock (2017) call the second case "isomorphic mimicry."

### Types of relationship

"Package" covers several different relationships, which call for different advice.

| Relationship | Meaning | Implication for advice |
|---|---|---|
| **Additive (menu)** | Value of A + B = value of A + value of B | Pick by cost and feasibility; order does not matter |
| **Complementary** | Each strategy raises the return to the other (A + B > A + B separately) | Adopt together; partial adoption gives up part of the value |
| **Prerequisite** | B has little or no effect unless A is in place | Sequence: A first |
| **Substitute** | Both address the same gap, so the second adds less (A + B < A + B separately) | Choose one; doing both is partly wasted |
| **Conflict** | One undermines the other | Avoid combining, or redesign one |
| **Binding constraint** | Nothing works until one specific constraint is relaxed | Diagnose the binding constraint first (Hausmann, Rodrik, and Velasco, 2008) |
| **Order-dependent** | The same set works in one order but not another | Plan the sequence, not just the set |

These relationships can also depend on context. Two strategies may be complements for a large national government and substitutes for a small city.

The menu-or-package question should be asked separately for each success criterion. Two strategies may add up for **outcomes** but be complementary for **durability**. For example, a digital team and a legal mandate each improve services on their own, but together they make each other last. Two strategies may also be complementary in a high-capacity jurisdiction yet impossible to combine in a low-capacity one, which matters for **scalability**.

### Hypothesized relationships

These are hypotheses to check against practitioner input and evidence before any model encodes them. Each is tagged with its proposed type.

| Strategies | Proposed type | Reasoning |
|---|---|---|
| In-house talent (A1–A4) → strategic procurement, modular contracting, contract rights (E1, E2, E5) | Prerequisite | Without skilled staff, government cannot write good requirements or oversee vendors |
| Open source (F1) + maintenance funding (F2) | Complementary or prerequisite | Released code that nobody maintains gives little real portability |
| Open source (F1) + data rights (E5) + open APIs (F3) | Complementary | Open code alone does not make data or interfaces portable |
| Digital team (A1) + legal mandate (B3) + continuous funding (C1) | Complementary (durability) | Teams without a mandate or stable funding can be shut down |
| Policy simplification (D1) → any delivery strategy | Binding constraint | Technical capacity cannot fix rules that cannot be implemented |
| Shared platforms (F4) + central authority (B) + funding (C) | Complementary | Without an owner and funding, agencies will not adopt shared components |
| Startup pipeline (E8) + portability (E5, F3) | Complementary | Without portability, a new entrant can become the next incumbent |
| Startup pipeline (E8) vs. public option (G1) | Possible conflict | Public provision may reduce the market new vendors need |
| Digital team (A1) vs. fellowships (A2) | Possible substitute or prerequisite | Both add talent; fellows may also need a permanent team to work within |
| Spend controls (B1) vs. agency autonomy for product teams (A5) | Possible conflict | Central approval can slow iterative delivery |
| Cooperative purchasing (E6) vs. modular contracting (E2) | Possible conflict | Large joint contracts can work against splitting work into small pieces |
| Digital team (A1) → insourcing at scale (A6) | Prerequisite | Moving work in-house needs experienced staff to plan and manage migration; without them the transition disrupts services |
| Hiring reform (A3) + insourcing at scale (A6) | Complementary | Hiring rules and pay limit how fast in-house capacity can grow |
| Insourcing at scale (A6) + pooled teams and shared platforms (I2, F4) | Complementary (scope) | Pooling lets small jurisdictions run more than they could alone |
| Insourcing at scale (A6) + strategic procurement (E1) | Complementary or substitute | A credible in-house alternative strengthens bargaining; but less vendor work leaves less to manage |
| Insourcing at scale (A6) vs. political turnover | Durability risk | Multi-year transitions can be cut halfway, sending work back to vendors |
| Existing capacity (A, F3, F4, A6) × AI shock | Moderator | Capacity in place when AI arrives decides whether AI strengthens the state or deepens vendor dependency |
| Strategic and modular procurement (E1, E2) × AI shock | Moderator | Unbundled, competed AI contracts limit the dependency that large, fast AI procurement creates |
| Safeguards (J) × AI shock | Moderator | Registers, impact assessments, and redress limit the loss of trust from AI errors |

### How to tell the difference

- **Patterns of joint adoption are not evidence of complementarity.** Governments that adopt several strategies together may simply have more money or stronger leadership. Athey and Stern (1998) set out how to test for complementarity without confusing it with this kind of selection.
- **Evidence that can help:** cases where only part of a package was adopted, or where strategies were adopted in different orders; strategies that were reversed; and practitioner accounts of what failed and why.
- **In models, complementarity is an assumption, not a finding.** A simulation shows interaction effects only if its equations contain them. A model of this question should state each assumed relationship from the table above in its code, cite it, and test how sensitive the conclusions are to it, including the menu (fully additive) case as a baseline.
- **Look beyond pairs.** Some packages may only work as a group of three or more (for example A1 + B3 + C1). Pairwise interaction tests will miss these.

## 6. Scope decisions to settle

1. **Jurisdiction.** Is the main focus national governments, US federal and state governments, or comparative across countries? Strategies such as spend controls and public options differ a lot across systems.
2. **Unit of analysis.** A single agency, a whole government, or a network of governments?
3. **Which constraints to model first.** The existing simulation covers market power only.
4. **Indicators and weights.** The three success criteria are set (Section 1). Still open: which indicators measure each one, and whether the criteria are combined into one score or kept separate so trade-offs stay visible.
5. **Typology of jurisdictions.** To test scalability, which types of jurisdiction should be distinguished (for example, high or low capacity crossed with high or low motivation)?
6. **Evidence base.** Which case studies, procurement data, or practitioner interviews will be used to check the relationships in Section 5 and set parameters?
7. **Menu or package claims.** Which relationships in Section 5 are central enough that the project should test them first?
8. **In-house role.** Which role along the informed buyer, product owner, and builder spectrum should be the default for each jurisdiction type, and what share of vendor work is realistic to insource?
9. **AI scenario.** When the AI shock is assumed to arrive, how strong it is, and which evidence can show whether AI procurement is following the dependency path or the capacity path.

## 7. Key sources

References use APA (7th edition) style. Each was checked against publisher, library, or index records (NBER, RePEc, OUP, MIT Press, Princeton University Press), and each DOI was confirmed to resolve at doi.org.

- Andrews, M., Pritchett, L., & Woolcock, M. (2017). *Building state capability: Evidence, analysis, action*. Oxford University Press. https://doi.org/10.1093/acprof:oso/9780198747482.001.0001 (Open access, CC BY-NC-ND 4.0.)
- Athey, S., & Stern, S. (1998). *An empirical framework for testing theories about complimentarity [sic] in organizational design* (NBER Working Paper No. 6600). National Bureau of Economic Research. https://doi.org/10.3386/w6600
- Besley, T., & Persson, T. (2011). *Pillars of prosperity: The political economics of development clusters*. Princeton University Press. ISBN 978-0-691-15268-4.
- Dunleavy, P., Margetts, H., Bastow, S., & Tinkler, J. (2006). *Digital era governance: IT corporations, the state, and e-government*. Oxford University Press. ISBN 0-19-929619-7.
- Greenway, A., Terrett, B., Bracken, M., & Loosemore, T. (2018). *Digital transformation at scale: Why the strategy is delivery*. London Publishing Partnership. (Second edition published 2021.)
- Hausmann, R., Rodrik, D., & Velasco, A. (2008). Growth diagnostics. In N. Serra & J. E. Stiglitz (Eds.), *The Washington Consensus reconsidered: Towards a new global governance* (pp. 324–355). Oxford University Press. (First circulated as a 2005 working paper.)
- Kattel, R., & Mazzucato, M. (2018). Mission-oriented innovation policy and dynamic capabilities in the public sector. *Industrial and Corporate Change, 27*(5), 787–801. https://doi.org/10.1093/icc/dty032
- Milgrom, P., & Roberts, J. (1995). Complementarities and fit: Strategy, structure, and organizational change in manufacturing. *Journal of Accounting and Economics, 19*(2–3), 179–208. https://doi.org/10.1016/0165-4101(94)00382-F
- O'Reilly, T. (2011). Government as a platform. *Innovations: Technology, Governance, Globalization, 6*(1), 13–40. https://doi.org/10.1162/INOV_a_00056 (An earlier version appeared in D. Lathrop & L. Ruma (Eds.), *Open government: Collaboration, transparency, and participation in practice*, O'Reilly Media, 2010.)
- Pahlka, J. (2023). *Recoding America: Why government is failing in the digital age and how we can do better*. Metropolitan Books. ISBN 978-1-250-26677-4.
- Pope, R. (2024). *Platformland: An anatomy of next-generation public services*. London Publishing Partnership. ISBN 978-1-916749-11-5.
