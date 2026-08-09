#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

if ! command -v bd >/dev/null 2>&1; then
  echo "[beads] bd not found; installing official gastownhall/beads release..."
  curl -fsSL https://raw.githubusercontent.com/gastownhall/beads/main/scripts/install.sh | bash
  export PATH="$HOME/.local/bin:$PATH"
fi

bd version

if [ ! -d .beads ]; then
  echo "[beads] initializing repository..."
  bd init --quiet
fi

# Set up integrations when available. These are idempotent/best-effort because
# a given machine may not have every host installed.
bd setup codex >/dev/null 2>&1 || true
bd setup claude >/dev/null 2>&1 || true

# Seed only when a North Star bead is not already present.
if bd list --json 2>/dev/null | grep -q 'Yappyverse North Star'; then
  echo "[beads] North Star already seeded; no duplicate created."
else
  echo "[beads] seeding North Star graph..."
  north_json="$(bd create "Yappyverse North Star — owner directs outcomes, agents execute verified work" -p 0 --json)"
  NORTH_ID="$(printf '%s' "$north_json" | python -c 'import json,sys; x=json.load(sys.stdin); x=x[0] if isinstance(x,list) else x; print(x["id"])')"

  milestone_json="$(bd create "Milestone 1 — autonomous ASC3ND Why We Started Reel acceptance run" -p 0 --json)"
  MILESTONE_ID="$(printf '%s' "$milestone_json" | python -c 'import json,sys; x=json.load(sys.stdin); x=x[0] if isinstance(x,list) else x; print(x["id"])')"

  bd dep add "$MILESTONE_ID" "$NORTH_ID"

  bd update "$NORTH_ID" --description "MODE: operating-system transformation. OUTCOME: owner directs outcomes instead of routing tasks. TARGET: autonomous, sovereign Yappyverse agent network. CONSTRAINTS: Beads mandatory; evidence before claims; cost governed; human gates for publishing/irreversible/high-consequence actions. PROOF: repeated end-to-end verified commercial or mission outcomes without owner task routing. COMMERCIAL VALUE: operating leverage, reusable IP, client delivery, revenue."

  bd update "$MILESTONE_ID" --description "MODE: production acceptance test. OUTCOME: prepare ASC3ND Wednesday 'Why We Started' Reel end-to-end without owner routing. TARGET: review-ready final MP4 + story/timestamp/cost/QA receipts. CONSTRAINTS: real footage/voice only; no publish before approval; Opus costs tracked; builders cannot self-approve. PROOF: final review MP4, independent taste + truth/privacy verdict, Opus credit delta, caption/post proposal. COMMERCIAL VALUE: proves Yappyverse can autonomously fulfill repeatable client media work."

  echo "[beads] North Star: $NORTH_ID"
  echo "[beads] First milestone: $MILESTONE_ID"
  echo "[beads] Claim the milestone when execution begins: bd update $MILESTONE_ID --claim"
fi

bd prime
bd ready --json

echo "[beads] bootstrap complete. Beads is now the mandatory task system for this repo."
