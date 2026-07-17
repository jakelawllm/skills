# Jakelaw skills

[Agent Skills](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview) maintained by Jakelaw for legal drafting.

## Skills

Three writing skills for lawyers, one for each register. All three write in Australian English, apply the same anti-AI-tell hygiene, and carry the same Supreme Court of NSW Practice Note SC Gen 23 guardrail: permitted work product only, never the content of an affidavit, witness statement, or character reference, and citations verified by a person rather than by AI. They differ in how formal the voice is. Pick the one that matches your reader.

### formal-legal-voice

Formal legal Australian English, for a court, the other side, or another lawyer: letters, written submissions, memos, file notes, and formal advices. Disciplined and direct: open with the point, take a position, cut the throat-clearing.

### prof-legal-voice

Professional Australian English, for client-facing writing: client emails and letters, updates, explaining a development or delivering news. Warmer than the formal register, it tells the client what a development means for them and sets them at ease while staying professional and honest.

### informal-legal-voice

Informal Australian English, for a client you have an easy ongoing relationship with, or one who prefers plain talk: quick updates and plain-language explanations. The softest register, conversational and approachable, still accurate and honest.

Each skill is self-contained. Install the one that fits how you write, or all three and let Claude choose by context.

## Installation

An Agent Skill is a `SKILL.md` inside a folder named for the skill. Claude Code loads it from the filesystem; the Claude desktop app and claude.ai take it as a ZIP upload. The steps are the same for each skill; substitute the folder name you want (`formal-legal-voice`, `prof-legal-voice`, or `informal-legal-voice`).

### Claude Code

Clone the repo, then copy the skills you want. For your own use across every project:

```bash
git clone https://github.com/jakelawllm/skills.git
mkdir -p ~/.claude/skills
cp -r skills/formal-legal-voice skills/prof-legal-voice skills/informal-legal-voice ~/.claude/skills/
```

To install into one project instead, shared with the team through that project's git, copy the same folders into `/path/to/your/project/.claude/skills/`.

Confirm Claude Code can see them:

```bash
ls ~/.claude/skills/*/SKILL.md        # personal
ls .claude/skills/*/SKILL.md          # project
```

### Claude desktop app and claude.ai

Custom skills are available on the Free, Pro, Max, Team, and Enterprise plans. First enable code execution, then upload each skill as a ZIP.

1. Turn on code execution.
   - Free, Pro, or Max: **Settings > Capabilities**, then enable **Code execution and file creation**.
   - Team or Enterprise: **Organization settings > Skills**, then enable both **Code execution and file creation** and **Skills**.
2. Build a ZIP for each skill you want. The archive must contain the skill folder with `SKILL.md` inside it (the folder name has to match the skill name):

   ```bash
   git clone https://github.com/jakelawllm/skills.git
   cd skills
   zip -r formal-legal-voice.zip formal-legal-voice
   ```

   Repeat for `prof-legal-voice` and `informal-legal-voice`. If you would rather not use the command line, download this repo as a ZIP from GitHub, then re-zip the folder you want on its own.
3. In Claude, go to **Customize > Skills**, click the **+** button, choose **+ Create skill**, then **Upload a skill**.
4. Upload the ZIP.

Menu names reflect the current Claude interface and may shift as it updates.

## Usage

Skills are model-invoked. When you ask Claude to draft or tighten a letter, email, advice, memo, or submission, or to strip an AI tone out of legal writing, it reads each skill's `description`, matches the register to the task, and applies it. You do not need to name the skill, though you can ask for one directly ("use prof-legal-voice"). Each skill is self-contained and does not depend on any other being installed.

Verification stays with you. Any citation a skill helps you draft must be checked against the primary source before you rely on it. Under SC Gen 23 that check is a professional obligation and cannot be discharged by AI.

## Licence

MIT. See [LICENSE](LICENSE).
