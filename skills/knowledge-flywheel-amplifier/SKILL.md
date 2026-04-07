---
name: knowledge-flywheel-amplifier
description: >
  跨源夜间放大器。合并文章整合结果与对话沉淀结果，输出主题更新、候选模式、开放问题与后续研究输入。Use when: knowledge flywheel, amplify knowledge, cross-source synthesis, nightly amplifier, 04:00 flywheel stage, topic merge, open question clustering.
---

# Knowledge Flywheel Amplifier

把 02:00 的文章整合结果与 03:00 的对话沉淀结果做轻量汇合，形成跨源主题、候选模式、开放问题与后续研究输入。

## 目标

这个技能负责 **跨文章与对话的 amplification 层**，而不是重新做 article integration 或 transcript mining。

它处理的是：
1. 汇总 Stage A（文章）与 Stage B（对话）的新增高价值信号
2. 识别重复主题、交叉问题、共同模式与项目路由机会
3. 更新少量高价值的 topic / open-question / pattern-candidate surfaces
4. 生成 research seeds / context-pack candidates
5. 为后续是否值得深研提供条件化升级输入

## 主要输入

- Stage A 输出：
  - article integration reports
  - high-value article candidates
  - updated article-derived relation/index signals
- Stage B 输出：
  - transcript mining brief
  - conversation-derived notes
  - daily suggestions updates
  - candidate research seeds / context-pack candidates
- 只读 Brain 上下文：
  - `03-KNOWLEDGE/99-SYSTEM/01-INDEXES/`
  - 相关 domain notes
  - `05-PROJECTS/` project briefs
  - 现有 open questions / topic maps / pattern candidate surfaces

## 必要输出

成功运行应产生以下部分或全部内容：
- 1 份机器向运行报告 → `03-KNOWLEDGE/99-SYSTEM/03-INTEGRATION-REPORTS/YYYY-MM-DD/amplifier-report-YYYY-MM-DD.md`
- 1 份人类向摘要追加 → `03-KNOWLEDGE/01-READING/04-DIGESTS/nightly-digest-YYYY-MM-DD.md`
- 有正当理由时的 merged topic / open-question / pattern-candidate 更新
- 零到两个 research seeds
- 零个或多个 context-pack 草稿
- 可选的项目/domain 路由建议
- Brain 改动时的 Brain git commit + post-commit 可见性确认

## 本技能可读取的内容

- `article-notes-integration` 的输出
- `conversation-knowledge-mining` 的输出
- 现有 Brain indexes / project briefs / knowledge notes / topic surfaces

## 本技能可写入的内容

- topic map / topic index 更新
- open questions
- pattern candidates
- 跨源路由 notes 或轻量 synthesis notes
- amplifier reports
- context-pack 草稿 / research seed 草稿

## 夜间摘要协调协议

本阶段必须撰写**两层内容**：

### A层 — 机器向运行报告

写入详细报告至：
- `03-KNOWLEDGE/99-SYSTEM/03-INTEGRATION-REPORTS/YYYY-MM-DD/amplifier-report-YYYY-MM-DD.md`

### B层 — 人类向夜间摘要

在以下文件中追加/更新 `04:00 Amplifier` 部分：
- `03-KNOWLEDGE/01-READING/04-DIGESTS/nightly-digest-YYYY-MM-DD.md`

摘要部分须让 {{USER_NAME}} 在 30 秒内读懂，仅包含：
- 今晚有没有真正形成跨源汇合
- 如果没有，是因为哪一段缺失 / degraded
- 如果有，最值得看的 topic / open question / research seed 是什么
- 是否触发深度研究，若没触发，原因是什么

本阶段应先读共享夜间摘要，必要时再读机器报告。

## 默认夜间行为

默认 04:00 行为有意设计为轻量级：
- 合并信号
- 检测重叠和缺口
- 只更新少量高价值图谱/index surfaces
- 有正当理由时才生成 research seeds 或 context-pack candidates

本阶段**禁止**每晚自动升级为重型外部 research。

## 升级条件

仅当以下条件全部满足时，才可派生后续 deep-research 任务：
- 主题高价值
- 内部上下文已存在
- 问题足够窄，不会漂移
- 预期收益值得额外复杂度

若以上未全部满足，维持在 candidate seed / context-pack 级别。

## 成功标准

运行成功当且仅当：
- 文章与对话信号合并，且不混淆其边界
- 仅做有正当理由的图谱/index 更新
- 高价值 open questions / pattern candidates 被清晰呈现
- deep research 保持可选且条件触发
- Brain 改动已 commit 并在 Obsidian 中可见

## 失败 / 降级模式

- **缺少 Stage A 输出** → 仅用 Stage B 继续，但要说明 article 上下文不完整
- **缺少 Stage B 输出** → 仅用 Stage A 继续，但要说明 conversation 上下文不完整
- **无跨源信号** → 发出 no-op amplifier 报告；不强制做图谱改动
- **主题合并不明确** → 保持候选分离，不过度合并

## 边界（不做什么）

本技能**禁止**：
- 重新运行全量 article note normalization
- 重新运行全量 transcript mining
- 默认自动运行重型 NotebookLM / agent-reach deep research
- 执行大规模图谱重写以假装活跃
- 抹除 article-derived 与 conversation-derived 知识之间的来源边界

## 输出质量底线

- 保守合并；保持来源追溯
- 倾向紧凑、高价值的更新，而非大幅拓扑改造
- Open questions 应具体，不应是模糊的头脑风暴
- Pattern candidates 应保持候选态，除非证据充分
- Research seeds 应范围明确，便于下游安全放大

## 在分片夜间流水线中的位置

本技能是分片夜间知识系统的 **04:00 阶段**：
1. `article-notes-integration` (02:00)
2. `conversation-knowledge-mining` (03:00)
3. `knowledge-flywheel-amplifier` (04:00)

上游约定：
- 读取 Stage A 和 Stage B 的输出（如果存在）
- 容忍上游部分成功
- 若输入缺失，绝不假装上游工作已完成

## 验收标准

只有满足以下条件，才算任务完成：
- 仅在有正当理由时写入 Brain
- Brain 改动时已 commit
- 已确认在 Obsidian / post-commit sync 路径中可见
- 明确说明 deep research 是仅提议还是实际已升级
