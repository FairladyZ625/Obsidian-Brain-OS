---
name: conversation-knowledge-flywheel
description: >
  Transcript-first nightly pipeline for mining AI conversations into structured
  knowledge notes, candidate research seeds, and next-day leverage. Use when:
  对话沉淀, 对话整理, conversation mining, transcript mining, 昨天的对话,
  nightly conversation knowledge, review AI chat transcripts,
  extract insights from conversations, or run the 03:00 conversation stage.
---

# Conversation Knowledge Flywheel

把“昨天和 AI 的高价值对话”变成：
1. 可复用知识
2. 今日可执行建议
3. 候选研究线索（默认不直接深研）

## Phase 1 Scope

- **原始真相层**：直接读取外置硬盘对话目录 `{{TRANSCRIPT_DIR}}`
- **项目归类层**：先按 project 分组，不依赖重标签体系
- **QMD 主召回层**：优先用 QMD 的 hybrid / vector / rerank 做高召回候选池（通过 skill-local `qmd-safe.sh` 入口调用，避免裸用漂移的全局运行时）
- **Surveillance 快扫层**：用轻量快模型做 broad scan，降低漏检风险
- **人工提炼层**：最终由我来判断、提炼、成文
- **可见性闭环**：知识库改动必须 commit，确保 Obsidian 可见

## Nightly Position in the Split Pipeline

This skill is the **03:00 conversation stage** in the split nightly knowledge system:
1. `article-notes-integration` (02:00)
2. `conversation-knowledge-mining` / `conversation-knowledge-flywheel` (03:00)
3. `knowledge-flywheel-amplifier` (04:00)

Downstream / upstream contract:
- 02:00 article integration may enrich Brain context before this stage runs
- this stage may read article-derived knowledge as context, but does not normalize article notes
- 04:00 amplifier may read this stage's notes, daily suggestions block, and candidate research seeds
- Preferred upstream read order for 03:00: shared nightly digest → `03-KNOWLEDGE/99-SYSTEM/03-INTEGRATION-REPORTS/run-reports/YYYY-MM-DD/` → stable indexes only if needed
- Do **not** rely on legacy article report paths under `12-REVIEWS/KNOWLEDGEBASE/` for this split pipeline

## Out of Scope (for now)

- 不负责 article notes 的 nightly normalization / integration
- 不做无锚点的全量 NotebookLM DeepResearch 自动执行（必须先有 Context Pack）
- 不依赖重度人工标签体系做主干判断
- 不对所有主题做外部补强，只生成少量高价值候选
- 不把原始 transcript 复制进 {{BRAIN_NAME}}

## Inputs

- Raw transcript root: `$TRANSCRIPT_ROOT` (default: `{{TRANSCRIPT_DIR}}`)
- Brain root: `$BRAIN_ROOT` (default: `{{BRAIN_ROOT}}`)
- Date: default = yesterday (Asia/Shanghai)
- Optional project hints / active initiatives from {{BRAIN_NAME}}
- Brain-side project registry at `$BRAIN_ROOT/05-PROJECTS/` when a project can be identified
- Existing article-derived knowledge in Brain as read-only routing context

## Outputs

### Required
- 1 daily manifest (`/tmp/conversation-flywheel-YYYY-MM-DD-manifest.json`)
- 1 recommendations draft (`/tmp/conversation-flywheel-YYYY-MM-DD-brief.md`)
- 1 machine-facing run report → `03-KNOWLEDGE/99-SYSTEM/03-INTEGRATION-REPORTS/run-reports/YYYY-MM-DD/conversation-mining-report-YYYY-MM-DD.md`
- 1 human-facing digest section append → `03-KNOWLEDGE/01-READING/04-DIGESTS/nightly-digest-YYYY-MM-DD.md`
- 1-3 conversation-derived knowledge note drafts or writer instructions when justified
- 0-2 candidate research seeds / context-pack candidates (only when signal exists)

### Knowledge Output Types
- **Project execution insight**
- **Reusable method / workflow insight**
- **Research seed**
- **Next-day leverage**

## Nightly Digest Coordination Protocol

This stage must always leave behind **two artifacts**, even on no-op / degraded runs:

### Layer A — machine-facing run report
Write a detailed run report to:
- `03-KNOWLEDGE/99-SYSTEM/03-INTEGRATION-REPORTS/run-reports/YYYY-MM-DD/conversation-mining-report-YYYY-MM-DD.md`

This report must explicitly state:
- transcript root / target date是否找到
- manifest 是否生成
- QMD 是否可用
- candidate set 是否形成
- why no-op / degraded / success
- whether Brain knowledge writes happened

### Layer B — human-facing nightly digest
Append / update the `03:00 Conversation Mining` section in:
- `03-KNOWLEDGE/01-READING/04-DIGESTS/nightly-digest-YYYY-MM-DD.md`

