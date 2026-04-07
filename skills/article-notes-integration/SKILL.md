---
name: article-notes-integration
description: >
  文章笔记夜间整合流水线。将前一天新增或待整合的 Article Notes 转化为可检索、可关联、可继续提炼的 Brain 知识输入层。Use when: 文章整合, article notes integration, nightly article sync, update article relations, topic index update, article knowledge graph, 前一天文章整理, 或 run the 02:00 article pipeline.
---

# Article Notes Integration

把前一天新增或待整合的 Article Notes，转成可检索、可关联、可继续提炼的 Brain 知识输入层。

## 目标

这个技能负责 **文章 ingestion 之后的 nightly integration**，而不是原始外部文章采集本身。

它处理的是：
1. 扫描昨天新增或尚未 integrated 的 article notes
2. 校验并补足结构 / frontmatter / relation 状态
3. **交叉引用更新**（见下方 Cross-Reference Protocol，每次 ingest 后执行）
4. 更新 topic / domain / project 相关的轻量图谱入口
5. 生成 open questions / pattern candidates / article-derived graph signals
6. 输出高价值 article candidates，供后续 flywheel amplification 使用

## 主要输入

- Brain root: `{{BRAIN_PATH}}`
- 源笔记：`03-KNOWLEDGE/02-WORKING/01-ARTICLE-NOTES/`
- 候选集：
  - 前一天新增 article notes
  - 或 `integration_status != integrated` 的 article notes
- 只读上下文：
  - 相关 domain notes
  - `03-KNOWLEDGE/99-SYSTEM/01-INDEXES/` 下已有 topic / topic-map / open-question surfaces
  - `05-PROJECTS/` 下 project briefs（若能稳定识别项目）

## 必要输出

成功运行应产生以下部分或全部内容：
- 1 份机器向运行报告 → `03-KNOWLEDGE/99-SYSTEM/03-INTEGRATION-REPORTS/YYYY-MM-DD/article-integration-report-YYYY-MM-DD.md`
- 1 份人类向摘要追加 → `03-KNOWLEDGE/01-READING/04-DIGESTS/nightly-digest-YYYY-MM-DD.md`
- article note frontmatter / relation 字段更新
- topic index / topic map 更新（仅在有正当理由时）
- open question / pattern candidate 标记（仅在有正当理由时）
- 高价值 article candidates，供 04:00 amplifier 阶段使用
- Brain git commit + post-commit 可见性确认

## 本技能可读取的内容

- Article notes 本身
- 现有 Brain 知识 / indexes / project briefs
- 现有 relation fields 和 topic surfaces

## 本技能可写入的内容

- Article note 元数据和 relation fields
- `03-KNOWLEDGE/99-SYSTEM/01-INDEXES/` 下的轻量图谱/index surfaces
- 仅候选级别的 pattern / open-question surfaces
- Integration reports

## 交叉引用协议（每次 ingest 后执行）

每次处理文章落库后，按以下步骤执行交叉引用：

### 步骤 1：topic-map 更新

- 读取文章 frontmatter 的 `topic` 字段
- 打开 `03-KNOWLEDGE/99-SYSTEM/01-INDEXES/topic-map.md`
- 若该 topic 已有 entry：在其下追加该文章作为新 source（含文件名、一行摘要、来源标记 `article-derived`）
- 若该 topic 不存在：在文件末尾创建新 entry（含 topic 名、一行说明、首个 source）
- 保守原则：每次仅追加小块增量，不重写整页

### 步骤 2：related_notes 双向链接

- 分两层扫描候选：
  1. `Article-Notes/` 中的原始相关文章
  2. 对应 domain 目录（如 `AI-Agent/`、`AI-Workflow/`）中的提炼页 / pattern 页
