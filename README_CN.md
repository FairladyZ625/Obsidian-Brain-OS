# 🧠 Obsidian Brain OS

> AI 驱动的个人知识管理系统——开箱即用，深度 Obsidian 原生。

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

[English](README.md) | 中文

---

## 这是什么？

**Obsidian Brain OS** 是一套经过实战打磨的完整框架，用于构建 AI 增强的个人知识系统。它不是一个普通模板——它是一个可运行的平台，包含：

- 📚 **三层知识架构**（阅读层 / 工作层 / 系统层）
- 🤖 **Nightly AI 流水线**（文章整合 → 对话挖掘 → 知识放大 → 每日摘要）
- 📋 **个人事务系统**（每日驾驶舱、周计划、承诺追踪、早间简报）
- 🛠️ **自动化脚本**（知识审计、摘要初始化、对话导出）
- 🎯 **Agent Skills**（AI 原生 skills，覆盖知识工作流、研究、写作、头脑风暴）
- ⏰ **OpenClaw Cron 配置**（开箱即用的定时任务模板）
- 🦭 **Brain OS 安装向导 Skill**（苏格拉底式引导安装，新用户友好）

这是真实在用的个人知识管理系统，经脱敏后开源，供所有人使用。

---

## 架构总览

```
Obsidian Brain OS
├── 📥 00-INBOX/              先把一切扔进来
├── 🎯 01-PERSONAL-OPS/       每日事务、计划、追踪
├── 👥 02-TEAM/               团队协作规则
├── 🧠 03-KNOWLEDGE/
│   ├── 01-READING/           你真正读过的内容
│   │   ├── 01-DOMAINS/       领域知识卡
│   │   ├── 02-TOPICS/        主题入口页
│   │   ├── 03-PATTERNS/      提炼后的模式
│   │   └── 04-DIGESTS/       每日/每周摘要 ← 从这里开始读
│   ├── 02-WORKING/           进行中的工作
│   │   ├── 01-ARTICLE-NOTES/ 原始文章处理
│   │   ├── 02-PATTERN-CANDIDATES/
│   │   ├── 03-TOPIC-DRAFTS/
│   │   └── 04-RESEARCH-QUESTIONS/
│   └── 99-SYSTEM/            AI 流水线输出（不要直接读）
├── 04-CUSTOM/                你的自定义区域（随便放）
├── 05-PROJECTS/              轻量项目注册层
├── 06-PERSONAL-DOCS/         个人私密文档（默认 gitignored）
├── 07-WORK-CONTEXT/          工作经验与上下文积累
└── templates/                文档模板
```

### Nightly AI 流水线

```
02:00  文章整合    → 处理文章笔记 → 领域知识
03:00  对话挖掘    → 提取 AI 对话中的洞察
04:00  知识放大    → 跨来源合成 → 模式提炼
       ↓
       每日摘要（你的早读内容）
```

---

## 快速开始

### 前置条件
- [Obsidian](https://obsidian.md/)（必须）
- [Git](https://git-scm.com/)
- [OpenClaw](https://openclaw.ai)（AI 流水线 & 定时任务）
- Python 3.9+（运行脚本）

### 交互式安装（推荐）

```bash
# 1. 克隆仓库
git clone https://github.com/FairladyZ625/Obsidian-Brain-OS.git
cd Obsidian-Brain-OS

# 2. 运行交互式安装脚本
bash setup.sh
```

脚本会引导你完成所有配置：vault 路径、用户信息、skill 安装、cron 配置生成、安装验证。

### 5 分钟手动安装

```bash
# 1. 克隆仓库
git clone https://github.com/FairladyZ625/Obsidian-Brain-OS.git

# 2. 在 Obsidian 中打开 vault 模板
# File → Open Vault → 选择 vault-template/

# 3. 配置路径
cp scripts/config.env.example scripts/config.env
# 编辑 config.env，填入你的路径

# 4. （可选）使用安装向导 skill
# 在 OpenClaw 中说："install brain-os"
# 向导会通过对话引导你完成所有步骤
```

→ 完整安装指南：**[docs/guide/00-overview.md](docs/guide/00-overview.md)**

---

## 包含什么

| 模块 | 说明 |
|------|------|
| `vault-template/` | 完整的 Obsidian vault 模板（8 个主目录） |
| `setup.sh` | 交互式安装脚本（支持 `--test` 模式） |
| `scripts/` | 自动化脚本（审计、摘要初始化、对话导出） |
| `prompts/` | Nightly Pipeline 提示词模板 |
| `skills/` | AI Agent Skills（6 个核心 + 18 个推荐） |
| `tools/conversation-mining/` | 对话挖掘工具（内嵌，无需额外安装） |
| `cron-examples/` | OpenClaw 定时任务配置模板 |
| `docs/` | 完整文档（中英文） |

### 核心 Skills
- **brain-os-installer** — 苏格拉底式引导安装，支持模块化选择
- **personal-ops-driver** — 个人事务驾驶系统
- **article-notes-integration** — 文章处理流水线
- **conversation-knowledge-flywheel** — 对话知识飞轮
- **knowledge-flywheel-amplifier** — 跨来源知识合成
- **notebooklm** — NotebookLM 深度研究集成
- **deep-research** — 多来源深度研究

### 推荐 Skills
规划、头脑风暴、写作、评审、人性化、润色等——见 `skills/recommended/`。

---

## 设计理念

> **上下文是基础设施。知识是复利。**

大多数 PKM 系统是静态的文件库。Brain OS 是一个活系统：

1. **捕获** → 所有内容先进 INBOX
2. **处理** → Nightly AI 流水线把原始笔记变成结构化知识
3. **复利** → 跨来源合成让模式自然涌现
4. **行动** → 每日摘要 + 个人事务系统保持推进

AI 不替代你的思考——它处理管道工作，让你专注在真正重要的信号上。

---

## 文档

### 📖 使用指南（中文，推荐先读）
1. [总览](docs/guide/00-overview.md) — 从这里开始
2. [核心方法论](docs/guide/00-philosophy.md) — 为什么这样设计
3. [Agent 配置指南](docs/guide/01-agent-setup.md) — 怎么配好你的 AI Agent
4. [频道设计](docs/guide/02-channel-design.md) — 怎么分频道防止上下文污染
5. [日常工作流](docs/guide/03-daily-workflow.md) — 每天怎么用这套系统
6. [迭代指南](docs/guide/04-iteration-guide.md) — 持续优化你的系统

### 📚 技术文档（中文翻译版）
→ [中文文档索引](docs/zh/README.md)

包含：快速开始 / 系统架构 / **Agent 团队配置** / Nightly Pipeline / 个人事务 / 知识库架构 / Obsidian 配置 / OpenClaw 配置 / QMD 语义搜索 / Skills 指南 / 项目管理 / 常见问题

### 📚 Technical Docs (English)
→ [docs/](docs/) directory

---

## 相关项目

- **[Agora](https://github.com/FairladyZ625/Agora)** — 多 Agent 治理框架（民主协商 + 人工审批 + 可审计执行）。Brain OS 提供知识上下文，Agora 提供 Agent 协作结构。Agora 2.0 正在迭代中。

---

## License

MIT © [FairladyZ](https://github.com/FairladyZ625)
