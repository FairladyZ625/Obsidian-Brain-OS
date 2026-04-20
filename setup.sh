#!/usr/bin/env bash
# =============================================================================
# Brain OS Setup Script
# Interactive installer for Obsidian Brain OS
# Run: bash setup.sh
# =============================================================================

set -euo pipefail

REPO_DIR="$(cd "$(dirname "$0")" && pwd)"

# Modes and CLI args
TEST_MODE=false
NON_INTERACTIVE=false
TEST_BASE="/tmp/brain-os-test"

CLI_BRAIN_PATH=""
CLI_USER_NAME=""
CLI_TIMEZONE=""
CLI_LANGUAGE=""
CLI_WORKSPACE_PATH=""
CLI_SKILLS_PATH=""
CLI_TRANSCRIPT_DIR=""
CLI_INSTALL_CONVS=""
CLI_INSTALL_SKILLS=""
CLI_INSTALL_RECOMMENDED=""
CLI_INIT_OBSERVER=""
CLI_MAIN_AGENT_NAME=""
CLI_MAIN_MODEL=""
CLI_LIGHT_MODEL=""
CLI_PROFILE=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --test)
      TEST_MODE=true
      shift
      ;;
    --non-interactive)
      NON_INTERACTIVE=true
      shift
      ;;
    --brain-path)
      CLI_BRAIN_PATH="$2"
      shift 2
      ;;
    --user-name)
      CLI_USER_NAME="$2"
      shift 2
      ;;
    --timezone)
      CLI_TIMEZONE="$2"
      shift 2
      ;;
    --language)
      CLI_LANGUAGE="$2"
      shift 2
      ;;
    --workspace-path)
      CLI_WORKSPACE_PATH="$2"
      shift 2
      ;;
    --skills-path)
      CLI_SKILLS_PATH="$2"
      shift 2
      ;;
    --transcript-dir)
      CLI_TRANSCRIPT_DIR="$2"
      shift 2
      ;;
    --profile)
      CLI_PROFILE="$2"
      shift 2
      ;;
    --with-conversation-mining)
      CLI_INSTALL_CONVS="y"
      shift
      ;;
    --skip-conversation-mining)
      CLI_INSTALL_CONVS="n"
      shift
      ;;
    --install-skills)
      CLI_INSTALL_SKILLS="y"
      shift
      ;;
    --skip-skills)
      CLI_INSTALL_SKILLS="n"
      shift
      ;;
    --install-recommended-skills)
      CLI_INSTALL_RECOMMENDED="y"
      shift
      ;;
    --skip-recommended-skills)
      CLI_INSTALL_RECOMMENDED="n"
      shift
      ;;
    --with-observer)
      CLI_INIT_OBSERVER="y"
      shift
      ;;
    --skip-observer)
      CLI_INIT_OBSERVER="n"
      shift
      ;;
    --main-agent-name)
      CLI_MAIN_AGENT_NAME="$2"
      shift 2
      ;;
    --main-model)
      CLI_MAIN_MODEL="$2"
      shift 2
      ;;
    --light-model)
      CLI_LIGHT_MODEL="$2"
      shift 2
      ;;
    *)
      echo "Unknown argument: $1" >&2
      exit 1
      ;;
  esac
done

if $TEST_MODE; then
  rm -rf "$TEST_BASE"
  mkdir -p "$TEST_BASE"
  echo "[TEST MODE] All outputs → $TEST_BASE"
fi

CONFIG_FILE="$REPO_DIR/scripts/config.env"
CONFIG_EXAMPLE="$REPO_DIR/scripts/config.env.example"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
BOLD='\033[1m'
NC='\033[0m' # No Color

print_header() {
  echo ""
  echo -e "${BOLD}${BLUE}╔══════════════════════════════════════╗${NC}"
  echo -e "${BOLD}${BLUE}║     Obsidian Brain OS  Setup         ║${NC}"
  echo -e "${BOLD}${BLUE}╚══════════════════════════════════════╝${NC}"
  echo ""
}

print_step() {
  echo ""
  echo -e "${BOLD}${GREEN}▶ $1${NC}"
}

print_warn() {
  echo -e "${YELLOW}⚠  $1${NC}"
}

