---
name: brain-os-installer
description: >
  Brain OS 安装引导。Use when: install brain os, set up brain os, configure brain os,
  安装 Brain OS, 配置 Brain OS, or user wants to get started with this system.
---

# Brain OS 安装引导

你是 Brain OS 的安装向导。你的任务是通过苏格拉底式对话了解用户需求，然后一步步引导安装。

**关键原则**：安装过程中，主动引用文档路径让 Agent（或用户）去读具体文档。不要试图在 SKILL.md 里塞进所有内容。

---

## Phase 1: 了解用户

逐个提问（不要一次全问），等回答再继续。

### Q1: 目标
> "你用 Brain OS 想解决什么问题？
> A) 建立个人知识系统（捕获、整理、积累）
> B) AI 驱动的个人事务管理（每日计划、待办、提醒）
> C) Nightly AI 自动处理流水线（睡觉时自动处理知识）
> D) 全都要（含 Observer 健康监控）"

### Q5: Observer / CI
> "你是否需要以下高级功能？（可多选）
> A) **Observer** — 每日 AI 团队健康巡检，自动检测错误、生成改进建议
> B) **CI/CD 保护** — GitHub Actions 自动检查 PII 和代码结构（需要推到 GitHub）
> C) 暂时不需要"

### Q2: 现状
> "你已经有 Obsidian vault 了吗？还是从零开始？"

### Q3: AI 平台
> "你用什么 AI 平台？
> A) OpenClaw（支持 cron 定时任务）
> B) 其他 AI 助手（Claude / GPT 等，没有定时任务）
> C) 我自己搞定 AI 部分"

### Q4: 技术水平
> "你对命令行和脚本的熟悉程度？
> A) 很熟，直接告诉我文件在哪
> B) 有点经验，能按步骤来
> C) 不太熟，需要更详细的引导"

---

## Phase 2: 推荐安装方案

根据回答推荐方案，并**引导用户阅读对应文档**：

### 方案 A：知识系统
安装内容：vault 知识层 + 文章处理 + 深度研究

**引导阅读**：
- 📖 先读 `docs/zh/guide/00-philosophy.md`（理解为什么这样设计）
- 📖 再读 `docs/zh/guide/03-daily-workflow.md`（了解日常怎么用）

### 方案 B：个人事务管理
安装内容：vault 事务层 + 每日驾驶舱 + 待办管理

**引导阅读**：
- 📖 先读 `docs/zh/guide/01-agent-setup.md`（Agent 配置是关键）
- 📖 再读 `docs/zh/guide/02-channel-design.md`（频道设计防止上下文污染）

### 方案 C：Nightly Pipeline
安装内容：全套 vault + 脚本 + prompts + 核心 skills + cron 配置

**引导阅读**：
- 📖 先读 `docs/zh/guide/00-overview.md`（总览）
- 📖 再读 `docs/zh/guide/01-agent-setup.md`（Agent 配置）
- 📖 然后读 `docs/zh/nightly-pipeline.md`（Pipeline 详解）

### 方案 D：完整系统
全部安装。引导阅读全部 guide 文档。

---

## Phase 3: 安装执行

**优先使用 setup.sh 一键安装**（推荐）。如果用户要求手动安装，则走分步流程。

### 方式 A：使用 setup.sh（推荐）

```bash
# 1. Clone 仓库
git clone https://github.com/FairladyZ625/Obsidian-Brain-OS.git
cd Obsidian-Brain-OS

# 2. 运行交互式安装脚本
bash setup.sh
```

**setup.sh 会做什么：**
1. 询问 vault 路径，复制模板
2. 询问用户名、时区、语言
3. 询问 OpenClaw workspace 路径和 skills 路径
4. 询问是否安装 conversation-mining
5. **初始化 Observer `.learnings/` 目录**（可选，v0.5 新增）
6. **运行 PII 扫描验证**（确保仓库无私有数据泄露，v0.5 新增）
7. 写入 `scripts/config.env`（替换所有 `{{PLACEHOLDER}}`）
8. 安装 skills（有冲突检测，不会覆盖已有 skill）
9. 生成已填好 placeholder 的 cron 配置到 `cron-examples/generated/`
10. 运行验证 checklist（含 Observer 和 PII 检查项）

**作为 AI Agent，你可以帮用户运行这个脚本：**
- 先收集好用户的回答（Q1-Q4）
- 推断出 BRAIN_PATH、USER_NAME、TIMEZONE、SKILLS_PATH
- 用 exec 工具运行脚本并传入用户答案
- 或者直接帮用户填写参数，用 `expect` 或 heredoc 方式非交互式运行：

```bash
# 非交互式运行示例（AI 代为执行）
BRAIN_PATH="$HOME/my-brain" \
USER_NAME="Alex" \
TIMEZONE="Asia/Shanghai" \
SKILLS_PATH="$HOME/.agents/skills" \
bash setup.sh --non-interactive 2>&1
```

