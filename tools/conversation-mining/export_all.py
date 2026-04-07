#!/usr/bin/env python3
"""
export_all.py - Unified AI conversation exporter
Usage: python3 export_all.py [--date YYYY-MM-DD] [--days N]
"""

import argparse
import hashlib
import json
import re
import sys
from datetime import datetime, timedelta
from pathlib import Path

SKILL_DIR = Path(__file__).parent
sys.path.insert(0, str(SKILL_DIR))

from lib.transcript_export import (  # noqa: E402
    build_search_entry,
    humanize_title_fragment,
    render_transcript_markdown,
    sanitize_filename,
    unique_markdown_path,
)

CLAUDE_DIR = Path.home() / ".claude"
OUTPUT_BASE = CLAUDE_DIR / "exported_conversations"
INDEX_FILE = OUTPUT_BASE / "conversations.json"
PREFERRED_MARKDOWN_DIR = Path("{{TRANSCRIPT_DIR}}")
MARKDOWN_DIR = PREFERRED_MARKDOWN_DIR if PREFERRED_MARKDOWN_DIR.parent.exists() else OUTPUT_BASE / "transcripts"


_CONTROL_CHAR_RE = re.compile(r"[\x00-\x08\x0b-\x1f\x7f]")


def load_index() -> dict:
    if INDEX_FILE.exists():
        try:
            with open(INDEX_FILE, encoding="utf-8") as handle:
                return json.load(handle)
        except Exception:
            pass
    return {"generated_at": "", "conversations": []}


def save_index(index: dict):
    OUTPUT_BASE.mkdir(parents=True, exist_ok=True)
    index["generated_at"] = datetime.now().isoformat()
    with open(INDEX_FILE, "w", encoding="utf-8") as handle:
        json.dump(index, handle, ensure_ascii=False, indent=2)


def get_existing_ids(index: dict) -> set:
    return {f"{conversation.get('source')}::{conversation.get('session_id')}" for conversation in index.get("conversations", [])}


def _preserve_existing_fields(existing: dict, conversation: dict) -> dict:
    for key in ("transcript_path", "transcript_rel_path"):
        if key not in conversation and existing.get(key):
            conversation[key] = existing[key]
    return conversation


def _clean_metadata_text(value) -> str:
    text = str(value or "")
    text = _CONTROL_CHAR_RE.sub("", text)
    return text.strip()


def _normalize_project_metadata(value) -> str:
    text = _clean_metadata_text(value)
    if not text:
        return ""
    text = text.replace("file://", "")
    project_match = re.search(r"(/Users/[^/\s]+/Projects/[^/\s)]+)", text)
    if project_match:
        return project_match.group(1)
    return text


def _sanitize_conversation_metadata(conversation: dict) -> dict:
    cleaned = dict(conversation)
    for key in (
        "id",
        "source",
        "date",
        "title",
        "project",
        "session_id",
        "file",
        "first_ts",
        "parent_session_id",
        "launch_prompt",
        "subagent_summary",
        "brain_dir",
        "transcript_path",
        "transcript_rel_path",
    ):
        if key in cleaned:
            if key == "project":
                cleaned[key] = _normalize_project_metadata(cleaned.get(key))
            else:
                cleaned[key] = _clean_metadata_text(cleaned.get(key))
    artifacts = []
    for artifact in cleaned.get("artifacts", []) or []:
        if not isinstance(artifact, dict):
            continue
        artifact_copy = dict(artifact)
        for field in ("name", "title", "path", "rel_path", "artifact_type", "updated_at"):
            if field in artifact_copy:
                artifact_copy[field] = _clean_metadata_text(artifact_copy.get(field))
        artifacts.append(artifact_copy)
    if "artifacts" in cleaned:
        cleaned["artifacts"] = artifacts
    return cleaned


def _sanitize_index_metadata(index: dict) -> None:
    index["conversations"] = [
        _sanitize_conversation_metadata(conversation)
        for conversation in index.get("conversations", [])
        if isinstance(conversation, dict)
    ]


def _content_hash(conversation: dict) -> str:
    """基于 messages 生成内容哈希，用于判断会话是否有变化"""
    msgs = conversation.get("messages", [])
    if not msgs:
        return ""
    last_text = msgs[-1].get("text", "")[:200] if msgs else ""
    raw = f"{len(msgs)}:{last_text}"
    return hashlib.md5(raw.encode()).hexdigest()[:12]


