# Cron Rules

## When to read this

Read before creating or editing scheduled jobs, cron prompts, heartbeat prompts, or recurring automation.

## Core rule

Scheduled agents need explicit inputs, safe fallbacks, and quiet failure modes. Do not rely on hidden chat context.

## Procedure

1. State the job purpose in one sentence.
2. Define schedule, timezone, model, and target agent.
3. Use an isolated session unless the job intentionally continues a known thread.
4. Include exact paths and placeholders.
5. Define degraded mode when optional dependencies are missing.
6. Define delivery target: quiet, file-only, or channel announcement.
7. Keep user-facing output short; put detailed logs in files.
8. Add verification or smoke test instructions.

## Common mistakes

- Assuming the cron job remembers prior chat context.
- Hardcoding private paths or channel IDs in public examples.
- Making every failure noisy.
- Claiming optional tools, such as QMD, are bundled with the runtime.

## Public examples

- `cron-examples/nightly-pipeline.json`
- `cron-examples/personal-ops.json`
- `cron-examples/governance.json`
- `docs/writing-cron-prompts.md`
