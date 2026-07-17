"""Tests for scripts/package_skills.py.

Run with:
    python -m unittest discover -s tests
"""

from __future__ import annotations

import pathlib
import sys
import tempfile
import unittest
import zipfile

_REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
_SCRIPTS_DIR = _REPO_ROOT / "scripts"
_TESTS_DIR = pathlib.Path(__file__).resolve().parent

for _p in (_SCRIPTS_DIR, _TESTS_DIR):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))

import package_skills  # noqa: E402
import _support  # noqa: E402


class _FixtureRepoTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.root = pathlib.Path(self._tmp.name)
        self.skill_names = _support.FIXTURE_SKILL_NAMES
        _support.patch_common_repo(self, self.root, self.skill_names)
        _support.build_minimal_repo(self.root, self.skill_names)
        self.dist_dir = self.root / "dist"


class ZipRootStructureTestCase(_FixtureRepoTestCase):
    def test_every_archive_member_is_rooted_at_the_skill_name(self) -> None:
        exit_code = package_skills.package_all(self.skill_names, dist_dir=self.dist_dir)
        self.assertEqual(exit_code, 0)
        for name in self.skill_names:
            archive_path = self.dist_dir / f"{name}.zip"
            self.assertTrue(archive_path.is_file())
            with zipfile.ZipFile(archive_path) as zf:
                names = zf.namelist()
                self.assertTrue(names, "archive must not be empty")
                for member in names:
                    self.assertTrue(
                        member == name or member.startswith(f"{name}/"),
                        f"{member!r} is not rooted at {name!r}",
                    )
                # A representative required file must be present at the expected path.
                self.assertIn(f"{name}/SKILL.md", names)
                self.assertIn(f"{name}/examples.md", names)
                self.assertIn(f"{name}/references/register-guide.md", names)

    def test_archive_contains_no_files_from_another_skill(self) -> None:
        package_skills.package_all(self.skill_names, dist_dir=self.dist_dir)
        first, second = self.skill_names
        with zipfile.ZipFile(self.dist_dir / f"{first}.zip") as zf:
            names = zf.namelist()
        self.assertFalse(any(n.startswith(f"{second}/") for n in names))


class DeterministicPackageTestCase(_FixtureRepoTestCase):
    def test_repeated_builds_produce_byte_identical_archives(self) -> None:
        first_dist = self.root / "dist-first"
        second_dist = self.root / "dist-second"
        package_skills.package_all(self.skill_names, dist_dir=first_dist)
        package_skills.package_all(self.skill_names, dist_dir=second_dist)
        for name in self.skill_names:
            first_bytes = (first_dist / f"{name}.zip").read_bytes()
            second_bytes = (second_dist / f"{name}.zip").read_bytes()
            self.assertEqual(first_bytes, second_bytes)

    def test_repeated_builds_list_members_in_the_same_order(self) -> None:
        first_dist = self.root / "dist-first"
        second_dist = self.root / "dist-second"
        package_skills.package_all(self.skill_names, dist_dir=first_dist)
        package_skills.package_all(self.skill_names, dist_dir=second_dist)
        for name in self.skill_names:
            with zipfile.ZipFile(first_dist / f"{name}.zip") as zf:
                first_names = zf.namelist()
            with zipfile.ZipFile(second_dist / f"{name}.zip") as zf:
                second_names = zf.namelist()
            self.assertEqual(first_names, second_names)


class ExclusionTestCase(_FixtureRepoTestCase):
    def test_cache_files_are_excluded_from_the_archive(self) -> None:
        skill_dir = self.root / self.skill_names[0]
        cache_dir = skill_dir / "__pycache__"
        cache_dir.mkdir(parents=True, exist_ok=True)
        (cache_dir / "leftover.pyc").write_bytes(b"not real bytecode")
        (skill_dir / "references" / ".DS_Store").write_bytes(b"\x00\x01")

        exit_code = package_skills.package_all(self.skill_names, dist_dir=self.dist_dir)
        self.assertEqual(exit_code, 0)
        with zipfile.ZipFile(self.dist_dir / f"{self.skill_names[0]}.zip") as zf:
            names = zf.namelist()
        self.assertFalse(any("__pycache__" in n for n in names))
        self.assertFalse(any(n.endswith(".pyc") for n in names))
        self.assertFalse(any(n.endswith(".DS_Store") for n in names))


class ValidationBeforePackagingTestCase(_FixtureRepoTestCase):
    def test_invalid_skill_is_not_packaged_and_exit_code_is_nonzero(self) -> None:
        skill_dir = self.root / self.skill_names[0]
        (skill_dir / "SKILL.md").unlink()

        exit_code = package_skills.package_all(self.skill_names, dist_dir=self.dist_dir)

        self.assertEqual(exit_code, 1)
        self.assertFalse((self.dist_dir / f"{self.skill_names[0]}.zip").exists())
        # The other, still-valid skill must still be packaged.
        self.assertTrue((self.dist_dir / f"{self.skill_names[1]}.zip").exists())

    def test_valid_skills_are_all_packaged_with_exit_code_zero(self) -> None:
        exit_code = package_skills.package_all(self.skill_names, dist_dir=self.dist_dir)
        self.assertEqual(exit_code, 0)
        for name in self.skill_names:
            self.assertTrue((self.dist_dir / f"{name}.zip").exists())


if __name__ == "__main__":
    unittest.main()
