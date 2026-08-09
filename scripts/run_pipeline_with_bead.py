"""Beads-gated entrypoint for YAPPYVERSE Character Factory.

Use this instead of invoking pipeline.py directly for production work.
"""
from __future__ import annotations

import argparse
import os

from beads_guard import BeadsGuardError, require_active_bead
from pipeline import run_batch, run_character


def main() -> int:
    """Validate a claimed Bead, then dispatch exactly one factory target."""
    parser = argparse.ArgumentParser(description="YAPPYVERSE Beads-gated Character Factory")
    parser.add_argument("--bead-id", default=os.environ.get("BEAD_ID"), help="Active Beads work-item ID")
    target = parser.add_mutually_exclusive_group(required=True)
    target.add_argument("--character", help="Character canonical ID (e.g. pauli)")
    target.add_argument("--batch", action="store_true", help="Run all queued characters")
    parser.add_argument(
        "--stage",
        default="all",
        choices=["all", "scan", "model", "rig", "nft", "qa"],
        help="Pipeline stage to run for --character (default: all)",
    )
    args = parser.parse_args()

    try:
        bead_id = require_active_bead(args.bead_id)
    except BeadsGuardError as exc:
        parser.error(str(exc))

    os.environ["BEAD_ID"] = bead_id
    print(f"[beads] execution authorized by {bead_id}")

    if args.batch:
        run_batch()
        return 0

    run_character(args.character, stage=args.stage)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
