# conversation-mining

Export local Claude Code, Codex, and Antigravity conversations into Markdown plus a static HTML viewer.

This project is designed for local forensics and recall:

- backfill or incrementally export conversation history
- browse everything in one viewer
- deep-link into a specific conversation
- copy a conversation reference/prompt for handoff to another AI
- inspect AG task artifacts when Antigravity leaves local files behind

It can be used in two ways:

- as a standalone local script/tool
- as an installable skill via [SKILL.md](./SKILL.md)

## Copy This To Your AI

```text
Install and learn `conversation-mining` from https://github.com/FairladyZ625/conversation-mining . Read README.md, SKILL.md, and AI_INSTALL.md, then install it locally as both a skill and a CLI if supported, and verify with `conversation-mining --no-open --days 1`.
```

## What It Supports

- Claude Code
  - reads local `{{CLAUDE_HOME}}/projects/*/*.jsonl`
  - reconstructs mainline conversations and embedded sub-agent relationships
- Codex
  - reads local `{{CODEX_HOME}}/sessions`, `history.jsonl`, and `state_5.sqlite`
- Antigravity
  - reads local `{{ANTIGRAVITY_PATH}}/.../state.vscdb`
  - extracts trajectory summaries and links AG brain artifacts from `{{ANTIGRAVITY_BRAIN_PATH}}/<uuid>/` when available

## Current Status

This is a pragmatic local-export tool, not an official SDK.

- Claude and Codex usually provide much richer transcript coverage
- Antigravity currently behaves more like task-summary extraction than full raw transcript recovery
- AG artifact linking works when a stable local brain workspace can be matched

## Quick Start

```bash
git clone git@github.com:FairladyZ625/conversation-mining.git
cd conversation-mining
python3 convs.py
```

That will:

1. export recent conversations
2. write JSON + viewer assets into `./exported_conversations`
3. write human-readable Markdown transcripts into a separate transcript directory
4. build `./exported_conversations/index.html`
5. open the viewer on macOS

## Install As a CLI

Editable install:

```bash
python3 -m pip install -e .
conversation-mining --no-open
```

Run as a module:

```bash
python3 -m conversation_mining --days 7
```

With `pipx`:

```bash
pipx install .
conversation-mining --date 2026-03-19
```

## Use As a Skill

This repository also includes [SKILL.md](./SKILL.md).

If your agent supports skill installation from a git repository, install this repo as a skill and then invoke `conversation-mining` for:

- locating a conversation by date or id
- exporting recent history
- opening the local viewer
- generating a handoff reference/prompt

## Common Commands

Export today and build the viewer:

```bash
python3 convs.py --no-open
```

Backfill the last 7 days:

```bash
python3 convs.py --days 7
```

Export a specific date:

```bash
python3 convs.py --date 2026-03-19
```

Write to a custom output directory:

```bash
python3 convs.py --output-dir ~/tmp/conversation-mining-output
```

Write Markdown transcripts to a custom directory:

```bash
python3 convs.py --markdown-dir {{TRANSCRIPT_DIR}}
```

Advanced: export only JSON/Markdown without building the viewer:

```bash
python3 export_all.py --days 7 --output-dir ./exported_conversations
```

## Output Structure

```text
exported_conversations/
  conversations.json
  index.html
```

Separate human-readable transcripts:

```text
{{TRANSCRIPT_DIR}}/
  2026-03-19/
    claude_*.md
    codex_*.md
    ag_*.md
```

## Viewer Features

- source filters: Claude / Codex / AG
- search by title, message text, workspace, tags, and AG artifact metadata
- light / dark mode
- reading modes:
  - mainline
  - mainline + sub-agents
  - forensics
- quick summary cards:
  - final answer
  - key files
  - commands
  - signals
- timeline replay
- bookmarks, tags, collections
- workspace grouping
- related task thread navigation
- AG artifact cards with direct local file links

## Known Limits

- AG is not guaranteed to have a full chat transcript store on disk
- AG artifact coverage is partial and depends on stable local brain workspace ids
- the viewer is optimized for local file usage
- localStorage is used for bookmarks/tags/collections

## Privacy

This tool reads from local application state and local conversation history.

Before publishing exported data, review it carefully:

- conversation content may contain secrets
- copied transcript Markdown can include absolute file paths
- AG artifact paths may expose local workspace layout

## License

MIT