def upsert_conversation(index: dict, conversation: dict) -> bool:
    """插入或更新会话。返回 True 表示内容有变化（需要重新 materialize），False 表示未变化。"""
    conversations = index.setdefault("conversations", [])
    conversation = _sanitize_conversation_metadata(conversation)
    new_hash = _content_hash(conversation)
    conversation["_content_hash"] = new_hash
    for index_pos, existing in enumerate(conversations):
        if existing.get("source") == conversation.get("source") and existing.get("session_id") == conversation.get("session_id"):
            old_hash = existing.get("_content_hash", "")
            is_dirty = old_hash != new_hash
            conversation["_dirty"] = is_dirty
            conversations[index_pos] = _preserve_existing_fields(existing, conversation)
            return is_dirty
    conversation["_dirty"] = True
    conversations.append(conversation)
    return True


def find_existing_conversation(index: dict, source: str, session_id: str) -> dict | None:
    for existing in index.get("conversations", []):
        if existing.get("source") == source and existing.get("session_id") == session_id:
            return existing
    return None


def make_conv_id(source: str, date: str, session_id: str) -> str:
    digest = hashlib.md5(session_id.encode()).hexdigest()[:8]
    return f"{source}-{date.replace('-', '')}-{digest}"


def _default_markdown_dir() -> Path:
    if PREFERRED_MARKDOWN_DIR.parent.exists():
        return PREFERRED_MARKDOWN_DIR
    return OUTPUT_BASE / "transcripts"


def _build_transcript_stem(conversation: dict) -> str:
    source = str(conversation.get("source", "conv"))
    if conversation.get("is_subagent"):
        source += "_subagent"
    project = str(conversation.get("project", "")).strip("/").split("/")[-1] if conversation.get("project") else ""
    title = humanize_title_fragment(conversation.get("title") or "", max_chars=52) or conversation.get("session_id", "")[:12]
    parts = [source]
    if project:
        parts.append(project)
    parts.append(title)
    return sanitize_filename("_".join(part for part in parts if part), max_len=100)


def materialize_transcripts(index: dict, markdown_dir: Path, dirty_ids: set[str] | None = None):
    """Materialize transcript markdown files.

    Args:
        dirty_ids: 如果非 None，只重写这些 id 对应的 transcript。
                   未变化的会话直接复用已有 transcript_path。
    """
    markdown_dir.mkdir(parents=True, exist_ok=True)
    conversations = list(index.get("conversations", []))
    used_paths: set[str] = set()

    for conversation in sorted(conversations, key=lambda item: (item.get("date", ""), item.get("source", ""), item.get("title", ""))):
        conv_id = conversation.get("id", "")
        is_dirty = dirty_ids is None or conv_id in dirty_ids

        # 已有 transcript_path 且未变化 → 直接复用
        existing_path = conversation.get("transcript_path")
        if existing_path and Path(existing_path).exists() and not is_dirty:
            used_paths.add(str(existing_path))
            continue

        date_dir = markdown_dir / (conversation.get("date") or "unknown-date")
        transcript_path = ""
        if existing_path:
            existing_candidate = Path(existing_path)
            try:
                existing_candidate.relative_to(markdown_dir)
                existing_name = existing_candidate.name
                if "_Users_" not in existing_name and "https___" not in existing_name and len(existing_name) <= 120:
                    transcript_path = str(existing_candidate)
            except Exception:
                transcript_path = ""
        if transcript_path:
            used_paths.add(transcript_path)
            out_path = Path(transcript_path)
        else:
            out_path = unique_markdown_path(date_dir, _build_transcript_stem(conversation), used_paths)

        content = render_transcript_markdown(conversation, conversations)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        with open(out_path, "w", encoding="utf-8") as handle:
            handle.write(content)

        conversation["transcript_path"] = str(out_path)
        conversation["transcript_rel_path"] = str(out_path.relative_to(markdown_dir))


