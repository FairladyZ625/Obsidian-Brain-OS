# AI Install Guide

This file is for coding agents that are asked to install and configure `conversation-mining` for a user.

Repository:

- SSH: `git@github.com:FairladyZ625/conversation-mining.git`
- HTTPS fallback: `https://github.com/FairladyZ625/conversation-mining.git`

## Goal

Set up this repository locally so the user can use:

- the skill entry point in `SKILL.md`
- the CLI entry points:
  - `conversation-mining`
  - `convs`
  - `python3 -m conversation_mining`

## Install Flow

1. Clone the repository to a sensible local tools/workspace directory.
2. If the repository already exists locally, update it instead of creating a duplicate.
3. Read:
   - `README.md`
   - `SKILL.md`
   - `pyproject.toml`
4. Install the Python package in editable mode:

```bash
python3 -m pip install -e .
```

5. If the runtime supports repo-based skill installation, also register this repository as a skill using `SKILL.md`.
6. Verify the CLI:

```bash
conversation-mining --no-open --days 1
```

7. Report back:
   - local repository path
   - whether skill installation succeeded
   - whether CLI installation succeeded
   - where the generated viewer was written

## Constraints

- Keep all data local on the machine.
- Do not upload exported conversations anywhere.
- Do not publish any private conversation data.
- If SSH clone fails, retry with the HTTPS URL.

## What This Tool Reads

- Claude Code local state under `{{CLAUDE_HOME}}`
- Codex local state under `{{CODEX_HOME}}`
- Antigravity local state under `{{ANTIGRAVITY_PATH}}`
- optional AG brain artifacts under `{{ANTIGRAVITY_BRAIN_PATH}}`

## Expected Output Location

By default:

```text
./exported_conversations/
  conversations.json
  index.html
```
