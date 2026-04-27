# Brain OS v1.1.0 内容全览 — 完整组件指南

> **English:** Everything included in Brain OS **v1.1.0**, what each component does, and how to start using it.
>
> **中文：** Brain OS **v1.1.0** 包含的所有内容、每个组件的作用、以及如何开始使用。

---

## At a Glance / 一览

| Category / 类别 | Components / 组件 | Count / 数量 |
|---|---|:---:|
| Vault Template / Vault 模板 | 8 directories | 1 |
| Skills / 技能 | Agent instruction packages | 10+ |
| Scripts / 脚本 | Automation + verification tools | 7+ |
| Cron Prompts / 定时任务模板 | Nightly pipeline + governance cron | 11+ |
| Documentation / 文档 | User guides + contributor guides + bilingual docs | 30+ |
| Schemas / 数据结构 | JSON schemas for structured data | 2 |
| Examples / 示例 | Sample data files | 1 |
| CI/CD Workflows | GitHub Actions | 4 |

---

## 🏗️ Core Architecture / 核心架构

### The Nightly Pipeline / 夜间流水线（4 阶段）

This is the heart of Brain OS — an automated knowledge processing pipeline that runs while you sleep.
这是 Brain OS 的核心——在你睡觉时自动运行的知识处理流水线。

```
01:00 Mon ──→ Knowledge Lint (知识库健康检查)
02:00 Daily ──→ Article Integration (文章整合)
03:00 Daily ──→ Conversation Mining (对话挖掘)
04:00 Daily ──→ Knowledge Amplifier (知识放大 + 摘要生成)
```

**How to enable / 如何启用：**
1. Copy `prompts/cron/*.md` to your OpenClaw cron jobs directory
2. Set `enabled: true` in each file's frontmatter
3. Configure paths in each prompt (replace `{{BRAIN_ROOT}}`, `{{USER_HOME}}` etc.)
4. Your AI agent will execute them at scheduled times

**Related docs / 相关文档：**
- [Nightly Pipeline Guide (detailed)](docs/nightly-pipeline-guide.md) — Full architecture & handoff protocol
- [Cron Prompt Writing Guide](docs/writing-cron-prompts.md) — How to write reliable cron prompts

---

## 🤖 Skills / 技能包

Skills are reusable instruction packages that tell your AI agent how to perform specific tasks.
Skill 是可复用的指令包，告诉你的 AI agent 如何执行特定任务。

### Included Skills / 内置技能

| Skill / 技能 | What it does / 作用 | Start here / 从这里开始 |
|---|---|---|
| **`brain-os-release`** 🆕 | Release SOP — version bump, PII check, PR, tag | [Release Playbook](docs/agent-playbooks/release-playbook.md) |
| **`observer`** 🆕 | Daily team health monitor — sessions + logs analysis | [Observer Playbook](docs/agent-playbooks/observer-playbook.md) |
| **`daily-timesheet`** | Scan git commits → align to OKRs → generate timesheet | `skills/daily-timesheet/SKILL.md` |
| **`english-tutor`** | Interactive listening practice with Whisper + TTS | `skills/english-tutor/SKILL.md` |
| **`article-notes-integration`** | Ingest articles into knowledge base with cross-references | `skills/article-notes-integration/SKILL.md` |
| **`conversation-knowledge-flywheel`** | Mine conversations for reusable knowledge patterns | `skills/conversation-knowledge-flywheel/SKILL.md` |
| **`knowledge-flywheel-amplifier`** | Cross-source synthesis and weak-signal amplification | `skills/knowledge-flywheel-amplifier/SKILL.md` |
| **`deep-research`** | Deep research using NotebookLM or web search | `skills/deep-research/skill.md` |
| **`knowledge-lint`** | Knowledge base health audit (broken links, orphans) | `skills/knowledge-lint/SKILL.md` |

🆕 = New in v0.4–v0.5
🆕 = Updated in v1.0.0–v1.1.0

---

## 🛡️ Knowledge Governance Stack / 知识库治理栈（v1.0.0）

