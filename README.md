# 🧠 Obsidian Brain OS

> A full implementation of [Karpathy's LLM Wiki](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) concept — automated, multi-agent, and production-ready.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

English | [中文](README_CN.md)

---

## The Idea (from Andrej Karpathy)

> *“Instead of just retrieving from raw documents at query time, the LLM incrementally builds and maintains a persistent wiki — a structured, interlinked collection of markdown files that sits between you and the raw sources… The wiki keeps getting richer with every source you add and every question you ask.”*
>
> *“Obsidian is the IDE; the LLM is the programmer; the wiki is the codebase.”*
>
> — [Andrej Karpathy, llm-wiki (2025)](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)

**Obsidian Brain OS is a complete, battle-tested implementation of this idea** — with automation, multi-agent pipelines, personal ops, and production-ready tooling built on top.

### What Karpathy described → What Brain OS delivers

| Karpathy’s concept | Brain OS implementation |
|--------------------|-----------------------|
| Raw sources layer | `00-INBOX/` + article notes ingestion |
| The wiki (LLM-maintained) | `03-KNOWLEDGE/` (3-layer: Reading/Working/System) |
| The schema (AGENTS.md) | `skills/` + `AGENTS.md` + `SOUL.md` |
| Ingest workflow | `article-notes-integration` skill + Nightly Pipeline |
| Query workflow | QMD semantic search + daily digest |
| Lint workflow | `knowledge-lint.sh` + weekly audit cron |
| LLM writes, you browse | Agent writes to vault; you browse in Obsidian |
| Compounding knowledge | Cross-source synthesis via `knowledge-flywheel-amplifier` |
| Nothing re-derived | All patterns, cross-refs compiled once and kept current |

### What Brain OS adds on top

Karpathy’s gist describes the *idea*. Brain OS is the *running system*:

- 🤖 **Multi-agent team**: main orchestrator + writer + chronicle historian + review auditor
- 🔭 **Observer (self-evolution monitor)**: daily AI team health check — collects session data & gateway logs, detects recurring errors, generates improvement suggestions, maintains an operational memory ledger. Three-level safety: alert only → suggest fix → execute with human confirmation. [Observer Playbook →](docs/agent-playbooks/observer-playbook.md)
- ⏰ **Nightly automation**: 4-stage pipeline runs while you sleep (article integration → conversation mining → amplification → digest)
- 📋 **Personal ops layer**: daily dashboard, todo tracking, commitment management, morning brief
- 🍎 **Apple Reminders integration**: bidirectional sync between Brain todos and Apple Reminders — morning push, evening pull-back
- 📋 **Daily timesheet**: scan git commits + project briefings, align to OKRs, generate draft for confirmation — supports file / Feishu / DingTalk backends
- 🔬 **Deep research**: NotebookLM + deep-research skill for Stage 0 research seeds
- 🎯 **22+ agent skills**: pre-built instruction sets for every workflow
- 🔒 **Governance**: single write entry point, auditable commits, QMD semantic search
- 🚀 **One-command install**: `bash setup.sh` — interactive, bulk placeholder replacement included

---

## Quick Start

```bash
# Clone & install
git clone https://github.com/FairladyZ625/Obsidian-Brain-OS.git
cd Obsidian-Brain-OS
bash setup.sh
```

`setup.sh` walks you through everything interactively: vault path, user info, skills, cron, verification. Use `bash setup.sh --test` for a dry run.

### 🚀 One-Click Install (Copy-Paste to Your AI Agent)

Don't want to read docs? Just **copy the message below and send it to your AI agent** (Claude, ChatGPT, Cursor, OpenClaw agent, or any coding assistant). It will clone the repo, read the installer skill, and guide you through setup step by step.

```
Hi! I want to install Obsidian Brain OS — an AI-driven personal context system. Please:
1. Clone the repo: git clone https://github.com/FairladyZ625/Obsidian-Brain-OS.git
2. Read skills/brain-os-installer/SKILL.md — that's the installation guide for you
3. Follow it to set up my vault: ask me where I want it, my name, timezone, etc.
4. Run bash setup.sh with my answers (or walk me through manually)
5. After install, read docs/agents.md and help me configure my agent team
6. Help me verify everything works with the checklist at the end of setup.sh
Start now — let's get Brain OS running!
```

→ Full guide: [docs/getting-started.md](docs/getting-started.md) | [中文指南](docs/zh/README.md)

---

## Documentation

### 📁 Structure

```
docs/                  ← English documentation (authoritative)
├── getting-started.md
├── agents.md          ← Agent team config (⭐ start here after install)
├── architecture.md
├── nightly-pipeline.md
├── personal-ops.md
├── chronicle-agent.md
├── qmd-setup.md
├── personal-context-guide.md
├── project-management.md
├── obsidian-setup.md
├── openclaw-setup.md
├── skills-guide.md
├── knowledge-architecture.md
└── faq.md

docs/zh/               ← 中文文档（Chinese translations）
├── README.md           ← 中文文档索引
├── agents.md           ← Agent 团队配置指南（详细中文版）
├── ... (same structure, all translated)
```

**Rule**: `docs/` = English, `docs/zh/` = Chinese. Same file names, same content, different language. Read whichever you prefer.

### 📖 Essential Reading (in order)

1. **[Getting Started](docs/getting-started.md)** — Install & first run
2. **[Agent Team Guide](docs/agents.md)** ⭐ — Configure your AI agents (most important post-install doc)
3. **[Architecture](docs/architecture.md)** — Understand the system design
4. **[Personal Ops](docs/personal-ops.md)** — Daily operations
5. **[Nightly Pipeline](docs/nightly-pipeline.md)** — Automated knowledge processing
6. **[NotebookLM Integration](docs/notebooklm.md)** — Deep research with Google NotebookLM
7. **[QMD Semantic Search](docs/qmd-setup.md)** — Vector search for large vaults

### 📋 Contributor & Maintainer Docs / 贡献者与维护者文档

1. **[Component Guide (⭐ Start Here)](docs/component-guide.md)** ⭐ — Everything included, what each component does, 5-min quick start
2. **[Release Playbook](docs/agent-playbooks/release-playbook.md)** — Complete release SOP (bilingual)
3. **[Observer Playbook](docs/agent-playbooks/observer-playbook.md)** — Observer skill usage guide
4. **[PII Deidentification Guide](docs/references/pii-deidentification-guide.md)** — How to keep private data out of the repo
5. **[Cron Prompt Writing Guide](docs/writing-cron-prompts.md)** — Best practices for reliable cron prompts
6. **[Skill Authoring Guide](docs/skill-authoring-guide.md)** — How to write well-structured skills
7. **[Nightly Pipeline Guide (Detailed)](docs/nightly-pipeline-guide.md)** — Full pipeline architecture & handoff protocol

### 🇨🇳 中文用户

→ 从 [docs/zh/README.md](docs/zh/README.md) 开始，顺序同上。

---

## What's Included

| Module | Description |
|--------|-------------|
| `vault-template/` | Complete Obsidian vault (8 directories) |
| `setup.sh` | Interactive installer (`--test` for dry run) |
| `scripts/` | Automation scripts (lint, digest, export, reminders sync, timesheet) |
| `prompts/` | Nightly pipeline prompt templates (8 files) |
| `skills/` | 9 core + 18 recommended agent skills |
| `tools/conversation-mining/` | Conversation mining tool (embedded) |
| `cron-examples/` | OpenClaw cron configs (7 jobs) |
| `docs/` | Full English documentation + contributor guides |
| `docs/agent-playbooks/` | Agent operation playbooks (release, observer) |
| `docs/references/` | Reference guides (PII, etc.) |
| `CHANGELOG_CN.md` | Chinese changelog (mirrors CHANGELOG.md) |
| `docs/zh/` | Full Chinese documentation |

---

## Philosophy

> **Context is infrastructure. Knowledge is compounding.**

1. **Capture** → everything goes to INBOX first
2. **Process** → Nightly AI pipeline turns raw notes into structured knowledge
3. **Compound** → patterns emerge from cross-source synthesis
4. **Act** → daily digest + personal ops keeps you moving

The AI handles the plumbing so you can focus on signal.

---

## 🍎 Apple Reminders Integration

Brain OS includes a **bidirectional sync** between your Brain todos and Apple Reminders — so your knowledge system stays connected to your native task manager.

### How it works

```
07:30 → brain-to-reminders.sh
         Reads today's priorities from daily-briefing.md
         Pushes them to Apple Reminders ("Brain Today" list)
         → You see your Brain todos on iPhone / Apple Watch

21:00 → reminders-to-brain.sh
         Reads completion status from Apple Reminders
         Writes a sync report back to Brain
         → Completed items are reflected in your evening review
```

### Setup

1. Install [`remindctl`](https://github.com/nicholasgasior/remindctl) — the CLI for Apple Reminders
2. Configure your list name in `config.env`:
   ```bash
   REMINDERS_LIST="Brain Today"   # or any list name you prefer
   ```
3. Add the two cron jobs from `prompts/cron/brain-to-reminders-0730.md` and `prompts/cron/reminders-to-brain-2100.md`
4. Run manually to test:
   ```bash
   bash scripts/brain-to-reminders.sh
   bash scripts/reminders-to-brain.sh
   ```

### What gets synced

- **Morning (07:30)**: Top priorities extracted from `daily-briefing.md` → pushed to Reminders with due time
- **Evening (21:00)**: Completion status pulled back → sync report written to `01-PERSONAL-OPS/05-OPS-LOGS/`
- **Deduplication**: Items already in Reminders are skipped
- **Overdue tracking**: Uncompleted past-due items are flagged in the evening report

> **macOS only.** Requires `remindctl` and Apple Reminders app.

---

## Related Project

- **[Agora](https://github.com/FairladyZ625/Agora)** — Multi-agent governance framework. Brain OS provides knowledge context; Agora provides agent collaboration structure.

---

## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=FairladyZ625/Obsidian-Brain-OS&type=Date)](https://star-history.com/#FairladyZ625/Obsidian-Brain-OS&Date)

---

## License

MIT © [FairladyZ](https://github.com/FairladyZ625)
