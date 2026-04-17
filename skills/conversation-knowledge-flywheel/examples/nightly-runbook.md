# Nightly Runbook

## Goal

For a given date, turn the previous day's AI conversations into:
- a manifest
- 1-3 knowledge note drafts
- a daily suggestions brief
- optional research seeds / NotebookLM prep packs
- a writer-ready Brain update package

All project-linked outputs should prefer the Brain-side project registry at `05-PROJECTS/` as their lightweight routing anchor.

## Commands

### 1) List transcripts

```bash
/tmp/brain-os-test/skills/conversation-knowledge-flywheel/scripts/list-day-transcripts.sh 2026-04-01
```

### 2) Build manifest

```bash
/tmp/brain-os-test/skills/conversation-knowledge-flywheel/scripts/preflight.sh 2026-04-01
python3 /tmp/brain-os-test/skills/conversation-knowledge-flywheel/scripts/build-day-manifest.py 2026-04-01
```

### 3) Resolve project routing before synthesis

For each likely project:
- map the transcript group to a stable `project_ref` when possible
- read the corresponding `05-PROJECTS/<slug>/project-brief.md`
- use that brief as the Brain-side context anchor
- if project confidence is low, leave the project unresolved instead of hallucinating

### 4) Use the manifest to draft outputs

Generate:
- knowledge note drafts
- daily suggestions block
- optional research seeds

When project mapping is clear, outputs should include lightweight project anchors such as:
- `project_ref`
- `related_projects`
- optional `project_brief` path

### 5) Write to Brain via approved path

Do not direct-write {{BRAIN_NAME}} unless explicitly allowed. Use writer flow.

### 6) Verify completion

Completion means:
- Brain files updated
- git commit exists
- post-commit hook ran
- Obsidian-visible
