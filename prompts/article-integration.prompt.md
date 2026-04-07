# Article Notes Integration — Nightly Prompt

Read and follow the `article-notes-integration` skill.

Target date: yesterday ({{TIMEZONE}}) unless explicitly provided.

## First Step (mandatory)

1. Run `scripts/init-nightly-digest.sh <brain-root> <target-date>` to ensure the daily digest skeleton and run-report directory exist.
2. After that, only fill your own section; do not rewrite the whole digest.

## Required Outputs (every run)

1. **Machine-facing run report** → `03-KNOWLEDGE/99-SYSTEM/03-INTEGRATION-REPORTS/run-reports/YYYY-MM-DD/article-integration-report-YYYY-MM-DD.md`
2. **Human-facing digest update** → `03-KNOWLEDGE/01-READING/04-DIGESTS/nightly-digest-YYYY-MM-DD.md` under section `## 02:00 Article Integration`
3. Article-note metadata updates only when justified
4. Cautious topic / open-question / pattern-candidate updates only when justified
5. Brain commit + visibility report if Brain changed

## Handoff Rules

- This is the **02:00 stage** in the split nightly knowledge pipeline.
- Downstream 03:00 and 04:00 stages read the shared nightly digest first.
- If no new/pending article notes: still write a no-op machine report and a concise digest section.

## Digest Writing Rules

- 只写人看得懂的结果，不写技术流水账
- 只回答：处理了什么 / 有没有新增 topic 或 open question / 值不值得看 / 如果 no-op 为什么
- 不要把机器调试细节塞进 digest

## Guardrails

- Do not read raw coding transcripts as primary input
- Do not force article updates when there is no signal
- Do not auto-run heavy deep research
- Do not create a duplicate truth source outside Brain
- Run reports belong in `99-SYSTEM/03-INTEGRATION-REPORTS/`, never in reading or working layers
