# 架构设计 — Obsidian Brain OS

> 本文档为英文版的中译本。如有歧义，以英文原版为准。

> 系统是如何组织的、为什么这样组织、各部件如何协同工作。

---

## 设计理念

### 1. 捕获一次，处理无限
一切从 `00-INBOX/` 进入。AI 负责路由、分类和整合。你只需专注于捕获。

### 2. 阅读层与工作层分离
知识被分为两个物理层：
- **READING/** — 你实际阅读的内容（精炼、精选）
- **WORKING/** — AI 的工作间（原始输入、草稿、候选内容）

这解决了"知识墓地"问题——有价值的内容不会被处理过程中的产物埋没。

### 3. Pipeline 优于手动整理
夜间 pipeline（02:00-04:00）自动完成：
1. 将新文章笔记整合到领域知识中
2. 从对话中挖掘洞见
3. 通过建立关联来放大知识

你不需要手动整理。醒来就是整理好的知识。

### 4. 轻量项目注册层，重型外部工具
`04-PROJECTS/` 是一个轻量索引——项目名、一句话说明、状态、外部链接。Agora 负责多 agent 治理；Linear/GitHub Issues 负责任务跟踪。Brain OS 提供知识上下文，但不试图替代它们。

---

## 系统地图

```
┌─────────────────────────────────────────────────────────┐
│                    INPUT LAYER                           │
│  00-INBOX/          所有新条目从这里进入                  │
│  ├─ todo-backlog    待办事项的唯一真相源                  │
│  └─ archive/        已归档待办（按月）                    │
├─────────────────────────────────────────────────────────┤
│                 PERSONAL CONTEXT                         │
│  01-PERSONAL-OPS/   AI 驱动的个人生活管理                 │
│  ├─ 01-DAILY-BRIEFS   早间驾驶舱（自动生成）              │
│  ├─ 02-PLANS           周计划/月计划                    │
│  ├─ 03-TODOS           承诺、决策、进度                  │
│  ├─ 04-REVIEWS         复盘                            │
│  └─ 05-OPS-LOGS        频道历史、日常日志                │
├─────────────────────────────────────────────────────────┤
│                    KNOWLEDGE LAYER                       │
│  03-KNOWLEDGE/      三层知识架构                         │
│  ├─ 01-READING/                                        │
│  │   ├─ 01-DOMAINS/     领域知识卡片                    │
│  │   ├─ 02-TOPICS/      主题聚合页面                   │
│  │   ├─ 03-PATTERNS/    已验证的模式卡片                │
│  │   └─ 04-DIGESTS/     日/周摘要（从这里开始阅读）       │
│  ├─ 02-WORKING/        AI 工作间（不要直接阅读）          │
│  │   ├─ 01-ARTICLE-NOTES/  原始文章输入                │
│  │   ├─ 02-PATTERN-CANDIDATES/  审核中的模式候选         │
│  │   ├─ 03-TOPIC-DRAFTS/      进行中的主题页面          │
│  │   └─ 04-RESEARCH-QUESTIONS/  开放研究问题            │
│  └─ 99-SYSTEM/         Pipeline 内部（仅 AI 可读）        │
│      ├─ 01-INDEXES/          自动生成的索引              │
│      ├─ 02-EXTRACTIONS/      提取的事实/片段             │
│      ├─ 03-INTEGRATION-REPORTS/  Pipeline 运行报告      │
│      ├─ 04-JOB-STATE/        Pipeline 状态检查点        │
│      └─ 05-META/             Schema、元数据、映射         │
├─────────────────────────────────────────────────────────┤
│                  SUPPORT LAYERS                          │
│  02-TEAM/           团队协作规则                           │
│  04-PROJECTS/       轻量项目注册表                       │
│  06-PERSONAL-DOCS/  私人文档（gitignored）               │
│  07-WORK-CONTEXT/   工作经历与上下文                     │
├─────────────────────────────────────────────────────────┤
│                  CONFIGURATION                           │
│  config/            Brain 级配置                         │
│  memory/            AI agent 记忆（每日日志）              │
│  templates/         文档模板                            │
└─────────────────────────────────────────────────────────┘
```

---

## 夜间 Pipeline

```
22:00  用户在一天中捕获文章、对话、想法
       │
02:00  ┌─ Article Integration ─────────────────────────────┐
       │  读取: 02-WORKING/01-ARTICLE-NOTES/              │
       │  写入: 01-READING/01-DOMAINS/, 02-TOPICS/        │
       │  输出: 摘要小节 + 运行报告                         │
       └───────────────────────────────────────────────────┘
       │
03:00  ┌─ Conversation Mining ─────────────────────────────┐
       │  读取: 导出的 AI 对话记录（最近 3 天）              │
       │  写入: 知识笔记、模式候选                          │
       │  输出: 摘要小节 + 运行报告                         │
       └───────────────────────────────────────────────────┘
       │
04:00  ┌─ Knowledge Amplification ─────────────────────────┐
       │  读取: 今日摘要 + 领域知识                         │
       │  写入: 关联、交叉引用、更新                        │
       │  输出: 最终摘要 + 推荐                             │
       └───────────────────────────────────────────────────┘
       │
05:00  每日知识图谱画布（可选）
07:00  生成早间简报供个人 ops 使用
       │
08:00  用户醒来，阅读摘要，开始新的一天
```

每个阶段：
1. 在隔离的 AI 会话中运行（不影响主会话）
2. 写入**共享夜间摘要**（`04-DIGESTS/nightly-digest-YYYY-MM-DD.md`）
3. 写入**机器可读的运行报告**（`99-SYSTEM/03-INTEGRATION-REPORTS/`）
4. 将更改提交到 Brain git 仓库

如果某阶段没有需要处理的内容，则写入无操作报告并继续。没有强制输出。

---

## 个人 Ops 系统

```
┌──────────────────────────────────────────┐
│  00-INBOX/todo-backlog.md                │
│  （一切从这里进入）                        │
│              │                           │
│              ▼                           │
│  01-PERSONAL-OPS/                        │
│  ├─ 01-DAILY-BRIEFS/daily-briefing.md   │
│  │   （每天早上自动生成）                 │
│  ├─ 03-TODOS-AND-FOLLOWUPS/             │
│  │   ├─ 当前承诺事项.md                   │
│  │   ├─ progress-board.md               │
│  │   └─ decision-queue.md               │
│  └─ 02-PLANS-AND-SCHEDULES/             │
│      ├─ weekly-plan.md                  │
│      └─ monthly-milestones.md           │
└──────────────────────────────────────────┘
```

**流程：**
1. 新条目 → `todo-backlog.md`（P0/P1/P2/P3 优先级排序）
2. 早间简报 AI 读取待办 + 承诺 + 决策 → 生成今日驾驶舱
3. 晚间提醒（15:00、20:00）提示回顾
4. 周计划（周一）+ 月里程碑（每月 1 日）提供更长视野

---

## 项目管理（可选）

Brain OS 提供**轻量项目注册表**（`04-PROJECTS/`）——仅为 AI 提供你正在做什么的上下文。

真正的项目管理，推荐搭配：
- **[Agora](https://github.com/FairladyZ625/Agora)** — 多 agent 治理框架（审议 → 决策 → 执行）
- Linear、GitHub Issues，或任何你喜欢的任务跟踪器

项目简报模板包含：
- 项目名称和一句话说明
- 当前阶段和重点
- 外部系统链接（真相源在其他地方）
- Brain 中相关的知识条目

---

## 知识架构

### 为什么是三层？

大多数知识系统混入了输入、处理和输出。这造成了混乱。

Brain OS 将它们物理分离：

| 层级 | 用途 | 谁来阅读？ | 谁来写入？ |
|------|------|-----------|-----------|
| READING | 你实际阅读的精选知识 | 你 + AI | AI（pipeline） |
| WORKING | 原始输入、草稿、候选内容 | 仅 AI | 你 + AI |
| SYSTEM | Pipeline 状态、索引、报告 | 仅 AI | AI（pipeline） |

### 知识流

```
文章 URL → 02-WORKING/01-ARTICLE-NOTES/
                    │
              [02:00 Pipeline]
                    │
                    ├─→ 01-READING/01-DOMAINS/  (领域知识卡片)
                    ├─→ 01-READING/02-TOPICS/   (更新主题页面)
                    ├─→ 01-READING/03-PATTERNS/ (如检测到模式)
                    └─→ 01-READING/04-DIGESTS/  (今日摘要)
```

### 入口点

**始终从 `04-DIGESTS/` 开始**——这是 AI 总结新内容和值得阅读内容的地方。如果你看到感兴趣的内容，再深入 DOMAINS 或 TOPICS。

---

## 文件命名规范

| 类型 | 格式 | 示例 |
|------|------|------|
| 每日简报 | `daily-briefing.md`（每日覆盖） | — |
| 夜间摘要 | `nightly-digest-YYYY-MM-DD.md` | `nightly-digest-2026-04-07.md` |
| 文章笔记 | `YYYY-MM-DD-topic.md` | `2026-04-07-building-pks-with-ai.md` |
| 领域卡片 | `topic-name.md` | `ai-agents.md` |
| 项目简报 | `project-name.md` | `personal-blog.md` |
| 周计划 | `weekly-plan.md`（每周覆盖） | — |
| 待办归档 | `todo-archive-YYYY-MM.md` | `todo-archive-2026-04.md` |
