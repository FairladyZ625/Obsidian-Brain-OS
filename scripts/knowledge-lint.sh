#!/usr/bin/env bash
# knowledge-lint.sh — content-level health check for a Brain vault
# Usage: ./scripts/knowledge-lint.sh [BRAIN_ROOT] [TARGET_DATE]

set -euo pipefail

BRAIN_ROOT="${1:-${BRAIN_ROOT:-$HOME/my-brain}}"
DOMAINS_DIR="$BRAIN_ROOT/03-KNOWLEDGE/01-READING/01-DOMAINS"
WORKING_DIR="$BRAIN_ROOT/03-KNOWLEDGE/02-WORKING"
INDEXES_DIR="$BRAIN_ROOT/03-KNOWLEDGE/06-INDEXES"
REVIEWS_DIR="$BRAIN_ROOT/12-REVIEWS/KNOWLEDGEBASE"
DATE=$(date +%Y-%m-%d)
TARGET_DATE="${2:-$(date -v-1d +%Y-%m-%d 2>/dev/null || date -d 'yesterday' +%Y-%m-%d)}"
RUN_REPORT_DIR="$BRAIN_ROOT/03-KNOWLEDGE/99-SYSTEM/03-INTEGRATION-REPORTS/run-reports/$TARGET_DATE"
RUN_REPORT="$RUN_REPORT_DIR/knowledge-lint-$TARGET_DATE.md"
REPORT="$REVIEWS_DIR/lint-$DATE.md"

mkdir -p "$REVIEWS_DIR" "$RUN_REPORT_DIR"

PROJECT_REGISTRY_TSV=$(mktemp)
trap 'rm -f "$PROJECT_REGISTRY_TSV"' EXIT

python3 - "$BRAIN_ROOT" > "$PROJECT_REGISTRY_TSV" <<'PYEOF'
import re, sys
from pathlib import Path

brain_root = Path(sys.argv[1])
projects_dir = brain_root / "05-PROJECTS"

for brief in projects_dir.rglob("project-brief.md"):
    text = brief.read_text(encoding="utf-8")
    if not text.startswith("---"):
        continue
    parts = text.split("---", 2)
    if len(parts) < 3:
        continue
    fm = parts[1]
    m = re.search(r'^project_ref:\s*"?([^"\n]+)"?\s*$', fm, re.MULTILINE)
    if not m:
        continue
    canonical = m.group(1).strip()
    aliases = {canonical, canonical.lower(), brief.parent.name, brief.parent.name.lower()}

    m_name = re.search(r'^project_name:\s*"?([^"\n]+)"?\s*$', fm, re.MULTILINE)
    if m_name:
        name = m_name.group(1).strip()
        aliases.add(name)
        aliases.add(name.lower())

    lines = fm.splitlines()
    in_aliases = False
    for line in lines:
        if re.match(r'^aliases:\s*$', line):
            in_aliases = True
            continue
        if in_aliases:
            m_alias = re.match(r'^\s*-\s+(.+?)\s*$', line)
            if m_alias:
                alias = m_alias.group(1).strip().strip('"')
                aliases.add(alias)
                aliases.add(alias.lower())
                continue
            if line.strip() and not line.startswith(' '):
                in_aliases = False

    for alias in sorted(aliases):
        print(f"{alias}\t{canonical}")
PYEOF

RED=0
YELLOW=0
BLUE=0
RED_CONTENT=""
YELLOW_CONTENT=""
BLUE_CONTENT=""

echo "🔍 Knowledge Lint start..."
echo "   Brain root: $BRAIN_ROOT"
echo "   Scan roots: $DOMAINS_DIR | $WORKING_DIR"
echo ""

resolve_project_ref() {
  local key="$1"
  awk -F '\t' -v key="$key" '$1 == key {print $2; exit}' "$PROJECT_REGISTRY_TSV"
}

