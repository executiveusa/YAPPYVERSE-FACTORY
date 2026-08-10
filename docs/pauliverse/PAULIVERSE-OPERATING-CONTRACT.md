# Pauliverse Operating Contract

## Status
LOCKED SHARED OPERATING RULE

## Internal naming
`Pauliverse` is an internal systems term only. It describes the owner's connected portfolio of repositories, agents, intellectual property, commercial systems, and social-purpose work. It is not automatically a public-facing brand.

## Core model
The portfolio is one interpretable system with many independently useful nodes.

- **Where's Pauli** is the story/IP laboratory and canon source for the Pauli mystery.
- **YAPPYVERSE-FACTORY** is the character/media factory and shared creative production layer.
- **Pauli's Place** is the commercial opportunity and financial execution node.
- **Hermes** is the primary portfolio orchestrator: it inventories, orients, routes, tests, consolidates, and escalates decisions.
- **ICM** is the portable context architecture. Folder structure, explicit contracts, plain-text state, provenance, and human gates make the operating model movable across agents, machines, and repositories.
- **Social-purpose organizations/projects** remain operationally distinct beneficiaries or partners. Commercial activity may support them, but their records, obligations, and claims must not be blurred into the commercial entity.

## The repo-as-node rule
Every owned GitHub repository is a node in the larger ontology, not an isolated project.

A repository can represent:
- a business;
- a product;
- an experiment;
- a capability;
- a reusable skill;
- an IP asset;
- a deployment;
- a social-purpose project;
- a duplicate or superseded implementation.

Hermes must reason across nodes before creating new work.

## Portfolio triage outcomes
Each repo/node must eventually resolve to one of four owner-visible outcomes:

1. `ACTIVATE` — there is a credible path to users, revenue, impact, or strategic leverage now.
2. `CONSOLIDATE` — useful capability or IP belongs inside another authoritative node.
3. `ARCHIVE` — retain provenance/history, stop active investment.
4. `DELETE` — propose deletion only when value and provenance have been safely extracted and an explicit owner gate approves the irreversible action.

No repository is deleted merely because it is old, unfinished, or confusing.

## Financial routing law
Any financial opportunity or money-moving task discovered anywhere in the Pauliverse is routed to **Pauli's Place** for commercial evaluation and execution.

Financial opportunities include:
- products and offers;
- pricing;
- print-on-demand and merchandise;
- sales funnels and checkout;
- licensing;
- sponsorships;
- paid partnerships;
- fundraising products tied to approved causes;
- subscriptions;
- marketplaces;
- vendor economics;
- revenue experiments;
- monetizable IP;
- contract/deal opportunities;
- other credible paths to cash flow.

The source repo keeps the originating context and a link to the handoff. Pauli's Place owns the commercial experiment, unit economics, transaction path, results, and financial learning. Do not copy competing versions of the same opportunity record into multiple repos.

## Minimum financial handoff
A handoff to Pauli's Place should contain:

```yaml
opportunity_id: stable-id
source_repo: owner/repo
source_ref: path-or-issue
problem_or_demand: ""
customer: ""
offer: ""
revenue_path: ""
time_to_first_cash: ""
test_cost: ""
expected_margin: ""
evidence: []
unknowns: []
risks: []
reusable_assets: []
social_purpose_connection: ""
recommended_experiment: ""
owner_gate: ""
status: PROPOSED
```

## Signal vs noise filter
Hermes must not treat every idea or repository as equally important.

Before material investment, score the opportunity on:

1. **Time to cash** — how quickly can a real customer pay?
2. **Evidence strength** — what observed demand, user behavior, prior sales, working code, audience, or owned distribution supports it?
3. **Strategic fit** — does it reinforce Pauli/Yappyverse, existing capabilities, owned channels, or another high-value node?
4. **Reusable IP** — does the work create assets, data, skills, templates, media, or infrastructure that compound?
5. **Maintenance leverage** — can agents/automation operate it without creating a permanent human burden?
6. **Margin/capital efficiency** — how much cash and labor must be committed before proof?
7. **Black-swan upside** — is there meaningful asymmetric upside without making the base case depend on it?
8. **Mission compatibility** — can value be created without compromising the separation, integrity, or claims of social-purpose work?

High novelty with weak evidence is not automatically high signal.

## Adversarial decision pass
Important opportunities receive bounded independent perspectives before an owner gate. These are roles, not necessarily permanent autonomous agents.

- **Operator** — smallest path to a real-world test.
- **CFO** — unit economics, cash conversion, capital exposure.
- **Consolidator** — existing repos/capabilities that make new build unnecessary.
- **Red Team** — reasons the thesis fails; legal, operational, technical, market, or reputation failure modes.
- **Evidence Judge** — separates facts, assumptions, anecdotes, and unsupported narrative.
- **Mission Guardian** — checks social-purpose alignment and entity separation.
- **Opportunity Advocate** — strongest good-faith case for acting.

