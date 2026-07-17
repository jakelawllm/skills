#!/usr/bin/env python3
"""Static validation for the three distributed legal-writing skills.

Checks, per skill directory (``formal-legal-voice``, ``prof-legal-voice``,
``informal-legal-voice``):

- the directory exists and contains ``SKILL.md``, ``examples.md`` and the
  three required reference files;
- ``SKILL.md`` frontmatter exists and is well formed, ``name`` matches the
  directory and is lowercase-hyphen, and ``description`` is present, at most
  1024 characters, and distinct across the three skills;
- ``SKILL.md`` is under 500 lines;
- every markdown link in a distributed file resolves to an existing local
  file;
- generated ``references/`` copies of the ``shared/`` canonical files are
  current (same logic as ``sync_shared.py --check``);
- no distributed file contains ``StoryScope``, ``93.2%``, ``93.9%`` or
  "harder to detect";
- no ``examples.md`` contains a placeholder such as ``[date]``, ``[name]``,
  ``2025-xx-xx``, ``xx/xx/xxxx`` or "insert name";
- no ``SKILL.md`` contains the inaccurate phrase "editing is limited to
  spelling and grammar", or a universal (unscoped) statement that an expert
  report requires prior leave of the Court;
- every distributed file is valid UTF-8 with no trailing whitespace on any
  line; and
- every distributed file resolves inside its skill directory, so the skill
  can be packaged without a path escaping outside it.

Python standard library only. Prints one line per failure in the form
``<repo-relative-path>:<line>: <message>`` (or ``<path>: <message>`` where a
single line is not applicable) and exits non-zero if any check fails.

Usage:
    python scripts/validate_skills.py
"""

from __future__ import annotations

import re
import sys
from dataclasses import dataclass

import _common as common

REQUIRED_REFERENCE_FILES = (
    "legal-accuracy-and-court-rules.md",
    "register-guide.md",
    "style-audit.md",
)
MAX_SKILL_MD_LINES = 500
MAX_DESCRIPTION_LENGTH = 1024
NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")

# (c) placeholders that must never appear in a finished example.
PLACEHOLDER_PATTERNS = ("[date]", "[name]", "2025-xx-xx", "xx/xx/xxxx", "insert name")

# (b) language that must never appear in anything a skill directory ships.
BANNED_ANYWHERE = ("storyscope", "93.2%", "93.9%", "harder to detect")

# (a) the inaccurate blanket phrase about witness-material editing.
INACCURATE_WITNESS_EDIT_PHRASE = "editing is limited to spelling and grammar"

# (a) a universal, unscoped "expert report ... requires prior leave" statement.
# Flagged unless the same sentence ties the requirement to a specific court,
# proceeding or confirmation step (i.e. reads as conditional, not universal).
_EXPERT_REPORT_RE = re.compile(r"expert report", re.IGNORECASE)
_PRIOR_LEAVE_RE = re.compile(r"requires?\s+prior\s+leave", re.IGNORECASE)
_EXPERT_REPORT_SCOPE_MARKERS = (
    "unless",
    "only if",
    "only where",
    "where the",
    "applicable court",
    "confirms",
    "confirm ",
    "check the",
    "depending on",
    "specific court",
    "terms the user",
)

_LINK_RE = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
_EXTERNAL_SCHEMES = ("http://", "https://", "mailto:", "tel:")


@dataclass
class Issue:
    path: str
    message: str
    line: int | None = None

    def __str__(self) -> str:
        location = self.path if self.line is None else f"{self.path}:{self.line}"
        return f"{location}: {self.message}"


def parse_frontmatter(text: str, relpath: str) -> tuple[dict, list[Issue]]:
    """Parse the simple ``key: value`` YAML-like frontmatter used by these skills.

    Not a general YAML parser: it only understands a flat block of
    ``key: value`` lines between two ``---`` delimiters, which is the whole of
    what this repository's ``SKILL.md`` frontmatter uses. Anything else is
    reported as malformed rather than silently accepted.
    """
    issues: list[Issue] = []
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        issues.append(Issue(relpath, "frontmatter must start with a '---' line", 1))
        return {}, issues

    end_index = None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            end_index = i
            break
    if end_index is None:
        issues.append(Issue(relpath, "frontmatter is missing a closing '---' line", 1))
        return {}, issues

    data: dict[str, str] = {}
    for i in range(1, end_index):
        line = lines[i]
        if not line.strip():
            continue
        if ":" not in line:
            issues.append(Issue(relpath, f"frontmatter line is not 'key: value': {line!r}", i + 1))
            continue
        key, _, value = line.partition(":")
        key = key.strip()
        value = value.strip()
        if not key:
            issues.append(Issue(relpath, f"frontmatter line has an empty key: {line!r}", i + 1))
            continue
        if key in data:
            issues.append(Issue(relpath, f"frontmatter key '{key}' is duplicated", i + 1))
        data[key] = value
    return data, issues


