# Architecture — Obsidian Brain OS

> How the system is structured, why it's structured that way, and how the pieces fit together.

---

## Design Philosophy

### 1. Capture Once, Process Forever
Everything enters through `00-INBOX/`. AI handles the routing, classification, and integration. You focus on capture.

### 2. Separate Reading from Working
Knowledge is split into two physical layers:
- **READING/** — What you actually read (polished, curated)
- **WORKING/** — AI's workshop (raw inputs, drafts, candidates)

This prevents the "knowledge graveyard" problem where good content is buried under processing artifacts.

### 3. Pipeline Over Manual Organization
The nightly pipeline (02:00-04:00) automatically:
1. Integrates new article notes into domain knowledge
2. Mines conversations for insights
3. Amplifies knowledge by finding connections

You don't organize. You wake up to organized knowledge.

### 4. Light Project Registry, Heavy External Tools
`04-PROJECTS/` is a lightweight index — project name, one-liner, status, external links. Agora handles multi-agent governance; Linear/GitHub Issues handle task tracking. Brain OS provides knowledge context and doesn't try to replace them.

---

## System Map

```
┌─────────────────────────────────────────────────────────┐
│                    INPUT LAYER                           │
│  00-INBOX/          All new items enter here             │
│  ├─ todo-backlog    Single source of truth for todos     │
│  └─ archive/        Archived todos (by month)            │
├─────────────────────────────────────────────────────────┤
│                 PERSONAL CONTEXT                         │
│  01-PERSONAL-OPS/   AI-powered life management           │
│  ├─ 01-DAILY-BRIEFS   Morning cockpit (auto-generated)   │
│  ├─ 02-PLANS           Weekly/monthly plans              │
│  ├─ 03-TODOS           Commitments, decisions, progress  │
│  ├─ 04-REVIEWS         Retrospectives                    │
│  └─ 05-OPS-LOGS        Channel history, daily logs       │
├─────────────────────────────────────────────────────────┤
│                    KNOWLEDGE LAYER                        │
│  03-KNOWLEDGE/      Three-layer knowledge architecture    │
│  ├─ 01-READING/                                        │
│  │   ├─ 01-DOMAINS/     Domain knowledge cards          │
│  │   ├─ 02-TOPICS/      Topic aggregation pages         │
│  │   ├─ 03-PATTERNS/    Verified pattern cards          │
│  │   └─ 04-DIGESTS/     Daily/weekly digests (start here)│
│  ├─ 02-WORKING/        AI workshop (don't read directly) │
│  │   ├─ 01-ARTICLE-NOTES/  Raw article inputs           │
│  │   ├─ 02-PATTERN-CANDIDATES/  Patterns under review   │
│  │   ├─ 03-TOPIC-DRAFTS/      Topic pages in progress   │
│  │   └─ 04-RESEARCH-QUESTIONS/  Open questions           │
│  └─ 99-SYSTEM/         Pipeline internals (AI only)      │
│      ├─ 01-INDEXES/          Auto-generated indexes      │
│      ├─ 02-EXTRACTIONS/      Extracted facts/fragments   │
│      ├─ 03-INTEGRATION-REPORTS/  Pipeline run reports    │
│      ├─ 04-JOB-STATE/        Pipeline state checkpoints  │
│      └─ 05-META/             Schema, metadata, mappings   │
├─────────────────────────────────────────────────────────┤
│                  SUPPORT LAYERS                           │
│  02-TEAM/           Team collaboration rules              │
│  04-PROJECTS/       Lightweight project registry          │
│  06-PERSONAL-DOCS/  Private documents (gitignored)       │
│  07-WORK-CONTEXT/   Work experience & context             │
├─────────────────────────────────────────────────────────┤
│                  CONFIGURATION                            │
│  config/            Brain-level configuration             │
│  memory/            AI agent memory (daily logs)          │
│  templates/         Document templates                    │
└─────────────────────────────────────────────────────────┘
```

---

## The Nightly Pipeline

```
22:00  User captures articles, conversations, ideas throughout the day
       │
02:00  ┌─ Article Integration ─────────────────────────────┐
       │  Reads: 02-WORKING/01-ARTICLE-NOTES/              │
       │  Writes: 01-READING/01-DOMAINS/, 02-TOPICS/       │
       │  Output: Digest section + run report               │
       └───────────────────────────────────────────────────┘
       │
03:00  ┌─ Conversation Mining ─────────────────────────────┐
       │  Reads: Exported AI transcripts (last 3 days)      │
       │  Writes: Knowledge notes, pattern candidates        │
       │  Output: Digest section + run report               │
       └───────────────────────────────────────────────────┘
       │
04:00  ┌─ Knowledge Amplification ─────────────────────────┐
       │  Reads: Today's digest + domain knowledge           │
       │  Writes: Connections, cross-references, updates     │
       │  Output: Final digest + recommendations             │
       └───────────────────────────────────────────────────┘
       │
05:00  Daily knowledge graph canvas (optional)
07:00  Morning brief generated for personal ops
       │
08:00  User wakes up, reads digest, starts their day
```

Each stage:
1. Runs in an isolated AI session (no main session pollution)
2. Writes to the **shared nightly digest** (`04-DIGESTS/nightly-digest-YYYY-MM-DD.md`)
3. Writes a **machine-facing run report** (`99-SYSTEM/03-INTEGRATION-REPORTS/`)
4. Commits changes to the Brain git repo

If a stage has nothing to process, it writes a no-op report and moves on. No forced output.

---

## Personal Ops System

```
┌──────────────────────────────────────────┐
│  00-INBOX/todo-backlog.md                │
│  (Everything enters here)                │
│              │                           │
│              ▼                           │
│  01-PERSONAL-OPS/                        │
│  ├─ 01-DAILY-BRIEFS/daily-briefing.md   │
│  │   (Auto-generated each morning)      │
│  ├─ 03-TODOS-AND-FOLLOWUPS/             │
│  │   ├─ 当前承诺事项.md                   │
│  │   ├─ progress-board.md               │
│  │   └─ decision-queue.md               │
│  └─ 02-PLANS-AND-SCHEDULES/             │
│      ├─ weekly-plan.md                  │
│      └─ monthly-milestones.md           │
└──────────────────────────────────────────┘
```

**Flow:**
1. New items → `todo-backlog.md` (P0/P1/P2/P3 prioritization)
2. Morning brief AI reads backlog + commitments + decisions → generates today's cockpit
3. Evening reminders (15:00, 20:00) prompt review
4. Weekly plan (Monday) + Monthly milestones (1st) provide longer horizons

---

## Project Management (Optional)

Brain OS provides a **lightweight project registry** (`04-PROJECTS/`) — just enough to give AI context about what you're working on.

For real project management, we recommend pairing with:
- **[Agora](https://github.com/FairladyZ625/Agora)** — Multi-agent governance framework (deliberation → decision → execution)
- Linear, GitHub Issues, or any task tracker you prefer

The project brief template captures:
- Project name and one-liner
- Current phase and focus
- External system links (source of truth lives elsewhere)
- Related knowledge entries in Brain

---

## Knowledge Architecture

### Why Three Layers?

Most knowledge systems mix inputs, processing, and outputs. This creates chaos.

Brain OS separates them physically:

| Layer | Purpose | Who reads it? | Who writes it? |
|-------|---------|---------------|---------------|
| READING | Curated knowledge you actually read | You + AI | AI (pipeline) |
| WORKING | Raw inputs, drafts, candidates | AI only | You + AI |
| SYSTEM | Pipeline state, indexes, reports | AI only | AI (pipeline) |

### Knowledge Flow

```
Article URL → 02-WORKING/01-ARTICLE-NOTES/
                    │
              [02:00 Pipeline]
                    │
                    ├─→ 01-READING/01-DOMAINS/  (domain knowledge card)
                    ├─→ 01-READING/02-TOPICS/   (topic page updated)
                    ├─→ 01-READING/03-PATTERNS/ (if pattern detected)
                    └─→ 01-READING/04-DIGESTS/  (today's digest)
```

### Entry Point

**Always start from `04-DIGESTS/`** — this is where AI summarizes what's new and what's worth reading. If something catches your eye, drill down into DOMAINS or TOPICS.

---

## File Naming Conventions

| Type | Format | Example |
|------|--------|---------|
| Daily brief | `daily-briefing.md` (overwritten daily) | — |
| Nightly digest | `nightly-digest-YYYY-MM-DD.md` | `nightly-digest-2026-04-07.md` |
| Article note | `YYYY-MM-DD-topic.md` | `2026-04-07-building-pks-with-ai.md` |
| Domain card | `topic-name.md` | `ai-agents.md` |
| Project brief | `project-name.md` | `personal-blog.md` |
| Weekly plan | `weekly-plan.md` (overwritten weekly) | — |
| Todo archive | `todo-archive-YYYY-MM.md` | `todo-archive-2026-04.md` |
