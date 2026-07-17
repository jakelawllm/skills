# Jakelaw skills

[Agent Skills](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview) maintained by Jakelaw for legal drafting.

## Skills

### human-legal-voice

A single, self-contained writing skill for lawyers. It makes everyday legal work product (letters to the other side, client emails and advices, file notes, memos, chronologies, and written submissions) read as a specific lawyer wrote it rather than a machine: precise, committed, and free of the usual AI tells.

Two layers are folded into the one file, so nothing else needs to be loaded alongside it:

1. Surface hygiene: vocabulary, punctuation, formatting, and the AI-tell banlists.
2. Structure and stance: be specific, take a position, cut throat-clearing, and structure a letter or submission around its point.

It carries a Supreme Court of NSW Practice Note SC Gen 23 guardrail: it is for permitted work product only, never for the content of an affidavit, witness statement, or character reference, and it requires that citations and evidence references be verified by a person, not by AI alone.

## Installation

`human-legal-voice` is an Agent Skill: a `SKILL.md` inside a folder named for the skill. Claude Code loads it from the filesystem; the Claude desktop app and claude.ai take it as a ZIP upload.

### Claude Code

Install for your own use across every project:

```bash
git clone https://github.com/jakelawllm/skills.git
mkdir -p ~/.claude/skills
cp -r skills/human-legal-voice ~/.claude/skills/
```

Or install into one project, shared with the team through that project's git:

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

### Claude desktop app and claude.ai

Custom skills are available on the Free, Pro, Max, Team, and Enterprise plans. First enable code execution, then upload the skill as a ZIP.

1. Turn on code execution.
   - Free, Pro, or Max: **Settings > Capabilities**, then enable **Code execution and file creation**.
   - Team or Enterprise: **Organization settings > Skills**, then enable both **Code execution and file creation** and **Skills**.
2. Build the ZIP. The archive must contain a `human-legal-voice/` folder with `SKILL.md` inside it (the folder name has to match the skill name):

   ```bash
   git clone https://github.com/jakelawllm/skills.git
   cd skills
   zip -r human-legal-voice.zip human-legal-voice
   ```

   If you would rather not use the command line, download this repo as a ZIP from GitHub, then re-zip just the `human-legal-voice` folder on its own.
3. In Claude, go to **Customize > Skills**, click the **+** button, choose **+ Create skill**, then **Upload a skill**.
4. Upload `human-legal-voice.zip`.

Menu names reflect the current Claude interface and may shift as it updates.

## Usage

Skills are model-invoked. When you ask Claude to draft or tighten a letter, email, advice, memo, or submission, or to strip an AI tone out of legal writing, it reads the skill's `description`, matches it to the task, and applies it. You do not need to name the skill, though you can ask for it directly ("use human-legal-voice"). The skill is self-contained and does not depend on any other skill being installed.

Verification stays with you. Any citation the skill helps you draft must be checked against the primary source before you rely on it. Under SC Gen 23 that check is a professional obligation and cannot be discharged by AI.

## Licence

MIT. See [LICENSE](LICENSE).
