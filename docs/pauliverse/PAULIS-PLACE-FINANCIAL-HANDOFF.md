# Pauli's Place Financial Handoff

## Status
LOCKED ROUTING CONTRACT

## Purpose
This document defines the boundary between creative/product nodes in the Pauliverse and the commercial execution node, **Pauli's Place**.

Whenever a repository, agent, conversation, experiment, character, story, capability, or asset produces a credible financial opportunity, the opportunity is handed to Pauli's Place rather than being built ad hoc inside the source repository.

## Source repo responsibility
The source node owns:
- the originating idea, asset, canon, capability, or user evidence;
- provenance;
- domain-specific constraints;
- links to the approved source material;
- any non-commercial work required to make the asset truthful/usable.

The source node does not need to become a storefront, billing system, product catalog, or financial ledger.

## Pauli's Place responsibility
Pauli's Place owns:
- commercial thesis;
- offer design;
- customer definition;
- pricing tests;
- unit economics;
- vendor/POD economics;
- checkout/funnel decisions;
- sales experiments;
- commercial partnerships;
- revenue measurements;
- financial task queue;
- commercial learning;
- escalation of consequential money/legal actions to the owner.

## Required handoff object

```yaml
opportunity_id: ""
created_at: ""
source_repo: ""
source_ref: ""
originating_agent: ""
category: product|service|licensing|sponsorship|fundraising-product|partnership|subscription|marketplace|other
customer: ""
problem_or_desire: ""
offer_hypothesis: ""
asset_or_ip: []
evidence: []
assumptions: []
time_to_first_cash: ""
expected_price: ""
estimated_variable_cost: ""
estimated_gross_margin: ""
startup_cost: ""
maintenance_burden: low|medium|high
strategic_fit: low|medium|high
reusable_ip: low|medium|high
black_swan_upside: low|medium|high
social_purpose_connection: ""
entity_separation_notes: ""
recommended_smallest_test: ""
owner_gate: ""
status: PROPOSED
```

## Decision filter
Pauli's Place evaluates opportunities in this order:

1. Can somebody pay soon?
2. Is there evidence beyond enthusiasm?
3. Can an existing asset/repo do most of the work?
4. What is the smallest paid test?
5. What is the actual margin after fulfillment, platform, labor, support, and returns?
6. Can agents operate most of the recurring work?
7. Does it strengthen reusable IP or distribution?
8. Does the social-purpose connection remain truthful and entity-safe?
9. What would make us stop?
10. What must the owner approve?

## Default experiment statuses

```text
PROPOSED
→ SCREENED
→ OWNER_APPROVED
→ TESTING
→ PROVEN | FAILED | INCONCLUSIVE
→ SCALE | ITERATE | ARCHIVE
```

A failed experiment is useful evidence. Record it so Hermes does not repeat it without a materially different thesis.

## Current first commercial pattern
The initial Pauli proof-of-market pattern is interactive mystery/puzzle products that can be produced with low inventory exposure and tied back to approved story/IP assets. This is a proving pattern, not a permanent restriction on Pauli's Place.

Potential extensions may include printable/digital puzzle products, print-on-demand physical games, limited/numbered collectible editions, signed artist editions, authentication/digital-unlock cards, mystery kits, game-night formats, and later physical experiences. Each extension must still pass the financial filter and owner gates before execution.

## Non-negotiable boundary
Pauli's Place is where financial opportunities are evaluated and operated. It is not the canonical home for story truth, character canon, nonprofit records, or every portfolio fact. It links to those authorities.
