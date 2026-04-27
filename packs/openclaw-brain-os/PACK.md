# PACK.md — Agent Instructions for OpenClaw Brain OS Pack

You are installing or reviewing the OpenClaw Brain OS distribution pack.

## Read order

1. `manifest.json`
2. `README.md`
3. `openclaw.json.patch.template`
4. `workspaces/main/AGENTS.md`
5. `vault/README.md`
6. `tests/smoke.sh`

## Critical rules

- This pack is a template, not a copy of a private runtime.
- Do not include private memory, credentials, cookies, logs, real Discord IDs, or local private paths.
- Treat root `vault-template/` as canonical.
- Do not blindly overwrite an existing `openclaw.json`.
- Do not enable cron jobs by default.
- If a target file already exists, skip by default and report the conflict.

## First implementation milestone

PR2 adds conservative safe apply, conflict detection, backup, and rollback.

Never overwrite conflicting user config by default. Apply must require explicit `--yes`, cron jobs must remain disabled, and rollback must restore config backups without deleting user workspace, skills, or vault files.
