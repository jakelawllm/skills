"""Tests for scripts/validate_skills.py.

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

import validate_skills  # noqa: E402
import _support  # noqa: E402


class _FixtureRepoTestCase(unittest.TestCase):
    """Base class that builds a fully-valid fixture repo per test."""

    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.root = pathlib.Path(self._tmp.name)
        self.skill_names = _support.FIXTURE_SKILL_NAMES
        _support.patch_common_repo(self, self.root, self.skill_names)
        _support.build_minimal_repo(self.root, self.skill_names)

    def messages(self, issues) -> list[str]:
        return [issue.message for issue in issues]


class BaselineFixtureTestCase(_FixtureRepoTestCase):
    """The fixture builder itself must produce a clean pass, or every other
    test in this file (which mutates one thing at a time) is meaningless."""

    def test_unmodified_fixture_repo_passes_validation(self) -> None:
        issues = validate_skills.validate_all()
        self.assertEqual(issues, [], msg="\n".join(str(i) for i in issues))


class FrontmatterValidationTestCase(_FixtureRepoTestCase):
    def test_missing_closing_delimiter_is_reported(self) -> None:
        skill_md = self.root / self.skill_names[0] / "SKILL.md"
        skill_md.write_text("---\nname: alpha-legal-voice\ndescription: x\n", encoding="utf-8")
        issues, frontmatter = validate_skills.validate_skill(self.root / self.skill_names[0])
        self.assertEqual(frontmatter, {})
        self.assertTrue(any("closing '---'" in m for m in self.messages(issues)))

    def test_missing_opening_delimiter_is_reported(self) -> None:
        skill_md = self.root / self.skill_names[0] / "SKILL.md"
        skill_md.write_text("name: alpha-legal-voice\ndescription: x\n---\n", encoding="utf-8")
        issues, frontmatter = validate_skills.validate_skill(self.root / self.skill_names[0])
        self.assertEqual(frontmatter, {})
        self.assertTrue(any("must start with a '---' line" in m for m in self.messages(issues)))

    def test_malformed_frontmatter_line_without_colon_is_reported(self) -> None:
        skill_md = self.root / self.skill_names[0] / "SKILL.md"
        original = skill_md.read_text(encoding="utf-8")
        broken = original.replace("description:", "not a key value line\ndescription:", 1)
        skill_md.write_text(broken, encoding="utf-8")
        issues, _ = validate_skills.validate_skill(self.root / self.skill_names[0])
        self.assertTrue(any("not 'key: value'" in m for m in self.messages(issues)))

    def test_well_formed_frontmatter_on_unmodified_fixture_has_no_frontmatter_issues(self) -> None:
        issues, frontmatter = validate_skills.validate_skill(self.root / self.skill_names[0])
        self.assertEqual(issues, [])
        self.assertEqual(frontmatter["name"], self.skill_names[0])
        self.assertIn("description", frontmatter)


class NameValidationTestCase(_FixtureRepoTestCase):
    def test_name_does_not_match_directory_is_reported(self) -> None:
        skill_dir = self.root / self.skill_names[0]
        skill_md = skill_dir / "SKILL.md"
        text = skill_md.read_text(encoding="utf-8")
        text = text.replace(f"name: {self.skill_names[0]}", "name: some-other-name", 1)
        skill_md.write_text(text, encoding="utf-8")
        issues, _ = validate_skills.validate_skill(skill_dir)
        self.assertTrue(
            any("does not match directory name" in m for m in self.messages(issues)),
            msg="\n".join(self.messages(issues)),
        )

    def test_uppercase_name_is_reported(self) -> None:
        skill_dir = self.root / self.skill_names[0]
        skill_md = skill_dir / "SKILL.md"
        text = skill_md.read_text(encoding="utf-8")
        text = text.replace(f"name: {self.skill_names[0]}", "name: Alpha-Legal-Voice", 1)
        skill_md.write_text(text, encoding="utf-8")
        issues, _ = validate_skills.validate_skill(skill_dir)
        self.assertTrue(any("lowercase letters, digits and hyphens" in m for m in self.messages(issues)))


class RequiredFileTestCase(_FixtureRepoTestCase):
    def test_missing_examples_md_is_reported(self) -> None:
        skill_dir = self.root / self.skill_names[0]
        (skill_dir / "examples.md").unlink()
        issues, _ = validate_skills.validate_skill(skill_dir)
        self.assertTrue(any("examples.md is missing" in m for m in self.messages(issues)))

    def test_missing_required_reference_file_is_reported(self) -> None:
        skill_dir = self.root / self.skill_names[0]
        (skill_dir / "references" / "register-guide.md").unlink()
        issues, _ = validate_skills.validate_skill(skill_dir)
        self.assertTrue(any("required reference file is missing" in m for m in self.messages(issues)))

    def test_missing_local_markdown_link_target_is_reported(self) -> None:
        skill_dir = self.root / self.skill_names[0]
        skill_md = skill_dir / "SKILL.md"
        text = skill_md.read_text(encoding="utf-8")
        text += "\nSee [a missing file](references/does-not-exist.md).\n"
        skill_md.write_text(text, encoding="utf-8")
        issues, _ = validate_skills.validate_skill(skill_dir)
        self.assertTrue(any("link target does not exist" in m for m in self.messages(issues)))

    def test_external_link_is_not_flagged_as_missing(self) -> None:
        skill_dir = self.root / self.skill_names[0]
        skill_md = skill_dir / "SKILL.md"
        text = skill_md.read_text(encoding="utf-8")
        text += "\nSee the [Practice Note](https://supremecourt.nsw.gov.au/practice-procedure/generative-artificial-intelligence.html).\n"
        skill_md.write_text(text, encoding="utf-8")
        issues, _ = validate_skills.validate_skill(skill_dir)
        self.assertEqual(issues, [])


class GeneratedCopyTestCase(_FixtureRepoTestCase):
    def test_stale_generated_copy_is_reported(self) -> None:
        target = self.root / self.skill_names[0] / "references" / "style-audit.md"
        target.write_text("this no longer matches shared/style-audit.md\n", encoding="utf-8")
        issues = validate_skills.validate_all()
        self.assertTrue(any("generated reference copy is stale" in i.message for i in issues))

    def test_missing_generated_copy_is_reported(self) -> None:
        target = self.root / self.skill_names[0] / "references" / "style-audit.md"
        target.unlink()
        issues = validate_skills.validate_all()
        self.assertTrue(any("generated reference copy is missing" in i.message for i in issues))


class PlaceholderTestCase(_FixtureRepoTestCase):
    def test_bracket_date_placeholder_is_reported(self) -> None:
        examples_md = self.root / self.skill_names[0] / "examples.md"
        examples_md.write_text(
            examples_md.read_text(encoding="utf-8") + "\nA letter dated [date].\n", encoding="utf-8"
        )
        issues, _ = self._validate_skill_and_placeholders()
        self.assertTrue(any("[date]" in m for m in self.messages(issues)))

    def test_xx_xx_xxxx_placeholder_is_reported(self) -> None:
        examples_md = self.root / self.skill_names[0] / "examples.md"
        examples_md.write_text(
            examples_md.read_text(encoding="utf-8") + "\nRespond by xx/xx/xxxx.\n", encoding="utf-8"
        )
        issues, _ = self._validate_skill_and_placeholders()
        self.assertTrue(any("xx/xx/xxxx" in m for m in self.messages(issues)))

    def test_insert_name_placeholder_is_reported(self) -> None:
        examples_md = self.root / self.skill_names[0] / "examples.md"
        examples_md.write_text(
            examples_md.read_text(encoding="utf-8") + "\nDear [Insert Name],\n", encoding="utf-8"
        )
        issues, _ = self._validate_skill_and_placeholders()
        self.assertTrue(any("insert name" in m for m in self.messages(issues)))

    def test_clean_examples_file_has_no_placeholder_issues(self) -> None:
        issues, _ = self._validate_skill_and_placeholders()
        self.assertEqual(issues, [])

    def _validate_skill_and_placeholders(self):
        skill_dir = self.root / self.skill_names[0]
        return validate_skills.validate_skill(skill_dir)


class BannedResearchLanguageTestCase(_FixtureRepoTestCase):
    def test_storyscope_is_reported(self) -> None:
        self._append_to_skill_md("The StoryScope study informs this rule.\n")
        issues, _ = validate_skills.validate_skill(self.root / self.skill_names[0])
        self.assertTrue(any("storyscope" in m for m in self.messages(issues)))

    def test_macro_f1_93_2_percent_is_reported(self) -> None:
        self._append_to_skill_md("Structure alone reached 93.2% macro-F1.\n")
        issues, _ = validate_skills.validate_skill(self.root / self.skill_names[0])
        self.assertTrue(any("93.2%" in m for m in self.messages(issues)))

    def test_93_9_percent_is_reported(self) -> None:
        self._append_to_skill_md("Detection barely moved, at 93.9%.\n")
        issues, _ = validate_skills.validate_skill(self.root / self.skill_names[0])
        self.assertTrue(any("93.9%" in m for m in self.messages(issues)))

    def test_harder_to_detect_is_reported(self) -> None:
        self._append_to_skill_md("Editing vocabulary makes text harder to detect.\n")
        issues, _ = validate_skills.validate_skill(self.root / self.skill_names[0])
        self.assertTrue(any("harder to detect" in m for m in self.messages(issues)))

    def test_clean_skill_md_has_no_banned_language_issues(self) -> None:
        issues, _ = validate_skills.validate_skill(self.root / self.skill_names[0])
        self.assertEqual(issues, [])

    def _append_to_skill_md(self, text: str) -> None:
        skill_md = self.root / self.skill_names[0] / "SKILL.md"
        skill_md.write_text(skill_md.read_text(encoding="utf-8") + "\n" + text, encoding="utf-8")


class WitnessAndExpertReportWordingTestCase(_FixtureRepoTestCase):
    def test_inaccurate_witness_editing_phrase_is_reported(self) -> None:
        self._append_to_skill_md(
            "Those must be the deponent's own words, and editing is limited to spelling and grammar.\n"
        )
        issues, _ = validate_skills.validate_skill(self.root / self.skill_names[0])
        self.assertTrue(
            any("editing is limited to spelling and grammar" in m for m in self.messages(issues))
        )

    def test_universal_expert_report_leave_statement_is_reported(self) -> None:
        self._append_to_skill_md("Expert report content requires prior leave of the Court.\n")
        issues, _ = validate_skills.validate_skill(self.root / self.skill_names[0])
        self.assertTrue(
            any("universal (unscoped) expert-report prior-leave" in m for m in self.messages(issues))
        )

    def test_scoped_expert_report_leave_statement_is_not_reported(self) -> None:
        self._append_to_skill_md(
            "An expert report requires prior leave of the Court only where the applicable "
            "court's rules require it; confirm the terms of leave with the user before drafting.\n"
        )
        issues, _ = validate_skills.validate_skill(self.root / self.skill_names[0])
        self.assertEqual(issues, [])

    def _append_to_skill_md(self, text: str) -> None:
        skill_md = self.root / self.skill_names[0] / "SKILL.md"
        skill_md.write_text(skill_md.read_text(encoding="utf-8") + "\n" + text, encoding="utf-8")


class DescriptionValidationTestCase(_FixtureRepoTestCase):
    def test_overlong_description_is_reported(self) -> None:
        skill_dir = self.root / self.skill_names[0]
        skill_md = skill_dir / "SKILL.md"
        text = skill_md.read_text(encoding="utf-8")
        long_description = "x" * 1025
        text = text.replace(
            "description: Drafts and revises test register 0 writing for a fixture skill.",
            f"description: {long_description}",
            1,
        )
        skill_md.write_text(text, encoding="utf-8")
        issues, _ = validate_skills.validate_skill(skill_dir)
        self.assertTrue(any("exceeds the 1024-character limit" in m for m in self.messages(issues)))

    def test_missing_description_is_reported(self) -> None:
        skill_dir = self.root / self.skill_names[0]
        skill_md = skill_dir / "SKILL.md"
        text = skill_md.read_text(encoding="utf-8")
        text = text.replace("description: Drafts and revises test register 0 writing for a fixture skill.\n", "")
        skill_md.write_text(text, encoding="utf-8")
        issues, _ = validate_skills.validate_skill(skill_dir)
        self.assertTrue(any("missing a 'description' field" in m for m in self.messages(issues)))

    def test_duplicate_descriptions_across_skills_are_reported(self) -> None:
        first_md = self.root / self.skill_names[0] / "SKILL.md"
        second_md = self.root / self.skill_names[1] / "SKILL.md"
        first_text = first_md.read_text(encoding="utf-8")
        second_text = second_md.read_text(encoding="utf-8")
        shared_description = "description: An identical description used by both fixture skills."
        first_text = first_text.replace(
            "description: Drafts and revises test register 0 writing for a fixture skill.",
            shared_description,
            1,
        )
        second_text = second_text.replace(
            "description: Drafts and revises test register 1 writing for a fixture skill.",
            shared_description,
            1,
        )
        first_md.write_text(first_text, encoding="utf-8")
        second_md.write_text(second_text, encoding="utf-8")
        issues = validate_skills.validate_all()
        self.assertTrue(any("description is not distinct" in i.message for i in issues))


class SkillMdLineLimitTestCase(_FixtureRepoTestCase):
    def test_oversized_skill_md_is_reported(self) -> None:
        skill_md = self.root / self.skill_names[0] / "SKILL.md"
        text = skill_md.read_text(encoding="utf-8")
        text += "\n".join(f"Padding line {i}." for i in range(600)) + "\n"
        skill_md.write_text(text, encoding="utf-8")
        issues, _ = validate_skills.validate_skill(self.root / self.skill_names[0])
        self.assertTrue(any("exceeds the 500-line limit" in m for m in self.messages(issues)))


class EncodingAndWhitespaceTestCase(_FixtureRepoTestCase):
    def test_trailing_whitespace_is_reported(self) -> None:
        examples_md = self.root / self.skill_names[0] / "examples.md"
        examples_md.write_text(
            examples_md.read_text(encoding="utf-8") + "This line has trailing space.   \n", encoding="utf-8"
        )
        issues, _ = validate_skills.validate_skill(self.root / self.skill_names[0])
        self.assertTrue(any("trailing whitespace" in m for m in self.messages(issues)))

    def test_non_utf8_file_is_reported(self) -> None:
        examples_md = self.root / self.skill_names[0] / "examples.md"
        examples_md.write_bytes(b"\xff\xfe not valid utf-8")
        issues, _ = validate_skills.validate_skill(self.root / self.skill_names[0])
        self.assertTrue(any("not valid UTF-8" in m for m in self.messages(issues)))


class PackagingContainmentTestCase(_FixtureRepoTestCase):
    def test_no_issues_for_a_clean_skill_directory(self) -> None:
        issues = validate_skills.validate_packaging_containment(self.root / self.skill_names[0])
        self.assertEqual(issues, [])


class RealRepositoryTestCase(unittest.TestCase):
    """Exercises validate_skills.py against the actual repository on disk.

    This is deliberately not run against a fixture: it is the acceptance
    check that the real, currently-committed formal-legal-voice,
    prof-legal-voice and informal-legal-voice directories pass validation.
    If a companion agent has not yet finished writing a required file (for
    example references/register-guide.md or examples.md), this test fails
    with that file's exact path reported by validate_skills rather than
    raising an unrelated error, which is the correct, informative behaviour
    for a validator, not a bug in it.
    """

    def test_real_repository_skills_pass_validation(self) -> None:
        issues = validate_skills.validate_all()
        self.assertEqual(issues, [], msg="\n".join(str(i) for i in issues))


if __name__ == "__main__":
    unittest.main()
