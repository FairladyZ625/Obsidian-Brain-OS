# Nightly Knowledge Flywheel Ops

## Chain Overview

- 02:00 `article-notes-integration`
- 03:00 `conversation-knowledge-mining`
- 04:00 `knowledge-flywheel-amplifier`

Each stage must:
- report independently
- commit independently when Brain changed
- tolerate partial upstream failure
- say whether the result is actually Obsidian-visible

## Success Definition by Hour

### 02:00
- article integration report
- article-related updates only
- no-op accepted when no signal
- raw article assets must be routed to `LOCAL-LARGE-FILES/knowledge-sources/`, not committed into Brain Git

### 03:00
- transcript manifest + brief
- conversation-derived notes only when justified
- degraded mode explicitly reported when QMD or article context is unavailable

### 04:00
- amplifier report
- compact cross-source updates only when justified
- research seeds/context-pack drafts are optional
- heavy deep research is not default nightly behavior

## Rerun Rules

- Re-run 02:00 only when article ingestion/integration failed or new article metadata was fixed
- Re-run 03:00 only when transcript/QMD/project routing failed or upstream context materially changed
- Re-run 04:00 only when upstream stage outputs changed or merge logic failed
- Do not rerun the whole chain by default; rerun the smallest broken stage

## Alert Conditions

Alert human when:
- Brain repo conflicts block progress
- a stage repeatedly fails on the same source
- visibility cannot be confirmed after commit
- a stage would require changing scope (e.g. deep research escalation)
- a stage is about to commit large raw article assets, image packs, PDFs, or other source attachments into Brain Git

## No-Op Is Valid

A valid nightly result may be:
- no new article notes
- no worthwhile transcript insight
- no cross-source signal worth amplification

No-op is better than forced garbage writes.
