Read and follow the `article-notes-integration` skill.

Target date: yesterday in Asia/Shanghai unless explicitly provided.

First step (mandatory):
- Run `scripts/init-nightly-digest.sh <brain-root> <target-date>` to ensure the daily digest skeleton and run-report directory already exist.
- After that, only fill your own section; do not freestyle the whole digest.

Required outputs for every run:
1. 1 machine-facing run report → `03-KNOWLEDGE/99-SYSTEM/03-INTEGRATION-REPORTS/run-reports/YYYY-MM-DD/article-integration-report-YYYY-MM-DD.md`
2. 1 human-facing digest update → `03-KNOWLEDGE/01-READING/04-DIGESTS/nightly-digest-YYYY-MM-DD.md` under section `## 02:00 Article Integration`
3. article-note relation / metadata updates only when justified
4. cautious topic / open-question / pattern-candidate updates only when justified
5. Brain commit + visibility report if Brain changed

Handoff rules:
- This is the 02:00 stage in the split nightly knowledge pipeline.
- Downstream 03:00 and 04:00 stages should read the shared nightly digest first.
- If detailed debugging is needed, downstream stages may read the machine-facing report.
- If there are no new/pending article notes, still write a no-op machine report and a concise digest section.

Digest writing rules:
- 只写{{USER_NAME}}看得懂的结果，不写技术流水账
- 只回答：处理了什么 / 有没有新增 topic 或 open question / 值不值得看 / 如果 no-op 为什么
- 不要把机器调试细节塞进 digest

Guardrails:
- Do not read raw coding transcripts as primary input.
- Do not force article updates when there is no signal.
- Do not auto-run heavy deep research.
- Do not create a duplicate truth source outside Brain.
- Do not write run reports into reading or working layers; they belong in `99-SYSTEM/03-INTEGRATION-REPORTS/`.
- Raw article assets (image packs, OCR screenshots, PDFs, debug html, raw responses) must go to `LOCAL-LARGE-FILES/knowledge-sources/`, not Brain Git.
- Do not submit `_images-*`, `images/`, `.raw/`, `raw/`, or source attachments as part of the formal knowledge layer.
