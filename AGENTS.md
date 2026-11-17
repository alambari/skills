# AGENTS.md

Instructions for coding agents that work on this repository. `CLAUDE.md` imports this file, so there is one source.

## What this is

A collection of skills for coding agents in the Agent Skills format: one folder per skill, each with a `SKILL.md` (front matter `name` and `description`, then the instructions), optional `references/`, `templates/` and `scripts/`. The README lists the skills for users.

## Layout

```text
beauty-readme/           the skill: SKILL.md, references/, templates/, scripts/audit_readme.py
assets/readme/           images used by this repository's README
README.md  LICENSE
```

## Commands

```sh
python3 beauty-readme/scripts/audit_readme.py README.md --host github    # must print 0 errors before a commit that touches the README
python3 -c "import ast,sys; ast.parse(open('beauty-readme/scripts/audit_readme.py').read())"   # the script still parses
```

There is no build step and no test runner. To check the audit script after a change, run it on a README you broke on purpose (a dead link, an image without alt text, an SVG with `<script>`) and on this repository's own README.

## Rules

- **Agent-neutral.** A skill never names one agent's tools. It asks for actions ("read the file", "run the script") that any agent with file access and a shell can do.
- **Scripts use the Python standard library only**, run on Python 3.8 or later, read files and never change them, and never use the network.
- **A skill's `description` is its trigger**: one or two sentences that say what it does and when to use it. Keep `SKILL.md` to what the agent must do in order; details go to `references/` and are named where they are needed.
- **Facts about a host or a tool come from its documentation.** `beauty-readme/references/hosts.md` says where GitLab's documentation is silent; keep it that way and do not fill gaps from memory.
- **The README follows the skill.** This repository's README is written with `beauty-readme`; every example output in it is real.
- **A new skill** gets its own folder, a row in the README table and, when it has a script, a line under Commands here.
- **Installed copies do not update themselves.** People copy or link the skill folder; say so in release notes when a change matters to them.

## Commits

Short imperative subject, no attribution or co-author lines. Do not push or publish unless the owner asks.
