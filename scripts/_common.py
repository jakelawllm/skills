"""Shared helpers for the repository maintenance scripts.

``sync_shared.py``, ``validate_skills.py`` and ``package_skills.py`` all need
the same notion of "which skills exist", "which files belong to a skill" and
"what does a generated reference copy look like". Keeping that logic in one
place means ``validate_skills.py --check``-equivalent logic and
``sync_shared.py --check`` can never silently drift apart.

Python standard library only.
"""

from __future__ import annotations

import pathlib

REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
SHARED_DIR = REPO_ROOT / "shared"

# The three public, independently installable skill directories. Listed
# explicitly (rather than discovered) because the plan treats these three
# names as fixed; a directory that has not been created yet is simply
# skipped by callers that iterate over ``skill_dirs()``.
SKILL_NAMES = ("formal-legal-voice", "prof-legal-voice", "informal-legal-voice")

# Files that never belong in a distributed skill ZIP even if they happen to
# be sitting inside a skill directory (editor/OS/tool artefacts).
EXCLUDED_DIR_NAMES = {"__pycache__", ".git", ".mypy_cache", ".pytest_cache"}
EXCLUDED_FILE_NAMES = {".DS_Store"}
EXCLUDED_FILE_SUFFIXES = (".pyc", ".pyo")

# File suffixes treated as text for encoding/whitespace/link/language checks.
TEXT_SUFFIXES = {".md", ".markdown", ".txt", ".yml", ".yaml", ".json"}


def repo_root() -> pathlib.Path:
    """Return the repository root (the parent of this ``scripts/`` directory)."""
    return REPO_ROOT


def rel(path: pathlib.Path) -> str:
    """Repo-relative path, forward-slash separated, for stable reporting."""
    try:
        return path.resolve().relative_to(REPO_ROOT).as_posix()
    except ValueError:
        # Path is not inside the repo root; fall back to its plain string form
        # rather than raising, so callers can still report a useful message.
        return path.as_posix()


def shared_files() -> list[pathlib.Path]:
    """Canonical shared source files, sorted for determinism.

    Returns an empty list if ``shared/`` does not exist yet rather than
    raising, since callers must treat that as a reportable condition, not a
    crash.
    """
    if not SHARED_DIR.is_dir():
        return []
    return sorted(p for p in SHARED_DIR.iterdir() if p.is_file())


def skill_dirs() -> list[pathlib.Path]:
    """The skill directories that currently exist on disk, in fixed order."""
    return [REPO_ROOT / name for name in SKILL_NAMES if (REPO_ROOT / name).is_dir()]


def generated_header(filename: str) -> str:
    """The exact header line prefixed to every generated reference copy."""
    return f"<!-- Generated from shared/{filename}. Do not edit this copy directly. -->\n"


def expected_generated_content(shared_file: pathlib.Path) -> str:
    """The exact bytes a synced copy of ``shared_file`` must contain."""
    header = generated_header(shared_file.name)
    source = shared_file.read_text(encoding="utf-8")
    return header + "\n" + source


def generated_copy_path(skill_dir: pathlib.Path, shared_file: pathlib.Path) -> pathlib.Path:
    """Where the synced copy of ``shared_file`` lives inside ``skill_dir``."""
    return skill_dir / "references" / shared_file.name


def check_generated_copies() -> list[dict]:
    """Compare every skill's generated reference copies against ``shared/``.

    Returns a list of problem dicts, each with ``status`` ("missing" or
    "stale"), ``shared_file`` (repo-relative) and ``target`` (repo-relative).
    An empty list means every copy is current. Never writes anything; this is
    the logic shared by ``sync_shared.py --check`` and
    ``validate_skills.py``.
    """
    problems: list[dict] = []
    for shared_file in shared_files():
        expected = expected_generated_content(shared_file)
        for skill_dir in skill_dirs():
            target = generated_copy_path(skill_dir, shared_file)
            if not target.is_file():
                problems.append(
                    {
                        "status": "missing",
                        "shared_file": rel(shared_file),
                        "target": rel(target),
                    }
                )
                continue
            try:
                actual = target.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                problems.append(
                    {
                        "status": "stale",
                        "shared_file": rel(shared_file),
                        "target": rel(target),
                    }
                )
                continue
            if actual != expected:
                problems.append(
                    {
                        "status": "stale",
                        "shared_file": rel(shared_file),
                        "target": rel(target),
                    }
                )
    return problems


def iter_distributable_files(skill_dir: pathlib.Path) -> list[pathlib.Path]:
    """Every file that should ship inside ``skill_dir``'s packaged ZIP.

    Deterministically ordered by repo-relative, forward-slash path so
    packaging and validation always see files in the same order.
    """
    if not skill_dir.is_dir():
        return []
    results = []
    for path in skill_dir.rglob("*"):
        if path.is_dir():
            continue
        relative_parts = path.relative_to(skill_dir).parts
        if any(part in EXCLUDED_DIR_NAMES for part in relative_parts[:-1]):
            continue
        if path.name in EXCLUDED_FILE_NAMES:
            continue
        if path.suffix in EXCLUDED_FILE_SUFFIXES:
            continue
        results.append(path)
    return sorted(results, key=lambda p: p.relative_to(skill_dir).as_posix())
