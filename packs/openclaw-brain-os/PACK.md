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

PR1b adds non-destructive dry-run rendering and preview verification.

Do not implement destructive apply behavior until patch preview, conflict detection, backup, and rollback are present.
