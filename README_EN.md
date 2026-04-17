# 🧠 Obsidian Brain OS

> We had already been building and operating this system for a long time before realizing it strongly converged with [Karpathy's LLM Wiki](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) at the conceptual level.  
> **But Brain OS goes beyond a wiki into a digital twin operating system** — where your knowledge, tasks, conversations, boundaries, and agent workflows are continuously compiled into a system that can assist, coordinate, and act within controlled scope.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

[中文（默认）](README.md) | English

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
> Your vault name is user-defined. `{{BRAIN_ROOT}}` means your own vault root path, it does not need to be named `ZeYu-AI-Brain`.

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

→ Full guide: [docs/getting-started.md](docs/getting-started.md) | [中文首页](README.md)

---

## Documentation

### 📋 Contributor & Maintainer Docs / 贡献者与维护者文档

1. **[Component Guide (⭐ Start Here)](docs/component-guide.md)** ⭐ — Everything included, what each component does, 5-min quick start
2. **[Release Playbook](docs/agent-playbooks/release-playbook.md)** — Complete release SOP (bilingual)
3. **[Observer Playbook](docs/agent-playbooks/observer-playbook.md)** — Observer skill usage guide
4. **[PII Deidentification Guide](docs/references/pii-deidentification-guide.md)** — How to keep private data out of the repo
5. **[Cron Prompt Writing Guide](docs/writing-cron-prompts.md)** — Best practices for reliable cron prompts
6. **[Skill Authoring Guide](docs/skill-authoring-guide.md)** — How to write well-structured skills
7. **[Nightly Pipeline Guide (Detailed)](docs/nightly-pipeline-guide.md)** — Full pipeline architecture & handoff protocol

### 📖 User Docs

- Chinese default homepage: [README.md](README.md)
- English quick start: [docs/getting-started.md](docs/getting-started.md)
- Component map: [docs/component-guide.md](docs/component-guide.md)
- Agent setup: [docs/agents.md](docs/agents.md)

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

## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=FairladyZ625/Obsidian-Brain-OS&type=Date)](https://star-history.com/#FairladyZ625/Obsidian-Brain-OS&Date)

---

## License

MIT © [FairladyZ](https://github.com/FairladyZ625)
