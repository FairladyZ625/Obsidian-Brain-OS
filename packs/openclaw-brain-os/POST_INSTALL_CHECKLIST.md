# OpenClaw Brain OS Pack Post-install Checklist

After `install.sh --apply --yes`, use this checklist before turning on scheduled jobs.

## 1. Read the install report

Open the generated `INSTALL_REPORT.md` under:

```text
{{OPENCLAW_ROOT}}/.brain-os-pack-installs/<install-id>/INSTALL_REPORT.md
```

Confirm:

- profile is correct
- paths are correct
- expected skills were installed
- expected workspaces exist
- cron jobs are still disabled

## 2. Inspect OpenClaw config

Check:

- `openclaw.json` is valid JSON
- pack agents were added as expected
- Discord channel IDs are correct
- channel `systemPrompt` values are present only where intended
- no existing user config was unexpectedly overwritten

## 3. Inspect workspace files

Check:

- `{{OPENCLAW_ROOT}}/agents/main/agent/AGENTS.md`
- `USER.md`
- `TOOLS.md`
- `references/`

Fill user-specific placeholders only in private local files, not public templates.

## 4. Inspect Brain vault

Check that the Brain vault contains the canonical template structure copied from `vault-template/`.

If the target vault was non-empty, the installer should have skipped overwriting existing files.

## 5. Optional QMD setup

QMD is optional and separately installed. If available, record the binary path in `TOOLS.md` and verify search manually.

If QMD is not installed, Brain OS still works in degraded mode; use filesystem search and direct vault reads.

## 6. Enable cron jobs last

Cron jobs are intentionally installed disabled.

Before enabling:

- verify prompt files exist
- verify delivery channel / Discord account
- verify model names
- run one job manually if possible
- enable one job at a time

## 7. Rollback if needed

If config looks wrong:

```bash
OPENCLAW_ROOT={{OPENCLAW_ROOT}} bash rollback.sh
```

Rollback restores backed-up `openclaw.json` and `cron/jobs.json`. It does not delete workspace, skills, or vault files.
