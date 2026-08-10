# Mission 001 — Pauliverse Command World

## Status
APPROVED DIRECTION / EXECUTION MISSION

## Mission owner
Owner governs consequential choices. Hermes leads orchestration. Specialist agents execute bounded work and return proof.

## Goal
Build the most extended **working prototype** of the Pauliverse operating system that can be verified end to end:

- Hermes is the authoritative portfolio orchestrator.
- Every owned repository is treated as a typed node with provenance, status, dependencies, reusable capabilities, evidence, and disposition.
- Pauli Pi is a subordinate execution worker.
- Pauli's Place is the commercial/financial execution node and the owner's observation cockpit.
- YAPPYVERSE-FACTORY is the character/media production node.
- Where's Pauli remains the Pauli story/IP authority.
- Financial opportunities discovered anywhere route to Pauli's Place.
- Important decisions run through a bounded adversarial LLM council.
- All cross-node execution is observable from a hardened 3D dashboard at Pauli's Place.
- ICM keeps the system portable: an agent can move to another machine/runtime and re-orient from files and authoritative links without requiring one giant proprietary memory blob.

The prototype only counts as working when the owner can observe a real repo/agent/opportunity moving through the system and see evidence of the result.

## Current verified baseline — 2026-08-10

- Pauli's Place production deployment is live on Vercel and returns HTTP 200.
- Pauli's Place already exposes routes for Dashboard, Trends, Products, Approval Queue, Research Lab, Observation, and `Paulie's Place 3D` at `/lounge`.
- The `/lounge` metadata describes a Yappyverse 3D observable world with voice/Jarvis, avatars, and real-time agent scenes.
- No runtime errors were reported by Vercel for Pauli's Place in the inspected 24-hour window.
- The Hermes Vercel project currently fails during build because the deployment is detecting a root/package configuration that expects Next.js even though the Vercel project is configured as FastAPI. Fixing Hermes deployment/root configuration is therefore a release blocker for the cloud control path.

The mission upgrades the existing 3D Lounge rather than creating a competing dashboard.

## Gauntlet bar

**Primary comparison bar:** GitNexus Web UI graph exploration.

Why this bar:
- it exposes repositories as a navigable knowledge graph rather than a flat project list;
- it supports multi-repository reasoning and dependency/process relationships;
- it is directly comparable with the Pauliverse repo/node graph;
- it is fetchable and inspectable by independent critics.

**3D technical reference:** the `3d-force-graph` Three.js/WebGL large-graph interaction model. This is an implementation/interaction reference, not a second quality bar.

The Pauliverse prototype wins only when it is at least as understandable as the GitNexus graph for orientation **and** adds operational state GitNexus does not need to provide: live agents, missions, approvals, financial signals, deployment health, evidence, and human gates.

## Gauntlet directive

> Build the most extended working Pauliverse prototype: Hermes must orient across real repository nodes, delegate bounded execution, route financial opportunities to Pauli's Place, preserve ICM authority/provenance, and expose the whole system through the existing Pauli's Place 3D Lounge. The bar is the live GitNexus Web UI graph exploration experience. Inspect the real bar directly and compare against it, not a description. Break the prototype into the smallest independently judgeable slices. For every slice, use a separate builder and harsh critic with fresh context. The critic inspects the real output, compares it blind against the bar where comparable, and names the single biggest remaining gap. If ours loses, return it to the builder. Do not exit on round count; exit only when the slice wins its comparison and passes its functional acceptance tests. Keep a live evidence/progress record. Run builders and critics as parallel subagents where safe, but keep irreversible, financial, credential, legal, deletion, and public-claim actions human-gated.

## Round 0 critic verdict

**Current result: LOSES / not yet the working prototype.**

The existing Pauli's Place deployment proves there is already a useful shell and a 3D route. It does **not yet prove** from the inspected evidence that:

- the 3D world is driven by the master ontology;
- real repositories appear as live nodes;
- Hermes activity is streaming into the scene;
- missions can be drilled into from the world;
- approval gates are enforced server-side;
- financial signals visibly route into Pauli's Place;
- the council records dissent and evidence;
- deployment/runtime states are shown across nodes;
- the owner can trace a node from idea → task → execution → proof → money/impact result.

That is the gap this mission closes.

## System roles

### Owner / Governor
Owns:
- strategic pivots;
- financial commitments and money movement;
- signatures/contracts;
- legal/compliance decisions;
- major ethics/mission decisions;
- destructive deletion;
- major public brand/canon changes;
- final approval where a gate explicitly requires a human.

Should not be interrupted for reversible implementation details that agents can test safely.

### Hermes — Portfolio Orchestrator
Owns:
- portfolio orientation;
- repo census;
- authority resolution;
- master ontology/index;
- signal-vs-noise prioritization;
- bounded council invocation;
- delegation packets;
- cross-repo dependency reasoning;
- portfolio state transitions;
- routing financial opportunities to Pauli's Place;
- surfacing only decisions requiring the owner.

Hermes coordinates. It does not become every domain's canonical database.

### Pauli Pi — Execution Worker
Owns:
- bounded coding/tool/local-machine missions delegated by Hermes;
- target-repo implementation under that repo's local rules;
- tests and proof packets;
- returning discovered capabilities, risks, and financial signals to Hermes.

Pi does not own the portfolio ontology or financial control.

### Pauli's Place — Commercial Control Plane + Observation Cockpit
Owns:
- opportunity queue;
- offers/pricing/unit economics;
- revenue experiments;
- product/vendor/POD operations;
- approval queue for commercial actions;
- commercial results and financial learning;
- the 3D observation world for the owner.

It links to story/character/cause authorities instead of duplicating their truth.

### YAPPYVERSE-FACTORY — Character / Media Factory
Owns:
- character production;
- reusable creative/media pipelines;
- Yappyverse assets and production evidence;
- approved production output.

### Where's Pauli — Story/IP Laboratory
Owns:
- Pauli canon;
- episodes;
- story engines;
- puzzle/clue/story mechanics;
- approved IP facts.

Commercialization routes outward to Pauli's Place; commercial systems do not silently rewrite canon.

### LLM Council
For consequential decisions, Hermes fans out bounded roles:
- Operator
- CFO
- Consolidator
- Red Team
- Evidence Judge
- Mission Guardian
- Opportunity Advocate

Hermes synthesizes but preserves disagreement.

### Gauntlet Critic
Independent from the builder. Binary job: does the slice beat the named bar and pass functional acceptance tests? If not, identify the single biggest remaining gap.

## 3D observation model — Pauli's Place Command World

The current `/lounge` becomes the **Pauliverse Command World**.

### Spatial grammar

**Center:** Hermes control core.

**Primary districts/rings:**
1. Businesses / commercial nodes
2. Story + IP
3. Agents + capabilities
4. Infrastructure + deployments
5. Social-purpose nodes
6. Archive / consolidation candidates

Every GitHub repository is rendered as a node in the appropriate district. Non-repo nodes such as agents, deployments, opportunities, experiments, and causes can appear as satellites or linked objects rather than pretending everything is a repository.

### Edges
Edges represent real ontology relationships such as:
- `DEPENDS_ON`
- `REUSES`
- `DUPLICATES`
- `REPLACES`
- `MONETIZES`
- `ROUTES_TO`
- `DEPLOYED_AS`
- `CANONIZED_IN`
- `PROVEN_BY`
- `BENEFITS`

Active edges can animate only when there is a current event/mission; the scene must not animate every relationship continuously.

### Financial routing visualization
A credible financial signal moves visibly from its source node to Pauli's Place as an opportunity event. The event is not money movement. It is a routed commercial work item until an approved payment/transaction path exists.

### Node status
The scene should visually distinguish at minimum:
- ACTIVE
- TESTING
- BLOCKED
- NEEDS APPROVAL
- HEALTHY
- DEGRADED
- CONSOLIDATE CANDIDATE
- ARCHIVED

Do not encode critical status by color alone; use iconography/text/state chips in the detail panel for accessibility.

### Interaction rule
3D is for **orientation and monitoring**, not dense administration.

Click/select a node → open a 2D evidence drawer containing:
- node identity and authority;
- current disposition;
- repository/deployment link;
- health;
- active missions;
- dependencies;
- recent evidence;
- financial signals;
- owner approvals required;
- latest verified result;
- next action.

### Command world rooms
The prototype may represent functional zones as rooms/panels without requiring literal game navigation for every task:

- **Command Deck** — global health and priority missions
- **Council Chamber** — decisions, dissent, recommendations, evidence
- **Money Room** — opportunity/revenue experiment flow in Pauli's Place
- **Factory Floor** — Yappyverse/media production jobs
- **Story Room** — Where's Pauli/Yappyverse story production status, read-only from commercial systems
- **Impact Room** — social-purpose outcomes/beneficiary links, with entity boundaries preserved
- **Archive** — consolidate/archive/delete candidates and provenance

## Event model

A shared event envelope allows the dashboard to observe without coupling every repo directly to the frontend:

```json
{
  "event_id": "uuid",
  "occurred_at": "ISO-8601",
  "source_node": "repo-or-agent-id",
  "actor": "hermes|pi|specialist|human|system",
  "event_type": "mission.started|mission.completed|approval.requested|opportunity.routed|deployment.changed|node.health_changed|evidence.added|decision.recorded",
  "mission_id": "optional",
  "node_id": "optional",
  "severity": "info|warning|critical",
  "summary": "human readable",
  "evidence_refs": [],
  "correlation_id": "stable workflow id",
  "schema_version": 1
}
```

The dashboard consumes the event stream; it does not become the authoritative source for the underlying fact.

## Connection hardening requirements

### Authentication / authorization
- authenticated organization/workspace scope;
- default read-only observer access;
- server-side role checks for mutations;
- explicit actor identity in audit records;
- no browser-exposed service-role or infrastructure secrets.

### Approval hardening
For consequential actions, approval must be server-verified and bound to the exact task/actor/run, with expiry where appropriate. Caller-supplied booleans such as `approved=true` are not sufficient authority.

### Agent execution
- bounded mission scope;
- allowlisted tools/actions;
- explicit timeouts;
- retry limits and circuit breakers;
- idempotency keys for side effects;
- duplicate-event suppression;
- cancellation propagation;
- no silent privilege expansion.

### Event transport
- WebSocket/SSE where useful for live state;
- resilient polling fallback;
- reconnect with bounded exponential backoff;
- monotonically ordered/cursor-based event recovery where possible;
- deduplication by `event_id`/correlation ID;
- scene rebuild only when topology/roster changes, not on every telemetry tick.

### Financial controls
- Pauli's Place can track opportunities and proposed transactions automatically;
- actual money movement remains human-gated unless a future explicit policy delegates a narrow spend envelope;
- every commercial experiment records revenue, variable cost, fees, labor/support burden, refunds/returns where relevant, and resulting gross contribution;
- nonprofit/social-purpose claims must remain tied to actual approved entities/terms.

### Secrets
- secret references, not copied credentials;
- least privilege;
- rotation/revocation path;
- no secrets in prompts, logs, screenshots, git commits, or client payloads.

### Evidence
Every important state transition should have inspectable receipts:
- commit/PR;
- CI/test result;
- deployment result;
- API/event receipt;
- payment/order result when applicable;
- human approval receipt where required.

## Prototype slices

### Slice 0 — Authority correction
PASS when:
- real Hermes is authoritative;
- Pi is explicitly subordinate worker;
- duplicate authority is removed/demoted;
- Pauli's Place remains the financial node.

### Slice 1 — Hermes cloud/runtime recovery
PASS when:
- Hermes production build succeeds;
- health endpoint responds;
- correct Vercel root/framework configuration is verified;
- no fake Next.js detection remains on the Hermes service path.

### Slice 2 — Repo census + ontology seed
PASS when Hermes can ingest an initial batch of real repos and emit typed nodes/edges with provenance and dispositions without modifying those repos.

### Slice 3 — Delegation proof
PASS when Hermes delegates one bounded mission to Pi or another worker, worker returns a proof packet, and Hermes records the result.

### Slice 4 — Financial routing proof
PASS when a real opportunity from a source node is converted into the Pauli's Place handoff schema and appears in the Pauli's Place opportunity/approval flow.

Initial candidate: limited-edition Pauli puzzle / puzzle-book product experiment.

### Slice 5 — Command World data adapter
PASS when `/lounge` reads a real ontology snapshot/event stream rather than static/demo-only scene data.

### Slice 6 — 3D repo graph
PASS when real repo nodes and ontology edges render, can be selected, and show evidence/status in the 2D drawer.

### Slice 7 — Live mission telemetry
PASS when mission/approval/deployment/opportunity events update node state without a full scene rebuild.

### Slice 8 — Council Chamber
PASS when one consequential decision visibly contains independent council outputs, disagreements, evidence, recommendation, and owner gate status.

### Slice 9 — Hardened approvals + audit
PASS when unauthorized/caller-forged approval attempts fail, legitimate server-bound approvals succeed, and both are recorded.

### Slice 10 — Owner cold-walk test
PASS when the owner can open Pauli's Place and answer in under a few interactions:
- What is working?
- What is broken?
- What is making/trying to make money?
- What needs my approval?
- What is Hermes doing now?
- Which repos should be activated, consolidated, archived, or reviewed for deletion?
- What proof supports those claims?

## First observable end-to-end demonstration

The first demo should use one real commercial signal so the system proves business value rather than only telemetry:

```text
WHERE'S PAULI / YAPPYVERSE IP
    ↓ opportunity discovered
