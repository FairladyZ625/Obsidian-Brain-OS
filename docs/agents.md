# Agent Team Guide

> Configure your AI agent team for Brain OS. **Chinese version**: [docs/zh/agents.md](docs/zh/agents.md)

---

## Why Multiple Agents?

Brain OS is not a single-agent system. It works like a team:

- **Main Agent (Orchestrator)**: Daily conversations, triage, scheduling, knowledge writing
- **Writer Agent**: Single writer to ensure consistency
- **Chronicle Agent**: Silent channel historian — records, never speaks
- **Review Agent**: Periodic quality auditor

Each agent has clear boundaries. No stepping on each other's toes.

---

## Required Agents

### 1. Main Agent (Orchestrator)

**Role**: Your personal AI chief of staff. Entry point and coordinator.

**Core duties**:
- Receive your requests → INBOX → triage → schedule → drive to completion
- Generate daily briefing, weekly plan, monthly milestones
- Execute Nightly Pipeline stages (article integration / conversation mining / amplification)
- Manage todo reminders (15:00 + 20:00)
- Coordinate other agents' work

**Behavior rules**:
- Conclusion first, then progress. No fluff.
- Can reorder/demote items, but **never delete** without user confirmation
- High-risk operations (delete/send externally) must confirm first

**⚠️ Model requirement: MUST be multimodal**

Your knowledge sources aren't text-only:
- Xiaohongshu / WeChat articles → images + text mixed
- PDF screenshots, webpage captures
- Image notes in Obsidian

Without multimodal support, your main agent cannot process these sources.

**Recommended models**: GPT-4o / Claude Sonnet 4 / GLM-5 (or any vision-capable model)

**Cron jobs** (executed by Main Agent):

| Task | Schedule | Description |
|------|----------|-------------|
| morning-brief | 07:00 daily | Today's dashboard |
| weekly-plan | Monday 05:10 | Weekly roadmap |
| monthly-milestones | 1st of month 06:20 | Monthly milestones |
| todo-reminder | 15:00 + 20:00 | Todo follow-up |

---

### 2. Writer Agent (Knowledge Base Writer)

**Role**: Single designated writer for the Brain vault.

**Why separate?**
- Avoid concurrent write conflicts
- Ensure consistent formatting and governance
- Single audit entry point for all changes

**Model requirement**: Low-cost model OK (GLM-4.7 / Haiku level). Mechanical writing + formatting.

---

### 3. Chronicle Agent (Historian)

**Role**: Silent recorder of channel history. Records only; never comments or intervenes.

**Full doc** → [chronicle-agent.md](docs/zh/chronicle-agent.md) (Chinese) | write English version if needed

**Core duties**:
- Scans Discord channel messages every 2 hours
- Extracts substantive content: decisions, assignments, discussions, commitments
- Writes to `01-PERSONAL-OPS/05-OPS-LOGS/channel-history/`

**Model requirement**: Cheapest available (MiniMax / Haiku). Structured recording, no deep reasoning needed.

**Cron job**: Every 2 hours (`0 */2 * * *`)

---

### 4. Review Agent (Auditor)

**Role**: Knowledge base quality gatekeeper.

**Core duties**:
- Periodic audits: dirty files, format violations, orphan notes, broken links
- Auto-commit pending changes every 30 minutes
- Output audit reports flagging issues needing human attention

**Model requirement**: Low-cost model. Rule checking, not creative work.

**Cron jobs**:

| Task | Schedule | Description |
|------|----------|-------------|
| commit-patrol | Every 30 min | Auto-commit brain changes |
| knowledge-lint | Weekly | Quality audit |

---

## Skills Overview

### Core Skills (install these)

| Skill | Used by | Purpose |
|-------|---------|---------|
| **brain-os-installer** | Installer | Socratic guided setup |
| **personal-ops-driver** | Main Agent | Personal ops: triage, schedule, track |
| **article-notes-integration** | Main/Nightly | Article processing pipeline |
| **conversation-knowledge-flywheel** | Main/Nightly | Conversation mining → knowledge |
| **knowledge-flywheel-amplifier** | Main/Nightly | Cross-source synthesis |
| **notebooklm** | Main Agent | NotebookLM deep research integration |
| **deep-research** | Main Agent | Multi-source deep research |

### Recommended Skills (install as needed)

| Skill | Purpose |
|-------|---------|
| **agent-reach** | Cross-platform content fetch (13+ platforms) ⭐ strongly recommended |
| **arrange** | Information organization |
| **brainstorming** | Brainstorming |
| **clarify** | Requirements clarification |
| **critique** | Review & critique |
| **distill** | Distill & compress |
| **extract** | Information extraction |
| **humanizer** | Humanize AI text |
| **normalize** | Format normalization |
| **optimize** | Optimization |
| **planning-with-files** | File-driven planning |
| **polish** | Language polish |
| **skillshare** | Skill library management |
| **teach-impeccable** | Teaching |
| **writing-plans** | Writing planning |
| **writing-skills** | Writing methodology |

**⚠️ `agent-reach` is strongly recommended** — it's how your main agent reads external image+text content from platforms like Xiaohongshu. Pairs with multimodal main agent.

---

## MVP → Full Progression

**Minimum viable (start here):**
1. One multimodal Main Agent + `personal-ops-driver` skill
2. Vault structure (`setup.sh`)
3. A `todo-backlog.md`

**Add next:**
4. Writer Agent
5. Chronicle Agent + cron
6. Review Agent + commit-patrol cron
7. Nightly Pipeline crons

**Long-term goal:**
8. All core + recommended skills
9. QMD semantic search
10. Agora multi-agent framework (optional)

---

## Quick Config Checklist

After running `setup.sh`:

- [ ] Confirm main agent is multimodal
- [ ] Install core skills
- [ ] Configure Writer Agent
- [ ] Import personal-ops crons
- [ ] Configure Chronicle Agent + cron
- [ ] Configure Review Agent + commit-patrol cron
- [ ] (Optional) Import nightly-pipeline crons
- [ ] Install recommended skills (at minimum `agent-reach`)
- [ ] Design channel structure (if using Discord/Slack)
- [ ] Test morning-brief once
- [ ] Read daily workflow guide

---

## Related

- [Getting Started](getting-started.md)
- [Nightly Pipeline](nightly-pipeline.md)
- [Personal Ops System](personal-ops.md)
- [OpenClaw Setup](openclaw-setup.md)
