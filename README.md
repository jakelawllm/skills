# Jakelaw skills

[Claude Code Agent Skills](https://code.claude.com/docs/en/skills) maintained by Jakelaw for legal drafting.

## Skills

### human-legal-voice

A single, self-contained writing skill for lawyers. It makes everyday legal work product (letters to the other side, client emails and advices, file notes, memos, chronologies, and written submissions) read as a specific lawyer wrote it rather than a machine: precise, committed, and free of the usual AI tells. It borrows the discipline of NSW Court of Appeal and High Court judgment prose (directness, economy, controlled reporting of a position) and adapts it for ordinary drafting, without imitating the voice of a judge deciding a case.

Three layers are folded into the one file, so nothing else needs to be loaded alongside it:

1. Surface hygiene: vocabulary, punctuation, formatting, and the AI-tell banlists.
2. Structure and stance: be specific, take a position, cut throat-clearing.
3. Judgment-prose discipline, backed by an empirical sample of real NSWCA and HCA judgments in `human-legal-voice/references/`.

It carries a Supreme Court of NSW Practice Note SC Gen 23 guardrail: it is for permitted work product only, never for the content of an affidavit, witness statement, or character reference, and it requires that citations and evidence references be verified by a person, not by AI alone.

## Installation

A skill loads from a `SKILL.md` inside a named directory. Install `human-legal-voice` either for your own use across every project, or inside one project so it is shared with your team through that project's git.

### Personal (available in all your projects)

```bash
git clone https://github.com/jakelawllm/skills.git
mkdir -p ~/.claude/skills
cp -r skills/human-legal-voice ~/.claude/skills/
```

### One project (shared with the team through that repo)

```bash
git clone https://github.com/jakelawllm/skills.git
mkdir -p /path/to/your/project/.claude/skills
cp -r skills/human-legal-voice /path/to/your/project/.claude/skills/
```

Confirm Claude Code can see it:

```bash
ls ~/.claude/skills/*/SKILL.md        # personal
ls .claude/skills/*/SKILL.md          # project
```

## Usage

Skills are model-invoked. When you ask Claude Code to draft or tighten a letter, email, advice, memo, or submission, or to strip an AI tone out of legal writing, it reads the skill's `description`, matches it to the task, and applies it. You do not need to name the skill, though you can ask for it directly ("use human-legal-voice"). The skill is self-contained and does not depend on any other skill being installed.

Verification stays with you. The corpus quotes, and any citation the skill helps you draft, must be checked against the primary source before you rely on them. Under SC Gen 23 that check is a professional obligation and cannot be discharged by AI.

## Licence

MIT. See [LICENSE](LICENSE).
