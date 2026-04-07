#!/usr/bin/env python3

import re
from pathlib import Path

KEYWORD_RE = re.compile(r"(结论|建议|下一步|计划|风险|原因|判断|推荐|todo|next step|recommend|decision|risk|plan|should|need to)", re.I)
ABSOLUTE_PATH_RE = re.compile(r"/Users/[^\s<>)\]\"'`]+")
RELATIVE_PATH_RE = re.compile(r"(?:docs|apps|packages|dashboard|extensions|lib|src)/[\w./-]+\.(?:py|html|md|tsx?|jsx?|json|sh|css|scss|toml|ya?ml)\b")
BACKTICK_FILE_RE = re.compile(r"`([^`\n]+?\.(?:py|html|md|tsx?|jsx?|json|sh|css|scss|toml|ya?ml))`")
URL_RE = re.compile(r"https?://\S+")
HOME_PATH_RE = re.compile(r"/Users/[^\s<>)\]\"'`]+")


def sanitize_filename(value: str, max_len: int = 80) -> str:
    if not value:
        return "untitled"
    safe = []
    for char in value:
        if ord(char) < 32:
            safe.append("_")
        elif char.isalnum() or char in ("-", "_", " ", ".", "，", "。"):
            safe.append(char)
        elif char in ("/", "\\", ":", "*", "?", '"', "<", ">", "|", "\n"):
            safe.append("_")
        else:
            safe.append(char)
    return "".join(safe)[:max_len].strip().rstrip(".") or "untitled"


def unique_markdown_path(directory: Path, stem: str, used_paths: set[str]) -> Path:
    directory.mkdir(parents=True, exist_ok=True)
    candidate = directory / f"{stem}.md"
    counter = 1
    while str(candidate) in used_paths:
        candidate = directory / f"{stem}_{counter}.md"
        counter += 1
    used_paths.add(str(candidate))
    return candidate


