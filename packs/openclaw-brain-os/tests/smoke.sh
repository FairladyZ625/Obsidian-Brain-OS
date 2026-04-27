#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
PACK="$ROOT/packs/openclaw-brain-os"

json_check() {
  local file="$1"
  python3 -m json.tool "$file" >/dev/null
}

json_check "$PACK/manifest.json"
json_check "$PACK/openclaw.json.patch.template"
json_check "$PACK/answers.example.json"
json_check "$PACK/skills/manifest.json"
json_check "$PACK/cron/jobs.patch.template"

# Ensure canonical root vault template exists and matches the pack manifest expectation.
for dir in $(cat "$PACK/vault/checks/expected-root-dirs.txt"); do
  test -d "$ROOT/vault-template/$dir" || {
    echo "missing canonical vault-template dir: $dir" >&2
    exit 1
  }
done

# Ensure pack does not contain obvious private runtime material.
PRIVATE_BRAIN_NAME='ZeYu-AI'
PRIVATE_BRAIN_NAME+='-Brain'
SECRET_PATTERN="(/Users/[A-Za-z0-9._-]+|${PRIVATE_BRAIN_NAME}|[0-9]{18,20}|discord[.]com/api/webhooks|sk-[A-Za-z0-9_-]{12,}|xoxb-|Bot [A-Za-z0-9._-]{20,})"
if grep -R -nE --exclude='smoke.sh' --exclude='scan-secrets.mjs' "$SECRET_PATTERN" "$PACK"; then
  echo "private or secret-looking material found in pack" >&2
  exit 1
fi

# Ensure cron templates are disabled by default.
python3 - "$PACK/cron/jobs.patch.template" <<'PY'
import json, sys
path = sys.argv[1]
data = json.load(open(path))
for job in data.get('jobs', []):
    if job.get('enabled') is not False:
        raise SystemExit(f"cron job must default disabled: {job.get('id')}")
PY

# Ensure forbidden OpenClaw top-level keys are not present in the patch template.
python3 - "$PACK/manifest.json" "$PACK/openclaw.json.patch.template" <<'PY'
import json, sys
manifest = json.load(open(sys.argv[1]))
patch = json.load(open(sys.argv[2]))
for key in manifest['configPatchScope']['forbiddenTopLevelKeys']:
    if key in patch:
        raise SystemExit(f"forbidden top-level key in openclaw patch template: {key}")
PY

# Exercise PR1b dry-run installer and preview verification for minimal and full profiles.
TMP_PREVIEW="${TMPDIR:-/tmp}/brain-os-pack-smoke-$$"
rm -rf "$TMP_PREVIEW"
bash "$PACK/install.sh" --check --answers "$PACK/tests/fixtures/answers.minimal.json" >/dev/null
bash "$PACK/install.sh" --dry-run --answers "$PACK/tests/fixtures/answers.minimal.json" --out "$TMP_PREVIEW/minimal" >/dev/null
bash "$PACK/verify.sh" "$TMP_PREVIEW/minimal" >/dev/null
bash "$PACK/install.sh" --dry-run --answers "$PACK/tests/fixtures/answers.full.json" --out "$TMP_PREVIEW/full" >/dev/null
bash "$PACK/verify.sh" "$TMP_PREVIEW/full" >/dev/null


# Conflict detection should block an existing same-id agent with different config.
CONFLICT_DIR="$TMP_PREVIEW/conflict"
mkdir -p "$CONFLICT_DIR"
printf '{"agents":{"list":[{"id":"main","workspace":"/already/there"}]}}
' > "$CONFLICT_DIR/existing-openclaw.json"
if node "$PACK/scripts/detect-openclaw-conflicts.mjs" --existing "$CONFLICT_DIR/existing-openclaw.json" --patch "$TMP_PREVIEW/minimal/openclaw.config-patch.json" --report "$CONFLICT_DIR/report.json" >/dev/null 2>&1; then
  echo "expected conflict detection to fail" >&2
  exit 1
fi
python3 - <<PY
import json
r=json.load(open('$CONFLICT_DIR/report.json'))
assert r['ok'] is False
assert any(b['type']=='agent' and b['id']=='main' for b in r['blockers'])
PY

# Exercise safe apply and rollback against an isolated temp OpenClaw root.
APPLY_ROOT="/tmp/brain-os-pack-apply-smoke"
rm -rf "$APPLY_ROOT"
mkdir -p "$APPLY_ROOT/.openclaw/cron"
printf '{"agents":{"list":[]},"bindings":[]}
' > "$APPLY_ROOT/.openclaw/openclaw.json"
printf '{"jobs":[]}
' > "$APPLY_ROOT/.openclaw/cron/jobs.json"
bash "$PACK/install.sh" --apply --yes --answers "$PACK/tests/fixtures/answers.apply.json" --out "$TMP_PREVIEW/apply" >/dev/null
test -f "$APPLY_ROOT/.openclaw/openclaw.json"
test -f "$APPLY_ROOT/.openclaw/cron/jobs.json"
test -f "$APPLY_ROOT/.openclaw/agents/main/agent/AGENTS.md"
test -d "$APPLY_ROOT/BrainOS-Vault/00-INBOX"
OPENCLAW_ROOT="$APPLY_ROOT/.openclaw" bash "$PACK/rollback.sh" >/dev/null
rm -rf "$APPLY_ROOT"
rm -rf "$TMP_PREVIEW"

echo "pack smoke ok"
