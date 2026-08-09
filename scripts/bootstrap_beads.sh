#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

NORTH_TITLE="Yappyverse North Star — owner directs outcomes, agents execute verified work"
MILESTONE_TITLE="Milestone 1 — autonomous ASC3ND Why We Started Reel acceptance run"

if ! command -v bd >/dev/null 2>&1; then
  cat >&2 <<'EOF'
[beads] ERROR: bd is not installed.
Install Beads from an official, checksum-verified gastownhall/beads release,
then re-run this script. Do not pipe mutable remote installer content to a shell.
Official releases: https://github.com/gastownhall/beads/releases
EOF
  exit 2
fi

bd version

if [ ! -d .beads ]; then
  echo "[beads] initializing repository..."
  bd init --quiet
fi

# Agent setup is best-effort because the corresponding host may not exist on
# every machine. Beads itself remains mandatory even when an editor integration
# is unavailable.
bd setup codex >/dev/null 2>&1 || true
bd setup claude >/dev/null 2>&1 || true

find_bead_id() {
  local title="$1"
  bd list --json | python -c '
import json, sys
wanted = sys.argv[1]
x = json.load(sys.stdin)
items = x if isinstance(x, list) else [x]
for item in items:
    if isinstance(item, dict) and item.get("title") == wanted:
        print(item.get("id", ""))
        break
' "$title"
}

create_bead() {
  local title="$1"
  local priority="$2"
  shift 2
  bd create "$title" -p "$priority" "$@" --json | python -c '
import json, sys
x = json.load(sys.stdin)
x = x[0] if isinstance(x, list) else x
print(x["id"])
'
}

echo "[beads] reconciling North Star graph..."
NORTH_ID="$(find_bead_id "$NORTH_TITLE")"
if [ -z "$NORTH_ID" ]; then
  NORTH_ID="$(create_bead "$NORTH_TITLE" 0 -t epic)"
fi

MILESTONE_ID="$(find_bead_id "$MILESTONE_TITLE")"
if [ -z "$MILESTONE_ID" ]; then
  # --parent creates hierarchy without making the long-lived North Star a
  # completion blocker. Child work remains discoverable through `bd ready`.
  MILESTONE_ID="$(create_bead "$MILESTONE_TITLE" 0 --parent "$NORTH_ID")"
fi

# Always reconcile descriptions so interrupted bootstrap runs self-heal.
bd update "$NORTH_ID" --description "MODE: operating-system transformation. OUTCOME: owner directs outcomes instead of routing tasks. TARGET: autonomous, sovereign Yappyverse agent network. CONSTRAINTS: Beads mandatory; evidence before claims; cost governed; human gates for publishing/irreversible/high-consequence actions. PROOF: repeated end-to-end verified commercial or mission outcomes without owner task routing. COMMERCIAL VALUE: operating leverage, reusable IP, client delivery, revenue."

bd update "$MILESTONE_ID" --description "MODE: production acceptance test. OUTCOME: prepare ASC3ND Wednesday 'Why We Started' Reel end-to-end without owner routing. TARGET: review-ready final MP4 + story/timestamp/cost/QA receipts. CONSTRAINTS: real footage/voice only; no publish before approval; Opus costs tracked; builders cannot self-approve. PROOF: final review MP4, independent taste + truth/privacy verdict, Opus credit delta, caption/post proposal. COMMERCIAL VALUE: proves Yappyverse can autonomously fulfill repeatable client media work."

# Reconcile the edge type on every run. A previous bootstrap version created a
# default `blocks` edge here, which would keep this milestone off `bd ready`
# forever because the North Star is intentionally long-lived. Remove any old
# edge, then restore the correct hierarchy relation.
bd dep remove "$MILESTONE_ID" "$NORTH_ID" >/dev/null 2>&1 || true
bd dep add "$MILESTONE_ID" "$NORTH_ID" --type parent-child

echo "[beads] North Star: $NORTH_ID"
echo "[beads] First milestone: $MILESTONE_ID"
echo "[beads] Claim the milestone when execution begins: bd update $MILESTONE_ID --claim"

bd prime
bd ready --json

echo "[beads] bootstrap complete. Beads is now the mandatory task system for this repo."
