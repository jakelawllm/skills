#!/usr/bin/env python3
"""Sync ``shared/`` canonical files into every skill's ``references/`` directory.

Each canonical file in ``shared/`` (currently
``legal-accuracy-and-court-rules.md`` and ``style-audit.md``) is copied into
``<skill>/references/<filename>`` for every skill directory that exists, with
a generated-file header prepended so nobody edits the copy directly:

    <!-- Generated from shared/<filename>. Do not edit this copy directly. -->

The generated copies are committed to the repository so that a single skill
folder, copied or zipped in isolation, is still self-contained.

Python standard library only.

Usage:
    python scripts/sync_shared.py            Write/update every generated copy.
    python scripts/sync_shared.py --check     Report stale or missing copies,
                                               exit non-zero, and write nothing.
"""

from __future__ import annotations

import argparse
import sys

import _common as common


def sync(*, check: bool) -> int:
    """Run the sync. Returns a process exit code (0 success, 1 problems found)."""
    shared_files = common.shared_files()
    if not shared_files:
        print(f"No canonical files found in {common.rel(common.SHARED_DIR)}/.", file=sys.stderr)
        return 1

    skill_dirs = common.skill_dirs()
    if not skill_dirs:
        print("No skill directories found; nothing to sync.", file=sys.stderr)
        return 1

    if check:
        problems = common.check_generated_copies()
        if not problems:
            print("All generated reference copies are current.")
            return 0
        for problem in problems:
            print(
                f"{problem['target']}: {problem['status']} copy of {problem['shared_file']}"
            )
        print(f"\n{len(problems)} stale or missing generated file(s).", file=sys.stderr)
        return 1

    written = 0
    for shared_file in shared_files:
        expected = common.expected_generated_content(shared_file)
        for skill_dir in skill_dirs:
            target = common.generated_copy_path(skill_dir, shared_file)
            target.parent.mkdir(parents=True, exist_ok=True)
            if target.is_file() and target.read_text(encoding="utf-8") == expected:
                continue
            target.write_text(expected, encoding="utf-8")
            written += 1
            print(f"wrote {common.rel(target)}")

    if written == 0:
        print("All generated reference copies were already current.")
    else:
        print(f"Updated {written} generated reference file(s).")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        action="store_true",
        help="report stale or missing generated copies without modifying anything",
    )
    args = parser.parse_args(argv)
    return sync(check=args.check)


if __name__ == "__main__":
    raise SystemExit(main())
