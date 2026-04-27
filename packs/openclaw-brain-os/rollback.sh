#!/usr/bin/env bash
set -euo pipefail

OPENCLAW_ROOT="${OPENCLAW_ROOT:-$HOME/.openclaw}"
INSTALL_STATE_DIR="${1:-}"
if [[ -z "$INSTALL_STATE_DIR" ]]; then
  LAST="$OPENCLAW_ROOT/.brain-os-pack-last-install.json"
  if [[ ! -f "$LAST" ]]; then
    echo "No install state provided and no last-install marker found: $LAST" >&2
    exit 2
  fi
  INSTALL_STATE_DIR="$(python3 - <<PY
import json
print(json.load(open('$LAST'))['installStateDir'])
PY
)"
fi
STATE="$INSTALL_STATE_DIR/install-state.json"
if [[ ! -f "$STATE" ]]; then
  echo "Install state not found: $STATE" >&2
  exit 2
fi
python3 - <<PY
import json, os, shutil
state=json.load(open('$STATE'))
root=state['paths']['openclawRoot']
backup=state['backupDir']
restored=[]
for rel in ['openclaw.json','jobs.json']:
    src=os.path.join(backup, rel)
    if rel == 'jobs.json':
        dest=os.path.join(root,'cron','jobs.json')
    else:
        dest=os.path.join(root,rel)
    if os.path.exists(src):
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        shutil.copy2(src,dest)
        restored.append(dest)
print(json.dumps({'ok': True, 'restored': restored, 'note': 'Workspace, skills, and vault files are not deleted automatically.'}, indent=2))
PY
