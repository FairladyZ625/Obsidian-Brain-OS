#!/usr/bin/env bash
# export-conversations.sh — 导出 AI 会话记录供 nightly pipeline 使用
# 用法: ./scripts/export-conversations.sh [DAYS]
# 依赖: convs.py（内嵌于 tools/conversation-mining/）

set -euo pipefail

# ── 配置 ──────────────────────────────────────────────────────
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
CONVS_MINING_DIR="$REPO_ROOT/tools/conversation-mining"

# convs 工具路径 — 优先使用 CLI，否则 fallback 到内嵌 Python 模块
CONVS_BIN="${CONVS_BIN:-$(which convs 2>/dev/null || echo '')}"
if [[ -z "$CONVS_BIN" ]] && [[ -f "$CONVS_MINING_DIR/convs.py" ]]; then
  CONVS_BIN="python3 $CONVS_MINING_DIR/convs.py"
fi

# 导出目标目录 — 替换为你的 transcript 存放路径
TRANSCRIPT_DIR="${TRANSCRIPT_DIR:-${HOME}/brain-transcripts}"

# 导出天数（默认 3 天，会自动去重）
DAYS="${1:-3}"

# ── 执行 ──────────────────────────────────────────────────────
if [[ -z "$CONVS_BIN" ]] || [[ ! -x "$CONVS_BIN" ]] && [[ ! -f "$CONVS_BIN" ]]; then
  echo "⚠️  convs not found. Please install convs or ensure tools/conversation-mining/convs.py exists."
  echo "   Skipping conversation export."
  exit 0
fi

mkdir -p "$TRANSCRIPT_DIR"

echo "📤 Exporting conversations (last ${DAYS} days)..."
if [[ "$CONVS_BIN" == *.py ]]; then
  python3 "$CONVS_BIN" --markdown-dir "$TRANSCRIPT_DIR" --days "$DAYS" --no-open
else
  "$CONVS_BIN" --days "$DAYS" --markdown-dir "$TRANSCRIPT_DIR" --no-open
fi

echo "exported_conversations_days=$DAYS"
echo "transcript_dir=$TRANSCRIPT_DIR"
echo "✅ Export complete"