Digest section must be readable by {{USER_NAME}} in 30 seconds and include only:
- 昨天对话有没有真正挖出东西
- 如果没挖出来，卡在哪里（例如 transcript 缺失 / QMD 异常）
- 如果挖出来了，最值得看的 1-3 个点是什么
- 是否生成 research seed / context pack

Downstream 04:00 stage should read this digest first, not infer blindly from scattered outputs.

## Nightly Ownership Chain

- **Trigger**: nightly cron job
- **Dispatcher / integrator**: {{MAIN_AGENT_NAME}}
- **Recall layers**: project grouping → QMD → Surveillance
- **Final judgment**: {{MAIN_AGENT_NAME}} only
- **Formal knowledge write**: Writer-Agent only
- **Acceptance standard**: Brain write + git commit + post-commit sync + Obsidian visible

This separation is strict:
- QMD does retrieval, not truth judgment
- Surveillance does candidate pre-screening, not knowledge writing
- Writer-Agent does formal landing, not idea selection

## Workflow

### Minimal Viable Path

When QMD is unavailable or Surveillance is not yet implemented, use this reduced path:

```
Step 1 (manifest) → Step 2 (project grouping) → Step 5 (read manifest + raw transcripts directly)
→ Step 6 (write via approved path) → Step 7 (verify visibility)
```

Skip Steps 3–4. In Step 5, read the top N largest transcripts per project group directly.
If a project brief is available, read it first as a routing anchor.

When QMD is healthy, run the full 7-step flow.

### Step 1: Build daily manifest
Run helper scripts to list the previous day's transcripts and produce a manifest.

### Step 2: Group by project
Infer project mapping primarily from filenames / transcript titles. This step is allowed to stay simple and explicit.

When a likely project is identified, resolve it to a stable project anchor:
- prefer an existing `project_ref` if already known
- otherwise use `scripts/resolve-project-ref.py <inferred-name>` to map to a known project brief under `$BRAIN_ROOT/05-PROJECTS/`
- if confidence is low, leave the project unresolved rather than hallucinating

### Step 3: Build a high-recall candidate pool with QMD
For each project group:
- create or refresh a QMD collection
- run `qmd-safe.sh update`
- run `qmd-safe.sh embed`
- use `qmd-safe.sh query` / `qmd-safe.sh vsearch` with reranking to retrieve likely high-value transcript chunks

This layer is for **recall**, not final judgment.

### Step 4: Run Surveillance scan
Use a fast, cheap model layer to quickly scan the recalled candidates.

Surveillance is a **candidate-recall layer**, not a knowledge-authoring layer.
It should answer:
- which conversations are most likely worth {{MAIN_AGENT_NAME}} review
- which ones may change today's execution quality
- which ones deserve outside reinforcement later

Recommended signal dimensions:
- **project relevance**: is it clearly tied to an active project?
- **structural density**: does it contain decisions, comparisons, review conclusions, architecture edges, rules, or reusable methods?
- **next-day leverage**: can it influence tomorrow's execution or judgment?
- **pattern / anomaly recurrence**: does it repeat across multiple transcripts or reveal a systemic issue?

Surveillance output should be:
- top candidate transcript paths per project
- one-line reason each candidate is worth human review
- priority bucket (`P1`, `P2`, `P3`) for {{MAIN_AGENT_NAME}} attention
- optional external research seed

### Step 5: Final human-quality synthesis
Before final synthesis, if a project can be identified with reasonable confidence, read the corresponding Brain-side project brief first:
- `$BRAIN_ROOT/05-PROJECTS/<project-slug>/project-brief.md`
- e.g. `$BRAIN_ROOT/05-PROJECTS/agora/project-brief.md` for `project_ref: proj-agora`
- Use `scripts/resolve-project-ref.py` to get the exact path; skip if unresolved.

Use that brief as a lightweight routing anchor so the synthesis knows:
- what the project is
- where its true execution context lives
- which recent knowledge is already attached
- which aliases / search terms are valid

{{MAIN_AGENT_NAME}} then does the final personalized extraction and generates:
- 1-3 conversation-derived knowledge notes
- 1 daily learning suggestions block
- optional external research seeds (not executed by default)

When the project mapping is clear, these outputs should carry lightweight project anchors such as:
- `project_ref`
- `related_projects`
- optional `project_brief` path for routing/reference

This is the only stage allowed to decide:
- what becomes knowledge
- what stays only as a candidate
- what should be ignored
- what should feed next-day briefing

### Step 6: Write via the approved Brain path
You must **not directly write {{BRAIN_NAME}}** from this skill unless the active environment explicitly allows it.

Preferred formal landing path:
- {{MAIN_AGENT_NAME}} prepares writer-ready package
- `sessions_send` to Writer-Agent with explicit target paths
- Writer-Agent writes, commits, and reports receipt

Writer-Agent responsibilities are intentionally narrow:
- preserve frontmatter and source transcript paths
- land approved content into Brain
- commit and verify visibility
- do not reinterpret or re-decide knowledge selection

### Step 7: Verify visibility
A successful run is not “draft written”. Success means:
- Brain files updated
- git commit created
- post-commit sync triggered
- Obsidian-visible