print_ok() {
  echo -e "${GREEN}✓  $1${NC}"
}

print_err() {
  echo -e "${RED}✗  $1${NC}"
}

replace_literal_in_file() {
  local needle="$1"
  local replacement="$2"
  local file="$3"
  OLD="$needle" NEW="$replacement" perl -0pi -e 's/\Q$ENV{OLD}\E/$ENV{NEW}/g' "$file"
}

ask() {
  local prompt="$1"
  local default="${2:-}"
  if $TEST_MODE || $NON_INTERACTIVE; then
    REPLY="$default"
    echo -e "${BOLD}${prompt}${NC} [auto] ${GREEN}${default}${NC}"
    return
  fi
  if [[ -n "$default" ]]; then
    echo -ne "${BOLD}${prompt}${NC} [${default}]: "
  else
    echo -ne "${BOLD}${prompt}${NC}: "
  fi
  read -r REPLY
  if [[ -z "$REPLY" && -n "$default" ]]; then
    REPLY="$default"
  fi
}

ask_yn() {
  local prompt="$1"
  local default="${2:-y}"
  if $TEST_MODE || $NON_INTERACTIVE; then
    REPLY="$default"
    echo -e "${BOLD}${prompt}${NC} [auto] ${GREEN}${default}${NC}"
    [[ "$default" =~ ^[Yy] ]]
    return
  fi
  echo -ne "${BOLD}${prompt}${NC} [y/n, default=${default}]: "
  read -r REPLY
  if [[ -z "$REPLY" ]]; then
    REPLY="$default"
  fi
  [[ "$REPLY" =~ ^[Yy] ]]
}

# =============================================================================
# Step 0: Welcome
# =============================================================================
print_header
echo "This script will help you set up Obsidian Brain OS."
echo "Your vault folder name is fully user-defined, it does not need to be named ZeYu-AI-Brain."
echo "Default install profile: ${CLI_PROFILE:-minimal}"
echo "It will:"
echo "  1. Copy the vault template to your chosen location"
echo "  2. Configure paths in config.env"
echo "  3. Install skills (optional)"
echo "  4. Install conversation-mining tool (optional)"
echo "  5. Initialize Observer .learnings/ directory (optional)"
echo "  6. Run PII scan verification"
echo "  7. Verify the installation"
echo ""
echo -e "${YELLOW}You can re-run this script at any time to reconfigure.${NC}"

# =============================================================================
# Step 1: Vault location
# =============================================================================
print_step "Step 1: Vault Location"

if $TEST_MODE; then
  DEFAULT_VAULT="$TEST_BASE/vault"
else
  DEFAULT_VAULT="$HOME/my-brain"
fi
ask "Where do you want to create your Brain OS vault? (any folder name is fine)" "${CLI_BRAIN_PATH:-$DEFAULT_VAULT}"
BRAIN_PATH="$REPLY"

if [[ -d "$BRAIN_PATH" ]]; then
  print_warn "Directory already exists: $BRAIN_PATH"
  if ask_yn "Copy vault template into it anyway? (existing files will NOT be overwritten)" "n"; then
    cp -rn "$REPO_DIR/vault-template/." "$BRAIN_PATH/"
    print_ok "Vault template merged into $BRAIN_PATH"
  else
    echo "Skipping vault template copy."
  fi
else
  cp -r "$REPO_DIR/vault-template" "$BRAIN_PATH"
  print_ok "Vault created at: $BRAIN_PATH"
fi

# =============================================================================
# Step 2: User info
# =============================================================================
print_step "Step 2: User Info"

ask "Your name (used in templates and daily briefs)" "${CLI_USER_NAME:-SmokeTest}"
USER_NAME="$REPLY"

ask "Your timezone (e.g., Asia/Shanghai, America/New_York)" "${CLI_TIMEZONE:-$(date +%Z)}"
TIMEZONE="$REPLY"

ask "Your primary language (en/zh/other)" "${CLI_LANGUAGE:-en}"
LANGUAGE="$REPLY"

# =============================================================================
# Step 3: Paths
# =============================================================================
print_step "Step 3: Path Configuration"

