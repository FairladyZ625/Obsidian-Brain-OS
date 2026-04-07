# Knowledge Flywheel Amplifier — Nightly Master Prompt

> Runtime location: `{{WORKSPACE_PATH}}/knowledge-flywheel-amplifier.prompt.md`
> This is a template — copy to your workspace and customize.

Read and follow the `knowledge-flywheel-amplifier` skill (`{{SKILLS_PATH}}/knowledge-flywheel-amplifier/SKILL.md`).

Target date: yesterday ({{TIMEZONE}}) unless explicitly provided.

## Role

This is the **04:00 stage** in the nightly knowledge pipeline — cross-source synthesis.

You merge Stage A (article integration) and Stage B (conversation mining) outputs into:
- Cross-source topic updates
- Candidate patterns
- Open questions & research seeds
- Context-pack candidates

## Inputs

- **Stage A (02:00)**: article integration reports, high-value candidates, updated indexes
- **Stage B (03:00)**: transcript mining brief, conversation-derived notes, research seed candidates
- **Brain read-only**: `03-KNOWLEDGE/99-SYSTEM/01-INDEXES/`, domain notes, `05-PROJECTS/`, open questions

## Required Outputs

1. **Machine report** → `03-KNOWLEDGE/99-SYSTEM/03-INTEGRATION-REPORTS/run-reports/YYYY-MM-DD/amplifier-report-YYYY-MM-DD.md`
2. **Digest update** → `03-KNOWLEDGE/01-READING/04-DIGESTS/nightly-digest-YYYY-MM-DD.md` under `## 04:00 Knowledge Amplification`
3. Merged topic / open-question / pattern-candidate updates (when justified)
4. 0-2 research seeds
5. 0+ context-pack drafts (when justified)
6. Brain commit + visibility report if Brain changed

## Rules

- This is a lightweight merge layer — do NOT redo article integration or transcript mining
- Only produce output when there is real cross-source signal
- Even no-op runs must write machine report + digest section (mark as "no significant signal")
- Do not force patterns or insights that don't exist in source material

## Guardrails

- Do not invent cross-source connections that aren't supported by inputs
- Research seeds must be grounded in actual source material
- Run reports belong in `99-SYSTEM/03-INTEGRATION-REPORTS/`, never in reading layers
