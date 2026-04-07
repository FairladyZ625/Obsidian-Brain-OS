#!/usr/bin/env bash
# =============================================================================
# Brain OS Setup Script
# Interactive installer for Obsidian Brain OS
# Run: bash setup.sh
# =============================================================================

set -euo pipefail

REPO_DIR="$(cd "$(dirname "$0")" && pwd)"

# --test mode: redirect all outputs to /tmp/brain-os-test/
TEST_MODE=false
TEST_BASE="/tmp/brain-os-test"
for arg in "$@"; do
  [[ "$arg" == "--test" ]] && TEST_MODE=true
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

ask() {
  local prompt="$1"
  local default="${2:-}"
  if $TEST_MODE; then
    REPLY="$default"
    echo -e "${BOLD}${prompt}${NC} [TEST: using default] ${GREEN}${default}${NC}"
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
  if $TEST_MODE; then
    REPLY="$default"
    echo -e "${BOLD}${prompt}${NC} [TEST: using default] ${GREEN}${default}${NC}"
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
echo "It will:"
echo "  1. Copy the vault template to your chosen location"
echo "  2. Configure paths in config.env"
echo "  3. Install skills (optional)"
echo "  4. Install conversation-mining tool (optional)"
echo "  5. Verify the installation"
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
ask "Where do you want to create your Brain OS vault?" "$DEFAULT_VAULT"
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

ask "Your name (used in templates and daily briefs)" "Alex"
USER_NAME="$REPLY"

ask "Your timezone (e.g., Asia/Shanghai, America/New_York)" "$(date +%Z)"
TIMEZONE="$REPLY"

ask "Your primary language (en/zh/other)" "en"
LANGUAGE="$REPLY"

# =============================================================================
# Step 3: Paths
# =============================================================================
print_step "Step 3: Path Configuration"

DEFAULT_WORKSPACE="$HOME/.openclaw/workspace"
if $TEST_MODE; then DEFAULT_WORKSPACE="$TEST_BASE/workspace"; fi
ask "Your OpenClaw workspace path" "$DEFAULT_WORKSPACE"
WORKSPACE_PATH="$REPLY"

DEFAULT_SKILLS="$HOME/.agents/skills"
if $TEST_MODE; then DEFAULT_SKILLS="$TEST_BASE/skills"; fi
ask "Your skills directory path" "$DEFAULT_SKILLS"
SKILLS_PATH="$REPLY"

# =============================================================================
# Step 4: Optional — conversation-mining
# =============================================================================
print_step "Step 4: Conversation Mining (Optional)"
echo "conversation-mining exports AI conversations for nightly processing."
echo "Requires: Python 3.9+, pip"

TRANSCRIPT_DIR=""
INSTALL_CONVS="n"

if ask_yn "Do you want to set up conversation-mining?" "n"; then
  INSTALL_CONVS="y"
  ask "Where are your AI conversation transcripts stored?" "$HOME/conversations"
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

if ask_yn "Install core skills to $SKILLS_PATH?" "y"; then
  if [[ -d "$SKILLS_PATH" ]]; then
    # Backup existing skills with same name
    for skill_dir in "$REPO_DIR/skills"/*/; do
      skill_name="$(basename "$skill_dir")"
      target="$SKILLS_PATH/$skill_name"
      if [[ -d "$target" ]]; then
        print_warn "Skill '$skill_name' already exists — skipping (use --force to overwrite)"
      else
        cp -r "$skill_dir" "$target"
        print_ok "Installed skill: $skill_name"
      fi
    done
  else
    mkdir -p "$SKILLS_PATH"
    cp -r "$REPO_DIR/skills"/. "$SKILLS_PATH/"
    print_ok "All core skills installed to $SKILLS_PATH"
  fi

  if ask_yn "Also install recommended skills?" "y"; then
    for skill_dir in "$REPO_DIR/skills/recommended"/*/; do
      skill_name="$(basename "$skill_dir")"
      target="$SKILLS_PATH/$skill_name"
      if [[ -d "$target" ]]; then
        print_warn "Skill '$skill_name' already exists — skipping"
      else
        cp -r "$skill_dir" "$target"
        print_ok "Installed: $skill_name"
      fi
    done
  fi
fi

# =============================================================================
# Step 7: Replace placeholders in cron examples
# =============================================================================
print_step "Step 7: Prepare Cron Templates (Optional)"
echo "If you use OpenClaw, you can import cron jobs for the nightly pipeline."

CRON_OUT_DIR="$REPO_DIR/cron-examples/generated"
mkdir -p "$CRON_OUT_DIR"

for template in "$REPO_DIR/cron-examples"/*.json; do
  filename="$(basename "$template")"
  output="$CRON_OUT_DIR/$filename"
  sed \
    -e "s|{{BRAIN_PATH}}|$BRAIN_PATH|g" \
    -e "s|{{WORKSPACE_PATH}}|$WORKSPACE_PATH|g" \
    -e "s|{{SKILLS_PATH}}|$SKILLS_PATH|g" \
    -e "s|{{TRANSCRIPT_DIR}}|${TRANSCRIPT_DIR:-$HOME/conversations}|g" \
    -e "s|{{USER_NAME}}|$USER_NAME|g" \
    -e "s|{{TIMEZONE}}|$TIMEZONE|g" \
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
# Step 8: Verify
# =============================================================================
print_step "Step 8: Verification"

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
if [[ -d "$SKILLS_PATH/personal-ops-driver" ]]; then
  check "personal-ops-driver skill installed" "ok"
else
  print_warn "personal-ops-driver not found in $SKILLS_PATH (skip if you didn't install skills)"
fi

# Run knowledge-lint
if bash "$REPO_DIR/scripts/knowledge-lint.sh" "$BRAIN_PATH" &>/dev/null; then
  check "knowledge-lint.sh runs without errors" "ok"
else
  check "knowledge-lint.sh" "returned errors (run manually to see details)"
fi

# Summary
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
echo "Next steps:"
echo "  1. Open Obsidian → File → Open Vault → $BRAIN_PATH"
echo "  2. Read docs/guide/03-daily-workflow.md to understand daily usage"
echo "  3. Configure your AI Agent following docs/guide/01-agent-setup.md"
if [[ $INSTALL_CONVS == "y" ]]; then
  echo "  4. Test conversation export: conversation-mining --no-open --days 1"
fi
echo ""
echo -e "${BLUE}Full documentation: https://github.com/FairladyZ625/Obsidian-Brain-OS${NC}"
