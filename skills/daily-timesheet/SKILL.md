# daily-timesheet

**Purpose:** Scan today's git commits and project context, align work to milestones/OKRs, generate a structured timesheet draft for human review, then write to your timesheet backend.

## When to use

Triggered by a daily cron job (typically 17:30). Can also be invoked manually.

## What it does

1. **Observe** — scan git commits across configured repos for today
2. **Read context** — load Project Briefings and active milestones
3. **Filter** — keep only work-related items (exclude personal knowledge base, side projects, etc.)
4. **Align** — map each item to a milestone + KR (key result)
5. **Draft** — generate a structured timesheet entry
6. **Confirm** — present draft to user for review
7. **Write** — after confirmation, write to timesheet backend

## Configuration

Set these in your environment or `config.env`:

```bash
# Required: space-separated list of git repo paths to scan
TIMESHEET_REPOS="/path/to/repo1 /path/to/repo2"

# Required: path to your milestones file (see format below)
TIMESHEET_MILESTONES="{{BRAIN_ROOT}}/05-PROJECTS/milestones.md"

# Optional: output backend (file | dingtalk | feishu | stdout)
# Default: file
TIMESHEET_BACKEND="file"

# Required if TIMESHEET_BACKEND=file
TIMESHEET_OUTPUT_DIR="{{BRAIN_ROOT}}/01-PERSONAL-OPS/06-TIMESHEETS"

# Required if TIMESHEET_BACKEND=feishu
FEISHU_APP_ID="..."
FEISHU_APP_SECRET="..."
FEISHU_BITABLE_APP_TOKEN="..."
FEISHU_BITABLE_TABLE_ID="..."

# Required if TIMESHEET_BACKEND=dingtalk
DINGTALK_BASE_ID="..."
DINGTALK_TABLE_ID="..."
```

## Milestones file format

Your milestones file should follow this structure:

```markdown
## M1 — Project Name (due: YYYY-MM-DD)
**O:** What you're trying to achieve
- KR1: Specific measurable outcome
- KR2: Specific measurable outcome

## M2 — Another Project (due: YYYY-MM-DD)
**O:** What you're trying to achieve
- KR1: Specific measurable outcome
```

## Execution steps

### Step 0: Get today's date

```bash
TZ="Asia/Shanghai" date "+%Y-%m-%d %A %H:%M"
```

Use this as the canonical date for all subsequent steps.

### Step 1: Scan git commits (parallel)

For each repo in `TIMESHEET_REPOS`:

```bash
git -C "$REPO" log --oneline --author="$(git config user.name)" \
  --since="$TODAY 00:00" --until="$TODAY 23:59" 2>/dev/null
```

Collect all commits with their repo context.

### Step 2: Load project context

Read the milestones file at `TIMESHEET_MILESTONES`. Extract:
- Active milestones (not yet past due)
- Each milestone's O + KR list

Also read any Project Briefings referenced in the milestones file if available.

### Step 3: Filter — work-related only

Keep items that relate to:
- Client deliverables, product features, bug fixes
- Team coordination, code reviews, architecture decisions
- Documentation for external/client use

Exclude:
- Personal knowledge base maintenance
- Personal learning / reading
- Open source side projects unrelated to work
- Personal automation scripts

### Step 4: Align to milestones

For each commit/work item:
1. Match to the most relevant milestone
2. Match to the most relevant KR within that milestone
3. Write a KR-style description: `[M#] KR#: <what was done, ~progress>`

If a commit doesn't map to any milestone, flag it as `[Untracked]`.

### Step 5: Generate draft

Output format:

```
📋 Timesheet Draft — {DATE}

[M1] Project Name (due: DATE)
  KR1 <label>: <what was done> — ~X% / done
  KR2 <label>: <what was done>

[M2] Another Project
  KR1 <label>: <what was done>

[Untracked]
  - <commit message> (repo: <name>)

📊 Estimated: X days | Status: in-progress / completed
⚠️  Blockers: none / <brief note>

🧭 Backlog suggestions (if any):
  - Possibly move to done: <item> (evidence: commit <hash>)
```

### Step 6: Present for confirmation

Send the draft to the user. Wait for confirmation or edits before writing.

### Step 7: Write to backend

**Backend: `file`** (default)

Write a markdown file to `TIMESHEET_OUTPUT_DIR/timesheet-{DATE}.md`.

**Backend: `feishu`**

Use the Feishu Bitable API to create a record. See `references/feishu-bitable.md` for field mapping.

**Backend: `dingtalk`**

Use the DingTalk AI Table API. See `references/dingtalk-bitable.md` for field mapping.

## Output (announce to channel)

After writing, send a 1-2 line summary:

```
✅ Timesheet {DATE} | M1/M3 | 1d | written to {backend}
```

## Notes

- Never auto-write without user confirmation
- If no commits found, still generate a draft based on briefing/backlog
- Backlog suggestions are advisory only — never auto-update backlog
