# Hermes Multiplayer Bridge

## Purpose

This file defines the contract by which Hermes consumes the canonical multiplayer Business OS state from `executiveusa/YAPPYVERSE-FACTORY`.

Hermes is a **consumer/orchestrator** of this state. YAPPYVERSE remains the shared multiplayer control and context layer.

## Load order

Hermes should load multiplayer mode in this order:

1. `EMERALD_TABLETS.md`
2. `AGENTS.md`
3. `ICM/multiplayer/manifest.yaml`
4. `ICM/multiplayer/MULTIPLAYER_SYSTEM_PROMPT.md`
5. `ICM/multiplayer/TEAM_GRAPH.json`
6. the active client's state package conforming to `ICM/multiplayer/CLIENT_STATE_CONTRACT.md`
7. the relevant workflow only, such as `ICM/multiplayer/credit/CREDIT_WORKFLOW.md`

## Activation contract

When a user says any of the following, Hermes should enter multiplayer mode:

- `multiplayer mode`
- `run this through the team`
- `route this through YAPPYVERSE`
- `use the Business OS`
- `use the team graph`

Activation means:

```text
INPUT
  current user request + active client/team context

PROCESS
  load multiplayer manifest + prompt + team graph
  determine whether task is client-level, team-level, or system-level
  route work to the smallest qualified human/agent role
  preserve evidence state and authority boundaries

OUTPUT
  result + updated shared state + owner of next move

GATE
  PASS or BLOCK

RECEIPT
  sources read + roles invoked + actions taken + approvals used + files/artifacts changed
```

## Routing rules

Hermes should not default to doing every task itself.

Route according to the shared team graph:

- Background orchestration: strategy, routing, standards, cross-business learning
- Akash lane: My Web Lane / Akash Engine / India opportunities
- Stacy lane: Max Digital Media / nontechnical operator workflows
- Stavare lane: Posta Tees / merchandise / print-on-demand
- Tyshawn lane: AfroMation / art / anime / social-purpose creative work
- Yvette lane: Coopery Media / Mexico and LATAM opportunities
- Credit lane: governed business-credit readiness and approved financial workflows

## Shared-state rule

All multiplayer work should resolve into one shared state instead of isolated agent reports.

For each active business/client, Hermes should be able to answer:

- What do we know?
- What is client-stated?
- What are we inferring?
- What remains unknown?
- What is the current binding constraint?
- What experiment is active?
- Who owns the next move?
- What requires approval?

## Evidence states

Only these are valid:

- `VERIFIED`
- `CLIENT_STATED`
- `INFERRED`
- `UNKNOWN`

Do not upgrade `INFERRED` or `UNKNOWN` to `VERIFIED` without new evidence.

## Multiplayer Business OS rule

For client growth work, route through:

```text
public / authorized evidence
-> shared client brain
-> Business Operating Map
-> 8-dimension diagnosis
-> Revenue Capture leak map
-> one binding constraint
-> owner correction
-> one bounded proof sprint
-> independent verifier
-> PASS / BLOCK
-> learning written back to shared state
```

Do not default to ads, websites, CRM migrations, social media, SEO retainers, chatbots, or automations before diagnosis.

## Subagent rule

Hermes may dispatch subagents when work is parallelizable or specialist-heavy, but every packet must contain:

- target
- role
- authority
- required evidence
- expected output
- gate
- receipt requirements

The builder cannot verify itself.

## Credit workflow

When the task concerns business credit, Hermes must load:

`ICM/multiplayer/credit/CREDIT_WORKFLOW.md`

Browser/subagent work is allowed for research, readiness, monitoring, comparison, and preparing owner-reviewed materials.

The following remain human approval gates:

- credit application submission
- personal guarantee acceptance
- bank/credit-line opening
- financial commitment
- material representation to a lender/vendor
- identity-verification completion where the human is required

Never fabricate business facts, revenue, trade history, ownership, addresses, or application data.

## Background-orchestration boundary

The orchestration layer may be white-label or private. Privacy is not permission to deceive.

Do not impersonate team members, conceal relationships when disclosure is legally or contractually required, or misrepresent professional/regulated qualifications.

## YAPPYVERSE visual mapping

The BERD/YAPPYVERSE interface should eventually render:

```text
avatar/person/agent
-> active role
-> businesses/projects
-> authority
-> current task
-> blockers
-> receipts
-> shared memories
```

The visual layer must reflect canonical state; it must not become a second source of truth.

## Hermes implementation expectation

The thin Hermes adapter should do only three things:

1. fetch/load the multiplayer manifest and referenced files;
2. route work using the team graph and ICM rules;
3. write outcome/receipt state back to the shared client brain/Open Brain.

Do not duplicate the full multiplayer prompt or team graph inside Hermes if it can load the canonical source. This prevents prompt drift.
