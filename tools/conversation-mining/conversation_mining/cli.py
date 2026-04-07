#!/usr/bin/env python3
"""
conversation_mining.cli - export local AI conversations and build a static viewer
"""

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

PACKAGE_ROOT = Path(__file__).resolve().parent
REPO_ROOT = PACKAGE_ROOT.parent
EXPORT_ALL = REPO_ROOT / "export_all.py"
VIEWER_TEMPLATE = PACKAGE_ROOT / "viewer.html"
DEFAULT_OUTPUT_BASE = REPO_ROOT / "exported_conversations"


def _json_for_html_script(value) -> str:
    text = json.dumps(value, ensure_ascii=False)
    return text.replace("</", "<\\/")


def run_export(days: int, date: str | None, output_dir: Path, markdown_dir: str | None) -> bool:
    cmd = [sys.executable, str(EXPORT_ALL), "--output-dir", str(output_dir)]
    if date:
        cmd += ["--date", date]
    if days > 1:
        cmd += ["--days", str(days)]
    if markdown_dir:
        cmd += ["--markdown-dir", markdown_dir]
    result = subprocess.run(cmd, cwd=str(REPO_ROOT))
    return result.returncode == 0


def build_html(output_dir: Path) -> bool:
    conversations_json = output_dir / "conversations.json"
    index_html = output_dir / "index.html"
    if not VIEWER_TEMPLATE.exists():
        print(f"Error: viewer template not found at {VIEWER_TEMPLATE}")
        return False
    if not conversations_json.exists():
        print(f"Error: conversations.json not found at {conversations_json}")
        return False

    html = VIEWER_TEMPLATE.read_text(encoding="utf-8")
    data = json.loads(conversations_json.read_text(encoding="utf-8"))

    index = []
    messages_map = {}
    for conv in data.get("conversations", []):
        conv_id = conv.get("id", "")
        messages = conv.get("messages", [])
        if messages:
            messages_map[conv_id] = messages
        index.append({key: value for key, value in conv.items() if key != "messages"})

    html = html.replace(
        '<script type="application/json" id="conv-index">[]</script>',
        f'<script type="application/json" id="conv-index">{_json_for_html_script(index)}</script>',
    )
    html = html.replace(
        '<script type="application/json" id="conv-messages">{}</script>',
        f'<script type="application/json" id="conv-messages">{_json_for_html_script(messages_map)}</script>',
    )

    output_dir.mkdir(parents=True, exist_ok=True)
    index_html.write_text(html, encoding="utf-8")
    return True


def main():
    parser = argparse.ArgumentParser(description="Export AI conversations and build the static viewer")
    parser.add_argument("--days", type=int, default=1, help="Number of past days to export (default: 1)")
    parser.add_argument("--date", help="Specific date to export (YYYY-MM-DD)")
    parser.add_argument(
        "--output-dir",
        default=str(DEFAULT_OUTPUT_BASE),
        help=f"Directory for exported data (default: {DEFAULT_OUTPUT_BASE})",
    )
    parser.add_argument("--markdown-dir", help="Directory for human-readable markdown transcripts")
    parser.add_argument("--no-open", action="store_true", help="Build the viewer without opening it")
    args = parser.parse_args()

    output_dir = Path(args.output_dir).expanduser().resolve()

    print("Exporting conversations...")
    ok = run_export(args.days, args.date, output_dir, args.markdown_dir)
    if not ok:
        print("Export finished with errors; continuing to build the viewer.")

    print("Building viewer...")
    if not build_html(output_dir):
        sys.exit(1)

    conversations_json = output_dir / "conversations.json"
    total = 0
    if conversations_json.exists():
        total = len(json.loads(conversations_json.read_text(encoding="utf-8")).get("conversations", []))

    index_html = output_dir / "index.html"
    print(f"Done: {total} conversations -> {index_html}")

    if not args.no_open:
        os.system(f'open "{index_html}"')
