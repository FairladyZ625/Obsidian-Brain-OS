# 🧠 Obsidian Brain OS

> [Karpathy 的 LLM Wiki](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) 概念的完整实现——自动化、多 Agent、生产就绪。

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

[English](README.md) | 中文

---

## 核心概念（来自 Andrej Karpathy）

> *“与其每次查询时都从原始文档中检索，不如让 LLM 增量构建和维护一个持久化的 wiki——一个结构化的、相互链接的 markdown 文件集合，位于你和原始来源之间……wiki 会随着你添加的每个来源和提出的每个问题而不断丰富。”*
>
> *“Obsidian 是 IDE；LLM 是程序员；wiki 是代码库。”*
>
> — [Andrej Karpathy, llm-wiki (2025)](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)

**Obsidian Brain OS 是这个概念的完整实现**——在此基础上叠加了自动化流水线、多 Agent 团队、个人事务系统和生产级工具链。

### Karpathy 描述了什么 → Brain OS 实现了什么

| Karpathy 的概念 | Brain OS 的实现 |
|----------------|----------------|
| Raw sources 层 | `00-INBOX/` + 文章笔记摄入 |
| The wiki（LLM 维护） | `03-KNOWLEDGE/`（三层：阅读/工作/系统） |
| The schema（AGENTS.md） | `skills/` + `AGENTS.md` + `SOUL.md` |
| Ingest 工作流 | `article-notes-integration` skill + Nightly Pipeline |
| Query 工作流 | QMD 语义搜索 + 每日摘要 |
| Lint 工作流 | `knowledge-lint.sh` + 每周巡检 cron |
| LLM 写入，你浏览 | Agent 写 vault；你在 Obsidian 中浏览 |
| 知识复利增长 | 通过 `knowledge-flywheel-amplifier` 跨源综合 |
| 不重复推导 | 所有模式、交叉引用编译一次并保持最新 |

### Brain OS 在此基础上增加了什么

Karpathy 的 gist 描述的是*想法*。Brain OS 是*运行中的系统*：

- 🤖 **多 Agent 团队**：主调度 + 写入者 + 史官 + 巡检官
- 🔭 **Observer（自我进化观察者）**：每日 AI 团队健康巡检——采集 session 数据与网关日志，检测反复出现的错误，生成系统改进建议，维护运行记忆账本。三级安全机制：仅告警 → 建议修复 → 经人工确认后执行。[Observer 使用手册 →](docs/agent-playbooks/observer-playbook.md)
- ⏰ **夜间自动化**：4 阶段流水线在你睡觉时自动运行
- 📋 **个人事务层**：每日驾驶舱、待办跟踪、承诺管理、早间简报
- 🍎 **Apple 提醒事项集成**：Brain 待办与 Apple 提醒事项双向同步，早上推送、晚上回写
- 📋 **每日工时自动填报**：扫描 git 提交 + 项目上下文，对齐 OKR/里程碑，生成草稿待确认——支持文件 / 飞书 / 钉钉多种写入方式
- 🔬 **深度研究集成**：NotebookLM + deep-research skill 做 Stage 0 研究
- 🎯 **22+ Agent Skills**：预置指令集覆盖所有工作流
- 🔒 **治理体系**：单一写入入口、可审计 commit、QMD 语义搜索
- 🚀 **一键安装**：`bash setup.sh` — 交互式引导 + 批量占位符替换

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

## 文档

### 📋 贡献者与维护者文档

1. **[组件全览指南 (⭐ 从这里开始)](docs/component-guide.md)** ⭐ — 仓库包含的所有内容、每个组件的作用、5 分钟快速上手
2. **[发版操作手册](docs/agent-playbooks/release-playbook.md)** ⭐ — 完整发版 SOP（中英双语）
3. **[观察者使用手册](docs/agent-playbooks/observer-playbook.md)** — Observer skill 配置指南
4. **[PII 脱敏指南](docs/references/pii-deidentification-guide.md)** — 如何避免私有数据进入仓库
5. **[Cron Prompt 编写指南](docs/writing-cron-prompts.md)** — 可靠 cron prompt 最佳实践
6. **[Skill 编写指南](docs/skill-authoring-guide.md)** — 如何编写结构良好的 skill
7. **[Nightly Pipeline 全景指南](docs/nightly-pipeline-guide.md)** — 完整流水线架构与交接协议

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
| `scripts/` | 自动化脚本（审计、摘要、导出、提醒事项同步、工时填报） |
| `prompts/` | Nightly Pipeline 提示词模板（8 个，覆盖率 100%） |
| `skills/` | 9 个核心 + 18 个推荐 Agent Skills |
| `tools/conversation-mining/` | 对话挖掘工具（内嵌，无需额外安装） |
| `cron-examples/` | OpenClaw Cron 配置（7 个 job） |
| `docs/` | 完整英文文档（14 篇） |
| `docs/zh/` | 完整中文文档（16 篇，含 agents/chronicle/qmd 等） |

---

## 🍎 Apple 提醒事项集成

Brain OS 内置了 Brain 待办与 Apple 提醒事项的**双向同步**——让你的知识库与原生任务管理器保持连通。

### 工作原理

```
07:30 → brain-to-reminders.sh
         从 daily-briefing.md 提取今日优先事项
         推送到 Apple 提醒事项（「Brain今日」列表）
         → iPhone / Apple Watch 上可直接看到 Brain 待办

21:00 → reminders-to-brain.sh
         从 Apple 提醒事项读取完成状态
         将同步报告写回 Brain
         → 已完成事项在晚间复盘中得到反映
```

### 配置方法

1. 安装 [`remindctl`](https://github.com/nicholasgasior/remindctl) — Apple 提醒事项的命令行工具
2. 在 `config.env` 中配置列表名：
   ```bash
   REMINDERS_LIST="Brain今日"   # 或任意列表名
   ```
3. 添加两个 cron 任务：`prompts/cron/brain-to-reminders-0730.md` 和 `prompts/cron/reminders-to-brain-2100.md`
4. 手动测试：
   ```bash
   bash scripts/brain-to-reminders.sh
   bash scripts/reminders-to-brain.sh
   ```

### 同步内容

- **早上（07:30）**：从 `daily-briefing.md` 提取今日优先事项 → 推送到提醒事项（带截止时间）
- **晚上（21:00）**：回写完成状态 → 同步报告写入 `01-PERSONAL-OPS/05-OPS-LOGS/`
- **去重**：已存在的提醒事项自动跳过
- **过期跟踪**：未完成的过期事项在晚间报告中标记

> **仅支持 macOS。** 需要 `remindctl` 和 Apple 提醒事项 App。

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
