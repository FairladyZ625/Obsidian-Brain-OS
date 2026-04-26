# Brain Vault Governance

A reusable governance skill for agents working inside an Obsidian Brain OS vault.

## What it prevents

- formal plans living forever in temporary workspaces
- prompts mixed with human-facing plans
- duplicate truth sources
- folders created from memory
- broken wikilinks from raw file moves
- raw OCR / PDF / screenshot dumps committed to Git

## When agents should load it

Load `brain-vault-governance` before:

- writing a formal plan
- creating or moving vault files
- adding folders or numbered sections
- deciding whether something is a prompt, plan, knowledge note, task, or raw asset
- ingesting external article assets
- auditing vault structure

## Basic rule

> Inspect the real vault structure first. Then write the smallest durable artifact to the correct home.

## Typical placement defaults

| Artifact | Default home |
|---|---|
| Project plan | `05-PROJECTS/<project>/plans/` |
| Sprint / implementation plan | `05-PROJECTS/<project>/plans/sprints/` |
| Agent prompt | `04-SYSTEM/prompts/` |
| Todo backlog | `00-INBOX/todo-backlog.md` |
| Knowledge note | `03-KNOWLEDGE/` |
| Raw captured assets | `LOCAL-LARGE-FILES/knowledge-sources/` |

Adapt these paths to your vault template if you use a different layout.

## Recommended install

Copy this directory into your agent skills path, for example:

```bash
cp -R skills/brain-vault-governance ~/.agents/skills/
```

Then instruct your main agent:

> Before writing, moving, or classifying durable vault files, read and follow the `brain-vault-governance` skill.

## Related docs

- `docs/references/vault-governance-guide.md`
- `docs/references/knowledge-asset-boundaries.md`
- `docs/governance-sync-boundary.md`
