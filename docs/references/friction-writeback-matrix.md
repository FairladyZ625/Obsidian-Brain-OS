# Friction Write-back Matrix

Use this matrix to decide where a recurring problem should be written back.

## Decision Flow

```
Is this recurring (2+ times)?
├─ No → Log locally, done
└─ Yes → Which layer is broken?
    ├─ Execution instructions unclear → Rewrite PROMPT
    ├─ Rule exists but forgotten → Strengthen REFERENCE
    ├─ Rule must be visible before action → Update AGENTS
    ├─ Automation misses the issue → Fix WORKFLOW
    ├─ New capability undocumented → Update DOCS/ONBOARDING
    └─ Private content leaking → Fix BOUNDARY rules
```

## Matrix Table

| If the problem is... | Write back to... | Example action |
|---------------------|------------------|---------------|
| Prompt allows wrong interpretation | **Prompt** | Add explicit path rule |
| Rule exists but skipped | **Reference** | Strengthen reference + add AGENTS hook |
| Rule should be seen before acting | **AGENTS** | Add to mandatory checklist |
| Scan/cron misses real upgrade surface | **Workflow** | Upgrade scan logic or prompt |
| New feature invisible to users | **Docs/Onboarding** | Update install guide + profiles |
| Naming/directory confuses agent | **Reference** | Clarify naming convention |
| Private data in public output | **Boundary** | Add PII/config leak check |
| Old docs out of date | **Docs** | Batch update version numbers |
| One-off human error | **None** | Daily memory only |

## Key Principle

> Not every mistake deserves a new rule.
> But every recurring structural mistake deserves a write-back.

## Anti-patterns

- Writing back everything (noise)
- Writing back nothing (stagnation)
- Only fixing prompts when the real issue is workflow
- Adding new docs when the real fix is strengthening an existing one
