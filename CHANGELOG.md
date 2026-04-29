# Changelog

All notable changes to Obsidian Brain OS are documented here.

---

## [1.5.8] — 2026-04-29

### Added
- **`skills/brain-os-open-source-sync/`** — Added a dedicated skill for public Brain OS synchronization, including the two-track distribution-pack/methodology model, A/B/C classification, system-upgrade detection, nightly planning workflow, and PR checklist.

### Changed
- **`prompts/cron/brain-os-daily-sync.md`** — Updated daily sync to read the open-source sync skill first and classify candidates by distribution-pack and methodology tracks before A/B/C scoring.
- **`docs/governance-sync-boundary.md`** / **`docs/zh/governance-sync-boundary.md`** — Documented the two public sync tracks so maintainers can separate installable package assets from reusable methodology assets.

## [1.5.7] — 2026-04-27

### Added
- **Install report** — Pack dry-run and apply now generate `INSTALL_REPORT.md` summarizing selected profile, paths, selected assets, backups, changes, next steps, and rollback guidance.
- **Profile guide** — Added `packs/openclaw-brain-os/PROFILE_GUIDE.md` to help users choose `minimal`, `knowledge`, `personal-ops`, `team`, or `full`.
- **Post-install checklist** — Added `packs/openclaw-brain-os/POST_INSTALL_CHECKLIST.md` for safe validation before enabling cron jobs.

### Changed
- **`packs/openclaw-brain-os/manifest.json`** — Bumped pack preview version to `1.0.0-alpha.5` for install-report milestone.

## [1.5.6] — 2026-04-27

### Added
- **OpenClaw Brain OS pack profiles** — Added profile-specific cron patch templates for minimal, knowledge, personal-ops, team, and full profiles, generated from public cron examples with all jobs disabled by default.
- **Bundled skills** — Added sanitized public skill bundles for Brain vault governance, article integration, conversation flywheel, knowledge amplifier, personal ops, observer, and Brain OS release workflows.
- **Skill installation support** — Apply now copies selected bundled skills in missing-only mode according to the selected profile.

### Changed
- **`packs/openclaw-brain-os/manifest.json`** — Bumped pack preview version to `1.0.0-alpha.4` and aligned profile cron groups.

## [1.5.5] — 2026-04-27

### Added
- **OpenClaw Brain OS pack safe apply** — Added config conflict detection, conservative OpenClaw config merge, cron job merge, temp-safe apply flow, backup state, and rollback script for config files.
- **Apply smoke fixture** — Pack smoke now applies into an isolated temp OpenClaw root and verifies rollback without touching real user config.

### Changed
- **`packs/openclaw-brain-os/manifest.json`** — Bumped pack preview version to `1.0.0-alpha.3` for the safe-apply milestone.

## [1.5.4] — 2026-04-27

### Added
- **OpenClaw Brain OS pack dry-run installer** — Added `install.sh --check`, `install.sh --dry-run`, `verify.sh`, render/placeholder/secret-scan helper scripts, minimal/full dry-run fixtures, and smoke coverage for preview generation.
- **Multi-workspace templates** — Added initial writer, review, chronicle, and observer workspace templates as available preview assets.

### Changed
- **`packs/openclaw-brain-os/manifest.json`** — Bumped pack skeleton to `1.0.0-alpha.2` for the dry-run preview milestone.

## [1.5.3] — 2026-04-27

### Added
- **`packs/openclaw-brain-os/`** — Added the first static skeleton for an installable OpenClaw Brain OS distribution pack, including manifest, scope-limited OpenClaw config patch template, main workspace bootstrap, canonical vault-template strategy, skill manifest, disabled cron placeholder, and smoke test.
- **`.github/workflows/pack-smoke.yml`** — Added CI coverage for pack JSON validity, canonical vault-template checks, disabled cron defaults, forbidden config scope, and private/secret material scanning.

### Changed
- **`docs/feature-matrix.md`** / **`docs/zh/feature-matrix.md`** and README entry points — Added discoverability for the OpenClaw Brain OS install pack.

## [1.5.2] — 2026-04-27

### Added
- **`examples/agent-workspace/AGENTS.example.md`**, **`examples/agent-workspace/USER.example.md`**, and **`examples/agent-workspace/references/`** — Added sanitized copyable agent workspace bootstrap templates.
- **`examples/openclaw/openclaw.channel-prompts.example.json`** — Added an OpenClaw example for per-channel Discord `systemPrompt` entries under `channels.discord.accounts.<accountId>.guilds.<guildId>.channels`.
- **`docs/agent-bootstrap-guide.md`** / **`docs/zh/agent-bootstrap-guide.md`** — Added bilingual guidance for writing small `AGENTS.md` files and organizing on-demand `references/` manuals.

### Changed
- **`docs/feature-matrix.md`** / **`docs/zh/feature-matrix.md`** — Added Agent bootstrap + references as a Core feature with install and verification checks, and clarified that specialized Discord channels can be verified by checking their per-channel `systemPrompt` entries.
- **`README.md`**, **`README_EN.md`**, and **`docs/zh/README.md`** — Added discoverability links for the agent bootstrap guide and examples.

## [1.5.1] — 2026-04-27

### Added
- **`examples/openclaw/openclaw.example.json`** and **`examples/openclaw/openclaw.multi-channel.example.json`** — Added sanitized OpenClaw config examples for single-agent and multi-channel Discord setups.
- **`docs/openclaw-config-guide.md`** / **`docs/zh/openclaw-config-guide.md`** — Added bilingual guidance for `openclaw.json`, channel routing, cron delivery, placeholders, secrets, and QMD boundaries.
- **`docs/feature-matrix.md`** / **`docs/zh/feature-matrix.md`** — Added a feature matrix SSOT so users and agents can see every public Brain OS capability, its install assets, and its verification checks.