- 计算 topic 字段交集 + tags 字段交集
- 交集 ≥ 2：自动在双方 `related_notes` 字段互相追加对方的 `[[文件名]]`（不含扩展名）
- 交集 = 1：标记为候选，列入 integration report，不自动写入
- 不跨 domain 强加关联；若 domain 不明确，先只在 Article-Notes 层做比较

### 步骤 3：open-questions 追加

- 阅读文章内容，识别文章中提出但未解答的问题（"未来工作"/"开放问题"/"值得探讨"等线索词）
- 若发现有价值的未解答问题，追加到 `03-KNOWLEDGE/99-SYSTEM/01-INDEXES/open-questions.md`
- 每条格式：`- [article-derived] 问题描述 → 来源：[[文章文件名]]`
- 若文章无明显 open questions，跳过此步骤

### 步骤 4：消费最新 lint 报告（不再重复执行）

- 若 `12-REVIEWS/KNOWLEDGEBASE/` 下存在最近 24 小时内的 lint 报告，可读取其摘要作为 integration 的参考上下文
- 若最新 lint 报告含 🔴 级问题，在 integration report 中单独标注
- 本 skill **不再主动执行 lint**；知识库 lint 由独立的 `knowledge-lint-weekly` job 负责，避免重复运行

## 成功标准

运行成功当且仅当：
- 新增或待处理的 article notes 已足够规范化，能参与 Brain 检索
- relation/index 更新只在有真实增量信号时发生
- 未制造重复真相源
- Brain 改动已 commit
- 结果文件在 Obsidian 中可见

## 失败 / 降级模式

- **未找到新笔记** → 发出明确的 no-op 报告；不强制做任何改动
- **元数据冲突** → 标记待 review，不假装整合已完成
- **Index 更新无实际变化** → 报告无实际意义变更
- **单个笔记失败** → 继续处理批次；单独报告失败的笔记

## 边界（不做什么）

本技能**禁止**：
- 以原始 coding transcripts 为主输入
- 执行 transcript mining / conversation synthesis
- 默认执行全量外部 deep research
- 在 Brain 外部制造平行真相源
- 为了显得"活跃"而覆盖稳定知识 surfaces

## 输出质量底线

- 保持 article/source 边界；不将推测变为事实
- 倾向最小化、高信号的 index 更新，而非批量重写
- Pattern 提取应保守；优先保留为候选态
- 若项目关联置信度低，不强行关联，宁可留空

## 夜间摘要协调协议

本阶段负责撰写**两层内容**：

### A层 — 机器向运行报告

写入详细报告至：
- `03-KNOWLEDGE/99-SYSTEM/03-INTEGRATION-REPORTS/YYYY-MM-DD/article-integration-report-YYYY-MM-DD.md`

供 agents、审计和下游调试使用。

### B层 — 人类向夜间摘要

在以下文件中追加/更新 `02:00 Article Integration` 部分：
- `03-KNOWLEDGE/01-READING/04-DIGESTS/nightly-digest-YYYY-MM-DD.md`

摘要部分须让 {{USER_NAME}} 在 30 秒内读完，仅包含：
- 处理了哪些文章
- 有无新增 topic / open question
- 是否 no-op / degraded
- 一句话说明为什么值得看或为什么没产出

下游 03:00 和 04:00 阶段应先读此摘要，必要时再读机器报告。

## 在分片夜间流水线中的位置

本技能是分片夜间知识系统的 **02:00 阶段**：
1. `knowledge-lint-weekly` (01:00, 仅周一)
2. `article-notes-integration` (02:00)
3. `conversation-knowledge-mining` (03:00)
4. `knowledge-flywheel-amplifier` (04:00)

下游约定：
- 03:00 应先读共享夜间摘要，必要时再读机器报告
- 04:00 应先读共享夜间摘要，必要时再读机器报告

## 验收标准

只有满足以下条件，才算任务完成：
- 知识已整合进 Brain（如有真实信号）
- 已 commit 到 git
- 已确认在 Obsidian / post-commit sync 路径中可见
