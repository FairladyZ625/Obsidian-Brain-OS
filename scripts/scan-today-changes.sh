#!/bin/bash
# scan-today-changes.sh
# 扫描当天所有 git 仓库的变更，输出与 Brain OS 相关的文件列表
# 用法: ./scan-today-changes.sh [--date YYYY-MM-DD]
# 输出: JSON 格式的变更文件列表（供 agent 消费）
# 兼容 macOS bash 3.2（无关联数组）

set -euo pipefail

DATE_ARG="${1:-today}"
if [ "$DATE_ARG" = "today" ]; then
  SINCE="today 00:00"
elif [[ "$DATE_ARG" =~ ^[0-9]{4}-[0-9]{2}-[0-9]{2}$ ]]; then
  SINCE="$DATE_ARG 00:00"
else
  echo "❌ 日期格式错误，用法: YYYY-MM-DD 或 today"
  exit 1
fi

OPEN_SOURCE_REPO="$HOME/Projects/Obsidian-Brain-OS"

# 与 Brain OS 相关的路径前缀
RELEVANT_PREFIXES="skills/|prompts/|scripts/|vault-template/|cron-examples/|docs/|tools/|setup.sh|README|LICENSE|.github/"

is_relevant() {
  echo "$1" | grep -qE "^(${RELEVANT_PREFIXES})" 2>/dev/null
}

scan_repo() {
  local repo_name="$1"
  local repo_path="$2"
  
  [ ! -d "$repo_path/.git" ] && return
  
  # 获取当天变更文件
  local changed_files
  changed_files=$(cd "$repo_path" && git log --since="$SINCE" --name-only --pretty=format: -- . 2>/dev/null | sort -u | grep -v '^$' || true)
  
  [ -z "$changed_files" ] && return
  
  local first_file=true
  echo -n '    "'"$repo_name"'": {"path": "'"$repo_path"'", "files": ['
  
  while IFS= read -r file; do
    local relevant="false"
    is_relevant "$file" && relevant="true"
    
    [ "$first_file" = true ] && first_file=false || echo ","
    printf '{"path":"%s","relevant":%s}' "$file" "$relevant"
  done <<< "$changed_files"
  
  echo "]} "
}

echo "{"
echo '"scanDate":"'"$SINCE"'",'
echo '"repos":{'

# 扫描各仓库
workspace_part=$(scan_repo "workspace" "$HOME/.openclaw/workspace")
brain_root="${BRAIN_ROOT:-$HOME/Documents/${BRAIN_NAME:-My-Brain}}"
brain_part=$(scan_repo "brain" "$brain_root")
skills_part=$(scan_repo "skills" "$HOME/.agents/skills")

# 输出（处理逗号分隔）
[ -n "$workspace_part" ] && echo -n "$workspace_part"
if [ -n "$brain_part" ]; then
  [ -n "$workspace_part" ] && echo ","
  echo -n "$brain_part"
fi
if [ -n "$skills_part" ]; then
  [ -n "$workspace_part" -o -n "$brain_part" ] && echo ","
  echo -n "$skills_part"
fi

echo ""
echo "},"

# 开源仓库状态
echo '"openSourceRepo":{'
echo -n '"path":"'"$OPEN_SOURCE_REPO"'",'
if [ -d "$OPEN_SOURCE_REPO/.git" ]; then
  os_branch=$(cd "$OPEN_SOURCE_REPO" && git branch --show-current 2>/dev/null || echo "unknown")
  os_last_commit=$(cd "$OPEN_SOURCE_REPO" && git log -1 --format="%h %s (%ci)" 2>/dev/null || echo "none")
  os_dirty=$(cd "$OPEN_SOURCE_REPO" && git status --porcelain 2>/dev/null | wc -l | tr -d ' ')
  echo '"branch":"'"$os_branch"'","lastCommit":"'"$os_last_commit"'","dirtyFiles":'$os_dirty
else
  echo '"exists":false'
fi
echo "}}"
