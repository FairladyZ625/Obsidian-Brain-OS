#!/usr/bin/env bash
# brain-to-reminders.sh
# 从 daily-briefing.md 提取今日事项，同步到 Apple 提醒事项「Brain今日」列表
# 用法: bash brain-to-reminders.sh [YYYY-MM-DD]
set -euo pipefail

BRAIN_ROOT="${BRAIN_ROOT:-{{BRAIN_ROOT}}}"
BRIEFING="$BRAIN_ROOT/01-PERSONAL-OPS/01-DAILY-BRIEFS/daily-briefing.md"
LIST_NAME="${REMINDERS_LIST:-Brain今日}"
DATE="${1:-$(TZ='Asia/Shanghai' date '+%Y-%m-%d')}"

echo "[$(date '+%F %T')] brain-to-reminders start for $DATE"

# 确保列表存在
remindctl list "$LIST_NAME" --create 2>/dev/null || true

# 读取 briefing 中"今天最重要的 3 件事"和"今天必须推进"两个章节
# 提取 - 开头的事项行（去掉 markdown 格式）
ITEMS=$(python3 - "$BRIEFING" "$DATE" << 'PYEOF'
import sys, re
briefing_path = sys.argv[1]
date_str = sys.argv[2]

try:
    with open(briefing_path, encoding='utf-8') as f:
        content = f.read()
except FileNotFoundError:
    print(f"ERROR: briefing not found: {briefing_path}", file=sys.stderr)
    sys.exit(1)

# Extract sections 一~五 (主线 + 支线)
sections = re.split(r'\n## ', content)
items = []
for sec in sections:
    if sec.startswith(('一、', '二、', '三、', '四、', '五、')):
        lines = sec.split('\n')
        for line in lines:
            line = line.strip()
            # Match numbered items like "1. **Title**" or "- Title"
            m = re.match(r'^[\d\-\*]+[\.\)]\s*\*{0,2}(.+?)\*{0,2}\s*(?:—.*)?$', line)
            if m:
                title = m.group(1).strip()
                # Remove markdown bold/italic
                title = re.sub(r'\*+', '', title).strip()
                if title and len(title) > 3:
                    items.append(title)

for item in items[:15]:  # max 15 items
    print(item)
PYEOF
)

if [ -z "$ITEMS" ]; then
    echo "[WARN] No items extracted from briefing"
    exit 0
fi

# Get existing reminders in list to avoid duplicates
EXISTING=$(remindctl list "$LIST_NAME" --plain 2>/dev/null | awk -F'\t' '{print $2}' || true)

COUNT=0
while IFS= read -r item; do
    [ -z "$item" ] && continue
    # Check if already exists (simple substring match)
    if echo "$EXISTING" | grep -qF "$item" 2>/dev/null; then
        echo "[skip] already exists: $item"
        continue
    fi
    remindctl add --title "[$DATE] $item" --list "$LIST_NAME" --due "$DATE 21:00"
    echo "[add] $item"
    COUNT=$((COUNT + 1))
done <<< "$ITEMS"

echo "[$(date '+%F %T')] done — added $COUNT reminders to '$LIST_NAME'"