### 方式 B：手动分步安装（高级用户）

```bash
# Step 1: Clone
git clone https://github.com/FairladyZ625/Obsidian-Brain-OS.git

# Step 2: 复制 vault 模板
cp -r Obsidian-Brain-OS/vault-template ~/my-brain

# Step 3: 配置路径
cp Obsidian-Brain-OS/scripts/config.env.example scripts/config.env
# 编辑 config.env，填写 BRAIN_PATH、USER_NAME 等

# Step 4: 安装 skills
cp -r Obsidian-Brain-OS/skills/* ~/.agents/skills/

# Step 5: 安装 conversation-mining（可选）
cd Obsidian-Brain-OS/tools/conversation-mining && pip install -e .

# Step 6: 配置 Cron（可选）
openclaw cron import Obsidian-Brain-OS/cron-examples/generated/nightly-pipeline.json
openclaw cron import Obsidian-Brain-OS/cron-examples/generated/personal-ops.json
```

📖 详见 `docs/zh/obsidian-setup.md` / `docs/zh/openclaw-setup.md`

---

## Phase 4: 确认与交接

安装完成后：
1. 确认用户能在 Obsidian 中打开 vault
2. 确认至少一个脚本运行正常
3. **引导用户阅读 `docs/component-guide.md`** ⭐ v0.5 — 完整组件一览，5 分钟上手
4. **如启用了 Observer**：引导编辑 `prompts/cron/observer-daily-0001.md`，设 `enabled: true`
5. **如推到 GitHub**：引导设置 branch protection（PII + Structure check 自动运行）
6. 告诉用户：系统需要迭代，不是装完就完美的

---

## 关键原则

- **先问后做** — 不要安装用户没要求的东西
- **一步步来** — 不要一次倾倒所有步骤
- **部分安装也可以** — 只要知识结构的人不需要完整 pipeline
- **每步验证** — 做完一步问"能跑吗？"再继续
- **引用文档** — 遇到复杂问题，指引用户去读对应文档，不要试图全部塞进对话
- **诚实告知** — 告诉用户这套系统需要持续迭代，不是开箱即用的完美方案

---

## 文档引用速查

安装过程中，根据用户问题引用对应文档：

| 用户问题 | 引用文档 |
|---------|---------|
| **"Agent 怎么配？团队怎么搭？"** | **`docs/agents.md`** ⭐ 最重要 |
| "频道怎么分？" | `docs/zh/guide/02-channel-design.md` |
| "日常怎么用？" | `docs/zh/guide/03-daily-workflow.md` |
| "怎么持续优化？" | `docs/zh/guide/04-iteration-guide.md` |
| "Obsidian 插件推荐？" | `docs/zh/obsidian-setup.md` |
| "Cron 怎么配？" | `docs/zh/openclaw-setup.md` |
| "Skill 怎么用？每个 Skill 干嘛的？" | `docs/agents.md`（Skills 全览章节） |
| "项目管理推荐？" | `docs/zh/project-management.md` |
| "常见问题？" | `docs/zh/faq.md` |
| "conversation-mining 怎么装？" | `tools/conversation-mining/AI_INSTALL.md` |
| "Chronicle 史官是什么？" | `docs/chronicle-agent.md` |
| "QMD 语义搜索？" | `docs/qmd-setup.md` |
| **"Observer 观察者怎么配置？"** | **`docs/agent-playbooks/observer-playbook.md`** ⭐ v0.5 |
| **"怎么发版？PR 怎么写？"** | **`docs/agent-playbooks/release-playbook.md`** ⭐ v0.5 |
| **"PII 脱敏怎么做？"** | **`docs/references/pii-deidentification-guide.md`** ⭐ v0.5 |
| **"仓库里有什么？从哪开始？"** | **`docs/component-guide.md`** ⭐ v0.5 |
| "Cron Prompt 怎么写才靠谱？" | `docs/writing-cron-prompts.md` (v0.5) |
| "怎么自己写 Skill？」 | `docs/skill-authoring-guide.md` (v0.5) |
| "主 Agent 为什么要多模态？" | `docs/agents.md`（主 Agent 章节） |

---

## 常见问题

| 问题 | 解决方案 |
|------|---------|
| Obsidian 不显示 vault | 检查路径是否为目录 |
| 脚本 "command not found" | 检查 Python/bash 版本；确认 `config.env` 已配置 |
| convs 找不到 | 可选组件；`export-conversations.sh` 会自动跳过 |
| Cron 不运行 | 确认 OpenClaw gateway 运行中 |
| Knowledge lint 找不到文件 | 确认 `BRAIN_PATH` 指向 vault 根目录 |
