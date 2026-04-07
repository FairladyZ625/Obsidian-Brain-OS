#!/usr/bin/env python3
"""
Codex 会话提取工具
用法: python3 extract_conversations.py
交互式输入日期，按天导出所有会话为可读 Markdown 文件。
"""

import json
import os
import re
import sqlite3
from datetime import datetime, timedelta
from pathlib import Path

CODEX_DIR = Path.home() / ".codex"
SESSIONS_DIR = CODEX_DIR / "sessions"
STATE_DB = CODEX_DIR / "state_5.sqlite"
HISTORY_FILE = CODEX_DIR / "history.jsonl"
SESSION_INDEX = CODEX_DIR / "session_index.jsonl"


def load_thread_titles():
    """从 session_index.jsonl 和 SQLite 加载会话标题"""
    titles = {}
    # From session_index.jsonl
    if SESSION_INDEX.exists():
        with open(SESSION_INDEX) as f:
            for line in f:
                try:
                    obj = json.loads(line.strip())
                    titles[obj["id"]] = obj.get("thread_name", "")
                except:
                    pass
    # From SQLite (more complete)
    if STATE_DB.exists():
        try:
            conn = sqlite3.connect(str(STATE_DB))
            cur = conn.execute("SELECT id, title, cwd, model_provider FROM threads")
            for row in cur:
                tid, title = row[0], row[1]
                titles[tid] = title or titles.get(tid, "")
            conn.close()
        except:
            pass
    return titles


def load_history_for_session(session_id):
    """从 history.jsonl 加载某个 session 的用户输入"""
    messages = []
    if HISTORY_FILE.exists():
        with open(HISTORY_FILE) as f:
            for line in f:
                try:
                    obj = json.loads(line.strip())
                    if obj.get("session_id") == session_id:
                        messages.append({
                            "ts": obj.get("ts", 0),
                            "text": obj.get("text", "")
                        })
                except:
                    pass
    return messages


def find_sessions_by_date(target_date: str):
    """
    找到某天活跃的所有会话文件。
    target_date 格式: YYYY-MM-DD

    策略:
    1. 直接匹配 sessions/YYYY/MM/DD/ 目录下的文件
    2. 同时从 SQLite 查找该天有更新的 thread，再找对应 rollout 文件
    """
    dt = datetime.strptime(target_date, "%Y-%m-%d")
    year = str(dt.year)
    month = f"{dt.month:02d}"
    day = f"{dt.day:02d}"

    found = {}  # session_id -> file_path

    # 方法1: 直接目录匹配
    day_dir = SESSIONS_DIR / year / month / day
    if day_dir.exists():
        for f in day_dir.glob("*.jsonl"):
            # 从文件名提取 session_id (最后的 UUID 部分)
            parts = f.stem.split("-")
            # rollout-YYYY-MM-DDTHH-MM-SS-UUID
            # UUID 是最后5段用-连接
            if len(parts) >= 11:
                sid = "-".join(parts[6:])
                found[sid] = str(f)

    # 方法2: 从 archived_sessions 查找
    archived_dir = CODEX_DIR / "archived_sessions"
    if archived_dir.exists():
        for f in archived_dir.glob("*.jsonl"):
            # 检查文件名中的日期
            name = f.stem
            if f"rollout-{year}-{month}-{day}" in name:
                parts = name.split("-")
                if len(parts) >= 11:
                    sid = "-".join(parts[6:])
                    found[sid] = str(f)

    # 方法3: 从 SQLite 查找该天有活动的 thread
    if STATE_DB.exists():
        try:
            conn = sqlite3.connect(str(STATE_DB))
            # updated_at 是毫秒时间戳
            day_start = int(dt.timestamp() * 1000)
            day_end = int((dt + timedelta(days=1)).timestamp() * 1000)
            cur = conn.execute(
                "SELECT id, rollout_path FROM threads WHERE "
                "(created_at BETWEEN ? AND ?) OR (updated_at BETWEEN ? AND ?)",
                (day_start, day_end, day_start, day_end)
            )
            for row in cur:
                tid, rollout_path = row
                if tid not in found and rollout_path:
                    full_path = CODEX_DIR / rollout_path
                    if full_path.exists():
                        found[tid] = str(full_path)
            conn.close()
        except Exception as e:
            print(f"  [警告] SQLite 查询失败: {e}")

    return found


def _is_system_noise(text):
    """过滤系统注入内容"""
    prefixes = ("<environment", "# AGENTS.md", "<INSTRUCTIONS>",
                "<permissions", "<app-context", "<collaboration_mode",
                "## Apps\n", "<developer>")
    return any(text.startswith(p) for p in prefixes)


# ── 噪音标签正则 ──
_NOISE_TAG_PATTERNS = [
    re.compile(r'<system-reminder>[\s\S]*?</system-reminder>'),
    re.compile(r'<command-message>[\s\S]*?</command-message>'),
    re.compile(r'<command-name>[\s\S]*?</command-name>'),
    re.compile(r'<command-args>[\s\S]*?</command-args>'),
    re.compile(r'<local-command-caveat>[\s\S]*?</local-command-caveat>'),
    re.compile(r'<local-command-stdout>[\s\S]*?</local-command-stdout>'),
    re.compile(r'<task-notification>[\s\S]*?</task-notification>'),
]