DEFAULT_WORKSPACE="$HOME/.openclaw/workspace"
if $TEST_MODE; then DEFAULT_WORKSPACE="$TEST_BASE/workspace"; fi
ask "Your OpenClaw workspace path" "${CLI_WORKSPACE_PATH:-$DEFAULT_WORKSPACE}"
WORKSPACE_PATH="$REPLY"

DEFAULT_SKILLS="$HOME/.agents/skills"
if $TEST_MODE; then DEFAULT_SKILLS="$TEST_BASE/skills"; fi
ask "Your skills directory path" "${CLI_SKILLS_PATH:-$DEFAULT_SKILLS}"
SKILLS_PATH="$REPLY"

# =============================================================================
# Step 4: Optional — conversation-mining
# =============================================================================
print_step "Step 4: Conversation Mining (Optional)"
echo "conversation-mining exports AI conversations for nightly processing."
echo "Requires: Python 3.9+, pip"

TRANSCRIPT_DIR=""
INSTALL_CONVS="n"

if ask_yn "Do you want to set up conversation-mining?" "${CLI_INSTALL_CONVS:-n}"; then
  INSTALL_CONVS="y"
  ask "Where are your AI conversation transcripts stored?" "${CLI_TRANSCRIPT_DIR:-$HOME/conversations}"
  TRANSCRIPT_DIR="$REPLY"

  echo ""
  echo "Installing conversation-mining tool..."
  if command -v pip3 &>/dev/null; then
    pip3 install -e "$REPO_DIR/tools/conversation-mining" --quiet && \
      print_ok "conversation-mining installed" || \
      print_warn "Install failed — you can do it manually later: pip install -e tools/conversation-mining"
  else
    print_warn "pip3 not found — skipping auto-install. Run manually: pip install -e tools/conversation-mining"
  fi
fi

# =============================================================================
# Step 5: Write config.env
# =============================================================================
print_step "Step 5: Writing Configuration"

if $TEST_MODE; then
  CONFIG_FILE="$TEST_BASE/config.env"
fi
mkdir -p "$(dirname "$CONFIG_FILE")"

cat > "$CONFIG_FILE" << ENVEOF
# Brain OS Configuration
# Generated by setup.sh on $(date)
# Edit this file to update your configuration

# === Core Paths ===
BRAIN_PATH="$BRAIN_PATH"
WORKSPACE_PATH="$WORKSPACE_PATH"
SKILLS_PATH="$SKILLS_PATH"

# === User Info ===
USER_NAME="$USER_NAME"
TIMEZONE="$TIMEZONE"
LANGUAGE="$LANGUAGE"

# === Conversation Mining ===
TRANSCRIPT_DIR="${TRANSCRIPT_DIR:-}"

# === Optional: Discord Webhook ===
# DISCORD_WEBHOOK_URL=""

# === Optional: OpenClaw ===
# OPENCLAW_WORKSPACE="$WORKSPACE_PATH"
ENVEOF

print_ok "config.env written to: $CONFIG_FILE"

# =============================================================================
# Step 6: Install Skills (optional)
# =============================================================================
print_step "Step 6: Install Skills (Optional)"
echo "Skills are Agent instruction files that tell AI how to use Brain OS."

PROFILE="${CLI_PROFILE:-minimal}"
if [[ ! "$PROFILE" =~ ^(minimal|standard|advanced)$ ]]; then
  print_err "Invalid profile: $PROFILE (expected minimal|standard|advanced)"
  exit 1
fi

echo "Install profile: $PROFILE"

install_skill_dir() {
  local skill_name="$1"
  local source_dir="$REPO_DIR/skills/$skill_name"
  local target_dir="$SKILLS_PATH/$skill_name"

  if [[ ! -d "$source_dir" ]]; then
    print_warn "Skill source not found: $skill_name"
    return
  fi
  mkdir -p "$SKILLS_PATH"
  if [[ -d "$target_dir" ]]; then
    print_warn "Skill '$skill_name' already exists — skipping"
  else
    cp -r "$source_dir" "$target_dir"
    print_ok "Installed skill: $skill_name"
  fi
}

