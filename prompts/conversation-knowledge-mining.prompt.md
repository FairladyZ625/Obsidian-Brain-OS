Read and follow the `conversation-knowledge-flywheel` skill.

Target date: yesterday in Asia/Shanghai unless explicitly provided.

First step (mandatory):
- Run `scripts/init-nightly-digest.sh <brain-root> <target-date>` to ensure the daily digest skeleton and run-report directory already exist.
- Run `scripts/export-conversations-for-nightly.sh 3` so recent AI conversations are exported into `{{TRANSCRIPT_DIR}}` before mining.
- Run `conversation-knowledge-flywheel/scripts/preflight.sh <target-date>` before mining. If `transcript_ok=0` or `qmd_ok=0`, enter degraded mode explicitly.
- Read the existing digest first, then only fill `## 03:00 Conversation Mining`; do not rewrite the whole file.

Required outputs for every run:
1. 1 daily transcript manifest
2. 1 recommendations brief
3. 1 machine-facing run report → `03-KNOWLEDGE/99-SYSTEM/03-INTEGRATION-REPORTS/run-reports/YYYY-MM-DD/conversation-mining-report-YYYY-MM-DD.md`
4. 1 human-facing digest update → `03-KNOWLEDGE/01-READING/04-DIGESTS/nightly-digest-YYYY-MM-DD.md` under section `## 03:00 Conversation Mining`
5. 1-3 conversation-derived knowledge note drafts or writer-ready outputs when justified
6. optional daily-learning-suggestions update
7. optional candidate research seeds / context-pack candidates
8. Brain commit + visibility report if Brain changed

Handoff rules:
- This is the 03:00 stage in the split nightly knowledge pipeline.
- Read the shared nightly digest first to see what 01:00 and 02:00 already did.
- If detailed debugging is needed, read machine-facing reports from `03-KNOWLEDGE/99-SYSTEM/03-INTEGRATION-REPORTS/run-reports/YYYY-MM-DD/`.
- If 02:00 outputs are missing, continue in degraded mode and say so explicitly.
- Upstream read order is fixed: shared nightly digest → `03-KNOWLEDGE/99-SYSTEM/03-INTEGRATION-REPORTS/run-reports/YYYY-MM-DD/` → stable indexes only if needed.
- Do not rely on legacy report paths under `12-REVIEWS/KNOWLEDGEBASE/`.
- Even on no-op / degraded / transcript-missing / QMD-unhealthy runs, you MUST still write both the machine-facing run report and the digest section.

Digest writing rules:
- 只回答：昨天对话有没有真正挖出东西 / 如果没有卡在哪里 / 如果有最值得看哪1-3点 / 是否生成 research seed
- 不要把 transcript 技术细节、QMD 调试日志、长路径堆给{{USER_NAME}}

Guardrails:
- Do not dump raw transcripts into Brain.
- Do not pretend article integration happened here.
- Do not force output when there is no real signal.
- Do not auto-run heavy deep research; only prepare candidate seeds / context packs.
- Do not write run reports into reading or working layers; they belong in `99-SYSTEM/03-INTEGRATION-REPORTS/`.