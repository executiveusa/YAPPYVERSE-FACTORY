# AGENTS.md — YAPPYVERSE-FACTORY Agent Roster
## The Full Agent Fleet — Topology, Capabilities, Invocation
**Authority:** EMERALD_TABLETS.md Part V (canonical topology)  
**Owner:** Agent Zero (Claude Code / GitHub Copilot)  
**Version:** 1.0 | March 2026

---

> All agents MUST read `EMERALD_TABLETS.md` before operating.
> All commits use ZTE format: `[SYNTHIA][BEAD-ID] type: what | LP# | score delta`
> All secrets stay in `.env` or Infisical. Nothing hardcoded. Ever.

---

## AGENT ZERO

| Field | Value |
|-------|-------|
| **Identity** | Claude Code / GitHub Copilot |
| **Role** | Orchestrator, architect, merge authority |
| **EMERALD_TABLETS** | Part I — Agent Zero Declaration (read first) |
| **Context loading** | EMERALD_TABLETS.md → CLAUDE.md → .claude/skills/* |

**Exclusive authorities:**
- Git commits to `main`
- PR merge decisions (after AI review + CI green)
- Vercel deploy approvals
- PopeBot dispatch (SOP-006)
- Secret rotation (SOP-007)
- Multi-service deploy plans (blast radius > 3)

**Invocation:** Active by default in this repo. No explicit invocation needed.  
**Constraints:** Never skip quality gates (EMERALD_TABLETS Part VIII). Never print secrets.

---

## JCODEMUNCH

| Field | Value |
|-------|-------|
| **Source** | `https://github.com/jgravelle/jcodemunch-mcp` |
| **Role** | Token-efficient code retrieval via MCP |
| **EMERALD_TABLETS** | SOP-001 (mandatory SOP before any code lookup) |
| **Token savings** | 95%+ vs. full file reads |

**Capabilities:**
- `list_repos` — view all indexed repositories
- `index_folder("<path>")` — build symbol index of a directory
- `search_symbols("<name>")` — find any function/class/variable by name
- `get_symbol("<file>", "<symbol>")` — retrieve exact symbol definition
- `get_context_bundle("<file>", "<symbol>")` — callers + callees + docs
- `get_file_outline("<file>")` — structure without content
- `invalidate_cache` — refresh after large merges

**Invocation:**
```
Load jcodemunch-mcp and follow SOP-001 for all code lookups.
```

**Constraints:** Index must be valid before symbol search. Invalidate after large merges.

---

## RALPHY

| Field | Value |
|-------|-------|
| **Source** | `https://github.com/michaelshimeles/ralphy` |
| **Role** | Autonomous AI coding loop (Ask→Plan→Execute→Observe→Iterate) |
| **EMERALD_TABLETS** | SOP-002 |
| **Config** | `.ralphy/config.yaml` |

**Capabilities:**
- Single task execution with `--copilot` engine
- PRD-driven multi-task with `--prd PRD.md`
- Parallel branch-per-task with `--parallel --branch-per-task --create-pr`
- Dry-run preview with `--dry-run`

**Invocation:**
```bash
ralphy --copilot "task description"
ralphy --copilot --prd PRD.md --parallel --max-parallel 3 --branch-per-task --create-pr
```

**Constraints:** Do not modify `.ralphy/config.yaml` mid-session. Max 3 parallel agents without approval.

---

## AUTONOMOUS_CI_AGENT

| Field | Value |
|-------|-------|
| **Source** | `.github/AUTONOMOUS_CI_AGENT.prompt.md` |
| **Role** | 6-phase CI/CD loop: review → CI → merge → deploy → E2E |
| **EMERALD_TABLETS** | SOP-003 |
| **Trigger** | Any open PR, or explicit invocation |

**6 Phases:**
1. Discovery — read state, collect open PRs
2. AI Code Review — OWASP + quality + schema + asset checks
3. CI Green Gate — poll GitHub Actions (10 min timeout)
4. Squash Merge — PUT /pulls/{n}/merge
5. Vercel Deploy — poll deployments, retry up to 5×
6. Live URL Check + Final Export — HTTP 200, write deploy_result.txt

**Invocation:**
```
Load E:\YAPPYVERSE-FACTORY\.github\AUTONOMOUS_CI_AGENT.prompt.md
and execute the full 6-phase autonomous CI/CD workflow for all open PRs.
```

**Constraints:** Never stop between phases. Never push to main except Phase 4 auto-fix. Never print secrets.

---

## SYNTHIA™ MCP

| Field | Value |
|-------|-------|
| **Source** | `.claude/skills/synthia-architecture/SKILL.md` → `EMERALD_TABLETS.md Part III` |
| **Role** | 12-axis architecture scoring, UDEC frontend audit, systems design intelligence |
| **EMERALD_TABLETS** | Part III (full SYNTHIA™ v4.0 force prompt) + SOP-008 |
| **Floor** | 8.5/10 overall | FBK ≥ 7.0 | RSL ≥ 7.0 | SEC ≥ 8.0 |

**Tools exposed (when running as MCP server):**
- `synthia_audit(url)` — 12-axis + UDEC score with violations + fixes
- `synthia_migrate(wp_xml, routes)` → Vercel preview URL + spec file
- `synthia_graph_query(cypher)` — Neo4j pattern store query
- `synthia_score_architecture(description)` — Meadows stock/flow/feedback analysis

**Skill invocation:**
```
Load .claude/skills/synthia-architecture/SKILL.md and score this architecture.
```

**MCP install:**
```json
{
  "mcpServers": {
    "synthia": {
      "command": "npx",
      "args": ["@kupurimedia/synthia-mcp", "proxy"],
      "env": { "SYNTHIA_LICENSE_KEY": "your-license-key" }
    }
  }
}
```

**Constraints:** Must have EMERALD_TABLETS.md present (stub skill points to it). Floor 8.5 blocks commits.

---

## POPEBOT FLEET

| Field | Value |
|-------|-------|
| **Source** | `git@github.com:executiveusa/paulis-pope-bot.git` |
| **Role** | Docker autonomous Pi coding agents — create branches, write code, open PRs |
| **EMERALD_TABLETS** | SOP-006 (dispatch protocol — Agent Zero ONLY) |
| **Authority** | Subordinate to Agent Zero. Cannot merge. Cannot touch main. |

**Dispatch flow:**
1. Agent Zero creates `job/<task-slug>` branch
2. Agent Zero pushes branch → GitHub Action triggers
3. PopeBot Docker container runs Pi coding agent
4. Pi commits + opens PR targeting main
5. Agent Zero processes PR via AUTONOMOUS_CI_AGENT

**Direct dispatch:**
```http
POST /api/create-job
X-API-Key: <AGENT_GH_TOKEN>
{"job_description": "task description", "priority": "normal"}
```

**Constraints:** Agent Zero authority only. Cost guard: $10/job. Cannot merge, rotate secrets, or spawn other bots.

---

## AGENT-BROWSER (E2E)

| Field | Value |
|-------|-------|
| **Source** | `.claude/skills/e2e-test/SKILL.md` |
| **Role** | Post-deploy end-to-end browser testing |
| **EMERALD_TABLETS** | SOP-004 |
| **Environment** | Linux / WSL / macOS ONLY — skip natively on Windows |

**Capabilities:**
- Open URLs and take screenshots
- Test complete user journeys
- Validate database state after form submissions
- Responsive checks across viewports
- Bug hunting across UI, logic, data, and security layers

**3-agent parallel research:**
- Sub-agent 1: App structure + user journeys + startup commands
- Sub-agent 2: DB schema + data flows + validation queries
- Sub-agent 3: Bug hunting (logic, UI, security, data)

**Invocation:**
```bash
agent-browser open <url>
# Then follow SOP-004 for full 6-phase e2e sweep
```

**Constraints:** WSL only on Windows. Screenshots → `e2e-screenshots/<journey>/NN-description.png`.

---

## AGENT INTERACTION RULES

1. **Reading order:** EMERALD_TABLETS.md → CLAUDE.md → relevant skill files → task
2. **Commit format:** `[SYNTHIA][BEAD-ID] type: what | LP# | score delta` (no exceptions)
3. **Blast radius:** No single action touches > 3 services without explicit plan + approval
4. **Secrets:** All in `.env` or Infisical. Never in code. Never in commits.
5. **Quality gate:** SYNTHIA™ score ≥ 8.5 before architectural commits. FBK/RSL ≥ 7.0 or redesign first.
6. **Cost guard:** $10/PopeBot job, $50/day API total. Halt and alert if exceeded.
7. **Circuit breaker:** Same failure 3× → escalate, do NOT retry same approach.
8. **Irreversible actions:** Always halt and confirm with user before proceeding.


---

## OPEN BRAIN

| Field | Value |
|-------|-------|
| **Source** | `tools/open_brain.py` + `db/second_brain_schema.sql` |
| **Role** | Persistent AI memory — semantic search, CRUD, tagging, linking |
| **Database** | `second_brain` on VPS `31.220.58.212` (Supabase self-hosted) |
| **EMERALD_TABLETS** | Part II (Persistence Layer) |
| **Docs** | `OPEN_BRAIN.md` |

**Capabilities:**
- `brain.save_memory(title, content, ...)` — persist insights, code, tasks, conversations
- `brain.search(query)` — ranked full-text search (BM25-style with tsvector weights)
- `brain.search_by_vector(embedding, min_similarity)` — cosine similarity (384-dim HNSW)
- `brain.tag_memory(id, tag)` / `brain.get_tags(id)` — flat tag vocabulary
- `brain.link_memories(a, b, relationship)` — directed knowledge graph edges
- `brain.start_conversation(title)` / `brain.add_message(conv_id, role, content)` — session logging
- `brain.set_preference(key, value)` / `brain.get_preference(key)` — agent settings
- `brain.create_collection(name)` / `brain.add_to_collection(coll_id, mem_id)` — curated sets
- `brain.stats()` — quick table counts

**Invocation:**
```python
from tools.open_brain import OpenBrain
brain = OpenBrain()  # env vars: SUPABASE_SERVICE_ROLE_KEY, DATABASE_URL
```

**Connection method:** Supabase pg meta `/pg/query` API — no direct PostgreSQL port required.
Credentials in `.env` (see `.env.template`). Schema in `db/second_brain_schema.sql`.

**Constraints:** Use service role key. Never expose credentials in commits.
Schema is idempotent — re-run `db/second_brain_schema.sql` to restore after wipe.


---

*AGENTS.md v1.0 | YAPPYVERSE-FACTORY | Agent Zero authority | Kupuri Media™*
