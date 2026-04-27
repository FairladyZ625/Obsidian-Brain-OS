#!/usr/bin/env bash
set -euo pipefail

PACK_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MODE=""
ANSWERS="$PACK_DIR/answers.example.json"
OUT=""
YES="false"
FORCE="false"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --check) MODE="check"; shift ;;
    --dry-run) MODE="dry-run"; shift ;;
    --answers) ANSWERS="$2"; shift 2 ;;
    --out) OUT="$2"; shift 2 ;;
    --apply) MODE="apply"; shift ;;
    --yes) YES="true"; shift ;;
    --force) FORCE="true"; shift ;;
    *) echo "Unknown argument: $1" >&2; exit 2 ;;
  esac
done

MODE="${MODE:-dry-run}"

check_json() { python3 -m json.tool "$1" >/dev/null; }

if [[ "$MODE" == "check" ]]; then
  check_json "$PACK_DIR/manifest.json"
  check_json "$PACK_DIR/openclaw.json.patch.template"
  check_json "$PACK_DIR/cron/jobs.patch.template"
  check_json "$ANSWERS"
  node "$PACK_DIR/scripts/scan-secrets.mjs" "$PACK_DIR" >/dev/null
  echo "OpenClaw Brain OS pack check ok"
  echo "Pack: $(python3 - <<PY
import json
m=json.load(open('$PACK_DIR/manifest.json'))
print(m['packName'], m['packVersion'])
PY
)"
  echo "Answers: $ANSWERS"
  exit 0
fi

if [[ "$MODE" == "dry-run" ]]; then
  if [[ -z "$OUT" ]]; then
    OUT="${TMPDIR:-/tmp}/openclaw-brain-os-pack-preview/$(date +%Y%m%d-%H%M%S)"
  fi
  node "$PACK_DIR/scripts/render.mjs" --pack "$PACK_DIR" --answers "$ANSWERS" --out "$OUT"
  echo "Dry-run preview written to: $OUT"
  exit 0
fi

if [[ "$MODE" == "apply" ]]; then
  if [[ -z "$OUT" ]]; then
    OUT="${TMPDIR:-/tmp}/openclaw-brain-os-pack-preview/$(date +%Y%m%d-%H%M%S)"
  fi
  node "$PACK_DIR/scripts/render.mjs" --pack "$PACK_DIR" --answers "$ANSWERS" --out "$OUT" >/dev/null
  bash "$PACK_DIR/verify.sh" "$OUT" >/dev/null
  APPLY_ARGS=("$PACK_DIR/scripts/apply.mjs" --pack "$PACK_DIR" --answers "$ANSWERS" --preview "$OUT")
  if [[ "$YES" == "true" ]]; then APPLY_ARGS+=(--yes); fi
  if [[ "$FORCE" == "true" ]]; then APPLY_ARGS+=(--force); fi
  node "${APPLY_ARGS[@]}"
  exit 0
fi

echo "Unsupported mode: $MODE" >&2
exit 2
