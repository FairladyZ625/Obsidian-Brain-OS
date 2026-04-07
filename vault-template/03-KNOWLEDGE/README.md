# 🧠 03-KNOWLEDGE — 知识库

> **三层架构：READING（读） / WORKING（做） / SYSTEM（系统）**

---

## 默认阅读入口

**从 `01-READING/04-DIGESTS/` 开始** — 这是 AI 每天为你生成的精华摘要，最省脑子。

```
04-DIGESTS/ ← 从这里开始
    ↓
02-TOPICS/ ← 按主题深入
    ↓
01-DOMAINS/ ← 领域知识卡
    ↓
03-PATTERNS/ ← 提炼出的规律
```

---

## 目录结构

### 01-READING/ — 你默认看的内容
| 目录 | 用途 | 谁写 |
|------|------|------|
| `01-DOMAINS/` | 领域知识卡（AI-Agent / AI-Infra / 等） | AI + 你 |
| `02-TOPICS/` | 主题聚合入口页 | AI |
| `03-PATTERNS/` | 已验证的规律卡片 | AI + 你 |
| `04-DIGESTS/` | 每日/每周摘要 | AI（nightly pipeline 自动生成） |

### 02-WORKING/ — 半成品，不要直接从这里读
| 目录 | 用途 |
|------|------|
| `01-ARTICLE-NOTES/` | 原始文章处理区（输入源） |
| `02-PATTERN-CANDIDATES/` | 待验证的规律候选 |
| `03-TOPIC-DRAFTS/` | 主题页草稿 |
| `04-RESEARCH-QUESTIONS/` | 开放研究问题 |

### 99-SYSTEM/ — AI pipeline 中间产物（不需要看）
| 目录 | 用途 |
|------|------|
| `01-INDEXES/` | 自动生成的索引 |
| `02-EXTRACTIONS/` | 从文章提取的事实/片段 |
| `03-INTEGRATION-REPORTS/` | Nightly pipeline 运行报告 |
| `04-JOB-STATE/` | Pipeline 状态检查点 |
| `05-META/` | Schema、元数据、路径映射 |

---

## 核心设计原则

1. **物理隔离中间产物** — 99-SYSTEM/ 里的东西你不需要直接看
2. **不混淆输入与输出** — ARTICLE-NOTES 是原料，DOMAINS 是成品
3. **AI 负责搬运，你负责方向** — pipeline 自动把 WORKING 提炼成 READING
