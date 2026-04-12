---
name: knowledge-flywheel-amplifier
description: >
  Cross-source nightly amplifier for merging article-derived and
  conversation-derived signals into topic updates, pattern candidates,
  open questions, and candidate research seeds. Use when: knowledge flywheel,
  amplify knowledge, cross-source synthesis, nightly amplifier,
  04:00 flywheel stage, topic merge, open question clustering.
---

# Knowledge Flywheel Amplifier

把 02:00 的文章整合结果与 03:00 的对话沉淀结果做轻量汇合，形成跨源主题、候选模式、开放问题与后续研究输入。

## Purpose

这个技能负责 **跨文章与对话的 amplification 层**，而不是重新做 article integration 或 transcript mining。

它处理的是：
1. 汇总 Stage A（文章）与 Stage B（对话）的新增高价值信号
2. 识别重复主题、交叉问题、共同模式与项目路由机会
3. 更新少量高价值的 topic / open-question / pattern-candidate surfaces
4. 生成 research seeds / context-pack candidates
5. 为后续是否值得深研提供条件化升级输入

## Primary Inputs

- Stage A outputs:
  - article integration reports
  - high-value article candidates
  - updated article-derived relation/index signals
- Stage B outputs:
  - transcript mining brief
  - conversation-derived notes
  - daily suggestions updates
  - candidate research seeds / context-pack candidates
- Read-only Brain context:
  - `03-KNOWLEDGE/99-SYSTEM/01-INDEXES/`
  - relevant domain notes
  - `05-PROJECTS/` project briefs
  - existing open questions / topic maps / pattern candidate surfaces

## Required Outputs

A successful run should produce some or all of:
- 1 machine-facing run report → `03-KNOWLEDGE/99-SYSTEM/03-INTEGRATION-REPORTS/YYYY-MM-DD/amplifier-report-YYYY-MM-DD.md`
- 1 human-facing digest section append → `03-KNOWLEDGE/01-READING/04-DIGESTS/nightly-digest-YYYY-MM-DD.md`
- merged topic / open-question / pattern-candidate updates when justified
- zero to two research seeds
- zero or more context-pack drafts
- optional project/domain routing suggestions
- Brain git commit + post-commit visibility confirmation when Brain changed

## What This Skill May Read

- outputs from `article-notes-integration`
- outputs from `conversation-knowledge-mining`
- existing Brain indexes / project briefs / knowledge notes / topic surfaces

## What This Skill May Write

- topic map / topic index updates
- open questions
- pattern candidates
- cross-source routing notes or compact synthesis notes
- amplifier reports
- context-pack drafts / research seed drafts

## Nightly Digest Coordination Protocol

This stage must always write **two layers**:

### Layer A — machine-facing run report
Write a detailed report to:
- `03-KNOWLEDGE/99-SYSTEM/03-INTEGRATION-REPORTS/YYYY-MM-DD/amplifier-report-YYYY-MM-DD.md`

### Layer B — human-facing nightly digest
Append / update the `04:00 Amplifier` section in:
- `03-KNOWLEDGE/01-READING/04-DIGESTS/nightly-digest-YYYY-MM-DD.md`

Digest section must tell {{USER_NAME}} only:
- 今晚有没有真正形成跨源汇合
- 如果没有，是因为哪一段缺失 / degraded
- 如果有，最值得看的 topic / open question / research seed 是什么
- 是否触发深度研究，若没触发，原因是什么

This stage should read the shared nightly digest first, then machine-facing reports only when needed.

## Default Nightly Behavior

The default 04:00 behavior is intentionally lightweight:
- merge signals
- detect overlaps and gaps
- update only small, high-value graph/index surfaces
- generate research seeds or context-pack candidates when warranted

It must **not** automatically escalate into heavy external research every night.

## Escalation Criteria

A follow-up deep-research task may be spawned only when:
- the theme is high-value
- internal context already exists
- the question is narrow enough to avoid drift
- the likely payoff is worth the additional complexity

If these are not met, stay at candidate seed / context-pack level.

## Success Criteria

A run is successful when:
- article and conversation signals are merged without collapsing their boundaries
- only justified graph/index updates are made
- high-value open questions / pattern candidates are surfaced clearly
- deep research remains optional and condition-based
- Brain changes are committed and Obsidian-visible

## Failure / Degraded Mode

- **Missing Stage A output** → continue with Stage B only, but say article context is partial
- **Missing Stage B output** → continue with Stage A only, but say conversation context is partial
- **No cross-source signal** → emit a no-op amplifier report; do not force graph changes
- **Unclear topic merge** → keep separate candidates rather than over-merge

## Anti-Scope

This skill must **not**:
- re-run full article note normalization
- re-run full transcript mining
- auto-run heavy NotebookLM / agent-reach deep research by default
- perform large-scale graph rewrites to simulate activity
- erase source boundaries between article-derived and conversation-derived knowledge

## Output Quality Bar

- Merge conservatively; preserve provenance
- Prefer compact high-value updates over broad topology surgery
- Open questions should be concrete, not vague brainstorming sludge
- Pattern candidates should remain candidates unless evidence is strong
- Research seeds should be scoped enough for safe downstream amplification

## Nightly Position in the Split Pipeline

This is the **04:00 stage** in the split nightly knowledge system:
1. `article-notes-integration` (02:00)
2. `conversation-knowledge-mining` (03:00)
3. `knowledge-flywheel-amplifier` (04:00)

Upstream contract:
- read Stage A and Stage B outputs if present
- tolerate partial upstream success
- never pretend upstream work succeeded if inputs are missing

## Acceptance Standard

Do not call the job complete unless the result is:
- written into Brain only where justified
- committed to git when Brain changed
- confirmed visible in Obsidian / post-commit sync path
- explicit about whether deep research was merely proposed or actually escalated
