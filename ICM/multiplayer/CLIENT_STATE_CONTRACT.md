# Multiplayer Client State Contract

Every client or internal business gets one canonical shared state package. Humans and agents may have different views, but there is one source of truth.

## Required state

```yaml
client_id: ""
identity: {}
locations: []
offers: []
customer_segments: []
revenue_paths: []
customer_journeys: []
systems: []
channels: []
seo_local_evidence: {}
reviews_reputation: {}
verified_facts: []
client_stated_facts: []
inferences: []
unknowns: []
owner_questions: []
economics: {}
capacity: {}
revenue_leaks: []
primary_constraint: null
candidate_proof_sprints: []
experiments: []
approvals: []
results: []
evidence: []
decisions: []
ownership: {}
next_action: null
```

## Finding contract

Every material finding should carry:

```yaml
claim: ""
evidence_status: VERIFIED | CLIENT_STATED | INFERRED | UNKNOWN
confidence: 0.0
source: ""
retrieved_at: ""
evidence_for: []
evidence_against: []
business_implication: ""
next_uncertainty_reducing_action: ""
```

## Handoff contract

Before assigning work to another person or agent, provide only what they need:

```yaml
mission: ""
client_id: ""
role: ""
inputs: []
known: []
unknowns: []
authority: []
prohibited_actions: []
required_outputs: []
gate: PASS | BLOCK
```

## Multiplayer rule

No agent creates a private parallel version of client truth when a shared state package exists. New evidence is appended with provenance. Contradictions are preserved until resolved; they are not silently overwritten.

## Owner-question budget

Default maximum first-call budget: 6 questions after outside reconnaissance.

Questions must be prioritized by how much they can change:
- diagnosis,
- economics,
- capacity,
- authority,
- proof-sprint selection.

## Proof sprint contract

```yaml
hypothesis: ""
baseline: {}
intervention: ""
primary_metric: ""
secondary_metrics: []
start_state: ""
end_state: ""
blast_radius: ""
rollback: ""
approvals_required: []
receipt: ""
result: null
```

The client-facing presentation is a projection of this state, not a separate truth source.