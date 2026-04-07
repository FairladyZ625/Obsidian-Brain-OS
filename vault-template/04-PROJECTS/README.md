# 04-PROJECTS

> Project Registry — Lightweight Briefing Layer

---

## Overview

**This is NOT a full project management system.** It is a lightweight project registry and briefing layer.

The goal is to give AI enough context to understand your active projects without replicating the complexity of a full task tracker.

### When to Use This vs. External Tools

| Scenario | Use This (04-PROJECTS) | Use External Tool |
|----------|------------------------|-------------------|
| Project brief, status, one-liner | ✅ | |
| Task breakdown, sprint board | | ❌ → Use Agora / Linear / GitHub Issues |
| Dependencies, milestones | | ❌ → Use external PM tool |
| Project info fits in <5 lines | ✅ | |
| Needs full Kanban / Gantt | | ❌ → Use external PM tool |

> See `docs/project-management.md` for recommended external tool stack.

---

## Directory Structure

```
04-PROJECTS/
├── 01-ACTIVE/       # Projects currently in progress
├── 02-PAUSED/       # Projects temporarily on hold
└── 03-COMPLETED/    # Finished projects (archived)
```

---

## File Format

Each project gets **one markdown file** using the `project-brief-template.md` template.

Required fields:
- `project_ref` — a short unique identifier (e.g., `proj-blog`, `proj-infra`)
- One-line description
- Current phase / current focus
- Source of truth link (Agora path / GitHub / docs)

---

## Workflow

1. **Register new project** → create a `.md` file in `01-ACTIVE/`
2. **Update status** → edit the frontmatter `status` field
3. **Archive** → move to `03-COMPLETED/` or `02-PAUSED/`
4. **Full task management** → keep in Agora / external system, link from here

---

*Last updated: {{DATE}}*
