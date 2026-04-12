---
name: observer
description: >
  Agent self-evolution observer skill. Collects daily Agent session data and Gateway log anomalies,
  analyzes patterns, updates the .learnings/ ledger, generates a human-readable "daily iteration plan",
  and announces to the observer channel.
  Triggers: (1) daily cron (2) user request (3) urgent anomaly analysis
---

# Observer — Agent Self-Evolution Observer

## Purpose

Observer watches the entire AI team's daily operations — execution quality and infrastructure stability — and surfaces actionable improvement suggestions. It never acts autonomously; it only observes, records, and recommends.

## Two data sources

### Source 1: Agent Session Data

Use `sessions_list` to pull all active sessions, then `sessions_history(sessionKey)` for details.

Focus on:
- Session ended with error (`isError`)
- Tool call failures or retries
- Execution time > 60 seconds
- Model fallback triggered

### Source 2: Gateway Logs

Scan local log files:
- `{{OPENCLAW_HOME}}/logs/gateway.err.log` — error log
- `{{OPENCLAW_HOME}}/logs/gateway.log` — normal requests (flag > 2000ms)
- `{{OPENCLAW_HOME}}/logs/commands.log` — command delivery log

Use `exec` + `grep` to scan for these patterns:

| Pattern | Category | Severity |
|---------|----------|:--------:|
| `plugins.*fetch failed` | infrastructure | medium |
| `gateway.*fetch failed` | infrastructure | medium |
| `FailoverError.*timed out` | infrastructure | high |
| `no available token` | infrastructure | high |
| `Skipping skill path` | infrastructure | low |
| `candidate_failed` | infrastructure | medium |
| `embedded run failover` | infrastructure | medium |

Count occurrences per pattern.

---

## Execution flow (6 steps)

### Step 1: Collect session data

```
sessions_list → get today's session list
→ sessions_history for each session
→ store structured data in .learnings/observer/raw/YYYY-MM-DD-sessions.jsonl
```

### Step 2: Scan gateway logs

```
exec: grep -c to count each anomaly pattern
exec: grep to extract context (2 lines before/after)
→ store in .learnings/observer/raw/YYYY-MM-DD-gateway.jsonl
```

### Step 3: Update .learnings/ ledger

Read `.learnings/observer/index.json`.

For each anomaly:
1. Check if key exists in `recurrenceMap`
2. Exists → update `lastSeen` and `count`
3. New → add entry
4. If root cause is clear → write markdown file to appropriate category directory

### Step 4: Evaluate promote candidates

Check `recurrenceMap`:
- Key with `count >= 7` and recurring within 7 days → flag as "suggest promote"
- Add to iteration plan's "needs human decision" section

### Step 5: Generate daily iteration plan

Use `references/plan-template.md` format, fill with real data.

Output path: `.learnings/observer/plans/YYYY-MM-DD-iteration-plan.md`

Required 6 sections:
1. Today's execution overview (session stats)
2. Infrastructure anomalies (gateway analysis)
3. Agent execution anomalies (session analysis)
4. What to change today (max 3-5 items, with rationale and expected effect)
5. What NOT to change today (with rationale)
6. Needs human decision (list explicitly)

### Step 6: Announce to observer channel

Generate a channel summary (≤ 20 lines) and send:
```
message(action=send, target={{OBSERVER_CHANNEL_ID}}, message=<summary>)
```

Format:
```
📊 **Observer Daily — YYYY-MM-DD**

**Infrastructure**: 🟢/🟡/🔴 one-line summary
**Agent execution**: 🟢/🟡/🔴 one-line summary

**Suggested changes today**:
1. suggestion 1
2. suggestion 2

**Needs decision**: yes/no (brief description)

*Full plan: .learnings/observer/plans/YYYY-MM-DD-iteration-plan.md*
```

---

## .learnings/ directory structure

```
.learnings/
  observer/
    errors/          ← Agent execution failures / timeouts / tool call errors
    infrastructure/  ← Gateway / provider / plugin / command delivery errors
    corrections/     ← User corrections / preference updates
    insights/        ← Observed patterns / best practices
    promoted/        ← Learnings promoted to long-term rules
    plans/           ← Daily iteration plans (human-readable)
    raw/             ← Raw session / gateway structured summaries
    index.json       ← Recurrence counts / search index
```

See `references/index-schema.md` for the full schema.
See `references/plan-template.md` for the plan format.

---

## Learning file template

Each learning is a markdown file:

```markdown
# Error: {{title}}

**Date:** {{DATE}}
**Type:** {{error_type}}
**Category:** errors / infrastructure / corrections / insights
**Severity:** high / medium / low
**Recurrence Count:** {{count}} (last 7 days)

## What Happened
{{description}}

## Context
- Agent: {{agent}} (if applicable)
- Sessions: {{session_ids}} (if applicable)
- Common Pattern: {{pattern}}

## Root Cause
{{root_cause}}

## Prevention
1. {{prevention_1}}
2. {{prevention_2}}

## Status
- [ ] Pending review
- [ ] Suggested (see iteration plan)
- [ ] Executed
- [ ] Promoted
```

---

## Three-level safety mechanism

| Level | Action | Requires confirmation |
|-------|--------|-----------------------|
| Level 1 Alert | Pattern detected → notify | ❌ automatic |
| Level 2 Suggest | Concrete proposal → wait for approval | ✅ required |
| Level 3 Execute | Modify config/skill/cron | ✅ human must confirm |

**Hard rule: Never autonomously modify any skill / cron / openclaw.json. Only observe, record, suggest.**

---

## Setup

1. Configure `{{OBSERVER_CHANNEL_ID}}` in your cron prompt with your actual observer channel ID
2. Set `{{OPENCLAW_HOME}}` to your OpenClaw home directory (default: `~/.openclaw`)
3. Create the `.learnings/observer/` directory structure (or let the skill create it on first run)
4. Add the cron job using `prompts/cron/observer-daily-0001.md` as a template

---

## Constraints

- Never modify skill / cron / openclaw.json without explicit human confirmation
- Never delete learning files (archive only)
- Raw logs in `.learnings/raw/` auto-purge after 7 days
- All git commits must use `[observer]` prefix
- P0 frozen layer (identity, authority, hard rules) is never touched

---

## Completion checklist

After each Observer run, confirm:
1. `.learnings/observer/plans/YYYY-MM-DD-iteration-plan.md` generated
2. `.learnings/observer/index.json` updated
3. `.learnings/observer/raw/` written for today
4. Observer channel announced
5. Git commit made (if files changed)
