#!/usr/bin/env python3
"""
Claude Code 会话提取工具
用法: python3 extract_claude_conversations.py
交互式输入日期，按天导出所有 Claude Code 会话为可读 Markdown 文件。
"""

import json
import os
import glob
import re
from datetime import datetime, timedelta
from pathlib import Path

CLAUDE_DIR = Path.home() / ".claude"
PROJECTS_DIR = CLAUDE_DIR / "projects"
HISTORY_FILE = CLAUDE_DIR / "history.jsonl"


def load_history_index():
    """从 history.jsonl 建立 sessionId -> 首条用户输入 的索引（用于标题）"""
    index = {}
    if HISTORY_FILE.exists():
        with open(HISTORY_FILE) as f:
            for line in f:
                try:
                    obj = json.loads(line.strip())
                    sid = obj.get("sessionId", "")
                    if sid and sid not in index:
                        index[sid] = {
                            "display": obj.get("display", ""),
                            "project": obj.get("project", ""),
                            "timestamp": obj.get("timestamp", 0),
                        }
                except:
                    pass
    return index


def find_sessions_by_date(target_date: str):
    """
    找到某天活跃的所有 Claude Code 会话。
    扫描所有 project 目录下的 .jsonl 文件，检查其中消息的时间戳。
    返回 list of {session_id, filepath, project, first_ts}
    """
    dt = datetime.strptime(target_date, "%Y-%m-%d")
    day_start = dt.isoformat() + "Z"
    day_end = (dt + timedelta(days=1)).isoformat() + "Z"
    day_start_ms = int(dt.timestamp() * 1000)
    day_end_ms = int((dt + timedelta(days=1)).timestamp() * 1000)

    results = []

    for jsonl_file in PROJECTS_DIR.rglob("*.jsonl"):
        # session_id 是文件名（不含扩展名）
        session_id = jsonl_file.stem
        is_subagent = "subagents" in jsonl_file.parts
        if is_subagent and len(jsonl_file.parts) >= 4:
            project = jsonl_file.parent.parent.parent.name
            parent_session_id = jsonl_file.parent.parent.name
        else:
            project = jsonl_file.parent.name
            parent_session_id = ""

        # 检查文件修改时间：如果 mtime 在目标日期当天，视为匹配
        # 这解决了"旧会话今天继续，但消息时间戳被压缩"的问题
        mtime = os.path.getmtime(jsonl_file)
        mtime_dt = datetime.fromtimestamp(mtime)
        mtime_matched = mtime_dt.date() == dt.date()

        # 读取文件，检查是否有目标日期的消息
        has_target_date = mtime_matched
        first_ts = ""
        try:
            with open(jsonl_file) as f:
                for line in f:
                    try:
                        obj = json.loads(line.strip())
                        ts = obj.get("timestamp", "")
                        if isinstance(ts, str) and ts >= day_start and ts < day_end:
                            has_target_date = True
                            if not first_ts:
                                first_ts = ts
                            break
                        elif isinstance(ts, (int, float)):
                            if ts >= day_start_ms and ts < day_end_ms:
                                has_target_date = True
                                if not first_ts:
                                    first_ts = datetime.fromtimestamp(ts / 1000).isoformat()
                                break
                    except:
                        continue
        except:
            continue

        if has_target_date:
            results.append({
                "session_id": session_id,
                "filepath": str(jsonl_file),
                "project": project,
                "first_ts": first_ts,
                "is_subagent": is_subagent,
                "parent_session_id": parent_session_id,
            })

    return results


CONTINUATION_MARKER = "This session is being continued from a previous conversation"
SYSTEM_NOISE_PREFIXES = ("<system-reminder>", "<environment_details>", "<local-command")


def _is_noise(text):
    return any(text.startswith(p) for p in SYSTEM_NOISE_PREFIXES)


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
            # 检查剩余行数是否超过 20 行
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