## Output Quality Bar

- No generic diary summary
- Must cite source transcript paths
- Must preserve the original insight boundary
- Must produce at least one concrete next-day recommendation when signal exists
- Must avoid duplicates with existing knowledge notes
- QMD / Surveillance only produce candidate recall, not final truth claims

## External reinforcement (Phase 2 hook)
If a theme is both high-value and incomplete, generate a **research seed** or **context-pack candidate** that can later be sent to:
- agent-reach
- web search
- NotebookLM

This stage does **not** execute heavy external research by default; it only prepares follow-up inputs.

Example seed fields:
- topic
- why_it_matters
- 1-3 research questions
- suggested notebook mapping

## Conditional NotebookLM Reinforcement Protocol

NotebookLM is defined here as:
- **an external research amplifier grounded by our internal context**, not a replacement for internal judgment

Its value comes from searching external sources, but that search must be anchored by our internal sources and research boundary.

### Trigger rule
Only trigger NotebookLM deep research when at least one of these concrete signals is present:
- A conversation revealed a design decision that lacks external best-practice grounding
- A recurring problem appeared across multiple transcripts but has no mature internal solution
- A new concept / framework was mentioned but internal understanding is incomplete
- {{MAIN_AGENT_NAME}} explicitly flagged a theme as needing external reinforcement

Do NOT trigger for: purely internal process issues, themes already well-covered in Brain, or low-confidence hunches without a clear research question.

### Required order (follow-up only, not default nightly)
1. Prepare internal **NotebookLM Context Pack** using `templates/notebooklm-context-pack-template.md`
2. Upload sources to the target notebook:
   ```bash
   notebooklm source add <path-to-note.md> -n <notebook-id>
   notebooklm source add <path-to-project-brief.md> -n <notebook-id>
   ```
   Or create a fresh notebook first: `notebooklm create "Research: <theme> YYYY-MM-DD"`
3. Prepare a constrained **NotebookLM Research Seed** using `templates/notebooklm-research-seed-template.md`
4. Run deep research by asking the notebook:
   ```bash
   notebooklm use <notebook-id>
   notebooklm ask "<research-seed-questions>" --new
   ```
5. {{MAIN_AGENT_NAME}} reviews results and extracts only useful ideas back into the system

### NotebookLM Context Pack requirements
Before deep research, include at least:
- 1 primary internal knowledge note
- 1 supporting project / architecture / governance note
- 1 daily suggestions / leverage note when relevant

The point is not to reduce external search. The point is to give external search the correct internal anchor.

### Research Seed requirements
The seed must explicitly specify:
- what the internal project/theme means in our system
- what is already known internally
- what exact design question needs outside reinforcement
- what public meanings / semantic drifts should be excluded
- what kind of output is desired (practical patterns, taxonomies, implementation guidance)

### Boundary rule
NotebookLM may search broadly across external sources. That is expected.
What must be controlled is not **externality** but **topical drift**.

### Post-research rule
NotebookLM output does not land directly into Brain.
{{MAIN_AGENT_NAME}} must:
- evaluate whether the external synthesis stayed on target
- separate actionable findings from interesting-but-irrelevant material
- decide whether to convert the result into a new knowledge note, a research appendix, or nothing

Unless that follow-up trigger is explicitly satisfied, the nightly conversation job stops at candidate seeds / context packs.

## Suggested Knowledge Sink Contract

### Conversation-derived note
Use the template at `templates/conversation-derived-note-template.md`.

### Daily suggestions index
Append or refresh a daily block in a file like:
- `03-KNOWLEDGE/99-SYSTEM/01-INDEXES/daily-learning-suggestions.md`

When applicable, daily suggestions should point back to the relevant project brief so the recommendation is not floating without project context.

### Daily briefing feed-in
Provide a compact block titled:
- `昨日沉淀带来的新想法`

## Failure Handling

- **No transcripts found** → still write machine report + digest section; state clearly that transcript root / target date was missing
- **QMD unhealthy** → first try skill-local `qmd-safe.sh` auto-repair once; if still unhealthy, enter degraded mode explicitly and still write machine report + digest section
- **Surveillance noisy / low confidence** → still pass only compact candidate shortlist to {{MAIN_AGENT_NAME}}, not long summaries
- **No high-value insights** → produce a short "no-signal" machine report + digest section; no forced note
- **Writer path unavailable** → emit ready-to-send writer instruction block
- **Commit not created** → report “not Obsidian-visible yet”

## Runtime Notes

- QMD is the preferred recall engine, but if local QMD runtime is unhealthy, emit a clear degraded-mode notice instead of silently pretending QMD ran.
- Current observed risk to watch for: Node ABI / native module mismatch in local `qmd` install.

## Phase 2 / 3 Evolution

Later this skill can add:
- better candidate scoring
- richer project graph linking
- trend detection across multiple days
- automated context-pack assembly for approved follow-up research

Heavy external reinforcement remains a separate escalation path, not the default nightly contract.
