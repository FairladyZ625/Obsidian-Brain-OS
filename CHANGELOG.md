# Changelog

All notable changes to Obsidian Brain OS are documented here.

---

## [0.5.2] — 2026-04-14

### Added
- **`docs/nightly-knowledge-flywheel-ops.md`** — Operations guide for the 02:00 / 03:00 / 04:00 nightly knowledge flywheel stages: success definition, rerun rules, alert conditions, and why no-op results are valid.

### Changed
- **`skills/article-notes-integration/SKILL.md`** — Added the Raw Asset Storage Rule to distinguish formal knowledge outputs from raw captured assets, routing screenshots / OCR bundles / PDFs / raw responses into `LOCAL-LARGE-FILES/knowledge-sources/` instead of Brain Git.
- **`prompts/article-notes-integration.prompt.md`** — Added matching raw-asset guardrails so the nightly 02:00 stage does not commit `_images-*`, `images/`, `.raw/`, `raw/`, or other source attachments into the formal knowledge layer.
- **`skills/deep-research/skill.md`** — Reverted the community version back to English for broader readability.

---

## [0.5.1] — 2026-04-13

### Added
- **`docs/component-guide.md`** — Complete component guide: everything included in v0.5, what each component does, how to start using it, 5-minute quick start. Bilingual (Chinese + English).
- **README.md** + **`README_CN.md`** — Added component guide as first item in contributor docs section.

---

## [0.5.0] — 2026-04-13

### Added
- **`CHANGELOG_CN.md`** — Chinese changelog mirroring English version (bilingual).
- **`docs/agent-playbooks/release-playbook.md`** — Complete release SOP: 7-step process, bilingual PR template, common pitfalls.
- **`docs/agent-playbooks/observer-playbook.md`** — Observer usage guide: 6-step process, three-level safety mechanism, configuration.
- **`docs/references/pii-deidentification-guide.md`** — PII deidentification guide: 4 PII categories, standard replacement table, common fixes.
- **`docs/writing-cron-prompts.md`** — Cron prompt best practices: system date fetch, output format, cross-prompt coordination.
- **`docs/skill-authoring-guide.md`** — Skill authoring conventions: SKILL.md structure, naming, CI requirements.
- **`docs/nightly-pipeline-guide.md`** — Full nightly pipeline architecture: 4 stages, handoff protocol, failure handling.

### Changed
- **`skills/brain-os-release/SKILL.md`** — Step 3 now requires updating BOTH `CHANGELOG.md` and `CHANGELOG_CN.md`; Step 5 adds mandatory bilingual PR template.
- **`.github/workflows/changelog-check.yml`** — CI now covers `CHANGELOG_CN.md`; docs/ changes are encouraged but not required.
- **`scripts/check-pii.sh`** — Exclude `pii-deidentification-guide` from scan (contains educational example paths).
- **`README.md`** + **`README_CN.md`** — Added contributor docs section with links to all new documents.

---

## [0.4.1] — 2026-04-13

### Fixed

- **`prompts/cron/chronicle-every-2h-log.md`** — Added mandatory system date fetch step so `YYYY-MM-DD` is always derived from the system clock, not guessed by the model, using the running machine's local timezone.
- **`prompts/cron/daily-knowledge-graph-canvas-0500.md`** — Added Step 0 to fetch system date/day-of-week/timezone before generating the daily canvas; commit message note now explicitly requires system-derived dates.
- **`prompts/cron/knowledge-lint-weekly.md`** — Added mandatory `target date (yesterday)` fetch via system command and clarified that downstream lint/report paths must use the system-derived date in the running machine's local timezone.

---

## [0.4.0] — 2026-04-12

### Added

