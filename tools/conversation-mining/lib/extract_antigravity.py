#!/usr/bin/env python3
"""
AntiGravity (VS Code fork) conversation extractor.

Primary source:
- antigravityUnifiedStateSync.trajectorySummaries

The value is a base64-wrapped protobuf blob that itself contains nested
base64 payloads. Those nested payloads expose readable session titles,
session ids, workspace paths, and often assistant-facing summaries
(`Message`, `TaskSummary`, `TaskStatus`, `TaskName`).

Fallback source:
- jetskiStateSync.agentManagerInitState

That fallback only covers the current in-memory agent manager state, so it is
best-effort only and should not be treated as the authoritative history store.
"""
import base64
import json
import re
import sqlite3
from datetime import datetime
from pathlib import Path

AG_DB = Path.home() / "Library/Application Support/Antigravity/User/globalStorage/state.vscdb"
BRAIN_ROOT = Path.home() / ".gemini/antigravity/brain"
TRAJ_KEY = "antigravityUnifiedStateSync.trajectorySummaries"
JETSKI_KEY = "jetskiStateSync.agentManagerInitState"
NESTED_B64_PATTERN = re.compile(r"[A-Za-z0-9+/]{80,}={0,2}")
UUID_PATTERN = re.compile(r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}")
FILE_URI_PATTERN = re.compile(r"file:///[^\s\"'`]+")
UUIDISH_TITLE_PATTERN = re.compile(r"^[0-9a-f]{8}-[0-9a-f]{3,}$")
ARTIFACT_EXTENSIONS = {".md", ".txt", ".png", ".jpg", ".jpeg", ".webp"}
ARTIFACT_IGNORE_PARTS = {".tempmediaStorage", "node_modules"}


def _decode_value(raw: str) -> bytes:
    try:
        return base64.b64decode(raw.strip())
    except Exception:
        return b""


