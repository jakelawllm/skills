"""Shared fixtures for the scripts test suite.

Not a test module itself (no ``TestCase`` classes, and the leading
underscore keeps ``unittest discover``'s default ``test*.py`` pattern from
picking it up). Import this after adding ``scripts/`` to ``sys.path``, since
it imports ``_common``.
"""

from __future__ import annotations

import pathlib

import _common as common

FIXTURE_SKILL_NAMES = ("alpha-legal-voice", "beta-legal-voice")


def _frontmatter(name: str, description: str) -> str:
    return f"---\nname: {name}\ndescription: {description}\n---\n\n"


def build_minimal_repo(root: pathlib.Path, skill_names=FIXTURE_SKILL_NAMES) -> None:
    """Build a small, fully valid repository layout under ``root``.

    Mirrors the real repository's shape: ``shared/`` canonical files, one
    directory per skill with a passing ``SKILL.md``, ``examples.md`` and
    ``references/`` (including references already synced from ``shared/``).
    Every check in ``validate_skills.py`` should pass against the result
    unmodified; individual tests mutate a copy of it to introduce exactly
    one failure at a time.
    """
    shared_dir = root / "shared"
    shared_dir.mkdir(parents=True, exist_ok=True)
    (shared_dir / "legal-accuracy-and-court-rules.md").write_text(
        "# Legal accuracy and court rules\n\nA dated summary reference for testing.\n",
        encoding="utf-8",
    )
    (shared_dir / "style-audit.md").write_text(
        "# Style audit\n\nCheck for common drafting defects.\n",
        encoding="utf-8",
    )

    for index, name in enumerate(skill_names):
        skill_dir = root / name
        (skill_dir / "references").mkdir(parents=True, exist_ok=True)
        description = f"Drafts and revises test register {index} writing for a fixture skill."
        skill_md = _frontmatter(name, description) + (
            f"# {name}\n\n"
            "A short, compliant skill body with no banned language or placeholders.\n\n"
            "See the [register guide](references/register-guide.md), "
            "[legal accuracy and court rules](references/legal-accuracy-and-court-rules.md), "
            "[style audit](references/style-audit.md) and "
            "[examples](examples.md) for more detail.\n"
        )
        (skill_dir / "SKILL.md").write_text(skill_md, encoding="utf-8")
        (skill_dir / "examples.md").write_text(
            "# Examples\n\n"
            "## Scenario\n\n"
            "A fictional scenario with complete, non-placeholder facts.\n\n"
            "## Poor version\n\nAn example of a weaker draft.\n\n"
            "## Improved version\n\nAn example of the improved draft.\n\n"
            "## Why the improved version works\n\nBecause it is accurate and direct.\n",
            encoding="utf-8",
        )
        (skill_dir / "references" / "register-guide.md").write_text(
            f"# {name} register guide\n\nShort patterns for this register.\n",
            encoding="utf-8",
        )

    sync_generated_copies(root, skill_names)


def sync_generated_copies(root: pathlib.Path, skill_names=FIXTURE_SKILL_NAMES) -> None:
    """Write generated reference copies matching what ``sync_shared.py`` would write."""
    shared_dir = root / "shared"
    for shared_file in sorted(p for p in shared_dir.iterdir() if p.is_file()):
        header = common.generated_header(shared_file.name)
        content = header + "\n" + shared_file.read_text(encoding="utf-8")
        for name in skill_names:
            target = root / name / "references" / shared_file.name
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(content, encoding="utf-8")


def patch_common_repo(test_case, root: pathlib.Path, skill_names=FIXTURE_SKILL_NAMES) -> None:
    """Point ``_common``'s module-level repo paths at a temporary fixture repo.

    Restores the original values via ``test_case.addCleanup``, so a test's
    fixture never leaks into another test or into a real-repository check
    that runs later in the same process.
    """
    original_root = common.REPO_ROOT
    original_shared = common.SHARED_DIR
    original_names = common.SKILL_NAMES

    resolved_root = root.resolve()
    common.REPO_ROOT = resolved_root
    common.SHARED_DIR = resolved_root / "shared"
    common.SKILL_NAMES = tuple(skill_names)

    def _restore() -> None:
        common.REPO_ROOT = original_root
        common.SHARED_DIR = original_shared
        common.SKILL_NAMES = original_names

    test_case.addCleanup(_restore)
