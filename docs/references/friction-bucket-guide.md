# Friction Bucket Guide

When classifying friction signals, use these standard buckets.

## Standard Buckets

### 1. Prompt Ambiguity
The execution instructions allow multiple interpretations.
- Example: "write the plan" without specifying where
- Typical write-back: **Prompt**

### 2. Reference Miss
A reusable rule exists but is skipped or forgotten.
- Example: knowledge-plan-governance exists but was not read before writing
- Typical write-back: **AGENTS** or **Reference**

### 3. AGENTS Visibility Gap
The rule should be visible before action, but it is buried or missing from AGENTS.
- Example: "check references first" is only in a deep doc, not in AGENTS
- Typical write-back: **AGENTS**

### 4. Workflow Blind Spot
Automation or scan logic keeps missing the real issue.
- Example: daily sync scans files but misses system-level upgrades
- Typical write-back: **Workflow** (cron prompt / scan script)

### 5. Naming / Structure Confusion
Names or directory structures mislead the agent about where things belong.
- Example: workspace looks like a valid place for formal plans
- Typical write-back: **Reference** or **Docs/Onboarding**

### 6. Boundary / Privacy Issue
Private content leaks into public-facing outputs, or vice versa.
- Example: internal agent names appear in OSS docs
- Typical write-back: **Reference** or **Workflow** (PII scanner / config leak scanner)

### 7. Onboarding Gap
New capability exists but install/onboarding docs never mention it.
- Example: governance cron stack added but INSTALL_FOR_AGENTS unchanged
- Typical write-back: **Docs/Onboarding**

### 8. Structural Drift
System has evolved but old docs/prompts/config were not updated.
- Example: component-guide still says v0.5 while latest is v1.1.0
- Typical write-back: **Docs** (multiple files)

## How to use

When processing friction signals:
1. Read each signal
2. Assign it to one of these buckets (or create a new one if none fits)
3. Count per bucket
4. Buckets with 2+ signals become candidates for governance write-back
5. Buckets with 1 signal stay as "watch"

## When to create a new bucket

If an issue does not fit any existing bucket after 10+ signals, consider whether a new bucket should be added.

Do not create new buckets for one-off issues.