def _locate_line(text: str, sentence: str) -> int | None:
    """Best-effort line number for a sentence found after whitespace normalisation."""
    words = sentence.split()[:6]
    if not words:
        return None
    for i, line in enumerate(text.splitlines(), start=1):
        if all(word in line for word in words):
            return i
    return None


def validate_expert_report_scope(text: str, relpath: str) -> list[Issue]:
    issues = []
    normalised = re.sub(r"\s+", " ", text)
    sentences = re.split(r"(?<=[.!?])\s+", normalised)
    for sentence in sentences:
        if _EXPERT_REPORT_RE.search(sentence) and _PRIOR_LEAVE_RE.search(sentence):
            lowered = sentence.lower()
            if not any(marker in lowered for marker in _EXPERT_REPORT_SCOPE_MARKERS):
                line = _locate_line(text, sentence)
                issues.append(
                    Issue(
                        relpath,
                        "states a universal (unscoped) expert-report prior-leave "
                        "requirement; must be conditional on the applicable court "
                        "and proceeding",
                        line,
                    )
                )
    return issues


def validate_skill_md(skill_md, skill_name: str) -> tuple[list[Issue], dict]:
    """Validate one ``SKILL.md``. Returns (issues, frontmatter dict)."""
    issues: list[Issue] = []
    relpath = common.rel(skill_md)
    try:
        text = skill_md.read_text(encoding="utf-8")
    except UnicodeDecodeError as exc:
        return [Issue(relpath, f"file is not valid UTF-8: {exc}")], {}

    line_count = len(text.splitlines())
    if line_count > MAX_SKILL_MD_LINES:
        issues.append(
            Issue(relpath, f"SKILL.md has {line_count} lines, exceeds the {MAX_SKILL_MD_LINES}-line limit")
        )

    frontmatter, fm_issues = parse_frontmatter(text, relpath)
    issues.extend(fm_issues)

    name = frontmatter.get("name")
    if not name:
        issues.append(Issue(relpath, "frontmatter is missing a 'name' field"))
    else:
        if name != skill_name:
            issues.append(
                Issue(relpath, f"frontmatter name '{name}' does not match directory name '{skill_name}'")
            )
        if not NAME_RE.match(name):
            issues.append(
                Issue(relpath, f"name '{name}' must use lowercase letters, digits and hyphens only")
            )

    description = frontmatter.get("description")
    if not description:
        issues.append(Issue(relpath, "frontmatter is missing a 'description' field"))
    elif len(description) > MAX_DESCRIPTION_LENGTH:
        issues.append(
            Issue(
                relpath,
                f"description is {len(description)} characters, exceeds the "
                f"{MAX_DESCRIPTION_LENGTH}-character limit",
            )
        )

    for i, line in enumerate(text.splitlines(), start=1):
        if INACCURATE_WITNESS_EDIT_PHRASE in line.lower():
            issues.append(
                Issue(relpath, f"contains the inaccurate phrase '{INACCURATE_WITNESS_EDIT_PHRASE}'", i)
            )

    issues.extend(validate_expert_report_scope(text, relpath))

    return issues, frontmatter


def validate_placeholders(examples_md) -> list[Issue]:
    issues: list[Issue] = []
    relpath = common.rel(examples_md)
    try:
        text = examples_md.read_text(encoding="utf-8")
    except UnicodeDecodeError as exc:
        return [Issue(relpath, f"file is not valid UTF-8: {exc}")]
    for i, line in enumerate(text.splitlines(), start=1):
        lowered = line.lower()
        for placeholder in PLACEHOLDER_PATTERNS:
            if placeholder in lowered:
                issues.append(Issue(relpath, f"contains placeholder text '{placeholder}'", i))
    return issues


def validate_banned_language(path) -> list[Issue]:
    issues: list[Issue] = []
    if path.suffix not in common.TEXT_SUFFIXES:
        return issues
    relpath = common.rel(path)
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return issues
    for i, line in enumerate(text.splitlines(), start=1):
        lowered = line.lower()
        for term in BANNED_ANYWHERE:
            if term in lowered:
                issues.append(Issue(relpath, f"contains prohibited language matching '{term}'", i))
    return issues


