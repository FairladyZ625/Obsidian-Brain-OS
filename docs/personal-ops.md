# Personal Ops — AI-Powered Life Management

---

## What It Does

Personal Ops turns your todo list into an **AI-driven daily cockpit**. Instead of manually organizing your life, you throw everything into the inbox, and AI generates a focused briefing each morning.

---

## Core Concepts

### The Inbox (SSoT)

`00-INBOX/todo-backlog.md` is your **Single Source of Truth** for everything you need to do.

Everything enters here first. No exceptions.

### Priority System

| Level | Meaning | Action |
|-------|---------|--------|
| **P0** | Must do today | Appears in today's top 3 |
| **P1** | Push this week | Scheduled into weekly plan |
| **P2** | Schedule this month | Added to monthly milestones |
| **P3** | Needs judgment | Stays in backlog until assessed |

### The Daily Briefing

AI generates `01-PERSONAL-OPS/01-DAILY-BRIEFS/daily-briefing.md` every morning at 07:00.

Structure:
```
一、今天最重要的 3 件事
二、今天必须推进但不必做完
三、今天等待反馈 / 需要催办
四、今天需要拍板的事
五、今天可委派的事
六、低能量时可做的小事
七、今天明确不做
八、今日提醒
```

### Decision Rules

AI follows these rules when generating the briefing:
1. Today/tomorrow deadlines first
2. High-leverage but unstarted items second
3. Completed/closed items are never presented as active
4. User items are never deleted (only reordered, consolidated, downgraded)

---

## The Daily Cycle

```
07:00  ┌─ Morning Brief ──────────────────────┐
       │  AI reads: todo-backlog, commitments,  │
       │  decisions, progress board             │
       │  Generates: daily-briefing.md          │
       └────────────────────────────────────────┘
       │
 全天    You work through the briefing
       │
15:00  ┌─ Afternoon Reminder ──────────────────┐
       │  "Check your progress on today's P0s"  │
       └────────────────────────────────────────┘
       │
20:00  ┌─ Evening Review ─────────────────────┐
       │  "Any updates? What carried over?"     │
       └────────────────────────────────────────┘
       │
 随时    New items → todo-backlog.md (P0-P3)
       │
周一    Weekly plan generated
每月1号  Monthly milestones reviewed
```

---

## File Structure

```
01-PERSONAL-OPS/
├─ 01-DAILY-BRIEFS/
│   └─ daily-briefing.md          ← Overwritten daily by AI
├─ 02-PLANS-AND-SCHEDULES/
│   ├─ weekly-plan.md             ← Overwritten weekly
│   └─ monthly-milestones.md      ← Updated monthly
├─ 03-TODOS-AND-FOLLOWUPS/
│   ├─ 当前承诺事项.md              ← Things you committed to
│   ├─ progress-board.md          ← What's in progress
│   └─ decision-queue.md          ← Decisions waiting for your input
├─ 04-REVIEWS-AND-RETROS/
│   └─ weekly-review.md           ← Self-reflection (optional)
└─ 05-OPS-LOGS/
    ├─ channel-history/           ← Cross-referenced channel logs
    ├─ daily-progress/            ← Daily progress notes
    └─ reviews/                   ← Review snapshots
```

---

## Adding New Items

### Quick Add

Just append to `00-INBOX/todo-backlog.md`:

```markdown
- [ ] [P1] Call the dentist
  - 领域：健康
  - 重要性：中
  - 紧急性：高
  - 下一动作：Call Dr. Smith at 555-0123
  - 截止：2026-04-10
```

AI will pick it up in the next morning brief.

### Bulk Import

If you have a brain dump, just list everything in the backlog. AI will triage during the next brief generation.

---

## What AI Can and Cannot Do

### ✅ AI Can
- Reorder items by priority and deadline
- Consolidate duplicates
- Downgrade stale items
- Generate structured briefings
- Track follow-ups and reminders
- Identify decision bottlenecks
- Run a lightweight insight analysis loop that connects external knowledge signals with current projects, blockers, deadlines, and recent conversation-derived ideas

### ❌ AI Cannot
- Delete your items (only you can close/archive)
- Make binding decisions for you
- Schedule meetings on your calendar
- Contact external people

---

## Customization

### Changing Briefing Time

Edit the cron job:
```json
{
  "schedule": {
    "expr": "0 7 * * *",  // Change to preferred hour
    "tz": "Your/Timezone"
  }
}
```

### Adding Briefing Sections

Edit `prompts/personal-ops-morning-brief.prompt.md` to add custom sections.

### Disabling Reminders

Set `"enabled": false` for `personal-ops-todo-reminder-1500` and `personal-ops-todo-reminder-2000` in cron config.
