# Knowledge Asset Boundaries

This guide defines what belongs in Git and what should stay in a local large-file area when running a Brain OS style knowledge workflow.

## Core rule

> Git stores the knowledge conclusion layer. Local large-file storage keeps the raw evidence layer.

## What belongs in Git

These are usually safe and useful to keep in the repository:

- distilled article notes
- topic pages
- pattern pages
- digests
- cross-analysis notes
- lightweight metadata and link context
- a very small number of critical images when the image itself is part of the knowledge

## What should stay out of Git

These should normally stay in a local large-file area:

- screenshot batches
- OCR image packs
- raw PDFs
- source attachments
- debug HTML
- raw API responses
- crawler intermediate outputs
- any bulky evidence that supports the note but is not the note itself

## Recommended local layout

```text
LOCAL-LARGE-FILES/knowledge-sources/<domain>/<yyyy-mm-dd>-<slug>/
```

Example:

```text
LOCAL-LARGE-FILES/knowledge-sources/ai-agent/2026-04-12-harness-survey/
```

## Practical ingestion flow

1. Capture source content and raw assets.
2. Store raw assets in local large-file storage.
3. Create the distilled note in the knowledge repository.
4. Reference the source URL and, when useful, the local raw asset path.
5. Do not commit the whole asset pack into the repo.

## Platform-specific caution

Some platforms are image-first or anti-crawler by design. In those cases:

- use the platform-specific capture path first
- do not assume a generic web reader captured the full content
- verify whether the real body lives in images, attachments, or comments

## Why this matters

Without this boundary, repositories become asset dumps instead of knowledge systems. With the boundary, the repo stays readable, sync stays fast, and raw evidence is still recoverable when needed.