def export_claude(date_str: str, existing_ids: set, index: dict) -> int:
    try:
        from lib.extract_claude import (
            _extract_subagent_summary,
            decode_project_name,
            extract_conversation,
            find_sessions_by_date,
        )
    except ImportError as error:
        print(f"  [Claude] Import error: {error}")
        return 0

    sessions = find_sessions_by_date(date_str)
    exported = 0

    for session in sorted(sessions, key=lambda item: item.get("first_ts", "")):
        session_id = session["session_id"]
        existing_key = f"claude::{session_id}"
        if existing_key in existing_ids:
            continue
        messages = extract_conversation(session["filepath"], target_date=date_str)
        if not messages:
            continue

        first_user = next((message["text"][:40] for message in messages if message["role"] == "user"), "")
        first_user_full = next((message["text"] for message in messages if message["role"] == "user"), "")
        subagent_summary = _extract_subagent_summary(first_user_full) if session.get("is_subagent") else ""
        title = subagent_summary or first_user or session_id[:40]
        upsert_conversation(index, {
            "id": make_conv_id("claude", date_str, session_id),
            "source": "claude",
            "date": date_str,
            "title": title,
            "project": decode_project_name(session.get("project", "")),
            "session_id": session_id,
            "first_ts": session.get("first_ts", ""),
            "is_subagent": bool(session.get("is_subagent")),
            "parent_session_id": session.get("parent_session_id", ""),
            "launch_prompt": first_user_full if session.get("is_subagent") else "",
            "subagent_summary": subagent_summary,
            "user_msg_count": sum(1 for message in messages if message["role"] == "user"),
            "assistant_msg_count": sum(1 for message in messages if message["role"] == "assistant"),
            "messages": [
                {
                    "role": message["role"],
                    "text": message["text"],
                    **({"prompt": message.get("prompt", "")} if message.get("prompt") else {}),
                    **({"description": message.get("description", "")} if message.get("description") else {}),
                    **({"tool_use_id": message.get("tool_use_id", "")} if message.get("tool_use_id") else {}),
                }
                for message in messages
            ],
        })
        existing_ids.add(existing_key)
        exported += 1
        print(f"    ✓ [Claude] {title[:60]}")

    return exported


def export_codex(date_str: str, existing_ids: set, index: dict) -> int:
    try:
        from lib.extract_codex import extract_conversation, find_sessions_by_date, load_thread_titles
    except ImportError as error:
        print(f"  [Codex] Import error: {error}")
        return 0

    titles = load_thread_titles()
    sessions = find_sessions_by_date(date_str)
    exported = 0

    for session_id, filepath in sorted(sessions.items()):
        existing_key = f"codex::{session_id}"
        if existing_key in existing_ids:
            continue
        messages, meta = extract_conversation(filepath)
        if not messages:
            continue

        title = titles.get(session_id, "")
        display_title = title or (messages[0]["text"][:50] if messages else session_id[:40])
        upsert_conversation(index, {
            "id": make_conv_id("codex", date_str, session_id),
            "source": "codex",
            "date": date_str,
            "title": display_title,
            "project": meta.get("cwd", "") if meta else "",
            "session_id": session_id,
            "user_msg_count": sum(1 for message in messages if message["role"] == "user"),
            "assistant_msg_count": sum(1 for message in messages if message["role"] == "assistant"),
            "messages": [{"role": message["role"], "text": message["text"]} for message in messages],
        })
        existing_ids.add(existing_key)
        exported += 1
        print(f"    ✓ [Codex] {display_title[:60]}")

    return exported


def export_antigravity(date_str: str, existing_ids: set, index: dict) -> int:
    try:
        from lib.extract_antigravity import find_sessions
    except ImportError as error:
        print(f"  [AG] Import error: {error}")
        return 0

    sessions = find_sessions(date_str)
    exported = 0

    for session in sessions:
        session_id = session["session_id"]
        existing_key = f"antigravity::{session_id}"
        if existing_key in existing_ids:
            continue
        messages = session.get("messages", [])
        title = session.get("title", session_id[:40])
        upsert_conversation(index, {
            "id": make_conv_id("ag", date_str, session_id),
            "source": "antigravity",
            "date": date_str,
            "title": title,
            "project": session.get("project", ""),
            "session_id": session_id,
            "brain_dir": session.get("brain_dir", ""),
            "artifacts": session.get("artifacts", []),
            "user_msg_count": sum(1 for message in messages if message["role"] == "user"),
            "assistant_msg_count": sum(1 for message in messages if message["role"] == "assistant"),
            "messages": messages,
        })
        existing_ids.add(existing_key)
        exported += 1
        print(f"    ✓ [AG] {title[:60]}")

    return exported


