#!/usr/bin/env bash
# export-conversations.sh — 导出 AI 会话记录供 nightly pipeline 使用
# 用法: ./scripts/export-conversations.sh [DAYS]
# 依赖: convs CLI (https://github.com/nicepkg/aide — or your AI chat export tool)

set -euo pipefail

# ── 配置 ──────────────────────────────────────────────────────
# convs 工具路径 — 替换为你的实际路径
CONVS_BIN="${CONVS_BIN:-$(which convs 2>/dev/null || echo '')}"

# 导出目标目录 — 替换为你的 transcript 存放路径
TRANSCRIPT_DIR="${TRANSCRIPT_DIR:-${HOME}/brain-transcripts}"

# 导出天数（默认 3 天，convs 会自动去重）
DAYS="${1:-3}"

# ── 执行 ──────────────────────────────────────────────────────
if [[ -z "$CONVS_BIN" ]] || [[ ! -x "$CONVS_BIN" ]]; then
  echo "⚠️  convs not found. Please install convs and set CONVS_BIN."
  echo "   See: https://github.com/nicepkg/aide or your preferred AI chat export tool"
  echo "   Skipping conversation export."
  exit 0
fi

mkdir -p "$TRANSCRIPT_DIR"

echo "📤 Exporting conversations (last ${DAYS} days)..."
"$CONVS_BIN" --days "$DAYS" --markdown-dir "$TRANSCRIPT_DIR" --no-open

echo "exported_conversations_days=$DAYS"
echo "transcript_dir=$TRANSCRIPT_DIR"
echo "✅ Export complete"
