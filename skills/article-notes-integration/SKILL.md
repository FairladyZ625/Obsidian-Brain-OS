---
name: article-notes-integration
description: >
  Nightly pipeline for integrating newly captured external article notes into
  Brain knowledge surfaces. Use when: 文章整合, article notes integration,
  nightly article sync, update article relations, topic index update,
  article knowledge graph, 前一天文章整理, 或 run the 02:00 article pipeline.
---

# Article Notes Integration

把前一天新增或待整合的 Article Notes，转成可检索、可关联、可继续提炼的 Brain 知识输入层。

## Purpose

这个技能负责 **文章 ingestion 之后的 nightly integration**，而不是原始外部文章采集本身。

它处理的是：
1. 扫描昨天新增或尚未 integrated 的 article notes
2. 校验并补足结构 / frontmatter / relation 状态
3. **交叉引用更新**（见下方 Cross-Reference Protocol，每次 ingest 后执行）
4. 更新 topic / domain / project 相关的轻量图谱入口
5. 生成 open questions / pattern candidates / article-derived graph signals
6. 输出高价值 article candidates，供后续 flywheel amplification 使用

## Primary Inputs

- Brain root: `{{BRAIN_ROOT}}`
- Source notes: `03-KNOWLEDGE/02-WORKING/01-ARTICLE-NOTES/`
- Candidate set:
  - 前一天新增 article notes
  - 或 `integration_status != integrated` 的 article notes
- Read-only context:
  - related domain notes
  - `03-KNOWLEDGE/99-SYSTEM/01-INDEXES/` 下已有 topic / topic-map / open-question surfaces
  - `05-PROJECTS/` 下 project briefs（若能稳定识别项目）

## Required Outputs

A successful run should produce some or all of:
- 1 machine-facing run report → `03-KNOWLEDGE/99-SYSTEM/03-INTEGRATION-REPORTS/YYYY-MM-DD/article-integration-report-YYYY-MM-DD.md`
- 1 human-facing digest section append → `03-KNOWLEDGE/01-READING/04-DIGESTS/nightly-digest-YYYY-MM-DD.md`
- article note frontmatter / relation field updates
- topic index / topic map updates when justified
- open question / pattern candidate markers when justified
- high-value article candidates for the 04:00 amplifier stage
- Brain git commit + post-commit visibility confirmation

## What This Skill May Read

- Article notes themselves
- Existing Brain knowledge / indexes / project briefs
- Existing relation fields and topic surfaces

## What This Skill May Write

- Article note metadata and relation fields
- Lightweight graph/index surfaces in `03-KNOWLEDGE/99-SYSTEM/01-INDEXES/`
- Candidate-only pattern / open-question surfaces
- Integration reports

## Raw Asset Storage Rule（2026-04-13）

这个 skill 必须严格区分：

### 正式知识层（可提交 Git）
- 提炼后的文章 note `.md`
- relation / topic / open-question / digest / report 等结构化产物

### 原始抓取层（默认不提交 Git）
- 微信/小红书抓下来的整套图片
- OCR 图包
- 原始 PDF / EPUB / Office 附件
- debug html
- `.raw/` / `raw/` 响应
- 任何可再抓取或可再生成的中间素材

### 默认本地落点
统一放到：
- `LOCAL-LARGE-FILES/knowledge-sources/`

例如：
- `LOCAL-LARGE-FILES/knowledge-sources/ai-agent/2026-04-12-harness-survey/`

### 禁止事项
- 不要把 `_images-*`、`images/`、`.raw/`、原始 PDF 当作正式知识产物提交到 Brain Git
- 不要为了“资料完整”把整包截图/附件塞进 `03-KNOWLEDGE/`
- 如果正文需要引用原始资产，只在 note 中写来源链接或本地路径说明

## Cross-Reference Protocol（每次 ingest 后执行）

每次处理文章落库后，按以下步骤执行交叉引用：

### Step 1：topic-map 更新
- 读取文章 frontmatter 的 `topic` 字段
- 打开 `03-KNOWLEDGE/99-SYSTEM/01-INDEXES/topic-map.md`
- 若该 topic 已有 entry：在其下追加该文章作为新 source（含文件名、一行摘要、来源标记 `article-derived`）
- 若该 topic 不存在：在文件末尾创建新 entry（含 topic 名、一行说明、首个 source）
- 保守原则：每次仅追加小块增量，不重写整页