def _clean_text(text: str) -> str:
    text = text.replace("\x00", " ")
    text = text.replace("\ufffd", " ")
    text = re.sub(r"[\x01-\x08\x0b-\x1f\x7f]", " ", text)
    text = re.sub(r"\s+\n", "\n", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = re.sub(r"[ \t]{2,}", " ", text)
    return text.strip()


def _looks_human_readable(text: str) -> bool:
    if not text or len(text) < 4:
        return False
    printable = sum(1 for c in text if c.isprintable() and ord(c) > 31)
    return printable / max(len(text), 1) > 0.8


def _extract_title(chunk_text: str, session_id: str) -> str:
    head = re.sub(r"^[\x00-\x20]+", "", chunk_text)
    head = re.split(r"[\x00-\x1f\x7f]", head, maxsplit=1)[0]
    uuid_match = UUID_PATTERN.search(head)
    if uuid_match:
        head = head[:uuid_match.start()]
    file_match = FILE_URI_PATTERN.search(head)
    if file_match:
        head = head[:file_match.start()]
    head = _clean_text(head).split("\n", 1)[0].strip()
    head = head.lstrip("$!#* ")
    head = head.strip(" :.-")
    if 4 <= len(head) <= 160 and _looks_human_readable(head):
        return head
    return session_id[:12]


def _is_poor_title(title: str) -> bool:
    if not title:
        return True
    if UUIDISH_TITLE_PATTERN.match(title):
        return True
    if title.startswith("/") or title.startswith("看 /Users") or title.startswith("/Users"):
        return True
    if len(title) < 6:
        return True
    return False


def _normalize_title_candidate(text: str) -> str:
    text = _clean_text(text)
    text = text.replace("**", "").replace("__", "").replace("`", "")
    text = re.sub(r"^[A-Za-z](?=[\u4e00-\u9fff])", "", text)
    text = text.lstrip("$!#*>-• ")
    text = text.strip(" :.-")
    if len(text) > 80:
        text = text[:80].rstrip()
    return text


def _title_from_messages(messages: list[dict], session_id: str) -> str:
    for msg in messages:
        text = _clean_text(msg.get("text", ""))
        if not text:
            continue
        for line in text.splitlines():
            candidate = _normalize_title_candidate(line)
            if not candidate or _is_poor_title(candidate):
                continue
            if _looks_human_readable(candidate):
                return candidate
    return session_id[:12]


def _extract_project(chunk_text: str) -> str:
    match = FILE_URI_PATTERN.search(chunk_text)
    if not match:
        return ""
    return match.group(0).replace("file://", "", 1)


def _extract_json_objects(chunk_text: str) -> list[dict]:
    decoder = json.JSONDecoder()
    objects: list[dict] = []
    i = 0
    while True:
        start = chunk_text.find("{", i)
        if start == -1:
            break
        try:
            parsed, end = decoder.raw_decode(chunk_text[start:])
        except json.JSONDecodeError:
            i = start + 1
            continue
        if isinstance(parsed, dict):
            objects.append(parsed)
        i = start + end
    return objects


def _append_message(messages: list[dict], role: str, text: str):
    cleaned = _clean_text(text)
    if not cleaned:
        return
    if messages and messages[-1]["role"] == role and messages[-1]["text"] == cleaned:
        return
    messages.append({"role": role, "text": cleaned})


def _extract_messages_from_chunk(chunk_text: str, title: str) -> list[dict]:
    messages: list[dict] = []
    for obj in _extract_json_objects(chunk_text):
        if isinstance(obj.get("TaskName"), str):
            lines = [obj["TaskName"]]
            if isinstance(obj.get("TaskStatus"), str) and obj["TaskStatus"].strip():
                lines.append(obj["TaskStatus"])
            _append_message(messages, "user", "\n\n".join(lines))
        if isinstance(obj.get("TaskSummary"), str):
            _append_message(messages, "assistant", obj["TaskSummary"])
        if isinstance(obj.get("Message"), str):
            _append_message(messages, "assistant", obj["Message"])

    if not messages:
        _append_message(messages, "user", title)
    return messages


def _extract_conversations_from_traj(decoded: bytes) -> list[dict]:
    outer_text = decoded.decode("utf-8", errors="replace")
    conversations = []
    seen = set()

    for match in NESTED_B64_PATTERN.finditer(outer_text):
        try:
            chunk_text = base64.b64decode(match.group()).decode("utf-8", errors="replace")
        except Exception:
            continue

        uuids = UUID_PATTERN.findall(chunk_text)
        if not uuids:
            continue
        session_id = uuids[0]
        if session_id in seen:
            continue
        seen.add(session_id)

        title = _extract_title(chunk_text, session_id)
        messages = _extract_messages_from_chunk(chunk_text, title)
        if _is_poor_title(title):
            title = _title_from_messages(messages, session_id)
        conversations.append({
            "session_id": session_id,
            "title": title,
            "project": _extract_project(chunk_text),
            "messages": messages,
        })

    return conversations


def _extract_messages_from_jetski(decoded: bytes) -> tuple[str, list[dict]]:
    """
    Extract conversation messages from jetski state (most recent conversation).
    Returns (session_id, messages).
    """
    text = decoded.decode("utf-8", errors="replace")
    uuids = UUID_PATTERN.findall(text)
    session_id = uuids[0] if uuids else "unknown"

    messages = []
    for line in text.split("\n"):
        stripped = line.strip()
        if len(stripped) < 5:
            continue
        if UUID_PATTERN.fullmatch(stripped):
            continue
        printable = sum(1 for c in stripped if c.isprintable() and ord(c) > 31)
        if printable / len(stripped) < 0.6:
            continue
        messages.append({"role": "user", "text": _clean_text(stripped)})

    return session_id, messages


def _safe_read_json(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}


def _extract_artifact_heading(path: Path) -> str:
    if path.suffix.lower() not in {".md", ".txt"} or not path.exists():
        return ""
    try:
        with path.open("r", encoding="utf-8") as handle:
            for _ in range(20):
                line = handle.readline()
                if not line:
                    break
                candidate = line.strip()
                if not candidate:
                    continue
                if candidate.startswith("#"):
                    candidate = candidate.lstrip("#").strip()
                candidate = _clean_text(candidate)
                if 4 <= len(candidate) <= 120:
                    return candidate
    except Exception:
        return ""
    return ""


def _artifact_priority(path: Path) -> tuple[int, int, str]:
    rel = path.relative_to(path.parents[1]) if len(path.parents) >= 2 else path
    rel_str = str(rel)
    name = path.name.lower()
    if name == "task.md":
        return (0, len(rel.parts), rel_str)
    if name == "implementation_plan.md":
        return (1, len(rel.parts), rel_str)
    if name == "walkthrough.md":
        return (2, len(rel.parts), rel_str)
    if name in {"handoff.md", "handoff_prompt.md", "handover_summary.md"}:
        return (3, len(rel.parts), rel_str)
    if path.suffix.lower() in {".md", ".txt"}:
        return (4, len(rel.parts), rel_str)
    return (5, len(rel.parts), rel_str)


def _collect_brain_artifacts(session_id: str) -> tuple[str, list[dict]]:
    brain_dir = BRAIN_ROOT / session_id
    if not brain_dir.exists() or not brain_dir.is_dir():
        return "", []

    candidates: list[Path] = []
    for path in brain_dir.rglob("*"):
        if not path.is_file():
            continue
        if any(part in ARTIFACT_IGNORE_PARTS for part in path.parts):
            continue
        if path.name.endswith(".metadata.json"):
            continue
        if ".resolved" in path.name:
            continue
        if path.suffix.lower() not in ARTIFACT_EXTENSIONS:
            continue
        candidates.append(path)

    candidates.sort(key=_artifact_priority)
    artifacts: list[dict] = []
    for path in candidates[:16]:
        metadata = _safe_read_json(path.parent / f"{path.name}.metadata.json")
        rel_path = str(path.relative_to(brain_dir))
        artifacts.append({
            "name": path.name,
            "title": metadata.get("summary") or _extract_artifact_heading(path) or path.stem,
            "path": str(path),
            "rel_path": rel_path,
            "artifact_type": metadata.get("artifactType", ""),
            "updated_at": metadata.get("updatedAt", ""),
        })

    return str(brain_dir), artifacts


def find_sessions(target_date: str | None = None) -> list[dict]:
    """
    Extract AntiGravity conversations from state.vscdb.
    Returns list of session dicts compatible with export_all.py.
    """
    if not AG_DB.exists():
        print(f"  [AG] DB not found: {AG_DB}")
        return []

    try:
        conn = sqlite3.connect(str(AG_DB))
        cur = conn.cursor()
        cur.execute("SELECT value FROM ItemTable WHERE key=?", (TRAJ_KEY,))
        row = cur.fetchone()
        traj_raw = row[0] if row else ""
        cur.execute("SELECT value FROM ItemTable WHERE key=?", (JETSKI_KEY,))
        row = cur.fetchone()
        jetski_raw = row[0] if row else ""
        conn.close()
    except Exception as e:
        print(f"  [AG] DB error: {e}")
        return []

    conversations = []
    if traj_raw:
        decoded = _decode_value(traj_raw)
        conversations = _extract_conversations_from_traj(decoded)

    jetski_messages: dict[str, list[dict]] = {}
    if jetski_raw:
        decoded = _decode_value(jetski_raw)
        sid, msgs = _extract_messages_from_jetski(decoded)
        if msgs:
            jetski_messages[sid] = msgs

    date_str = target_date or datetime.now().strftime("%Y-%m-%d")
    result = []
    for conv in conversations:
        sid = conv["session_id"]
        messages = list(conv.get("messages", []))
        brain_dir, artifacts = _collect_brain_artifacts(sid)
        if sid in jetski_messages:
            for msg in jetski_messages[sid]:
                _append_message(messages, msg["role"], msg["text"])
        result.append({
            "session_id": sid,
            "title": conv["title"],
            "source": "antigravity",
            "date": date_str,
            "project": conv.get("project", ""),
            "messages": messages,
            "brain_dir": brain_dir,
            "artifacts": artifacts,
        })

    return result
