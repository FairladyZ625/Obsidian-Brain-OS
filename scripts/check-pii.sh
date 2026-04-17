#!/usr/bin/env bash
# check-pii.sh
# Scan committed files for PII: absolute paths with real usernames, and Discord-style IDs.
# Template tokens ({{PLACEHOLDER}}) in .md/.prompt.md files are intentional and excluded.
# Usage: bash scripts/check-pii.sh [--strict]
#   --strict: exit 1 if any hits found (used by CI)
set -euo pipefail

STRICT=false
[[ "${1:-}" == "--strict" ]] && STRICT=true

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
HITS=0

echo "🔍 PII scan — $ROOT"
echo ""

# 1. Absolute paths with likely real usernames
# Ignore generic examples like /tmp/... and /home/user/...
echo "── Absolute paths ──"
RESULT=$(grep -rn \
  --include="*.md" --include="*.sh" --include="*.py" --include="*.yml" --include="*.yaml" \
  -E '/Users/[a-zA-Z][a-zA-Z0-9_-]+/|/home/[a-zA-Z][a-zA-Z0-9_-]+/' \
  "$ROOT" \
  --exclude-dir=".git" \
  2>/dev/null | grep -vE '/tmp/|/home/user/|docs/references/pii-deidentification-guide\.md' || true)

if [ -n "$RESULT" ]; then
  echo "$RESULT"
  HITS=$((HITS + $(echo "$RESULT" | wc -l)))
else
  echo "  ✅ none"
fi
echo ""

# 2. Unresolved template tokens — only in runtime scripts that should be resolved before execution
# setup.sh and template/example scripts intentionally contain {{PLACEHOLDER}} and are excluded.
echo "── Unresolved template tokens (runtime scripts only) ──"
RESULT=$(grep -rn \
  --include="*.sh" --include="*.py" \
  -E '\{\{[A-Z_]+\}\}' \
  "$ROOT" \
  --exclude-dir=".git" \
  2>/dev/null | grep -vE '(^|/)(setup\.sh|scripts/check-pii\.sh|tools/conversation-mining/export_all\.py|skills/.*/scripts/.*|prompts/|cron-examples/|docs/references/pii-)' || true)

if [ -n "$RESULT" ]; then
  echo "$RESULT"
  HITS=$((HITS + $(echo "$RESULT" | wc -l)))
else
  echo "  ✅ none"
fi
echo ""

# 3. Discord IDs (18-digit snowflakes) — only in scripts and Python files
# Docs may reference example IDs; scripts should use env vars instead
echo "── Potential Discord IDs in scripts/py (18-digit) ──"
RESULT=$(grep -rn \
  --include="*.sh" --include="*.py" \
  -E '\b[0-9]{17,19}\b' \
  "$ROOT" \
  --exclude-dir=".git" \
  2>/dev/null | grep -vE 'scripts/check-brain-config-leaks\.sh' || true)

if [ -n "$RESULT" ]; then
  echo "$RESULT"
  HITS=$((HITS + $(echo "$RESULT" | wc -l)))
else
  echo "  ✅ none"
fi
echo ""

# Summary
echo "══════════════════════════════"
if [ "$HITS" -eq 0 ]; then
  echo "✅ PII scan passed — 0 hits"
  exit 0
else
  echo "⚠️  PII scan found $HITS potential hit(s). Review above before merging."
  if [ "$STRICT" = true ]; then
    exit 1
  else
    exit 0
  fi
fi