def strip_markdown_for_text(text: str) -> str:
    text = str(text or "")
    text = re.sub(r"```[\s\S]*?```", " ", text)
    text = re.sub(r"`([^`]+)`", r"\1", text)
    text = re.sub(r"!\[[^\]]*\]\([^)]+\)", " ", text)
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
    text = re.sub(r"[*_>#-]+", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def clean_project_label(project: str) -> str:
    project = str(project or "").replace("\x00", "").strip()
    project = re.sub(r"[\x01-\x1f\x7f]", "", project)
    project = re.sub(r"/{3,}", "/", project)
    return project.strip()


def truncate_text(text: str, max_chars: int) -> str:
    clean = strip_markdown_for_text(text)
    if len(clean) <= max_chars:
        return clean
    return clean[: max_chars - 1].rstrip() + "…"


def humanize_title_fragment(text: str, max_chars: int = 52) -> str:
    cleaned = strip_markdown_for_text(text)
    cleaned = URL_RE.sub("", cleaned)
    cleaned = HOME_PATH_RE.sub("", cleaned)
    cleaned = re.sub(r"\b(file|path|workspace|session id|viewer id)\b[:：]?\s*", "", cleaned, flags=re.I)
    cleaned = re.sub(r"[\[\](){}]+", " ", cleaned)
    cleaned = re.sub(r"\s+", " ", cleaned).strip(" -_:,.，。")
    if not cleaned:
        return ""
    return truncate_text(cleaned, max_chars)


def _normalize_path_candidate(path: str) -> str:
    cleaned = str(path or "").strip().strip("[]()'\"`")
    cleaned = cleaned.rstrip(":;,。！？")
    if not cleaned:
        return ""
    if cleaned.startswith("/Users/"):
        return cleaned
    if RELATIVE_PATH_RE.fullmatch(cleaned):
        return cleaned
    return ""


def _push_unique(target: list[str], seen: set[str], value: str, limit: int):
    if not value or value in seen or len(target) >= limit:
        return
    seen.add(value)
    target.append(value)


def extract_file_mentions(messages: list[dict], limit: int = 8) -> list[str]:
    files: list[str] = []
    seen: set[str] = set()
    for message in messages:
        text = str(message.get("text", ""))
        for match in ABSOLUTE_PATH_RE.findall(text):
            _push_unique(files, seen, _normalize_path_candidate(match), limit)
        for match in RELATIVE_PATH_RE.findall(text):
            _push_unique(files, seen, _normalize_path_candidate(match), limit)
        for match in BACKTICK_FILE_RE.findall(text):
            _push_unique(files, seen, _normalize_path_candidate(match), limit)
    return files


def extract_command_mentions(messages: list[dict], limit: int = 8) -> list[str]:
    commands: list[str] = []
    seen: set[str] = set()
    prefixes = ("python3", "python", "git", "npm", "pnpm", "yarn", "uv", "pytest", "npx", "node", "bash", "sh", "rg", "ls", "cd", "open")
    for message in messages:
        text = str(message.get("text", ""))
        for line in text.splitlines():
            line = line.strip()
            if line.startswith("$ "):
                line = line[2:].strip()
            if line.startswith(prefixes):
                _push_unique(commands, seen, truncate_text(line, 140), limit)
    return commands


def extract_signal_mentions(messages: list[dict], limit: int = 6) -> list[str]:
    signals: list[str] = []
    seen: set[str] = set()
    for message in messages:
        if message.get("role") != "assistant":
            continue
        for line in str(message.get("text", "")).splitlines():
            candidate = line.strip().lstrip("-* ").strip()
            if len(candidate) < 12 or len(candidate) > 180:
                continue
            if not KEYWORD_RE.search(candidate):
                continue
            _push_unique(signals, seen, truncate_text(candidate, 160), limit)
    return signals


def pick_final_answer(messages: list[dict]) -> str:
    for message in reversed(messages):
        if message.get("role") == "assistant":
            text = str(message.get("text", "")).strip()
            if text:
                return truncate_text(text, 800)
    return ""


def prompts_match(left: str, right: str) -> bool:
    left = re.sub(r"\s+", " ", str(left or "")).strip()
    right = re.sub(r"\s+", " ", str(right or "")).strip()
    if not left or not right:
        return False
    if left == right:
        return True
    left_short = left[:220]
    right_short = right[:220]
    return left_short == right_short or left_short in right_short or right_short in left_short


def build_search_entry(conversation: dict) -> dict:
    """从 conversation 中提取搜索索引条目，用于轻量快速搜索。"""
    messages = conversation.get("messages", [])
    # 提取关键词：title 分词 + signals + files
    title = strip_markdown_for_text(conversation.get("title", ""))
    title_words = [w for w in re.split(r"[\s/_\-.,:;!?|<>{}()\[\]]+", title) if len(w) > 2][:10]
    signals = extract_signal_mentions(messages, limit=4)
    files = extract_file_mentions(messages, limit=4)
    commands = extract_command_mentions(messages, limit=3)
    keywords = list(dict.fromkeys(title_words + signals + files + commands))[:15]
    return {
        "id": conversation.get("id", ""),
        "source": conversation.get("source", ""),
        "date": conversation.get("date", ""),
        "session_id": conversation.get("session_id", ""),
        "title": title[:120],
        "keywords": keywords,
        "transcript_path": conversation.get("transcript_path", ""),
    }


def is_subagent_conversation(conversation: dict) -> bool:
    if conversation.get("is_subagent"):
        return True
    file_value = str(conversation.get("file", "")).lower()
    project_value = str(conversation.get("project", "")).lower()
    return "subagents_" in file_value or project_value == "subagents"


def get_subagent_display_name(conversation: dict) -> str:
    return conversation.get("subagent_summary") or conversation.get("title") or "Sub-agent"


def build_subagent_index(conversations: list[dict]) -> dict[str, list[dict]]:
    grouped: dict[str, list[dict]] = {}
    for conversation in conversations:
        if not is_subagent_conversation(conversation):
            continue
        parent_session_id = conversation.get("parent_session_id") or ""
        if not parent_session_id:
            continue
        grouped.setdefault(parent_session_id, []).append(conversation)
    for items in grouped.values():
        items.sort(key=lambda item: str(item.get("first_ts", item.get("date", ""))))
    return grouped


def match_subagent_calls(conversation: dict, subagent_index: dict[str, list[dict]]) -> list[tuple[dict, list[dict]]]:
    related = list(subagent_index.get(conversation.get("session_id", ""), []))
    used_ids: set[str] = set()
    matched: list[tuple[dict, list[dict]]] = []
    for message in conversation.get("messages", []):
        if message.get("role") != "subagent_call":
            continue
        matches = []
        for candidate in related:
            if candidate.get("id") in used_ids:
                continue
            if prompts_match(message.get("prompt", "") or message.get("text", ""), candidate.get("launch_prompt", "")):
                matches.append(candidate)
        for candidate in matches:
            used_ids.add(candidate.get("id"))
        matched.append((message, matches))
    return matched


def _render_frontmatter(conversation: dict) -> list[str]:
    return [
        "---",
        f"id: {conversation.get('id', '')}",
        f"source: {conversation.get('source', '')}",
        f"date: {conversation.get('date', '')}",
        f"session_id: {conversation.get('session_id', '')}",
        f"viewer_id: {conversation.get('id', '')}",
        "transcript_version: 2",
        f"project: {conversation.get('project', '')}".rstrip(),
        "---",
        "",
    ]


def _append_section(lines: list[str], title: str, body_lines: list[str]):
    lines.append(f"## {title}")
    lines.append("")
    lines.extend(body_lines or ["- None"])
    lines.append("")


def _render_quick_summary(conversation: dict) -> list[str]:
    messages = conversation.get("messages", [])
    project = clean_project_label(conversation.get("project", ""))
    final_answer = pick_final_answer(messages)
    files = extract_file_mentions(messages)
    commands = extract_command_mentions(messages)
    signals = extract_signal_mentions(messages)
    lines: list[str] = []
    _append_section(lines, "Session", [
        f"- Source: {conversation.get('source', '')}",
        f"- Date: {conversation.get('date', '')}",
        f"- Project: `{project}`" if project else "- Project: Unknown",
        f"- Session ID: `{conversation.get('session_id', '')}`",
    ])
    _append_section(lines, "Quick Summary", [
        f"- Final answer: {final_answer}" if final_answer else "- Final answer: Not available",
    ])
    _append_section(lines, "Files Mentioned", [f"- `{item}`" for item in files] or ["- None detected"])
    _append_section(lines, "Commands Mentioned", [f"- `{item}`" for item in commands] or ["- None detected"])
    _append_section(lines, "Signals", [f"- {item}" for item in signals] or ["- No clear recommendation / next-step markers detected"])
    return lines


def _render_artifacts(conversation: dict) -> list[str]:
    artifacts = list(conversation.get("artifacts", []))
    if not artifacts and not conversation.get("brain_dir"):
        return []
    lines: list[str] = []
    if conversation.get("brain_dir"):
        lines.append(f"- Brain workspace: `{conversation['brain_dir']}`")
    for artifact in artifacts:
        title = artifact.get("title") or artifact.get("name") or artifact.get("rel_path") or "artifact"
        rel_path = artifact.get("rel_path") or artifact.get("name") or title
        lines.append(f"- `{rel_path}`: {title}")
        if artifact.get("path"):
            lines.append(f"  - path: `{artifact['path']}`")
    return lines


def _role_heading(role: str, source: str = "") -> str:
    if role == "user":
        return "### User"
    if role == "assistant":
        label = source.capitalize() if source else "Assistant"
        return f"### {label}"
    if role == "summary":
        return "### Context Compression Summary"
    return "### Note"


def _append_text_block(lines: list[str], heading: str, text: str):
    lines.append(heading)
    lines.append("")
    lines.append(text.strip() or "_(empty)_")
    lines.append("")


def render_transcript_markdown(conversation: dict, all_conversations: list[dict]) -> str:
    title = conversation.get("title") or conversation.get("session_id") or "Untitled"
    lines = _render_frontmatter(conversation)
    lines.append(f"# {title}")
    lines.append("")
    lines.extend(_render_quick_summary(conversation))

    artifact_lines = _render_artifacts(conversation)
    if artifact_lines:
        _append_section(lines, "Artifacts", artifact_lines)

    lines.append("## Transcript")
    lines.append("")

    subagent_index = build_subagent_index(all_conversations)
    subagent_matches = match_subagent_calls(conversation, subagent_index)
    subagent_iter = iter(subagent_matches)

    for message in conversation.get("messages", []):
        role = message.get("role")
        if role == "subagent_call":
            lines.append("### Sub-agent Call")
            lines.append("")
            if message.get("description"):
                lines.append(f"- Description: {message['description']}")
            if message.get("prompt"):
                lines.append("- Prompt:")
                lines.append("")
                lines.append("```text")
                lines.append(message["prompt"])
                lines.append("```")
            lines.append("")
            _, matches = next(subagent_iter, (message, []))
            if matches:
                for match in matches:
                    lines.append(f"#### Embedded Sub-agent Transcript: {get_subagent_display_name(match)}")
                    lines.append("")
                    for child_message in match.get("messages", []):
                        if child_message.get("role") == "subagent_call":
                            continue
                        _append_text_block(lines, _role_heading(child_message.get("role"), "sub-agent"), str(child_message.get("text", "")))
            else:
                lines.append("_No exported sub-agent transcript was matched to this call._")
                lines.append("")
            continue

        _append_text_block(lines, _role_heading(role, conversation.get("source", "")), str(message.get("text", "")))

    return "\n".join(lines).rstrip() + "\n"