scan_note_roots() {
  for dir in "$DOMAINS_DIR" "$WORKING_DIR"; do
    [ -d "$dir" ] || continue
    find "$dir" -name "*.md" -not -name "*.template.md" -print0
  done
}

echo "  [A] Required frontmatter fields..."
A_ISSUES=""
REQUIRED_FIELDS=("title" "status" "created" "tags")
while IFS= read -r -d '' f; do
  FNAME=$(basename "$f" .md)
  for field in "${REQUIRED_FIELDS[@]}"; do
    if ! grep -q "^${field}:" "$f" 2>/dev/null; then
      A_ISSUES="$A_ISSUES\n- [[${FNAME}]] — missing \`${field}\`"
      RED=$((RED + 1))
    fi
  done
  if ! grep -qE "^(source|source_type|source_url):" "$f" 2>/dev/null; then
    A_ISSUES="$A_ISSUES\n- [[${FNAME}]] — missing source-related field"
    RED=$((RED + 1))
  fi
done < <(scan_note_roots)
[ -n "$A_ISSUES" ] && RED_CONTENT="$RED_CONTENT\n### [Check A] Missing required fields\n$A_ISSUES\n"

echo "  [P] project_ref validity..."
P_ISSUES=""
while IFS= read -r -d '' f; do
  FNAME=$(basename "$f" .md)
  PROJECT_REF=$(grep "^project_ref:" "$f" 2>/dev/null | head -1 | sed 's/^project_ref:[[:space:]]*//' | tr -d '"' || true)
  if [ -n "$PROJECT_REF" ]; then
    CANONICAL_REF=$(resolve_project_ref "$PROJECT_REF")
    if [ -z "$CANONICAL_REF" ]; then
      P_ISSUES="$P_ISSUES\n- [[${FNAME}]] — project_ref: ${PROJECT_REF} not registered in 05-PROJECTS"
      YELLOW=$((YELLOW + 1))
    elif [ "$CANONICAL_REF" != "$PROJECT_REF" ]; then
      P_ISSUES="$P_ISSUES\n- [[${FNAME}]] — project_ref: ${PROJECT_REF} is not canonical, suggest ${CANONICAL_REF}"
      YELLOW=$((YELLOW + 1))
    fi
  fi
done < <(scan_note_roots)
[ -n "$P_ISSUES" ] && YELLOW_CONTENT="$YELLOW_CONTENT\n### [Check P] project_ref validity\n$P_ISSUES\n"

echo "  [RP] related_projects validity..."
RP_ISSUES=$(python3 - "$BRAIN_ROOT" "$PROJECT_REGISTRY_TSV" <<'PYEOF'
import re, sys
from pathlib import Path

brain_root = Path(sys.argv[1])
registry_tsv = Path(sys.argv[2])
valid = set()
for line in registry_tsv.read_text(encoding='utf-8').splitlines():
    alias, canonical = line.split('\t', 1)
    valid.add(canonical.strip())

scan_roots = [
    brain_root / '03-KNOWLEDGE/01-READING',
    brain_root / '03-KNOWLEDGE/02-WORKING',
]

for root in scan_roots:
    if not root.exists():
        continue
    for path in root.rglob('*.md'):
        text = path.read_text(encoding='utf-8')
        if not text.startswith('---\n'):
            continue
        parts = text.split('---\n', 2)
        if len(parts) < 3:
            continue
        fm = parts[1]
        lines = fm.splitlines()
        in_block = False
        refs = []
        for line in lines:
            if not in_block and re.match(r'^related_projects:\s*$', line):
                in_block = True
                continue
            if in_block:
                m = re.match(r'^\s*-\s+(.+?)\s*$', line)
                if m:
                    refs.append(m.group(1).strip().strip('"'))
                    continue
                if line.strip() and not line.startswith(' '):
                    break
        for ref in refs:
            if ref not in valid:
                print(f"- [[{path.stem}]] — related_projects: {ref} not registered in 05-PROJECTS")
PYEOF
)
if [ -n "$RP_ISSUES" ]; then
  RP_COUNT=$(printf "%s\n" "$RP_ISSUES" | grep -c '^-' || true)
  YELLOW=$((YELLOW + RP_COUNT))
  YELLOW_CONTENT="$YELLOW_CONTENT\n### [Check RP] related_projects validity\n$RP_ISSUES\n"
