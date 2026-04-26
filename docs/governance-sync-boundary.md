# Governance Sync Boundary

This document explains what should and should not be synced from a private Brain OS deployment back into the public Obsidian Brain OS repository.

## One-sentence rule

> Open-source reusable framework capability, not your private operating system.

Before syncing anything, ask:

> If a stranger forks this repository, is this useful as a reusable Brain OS pattern, or is it only meaningful inside my personal/team setup?

If it is reusable, consider syncing it. If it is private glue, do not sync it.

## Default categories

### A. Mainline framework assets — sync candidates

Sync when most of these are true:

- directly supports the Brain OS knowledge / governance / automation model
- understandable without your private team context
- reusable by another user after placeholder replacement
- safe after de-identification
- belongs in skills, docs, templates, prompts, scripts, schemas, or cron examples

Examples:

- generic knowledge ingestion skills
- vault governance skills
- nightly pipeline prompts
- lint / validation scripts
- anonymized cron examples
- setup and install documentation
- reusable schemas and templates

### B. Boundary assets — human review required

Treat as "review before sync" when any of these are true:

- useful pattern but tightly coupled to your roles, channels, tools, or schedule
- requires heavy de-identification
- could be mistaken as the official default workflow
- is more of an internal implementation than a community-facing template

Examples:

- an internal chronicle prompt that contains a reusable friction schema
- a personal ops prompt with a reusable planning idea but private daily rhythm
- a governance ledger that may need abstraction before publication

### C. Private operating assets — do not sync

Do not sync when any of these are true:

- personal schedules, diary, reminders, health, finance, or relationship context
- private team rosters, channel IDs, bot IDs, webhooks, or operational routing
- internal approval workflows
- raw logs, raw transcripts, raw friction samples, or private run reports
- private open-source sync tools that exist only to bridge your vault to this repository
- one-off migration plans or internal project management records

## PII is the last check, not the first

De-identification is necessary but not sufficient.

A file can contain no private information and still be wrong for open source if it only serves your internal operating model.

Use this order:

1. Is it part of Brain OS mainline capability?
2. Is it reusable by an external user?
3. Can it be safely de-identified?

## Name mapping is expected

Private asset names and public asset names may differ.

Example:

| Private concept | Public concept |
|---|---|
| personal vault governance SOP | `brain-vault-governance` skill |
| private sync policy reference | public governance sync boundary doc |

Do not assume an asset is unsynced just because the names differ. Maintain a sync registry in your private project notes when operating a private-to-public sync workflow.

## Recommended sync registry

If you maintain a private Brain OS deployment and periodically sync improvements to the public repository, keep a registry like:

```markdown
| Private asset | Public asset | Status | Last sync | Notes |
|---|---|---|---|---|
| `~/.agents/skills/my-vault-sop/` | `skills/brain-vault-governance/` | synced | 2026-04-26 | public abstraction |
```

The registry prevents future agents from repeatedly classifying already-synced assets as new candidates.

## What to publish instead of private internals

| Private thing | Publish this instead |
|---|---|
| raw team prompt | anonymized prompt template |
| private operating rule | reusable governance principle |
| personal schedule cron | generic cron example with placeholders |
| raw run report | report template or schema |
| internal migration plan | stable user-facing documentation |
| private script with hardcoded paths | parameterized script + config example |

## Minimum checklist before syncing

- [ ] The asset is a reusable Brain OS capability.
- [ ] Private names, paths, IDs, webhooks, and project details are removed.
- [ ] User-specific rhythms are generalized or moved to examples.
- [ ] Raw logs and evidence are not included.
- [ ] Placeholders are documented.
- [ ] The public file has a clear home in this repository.
- [ ] Changelog or release notes are updated when appropriate.

## Conservative default

When uncertain, do not sync the raw asset.

Instead, create a short plan or issue describing:

- what might be reusable
- what is private
- what abstraction would be needed
- who should decide
