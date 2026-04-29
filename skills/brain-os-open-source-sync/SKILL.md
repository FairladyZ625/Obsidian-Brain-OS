---
name: brain-os-open-source-sync
description: Plan and execute safe public synchronization from a private Brain OS deployment to the Obsidian Brain OS open-source repository. Use for nightly daily-sync plans, release PR preparation, deciding whether private changes should become public assets, and classifying distribution-pack versus methodology sync candidates.
---

# Brain OS Open Source Sync

## When to use

Use this skill when planning or executing public synchronization from a private Brain OS deployment into the Obsidian Brain OS open-source repository, especially for nightly daily-sync plans, release PR preparation, and deciding whether a private change should become a distribution-pack asset, methodology asset, review item, or no-sync item.

## Core contract

Sync reusable Brain OS capability, not a private operating system mirror.

Before recommending or publishing any asset, answer:

1. Does this improve the public Brain OS framework?
2. Can an external user understand and reuse it without private context?
3. Can it be safely de-identified without destroying its value?

If uncertain, classify as **B: review required** or **C: do not sync**. Never default to publishing.

## Two-track sync model

Every sync scan must classify candidates into two public tracks before A/B/C scoring.

### Track 1: Distribution pack

Use this track for assets that help users install, verify, operate, or roll back a complete OpenClaw Brain OS package.

Typical assets:

- `packs/openclaw-brain-os/**`
- `setup.sh`, `scripts/verify-install.sh`, installer helpers, smoke tests
- install profiles, manifests, rollback guidance, post-install checklists
- installer or release skills that are public and sanitized
- docs explaining setup, profiles, validation, or feature availability

Ask:

- Would this help a fresh user install or validate Brain OS?
- Does it reduce install risk or clarify operational expectations?
- Does it avoid hardcoded local paths, secrets, real users, and private channels?

### Track 2: Methodology assets

Use this track for reusable operating models, governance patterns, prompt workflows, skills, and knowledge-system methods.

Typical assets:

- public skills that encode repeatable Brain OS workflows
- nightly pipeline prompts and cron examples
- governance, vault, knowledge flywheel, article integration, conversation mining, and personal-ops methods
- templates, schemas, checklists, and public docs explaining how the system works

Ask:

- Does this describe a reusable way to run a knowledge OS?
- Is it a method or pattern rather than a private implementation detail?
- Can it be expressed with placeholders and examples instead of private names?

## A/B/C classification

After assigning a track, classify each candidate:

### A — sync candidate

Publish when most are true:

- belongs to distribution-pack or methodology track
- is public-framework capability, not private glue
- works with placeholders or generic examples
- is understandable from repository context
- has manageable PII risk

### B — review required

Hold for human decision when any are true:

- useful pattern but coupled to a specific team, channel, schedule, or role
- needs heavy abstraction before publication
- could be mistaken as the default product path
- crosses distribution-pack and methodology boundaries in a way that needs positioning

### C — do not sync

Skip when any are true:

- personal schedules, health, diary, reminders, raw conversations, raw logs, private run reports
- team rosters, Discord IDs, bot IDs, webhooks, secrets, private routing
- internal approval flows or one-off migration plans
- private sync tooling whose only purpose is bridging a private vault to this repository
- de-identified but still not useful to the public framework

PII safety is necessary but not sufficient. A safe private workflow can still be wrong for open source.

## System-upgrade detection

Do not reduce a sync plan to changed files. Look for system-level upgrades in three layers.

1. **File-change layer** — What changed?
2. **Capability layer** — What capability became possible, safer, or more complete?
3. **Paradigm layer** — Did the default way of operating Brain OS change?

Escalate from a normal file sync to a methodology/milestone sync when any are true:

- multiple files now form an input → process → output → maintenance loop
- a workflow changed from ad hoc to repeatable
- a new public skill captures a previously prompt-only practice
- an install path moved from manual docs to packaged verification
- a governance rule became stable enough for external users
- the change is better explained as a version/milestone than as a list of diffs

## Nightly sync workflow

When used by a nightly daily-sync cron prompt:

1. Get the system date from the shell.
2. Read this skill first.
3. Read the public/private boundary doc only as supporting detail.
4. Run the local change scanner and repository baseline checks.
5. Filter out private logs, memory, diaries, raw transcripts, and internal state.
6. Cluster remaining candidates by upgrade theme, not by folder.
7. Assign each theme to distribution-pack, methodology, both, or neither.
8. Apply A/B/C classification.
9. For A and B items, list required de-identification and public destination paths.
10. Write a plan with:
    - one-line judgment
    - top three conclusions
    - two-track assessment
    - A/B/C table
    - PII and abstraction work
    - recommended PR scope or reason to stop

If there are no A items, still explain whether the reason is no relevant changes, already-synced baseline, or private-only changes.

## PR execution checklist

Before opening a PR:

- [ ] New or changed skills have `skills/<name>/SKILL.md`.
- [ ] Public-facing docs avoid private names, real paths, IDs, and channel references.
- [ ] Distribution-pack changes update relevant install/profile/verification docs.
- [ ] Methodology changes update relevant governance/nightly/skill docs.
- [ ] `CHANGELOG.md` and `CHANGELOG_CN.md` are updated when skills, scripts, prompts, packs, or setup change.
- [ ] PII scan passes.
- [ ] PR body is bilingual and explains both Chinese and English user value.

## Guardrails

- Keep private sync prompts and internal bridge automation out of the public product surface unless they are abstracted as optional maintainer patterns.
- Prefer a small public abstraction over copying a private asset verbatim.
- Do not publish raw evidence; publish templates, schemas, guides, or sanitized examples.
- If an asset belongs in the private deployment registry rather than this repository, mark it C and stop.
