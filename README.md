# 🧠 Obsidian Brain OS

> An AI-driven personal knowledge management system — fully runnable, Obsidian-native.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## What is this?

**Obsidian Brain OS** is a complete, battle-tested framework for building an AI-augmented personal knowledge system. It's not just a template — it's a running platform with:

- 📚 **Three-layer knowledge architecture** (Reading / Working / System)
- 🤖 **Nightly AI pipeline** (article integration → conversation mining → knowledge amplification → daily digest)
- 📋 **Personal ops system** (daily dashboard, weekly planning, commitment tracking, morning brief)
- 🛠️ **Automation scripts** (knowledge lint, nightly digest init, conversation export, knowledge canvas)
- 🎯 **Agent Skills** (AI-native skills for knowledge workflows, research, writing, brainstorming)
- ⏰ **OpenClaw cron configs** (ready-to-use scheduling templates)
- 🦭 **Brain OS Installer Skill** (guided Socratic setup for new users)

This is the exact system used to manage knowledge, projects, and daily operations — open-sourced and anonymized for everyone.

---

## Architecture Overview

```
Obsidian Brain OS
├── 📥 00-INBOX/              Capture everything first
├── 🎯 01-PERSONAL-OPS/       Daily ops, planning, tracking
├── 👥 02-TEAM/               Team collaboration rules
├── 🧠 03-KNOWLEDGE/
│   ├── 01-READING/           What you actually read
│   │   ├── 01-DOMAINS/       Domain knowledge cards
│   │   ├── 02-TOPICS/        Topic entry pages
│   │   ├── 03-PATTERNS/      Distilled patterns
│   │   └── 04-DIGESTS/       Daily/weekly digests ← Start here
│   ├── 02-WORKING/           Work in progress
│   │   ├── 01-ARTICLE-NOTES/ Raw article processing
│   │   ├── 02-PATTERN-CANDIDATES/
│   │   ├── 03-TOPIC-DRAFTS/
│   │   └── 04-RESEARCH-QUESTIONS/
│   └── 99-SYSTEM/            AI pipeline outputs (don't read directly)
├── 05-PROJECTS/              Project registry layer
├── 06-PERSONAL-DOCS/       Personal docs (gitignored by default)
├── 07-WORK-CONTEXT/       Work experience & context
└── templates/                Document templates
```

### Nightly AI Pipeline

```
02:00  Article Integration    → process article notes → domain knowledge
03:00  Conversation Mining    → extract insights from AI conversations
04:00  Knowledge Amplification → cross-source synthesis → patterns
       ↓
       Daily Digest (your morning reading)
```

---

## Quick Start

### Prerequisites
- [Obsidian](https://obsidian.md/) (required)
- [Git](https://git-scm.com/)
- [OpenClaw](https://openclaw.ai) (for AI pipeline & scheduling)
- Python 3.9+ (for scripts)

### 5-Minute Setup

```bash
# 1. Clone this repo as your vault
git clone git@github.com:FairladyZ625/Obsidian-Brain-OS.git ~/brain

# 2. Open in Obsidian
# File → Open Vault → select ~/brain/vault-template

# 3. Install recommended Obsidian plugins
# See docs/obsidian-setup.md

# 4. Configure your paths
cp scripts/config.env.example scripts/config.env
# Edit config.env with your paths

# 5. Run the installer skill (optional — guided setup)
# In OpenClaw: "install brain-os" 
# The installer will walk you through everything via Socratic dialogue
```

→ See **[docs/getting-started.md](docs/getting-started.md)** for full setup guide.

---

## What's Included

| Module | Description |
|--------|-------------|
| `vault-template/` | Complete Obsidian vault template |
| `scripts/` | Automation scripts (lint, digest, export, canvas) |
| `prompts/` | Nightly pipeline prompt templates |
| `skills/` | AI agent skills (core + recommended) |
| `cron-examples/` | OpenClaw scheduling configs |
| `examples/` | Sample notes, digests, project briefs |
| `docs/` | Full documentation |

### Core Skills
- **brain-os-installer** — Guided Socratic setup for new users
- **personal-ops-driver** — Daily personal ops management
- **article-notes-integration** — Article processing pipeline
- **conversation-knowledge-flywheel** — Knowledge flywheel orchestration
- **knowledge-flywheel-amplifier** — Cross-source synthesis
- **notebooklm** — NotebookLM deep research integration
- **deep-research** — Multi-source deep research

### Recommended Skills
Planning, brainstorming, writing, critique, humanizing, polishing and more — see `skills/recommended/`.

---

## Philosophy

> **Context is infrastructure. Knowledge is compounding.**

Most PKM systems are static vaults. Brain OS is a living system:

1. **Capture** → everything goes to INBOX first
2. **Process** → nightly AI pipeline turns raw notes into structured knowledge
3. **Compound** → patterns emerge from cross-source synthesis
4. **Act** → daily digest + personal ops keeps you moving

The AI doesn't replace your thinking — it handles the plumbing so you can focus on the signal.

---

## Documentation

### 📖 使用指南（中文，推荐先读）
- [总览](docs/guide/00-overview.md) — 从这里开始
- [核心方法论](docs/guide/00-philosophy.md) — 为什么这样设计
- [Agent 配置指南](docs/guide/01-agent-setup.md) — 怎么配好你的 AI Agent
- [频道设计](docs/guide/02-channel-design.md) — 怎么分频道防止上下文污染
- [日常工作流](docs/guide/03-daily-workflow.md) — 每天怎么用这套系统
- [迭代指南](docs/guide/04-iteration-guide.md) — 持续优化你的系统

### 📚 技术文档（English）
- [Getting Started](docs/getting-started.md)
- [Architecture](docs/architecture.md)
- [Obsidian Setup](docs/obsidian-setup.md)
- [OpenClaw Setup](docs/openclaw-setup.md)
- [Nightly Pipeline](docs/nightly-pipeline.md)
- [Personal Ops System](docs/personal-ops.md)
- [Knowledge Architecture](docs/knowledge-architecture.md)
- [Skills Guide](docs/skills-guide.md)
- [Project Management](docs/project-management.md)
- [FAQ](docs/faq.md)

---

## License

MIT © [FairladyZ](https://github.com/FairladyZ625)
