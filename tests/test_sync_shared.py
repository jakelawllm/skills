"""Tests for scripts/sync_shared.py.

Run with:
    python -m unittest discover -s tests
"""

from __future__ import annotations

import pathlib
import sys
import tempfile
import unittest

_REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
_SCRIPTS_DIR = _REPO_ROOT / "scripts"
_TESTS_DIR = pathlib.Path(__file__).resolve().parent

for _p in (_SCRIPTS_DIR, _TESTS_DIR):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))

import _common as common  # noqa: E402
import sync_shared  # noqa: E402
import _support  # noqa: E402


class SyncSharedTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.root = pathlib.Path(self._tmp.name)
        self.skill_names = _support.FIXTURE_SKILL_NAMES
        _support.patch_common_repo(self, self.root, self.skill_names)

    def _make_shared_only(self) -> None:
        """Shared canonical files and bare skill directories, no generated copies yet."""
        shared_dir = self.root / "shared"
        shared_dir.mkdir(parents=True, exist_ok=True)
        (shared_dir / "legal-accuracy-and-court-rules.md").write_text(
            "# Legal accuracy\n\nContent.\n", encoding="utf-8"
        )
        (shared_dir / "style-audit.md").write_text("# Style audit\n\nContent.\n", encoding="utf-8")
        for name in self.skill_names:
            (self.root / name / "references").mkdir(parents=True, exist_ok=True)

    def test_check_reports_missing_copies_and_does_not_write(self) -> None:
        self._make_shared_only()
        exit_code = sync_shared.sync(check=True)
        self.assertEqual(exit_code, 1)
        for name in self.skill_names:
            self.assertFalse((self.root / name / "references" / "legal-accuracy-and-court-rules.md").exists())
            self.assertFalse((self.root / name / "references" / "style-audit.md").exists())

    def test_sync_writes_header_and_content(self) -> None:
        self._make_shared_only()
        exit_code = sync_shared.sync(check=False)
        self.assertEqual(exit_code, 0)
        for name in self.skill_names:
            written = (self.root / name / "references" / "legal-accuracy-and-court-rules.md").read_text(
                encoding="utf-8"
            )
            self.assertTrue(
                written.startswith(
                    "<!-- Generated from shared/legal-accuracy-and-court-rules.md. "
                    "Do not edit this copy directly. -->\n\n"
                )
            )
            self.assertIn("# Legal accuracy\n\nContent.\n", written)

    def test_check_passes_once_copies_are_current(self) -> None:
        self._make_shared_only()
        sync_shared.sync(check=False)
        exit_code = sync_shared.sync(check=True)
        self.assertEqual(exit_code, 0)

    def test_check_detects_stale_copy(self) -> None:
        self._make_shared_only()
        sync_shared.sync(check=False)
        # Hand-edit one generated copy so it no longer matches shared/.
        stale_target = self.root / self.skill_names[0] / "references" / "style-audit.md"
        stale_target.write_text("stale content that does not match shared/style-audit.md\n", encoding="utf-8")
        exit_code = sync_shared.sync(check=True)
        self.assertEqual(exit_code, 1)

    def test_check_never_modifies_files(self) -> None:
        self._make_shared_only()
        sync_shared.sync(check=False)
        target = self.root / self.skill_names[0] / "references" / "style-audit.md"
        before = target.read_text(encoding="utf-8")
        before_mtime = target.stat().st_mtime_ns
        sync_shared.sync(check=True)
        after = target.read_text(encoding="utf-8")
        after_mtime = target.stat().st_mtime_ns
        self.assertEqual(before, after)
        self.assertEqual(before_mtime, after_mtime)

    def test_sync_is_idempotent(self) -> None:
        self._make_shared_only()
        sync_shared.sync(check=False)
        first_pass_content = {
            name: (self.root / name / "references" / "style-audit.md").read_text(encoding="utf-8")
            for name in self.skill_names
        }
        sync_shared.sync(check=False)
        second_pass_content = {
            name: (self.root / name / "references" / "style-audit.md").read_text(encoding="utf-8")
            for name in self.skill_names
        }
        self.assertEqual(first_pass_content, second_pass_content)

    def test_check_uses_forward_slash_repo_relative_paths(self) -> None:
        self._make_shared_only()
        problems = common.check_generated_copies()
        self.assertTrue(problems)
        for problem in problems:
            self.assertNotIn("\\", problem["target"])
            self.assertNotIn("\\", problem["shared_file"])
            self.assertFalse(problem["target"].startswith("/"))
            self.assertFalse(pathlib.PurePosixPath(problem["target"]).is_absolute())


if __name__ == "__main__":
    unittest.main()