def _clean_text(text):
    """清洗文本，去掉各种噪音标签和 skill 加载内容"""
    if not text:
        return text
    # 去掉噪音标签
    for pat in _NOISE_TAG_PATTERNS:
        text = pat.sub('', text)
    # 去掉 skill 加载大段内容（Base directory for this skill: 开头，后跟超过 20 行）
    lines = text.split('\n')
    cleaned_lines = []
    skip = False
    for i, line in enumerate(lines):
        if line.strip().startswith('Base directory for this skill:'):
            remaining = len(lines) - i - 1
            if remaining > 20:
                skip = True
                continue
        if skip:
            continue
        cleaned_lines.append(line)
    text = '\n'.join(cleaned_lines)
    # 清理多余空行（连续 3 个以上空行合并为 2 个）
    text = re.sub(r'\n{4,}', '\n\n\n', text)
    return text.strip()


def _extract_from_history(rh, ts_hint=""):
    """
    从 replacement_history 列表提取对话消息。
    rh: list of {role, content} dicts
    返回 list of {role, text, ts}
    """
    msgs = []
    for item in rh:
        if not isinstance(item, dict):
            continue
        role = item.get("role")
        content = item.get("content", [])
        if role not in ("user", "assistant"):
            continue
        if isinstance(content, list):
            for c in content:
                if not isinstance(c, dict):
                    continue
                ctype = c.get("type", "")
                text = c.get("text", "").strip()
                if not text:
                    continue
                if ctype == "output_text" and role == "assistant":
                    text = _clean_text(text)
                    if text:
                        msgs.append({"role": "assistant", "text": text, "ts": ts_hint})
                elif ctype == "input_text" and role == "user":
                    if not _is_system_noise(text) and len(text) < 10000:
                        text = _clean_text(text)
                        if text:
                            msgs.append({"role": "user", "text": text, "ts": ts_hint})
        elif isinstance(content, str) and content.strip():
            text = content.strip()
            if role == "user" and not _is_system_noise(text):
                text = _clean_text(text)
                if text:
                    msgs.append({"role": "user", "text": text, "ts": ts_hint})
            elif role == "assistant":
                text = _clean_text(text)
                if text:
                    msgs.append({"role": "assistant", "text": text, "ts": ts_hint})
    return msgs


def extract_conversation(filepath):
    """
    从 session JSONL 文件提取纯对话内容（用户问题 + Codex 回答）。

    处理两种情况：
    1. 普通 session：从 event_msg/user_message 和 response_item/message/assistant 提取
    2. 压缩 session：从 compacted 事件的 replacement_history 提取（取最后一次，最完整）

    返回 (messages, session_meta)
    """
    with open(filepath) as f:
        lines = f.readlines()

    session_meta = None
    # 普通流式消息
    stream_messages = []
    # compacted 快照列表，每次压缩都是全量历史，取最后一个
    compacted_snapshots = []

    for line in lines:
        try:
            obj = json.loads(line.strip())
        except:
            continue

        event_type = obj.get("type")
        payload = obj.get("payload", {})
        ts = obj.get("timestamp", "")

        # 会话元数据
        if event_type == "session_meta":
            session_meta = payload if isinstance(payload, dict) else None
            continue

        # ── compacted 事件：保存快照（取最后一个，最完整）──
        if event_type == "compacted" and isinstance(payload, dict):
            rh = payload.get("replacement_history", [])
            if rh:
                compacted_snapshots.append({"ts": ts, "rh": rh})
            continue

        if not isinstance(payload, dict):
            continue

        # ── 普通流式：用户消息 ──
        if event_type == "event_msg" and payload.get("type") == "user_message":
            text = payload.get("message", "").strip()
            if text:
                text = _clean_text(text)
                if text:
                    stream_messages.append({"role": "user", "text": text, "ts": ts})
            continue

        # ── 普通流式：Codex 回复 ──
        if event_type == "response_item":
            pt = payload.get("type")
            role = payload.get("role")

            if pt == "message" and role == "assistant":
                content = payload.get("content", [])
                if isinstance(content, list):
                    for c in content:
                        if isinstance(c, dict) and c.get("type") == "output_text":
                            text = c.get("text", "").strip()
                            if text:
                                text = _clean_text(text)
                                if text:
                                    stream_messages.append({"role": "assistant", "text": text, "ts": ts})

            # 早期版本备用路径（无 event_msg 时）
            elif pt == "message" and role == "user" and not any(
                m["role"] == "user" for m in stream_messages
            ):
                content = payload.get("content", [])
                if isinstance(content, list):
                    for c in content:
                        if isinstance(c, dict) and c.get("type") == "input_text":
                            text = c.get("text", "").strip()
                            if text and not _is_system_noise(text) and len(text) < 5000:
                                text = _clean_text(text)
                                if text:
                                    stream_messages.append({"role": "user", "text": text, "ts": ts})

    # ── 合并策略 ──
    if compacted_snapshots:
        # 取最后一次压缩快照（最完整的历史）
        last_snapshot = compacted_snapshots[-1]
        base_messages = _extract_from_history(last_snapshot["rh"], last_snapshot["ts"])

        # 找出快照之后新增的流式消息（时间戳晚于最后一次压缩）
        last_compact_ts = last_snapshot["ts"]
        new_stream = [m for m in stream_messages if m["ts"] > last_compact_ts]

        # 去重：新流式消息可能和快照末尾重叠
        if base_messages and new_stream:
            last_base_texts = {m["text"] for m in base_messages[-6:]}
            new_stream = [m for m in new_stream if m["text"] not in last_base_texts]

        messages = base_messages + new_stream
    else:
        messages = stream_messages

    # 最后兜底：早期 session 文件无内容时从 history.jsonl 补
    if not messages:
        parts = os.path.basename(filepath).replace(".jsonl", "").split("-")
        sid = "-".join(parts[6:]) if len(parts) >= 11 else ""
        hist = load_history_for_session(sid) if sid else []
        for h in hist:
            messages.append({"role": "user", "text": h["text"], "ts": ""})

    return messages, session_meta


