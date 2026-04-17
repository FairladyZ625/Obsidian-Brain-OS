#!/usr/bin/env bash
# Check for potential duplicate knowledge notes in {{BRAIN_NAME}} before writing.
#
# Usage:
#   check-duplicates.sh "<keyword or title>"
#   check-duplicates.sh "<keyword>" --dir 03-KNOWLEDGE/01-READING/01-DOMAINS/AI-Agent
#
# Exit codes:
#   0  no duplicates found
#   1  potential duplicates found (review before writing)
#   2  usage error

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
source "$SCRIPT_DIR/config.sh"

if [[ $# -lt 1 ]]; then
  echo "Usage: $0 \"<keyword>\" [--dir <relative-path>]" >&2
  exit 2
fi

KEYWORD="$1"
SEARCH_DIR="${BRAIN_ROOT}/03-KNOWLEDGE"

# Optional --dir override
if [[ $# -ge 3 && "$2" == "--dir" ]]; then
  SEARCH_DIR="${BRAIN_ROOT}/$3"
fi

if [[ ! -d "$SEARCH_DIR" ]]; then
  echo "[WARN] Search directory not found: $SEARCH_DIR" >&2
  exit 0
fi

echo "Searching for: \"$KEYWORD\""
echo "In: $SEARCH_DIR"
echo ""

# Search in frontmatter title, summary, key_points, and body
MATCHES=$(grep -ril "$KEYWORD" "$SEARCH_DIR" --include="*.md" 2>/dev/null || true)

if [[ -z "$MATCHES" ]]; then
  echo "No duplicates found. Safe to write."
  exit 0
fi

echo "Potential duplicates found:"
echo ""

while IFS= read -r file; do
  # Extract title from frontmatter if present
  TITLE=$(grep -m1 "^title:" "$file" 2>/dev/null | sed 's/^title: *//' || echo "")
  CREATED=$(grep -m1 "^created_at:" "$file" 2>/dev/null | sed 's/^created_at: *//' || echo "")
  REL_PATH="${file#$BRAIN_ROOT/}"
  if [[ -n "$TITLE" ]]; then
    echo "  [$CREATED] $TITLE"
    echo "  → $REL_PATH"
  else
    echo "  → $REL_PATH"
  fi
  echo ""
done <<< "$MATCHES"

COUNT=$(echo "$MATCHES" | wc -l | tr -d ' ')
echo "Found $COUNT potential duplicate(s). Review before writing."
exit 1
