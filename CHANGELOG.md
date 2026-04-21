# Changelog

All notable changes to Obsidian Brain OS are documented here.

---

## [0.7.0] — 2026-04-20

### Added
- **`INSTALL_FOR_AGENTS.md`** — Added a dedicated agent-first installation guide with a single linear happy path and a default Minimal profile recommendation.
- **`docs/install-profiles.md`** — Added explicit Minimal / Standard / Advanced install tiers so onboarding can scale from first-run to full-system adoption.
- **`scripts/verify-install.sh`** — Added a post-install verifier that checks config, vault structure, installed skills, lint execution, and PII scan results.
- **`.github/workflows/install-smoke.yml`** — Added CI smoke coverage for `setup.sh --non-interactive --profile minimal` followed by `verify-install.sh`.

### Changed
- **`setup.sh`** — Added non-interactive CLI flags, profile-aware skill installation, cross-platform placeholder replacement, and cleaner day-one next-step guidance.
- **`README.md`**, **`README_EN.md`**, **`docs/getting-started.md`**, **`docs/zh/getting-started.md`**, **`docs/component-guide.md`** — Reworked install entry points around agent install, install profiles, verification, and the minimal-success path.
- **`skills/brain-os-installer/SKILL.md`** — Re-aligned the installer skill to the current docs tree and removed guidance that implied unsupported install flows.

### Fixed
- Removed onboarding drift where the repo described install layering, but the setup flow still behaved like a broad all-in install.
- Removed macOS-only in-place replacement behavior from `setup.sh`, improving Linux friendliness for agent-driven installs and CI.

## [1.0.0] — 2026-04-21

### Added
- **`prompts/cron/qmd-index-refresh-daily.md`** — Added a daily QMD refresh cron template to keep vault and workspace search indexes fresh.
- **`prompts/cron/knowledge-librarian-3day.md`** — Added a 3-day knowledge maintenance cron template for frontmatter repair, link audit, tag normalization, duplicate detection, and digest consolidation.
- **`prompts/cron/knowledge-governance-10day.md`** — Added a 10-day governance cron template for domain health review, semantic drift detection, staleness review, archive suggestions, and MOC review.

### Changed
- The OSS knowledge workflow now covers not only knowledge creation, but also freshness, maintenance, and governance as a reusable operating pattern.
- **`docs/getting-started.md`**, **`docs/zh/getting-started.md`**, and **`INSTALL_FOR_AGENTS.md`** — Updated install and onboarding guidance so agents and users understand that the new governance stack is a staged expansion after a working minimal setup, not a default first-run requirement.

## [0.6.1] — 2026-04-18

### Added
- **`prompts/cron/knowledge-soft-link-sync-nightly.md`** — Added a standalone nightly prompt for Knowledge ↔ Project soft-link sync so project references can be repaired in both directions without coupling to the main 02:00–04:00 pipeline.
- **`scripts/sync-knowledge-soft-links.py`** — Added a reusable script to sync explicitly declared knowledge ↔ project relationships across knowledge notes, project briefs, and the projects index.

### Changed
- **`scripts/knowledge-lint.sh`** — Upgraded the lint script to be project-aware: validates `project_ref` and `related_projects`, checks project-side knowledge paths, and writes both a review report and a run-report suitable for nightly operations.


### Added
- **`scripts/check-brain-config-leaks.sh`** — Added a dedicated config-leak scanner to catch author-specific vault names, private paths, internal names, and fixed IDs before they reach OSS.
- **`.github/workflows/brain-config-scan.yml`** — Added CI enforcement for the config-leak scanner on PRs and pushes to main.
- **`prompts/cron/brain-os-daily-sync.md`** — Added the OSS-facing Brain OS daily sync prompt for evaluating local upgrades and generating sync plans.
- **`docs/references/knowledge-asset-boundaries.md`** — Added an OSS-facing governance guide for separating formal knowledge outputs from raw captured assets.
- **`docs/references/vault-governance-guide.md`** — Added an OSS-facing vault governance guide for directory discipline, plan placement, and structure evolution.

### Changed
- **`README.md`**, **`README_EN.md`**, **`docs/getting-started.md`**, **`docs/openclaw-setup.md`**, **`docs/obsidian-setup.md`**, **`setup.sh`** — Clarified that vault naming is user-defined, and aligned `BRAIN_PATH` / `{{BRAIN_ROOT}}` as the user-facing vault root concept.
- **Multiple prompts, skills, and support scripts** — Replaced author-specific vault names, private absolute paths, internal agent names, and fixed IDs with reusable placeholders or environment-based path resolution.
- **`scripts/scan-today-changes.sh`** — Switched Brain path discovery from a hardcoded vault name to `BRAIN_ROOT` with a safe fallback.
- **`scripts/check-pii.sh`** — Aligned PII scanning with the new config-leak scanner so the two checks do not conflict.

### Fixed
- Removed lingering OSS confusion where parts of the repo still implied users had to name their vault `ZeYu-AI-Brain` or match the maintainer's local machine layout.
- Reduced onboarding ambiguity by making install, docs, prompts, and CI use the same path and naming model.

---

## [0.5.3] — 2026-04-14

### Changed
- **`README.md`** — Switched the default GitHub README to Chinese, preserved Karpathy / LLM Wiki as an external reference point (not the project origin), and rewrote the first-screen positioning around "digital twin", "second brain", "24-hour personal operator", and boundary-controlled work agents; restored Star History to the default homepage.
- **`README_EN.md`** — Added the previous English README as the preserved English entry point.
- **`README_CN.md`** — Converted into a compatibility redirect to the new default Chinese `README.md`.

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