def format_conversation(messages, session_id, title, meta):
    """格式化为 Markdown"""
    lines = []
    lines.append(f"# {title or '未命名会话'}")
    lines.append("")
    lines.append(f"- Session ID: `{session_id}`")
    if meta:
        lines.append(f"- 工作目录: `{meta.get('cwd', '?')}`")
        lines.append(f"- CLI 版本: `{meta.get('cli_version', '?')}`")
        ts = meta.get("timestamp", "")
        if ts:
            lines.append(f"- 开始时间: {ts}")
    lines.append("")
    lines.append("---")
    lines.append("")

    if not messages:
        lines.append("*（此会话无可提取的对话内容）*")
        return "\n".join(lines)

    for msg in messages:
        role = msg["role"]
        text = msg["text"]
        if role == "user":
            lines.append(f"## 🧑 用户")
            lines.append("")
            lines.append(text)
            lines.append("")
        else:
            lines.append(f"## 🤖 Codex")
            lines.append("")
            lines.append(text)
            lines.append("")

    return "\n".join(lines)


def sanitize_filename(s, max_len=60):
    """清理文件名"""
    if not s:
        return "untitled"
    # 移除不安全字符
    safe = ""
    for c in s:
        if c.isalnum() or c in ("-", "_", " ", ".", "，", "。"):
            safe += c
        elif c in ("/", "\\", ":", "*", "?", '"', "<", ">", "|"):
            safe += "_"
        else:
            safe += c
    return safe[:max_len].strip().rstrip(".")


def main():
    print("=" * 50)
    print("  Codex 会话提取工具")
    print("=" * 50)
    print()

    # 加载标题索引
    print("加载会话索引...")
    titles = load_thread_titles()
    print(f"  已索引 {len(titles)} 个会话")
    print()

    while True:
        date_input = input("请输入日期 (YYYY-MM-DD)，输入 q 退出: ").strip()
        if date_input.lower() == "q":
            print("再见！")
            break

        # 验证日期格式
        try:
            datetime.strptime(date_input, "%Y-%m-%d")
        except ValueError:
            print("  日期格式错误，请使用 YYYY-MM-DD 格式")
            continue

        print(f"\n搜索 {date_input} 的会话...")
        sessions = find_sessions_by_date(date_input)

        if not sessions:
            print(f"  未找到 {date_input} 的任何会话")
            print()
            continue

        print(f"  找到 {len(sessions)} 个会话")

        # 创建输出目录
        out_dir = OUTPUT_BASE / date_input
        out_dir.mkdir(parents=True, exist_ok=True)

        exported = 0
        skipped = 0

        for sid, fpath in sorted(sessions.items()):
            title = titles.get(sid, "")
            print(f"\n  处理: {title or sid}")

            messages, meta = extract_conversation(fpath)

            if not messages:
                print(f"    跳过（无对话内容）")
                skipped += 1
                continue

            md = format_conversation(messages, sid, title, meta)

            # 生成文件名
            safe_title = sanitize_filename(title) if title else sid[:12]
            fname = f"{safe_title}.md"
            out_path = out_dir / fname

            # 避免重名
            counter = 1
            while out_path.exists():
                fname = f"{safe_title}_{counter}.md"
                out_path = out_dir / fname
                counter += 1

            with open(out_path, "w", encoding="utf-8") as f:
                f.write(md)

            msg_count = len(messages)
            user_count = sum(1 for m in messages if m["role"] == "user")
            asst_count = sum(1 for m in messages if m["role"] == "assistant")
            print(f"    ✓ {msg_count} 条消息 (用户:{user_count}, Codex:{asst_count}) -> {fname}")
            exported += 1

        print(f"\n{'=' * 40}")
        print(f"  导出: {exported} 个会话")
        print(f"  跳过: {skipped} 个（无内容）")
        print(f"  输出目录: {out_dir}")
        print(f"{'=' * 40}\n")


if __name__ == "__main__":
    main()
