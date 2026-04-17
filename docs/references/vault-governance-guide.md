# Vault Governance Guide

This guide captures reusable governance rules for maintaining a long-lived knowledge vault without letting structure drift.

## 1. Plans and prompts are different things

Use different homes for different artifacts.

- Plans are for people to review, coordinate, approve, and revisit.
- Prompts are for agents and automations to execute.
- Scratch notes are temporary thinking surfaces.

Do not keep formal plans mixed into prompt folders.

## 2. Formal plans need a durable home

Once a plan is stable enough for review or collaboration, move it into the vault's formal project or governance area.

Good default pattern:

- project plans live under the project area
- cross-project governance plans live under a governance area
- temporary drafts may exist in a workspace, but should not remain the long-term source of truth

## 3. Do not create folders from memory

Before creating a folder or numbered area:

- inspect the existing structure
- confirm the numbering scheme at that level
- prefer attaching to an existing parent over creating a parallel structure

## 4. Keep numbering local to the current layer

A child folder should follow the numbering rules of its own level, not blindly mirror top-level numbers.

## 5. Workspace hygiene matters

A workspace should not become a dumping ground. Keep:

- core identity and operating files at the root only when necessary
- prompts in a prompt area
- scripts in a scripts area
- internal references in a references area
- transient outputs in output folders, ideally ignored by Git

## 6. Governance should reduce cognitive load

A good vault rule is not just tidy, it should reduce repeated decisions:

- fewer duplicate truth sources
- clearer document homes
- easier onboarding for humans and agents
- lower chance of accidental structural drift

## 7. What should not be open-sourced directly

Do not publish:

- personal operating details
- internal role choreography
- private logs and diaries
- highly organization-specific glue that has no reusable value

Instead, extract the reusable rule behind the practice and publish that.
