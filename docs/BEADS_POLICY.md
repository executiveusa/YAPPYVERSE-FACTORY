# YAPPYVERSE GLOBAL BEADS POLICY

## Policy

**No substantive Yappyverse work exists unless it has a Bead.**

Beads (`bd`) is the authoritative system for task state, dependencies, ownership, execution notes, acceptance criteria, receipts, and durable operating memory.

GitHub issues, pull requests, chat messages, markdown plans, kanban screenshots, and agent memory may summarize or reference work, but they do not replace the Bead graph.

## Mandatory lifecycle

Before work:

1. `bd prime`
2. `bd ready --json`
3. Find the existing bead or create one.
4. Ensure it contains MODE, OUTCOME, TARGET, CONSTRAINTS, PROOF, COMMERCIAL VALUE, and dependencies where relevant.
5. Claim it with `bd update <id> --claim`.

During work:

- Link dependencies with `bd dep add`.
- Record material decisions and blockers on the bead.
- Record paid-tool/API cost receipts on the bead.
- Record artifacts, commit/PR identifiers, test results, URLs, and verification evidence on the bead.
- If scope expands, create/link a new bead rather than silently expanding the current one.
- If a worker delegates a bounded slice, create/link a child bead or use an existing linked bead.

Before completion:

- Verify acceptance criteria independently where required.
- Attach or reference observable proof.
- Close the bead only after proof exists.
- Push Beads/Dolt state when a remote is configured: `bd dolt push`.

## Bootstrap exception

If Beads is not initialized, no production work may proceed. The only allowed operation is the bootstrap itself:

- install `bd` system-wide;
- run `bd init --quiet` in the repository;
- configure the active agent integration (`bd setup codex`, `bd setup claude`, etc.);
- seed the North Star and initial milestone beads;
- claim the active bootstrap/milestone bead;
- continue normal work.

Use `scripts/bootstrap_beads.sh` on Linux/macOS/WSL or `scripts/bootstrap_beads.ps1` on Windows.

## Global agent rule

Every Yappyverse orchestrator, subagent, coding agent, media operator, browser agent, scheduled worker, and deployment worker must receive an active Bead ID before it performs mutating work.

Recommended environment contract:

```text
BEAD_ID=<active-bead-id>
```

Commands that mutate canonical assets or production state should reject execution if the bead is absent or cannot be resolved with `bd show`.

## Parent/child structure

Use the graph rather than a flat backlog:

- **P0 North Star** — long-lived governing outcome.
- **Milestones** — measurable system capabilities or commercial outcomes.
- **Epics** — end-to-end workflows or product slices.
- **Tasks** — bounded executable work.
- **Verification beads** — independent review when risk/quality warrants it.
- **Incident beads** — failures, regressions, cost overruns, or production anomalies.

Dependencies must make the next safe work discoverable through `bd ready`.

## Cost receipts

Any paid external operation should record at minimum:

- provider;
- project/client;
- Bead ID;
- operation;
- estimated cost/credits before execution when available;
- actual cost/credit delta after execution when available;
- produced artifact or result;
- whether the result was useful/accepted.

## No hidden TODOs

Do not create markdown task lists as an alternate backlog. If a plan contains executable items, each actionable item must be represented in Beads or explicitly labeled as non-actionable reference material.

## Definition of done

A Bead is complete only when its declared proof is observable. "Implemented", "generated", "looks done", or an agent's self-report is not sufficient where independent verification is required.

## Why this is mandatory

Yappyverse's North Star requires the owner to supervise outcomes rather than route tasks. That is only possible if the work graph survives sessions, models, agents, branches, and machines. Beads provides that durable dependency-aware operating memory; ICM provides the contextual structure around it.
