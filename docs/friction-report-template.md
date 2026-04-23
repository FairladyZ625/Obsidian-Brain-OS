# Friction Report Template

Use this template when you want to produce a structured friction report.

## Header

```yaml
report_id: auto-generated
period: YYYY-MM-DD to YYYY-MM-DD
agent: {{MAIN_AGENT_NAME}}
status: draft | final
```

## 1. Friction Signals

For each signal, record:

| ID | Timestamp | Source | Summary | Bucket | Recurring? |
|----|-----------|--------|---------|--------|------------|
| F-001 | ... | user correction | plan written to workspace instead of brain | reference miss | yes (3rd time) |

### Rules
- Only include signals that have appeared **at least twice**, or are clearly structural
- One-off mistakes go in a separate "noise" section at the bottom

## 2. Buckets

Group signals into recurring buckets:

### Bucket: Reference Miss
- Signals: F-001, F-005, ...
- Pattern: rule exists but not consulted early enough
- Count: N

### Bucket: Prompt Ambiguity
- Signals: ...
- Pattern: execution instructions allow multiple interpretations
- Count: N

(Continue for each bucket)

## 3. Findings

For each bucket with 2+ signals:
- What is the real root cause?
- Which system layer is broken?
- Is this structural or one-off?

## 4. Recommended Write-backs

For each structural finding:

| Finding | Layer | Proposed Action | Priority |
|---------|-------|----------------|----------|
| Plans go to wrong place | AGENTS + Reference | Strengthen pre-action check | High |

### Write-back layer options
- **Prompt**: rewrite execution instructions
- **AGENTS**: add or strengthen visible guidance
- **Reference**: add or improve a reusable rule
- **Workflow**: adjust scan logic or automation
- **Docs/Onboarding**: update install or usage guides
- **No change**: log locally, do not systematize

## 5. Noise (Not Systematized)

List one-off issues here with a brief reason why they should stay local:

| Issue | Reason to Skip |
|-------|---------------|
| Single typo in output | One-off, no pattern |

## 6. Next Review Date

Schedule the next friction review: YYYY-MM-DD
