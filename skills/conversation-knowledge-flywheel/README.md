# conversation-knowledge-flywheel

Nightly skill for turning AI conversations into knowledge assets.

## Purpose

This skill exists because cron prompts are too thin for the full workflow. The logic belongs here, with helper scripts and templates.

## Raw source of truth

- `/Volumes/LIZEYU/Converstions`

The skill reads from that root and does not move raw transcripts into {{BRAIN_NAME}}.

## Phase 1 deliverables

- transcript manifest generation
- project grouping
- Brain-side project routing via `05-PROJECTS/`
- QMD-backed candidate recall
- Surveillance pre-screen shortlist
- knowledge-note draft generation
- daily suggestions draft generation
- writer-ready output for {{BRAIN_NAME}}
- commit / visibility checklist

## NotebookLM role

NotebookLM is treated as an **external research amplifier grounded by our internal context**.
It should not be used as a free-floating generic deep-research engine. Before deep research, prepare:
- a NotebookLM context pack
- a constrained research seed

Only Brain OS Manager decides whether a theme deserves NotebookLM reinforcement.

## Responsibility split

- **Brain OS Manager**: integrate recall layers, resolve project routing, decide what becomes knowledge, prepare writer package
- **Writer-Agent**: formally land approved content into Brain, commit, verify Obsidian visibility
- **Surveillance layer**: pre-screen only; no final note decisions

## Project routing rule

`05-PROJECTS/` is the default Brain-side project entrypoint for this skill.
Use it to:
- identify what a project is
- locate source-of-truth paths
- recover aliases / search terms
- attach new knowledge / suggestions / research back to the right project

Do **not** treat `05-PROJECTS/` as the execution source of truth.
That still belongs in Agora / repo / external project systems.

When project mapping is clear, new outputs should carry lightweight anchors such as:
- `project_ref`
- `related_projects`
- optional `project_brief` path

## Main helper files

- `scripts/list-day-transcripts.sh`
- `scripts/build-day-manifest.py`
- `scripts/qmd-project-collections.sh`
- `scripts/render-writer-package.py`
- `templates/conversation-derived-note-template.md`
- `templates/daily-learning-suggestions-template.md`
- `templates/writer-instruction-template.md`
- `templates/notebooklm-context-pack-template.md`
- `templates/notebooklm-research-seed-template.md`
- `examples/nightly-runbook.md`
- `examples/surveillance-scan-spec.md`