### Changed
- **`docs/qmd-setup.md`** / **`docs/zh/qmd-setup.md`** — Clarified that QMD is a separately installed retrieval engine, not a bundled OpenClaw component.
- **`docs/openclaw-setup.md`**, **`docs/zh/openclaw-setup.md`**, **`docs/getting-started.md`**, **`docs/zh/getting-started.md`**, **`docs/component-guide.md`**, **`README.md`**, and **`README_EN.md`** — Added links and wording so users configure OpenClaw channels and QMD separately and can find the feature matrix.
- **`scripts/config.env.example`** — Documented optional `QMD_BIN` / `QMD_BIN_REAL` environment variables for deployments where QMD is not on `PATH`.

### Fixed
- Removed wording that could lead users or agents to claim that QMD comes with OpenClaw by default.

## [1.5.0] — 2026-04-27

### Changed
- **`prompts/cron/personal-ops-morning-brief.md`** and **`prompts/personal-ops-morning-brief.prompt.md`** — Added the Insight Analysis / 洞察落地 module for daily briefings, using an HV-lite horizontal/vertical method to connect external knowledge signals with active projects, todos, blockers, deadlines, and recent conversation-derived ideas.
- **`docs/personal-ops.md`** / **`docs/zh/personal-ops.md`** — Documented that Personal Ops can run lightweight insight analysis, not only task prioritization and reminders.

### Fixed
- Made “no high-confidence insight today” visible in the briefing output by requiring candidate observations and rejection reasons instead of silently omitting the insight section.

## [1.4.0] — 2026-04-27

### Changed
- **`tools/conversation-mining/`** — Synced the embedded Conversation Mining tool to the latest upstream implementation from `FairladyZ625/conversation-mining`, including the updated exporter, viewer assets, Codex recency indexing fixes, transcript export helpers, and CLI behavior.
- **`tools/conversation-mining/pyproject.toml`** — Bumped the embedded tool version from `0.1.0` to `0.2.0` so downstream agent installers can identify the newer conversation mining capability.

### Fixed
- Ensured users who install or vendor Conversation Mining through Obsidian Brain OS receive the latest agent conversation export/mining scripts instead of the older embedded copy.

## [1.3.0] — 2026-04-26

### Added
- **`skills/brain-vault-governance/`** — Added a reusable vault governance skill for agents writing, moving, classifying, and auditing durable Brain OS vault files.
- **`docs/governance-sync-boundary.md`** / **`docs/zh/governance-sync-boundary.md`** — Added bilingual guidance for deciding what should be synced from a private Brain OS deployment into the public repository.
- **`docs/release-versioning.md`** / **`docs/zh/release-versioning.md`** — Added bilingual release versioning rules for patch / minor / major decisions and changelog expectations.
- **`docs/governance-cron-guide.md`** / **`docs/zh/governance-cron-guide.md`** — Added bilingual guidance for running read-only vault governance audits.
- **`prompts/cron/brain-governance-audit.prompt.md`** and **`cron-examples/governance.json`** — Added an anonymized governance audit prompt and importable OpenClaw cron example.

### Changed
- **`README.md`**, **`README_EN.md`**, **`docs/getting-started.md`**, **`docs/zh/getting-started.md`**, **`docs/skills-guide.md`**, **`docs/zh/skills-guide.md`**, **`docs/zh/README.md`**, **`INSTALL_FOR_AGENTS.md`**, and **`cron-examples/README.md`** — Added discoverability and setup guidance for vault governance.

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

## [1.2.0] — 2026-04-23

### Added
- **`docs/friction-report-template.md`** / **`docs/zh/friction-report-template.md`** — Structured friction report template (bilingual)
- **`docs/references/friction-bucket-guide.md`** / **`docs/zh/friction-bucket-guide.md`** — Standard friction bucket taxonomy (bilingual)
- **`docs/references/friction-writeback-matrix.md`** / **`docs/zh/friction-writeback-matrix.md`** — Decision matrix for write-back layer selection (bilingual)
- **`schemas/friction-event.schema.json`** — JSON schema for a single friction signal
- **`schemas/friction-report.schema.json`** — JSON schema for aggregated friction reports
- **`examples/friction-log.sample.jsonl`** — 5 example friction signals in JSONL format

### Changed
- **`INSTALL_FOR_AGENTS.md`** — Added friction-to-governance loop to Advanced profile and install routing
- **`docs/install-profiles.md`** — Advanced profile now includes governance stack + friction loop
- **`docs/component-guide.md`** — Updated from v0.5 to v1.1.0; added governance stack + friction loop sections

## [1.1.0] — 2026-04-23

### Added
- **`docs/zh/friction-to-governance-loop.md`** — Added a Chinese companion document for the friction-to-governance loop so the governance pattern is documented bilingually.
- **`prompts/friction-to-governance-loop.prompt.md`** — Added a reusable prompt template for diagnosing repeated friction and converting it into governance write-backs.
- **`docs/references/system-governance-guide.md`** — Added a reference guide for deciding where recurring problems should be written back into the system.

### Changed
- **`README.md`** — Updated the friction-to-governance entry to point to both English and Chinese documents.

## [1.0.1] — 2026-04-23

### Added
- **`docs/friction-to-governance-loop.md`** — Added a new governance pattern document for turning repeated friction signals into prompts, references, AGENTS, workflow, and onboarding improvements.

### Changed
- **`README.md`** — Added a direct entry point to the friction-to-governance loop so maintainers and contributors can find the governance pattern from the main documentation surface.

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
