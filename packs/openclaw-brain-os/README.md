# OpenClaw Brain OS Pack

This pack is the installable distribution form of Obsidian Brain OS for OpenClaw.

It is different from the rest of the repository:

- `docs/` teaches users how Brain OS works.
- `examples/` provides small copyable snippets.
- `packs/openclaw-brain-os/` is a self-contained install pack that an agent can apply to an existing OpenClaw installation.

Current status: **safe apply preview**. The pack can run `--check`, render and verify a dry-run preview, apply into a target OpenClaw root with backups, and roll back backed-up config files. Apply remains conservative: it refuses to run without `--yes`, skips existing workspace/vault files by default, and does not overwrite conflicting config unless future workflows explicitly opt into force mode.

## What this pack installs

The target full pack will install or patch:

- OpenClaw agent/workspace configuration
- per-channel Discord `systemPrompt` entries
- Brain OS agent workspace bootstrap files
- Brain OS skills into `~/.agents/skills`
- Brain vault structure from the repository root `vault-template/`
- cron job templates, installed disabled by default

## Canonical vault template

The canonical Brain OS vault template is the repository root:

```text
../../vault-template/
```

This pack does not maintain a second full vault template. The installer should copy the root `vault-template/` into the user's chosen Brain vault path, then apply pack-specific overlays only if needed.

## Safety rules

- Do not commit real tokens, webhook URLs, Discord IDs, user IDs, or private local paths.
- Do not copy runtime data such as credentials, cookies, memory sqlite files, logs, browser state, or delivery queue data.
- Cron jobs must default to `enabled: false`.
- Config writes must use patch + conflict detection, not blind deep merge.
- Existing user config should be skipped by default when conflicts exist.

## Commands

Available now:

```bash
bash install.sh --check
bash install.sh --dry-run
bash install.sh --answers answers.json --out /tmp/brain-os-preview
bash verify.sh /tmp/brain-os-preview
bash install.sh --answers answers.json --apply --yes
OPENCLAW_ROOT=~/.openclaw bash rollback.sh
```

Run the smoke test:

```bash
bash tests/smoke.sh
```
