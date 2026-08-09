"""Hermetic tests for Yappyverse's mandatory Beads execution contract."""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS))

import beads_guard  # noqa: E402
import pipeline  # noqa: E402


class BeadsGuardTests(unittest.TestCase):
    """Verify fail-closed behavior without requiring a real Beads database."""

    def _root_with_db(self, temp_dir: str) -> Path:
        root = Path(temp_dir)
        (root / ".beads").mkdir()
        return root

    def test_missing_id_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            with patch.dict("os.environ", {}, clear=True):
                with self.assertRaises(beads_guard.BeadsGuardError):
                    beads_guard.require_active_bead(repo_root=Path(temp_dir))

    def test_missing_bd_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = self._root_with_db(temp_dir)
            with patch("beads_guard.shutil.which", return_value=None):
                with self.assertRaises(beads_guard.BeadsGuardError):
                    beads_guard.require_active_bead("bd-test", repo_root=root)

    def test_unresolved_bead_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = self._root_with_db(temp_dir)
            result = subprocess.CompletedProcess(["bd"], 1, stdout="", stderr="not found")
            with patch("beads_guard.shutil.which", return_value="/fake/bd"), patch(
                "beads_guard.subprocess.run", return_value=result
            ):
                with self.assertRaises(beads_guard.BeadsGuardError):
                    beads_guard.require_active_bead("bd-missing", repo_root=root)

    def test_malformed_json_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = self._root_with_db(temp_dir)
            result = subprocess.CompletedProcess(["bd"], 0, stdout="not-json", stderr="")
            with patch("beads_guard.shutil.which", return_value="/fake/bd"), patch(
                "beads_guard.subprocess.run", return_value=result
            ):
                with self.assertRaises(beads_guard.BeadsGuardError):
                    beads_guard.require_active_bead("bd-bad-json", repo_root=root)

    def test_open_unclaimed_bead_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = self._root_with_db(temp_dir)
            payload = {"id": "bd-open", "status": "open", "assignee": ""}
            result = subprocess.CompletedProcess(["bd"], 0, stdout=json.dumps(payload), stderr="")
            with patch("beads_guard.shutil.which", return_value="/fake/bd"), patch(
                "beads_guard.subprocess.run", return_value=result
            ):
                with self.assertRaises(beads_guard.BeadsGuardError):
                    beads_guard.require_active_bead("bd-open", repo_root=root)

    def test_active_assigned_bead_accepted(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = self._root_with_db(temp_dir)
            payload = {"id": "bd-good", "status": "in_progress", "assignee": "worker-1"}
            result = subprocess.CompletedProcess(["bd"], 0, stdout=json.dumps(payload), stderr="")
            with patch("beads_guard.shutil.which", return_value="/fake/bd"), patch(
                "beads_guard.subprocess.run", return_value=result
            ):
                self.assertEqual(
                    beads_guard.require_active_bead("bd-good", repo_root=root),
                    "bd-good",
                )


class SharedMutationBoundaryTests(unittest.TestCase):
    """Ensure bypassing the wrapper cannot bypass Beads enforcement."""

    def test_run_character_checks_bead_before_work(self) -> None:
        with patch("pipeline.require_active_bead", side_effect=beads_guard.BeadsGuardError("blocked")):
            with self.assertRaises(beads_guard.BeadsGuardError):
                pipeline.run_character("pauli")

    def test_run_batch_checks_bead_before_work(self) -> None:
        with patch("pipeline.require_active_bead", side_effect=beads_guard.BeadsGuardError("blocked")):
            with self.assertRaises(beads_guard.BeadsGuardError):
                pipeline.run_batch()


if __name__ == "__main__":
    unittest.main()
