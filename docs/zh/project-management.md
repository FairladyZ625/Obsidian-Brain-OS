> 本文档为英文版的中译本。如有歧义，以英文原版为准。

# 项目管理 — 轻量注册与工具推荐

---

## Brain OS 的项目管理理念

Brain OS 不是项目管理工具。它是一个**个人上下文系统**。

对于项目管理，Brain OS 提供：
1. **轻量项目注册**（`04-PROJECTS/`）——刚好足够给 AI 上下文
2. **外部工具的集成推荐**

---

## 轻量项目注册

### 何时使用

- 你的项目上下文不到 5 行
- 你想让 AI 知道你在做什么
- 你需要快速参考外部项目链接

### 何时不使用

- 你需要看板、燃尽图或冲刺规划
- 你在管理有多个贡献者的团队
- 你需要带分配和截止日的 issue 跟踪

→ 请使用外部工具。

---

## 项目简介格式

每个项目在 `04-PROJECTS/01-ACTIVE/` 中有一个 markdown 文件：

```yaml
---
title: "My Project"
date: 2026-04-07
project_ref: "my-project"
status: active          # active | paused | completed
source_of_truth: "https://github.com/user/repo"
owner: "{{USER_NAME}}"
tags: [web, side-project]
---

# My Project

## 一句话
Build a personal blog with AI-powered content suggestions.

## 当前阶段
MVP 开发

## 当前焦点
搭建文章生成 pipeline。

## 真相源
- 代码：`https://github.com/user/my-blog`
- 任务：`https://github.com/user/my-blog/issues`
- 文档：`{{BRAIN_PATH}}/04-PROJECTS/01-ACTIVE/my-project.md`

## 相关知识
- [[content-generation-patterns]]
- [[ai-writing-assistants]]

## 关键决策
| 日期 | 决策 | 原因 |
|------|------|------|
| 2026-04-01 | 使用 Astro 框架 | 最佳静态站点性能 |

## 搜索关键词
my-blog, astro, content-generation, side-project
```

---

## 推荐的外部工具

### 1. Agora — 多 Agent 治理框架

**最适合：** 用结构化审议和人工门控决策来编排多个 AI agent。

Agora 是多 agent 系统的编排和治理层。它提供：

- **分阶段审议** — Citizens（agent）辩论，Archon（人类）决策，Craftsman（执行者）交付
- **明确的治理语义** — 不是 prompt 民间传说，而是结构化编排
- **人工门控决策** — 只有人工批准后才开始执行
- **可审计交付** — 聊天记录 ≠ 交付；Agora 跟踪实际成果

**如何与 Brain OS 配合：**

| Brain OS | Agora |
|----------|-------|
| 个人知识与上下文 | 多 agent 编排 |
| 你知道什么 | agent 如何协作 |
| 单用户知识管理 | 多 agent 治理 |
| Vault 是知识存储 | Agora 是决策竞技场 |

Brain OS 的项目简介给 agent 提供他们在做什么的**上下文**。Agora 给他们提供如何协作的**结构**。

**集成模式：**
1. 在 `04-PROJECTS/` 中创建引用 Agora 任务 URL 的项目简介
2. Agora agent 在处理任务时从 Brain OS 读取项目上下文
3. Agora 审议期间生成的知识回流到 `03-KNOWLEDGE/`

**仓库：** [github.com/FairladyZ625/Agora](https://github.com/FairladyZ625/Agora)

### 2. Linear

**最适合：** 需要快速、现代 issue 跟踪的软件团队。

干净的界面，出色的键盘快捷键，优秀的 API。将任务链接到 Brain OS 项目简介。

### 3. GitHub Issues / Projects

**最适合：** 已在 GitHub 上的开源项目或团队。

无需额外设置。在项目简介中引用 issue URL。

---

## 集成模式

```
Brain OS (04-PROJECTS/)
    │
    │  "我在做什么？"
    │  AI 读取项目简介获取上下文
    │
    ├──→ Agora / Linear / GitHub Issues
    │    "agent 如何在上面协作？"
    │    治理和任务跟踪在这里
    │
    └──→ 03-KNOWLEDGE/
         "我学到了什么？"
         项目工作中的知识流入这里
```

---

## 项目生命周期

```
01-ACTIVE/      ← 当前进行中
    │
    ├─→ 02-PAUSED/     ← 暂停（附原因）
    │       │
    │       └─→ 01-ACTIVE/  （恢复）
    │
    └─→ 03-COMPLETED/  ← 完成（附回顾笔记）
```

移动项目时：
1. 更新 frontmatter 中的 `status`
2. 将文件移到相应目录
3. 添加关于为什么移动的简短说明
4. 对于已完成的项目：将关键经验添加到 `03-KNOWLEDGE/`
