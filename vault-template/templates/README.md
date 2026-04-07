# Templates Directory

This directory contains all reusable note templates for the Obsidian Brain OS vault.

---

## Available Templates

### Core Templates

| Template File | Purpose |
|--------------|---------|
| `article-note-template.md` | For capturing external articles, blog posts, papers, videos, podcasts, and GitHub content. Processed by the `article-notes-integration` pipeline. |
| `project-brief-template.md` | For registering projects in `04-PROJECTS/`. A lightweight briefing layer — not a full project management tool. |
| `daily-brief-template.md` | For the AI-generated daily cockpit view (`01-PERSONAL-OPS/01-DAILY-BRIEFS/`). Updated each morning by the AI. |
| `weekly-plan-template.md` | For weekly planning and scheduling (`01-PERSONAL-OPS/02-PLANS-AND-SCHEDULES/`). |

---

## Template Usage Guidelines

### When to Use Each

- **New external content (article/video/paper)** → `article-note-template.md` → `03-KNOWLEDGE/02-WORKING/01-ARTICLE-NOTES/`
- **New project or project update** → `project-brief-template.md` → `04-PROJECTS/01-ACTIVE/`
- **Daily cockpit (AI-generated)** → `daily-brief-template.md` → `01-PERSONAL-OPS/01-DAILY-BRIEFS/`
- **Weekly planning session** → `weekly-plan-template.md` → `01-PERSONAL-OPS/02-PLANS-AND-SCHEDULES/`

### Frontmatter Fields

All templates include frontmatter with the following standard fields:

| Field | Description |
|-------|-------------|
| `title` | Note title |
| `date` | Creation date (use `{{DATE}}` as placeholder in templates) |
| `owner` | Owner (`{{USER_NAME}}` in templates) |
| `status` | Workflow status (varies by template) |
| `tags` | Array of tags for search and classification |

### Placeholder Syntax

When creating new notes from templates, replace placeholders:

| Placeholder | Replace With |
|-------------|--------------|
| `{{DATE}}` | Current date in `YYYY-MM-DD` format |
| `{{USER_NAME}}` | The owner's name |
| `{{PLACEHOLDER_*}}` | Context-specific value (URL, path, etc.) |
| `{{PROJECT_REF}}` | Unique project identifier (e.g., `proj-blog`) |

---

## Creating a New Note from Template

1. Copy the template file to the target directory
2. Rename to follow naming convention
3. Fill in all `{{PLACEHOLDER}}` fields
4. Set appropriate frontmatter `status`
5. Commit to vault

---

*Maintained by: Brain OS Template Working Group*
*Last updated: {{DATE}}*