### Step 2：related_notes 双向链接
- 分两层扫描候选：
  1. `Article-Notes/` 中的原始相关文章
  2. 对应 domain 目录（如 `AI-Agent/`、`AI-Workflow/`）中的提炼页 / pattern 页
- 计算 topic 字段交集 + tags 字段交集
- 交集 ≥ 2：自动在双方 `related_notes` 字段互相追加对方的 `[[文件名]]`（不含扩展名）
- 交集 = 1：标记为候选，列入 integration report，不自动写入
- 不跨 domain 强加关联；若 domain 不明确，先只在 Article-Notes 层做比较

### Step 3：open-questions 追加
- 阅读文章内容，识别文章中提出但未解答的问题（"未来工作"/"开放问题"/"值得探讨"等线索词）
- 若发现有价值的未解答问题，追加到 `03-KNOWLEDGE/99-SYSTEM/01-INDEXES/open-questions.md`
- 每条格式：`- [article-derived] 问题描述 → 来源：[[文章文件名]]`
- 若文章无明显 open questions，skip 此步骤

### Step 4：Consume latest lint report（不再重复执行）
- 若 `12-REVIEWS/KNOWLEDGEBASE/` 下存在最近 24 小时内的 lint 报告，可读取其摘要作为 integration 的参考上下文
- 若最新 lint 报告含 🔴 级问题，在 integration report 中单独标注
- 本 skill **不再主动执行 lint**；知识库 lint 由独立的 `knowledge-lint-weekly` job 负责，避免重复运行

## Success Criteria

A run is successful when:
- new or pending article notes are normalized enough to participate in Brain retrieval
- relation/index updates happen only when there is real incremental signal
- no duplicate truth source is created
- Brain changes are committed
- resulting files are Obsidian-visible

## Failure / Degraded Mode

- **No new notes found** → emit a clear no-op report; do not force changes
- **Conflicting metadata** → mark for review, avoid pretending integration is complete
- **Index update would be no-op** → report that nothing meaningful changed
- **One note fails** → keep batch going; report the failed note separately

## Anti-Scope

This skill must **not**:
- use raw coding transcripts as its primary input
- perform transcript mining / conversation synthesis
- run full external deep research by default
- create a parallel truth source outside Brain
- over-write stable knowledge surfaces just to appear active

## Output Quality Bar

- Preserve article/source boundary; do not turn speculation into fact
- Prefer minimal, high-signal index updates over bulk rewrites
- Pattern extraction should be cautious; candidate-first is preferred
- If project linkage is low-confidence, leave it unresolved rather than hallucinating

## Nightly Digest Coordination Protocol

This stage is responsible for writing **two layers**:

### Layer A — machine-facing run report
Write a detailed report to:
- `03-KNOWLEDGE/99-SYSTEM/03-INTEGRATION-REPORTS/YYYY-MM-DD/article-integration-report-YYYY-MM-DD.md`

This is for agents, auditing, and downstream debugging.

### Layer B — human-facing nightly digest
Append / update the `02:00 Article Integration` section in:
- `03-KNOWLEDGE/01-READING/04-DIGESTS/nightly-digest-YYYY-MM-DD.md`

Digest section must be readable by {{USER_NAME}} in 30 seconds and include only:
- 处理了哪些文章
- 有无新增 topic / open question
- 是否 no-op / degraded
- 一句话说明为什么值得看或为什么没产出

Downstream 03:00 and 04:00 stages should read this digest first, then read machine reports only if needed.

## Nightly Position in the Split Pipeline

This is the **02:00 stage** in the split nightly knowledge system:
1. `knowledge-lint-weekly` (01:00, Mondays only)
2. `article-notes-integration` (02:00)
3. `conversation-knowledge-mining` (03:00)
4. `knowledge-flywheel-amplifier` (04:00)

Downstream contract:
- 03:00 should first read the shared nightly digest, then machine reports if needed
- 04:00 should first read the shared nightly digest, then machine reports if needed

## Acceptance Standard

Do not call the job complete unless the result is:
- integrated into Brain (if there was real signal)
- committed to git
- confirmed visible in Obsidian / post-commit sync path
