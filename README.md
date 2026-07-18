# Jakelaw skills

[Agent Skills](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview) maintained by Jakelaw for legal drafting.

## Skills

Three writing skills for lawyers, one for each register. All three write in Australian English, apply the same anti-AI-tell hygiene, and follow the same drafting and revision workflow. They differ in how formal the voice is and who the reader is. Pick the one that matches your reader, or install all three and let Claude choose by context.

| Reader or task | Skill |
|---|---|
| Court, tribunal, opponent, barrister, other solicitor, formal advice, memorandum or file note | `formal-legal-voice` |
| Own client, ordinary advice, risks, costs, serious or complex updates | `prof-legal-voice` |
| Established client, routine low-stakes update, expressly informal or conversational message | `informal-legal-voice` |

An express instruction from you about register normally controls. Claude will follow a request to draft something more formal or more casual unless doing so would change the facts, the legal meaning, or a court-specific obligation, in which case it will say so rather than comply silently.

### formal-legal-voice

Formal legal Australian English, for a court, the other side, or another lawyer: letters, written submissions, memoranda, file notes, and formal advices. Disciplined and direct, with the structure matched to the document's function rather than one advocacy voice applied everywhere.

### prof-legal-voice

Professional Australian English, for client-facing writing: client emails and letters, updates, explaining a development or delivering news. Warmer than the formal register, it tells the client what a development means for them while staying honest about risk. This is the default client register where the audience or occasion is unclear.

### informal-legal-voice

Informal Australian English, for a client you have an easy ongoing relationship with, or one who prefers plain talk: quick updates and plain-language explanations. The softest register, conversational and approachable, still accurate and honest, and not the default for serious or ambiguous client communication.

Each skill is self-contained. Common material, such as the legal-accuracy and style-audit references, is maintained once in the repository and synced into every skill's `references/` folder, so installing or uploading a single skill folder still gives you everything that skill needs.

## Installation

An Agent Skill is a `SKILL.md` inside a folder named for the skill. Claude Code loads it from the filesystem; the Claude desktop app and claude.ai take it as a ZIP upload. The steps are the same for each skill; substitute the folder name you want (`formal-legal-voice`, `prof-legal-voice`, or `informal-legal-voice`).

### Claude Code

Clone the repo, then copy the skills you want. For your own use across every project:

```bash
git clone https://github.com/jakelawllm/skills.git
mkdir -p ~/.claude/skills
cp -r skills/formal-legal-voice skills/prof-legal-voice skills/informal-legal-voice ~/.claude/skills/
```

On Windows, `~/.claude` resolves through your user profile home directory (typically `C:\Users\<you>\.claude`), so the same relative path works.

To install into one project instead, shared with the team through that project's git, copy the same folders into `/path/to/your/project/.claude/skills/`.

Confirm Claude Code can see them:

```bash
ls ~/.claude/skills/*/SKILL.md        # personal
ls .claude/skills/*/SKILL.md          # project
```

### Claude desktop app and claude.ai

Custom skills are available on the Pro, Max, Team, and Enterprise plans, with code execution enabled. First enable code execution, then upload each skill as a ZIP.

1. Turn on code execution.
   - Pro or Max: **Settings > Capabilities**, then enable **Code execution and file creation**.
   - Team or Enterprise: **Organization settings > Skills**, then enable both **Code execution and file creation** and **Skills**.
2. Build a ZIP for each skill you want. The archive must contain the skill folder with `SKILL.md` inside it, as the root of the ZIP (the folder name has to match the skill name):

   ```bash
   git clone https://github.com/jakelawllm/skills.git
   cd skills
   zip -r formal-legal-voice.zip formal-legal-voice
   ```

   Repeat for `prof-legal-voice` and `informal-legal-voice`, or run `python3 scripts/package_skills.py` (see below) to build all three ZIPs at once. If you would rather not use the command line, download this repo as a ZIP from GitHub, then re-zip the folder you want on its own.
3. In Claude, go to **Customize > Skills**, click the **+** button, choose **+ Create skill**, then **Upload a skill**.
4. Upload the ZIP.

On claude.ai each person uploads their own custom skills. There is no central admin distribution across a team or organisation, so each solicitor who wants these skills installs them on their own account.

Menu names reflect the current Claude interface and may shift as it updates. Correct as at 17 July 2026: see the official Claude Help Center article, [Use skills in Claude](https://support.claude.com/en/articles/12512180-use-skills-in-claude), for the current menu path and plan availability rather than treating this README as the source of truth.

## Packaging and validation

The repository builds each skill's ZIP the same way it will be distributed:

```bash
python3 scripts/package_skills.py
```

This writes `dist/formal-legal-voice.zip`, `dist/prof-legal-voice.zip`, and `dist/informal-legal-voice.zip`, each with the skill folder as the ZIP root and every reference and example file the skill needs. Packaging validates the skill first, so a broken skill will not produce a ZIP.

These commands assume `python3`. On Windows, use `python` or the `py` launcher instead.

Before relying on a change, run:

```bash
python3 scripts/sync_shared.py --check
python3 scripts/validate_skills.py
python3 -m unittest discover -s tests -v
```

`sync_shared.py --check` confirms the copies of the shared references inside each skill's `references/` folder are current with the canonical files in `shared/`. `validate_skills.py` checks frontmatter, file structure, and known defects across all three skills. The unit tests cover the sync, validation, and packaging scripts themselves.

## Usage

Skills are model-invoked. When you ask Claude to draft or tighten a letter, email, advice, memo, or submission, or to strip an AI tone out of legal writing, it reads each skill's `description`, matches the register to the task, and applies it. You do not need to name the skill, though you can ask for one directly ("use prof-legal-voice"). Each skill is self-contained and does not depend on any other being installed.

Verification stays with you. Any citation a skill helps you draft must be checked against the primary source before you rely on it, and that check cannot be discharged by AI. Each skill carries a dated summary of the Supreme Court of NSW Practice Note SC Gen 23 as its distributed legal reference. That practice note applies to Supreme Court of NSW proceedings. Confirm the practice note or rule that actually applies to your court and matter before you rely on the summary.

## Licence

MIT. See [LICENSE](LICENSE).
