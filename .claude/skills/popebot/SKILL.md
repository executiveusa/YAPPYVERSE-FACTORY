---
name: popebot
description: >
  Agent Zero dispatch SOP for paulis-pope-bot (thepopebot) Docker job agents.
  Use when Agent Zero (Claude Code / GitHub Copilot) needs to dispatch
  background work to autonomous Docker job agents — tasks that require
  long-running execution, scheduled jobs, or parallel background processing.
  PopeBots execute jobs, create PRs, and notify. Agent Zero supervises and
  merges. PopeBots NEVER have git authority to push directly to main.
  Source: git@github.com:executiveusa/paulis-pope-bot.git
alwaysApply: false
---

# PopeBot Dispatch SOP

## Overview

**PopeBot** (thepopebot) is a Docker-based autonomous agent system where:
- The **Event Handler** receives job requests and creates `job/*` branches
- The **Docker Agent** (Pi coding agent) executes work in a container
- The agent commits results and opens a **PR** for review
- **Auto-merge** handles the PR if ALLOWED_PATHS passes
- **Notifications** arrive when done

**Agent Zero** (Claude Code / GitHub Copilot) is the ONLY entity authorized to:
1. Decide which tasks go to PopeBot vs. executing locally
2. Trigger PopeBot jobs via `/api/create-job`
3. Review and approve PopeBot PRs after AUTONOMOUS_CI_AGENT Phase 1
4. Merge PopeBot PRs to `main`

PopeBots are workers. Agent Zero is the orchestrator. This hierarchy is
non-negotiable.

## When to Dispatch to PopeBot

Use PopeBot for tasks that are:
- Long-running (> 10 min expected execution time)
- Fully specifiable upfront (clear inputs, clear done criteria)
- Safe to run in isolation (blast radius ≤ 3 services)
- Not requiring interactive back-and-forth with the user

Do NOT use PopeBot for:
- Tasks requiring real-time user input
- Architecture decisions (those stay with Agent Zero + SYNTHIA™)
- Multi-service deploys (require explicit multi-service deploy plan first)
- Any task touching `src/assets/pauli/**` or `*.lock` files

## Dispatch Protocol (SOP-006)

### Step 1 — Define the Job

Write a clear job spec:
```
TASK: <one-sentence description of what to do>
INPUTS: <files, URLs, data the agent needs>
DONE_WHEN: <verifiable completion criteria>
AFFECTED_PATHS: <list of files/dirs the agent may modify>
BLAST_RADIUS: <number of services affected — must be ≤ 3>
```

### Step 2 — Verify Blast Radius

If BLAST_RADIUS > 3: **STOP**. Write an explicit multi-service deploy plan first.
Have Agent Zero execute it manually rather than dispatching to PopeBot.

### Step 3 — Dispatch via API

```bash
curl -X POST <APP_URL>/api/create-job \
  -H "x-api-key: <POPEBOT_API_KEY>" \
  -H "Content-Type: application/json" \
  -d '{
    "task": "<task description>",
    "context": "<additional context>",
    "allowedPaths": ["<path1>", "<path2>"]
  }'
```

The Event Handler will:
1. Create branch `job/<task-slug>`
2. Trigger GitHub Actions run-job.yml
3. Spin up Docker container with Pi agent
4. Agent executes, commits, opens PR

### Step 4 — Monitor the Job

Poll for the PR created on `job/*` branch:
```
GET /repos/executiveusa/YAPPYVERSE-FACTORY/pulls?state=open&head=executiveusa:job/
```

Expected flow:
- Branch created → GitHub Actions triggered → Docker container running → PR opened
- Typical turnaround: 2–15 minutes depending on task complexity

### Step 5 — Route PR Through AUTONOMOUS_CI_AGENT

Once the PopeBot PR is open, invoke the full 6-phase CI/CD workflow:
```
Load .github/AUTONOMOUS_CI_AGENT.prompt.md and execute for PR #<N>.
```

Phase 1 (AI Code Review) is especially critical for PopeBot PRs — the Docker
agent may introduce subtle issues that look syntactically valid but violate
project conventions (OWASP checks, schema integrity, no hardcoded secrets).

### Step 6 — Merge and Notify

On clean CI + Phase 1 APPROVE: Phase 3 squash-merges.
Notification arrives via configured webhook (Discord/Slack) in `.ralphy/config.yaml`.

## PopeBot Architecture Reference

```
┌────────────────────────────────────────────────────────────┐
│                    AGENT ZERO (orchestrator)               │
│           Claude Code / GitHub Copilot                     │
│    Dispatches → Monitors → Reviews → Merges                │
└──────────────────┬─────────────────────────────────────────┘
                   │ POST /api/create-job
                   ▼
┌────────────────────────────────────────────────────────────┐
│               EVENT HANDLER (always-on server)             │
│          Creates job/* branch → triggers GH Actions        │
└──────────────────┬─────────────────────────────────────────┘
                   │ run-job.yml triggers
                   ▼
┌────────────────────────────────────────────────────────────┐
│            DOCKER AGENT (Pi coding agent)                  │
│       Executes task → commits → opens PR                   │
└──────────────────┬─────────────────────────────────────────┘
                   │ PR opened
                   ▼
┌────────────────────────────────────────────────────────────┐
│          AUTONOMOUS_CI_AGENT (6-phase review)              │
│    Phase 1 review → Phase 2 CI gate → Phase 3 merge        │
└────────────────────────────────────────────────────────────┘
```

## PopeBot Configuration Files

| File | Purpose |
|------|---------|
| `config/SOUL.md` | Agent personality and behavior — customize this |
| `config/EVENT_HANDLER.md` | How the event handler interprets job requests |
| `config/AGENT.md` | Agent operating instructions |
| `config/CRONS.json` | Scheduled recurring jobs |
| `config/TRIGGERS.json` | Webhook triggers |
| `docker/job/Dockerfile` | Docker image for the job container |
| `.github/workflows/` | run-job.yml, auto-merge.yml, rebuild-event-handler.yml |

## Secrets for PopeBot (via Infisical)

Required GitHub repository secrets (set via `npx thepopebot set-agent-secret`):
```
AGENT_GH_TOKEN          — GitHub token for the Docker agent
AGENT_ANTHROPIC_API_KEY — Anthropic API key for Pi agent
GH_WEBHOOK_SECRET       — HMAC secret for webhook validation (workflow-only)
```

Optional:
```
AGENT_LLM_BRAVE_API_KEY — Brave Search for web research
```

**Never commit these to .env or any repo file.**
Use `npx thepopebot set-agent-secret KEY VALUE` to set them.

## Graph Logic for PopeBot Jobs

Every PopeBot job dispatch must be recorded as a graph node in the session:

```
node: {type: "task", id: "job-<slug>", owner: "popebot", status: "dispatched"}
edge: {from: "agent-zero", to: "popebot", type: "dispatches"}
edge: {from: "job-<slug>", to: "main", type: "produces" (pending merge)}
```

This ensures Agent Zero maintains graph awareness of all in-flight work and can
apply Meadows blast radius analysis before dispatching the next job.

## Source Repository
`git@github.com:executiveusa/paulis-pope-bot.git`
(forked from `stephengpope/thepopebot`)