HERMES
    ↓ signal scoring + council
PAULI'S PLACE
    ↓ limited-edition puzzle experiment
OWNER APPROVAL (price/spend/public launch)
    ↓
WORKER/FABRICATION TASKS
    ↓
PROOF + DEPLOYMENT/PRODUCT RESULT
    ↓
PAULI'S PLACE COMMAND WORLD
    ↓
REVENUE/RESULT EVENT
    ↓
HERMES UPDATES ONTOLOGY + NEXT ACTION
```

This is the prototype's primary acceptance journey.

## Stop conditions
Stop and escalate rather than silently continuing if:
- a destructive consolidation/delete is required;
- money movement is required outside an approved spend envelope;
- a legal/public claim about social-purpose use is not verified;
- a credential must be exposed to proceed;
- two authorities claim the same canonical fact;
- the critic cannot inspect the real bar/output;
- an external dependency makes the end-to-end test non-reproducible and no safe substitute exists.

## Success definition
Mission 001 is complete only when the system is not merely documented:

1. Hermes is online and authoritative.
2. At least one real repo census exists.
3. At least one bounded delegation completes with proof.
4. At least one real financial opportunity routes into Pauli's Place.
5. The Pauli's Place 3D Lounge renders real portfolio nodes and live operational state.
6. The owner can inspect evidence and approvals from the dashboard.
7. Critical connections pass hardening tests.
8. Independent critic says the graph-orientation experience is at least competitive with the named bar for the comparable task.
9. All unresolved blockers are explicit rather than hidden behind simulated/demo data.
