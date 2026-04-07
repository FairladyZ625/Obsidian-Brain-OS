---
title: "Build Personal Blog"
date: 2026-01-15
project_ref: "proj-personal-blog"
status: active
source_of_truth: "{{PLACEHOLDER_REPO_PATH}}"
owner: "{{USER_NAME}}"
---

# Build Personal Blog

## 一句话说明

A minimal, fast, and AI-friendly personal blog for publishing technical articles and project updates, built with modern static site generation.

## 当前阶段

**Phase 2: Content Migration & SEO Setup**

Migrating legacy articles from the old blog; implementing structured data and OpenGraph tags for better AI and search engine discoverability.

## 当前 Focus

- Migrating 15 existing articles to the new platform
- Setting up RSS and JSON Feed for AI agent subscription
- Implementing auto-generated table of contents per article

## Source of Truth

- 代码库：`{{PLACEHOLDER_REPO_PATH}}`
- 文档：`{{PLACEHOLDER_DOCS_PATH}}`
- 任务：`{{PLACEHOLDER_AGORA_PATH}}` (Agora project: `proj-personal-blog`)

## 相关知识

<!-- 指向 03-KNOWLEDGE/ 里的相关笔记 -->

- `03-KNOWLEDGE/02-WORKING/01-ARTICLE-NOTES/building-personal-knowledge-systems-with-ai.md` — Articles that may become blog posts
- `03-KNOWLEDGE/01-READING/03-PATTERNS/content-pipeline-patterns.md` — Content workflow reference

## 相关待办

<!-- 指向 00-INBOX/todo-backlog.md 里的相关条目 -->

- `[P2] Migrate legacy notes to new domain structure` — will include blog article migration workflow

## 关键决策记录

| 日期 | 决策 | 原因 |
|------|------|------|
| 2026-01-15 | Use static site generator (Astro) | Zero runtime overhead, native Markdown support, AI-friendly output |
| 2026-02-20 | Self-host instead of using Medium/Toutiao | Full control over data, branding, and AI-readable markup |
| 2026-03-10 | Add RSS + JSON Feed | Enable AI agents to subscribe to new content without scraping |

## 检索关键词 / Aliases

`blog`, `personal-site`, `static-site`, `writing-platform`, `content publishing`
