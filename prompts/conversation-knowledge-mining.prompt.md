# Conversation Knowledge Mining — Nightly Master Prompt

> Runtime location: `{{WORKSPACE_PATH}}/conversation-knowledge-mining.prompt.md`
> This is a template — copy to your workspace and customize.

Read and follow the `conversation-knowledge-flywheel` skill (`{{SKILLS_PATH}}/conversation-knowledge-flywheel/SKILL.md`).

Target date: yesterday ({{TIMEZONE}}) unless explicitly provided.

## First Step (mandatory)

1. Run `scripts/init-nightly-digest.sh <brain-root> <target-date>` — ensure digest skeleton exists.
2. Run `scripts/export-conversations.sh 3` — export recent AI conversations before mining.
3. Run `conversation-knowledge-flywheel/scripts/preflight.sh <target-date>` — check transcript availability.
   - If `transcript_ok=0` or search unavailable: enter degraded mode explicitly.
4. Read the existing digest first, then only fill `## 03:00 Conversation Mining`.

## Required Outputs (every run)

1. **Daily transcript manifest**
2. **Recommendations brief**
3. **Machine-facing run report** → `03-KNOWLEDGE/99-SYSTEM/03-INTEGRATION-REPORTS/run-reports/YYYY-MM-DD/conversation-mining-report-YYYY-MM-DD.md`
4. **Human-facing digest update** → `03-KNOWLEDGE/01-READING/04-DIGESTS/nightly-digest-YYYY-MM-DD.md` under `## 03:00 Conversation Mining`
5. 1-3 conversation-derived knowledge note drafts when justified
6. Optional: daily-learning-suggestions update
7. Optional: candidate research seeds / context-pack candidates
8. Brain commit + visibility report if Brain changed

## Handoff Rules

- This is the **03:00 stage** in the split nightly knowledge pipeline.
- Read the shared nightly digest first (see what 02:00 already did).
- If 02:00 outputs are missing: continue in degraded mode, say so explicitly.
- Even on no-op / degraded / transcript-missing runs: **still write both the machine report and the digest section**.

## Digest Writing Rules

- 只回答：昨天对话有没有挖出东西 / 如果没有卡在哪里 / 如果有最值得看哪 1-3 点 / 是否生成 research seed
- 不要把 transcript 技术细节、调试日志、长路径堆给用户看

## Guardrails

- Do not dump raw transcripts into Brain
- Do not pretend article integration happened in this stage
- Do not force output when there is no real signal
- Do not auto-run heavy deep research (only prepare candidate seeds)
- Run reports belong in `99-SYSTEM/03-INTEGRATION-REPORTS/`, never in reading or working layers
