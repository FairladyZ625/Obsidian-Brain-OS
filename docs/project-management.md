# Project Management — Lightweight Registry and Tool Recommendations

---

## Brain OS Philosophy on Projects

Brain OS is not a project management tool. It's a **personal context system**.

For project management, Brain OS provides:
1. **A lightweight project registry** (`04-PROJECTS/`) — just enough to give AI context
2. **Integration recommendations** for external tools

---

## The Lightweight Project Registry

### When to Use It

- You have a project that's < 5 lines of context
- You want AI to know what you're working on
- You need a quick reference to external project links

### When NOT to Use It

- You need kanban boards, burndown charts, or sprint planning
- You're managing a team with multiple contributors
- You need issue tracking with assignments and due dates

→ Use an external tool instead.

---

## Project Brief Format

Each project gets one markdown file in `04-PROJECTS/01-ACTIVE/`:

```yaml
---
title: "My Project"
date: 2026-04-07
project_ref: "my-project"
status: active          # active | paused | completed
source_of_truth: "https://github.com/user/repo"
owner: "{{USER_NAME}}"
tags: [web, side-project]
---

# My Project

## One-Liner
Build a personal blog with AI-powered content suggestions.

## Current Phase
MVP Development

## Current Focus
Setting up the article generation pipeline.

## Source of Truth
- Code: `https://github.com/user/my-blog`
- Tasks: `https://github.com/user/my-blog/issues`
- Docs: `{{BRAIN_PATH}}/04-PROJECTS/01-ACTIVE/my-project.md`

## Related Knowledge
- [[content-generation-patterns]]
- [[ai-writing-assistants]]

## Key Decisions
| Date | Decision | Reason |
|------|----------|--------|
| 2026-04-01 | Use Astro framework | Best static site performance |

## Search Keywords
my-blog, astro, content-generation, side-project
```

---

## Recommended External Tools

### 1. Agora — Multi-Agent Governance Framework

**Best for:** Orchestrating multiple AI agents with structured deliberation and human-gated decision making.

Agora is an orchestration and governance layer for multi-agent systems. It provides:

- **Staged deliberation** — Citizens (agents) debate, Archon (human) decides, Craftsman (executor) delivers
- **Explicit governance semantics** — not prompt folklore, but structured orchestration
- **Human-gated decisions** — execution only starts after human approval
- **Auditable delivery** — chat logs ≠ delivery; Agora tracks actual outcomes

**How it pairs with Brain OS:**

| Brain OS | Agora |
|----------|-------|
| Personal knowledge & context | Multi-agent orchestration |
| What you know | How agents collaborate |
| Single-user knowledge management | Multi-agent governance |
| Vault is the knowledge store | Agora is the decision arena |

Brain OS's project briefs give agents **context** about what they're working on. Agora gives them **structure** for how to collaborate on it.

**Integration pattern:**
1. Create project briefs in `04-PROJECTS/` referencing Agora task URLs
2. Agora agents read project context from Brain OS when working on tasks
3. Knowledge generated during Agora deliberation flows back into `03-KNOWLEDGE/`

**Repository:** [github.com/FairladyZ625/Agora](https://github.com/FairladyZ625/Agora)

### 2. Linear

**Best for:** Software teams that need fast, modern issue tracking.

Clean interface, great keyboard shortcuts, good API. Link tasks to Brain OS project briefs.

### 3. GitHub Issues / Projects

**Best for:** Open-source projects or teams already on GitHub.

No additional setup needed. Reference issue URLs in project briefs.

---

## Integration Pattern

```
Brain OS (04-PROJECTS/)
    │
    │  "What am I working on?"
    │  AI reads project briefs for context
    │
    ├──→ Agora / Linear / GitHub Issues
    │    "How do agents collaborate on it?"
    │    Governance and task tracking happens here
    │
    └──→ 03-KNOWLEDGE/
         "What have I learned?"
         Knowledge from project work flows here
```

---

## Project Lifecycle

```
01-ACTIVE/      ← Currently working on
    │
    ├─→ 02-PAUSED/     ← On hold (with reason)
    │       │
    │       └─→ 01-ACTIVE/  (resumed)
    │
    └─→ 03-COMPLETED/  ← Done (with retrospective notes)
```

When moving a project:
1. Update `status` in frontmatter
2. Move the file to the appropriate directory
3. Add a brief note about why it moved
4. For completed projects: add key learnings to `03-KNOWLEDGE/`
