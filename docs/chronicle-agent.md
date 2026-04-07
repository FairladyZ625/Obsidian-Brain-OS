# Chronicle Agent (Historian)

> Silent channel recorder. **Chinese version**: [docs/zh/chronicle-agent.md](docs/zh/chronicle-agent.md)

---

## Concept

**Chronicle** is a dedicated Agent role in Brain OS that records Discord channel history. Like ancient Chinese court historians: **records only; never comments or intervenes.**

### Why?

1. **AI memory is short** — each session reset loses all context
2. **Channel discussions are valuable knowledge** — decisions, solutions, experience scattered in chat
3. **Need structured evidence** — `channel-history/` as the "historical evidence layer"
4. **Offload main agent** — let Codex Main focus on execution

---

## How It Works

```
Every 2 hours trigger
       ↓
Chronicle reads last 2h of channel messages
       ↓
Write structured record to channel-history/YYYY-MM-DD-HH.md
       ↓
Git commit → Obsidian visible
```

### What Gets Recorded

- Decisions and conclusions
- Task assignments and commitments
- Technical discussions with outcomes
- Status changes

### What Gets Filtered Out

- Pure chat, emoji reactions, single-word replies
- Content already captured by other systems (e.g., todo-backlog entries)
- Sensitive personal info (unless user requests)

---

## Configuration

| Setting | Recommended |
|---------|-------------|
| Frequency | Every 2 hours |
| Model | Cheapest available (MiniMax / Haiku) |
| Storage | `01-PERSONAL-OPS/05-OPS-LOGS/channel-history/` |
| Format | `YYYY-MM-DD-HH.md` |

See `cron-examples/personal-ops.json` for the full cron job template (`chronicle-channel-history`).

---

## Storage Strategy

- Keep files in `channel-history/` for **30 days**
- Archive or delete older files per your preference
- Maintain an `index.md` for quick navigation

---

## Relation to Other Systems

```
Discord messages → Chronicle (every 2h) → channel-history/ (evidence)
                                                    ↓
                            Personal Ops Driver reads as reference
                                                    ↓
                                    daily-briefing / decision-queue
```

- **Chronicle produces**: writes to `channel-history/`
- **Personal Ops Driver consumes**: reads from `channel-history/`
- **Main Agent coordinates**: file-based coupling, no direct agent chat
