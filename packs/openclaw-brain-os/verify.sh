#!/usr/bin/env bash
set -euo pipefail

TARGET="${1:-}"
if [[ -z "$TARGET" ]]; then
  echo "Usage: bash verify.sh <preview-dir>" >&2
  exit 2
fi

python3 -m json.tool "$TARGET/openclaw.config-patch.json" >/dev/null
python3 -m json.tool "$TARGET/cron.jobs-patch.json" >/dev/null
python3 -m json.tool "$TARGET/summary.json" >/dev/null

ALLOW_PLACEHOLDERS="DISCORD_GUILD_ID,DISCORD_OWNER_USER_ID,MAIN_CHANNEL_ID,PERSONAL_OPS_CHANNEL_ID,KNOWLEDGE_INGEST_CHANNEL_ID,KNOWLEDGE_QUERY_CHANNEL_ID,OSS_SYNC_CHANNEL_ID,CRON_NOTIFICATION_CHANNEL_ID,OWNER_NAME,MAIN_MODEL,LIGHT_MODEL,QMD_BIN" node "$(dirname "${BASH_SOURCE[0]}")/scripts/check-placeholders.mjs" "$TARGET"
node "$(dirname "${BASH_SOURCE[0]}")/scripts/scan-secrets.mjs" "$TARGET"

test -f "$TARGET/diff-summary.md"
test -f "$TARGET/INSTALL_REPORT.md"
test -d "$TARGET/workspaces/main"
test -f "$TARGET/workspaces/main/AGENTS.md"

echo "OpenClaw Brain OS pack preview verify ok"
