"""Yappyverse Beads execution guard.

Mutating production work must have a resolvable Bead ID. This module is
intentionally small so any workflow can import it without depending on the
rest of the factory runtime.
"""
from __future__ import annotations

import json
import os
import shutil
import subprocess
from pathlib import Path


class BeadsGuardError(RuntimeError):
    """Raised when a mutating operation has no valid Beads work item."""


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def require_active_bead(bead_id: str | None = None, repo_root: Path | None = None) -> str:
    """Validate that Beads is installed, initialized, and the bead resolves.

    Returns the validated bead ID. The guard is fail-closed by design.
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

    if not payload:
        raise BeadsGuardError(f"Bead '{resolved_id}' resolved to an empty result")

    return resolved_id
