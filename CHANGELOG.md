# Changelog

All notable changes to Obsidian Brain OS are documented here.

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
