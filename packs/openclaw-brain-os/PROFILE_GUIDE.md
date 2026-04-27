# OpenClaw Brain OS Pack Profile Guide

Choose the smallest profile that matches the system you want to operate. You can expand later.

## Quick recommendation

| If you want... | Choose |
|---|---|
| A safe first install with vault + main agent workspace | `minimal` |
| Knowledge ingestion, article integration, and nightly knowledge flow | `knowledge` |
| Personal ops dashboards, reminders, and planning workflows | `personal-ops` |
| Multiple agent workspaces for writer/review/chronicle/observer collaboration | `team` |
| Everything above, installed disabled-by-default where scheduled | `full` |

## Profiles

### `minimal`

Installs the core structure:

- main workspace template
- Brain vault template wiring
- `brain-vault-governance` skill
- OpenClaw config patch for main coordination

Best for first-time users and CI smoke tests.

### `knowledge`

Adds knowledge pipeline assets:

- article integration skill
- knowledge-focused channel prompts
- nightly pipeline cron patch, disabled by default

Use this when the vault will receive articles, papers, notes, and AI conversation summaries.

### `personal-ops`

Adds personal operations assets:

- personal ops skill
- personal-ops cron patch, disabled by default
- channel prompt for daily planning and todo triage

Use this when Brain OS should manage commitments, reminders, and daily dashboards.

### `team`

Adds multi-agent operating surfaces:

- writer workspace
- review workspace
- chronicle workspace
- observer workspace
- governance cron patch, disabled by default

Use this when more than one agent role will participate in the system.

### `full`

Installs all current pack assets:

- all workspaces
- all bundled skills
- nightly, personal ops, and governance cron patches, all disabled by default

Use this only when you understand the moving pieces and want the full Brain OS operating model.

## Safety defaults

- Cron jobs are installed with `enabled: false`.
- Skills are installed in `missing-only` mode.
- Existing workspace/vault files are skipped by default.
- Existing config conflicts block apply unless explicitly forced.

## Suggested rollout

1. Start with `minimal`.
2. Run `--dry-run` and inspect `INSTALL_REPORT.md`.
3. Apply only after reviewing the report.
4. Add `knowledge` or `personal-ops` once the core install is stable.
5. Use `team` or `full` after channels, models, and cron delivery have been verified.
