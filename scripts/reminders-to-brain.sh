#!/usr/bin/env bash
# reminders-to-brain.sh
# 从 Apple 提醒事项读取完成状态，反向 double-check Brain 待办
# 输出：过期未完成事项列表 + 已完成事项列表（供 evening review 使用）
# 用法: bash reminders-to-brain.sh [YYYY-MM-DD]
set -euo pipefail

BRAIN_ROOT="${BRAIN_ROOT:-{{BRAIN_ROOT}}}"
LIST_NAME="${REMINDERS_LIST:-Brain今日}"
DATE="${1:-$(TZ='Asia/Shanghai' date '+%Y-%m-%d')}"
REPORT_DIR="$BRAIN_ROOT/01-PERSONAL-OPS/05-OPS-LOGS"
REPORT_FILE="$REPORT_DIR/reminders-sync-$DATE.md"

echo "[$(date '+%F %T')] reminders-to-brain start for $DATE"

mkdir -p "$REPORT_DIR"

# Get all reminders from Brain今日 list as JSON
REMINDERS_JSON=$(remindctl list "$LIST_NAME" --json 2>/dev/null || echo "[]")

# Parse and categorize
python3 - "$REMINDERS_JSON" "$DATE" "$REPORT_FILE" << 'PYEOF'
import sys, json, re
from datetime import datetime, timezone

reminders_json = sys.argv[1]
date_str = sys.argv[2]
report_path = sys.argv[3]

try:
    reminders = json.loads(reminders_json)
except:
    reminders = []

completed = []
overdue = []
today_pending = []

now = datetime.now(timezone.utc)

for r in reminders:
    title = r.get('title', '')
    is_done = r.get('isCompleted', False)
    due_str = r.get('dueDate', '')

    # Only process items tagged with today's date
    if date_str not in title and due_str and date_str not in due_str[:10]:
        continue

    clean_title = re.sub(r'^\[[\d\-]+\]\s*', '', title).strip()

    if is_done:
        completed.append(clean_title)
    else:
        # Check if overdue
        if due_str:
            try:
                due_dt = datetime.fromisoformat(due_str.replace('Z', '+00:00'))
                if due_dt < now:
                    overdue.append(clean_title)
                else:
                    today_pending.append(clean_title)
            except:
                today_pending.append(clean_title)
        else:
            today_pending.append(clean_title)

# Write report
with open(report_path, 'w', encoding='utf-8') as f:
    f.write(f"---\ntype: reminders-sync\ndate: {date_str}\ngenerated: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n---\n\n")
    f.write(f"# Apple 提醒事项同步报告 — {date_str}\n\n")

    f.write(f"## ✅ 已完成（{len(completed)} 项）\n\n")
    for item in completed:
        f.write(f"- [x] {item}\n")
    if not completed:
        f.write("- （无）\n")

    f.write(f"\n## ⏰ 今日待完成（{len(today_pending)} 项）\n\n")
    for item in today_pending:
        f.write(f"- [ ] {item}\n")
    if not today_pending:
        f.write("- （无）\n")

    f.write(f"\n## ⚠️ 已过期未完成（{len(overdue)} 项）\n\n")
    for item in overdue:
        f.write(f"- [ ] {item}  ← **需追问**\n")
    if not overdue:
        f.write("- （无）\n")

    f.write(f"\n---\n*由 reminders-to-brain.sh 自动生成*\n")

print(f"completed={len(completed)}")
print(f"pending={len(today_pending)}")
print(f"overdue={len(overdue)}")
print(f"report={report_path}")

# Output overdue items for cron to pick up and ask user
if overdue:
    print("OVERDUE_ITEMS:")
    for item in overdue:
        print(f"  - {item}")
PYEOF

echo "[$(date '+%F %T')] done — report written to $REPORT_FILE"
