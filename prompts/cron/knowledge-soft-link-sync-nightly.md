---
name: knowledge-soft-link-sync-nightly
schedule: "30 4 * * *"
agent: main
model: {{CRON_MODEL}}
enabled: true
description: Daily 04:30 standalone Knowledge ↔ Project soft-link sync
---

# knowledge-soft-link-sync-nightly

You are {{MAIN_AGENT_NAME}}, responsible for running a daily standalone Knowledge ↔ Project soft-link sync.

## Goal

Run `scripts/sync-knowledge-soft-links.py` to make manually declared relationships between knowledge notes and project pages visible in both directions.

This is a **standalone cron**. Do not tightly couple it with the 02:00–04:00 nightly pipeline. The goal is to reduce concurrency pressure and keep debugging boundaries clean.

## Steps

### 1. Get target date

First, fetch yesterday's date from the system clock in local timezone. Do not guess.

- macOS: `date -v-1d +"%Y-%m-%d"`
- Linux: `date --date=yesterday +"%Y-%m-%d"`

Store it as `TARGET_DATE`.

### 2. Initialize run-report directory

Run:

```bash
bash {{BRAIN_ROOT}}/scripts/init-nightly-digest.sh {{BRAIN_ROOT}} "$TARGET_DATE"
```

### 3. Dry run first

Run:

```bash
python3 {{BRAIN_ROOT}}/scripts/sync-knowledge-soft-links.py --dry-run
```

Check whether the output contains:
- `knowledge_updates`
- `project_brief_updates`
- `projects_index_updates`
- `invalid_project_refs`
- `invalid_paths`
- `normalized_paths`

### 4. Run for real

If dry-run looks healthy, then run:

```bash
python3 {{BRAIN_ROOT}}/scripts/sync-knowledge-soft-links.py
```

### 5. Write run report

Write the execution result to:

`{{BRAIN_ROOT}}/03-KNOWLEDGE/99-SYSTEM/03-INTEGRATION-REPORTS/run-reports/$TARGET_DATE/knowledge-soft-link-sync-$TARGET_DATE.md`

Suggested structure:

```md
# Knowledge Soft Link Sync Report — YYYY-MM-DD

status: success | noop | degraded
knowledge_updates: N
project_brief_updates: N
projects_index_updates: N
invalid_project_refs: N
invalid_paths: N
normalized_paths: N

## Summary
- ...

## Dry Run
```text
...
```

## Final Run
```text
...
```
```

### 6. Commit Brain changes if needed

If this run changed files in Brain, run:

```bash
cd {{BRAIN_ROOT}}
git add scripts/sync-knowledge-soft-links.py scripts/knowledge-lint.sh 03-KNOWLEDGE 05-PROJECTS 04-SYSTEM/prompts/cron/knowledge-soft-link-sync-nightly.md
git commit -m "chore: sync knowledge soft links"
```

If there are no file changes, keep the run report but do not force an empty commit.

### 7. Output a short webhook result

The final reply must be short and should not dump long logs.

Examples:

`✅ Soft-link sync complete YYYY-MM-DD | knowledge 2 / project 2 / index 2 | commit abc1234`

If no changes:

`✅ Soft-link sync complete YYYY-MM-DD | no-op | no commit needed`

If degraded:

`⚠️ Soft-link sync degraded YYYY-MM-DD | invalid refs/path N items | manual review needed`

## Hard rules

1. Do not invent new relationships, only sync explicitly declared ones
2. Do not change note meaning, only add or normalize links
3. Do not fail just because a note has no `related_projects`
4. Invalid project-side paths and invalid refs must be explicitly listed in the report
5. Keep this separate from the nightly pipeline, do not chain other jobs casually
