# Friction-to-Governance Loop

Brain OS should not only help create knowledge and run workflows. Over time, it should also help reduce repeated mistakes.

This document describes a reusable pattern for turning recurring friction signals into governance improvements.

---

## What this loop is

The friction-to-governance loop is a simple idea:

1. collect friction signals
2. group them into recurring problem types
3. identify the real cause
4. write the fix back into the system

The goal is not reflection for its own sake.

The goal is to help Brain OS become more stable over time.

---

## What counts as friction

A friction signal is a repeated or structural problem such as:
- the agent keeps writing files to the wrong place
- the same rule is forgotten again and again
- a cron or workflow keeps missing the real upgrade surface
- prompts are technically correct but operationally misleading
- users must repeatedly correct the same behavior

One-off mistakes are not enough.

This loop is for patterns that keep coming back.

---

## The four stages

### 1. Capture
Collect concrete evidence of repeated friction:
- user corrections
- failed or misleading outputs
- recurring workflow misses
- repeated planning or governance mistakes

### 2. Diagnose
Ask what layer is actually broken:
- prompt problem
- AGENTS / team rule problem
- reference problem
- scan / automation logic problem
- naming or structure problem

### 3. Govern
Choose the right governance action:
- rewrite a prompt
- strengthen AGENTS guidance
- add or improve a reference
- adjust a scan rule
- change the default rollout path

### 4. Write back
The fix is not complete until it is written back into the system.

Examples:
- update `AGENTS.md`
- update a reference file
- update onboarding docs
- update a cron prompt
- update release guidance

---

## What this is not

This is not:
- private journaling
- abstract self-reflection
- a place to dump all mistakes
- a requirement to systematize every small issue

The loop should be selective.

Use it for recurring friction, not normal noise.

---

## Why it matters

Without a governance loop, Brain OS can gain features while repeating the same mistakes.

With a governance loop, repeated friction becomes a source of system improvement.

That makes the system more teachable, more stable, and easier for other people to adopt.

---

## Typical write-back targets

A friction signal should usually write back into one of these layers:

- **Prompt layer**: when execution instructions are unclear
- **Reference layer**: when a reusable rule exists but is easy to skip or forget
- **AGENTS layer**: when the rule must be visible before action
- **Workflow layer**: when automation or scan logic is missing the real issue
- **Docs / onboarding layer**: when outside users or agents cannot understand how to use a new capability correctly

---

## Example pattern

A recurring problem appears:
- formal plans keep getting written to workspace instead of the knowledge base

Diagnosis:
- the plan rule exists, but the reference is not being consulted early enough

Governance action:
- strengthen `AGENTS.md`
- strengthen the relevant reference
- strengthen the affected cron or sync prompt

Write-back result:
- future runs are more likely to route formal plans correctly

---

## Recommended adoption order

For OSS users, adopt this loop in stages:

1. first make one workflow succeed
2. then identify repeated friction
3. then define a small governance loop
4. only later add templates, reports, or automation

Do not start with a heavy internal governance stack.

Start with the pattern.

---

## Relationship to other Brain OS parts

- **Knowledge governance** keeps the knowledge base healthy
- **Friction-to-governance** keeps the operating system healthy
- **Observer** or similar review agents may provide inputs
- **References** and **AGENTS** are common write-back targets

These layers reinforce each other.

---

## Final principle

> Repeated friction should not stay as repeated friction.
> It should become governance.