def _extract_user_text(content):
    """从 user message content 提取纯文本"""
    if isinstance(content, str):
        return _clean_text(content)
    if isinstance(content, list):
        parts = []
        for c in content:
            if isinstance(c, dict):
                if c.get("type") == "text":
                    parts.append(c.get("text", ""))
                elif c.get("type") == "image":
                    parts.append("[图片]")
            elif isinstance(c, str):
                parts.append(c)
        return _clean_text("\n".join(parts))
    return ""


def _extract_assistant_text(content):
    """从 assistant message content 提取纯文本"""
    if isinstance(content, list):
        parts = [c.get("text", "").strip()
                 for c in content
                 if isinstance(c, dict) and c.get("type") == "text" and c.get("text", "").strip()]
        return _clean_text("\n\n".join(parts))
    if isinstance(content, str):
        return _clean_text(content)
    return ""


def _extract_subagent_summary(text):
    if not text:
        return ""
    m = re.search(r'<teammate-message[^>]*summary="([^"]+)"', text)
    if m:
        return m.group(1).strip()
    return ""


def extract_conversation(filepath, target_date=None):
    """
    从 Claude Code session JSONL 提取对话。

    处理两种情况：
    1. 普通 session：直接从 user/assistant 消息提取
    2. 压缩 session：Claude Code 压缩时会插入一条特殊 user 消息，内容是
       "This session is being continued from a previous conversation..."
       后面跟着 Summary。这条消息标志着之前的历史已被摘要替换。
       策略：把 Summary 作为一条特殊的 [摘要] 消息插入，然后继续提取后续真实消息。

    如果指定 target_date，只提取该天的消息。
    返回 list of {role, text, timestamp}
    """
    dt = None
    if target_date:
        dt = datetime.strptime(target_date, "%Y-%m-%d")
        day_start = dt.isoformat() + "Z"
        day_end = (dt + timedelta(days=1)).isoformat() + "Z"

    messages = []

    with open(filepath) as f:
        for line in f:
            try:
                obj = json.loads(line.strip())
            except:
                continue

            msg_type = obj.get("type")
            ts = obj.get("timestamp", "")

            # 日期过滤
            if dt and isinstance(ts, str) and ts:
                if ts < day_start or ts >= day_end:
                    continue

            msg = obj.get("message", {})
            if not isinstance(msg, dict):
                continue

            role = msg.get("role", "")
            content = msg.get("content", "")

            if msg_type == "user" and role == "user":
                text = _extract_user_text(content)
                if not text or _is_noise(text):
                    continue

                # 检测压缩续接消息
                if text.startswith(CONTINUATION_MARKER):
                    # 提取 Summary 部分作为特殊标记消息
                    summary_start = text.find("Summary:")
                    if summary_start != -1:
                        summary_text = text[summary_start:].strip()
                        messages.append({
                            "role": "summary",
                            "text": summary_text,
                            "ts": ts
                        })
                    # 不把这条当普通用户消息
                    continue

                messages.append({"role": "user", "text": text, "ts": ts})

            elif msg_type == "assistant" and role == "assistant":
                if isinstance(content, list):
                    text_parts = []
                    subagent_calls = []
                    for part in content:
                        if not isinstance(part, dict):
                            continue
                        if part.get("type") == "text" and part.get("text", "").strip():
                            text_parts.append(part.get("text", ""))
                        elif part.get("type") == "tool_use" and part.get("name") == "Agent":
                            tool_input = part.get("input", {}) or {}
                            prompt = _clean_text(tool_input.get("prompt", ""))
                            description = _clean_text(tool_input.get("description", ""))
                            subagent_calls.append({
                                "role": "subagent_call",
                                "text": description or prompt,
                                "prompt": prompt,
                                "description": description,
                                "tool_use_id": part.get("id", ""),
                                "ts": ts,
                            })

                    text = _clean_text("\n\n".join(text_parts))
                    if text:
                        messages.append({"role": "assistant", "text": text, "ts": ts})
                    messages.extend(subagent_calls)
                else:
                    text = _extract_assistant_text(content)
                    if text:
                        messages.append({"role": "assistant", "text": text, "ts": ts})

    return messages


def decode_project_name(encoded):
    """将编码的项目目录名还原为可读路径"""
    return encoded.replace("-", "/").lstrip("/")