def _build_search_index(index: dict):
    """导出时生成轻量搜索索引 search_index.json"""
    search_file = OUTPUT_BASE / "search_index.json"
    conversations = index.get("conversations", [])
    entries = []
    for conv in conversations:
        entry = build_search_entry(conv)
        if entry:
            entries.append(entry)
    search_data = {
        "version": 1,
        "generated_at": datetime.now().isoformat(),
        "count": len(entries),
        "entries": entries,
    }
    with open(search_file, "w", encoding="utf-8") as f:
        json.dump(search_data, f, ensure_ascii=False, indent=2)
    print(f"  搜索索引: {search_file} ({len(entries)} entries)")


def main():
    global OUTPUT_BASE, INDEX_FILE, MARKDOWN_DIR
    parser = argparse.ArgumentParser(description="Export AI conversations")
    parser.add_argument("--date", help="Date to export (YYYY-MM-DD), default: today")
    parser.add_argument("--days", type=int, default=1, help="Number of past days to export")
    parser.add_argument("--output-dir", help=f"Directory for JSON/viewer export data (default: {OUTPUT_BASE})")
    parser.add_argument("--markdown-dir", help=f"Directory for human-readable markdown transcripts (default: {_default_markdown_dir()})")
    parser.add_argument("--clean", action="store_true", help="Remove orphaned transcript files not in conversations.json")
    args = parser.parse_args()

    if args.output_dir:
        OUTPUT_BASE = Path(args.output_dir).expanduser().resolve()
        INDEX_FILE = OUTPUT_BASE / "conversations.json"
    MARKDOWN_DIR = Path(args.markdown_dir).expanduser() if args.markdown_dir else _default_markdown_dir()

    if args.date:
        try:
            start_date = datetime.strptime(args.date, "%Y-%m-%d")
        except ValueError:
            print(f"Invalid date: {args.date}")
            sys.exit(1)
    else:
        start_date = datetime.now()

    dates = [(start_date - timedelta(days=offset)).strftime("%Y-%m-%d") for offset in range(args.days)]

    print("=" * 50)
    print("  AI 对话统一导出工具")
    print("=" * 50)

    index = load_index()
    existing_ids = get_existing_ids(index)
    print(f"  已有 {len(existing_ids)} 个会话记录")
    print(f"  Markdown transcript dir: {MARKDOWN_DIR}\n")

    dirty_ids: set[str] = set()
    total = 0
    for index_pos, date_str in enumerate(dates):
        print(f"📅 {date_str}")
        total += export_claude(date_str, existing_ids, index)
        total += export_codex(date_str, existing_ids, index)
        if index_pos == 0:
            total += export_antigravity(date_str, existing_ids, index)

    # Collect dirty IDs (conversations that changed or are new)
    for conv in index.get("conversations", []):
        if conv.get("_dirty"):
            dirty_ids.add(conv.get("id", ""))
            del conv["_dirty"]

    _sanitize_index_metadata(index)

    # --clean: remove orphaned transcript files
    if args.clean:
        valid_paths = {c.get("transcript_path") for c in index.get("conversations", []) if c.get("transcript_path")}
        removed = 0
        for md_file in MARKDOWN_DIR.rglob("*.md"):
            if str(md_file) not in valid_paths:
                md_file.unlink()
                removed += 1
                print(f"  清理孤立文件: {md_file.name}")
        print(f"  清理完成: 删除 {removed} 个孤立文件\n")

    materialize_transcripts(index, MARKDOWN_DIR, dirty_ids or None)
    save_index(index)

    # Generate search index
    _build_search_index(index)

    print(f"\n{'=' * 40}")
    print(f"  新增: {total} 个会话")
    print(f"  总计: {len(index['conversations'])} 个会话")
    print(f"  索引: {INDEX_FILE}")
    print(f"  Markdown: {MARKDOWN_DIR}")
    print(f"{'=' * 40}")


if __name__ == "__main__":
    main()
