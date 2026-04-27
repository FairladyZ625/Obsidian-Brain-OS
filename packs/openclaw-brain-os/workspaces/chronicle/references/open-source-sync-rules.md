# Open Source Sync Rules

## When to read this

Read before copying private/local Brain OS material into a public repository, example, template, docs page, or PR.

## Core rule

Open source Brain OS is a reusable framework, not a mirror of a private operating system.

A thing is a good public candidate only if it remains useful after private names, paths, IDs, and local workflows are removed.

## Decision checklist

Classify each candidate:

| Class | Meaning | Action |
|---|---|---|
| A | Mainline framework asset, reusable, de-identified | Can sync |
| B | Potentially reusable but tied to local workflow | Ask / mark pending |
| C | Internal-only operations or private context | Do not sync |

Ask these questions:

1. Is this part of the Brain OS public framework?
2. Would a stranger understand and reuse it after setup?
3. Does it avoid private names, IDs, paths, tokens, screenshots, or logs?
4. Is it a template/method, not a live private configuration?
5. Is there a doc or example explaining how to use it?

## Common mistakes

- Assuming “de-identified” means “worth open sourcing.”
- Publishing internal sync machinery instead of the reusable framework pattern.
- Copying a real `AGENTS.md` instead of an example template.
- Leaving real channel IDs, webhooks, local paths, or human names in examples.

## Preferred output

When unsure, produce three lists:

1. Recommended to sync
2. Needs owner confirmation
3. Should stay private
