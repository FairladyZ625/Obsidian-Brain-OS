#!/usr/bin/env bash
# check-pii.sh
# Scan all tracked files for PII: absolute paths, real names, unresolved template tokens.
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
echo "── Absolute paths ──"
RESULT=$(grep -rn \
  --include="*.md" --include="*.sh" --include="*.py" --include="*.yml" --include="*.yaml" \
  -E '/Users/[a-zA-Z][a-zA-Z0-9_-]+/|/home/[a-zA-Z][a-zA-Z0-9_-]+/' \
  "$ROOT" \
  --exclude-dir=".git" \
  2>/dev/null || true)

if [ -n "$RESULT" ]; then
  echo "$RESULT"
  HITS=$((HITS + $(echo "$RESULT" | wc -l)))
else
  echo "  ✅ none"
fi
echo ""

# 2. Unresolved template tokens ({{...}} that weren't replaced)
echo "── Unresolved template tokens ──"
RESULT=$(grep -rn \
  --include="*.md" --include="*.sh" --include="*.py" \
  -E '\{\{[A-Z_]+\}\}' \
  "$ROOT" \
  --exclude-dir=".git" \
  2>/dev/null || true)

if [ -n "$RESULT" ]; then
  echo "$RESULT"
  HITS=$((HITS + $(echo "$RESULT" | wc -l)))
else
  echo "  ✅ none"
fi
echo ""

# 3. Discord IDs (18-digit snowflakes that look like real IDs)
echo "── Potential Discord IDs (18-digit) ──"
RESULT=$(grep -rn \
  --include="*.md" --include="*.sh" --include="*.py" \
  -E '\b[0-9]{17,19}\b' \
  "$ROOT" \
  --exclude-dir=".git" \
  2>/dev/null || true)

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
