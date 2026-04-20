#!/usr/bin/env bash
set -euo pipefail

REPO_DIR="$(cd "$(dirname "$0")/.." && pwd)"
CONFIG_FILE="${BRAIN_OS_CONFIG:-$REPO_DIR/scripts/config.env}"

PASS=0
FAIL=0
WARN=0

ok() {
  echo "✓ $1"
  PASS=$((PASS+1))
}

warn() {
  echo "⚠ $1"
  WARN=$((WARN+1))
}

fail() {
  echo "✗ $1"
  FAIL=$((FAIL+1))
}

if [[ ! -f "$CONFIG_FILE" ]]; then
  fail "config file not found: $CONFIG_FILE"
  echo "Set BRAIN_OS_CONFIG=/path/to/config.env if needed."
  exit 1
fi

# shellcheck disable=SC1090
source "$CONFIG_FILE"

BRAIN_PATH="${BRAIN_PATH:-}"
WORKSPACE_PATH="${WORKSPACE_PATH:-}"
SKILLS_PATH="${SKILLS_PATH:-}"
USER_NAME="${USER_NAME:-}"
TIMEZONE="${TIMEZONE:-}"
LANGUAGE="${LANGUAGE:-}"

check_dir() {
  local path="$1"
  local label="$2"
  if [[ -n "$path" && -d "$path" ]]; then
    ok "$label exists: $path"
  else
    fail "$label missing: ${path:-<empty>}"
  fi
}

check_file() {
  local path="$1"
  local label="$2"
  if [[ -f "$path" ]]; then
    ok "$label exists: $path"
  else
    fail "$label missing: $path"
  fi
}

check_value() {
  local value="$1"
  local label="$2"
  if [[ -n "$value" ]]; then
    ok "$label is set"
  else
    fail "$label is empty"
  fi
}

echo "Brain OS install verification"
echo "Config: $CONFIG_FILE"
echo "---"

check_value "$BRAIN_PATH" "BRAIN_PATH"
check_value "$USER_NAME" "USER_NAME"
check_value "$TIMEZONE" "TIMEZONE"
check_value "$LANGUAGE" "LANGUAGE"
check_value "$WORKSPACE_PATH" "WORKSPACE_PATH"
check_value "$SKILLS_PATH" "SKILLS_PATH"

if [[ -n "$BRAIN_PATH" ]]; then
  check_dir "$BRAIN_PATH" "Vault root"
  [[ -d "$BRAIN_PATH/00-INBOX" ]] && ok "Vault inbox structure present" || fail "Vault missing 00-INBOX"
  [[ -d "$BRAIN_PATH/03-KNOWLEDGE" ]] && ok "Vault knowledge structure present" || fail "Vault missing 03-KNOWLEDGE"
fi

if [[ -n "$SKILLS_PATH" ]]; then
  check_dir "$SKILLS_PATH" "Skills directory"
  [[ -d "$SKILLS_PATH/brain-os-installer" ]] && ok "brain-os-installer skill installed" || warn "brain-os-installer skill not found"
  [[ -d "$SKILLS_PATH/article-notes-integration" ]] && ok "article-notes-integration skill installed" || warn "article-notes-integration skill not found"
fi

check_file "$REPO_DIR/scripts/knowledge-lint.sh" "knowledge-lint.sh"
check_file "$REPO_DIR/scripts/check-pii.sh" "check-pii.sh"

if [[ -n "$BRAIN_PATH" && -d "$BRAIN_PATH" ]]; then
  if bash "$REPO_DIR/scripts/knowledge-lint.sh" "$BRAIN_PATH" >/dev/null 2>&1; then
    ok "knowledge-lint.sh runs successfully"
  else
    fail "knowledge-lint.sh returned non-zero"
  fi
fi

if bash "$REPO_DIR/scripts/check-pii.sh" --strict >/dev/null 2>&1; then
  ok "PII scan passes"
else
  fail "PII scan returned non-zero"
fi

if [[ -d "$BRAIN_PATH/.learnings/observer" ]]; then
  ok "Observer directory exists"
else
  warn "Observer directory not initialized"
fi

echo "---"
echo "Passed: $PASS"
echo "Warnings: $WARN"
echo "Failed: $FAIL"

if [[ $FAIL -gt 0 ]]; then
  exit 1
fi