fi

echo "  [PK] project-side knowledge paths..."
PK_ISSUES=$(python3 - "$BRAIN_ROOT" <<'PYEOF'
import re, sys
from pathlib import Path

brain_root = Path(sys.argv[1])
files = [brain_root / '05-PROJECTS/projects-index.md'] + list((brain_root / '05-PROJECTS').rglob('project-brief.md'))
for path in files:
    if not path.exists():
        continue
    text = path.read_text(encoding='utf-8')
    for raw in re.findall(r'`(03-KNOWLEDGE/[^`]+\.md)`', text):
        if not (brain_root / raw).exists():
            print(f"- `{path.relative_to(brain_root).as_posix()}` → `{raw}` does not exist")
PYEOF
)
if [ -n "$PK_ISSUES" ]; then
  PK_COUNT=$(printf "%s\n" "$PK_ISSUES" | grep -c '^-' || true)
  YELLOW=$((YELLOW + PK_COUNT))
  YELLOW_CONTENT="$YELLOW_CONTENT\n### [Check PK] project-side knowledge path validity\n$PK_ISSUES\n"
fi

echo "  [E] orphan candidate pages..."
E_ISSUES=""
SEARCH_SCOPE="$INDEXES_DIR $DOMAINS_DIR"
if [ -d "$DOMAINS_DIR" ]; then
  while IFS= read -r -d '' f; do
    FNAME=$(basename "$f" .md)
    REF_COUNT=$(grep -rl "\[\[${FNAME}\]\]" $SEARCH_SCOPE 2>/dev/null | grep -v "^${f}$" | wc -l | xargs echo 2>/dev/null || echo "0")
    REF_COUNT=$(echo "$REF_COUNT" | tr -d '[:space:]')
    if [[ "$REF_COUNT" =~ ^[0-9]+$ ]] && [ "$REF_COUNT" -eq 0 ]; then
      E_ISSUES="$E_ISSUES\n- [[${FNAME}]] — not referenced by indexes or domains"
      BLUE=$((BLUE + 1))
    fi
  done < <(find "$DOMAINS_DIR" -not -path "*/Article-Notes/*" -name "*.md" -not -name "*.template.md" -print0 2>/dev/null)
fi
[ -n "$E_ISSUES" ] && BLUE_CONTENT="$BLUE_CONTENT\n### [Check E] orphan page candidates\n$E_ISSUES\n"

STATUS="healthy"
if [ "$RED" -gt 0 ]; then
  STATUS="needs-attention"
elif [ "$YELLOW" -gt 0 ]; then
  STATUS="warning"
fi

cat > "$REPORT" <<EOF
# Knowledge Lint Report — $DATE

status: $STATUS
red: $RED
yellow: $YELLOW
blue: $BLUE

## Summary
- red: $RED
- yellow: $YELLOW
- blue: $BLUE
$RED_CONTENT
$YELLOW_CONTENT
$BLUE_CONTENT
EOF

cat > "$RUN_REPORT" <<EOF
# Knowledge Lint Run Report — $TARGET_DATE

status: $STATUS
red: $RED
yellow: $YELLOW
blue: $BLUE
report: ${REPORT#$BRAIN_ROOT/}

## Summary
- red: $RED
- yellow: $YELLOW
- blue: $BLUE
- review report: `${REPORT#$BRAIN_ROOT/}`
$RED_CONTENT
$YELLOW_CONTENT
$BLUE_CONTENT
EOF

echo ""
echo "✅ Knowledge Lint complete"
echo "   status: $STATUS"
echo "   red: $RED | yellow: $YELLOW | blue: $BLUE"
echo "   report: $REPORT"
echo "   run-report: $RUN_REPORT"