Hermes synthesizes disagreements. It does not hide minority objections. Consequential decisions remain human-gated.

## Experiment law
Do not answer uncertainty with more architecture when a cheap external test is possible.

Default sequence:

```text
INGEST
→ ORIENT
→ FIND EXISTING CAPABILITY
→ CLASSIFY NODE
→ SCORE SIGNAL
→ ADVERSARIAL PASS
→ DEFINE SMALLEST TEST
→ OWNER GATE
→ EXECUTE
→ MEASURE
→ RECORD LEARNING
→ ROUTE MONEY WORK TO PAULI'S PLACE
→ UPDATE ONTOLOGY
→ NEXT ACTION
```

A test should prefer observable external evidence: payment, signup, reply, booked call, completed workflow, usage, cost reduction, or verified impact.

## Master-brain ontology
The master brain is a knowledge graph over authoritative ICM files. The graph is derived; the files remain the inspectable source of truth.

### Core node types
- `REPOSITORY`
- `PROJECT`
- `BUSINESS`
- `CAPABILITY`
- `SKILL`
- `AGENT`
- `PERSON`
- `IDEA`
- `IP_ASSET`
- `CHARACTER`
- `STORY_CANON`
- `PRODUCT`
- `OPPORTUNITY`
- `EXPERIMENT`
- `DECISION`
- `EVIDENCE`
- `CUSTOMER`
- `PARTNER`
- `CAUSE`
- `DEPLOYMENT`

### Core edge types
- `OWNS`
- `BUILDS`
- `REUSES`
- `DEPENDS_ON`
- `DERIVED_FROM`
- `DUPLICATES`
- `REPLACES`
- `MONETIZES`
- `SUPPORTS`
- `BENEFITS`
- `PROVEN_BY`
- `CONTRADICTED_BY`
- `ROUTES_TO`
- `DEPLOYED_AS`
- `ARCHIVED_AS`
- `CANONIZED_IN`

## Thought ingestion rule
Owner thoughts, conversations, notes, memories, and second-brain material are valuable inputs, but they are not silently promoted to fact or canon.

Each ingested thought must preserve:
- source;
- date/time when available;
- project/repo associations;
- whether it is an idea, preference, decision, observation, claim, or locked rule;
- confidence/evidence where relevant;
- supersession links when the owner's thinking changes.

The system should merge context, not erase provenance.

## ICM portability rules
This operating model follows the ICM invariants:

- inventory before restructuring;
- one folder, one job;
- small root routers;
- explicit `CONTEXT.md` contracts;
- numbered folders where sequence matters;
- stable factory references separated from per-run products;
- one authoritative home per fact;
- plain Markdown/YAML/JSON as inspectable interfaces;
- outputs remain human-editable;
- irreversible actions require human approval;
- generated graph/index files are rebuilt from sources rather than hand-maintained.

## Repository onboarding contract
When Hermes encounters a repo for the first time:

1. Inventory without changing anything.
2. Identify the repo's real job, current runtime/deployment, active users, valuable assets, duplication, dependencies, and evidence of use.
3. Locate existing routing/context files before adding new ones.
4. Classify the node: `ACTIVATE`, `CONSOLIDATE`, `ARCHIVE`, or candidate `DELETE`.
5. Detect financial opportunities and route them to Pauli's Place.
6. Detect reusable capabilities and link them into the ontology.
7. Propose the smallest ICM correction needed to make the repo walkable by a cold agent.
8. Human gate before destructive migration or ownership changes.
9. Verify the resulting repo can be oriented from its root in at most a few reads.
10. Record the learning so the next visit does not rediscover the same facts.

## Authority and boundaries
- Story canon remains with its story authority; financial systems must not silently rewrite it.
- Pauli's Place may commercialize approved IP but does not become the canonical story bible.
- YAPPYVERSE-FACTORY may produce characters/media but does not become the financial ledger.
- Hermes coordinates; it does not become the authoritative home for every fact.
- The master ontology points to authoritative nodes instead of duplicating their payload.
- Human approval remains required for signing, moving money, deleting repositories/data, changing legal claims, or other irreversible/high-consequence actions.

## North-star outcome
The owner should be able to express an outcome in plain language while Hermes can:

1. orient to the relevant parts of the portfolio;
2. retrieve the right context without loading everything;
3. discover existing assets before proposing new work;
4. identify money/impact opportunities;
5. run adversarial reasoning and small experiments;
6. route execution to the correct node;
7. surface only the decisions that require a human;
8. record results back into the ontology;
9. leave the portfolio clearer than it found it.
