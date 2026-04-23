# System Governance Guide

This guide explains how Brain OS should write recurring problems back into the system.

## Core principle

When the same class of mistake happens repeatedly, the fix should not remain conversational.

It should be written back into one of the system layers.

## Common write-back targets

### 1. Prompt layer
Use when execution instructions are missing or misleading.

### 2. Reference layer
Use when the rule exists but is easy to skip, forget, or misapply.

### 3. AGENTS layer
Use when the rule must be visible before action, not discovered later.

### 4. Workflow layer
Use when automation or scan logic keeps missing the real issue.

### 5. Docs / onboarding layer
Use when new users or agents cannot understand how to use a capability correctly.

## Decision rule

Before writing back, ask:
- is this recurring?
- is it structural?
- will the same mistake likely happen again?

If not, keep it local.

If yes, write it back.