def validate_encoding_and_whitespace(path) -> list[Issue]:
    issues: list[Issue] = []
    if path.suffix not in common.TEXT_SUFFIXES:
        return issues
    relpath = common.rel(path)
    raw = path.read_bytes()
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        return [Issue(relpath, f"file is not valid UTF-8: {exc}")]
    for i, line in enumerate(text.splitlines(), start=1):
        if line != line.rstrip():
            issues.append(Issue(relpath, "line has trailing whitespace", i))
    return issues


def _is_external_or_anchor(target: str) -> bool:
    if not target or target.startswith("#"):
        return True
    lowered = target.lower()
    return any(lowered.startswith(scheme) for scheme in _EXTERNAL_SCHEMES)


def validate_markdown_links(path) -> list[Issue]:
    issues: list[Issue] = []
    if path.suffix not in (".md", ".markdown"):
        return issues
    relpath = common.rel(path)
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return issues
    for i, line in enumerate(text.splitlines(), start=1):
        for match in _LINK_RE.finditer(line):
            target = match.group(1).strip()
            if not target:
                continue
            # Drop an optional Markdown link title: [text](path "title")
            target = target.split(" ", 1)[0].strip('"').strip("'")
            if _is_external_or_anchor(target):
                continue
            target = target.split("#", 1)[0]
            if not target:
                continue
            target_path = (path.parent / target).resolve()
            if not target_path.is_file():
                issues.append(Issue(relpath, f"link target does not exist: '{match.group(1).strip()}'", i))
    return issues


def validate_packaging_containment(skill_dir) -> list[Issue]:
    issues: list[Issue] = []
    skill_dir_resolved = skill_dir.resolve()
    for path in common.iter_distributable_files(skill_dir):
        resolved = path.resolve()
        try:
            resolved.relative_to(skill_dir_resolved)
        except ValueError:
            issues.append(
                Issue(common.rel(path), "resolves outside its skill directory and cannot be packaged safely")
            )
    return issues


def validate_generated_copies() -> list[Issue]:
    issues = []
    for problem in common.check_generated_copies():
        issues.append(
            Issue(
                problem["target"],
                f"generated reference copy is {problem['status']} relative to {problem['shared_file']}",
            )
        )
    return issues


def validate_skill(skill_dir) -> tuple[list[Issue], dict]:
    """Validate one skill directory. Returns (issues, SKILL.md frontmatter dict)."""
    issues: list[Issue] = []
    skill_name = skill_dir.name

    if not skill_dir.is_dir():
        return [Issue(common.rel(skill_dir), "skill directory does not exist")], {}

    skill_md = skill_dir / "SKILL.md"
    examples_md = skill_dir / "examples.md"
    references_dir = skill_dir / "references"

    frontmatter: dict = {}

    if not skill_md.is_file():
        issues.append(Issue(common.rel(skill_md), "SKILL.md is missing"))
    else:
        skill_md_issues, frontmatter = validate_skill_md(skill_md, skill_name)
        issues.extend(skill_md_issues)

    if not examples_md.is_file():
        issues.append(Issue(common.rel(examples_md), "examples.md is missing"))
    else:
        issues.extend(validate_placeholders(examples_md))

    for ref_name in REQUIRED_REFERENCE_FILES:
        ref_path = references_dir / ref_name
        if not ref_path.is_file():
            issues.append(Issue(common.rel(ref_path), "required reference file is missing"))

    for path in common.iter_distributable_files(skill_dir):
        issues.extend(validate_encoding_and_whitespace(path))
        issues.extend(validate_banned_language(path))
        issues.extend(validate_markdown_links(path))

    issues.extend(validate_packaging_containment(skill_dir))

    return issues, frontmatter


def validate_all() -> list[Issue]:
    """Validate every skill named in ``common.SKILL_NAMES`` plus cross-skill checks."""
    issues: list[Issue] = []
    descriptions: dict[str, list[str]] = {}

    for name in common.SKILL_NAMES:
        skill_dir = common.repo_root() / name
        skill_issues, frontmatter = validate_skill(skill_dir)
        issues.extend(skill_issues)
        description = frontmatter.get("description")
        if description:
            descriptions.setdefault(description, []).append(name)

    for description, names in descriptions.items():
        if len(names) > 1:
            for name in names:
                others = [n for n in names if n != name]
                issues.append(
                    Issue(
                        f"{name}/SKILL.md",
                        f"description is not distinct; identical to {', '.join(others)}",
                    )
                )

    issues.extend(validate_generated_copies())

    return issues


def main(argv: list[str] | None = None) -> int:
    issues = validate_all()
    for issue in issues:
        print(str(issue))
    if issues:
        print(f"\n{len(issues)} validation issue(s) found.", file=sys.stderr)
        return 1
    print("All skill validation checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
