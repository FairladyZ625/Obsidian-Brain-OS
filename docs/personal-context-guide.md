# Personal Context Guide (06 & 07)

> How Brain OS handles your private documents and work context layers.
> **Chinese version**: [docs/zh/personal-context-guide.md](docs/zh/personal-context-guide.md)

---

## Three-Layer Context Architecture

Brain OS organizes personal information into three distinct layers:

```
┌─────────────────────────────────────┐
│  Layer 3: Knowledge (03-KNOWLEDGE)  │ ← AI reads, processes, writes
│  Articles, patterns, research       │
├─────────────────────────────────────┤
│  Layer 2: Work Context (07)         │ ← AI reads, references
│  Clients, decisions, experience     │
├─────────────────────────────────────┤
│  Layer 1: Private Docs (06)         │ ← AI does NOT touch (by default)
│  Finance, health, relationships     │
└─────────────────────────────────────┘
```

---

## 06-PERSONAL-DOCS (Private Layer)

**Principle: AI-opt-out by default.**

This directory contains sensitive personal information:
- `01-FINANCE/` — Financial records
- `02-HEALTH/` — Health data
- `03-RELATIONSHIPS/` — Relationship notes
- `04-LIFE-GOALS/` — Life goals
- `05-LEARNING/` — Learning plans

**AI access rules**:
- ❌ Not processed by Nightly Pipeline
- ❌ Not included in knowledge synthesis
- ✅ Only read if **you explicitly ask**
- 📝 Listed in `.gitignore` by default (not committed to public repos)

**When to use**: Store anything you don't want AI to routinely access but want in your vault for personal reference.

---

## 07-WORK-CONTEXT (Work Layer)

**Principle: AI-read-only reference.**

This directory captures professional context that helps AI give better advice:
- `01-CLIENTS/` — Client profiles
- `02-DECISIONS/` — Decision records with rationale
- `03-SUCCESS-PATTERNS/` — What worked before
- `04-FAILURE-LESSONS/` — What didn't work
- `05-STAKEHOLDERS/` — Key people

**AI access rules**:
- ✅ AI can read for context
- ✅ Referenced by Nightly Pipeline for project routing
- ❌ AI should not modify without explicit request
- ⚠️ May contain sensitive business info — consider `.gitignore`

**When to use**: Accumulate work experience so AI can give contextualized advice based on your actual history.

---

## Interaction Rules

| Scenario | 06 (Private) | 07 (Work Context) |
|----------|-------------|-------------------|
| User asks "how's my health?" | Only if user points to file | N/A |
| User asks "what did we learn from X client?" | N/A | AI reads 07-WORK-CONTEXT |
| Nightly Pipeline runs | ❌ Skipped | ✅ Referenced for context |
| Git commit | User decides | User decides |
| Public repo | ❌ Never commit | ⚠️ Check sensitivity |

---

## Practical Tips

1. **Start lean**: You don't need to populate 06/07 immediately. Begin with 00-05.
2. **07 is high-leverage**: The more work context you accumulate, the better AI's advice becomes.
3. **06 is your safe space**: Nothing in 06 gets touched unless you say so.
4. **Both are optional**: Brain OS works fine with just 00-05 (INBOX through PROJECTS).

---

## Related

- [Architecture](architecture.md)
- [Personal Ops System](personal-ops.md)
- [Project Management](project-management.md)
