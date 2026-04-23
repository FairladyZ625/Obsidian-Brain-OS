# Friction-to-Governance Loop Prompt

Use this prompt when you want an agent to turn repeated friction into governance actions.

## Goal

Do not just summarize mistakes.

Your job is to:
1. identify repeated friction
2. diagnose the broken layer
3. propose governance write-backs
4. avoid over-systematizing one-off noise

## Inputs

You may receive:
- repeated user corrections
- failed outputs
- recurring planning mistakes
- repeated workflow misses
- review or observer findings

## Output structure

### 1. Friction signals
List the repeated signals only.

### 2. Root cause diagnosis
For each signal, classify the likely root cause:
- prompt
- AGENTS
- reference
- workflow / scan logic
- docs / onboarding
- naming / structure

### 3. Governance write-back
For each recurring signal, propose the smallest effective write-back:
- edit a prompt
- edit AGENTS
- add or improve a reference
- adjust workflow logic
- update docs / onboarding

### 4. Do not overreact
Explicitly mark which issues are:
- structural and worth systematizing
- one-off and should stay local

## Important rule

A repeated friction signal should not stay as repeated friction.
But not every mistake deserves a new rule.

Your job is to separate recurring governance problems from normal execution noise.
