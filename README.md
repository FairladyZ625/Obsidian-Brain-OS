# 🧠 Obsidian Brain OS

> AI-driven personal knowledge management system — fully runnable, Obsidian-native.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

English | [中文](README_CN.md)

---

## What is this?

**Obsidian Brain OS** is a complete, battle-tested framework for building an AI-augmented personal knowledge system. Not just a template — it's a running platform:

- 📚 **Three-layer knowledge architecture** (Reading / Working / System)
- 🤖 **Nightly AI pipeline** (article integration → conversation mining → knowledge amplification → daily digest)
- 📋 **Personal ops system** (daily dashboard, weekly planning, commitment tracking, morning brief)
- 🛠️ **Automation scripts** (knowledge lint, nightly digest init, conversation export)
- 🎯 **Agent Skills** (AI-native skills for knowledge workflows, research, writing)
- ⏰ **Cron configs** (ready-to-use scheduling templates)
- 🦭 **Installer Skill** (guided Socratic setup for new users)

---

## Quick Start

```bash
# Clone & install
git clone https://github.com/FairladyZ625/Obsidian-Brain-OS.git
cd Obsidian-Brain-OS
bash setup.sh
```

`setup.sh` walks you through everything interactively: vault path, user info, skills, cron, verification. Use `bash setup.sh --test` for a dry run.

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

### 🇨🇳 中文用户

→ 从 [docs/zh/README.md](docs/zh/README.md) 开始，顺序同上。

---

## What's Included

| Module | Description |
|--------|-------------|
| `vault-template/` | Complete Obsidian vault (8 directories) |
| `setup.sh` | Interactive installer (`--test` for dry run) |
| `scripts/` | Automation scripts (lint, digest, export) |
| `prompts/` | Nightly pipeline prompt templates (5 files) |
| `skills/` | 7 core + 18 recommended agent skills |
| `tools/conversation-mining/` | Conversation mining tool (embedded) |
| `cron-examples/` | OpenClaw cron configs (7 jobs) |
| `docs/` | Full English documentation |
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

## Related Project

- **[Agora](https://github.com/FairladyZ625/Agora)** — Multi-agent governance framework. Brain OS provides knowledge context; Agora provides agent collaboration structure.

---

## License

MIT © [FairladyZ](https://github.com/FairladyZ625)
