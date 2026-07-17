#!/usr/bin/env python3
"""Package each skill directory into a reproducible ZIP under ``dist/``.

For every skill in ``_common.SKILL_NAMES`` that exists on disk, validates the
skill (see ``validate_skills.validate_skill``) and, if it passes, writes
``dist/<skill-name>.zip`` with the skill directory itself as the ZIP root
(so extracting the archive produces ``<skill-name>/SKILL.md`` and so on).
Caches, OS/editor artefacts and repo-only files are excluded (the same
exclusion list used by validation, via ``_common.iter_distributable_files``).

Files are added in a fixed, sorted order and every ``ZipInfo`` gets a fixed
timestamp and permission bits, so re-running the script over unchanged
sources produces byte-identical archives.

A skill that fails validation is not packaged; its failures are printed and
the script exits non-zero, leaving any already-written archives for other
skills in place.

Python standard library only.

Usage:
    python scripts/package_skills.py
"""

from __future__ import annotations

import sys
import zipfile
from pathlib import Path

import _common as common
import validate_skills

DIST_DIR_NAME = "dist"

# Fixed modification time for every archive member, so two builds from
# identical sources produce byte-identical ZIPs regardless of when or on
# which machine they were built.
_STABLE_DATE_TIME = (2020, 1, 1, 0, 0, 0)
_STABLE_EXTERNAL_ATTR = 0o644 << 16


def build_archive(skill_dir: Path, dist_dir: Path) -> Path:
    skill_name = skill_dir.name
    archive_path = dist_dir / f"{skill_name}.zip"
    dist_dir.mkdir(parents=True, exist_ok=True)

    files = common.iter_distributable_files(skill_dir)
    with zipfile.ZipFile(archive_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for path in files:
            arcname = f"{skill_name}/{path.relative_to(skill_dir).as_posix()}"
            info = zipfile.ZipInfo(arcname, date_time=_STABLE_DATE_TIME)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = _STABLE_EXTERNAL_ATTR
            zf.writestr(info, path.read_bytes())
    return archive_path


def package_all(skill_names=common.SKILL_NAMES, dist_dir: Path | None = None) -> int:
    dist_dir = dist_dir if dist_dir is not None else common.repo_root() / DIST_DIR_NAME
    overall_ok = True

    for name in skill_names:
        skill_dir = common.repo_root() / name
        issues, _ = validate_skills.validate_skill(skill_dir)
        if issues:
            overall_ok = False
            print(f"Skipping {name}: failed validation.", file=sys.stderr)
            for issue in issues:
                print(f"  {issue}", file=sys.stderr)
            continue
        archive_path = build_archive(skill_dir, dist_dir)
        print(f"wrote {common.rel(archive_path)}")

    return 0 if overall_ok else 1


def main(argv: list[str] | None = None) -> int:
    return package_all()


if __name__ == "__main__":
    raise SystemExit(main())
