# YAPPYVERSE-FACTORY — Claude Code Instructions

## 1. Code Lookup: Use jcodemunch-mcp FIRST

Never read full files when jcodemunch-mcp is available.

**Mandatory workflow for any code lookup:**
1. Call `list_repos` — if the repo isn't indexed, call `index_folder` with `E:\YAPPYVERSE-FACTORY`
2. Use `search_symbols` / `get_symbol` to find and retrieve code by name (function, class, variable)
3. Use `get_repo_outline` or `get_file_outline` to see a file's structure without reading it whole
4. Use `get_context_bundle` to pull a symbol plus its callers/callees in one shot
5. Fall back to direct file reads **only when editing** or when MCP is unavailable

Token savings: ~200 tokens to find a function vs ~40,000 for reading the file.
Indexing: `index_folder` on `E:\YAPPYVERSE-FACTORY` once per session; `invalidate_cache` after large merges.

---

## 2. Task Execution: Use Ralphy for PRD-based Work

Ralphy (`ralphy-cli`) runs AI agents in a loop until a PRD or single task is done.

**Install (once):**
```bash
npm install -g ralphy-cli
```

**Common invocations:**
```bash
# Single task (uses GitHub Copilot engine by default here)
ralphy --copilot "add dark mode toggle to public/index.html"

# Work through PRD.md
ralphy --copilot --prd PRD.md

# Parallel agents, one branch + PR per task (triggers AUTONOMOUS_CI_AGENT)
ralphy --copilot --prd PRD.md --parallel --max-parallel 3 --branch-per-task --create-pr

# Dry-run to preview tasks without executing
ralphy --dry-run --prd PRD.md
```

**Project config** is in `.ralphy/config.yaml` — never modify it manually mid-session.

**Ralphy loop:** Ask → Plan → Execute → Observe → Iterate (retries up to 3× per task).

---

## 3. Testing: Use the e2e-test Skill

Run `/e2e-test` after any deploy to validate the Vercel site end-to-end.

The skill lives at `.claude/skills/e2e-test/SKILL.md`.

- Requires Linux/WSL/macOS (`agent-browser` does NOT work on native Windows)
- Launches 3 parallel research sub-agents (app structure, DB schema, bug hunting)
- Tests every user journey with `agent-browser` + takes screenshots
- Validates DB records after each interaction
- Handles responsive testing at mobile / tablet / desktop viewports

---

## 4. CI/CD: Autonomous Agent

The full CI/CD meta-prompt is at `.github/AUTONOMOUS_CI_AGENT.prompt.md`.

Invocation one-liner:
```
Load E:\YAPPYVERSE-FACTORY\.github\AUTONOMOUS_CI_AGENT.prompt.md and execute
the 6-phase autonomous CI/CD workflow for all open PRs on
github.com/executiveusa/YAPPYVERSE-FACTORY targeting main.
Do not stop until you print a working Vercel URL or exhaust all retries.
```

---

## 5. Project Boundaries

Never touch:
- `*.lock`
- `.ralphy/progress.txt`, `.ralphy-worktrees/`, `.ralphy-sandboxes/`
- `src/assets/pauli/**` (source-of-truth Pauli character assets)

Test command: `python -S scripts/pipeline.py --dry-run`
Lint: (none configured yet)
Build: Vercel auto-builds from `public/` on push to `main`