A three-layer system for keeping the knowledge base healthy over time.
让知识库长期保持健康的三层治理系统。

```
Daily (保鲜)  → qmd-index-refresh-daily.md
3-Day (整理) → knowledge-librarian-3day.md
10-Day (治理) → knowledge-governance-10day.md
```

**How to enable / 如何启用：**
1. Copy `prompts/cron/knowledge-*.md` to your OpenClaw cron jobs directory
2. Set `enabled: true` in each file's frontmatter
3. Configure paths (replace `{{BRAIN_ROOT}}`, `{{QMD_BIN}}` etc.)
4. Follow staged rollout: Daily → 3-Day → 10-Day (one layer at a time)

**Related docs / 相关文档：**
- [Getting Started](docs/getting-started.md) — Install guide
- [Friction-to-Governance Loop](docs/friction-to-governance-loop.md) — Self-improvement methodology

---

## 🔄 Friction-to-Governance Loop / 摩擦治理循环（v1.0.0–v1.2.0）

A pattern for turning recurring operational friction into system-level improvements.
把重复出现的运营摩擦转化为系统级改进的模式。

### Core components / 核心组件

| Component / 组件 | What it does / 作用 | Start here / 从这里开始 |
|---|---|---|
| **Methodology doc** | Explains the 4-stage loop (Capture → Diagnose → Govern → Write-back) | [EN](docs/friction-to-governance-loop.md) / [中文](docs/zh/friction-to-governance-loop.md) |
| **Prompt template** | Reusable prompt for agents to diagnose and fix recurring friction | `prompts/friction-to-governance-loop.prompt.md` |
| **System governance guide** | Which system layer to write fixes into | [Guide](docs/references/system-governance-guide.md) |
| **Bucket guide** | Standard taxonomy for classifying friction types | [EN](docs/references/friction-bucket-guide.md) / [中文](docs/zh/friction-bucket-guide.md) |
| **Write-back matrix** | Decision matrix: which problem → which layer | [EN](docs/references/friction-writeback-matrix.md) / [中文](docs/zh/friction-writeback-matrix.md) |
| **Report template** | Structured report format for friction reviews | [EN](docs/friction-report-template.md) / [中文](docs/zh/friction-report-template.md) |
| **Event schema** | JSON schema for a single friction signal | `schemas/friction-event.schema.json` |
| **Report schema** | JSON schema for aggregated reports | `schemas/friction-report.schema.json` |
| **Sample data** | 5 example friction signals in JSONL format | `examples/friction-log.sample.jsonl` |

**How to use / 如何使用：**
1. Read the methodology doc first
2. When you see a recurring problem, classify it using the bucket guide
3. Use the write-back matrix to decide where to fix it
4. Use the report template for periodic reviews
5. Use the prompt template to automate diagnosis with an AI agent

1. Read the SKILL.md file for instructions
2. Point your AI agent to the skill path when assigning tasks
3. For cron automation, use the corresponding prompt in `prompts/cron/`

**Related docs / 相关文档：**
- [Skill Authoring Guide](docs/skill-authoring-guide.md) — How to write your own skills

---

## 🔧 Scripts / 脚本工具

| Script / 脚本 | Purpose / 用法 | Usage / 使用方式 |
|---|---|---|
| **`check-pii.sh`** 🆕 | Scan files for PII before committing | `bash scripts/check-pii.sh --strict` |
| **`verify-install.sh`** 🆕 | Verify config, vault structure, installed skills, and core checks after setup | `bash scripts/verify-install.sh` |
| **`scan-today-changes.sh`** | Detect today's changes across repos | Used by daily sync cron |
| **`brain-to-reminders.sh`** | Push Brain todos → Apple Reminders | `BRAIN_ROOT=/path bash scripts/brain-to-reminders.sh` |
| **`reminders-to-brain.sh`** | Pull Reminders completion → Brain | `BRAIN_ROOT=/path bash scripts/reminders-to-brain.sh` |
| **`init-nightly-digest.sh`** | Initialize nightly digest skeleton | `bash scripts/init-nightly-digest.sh <brain-root> <date>` |

