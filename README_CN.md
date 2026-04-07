# 🧠 Obsidian Brain OS

> AI 驱动的个人上下文管理系统——开箱即用，深度 Obsidian 原生。

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

[English](README.md) | 中文

---

## 这是什么？

**Obsidian Brain OS** 是一套经过实战打磨的完整框架，用于构建 AI 增强的个人知识系统。不是普通模板——它是可运行的平台：

- 📚 **三层知识架构**（阅读层 / 工作层 / 系统层）
- 🤖 **Nightly AI 流水线**（文章整合 → 对话挖掘 → 知识放大 → 每日摘要）
- 📋 **个人事务系统**（每日驾驶舱、周计划、承诺追踪、早间简报）
- 🛠️ **自动化脚本**（知识审计、摘要初始化、对话导出）
- 🎯 **Agent Skills**（AI 原生 skills，覆盖知识工作流、研究、写作）
- ⏰ **Cron 配置**（7 个开箱即用的定时任务模板）
- 🦭 **安装向导 Skill**（苏格拉底式引导安装）

---

## 快速开始

```bash
# 克隆 & 安装
git clone https://github.com/FairladyZ625/Obsidian-Brain-OS.git
cd Obsidian-Brain-OS
bash setup.sh
```

`setup.sh` 交互式引导完成所有配置：vault 路径、用户信息、skills 安装、cron 生成、验证检查。

`bash setup.sh --test` 可以无痕测试（输出到 `/tmp/brain-os-test/`）。

### 🚀 一键安装（复制这段话发给你的 AI Agent）

不想看文档？**直接复制下面这段话，发给你的 AI Agent**（Claude / ChatGPT / Cursor / OpenClaw / 任何编程助手）。它会自动拉取仓库、阅读安装向导、一步步帮你装好。

```
你好！我想安装 Obsidian Brain OS——一个 AI 驱动的个人上下文管理系统。请帮我：
1. 克隆仓库：git clone https://github.com/FairladyZ625/Obsidian-Brain-OS.git
2. 阅读 skills/brain-os-installer/SKILL.md —— 这是给你的安装指南
3. 按指南帮我配置：问我 vault 放哪、我叫什么、时区等
4. 用我的回答运行 bash setup.sh（或手动一步步来）
5. 装完后读 docs/agents.md，帮我配好 Agent 团队
6. 最后跑一遍 setup.sh 的验证清单确认一切正常
现在就开始吧！
```

→ 完整指南：[docs/zh/README.md](docs/zh/README.md) | [English guide](docs/getting-started.md)

---

## 文档结构

### 📁 目录说明

```
docs/                  ← 英文文档（权威版本）
├── getting-started.md
├── agents.md          ← Agent 团队配置（⭐ 装完必读）
├── architecture.md
├── nightly-pipeline.md
├── ...（共 14 篇）

docs/zh/               ← 中文文档（完整翻译）
├── README.md           ← 中文文档索引
├── agents.md           ← Agent 团队配置指南（详细中文版）⭐
├── chronicle-agent.md  ← 史官系统
├── qmd-setup.md        ← QMD 语义搜索
├── personal-context-guide.md ← 06/07 私密层/工作层
├── ...（与 docs/ 结构完全一致，共 16 篇）
```

**规则**：`docs/` = 英文，`docs/zh/` = 中文。文件名相同，内容相同，语言不同。读哪个都行。

### 📖 建议阅读顺序

1. **[快速开始](docs/getting-started.md)** / **[中文总览](docs/zh/README.md)** — 安装 & 首次运行
2. **[Agent 团队配置](docs/agents.md)** / **[中文详细版](docs/zh/agents.md)** ⭐ — **装完第一件事：配好你的 Agent 团队**
3. **[系统架构](docs/architecture.md)** / **[中文版](docs/zh/architecture.md)**
4. **[个人事务系统](docs/personal-ops.md)** / **[中文版](docs/zh/personal-ops.md)**
5. **[Nightly Pipeline](docs/nightly-pipeline.md)** / **[中文版](docs/zh/nightly-pipeline.md)**
6. **[NotebookLM 集成指南](docs/notebooklm.md)** / **[中文版](docs/zh/notebooklm.md)** — 深度研究
7. **[QMD 语义搜索](docs/qmd-setup.md)** / **[中文版](docs/zh/qmd-setup.md)** — 向量搜索

---

## 包含什么

| 模块 | 说明 |
|------|------|
| `vault-template/` | 完整 Obsidian vault 模板（8 个目录） |
| `setup.sh` | 交互式安装脚本（支持 `--test` 无痕模式） |
| `scripts/` | 自动化脚本（审计、摘要、导出） |
| `prompts/` | Nightly Pipeline 提示词模板（5 个，覆盖率 100%） |
| `skills/` | 7 个核心 + 18 个推荐 Agent Skills |
| `tools/conversation-mining/` | 对话挖掘工具（内嵌，无需额外安装） |
| `cron-examples/` | OpenClaw Cron 配置（7 个 job） |
| `docs/` | 完整英文文档（14 篇） |
| `docs/zh/` | 完整中文文档（16 篇，含 agents/chronicle/qmd 等） |

---

## 设计理念

> **上下文是基础设施。知识是复利。**

1. **捕获** → 所有内容先进 INBOX
2. **处理** → Nightly AI 流水线把原始笔记变成结构化知识
3. **复利** → 跨来源合成让模式自然涌现
4. **行动** → 每日摘要 + 个人事务系统保持推进

AI 不替代你的思考——它处理管道工作，让你专注在真正重要的信号上。

---

## 相关项目

- **[Agora](https://github.com/FairladyZ625/Agora)** — 多 Agent 治理框架。Brain OS 提供知识上下文，Agora 提供 Agent 协作结构。Agora 2.0 迭代中。

---

## License

MIT © [FairladyZ](https://github.com/FairladyZ625)
