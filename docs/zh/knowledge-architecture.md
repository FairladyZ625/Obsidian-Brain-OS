> 本文档为英文版的中译本。如有歧义，以英文原版为准。

# 知识架构 — 知识库如何组织

---

## Brain OS 解决的问题

大多数个人知识系统失败，因为它们混淆了三件事：
1. **你在阅读的**（策划的、精修的内容）
2. **AI 在处理的**（原始输入、草稿、进行中的工作）
3. **系统如何运作**（索引、状态、报告）

当这些重叠时，你的知识库变成半成品笔记、重复条目和处理副产品的混乱堆。

Brain OS 用**物理分离**解决这个问题。

---

## 三层架构

### 第 1 层：READING — 你读的内容

```
03-KNOWLEDGE/01-READING/
├─ 01-DOMAINS/        ← 领域知识卡片（AI + 你）
├─ 02-TOPICS/         ← 主题聚合页（AI）
├─ 03-PATTERNS/       ← 已验证的模式卡片（AI + 你）
└─ 04-DIGESTS/        ← 日/周摘要（AI 自动生成）
```

**这是你每天开始的地方。** 打开 `04-DIGESTS/` 看看有什么新内容。

| 子目录 | 内容 | 示例 |
|--------|------|------|
| `01-DOMAINS/` | 按领域组织的知识卡片 | `ai-agents.md`、`distributed-systems.md` |
| `02-TOPICS/` | 跨领域主题页 | `llm-reliability.md`、`prompt-engineering.md` |
| `03-PATTERNS/` | 从经验中提取的可复用模式 | `retry-with-exponential-backoff.md` |
| `04-DIGESTS/` | AI 生成的日/周摘要 | `nightly-digest-2026-04-07.md` |

### 第 2 层：WORKING — AI 的工作坊

```
03-KNOWLEDGE/02-WORKING/
├─ 01-ARTICLE-NOTES/        ← 原始文章输入（你的捕捉点）
├─ 02-PATTERN-CANDIDATES/   ← 等待验证的模式
├─ 03-TOPIC-DRAFTS/         ← 进行中的主题页
└─ 04-RESEARCH-QUESTIONS/   ← 开放研究问题
```

**你很少需要看这里。** 这是 AI 的工作空间。

| 子目录 | 这里发生什么 |
|--------|-------------|
| `01-ARTICLE-NOTES/` | 新文章落在这里（你或 AI 创建） |
| `02-PATTERN-CANDIDATES/` | AI 起草模式，你验证后提升到 `03-PATTERNS/` |
| `03-TOPIC-DRAFTS/` | AI 起草主题页，你审核后发布到 `02-TOPICS/` |
| `04-RESEARCH-QUESTIONS/` | 可能成为研究主题的开放问题 |

### 第 3 层：SYSTEM — Pipeline 内部

```
03-KNOWLEDGE/99-SYSTEM/
├─ 01-INDEXES/               ← 自动生成的索引
├─ 02-EXTRACTIONS/           ← 提取的事实/片段
├─ 03-INTEGRATION-REPORTS/   ← Pipeline 运行报告
├─ 04-JOB-STATE/             ← Pipeline 状态检查点
└─ 05-META/                  ← Schema、元数据、路径映射
```

**你永远不需要看这里。** 完全是 AI 内部使用。

---

## 知识流

```
你读了一篇文章
        │
        ▼
02-WORKING/01-ARTICLE-NOTES/
( 带有 frontmatter 的原始捕捉 )
        │
   [02:00 Pipeline]
        │
        ├─→ 01-READING/01-DOMAINS/   (新建/更新知识卡片)
        ├─→ 01-READING/02-TOPICS/    (主题页更新)
        ├─→ 01-READING/03-PATTERNS/  (如果检测到模式)
        └─→ 01-READING/04-DIGESTS/   (摘要条目)
        │
   [04:00 Pipeline]
        │
        └─→ 添加交叉引用
        └─→ 填充"今日推荐阅读"
```

---

## 文章笔记生命周期

```
pending     → 原始捕捉，刚创建
             │
             ▼
integrated  → Pipeline 已处理，知识已提取
             │
             ▼
archived    → 不再被活跃引用
             （保留以供搜索）
```

---

## 领域知识卡片格式

```yaml
---
title: "AI Agent 架构"
date: 2026-04-07
domain: AI-Agent
status: active        # active | archived | draft
tags: [agents, architecture, design-patterns]
source_type: curated  # article | curated | synthesized
related_notes:
  - [[tool-use-patterns]]
  - [[llm-reliability]]
updated: 2026-04-07
---

# AI Agent 架构

## 一句话
构建可靠 AI agent 系统的常见架构模式。

## 核心概念
- ReAct 循环
- Tool calling
- 记忆管理
- 错误处理模式

## 模式
- [[retry-with-exponential-backoff]]
- [[graceful-degradation]]

## 开放问题
- 如何处理工具冲突？
- 最优上下文窗口管理？
```

---

## 最佳实践

### 1. 从摘要开始
不要随机浏览 `01-DOMAINS/`。先查看 `04-DIGESTS/`——AI 会告诉你什么新、什么重要。

### 2. 让 AI 做连接
不要手动创建交叉引用。Pipeline 会自动完成。你只需捕捉输入。

### 3. 提升前先验证
`02-WORKING/` 中的模式候选是 AI 的最佳猜测。在它们成为 `01-READING/` 中的永久内容之前先审核。

### 4. 不要编辑系统文件
`99-SYSTEM/` 完全由 pipeline 管理。你的编辑会被覆盖。

### 5. 归档，不要删除
旧知识卡片应改为 `status: archived`，不要删除。它们仍然对搜索有用。

---

## 系统扩展

随着知识库增长：

| 规模 | 策略 |
|------|------|
| < 100 条笔记 | 无需特殊处理 |
| 100-500 条笔记 | 每周运行 `knowledge-lint.sh` 检查问题 |
| 500+ 条笔记 | 考虑使用 QMD（query-memory-docs）做语义搜索 |
| 1000+ 条笔记 | 增加 lint 频率，考虑领域子目录 |

---

## 与外部工具的集成

- **QMD（query-memory-docs）**：推荐用于大型知识库的语义搜索。作为即插即用的搜索后端。
- **Obsidian**：原生 markdown 渲染、反向链接、图谱视图。
- **OpenClaw**：AI 调度、nightly pipeline 执行、cron jobs。