🆕 = New in v0.4–v0.5

### Install & onboarding / 安装与上手

For the cleanest first-run path:
- humans: start with `docs/getting-started.md`
- AI agents: start with `INSTALL_FOR_AGENTS.md`
- unsure which scope to choose: read `docs/install-profiles.md`

### PII Safety / PII 安全

Every commit should pass PII scan:
每次提交前都应通过 PII 扫描：

```bash
bash scripts/check-pii.sh --strict   # Must output: ✅ 0 hits
```

CI enforces this automatically on every PR.
CI 在每个 PR 上自动强制执行此检查。

**Related docs / 相关文档：**
- [PII Deidentification Guide](docs/references/pii-deidentification-guide.md)

---

## ⏰ Cron Prompts / 定时任务模板

Templates for automated tasks you can schedule in OpenClaw:
可在 OpenClaw 中调度的自动化任务模板：

| Prompt / 模板 | Schedule / 时间 | Function / 功能 |
|---|---|---|
| `observer-daily-0001.md` 🆕 | 00:01 daily | Team health monitoring (disabled by default) |
| `daily-knowledge-graph-canvas-0500.md` | 05:00 daily | Generate knowledge graph canvas |
| `brain-to-reminders-0730.md` | 07:30 daily | Push todos to Apple Reminders |
| `daily-timesheet-1730.md` | 17:30 weekdays | Generate timesheet from commits |
| `reminders-to-brain-2100.md` | 21:00 daily | Pull completion status back |
| `chronicle-every-2h-log.md` 🆕 | Every 2h | Channel history logging |
| `knowledge-lint-weekly.md` | Monday 01:00 | Weekly knowledge base audit |
| `article-notes-integration-nightly.md` | 02:00 daily | Article ingestion (Stage 2 of pipeline) |
| `conversation-mining-nightly.md` | 03:00 daily | Conversation mining (Stage 3 of pipeline) |
| `amplifier-nightly.md` | 04:00 daily | Knowledge synthesis (Stage 4 of pipeline) |

🆕 = Updated in v0.4–v0.5 with system date fetch

### Key improvement in v0.4.1 / v0.4.1 关键改进

All cron prompts now **force system date fetching** as Step 0 — no more LLM date hallucination:
所有 cron prompt 现在都在步骤 0 **强制获取系统日期**——不再有 LLM 日期幻觉：

```markdown
Step 0: Run `date "+%Y-%m-%d %A %H:%M %Z"` → get REAL date from system
# All subsequent YYYY-MM-DD references use this value
```

Uses your machine's local timezone by default — works anywhere in the world.
默认使用你机器的本地时区——全球通用。

---

## 📚 Documentation Map / 文档地图

### For Users / 用户文档（入门顺序）

1. **[README](README.md)** — Project overview & quick start
2. **[Feature Matrix SSOT](docs/feature-matrix.md)** ⭐ — All features, install assets, and verification checks
3. **[Getting Started](docs/getting-started.md)** — Install & first run
4. **[Agent Team Guide](docs/agents.md)** ⭐ — Configure your AI agents
5. **[Architecture](docs/architecture.md)** — System design
5. **[Nightly Pipeline](docs/nightly-pipeline.md)** — Automated knowledge processing
6. **[Personal Ops](docs/personal-ops.md)** — Daily operations dashboard
7. **[QMD Semantic Search](docs/qmd-setup.md)** — Vector search setup
8. **[Friction-to-Governance Loop](docs/friction-to-governance-loop.md)** 🆕 — Self-improvement methodology

### For Contributors / 贡献者文档

1. **[Release Playbook](docs/agent-playbooks/release-playbook.md)** ⭐ — How to publish a release
2. **[Observer Playbook](docs/agent-playbooks/observer-playbook.md)** — Observer usage guide
3. **[PII Deidentification Guide](docs/references/pii-deidentification-guide.md)** — Keep private data out
4. **[Cron Prompt Writing Guide](docs/writing-cron-prompts.md)** — Reliable cron best practices
5. **[Skill Authoring Guide](docs/skill-authoring-guide.md)** — Write good skills
6. **[Nightly Pipeline Guide (Detailed)](docs/nightly-pipeline-guide.md)** — Full architecture deep-dive

