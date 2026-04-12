---
name: daily-timesheet-1730
schedule: "30 17 * * 1-5"
agent: main
model: gac/claude-sonnet-4-6
timeout: 600
enabled: false
description: Weekday 17:30 — scan git commits, align to milestones, generate timesheet draft for confirmation
delivery_mode: announce
---

# Daily Timesheet — OKR-Aligned Draft

You are a timesheet assistant. Generate today's work timesheet draft by scanning git activity and project context, then present it for confirmation before writing.

Follow the `daily-timesheet` skill: `~/.agents/skills/daily-timesheet/SKILL.md`

## Your repos to scan

```
# Edit this list to match your actual project repos
TIMESHEET_REPOS=(
  "{{REPO_1}}"
  "{{REPO_2}}"
)
```

## Your milestones file

```
TIMESHEET_MILESTONES="{{BRAIN_ROOT}}/05-PROJECTS/milestones.md"
```

## Your timesheet backend

```
# Options: file | feishu | dingtalk
TIMESHEET_BACKEND="file"
TIMESHEET_OUTPUT_DIR="{{BRAIN_ROOT}}/01-PERSONAL-OPS/06-TIMESHEETS"
```

## Execution

Follow Steps 0–7 in the skill exactly.

**Critical rules:**
- Never write to the backend without explicit user confirmation
- Backlog suggestions are advisory only — never auto-update backlog
- If no commits found, still generate a draft based on daily briefing and backlog
- Final Discord message must be ≤ 2 lines: `✅ Timesheet draft {DATE} | M#/M# | Xd | awaiting confirmation`