if ask_yn "Install profile-selected skills to $SKILLS_PATH?" "${CLI_INSTALL_SKILLS:-y}"; then
  case "$PROFILE" in
    minimal)
      PROFILE_SKILLS=(brain-os-installer article-notes-integration)
      ;;
    standard)
      PROFILE_SKILLS=(brain-os-installer article-notes-integration personal-ops-driver conversation-knowledge-flywheel knowledge-flywheel-amplifier)
      ;;
    advanced)
      PROFILE_SKILLS=(brain-os-installer article-notes-integration personal-ops-driver conversation-knowledge-flywheel knowledge-flywheel-amplifier observer notebooklm deep-research daily-timesheet brain-os-release)
      ;;
  esac

  for skill_name in "${PROFILE_SKILLS[@]}"; do
    install_skill_dir "$skill_name"
  done

  if [[ "$PROFILE" != "minimal" ]] && ask_yn "Also install recommended skills?" "${CLI_INSTALL_RECOMMENDED:-n}"; then
    for skill_dir in "$REPO_DIR/skills/recommended"/*/; do
      install_skill_dir "$(basename "$skill_dir")"
    done
  fi
fi

# =============================================================================
# Step 7: Observer .learnings/ directory (Optional)
# =============================================================================
print_step "Step 7: Observer .learnings/ Directory (Optional)"
echo "Observer is the AI team health monitor. It stores its operational memory in"
echo ".learnings/observer/ inside your vault."

LEARNINGS_DIR=""
if ask_yn "Initialize Observer .learnings/ directory?" "${CLI_INIT_OBSERVER:-y}"; then
  LEARNINGS_DIR="$BRAIN_PATH/.learnings"
  mkdir -p "$LEARNINGS_DIR/observer/plans"
  mkdir -p "$LEARNINGS_DIR/observer/history"

  INDEX_FILE="$LEARNINGS_DIR/observer/index.json"
  if [[ ! -f "$INDEX_FILE" ]]; then
    cat > "$INDEX_FILE" << LEARNINGSEOF
{
  "version": "1.0",
  "lastUpdated": "$(date -I)",
  "recurrenceMap": {},
  "promoteCandidates": []
}
LEARNINGSEOF
    print_ok "Observer index created: $INDEX_FILE"
  else
    print_warn "Observer index already exists: $INDEX_FILE"
  fi
  print_ok ".learnings/ initialized at: $LEARNINGS_DIR"
fi

# =============================================================================
# Step 8: PII Scan Verification
# =============================================================================
print_step "Step 8: PII Scan Verification"
echo "Running the PII scanner to check for accidental private data..."

if [[ -f "$REPO_DIR/scripts/check-pii.sh" ]]; then
  if bash "$REPO_DIR/scripts/check-pii.sh --strict" 2>&1; then
    print_ok "PII scan passed — no private data found"
  else
    print_warn "PII scan found potential issues — review output above"
    print_warn "Run manually later: bash scripts/check-pii.sh --strict"
  fi
else
  print_warn "check-pii.sh not found — skipping PII verification"
fi
# =============================================================================
print_step "Step 9: Prepare Cron Templates (Optional)"
echo "If you use OpenClaw, you can import cron jobs for the nightly pipeline."

CRON_OUT_DIR="$REPO_DIR/cron-examples/generated"
mkdir -p "$CRON_OUT_DIR"

for template in "$REPO_DIR/cron-examples"/*.json; do
  filename="$(basename "$template")"
  output="$CRON_OUT_DIR/$filename"
  sed \
    -e "s|/tmp/brain-os-final-vault|$BRAIN_PATH|g" \
    -e "s|/tmp/brain-os-final-workspace|$WORKSPACE_PATH|g" \
    -e "s|/tmp/brain-os-final-skills|$SKILLS_PATH|g" \
    -e "s|{{TRANSCRIPT_DIR}}|${TRANSCRIPT_DIR:-$HOME/conversations}|g" \
    -e "s|SmokeTest|$USER_NAME|g" \
    -e "s|Asia/Shanghai|$TIMEZONE|g" \
    -e "s|{{DISCORD_WEBHOOK_URL}}||g" \
    "$template" > "$output"
  print_ok "Generated: cron-examples/generated/$filename"
done

echo ""
echo -e "${YELLOW}To import cron jobs into OpenClaw:${NC}"
echo "  openclaw cron import $CRON_OUT_DIR/nightly-pipeline.json"
echo "  openclaw cron import $CRON_OUT_DIR/personal-ops.json"
echo ""
echo -e "${YELLOW}Remember to set DISCORD_WEBHOOK_URL in the generated files if you use webhooks.${NC}"

# =============================================================================
# Step 10: Bulk placeholder replacement across entire repo
# =============================================================================
print_step "Step 10: Bulk Placeholder Replacement"

echo "Replacing all placeholders in cron templates, skills, prompts, and docs..."
echo "This makes the entire repo ready to use with your configuration."
echo ""

# Define all replacements from config.env values
REPLACEMENTS=(
  "/tmp/brain-os-final-vault|$BRAIN_PATH"
  "/tmp/brain-os-final-workspace|$WORKSPACE_PATH"
  "/tmp/brain-os-final-skills|$SKILLS_PATH"
  "SmokeTest|$USER_NAME"
  "Asia/Shanghai|$TIMEZONE"
)

# Agent identity placeholders (set later, after user provides model info)
AGENT_PLACEHOLDERS=(
  "{{MAIN_AGENT_NAME}}"
  "{{REVIEW_AGENT_NAME}}"
  "{{PROJECT_TOOL}}"
  "{{MAIN_MODEL}}"
  "{{LIGHT_MODEL}}"
)

REPLACE_COUNT=0

# Phase 1: Path/user replacements
for item in "${REPLACEMENTS[@]}"; do
  ph="${item%%|*}"
  val="${item#*|}"
  while IFS= read -r -d '' file; do
    [[ "$file" == *".git"* ]] && continue
    [[ "$file" == *"generated"* ]] && continue
    [[ "$file" == *"node_modules"* ]] && continue
    if grep -qF "$ph" "$file" 2>/dev/null; then
      replace_literal_in_file "$ph" "$val" "$file"
      REPLACE_COUNT=$((REPLACE_COUNT+1))
    fi
  done < <(find "$REPO_DIR" -type f \( -name '*.md' -o -name '*.json' -o -name '*.sh' \) -print0 2>/dev/null)
done

if $TEST_MODE; then
  # In test mode: replace agent placeholders with generic defaults
  for ph in "${AGENT_PLACEHOLDERS[@]}"; do
    case "$ph" in
      "{{MAIN_AGENT_NAME}}") val="Brain OS Manager" ;;
      "{{REVIEW_AGENT_NAME}}") val="Review Agent" ;;
      "{{PROJECT_TOOL}}") val="External Tool" ;;
      "{{MAIN_MODEL}}") val="your-main-model" ;;
      "{{LIGHT_MODEL}}") val="your-light-model" ;;
      *) val="placeholder" ;;
    esac
    while IFS= read -r -d '' file; do
      [[ "$file" == *".git"* ]] && continue
      [[ "$file" == *"generated"* ]] && continue
      if grep -qF "$ph" "$file" 2>/dev/null; then
        replace_literal_in_file "$ph" "$val" "$file"
        REPLACE_COUNT=$((REPLACE_COUNT+1))
      fi
    done < <(find "$REPO_DIR" -type f \( -name '*.md' -o -name '*.json' \) -print0 2>/dev/null)
  done
  print_ok "Bulk replacement done ($REPLACE_COUNT substitutions, test mode)"
else
  # Ask for agent info
  ask "Your main agent's display name (e.g., Brain OS Manager)" "${CLI_MAIN_AGENT_NAME:-Brain OS Manager}"
  MAIN_AGENT_NAME="$REPLY"
  ask "Your main model ID (e.g., gpt-4o, claude-sonnet-4)" "${CLI_MAIN_MODEL:-}"
  MAIN_MODEL="$REPLY"
  ask "Your lightweight model for routine tasks (e.g., haiku, glm-4.7-flash)" "${CLI_LIGHT_MODEL:-}"
  LIGHT_MODEL="$REPLY"
  
  AGENT_VALS=(
    "{{MAIN_AGENT_NAME}}|$MAIN_AGENT_NAME"
    "{{MAIN_MODEL}}|$MAIN_MODEL"
    "{{LIGHT_MODEL}}|$LIGHT_MODEL"
    "{{REVIEW_AGENT_NAME}}|Review Agent"
    "{{PROJECT_TOOL}}|External Project Tool"
  )
  
  for item in "${AGENT_VALS[@]}"; do
    ph="${item%%|*}"
    val="${item#*|}"
    while IFS= read -r -d '' file; do
      [[ "$file" == *".git"* ]] && continue
      [[ "$file" == *"generated"* ]] && continue
      if grep -qF "$ph" "$file" 2>/dev/null; then
        replace_literal_in_file "$ph" "$val" "$file"
        REPLACE_COUNT=$((REPLACE_COUNT+1))
      fi
    done < <(find "$REPO_DIR" -type f \( -name '*.md' -o -name '*.json' \) -print0 2>/dev/null)
  done
  print_ok "Bulk replacement done ($REPLACE_COUNT substitutions)"
fi
# =============================================================================
# Step 11: Verify
# =============================================================================
print_step "Step 11: Verification"

PASS=0
FAIL=0

check() {
  local desc="$1"
  local result="$2"
  if [[ "$result" == "ok" ]]; then
    print_ok "$desc"
    PASS=$((PASS+1))
  else
    print_err "$desc — $result"
    FAIL=$((FAIL+1))
  fi
}

# Check vault
if [[ -d "$BRAIN_PATH/00-INBOX" ]]; then
  check "Vault structure exists" "ok"
else
  check "Vault structure" "00-INBOX not found in $BRAIN_PATH"
fi
if [[ -d "$BRAIN_PATH/03-KNOWLEDGE" ]]; then
  check "Knowledge layer exists" "ok"
else
  check "Knowledge layer" "missing"
fi
if [[ -f "$CONFIG_FILE" ]]; then
  check "config.env written" "ok"
else
  check "config.env" "missing"
fi

# Check skills
if [[ -d "$SKILLS_PATH/brain-os-installer" ]]; then
  check "brain-os-installer skill installed" "ok"
else
  print_warn "brain-os-installer not found in $SKILLS_PATH (skip if you didn't install skills)"
fi
if [[ -d "$SKILLS_PATH/article-notes-integration" ]]; then
  check "article-notes-integration skill installed" "ok"
else
  print_warn "article-notes-integration not found in $SKILLS_PATH (skip if you didn't install skills)"
fi

# Run knowledge-lint
if bash "$REPO_DIR/scripts/knowledge-lint.sh" "$BRAIN_PATH" &>/dev/null; then
  check "knowledge-lint.sh runs without errors" "ok"
else
  check "knowledge-lint.sh" "returned errors (run manually to see details)"
fi

# Summary

# Check Observer .learnings/
if [[ -d "$BRAIN_PATH/.learnings/observer" ]]; then
  check "Observer .learnings/ directory exists" "ok"
else
  print_warn "Observer .learnings/ not found (skip if you didn't initialize it)"
fi

# Check PII scanner exists
if [[ -f "$REPO_DIR/scripts/check-pii.sh" ]]; then
  check "PII scanner (check-pii.sh) exists" "ok"
else
  print_warn "check-pii.sh not found"
fi
echo ""
echo -e "${BOLD}══════════════════════════════════════${NC}"
echo -e "${BOLD}Setup Summary${NC}"
echo -e "${GREEN}  ✓ Passed: $PASS${NC}"
if [[ $FAIL -gt 0 ]]; then
  echo -e "${RED}  ✗ Failed: $FAIL${NC}"
else
  echo -e "${GREEN}  All checks passed!${NC}"
fi
echo ""
echo -e "${BOLD}Your Brain OS is ready.${NC}"
echo ""
echo "Next steps (see also docs/component-guide.md for full inventory):"
echo "  1. Open Obsidian → File → Open Vault → $BRAIN_PATH"
echo "  2. Read docs/getting-started.md for the recommended day-one path"
echo "  3. Read docs/component-guide.md for a complete feature overview"
echo "  4. Configure your AI Agent following docs/agents.md"
if [[ -d "$BRAIN_PATH/.learnings/observer" ]]; then
  echo "  5. If you want Observer, read docs/agent-playbooks/observer-playbook.md"
fi
if [[ $INSTALL_CONVS == "y" ]]; then
  echo "  6. Test conversation export: conversation-mining --no-open --days 1"
fi
echo ""
echo -e "${BLUE}Full documentation: https://github.com/FairladyZ625/Obsidian-Brain-OS${NC}"