def sanitize_filename(s, max_len=60):
    if not s:
        return "untitled"
    safe = ""
    for c in s:
        if c.isalnum() or c in ("-", "_", " ", ".", "，", "。"):
            safe += c
        elif c in ("/", "\\", ":", "*", "?", '"', "<", ">", "|", "\n"):
            safe += "_"
        else:
            safe += c
    return safe[:max_len].strip().rstrip(".")


def format_conversation(messages, session_id, project, first_ts):
    lines = []
    proj_path = decode_project_name(project)
    title = ""
    # 用第一条用户消息作为标题
    for m in messages:
        if m["role"] == "user":
            title = m["text"][:80]
            break
    lines.append(f"# {title or '未命名会话'}")
    lines.append("")
    lines.append(f"- Session ID: `{session_id}`")
    lines.append(f"- 项目: `{proj_path}`")
    if first_ts:
        lines.append(f"- 时间: {first_ts}")
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
            lines.append("## 🧑 用户")
            lines.append("")
            lines.append(text)
            lines.append("")
        elif role == "assistant":
            lines.append("## 🤖 Claude")
            lines.append("")
            lines.append(text)
            lines.append("")
        elif role == "subagent_call":
            lines.append("## 🧩 子智能体调用")
            lines.append("")
            if msg.get("description"):
                lines.append(f"调用说明：{msg['description']}")
                lines.append("")
            if msg.get("prompt"):
                lines.append("调用 Prompt：")
                lines.append("")
                lines.append(msg["prompt"])
                lines.append("")
        elif role == "summary":
            lines.append("## 📋 [上下文压缩摘要]")
            lines.append("")
            lines.append("> " + text.replace("\n", "\n> "))
            lines.append("")

    return "\n".join(lines)


def main():
    print("=" * 50)
    print("  Claude Code 会话提取工具")
    print("=" * 50)
    print()

    # 加载历史索引
    print("加载历史索引...")
    history = load_history_index()
    print(f"  已索引 {len(history)} 个会话")
    print()

    while True:
        date_input = input("请输入日期 (YYYY-MM-DD)，输入 q 退出: ").strip()
        if date_input.lower() == "q":
            print("再见！")
            break

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

        out_dir = OUTPUT_BASE / date_input
        out_dir.mkdir(parents=True, exist_ok=True)

        exported = 0
        skipped = 0

        for sess in sorted(sessions, key=lambda x: x["first_ts"]):
            sid = sess["session_id"]
            project = sess["project"]
            proj_short = decode_project_name(project)

            print(f"\n  处理: [{proj_short}] {sid[:12]}...")

            messages = extract_conversation(sess["filepath"], target_date=date_input)

            if not messages:
                print(f"    跳过（无对话内容）")
                skipped += 1
                continue

            md = format_conversation(messages, sid, project, sess["first_ts"])

            # 文件名: 项目缩写 + 第一条用户消息
            first_user = ""
            for m in messages:
                if m["role"] == "user":
                    first_user = m["text"][:40]
                    break
            proj_abbr = project.split("-")[-1][:15] if project else "unknown"
            fname_base = sanitize_filename(f"{proj_abbr}_{first_user}" if first_user else f"{proj_abbr}_{sid[:8]}")
            fname = f"{fname_base}.md"
            out_path = out_dir / fname

            counter = 1
            while out_path.exists():
                fname = f"{fname_base}_{counter}.md"
                out_path = out_dir / fname
                counter += 1

            with open(out_path, "w", encoding="utf-8") as f:
                f.write(md)

            user_count = sum(1 for m in messages if m["role"] == "user")
            asst_count = sum(1 for m in messages if m["role"] == "assistant")
            print(f"    ✓ {len(messages)} 条消息 (用户:{user_count}, Claude:{asst_count}) -> {fname}")
            exported += 1

        print(f"\n{'=' * 40}")
        print(f"  导出: {exported} 个会话")
        print(f"  跳过: {skipped} 个（无内容）")
        print(f"  输出目录: {out_dir}")
        print(f"{'=' * 40}\n")


if __name__ == "__main__":
    main()