- **`skills/brain-os-release/SKILL.md`** — Release SOP skill for maintainers and contributors: version bump rules, PII check, CHANGELOG update, PR template, merge and tag steps.
- **`scripts/check-pii.sh`** — PII scan script: checks for absolute paths, unresolved `{{PLACEHOLDER}}` tokens, and Discord-style IDs. Run manually or via CI.
- **`.github/workflows/pii-scan.yml`** — CI: runs `check-pii.sh --strict` on every PR and push to main. Fails if PII found.
- **`.github/workflows/structure-check.yml`** — CI: verifies every skill has `SKILL.md` and every script has a shebang.
- **`.github/workflows/changelog-check.yml`** — CI: warns (non-blocking) if `skills/`, `scripts/`, or `prompts/` changed without a CHANGELOG update.
- **`skills/observer/SKILL.md`** — Observer skill: daily AI team health monitor. Collects session data + gateway logs, updates `.learnings/` ledger, generates iteration plan, announces to observer channel. Three-level safety mechanism (alert / suggest / execute with human confirmation).
- **`skills/observer/references/plan-template.md`** — Iteration plan template for Observer output.
- **`prompts/cron/observer-daily-0001.md`** — Daily 00:01 cron prompt template for Observer (disabled by default).
- **`README.md`** — Added Star History chart.

### Changed

- **`prompts/cron/brain-os-daily-sync.md`** (private, not in repo) — Added Step 7: auto-suggest article direction when A-class syncs >= 3.

---

## [0.3.0] — 2026-04-12

### Added

- **`skills/daily-timesheet/`** — New skill: scan git commits daily, align work to OKR milestones, generate a structured timesheet draft for human confirmation. Supports three write backends: local file, Feishu Bitable, and DingTalk AI Table.
- **`skills/daily-timesheet/references/feishu-bitable.md`** — Feishu Bitable API reference with field mapping and auth flow.
- **`skills/daily-timesheet/references/dingtalk-bitable.md`** — DingTalk AI Table API reference.
- **`prompts/cron/daily-timesheet-1730.md`** — Weekday 17:30 cron prompt template (disabled by default; configure `TIMESHEET_REPOS` and `BRAIN_ROOT` to enable).
- **`scripts/brain-to-reminders.sh`** — Push today's Brain todos to Apple Reminders at 07:30.
- **`scripts/reminders-to-brain.sh`** — Pull completion status from Apple Reminders back to Brain at 21:00.
- **`prompts/cron/brain-to-reminders-0730.md`** — Cron prompt for morning Reminders push.
- **`prompts/cron/reminders-to-brain-2100.md`** — Cron prompt for evening Reminders pull-back.
- **`skills/english-tutor/`** — Interactive listening tutor skill with Whisper transcription and edge-tts voice synthesis.

### Changed

- **`skills/conversation-knowledge-flywheel/SKILL.md`** — Upgraded to transcript-first 3-layer split nightly pipeline architecture with explicit upstream/downstream handoff contracts.
- **`skills/article-notes-integration/SKILL.md`** — Refreshed with English structure, cross-reference protocol, and 02:00 stage contract.
- **`skills/knowledge-flywheel-amplifier/SKILL.md`** — Refreshed with cross-source synthesis protocol and 04:00 stage contract.
- **`prompts/cron/conversation-knowledge-mining-nightly.md`** — Aligned with split pipeline (preflight check, digest-first read, dual-layer output).
- **`prompts/conversation-knowledge-mining.prompt.md`** + **`conversation-knowledge-flywheel.prompt.md`** — Aligned wording with new skill contracts.

### Fixed

- **`scripts/brain-to-reminders.sh`** — `BRAIN_ROOT` now required via env var; exits with a clear error if unset (was silently using literal `{{BRAIN_ROOT}}` as path).
- **`scripts/reminders-to-brain.sh`** — Same fix: `BRAIN_ROOT` required, clear error on missing.
- **`scripts/brain-to-reminders.sh`** — Extraction regex now matches bullet/checklist items (`- task`, `- [ ] task`) in addition to numbered lists.

---

## [0.2.0] — 2026-04-08

### Added

- `skills/conversation-knowledge-flywheel/` — Nightly conversation mining and knowledge synthesis skill.
- `skills/article-notes-integration/` — Article ingestion and knowledge graph integration skill.
- `skills/knowledge-flywheel-amplifier/` — Cross-source knowledge amplification skill.
- `prompts/cron/conversation-knowledge-mining-nightly.md` — Nightly conversation mining cron prompt.
- `cron-examples/` — 7 OpenClaw cron job configuration examples.

---

## [0.1.0] — 2026-03-15

### Added

- Initial release: vault template, setup.sh, core skills, nightly pipeline prompts, docs.
