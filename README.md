# academic-writing-skill

Claude Code skills and an agent for writing and revising research papers (NLP, ML systems, edge-AI hardware), built for a LaTeX paper cloned from Overleaf inside a research code repository.

- `.claude/skills/academic-writing/`: the main skill (Method and Results guidance, terminology, register, LaTeX and repository rules), the author's voice profile, a 20-paper style corpus with notes, worked examples, and `scripts/check.py`.
- `.claude/skills/humanizer/`: removes AI-writing patterns; has an academic mode.
- `.claude/agents/academic-writer.md`: runs the full pipeline (read paper and code, check, revise, humanize, verify, report).

## Install

**User-level (recommended).** Available in every repository, and nothing is added to the research repo's git history. Tell Claude Code:

> Clone https://github.com/raeesiarya/academic-writing-skill into a temporary folder and copy its `.claude/skills/academic-writing`, `.claude/skills/humanizer`, and `.claude/agents/academic-writer.md` into `~/.claude/skills/` and `~/.claude/agents/`. Overwrite older copies of these three, and leave everything else in `~/.claude` alone.

Or run it yourself:

```bash
git clone --depth 1 https://github.com/raeesiarya/academic-writing-skill /tmp/aws
mkdir -p ~/.claude/skills ~/.claude/agents
rm -rf ~/.claude/skills/academic-writing ~/.claude/skills/humanizer
cp -R /tmp/aws/.claude/skills/academic-writing /tmp/aws/.claude/skills/humanizer ~/.claude/skills/
cp /tmp/aws/.claude/agents/academic-writer.md ~/.claude/agents/
rm -rf /tmp/aws
```

**Project-level.** Same commands with `<repo>/.claude/` instead of `~/.claude/`. The skill then travels with the repository, but the corpus (about 66 MB of PDFs) is committed with it.

Restart Claude Code (or start a new session) after installing.

## Update

Run the same install again. The copies are not linked to this repository.

## Check the script

```bash
python3 ~/.claude/skills/academic-writing/scripts/check.py ~/.claude/skills/academic-writing/tests/fixtures
```

It should report about 25 candidates in the test fixture.
