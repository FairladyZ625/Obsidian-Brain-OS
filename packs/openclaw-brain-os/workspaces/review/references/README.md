# Agent Workspace References

References are on-demand operating manuals. Keep `AGENTS.md` short and put long, task-specific rules here.

## Why references exist

`AGENTS.md` is loaded often. If it becomes a giant operations manual, every task pays the context cost and important rules become harder to see.

Use this split:

| Layer | Purpose | Example |
|---|---|---|
| `AGENTS.md` | Always-on constitution: identity, safety, routing index | “Ask before deleting or publishing” |
| `USER.md` | Stable owner preferences and safe profile | timezone, response style |
| `references/` | Task-specific procedures loaded on demand | vault writes, cron rules, sync rules |
| skills | Reusable capabilities with their own instructions | article ingestion, governance, research |

## Naming convention

Use lowercase kebab-case:

```text
references/vault-write-rules.md
references/open-source-sync-rules.md
references/channel-collaboration-rules.md
references/cron-rules.md
```

## When to create a reference

Create a reference when a rule or procedure is:

- longer than ~50 lines
- only needed for specific tasks
- likely to be reused
- too detailed for always-on `AGENTS.md`

Do not create references for one-off notes. Put those in daily memory or a project note.

## Required shape

Each reference should include:

1. **When to read this** — clear triggers
2. **Core rule** — one-paragraph summary
3. **Procedure** — step-by-step instructions
4. **Examples** — safe placeholders, no private values
5. **Common mistakes** — what agents often get wrong

## AGENTS.md index pattern

In `AGENTS.md`, keep a small index:

```markdown
## Reference Index

| Reference | Trigger |
|---|---|
| `references/vault-write-rules.md` | Creating or moving durable vault files |
| `references/open-source-sync-rules.md` | Deciding what belongs in a public repo |
```

Agents should read a reference only when the trigger matches the task.
