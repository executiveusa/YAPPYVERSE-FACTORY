"""Yappyverse Beads execution guard.

Mutating production work must have a resolvable, claimed, active Bead ID. This
module is intentionally small so any workflow can import it without depending
on the rest of the factory runtime.
"""
from __future__ import annotations

import json
import os
import shutil
import subprocess
from pathlib import Path


class BeadsGuardError(RuntimeError):
    """Raised when a mutating operation has no valid active Beads work item."""


def _repo_root() -> Path:
    """Return the repository root inferred from this script location."""
    return Path(__file__).resolve().parents[1]


def _issue_from_payload(payload: object) -> dict:
    """Normalize `bd show --json` output to one issue object."""
    if isinstance(payload, list):
        if not payload:
            return {}
        issue = payload[0]
    else:
        issue = payload
    return issue if isinstance(issue, dict) else {}


def require_active_bead(bead_id: str | None = None, repo_root: Path | None = None) -> str:
    """Validate that Beads is installed and the requested work item is claimed.

    The guard fails closed. A Bead must resolve, be assigned, and be in an
    active/in-progress status before mutating work may proceed.
    """
    root = repo_root or _repo_root()
    resolved_id = (bead_id or os.environ.get("BEAD_ID") or "").strip()

    if not resolved_id:
        raise BeadsGuardError(
            "Mutating Yappyverse work requires an active Bead ID. "
            "Set BEAD_ID=<id> or pass --bead-id <id>."
        )

    bd = shutil.which("bd")
    if not bd:
        raise BeadsGuardError(
            "Beads CLI (bd) is not installed. Run scripts/bootstrap_beads.* first."
        )

    if not (root / ".beads").exists():
        raise BeadsGuardError(
            f"Beads is not initialized in {root}. Run 'bd init --quiet' there first."
        )

    result = subprocess.run(
        [bd, "show", resolved_id, "--json"],
        cwd=str(root),
        capture_output=True,
        text=True,
        timeout=20,
    )
    if result.returncode != 0:
        detail = (result.stderr or result.stdout or "unknown bd error").strip()
        raise BeadsGuardError(f"Bead '{resolved_id}' did not resolve: {detail[:300]}")

    try:
        payload = json.loads(result.stdout)
    except json.JSONDecodeError as exc:
        raise BeadsGuardError("bd show returned non-JSON output; cannot verify work item") from exc

    issue = _issue_from_payload(payload)
    if not issue:
        raise BeadsGuardError(f"Bead '{resolved_id}' resolved to an empty result")

    status = str(issue.get("status") or "").strip().lower()
    assignee = str(issue.get("assignee") or "").strip()
    active_statuses = {"in_progress", "active", "wip"}

    if status not in active_statuses:
        raise BeadsGuardError(
            f"Bead '{resolved_id}' is not active/claimed (status={status or 'missing'}). "
            f"Claim it first with 'bd update {resolved_id} --claim'."
        )

    if not assignee:
        raise BeadsGuardError(
            f"Bead '{resolved_id}' has no assignee. Claim it first with "
            f"'bd update {resolved_id} --claim'."
        )

    return resolved_id