### Bilingual / 双语

| English | 中文 |
|---------|------|
| `README.md` | `README_CN.md` |
| `CHANGELOG.md` | `CHANGELOG_CN.md` |
| `docs/*.md` | `docs/zh/*.md` |
| All playbooks & guides | Each file contains both languages |

---

## 🔒 CI/CD / 自动化保护

Three GitHub Actions workflows protect code quality:
三个 GitHub Actions 工作流保护代码质量：

| Workflow / 工作流 | Trigger / 触发条件 | Block merge? / 阻断合并？ |
|---|---|:---:|
| **PII Scan** (`pii-scan.yml`) | Every PR & push to main | ✅ Yes |
| **Structure Check** (`structure-check.yml`) | Every PR & push to main | ✅ Yes |
| **CHANGELOG Check** (`changelog-check.yml`) | Every PR | ⚠️ Warn only |

Additionally, **branch protection** is enabled on `main`:
此外，**分支保护**已在 main 上启用：

- No direct pushes to main（禁止直接推送到 main）
- Required: 1 approval + PII scan pass + Structure check pass
- No force pushes, no deletions
- Even repo admins must follow these rules

---

## 🚀 Quick Start (5 Minutes) / 快速上手（5 分钟）

```bash
# 1. Clone
git clone https://github.com/FairladyZ625/Obsidian-Brain-OS.git
cd Obsidian-Brain-OS

# 2. Install (interactive)
bash setup.sh

# 3. Verify PII scanner works
bash scripts/check-pii.sh --strict
# Expected: ✅ PII scan passed — 0 hits

# 4. Pick a skill to try
cat skills/observer/SKILL.md        # Team health monitor
cat skills/daily-timesheet/SKILL.md # Timesheet generation

# 5. Enable one cron prompt (e.g., observer)
# Edit prompts/cron/observer-daily-0001.md:
#   Set enabled: true
#   Replace {{YOUR_CHANNEL_ID}} with your Discord channel
#   Add to your OpenClaw cron jobs

# 6. Make your first change
# Edit a file → run PII check → commit → push PR
```

---

## Version History / 版本历史

| Version / 版本 | Date / 日期 | Highlights / 亮点 |
|---|---|---|
| **v1.1.0** | 2026-04-23 | Friction loop practice templates, bilingual docs, prompt + governance guide |
| **v1.0.0** | 2026-04-21 | Knowledge governance stack (3-layer cron), staged rollout guide |
| **v0.6.1** | 2026-04-18 | Soft-link sync, project-aware lint, governance updates |
| **v0.5.0** | 2026-04-13 | Bilingual governance, 6 contributor docs, CHANGELOG_CN, branch protection |
| **v0.4.1** | 2026-04-13 | System-local timezone for all cron prompts |
| **v0.4.0** | 2026-04-12 | Release SOP, Observer skill, PII scanner, 3 CI workflows |
| **v0.3.0** | 2026-04-12 | Daily timesheet, Apple Reminders sync, English tutor |
| **v0.2.0** | 2026-04-08 | Nightly pipeline skills (flywheel, article integration, conversation mining) |
| **v0.1.0** | 2026-03-15 | Initial release: vault template, setup.sh, core skills |

See [CHANGELOG.md](CHANGELOG.md) / [CHANGELOG_CN.md](CHANGELOG_CN.md) for full details.
详见 [CHANGELOG.md](CHANGELOG.md) / [CHANGELOG_CN.md](CHANGELOG_CN.md)。

---

## Need Help? / 需要帮助？

- 📖 **Read the docs first** — Start with [README](README.md) and [Agent Team Guide](docs/agents.md)
- 🐛 **Found a bug?** — Open an Issue on GitHub
- 💡 **Want to contribute?** — Read [Release Playbook](docs/agent-playbooks/release-playbook.md) and [PII Guide](docs/references/pii-deidentification-guide.md) first
- 💬 **Questions?** — Discussions tab on GitHub
