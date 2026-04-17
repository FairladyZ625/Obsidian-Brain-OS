#!/usr/bin/env bash
set -euo pipefail

STRICT=false
[[ "${1:-}" == "--strict" ]] && STRICT=true

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
HITS=0

patterns=(
  'ZeYu-AI-Brain'
  '/Users/lizeyu'
  '李主席'
  '小宁'
  '泽宇'
  'Review-Search-Brain-Manager'
  '1475328660373372940'
  '530383608410800138'
)

exclude_regex='README|LICENSE|CHANGELOG\.md|CHANGELOG_CN\.md|docs/references/pii-deidentification-guide\.md|tools/conversation-mining|README_EN\.md|README\.md|setup\.sh|docs/getting-started\.md|docs/openclaw-setup\.md|docs/obsidian-setup\.md'

echo "🔎 Brain config leak scan — $ROOT"
echo

for pattern in "${patterns[@]}"; do
  echo "── $pattern ──"
  result=$(grep -RIn --exclude-dir=.git --include='*.md' --include='*.sh' --include='*.py' --include='*.yml' --include='*.yaml' --include='*.toml' -- "$pattern" "$ROOT" 2>/dev/null | grep -vE "$exclude_regex|scripts/check-brain-config-leaks\.sh" || true)
  if [[ -n "$result" ]]; then
    echo "$result"
    HITS=$((HITS + $(echo "$result" | wc -l)))
  else
    echo "  ✅ none"
  fi
  echo
 done

echo "══════════════════════════════"
if [[ "$HITS" -eq 0 ]]; then
  echo "✅ Brain config leak scan passed — 0 hits"
  exit 0
else
  echo "⚠️  Brain config leak scan found $HITS hit(s). Review before merging."
  if [[ "$STRICT" == true ]]; then
    exit 1
  fi
fi
