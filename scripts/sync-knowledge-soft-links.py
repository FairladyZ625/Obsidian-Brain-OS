#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
import sys
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

DEFAULT_BRAIN_ROOT = Path.home() / 'my-brain'
RELATED_SECTION_TITLES = ('## Related Knowledge', '## Related Knowledge Entries', '## 相关知识入口', '## 相关知识')


@dataclass
class ProjectInfo:
    project_ref: str
    brief_path: Path
    section_title: str | None
    related_paths: set[str]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='Sync soft links between knowledge notes and project pages')
    parser.add_argument('--brain-root', default=str(DEFAULT_BRAIN_ROOT), help='Brain vault root path')
    parser.add_argument('--dry-run', action='store_true', help='Show intended updates without writing files')
    return parser.parse_args()


def rel_brain(path: Path, brain_root: Path) -> str:
    return path.relative_to(brain_root).as_posix()


def sort_knowledge_paths(paths: Iterable[str]) -> list[str]:
    def key(path: str):
        if path.startswith('03-KNOWLEDGE/01-READING/'):
            group = 0
        elif path.startswith('03-KNOWLEDGE/02-WORKING/'):
            group = 1
        else:
            group = 2
        return (group, path)

    return sorted(set(paths), key=key)


def read_text(path: Path) -> str:
    return path.read_text(encoding='utf-8')


def parse_frontmatter(text: str) -> tuple[str | None, str]:
    if not text.startswith('---\n'):
        return None, text
    parts = text.split('---\n', 2)
    if len(parts) < 3:
        return None, text
    return parts[1], parts[2]


def extract_project_ref(frontmatter: str | None) -> str | None:
    if not frontmatter:
        return None
    m = re.search(r'^project_ref:\s*"?([^"\n]+)"?\s*$', frontmatter, re.MULTILINE)
    return m.group(1).strip() if m else None


def parse_yaml_list(frontmatter: str, field: str) -> list[str]:
    lines = frontmatter.splitlines()
    items: list[str] = []
    in_block = False
    base_indent = None
    for line in lines:
        if not in_block:
            if re.match(rf'^{re.escape(field)}:\s*$', line):
                in_block = True
                continue
            m_inline = re.match(rf'^{re.escape(field)}:\s*\[(.*)\]\s*$', line)
            if m_inline:
                raw = m_inline.group(1).strip()
                if not raw:
                    return []
                return [p.strip().strip('"\'') for p in raw.split(',') if p.strip()]
            continue
        if not line.strip():
            break
        indent = len(line) - len(line.lstrip(' '))
        if base_indent is None and re.match(r'^\s*-\s+', line):
            base_indent = indent
        if re.match(r'^\s*-\s+', line):
            items.append(re.sub(r'^\s*-\s+', '', line).strip().strip('"\''))
            continue
        if indent == 0:
            break
        if base_indent is not None and indent < base_indent:
            break
    return items


def set_yaml_list(frontmatter: str | None, field: str, items: list[str]) -> str:
    items = list(dict.fromkeys(items))
    block = field + ':\n' + '\n'.join(f'  - {item}' for item in items)
    if frontmatter is None:
        return block + '\n'

    lines = frontmatter.splitlines()
    out: list[str] = []
    i = 0
    replaced = False
    while i < len(lines):
        line = lines[i]
        if re.match(rf'^{re.escape(field)}:\s*$', line) or re.match(rf'^{re.escape(field)}:\s*\[.*\]\s*$', line):
            if not replaced:
                out.extend(block.splitlines())
                replaced = True
            i += 1
            while i < len(lines):
                nxt = lines[i]
                if not nxt.strip():
                    break
                if re.match(r'^\s*-\s+', nxt):
                    i += 1
                    continue
                if re.match(r'^[A-Za-z0-9_-]+:\s*', nxt):
                    break
                if len(nxt) - len(nxt.lstrip(' ')) > 0:
                    i += 1
                    continue
                break
            continue
        out.append(line)
        i += 1

    if not replaced:
        if out and out[-1].strip():
            out.append('')
        out.extend(block.splitlines())
    return '\n'.join(out).rstrip() + '\n'


def extract_paths_from_related_section(text: str, section_title: str | None = None) -> tuple[str | None, list[str]]:
    lines = text.splitlines()
    title_idx = None
    matched_title = None
    for idx, line in enumerate(lines):
        if line.strip() in RELATED_SECTION_TITLES:
            title_idx = idx
            matched_title = line.strip()
            if section_title is None or section_title == matched_title:
                break
    if title_idx is None:
        return section_title, []
    paths: list[str] = []
    i = title_idx + 1
    while i < len(lines):
        line = lines[i]
        if line.startswith('## '):
            break
        m = re.match(r'^-\s+`([^`]+)`\s*$', line.strip())
        if m:
            paths.append(m.group(1).strip())
        i += 1
    return matched_title or section_title, paths


def replace_related_section(text: str, title: str, paths: list[str]) -> str:
    lines = text.splitlines()
    start = None
    for idx, line in enumerate(lines):
        if line.strip() in RELATED_SECTION_TITLES:
            start = idx
            break
    block = [title, ''] + [f'- `{p}`' for p in paths]
    if start is None:
        if lines and lines[-1].strip():
            lines.extend(['', ''])
        lines.extend(block)
        return '\n'.join(lines).rstrip() + '\n'
    end = start + 1
    while end < len(lines) and not lines[end].startswith('## '):
        end += 1
    new_lines = lines[:start] + block + ([''] if end < len(lines) and block[-1] != '' else []) + lines[end:]
    return '\n'.join(new_lines).rstrip() + '\n'


def parse_projects_index(text: str) -> dict[str, set[str]]:
    result: dict[str, set[str]] = {}
    blocks = re.split(r'(?m)^###\s+', text)
    for block in blocks[1:]:
        lines = block.splitlines()
        project_ref = None
        related: set[str] = set()
        in_related = False
        for line in lines:
            m_ref = re.search(r'`project_ref`:\s*`([^`]+)`', line)
            if m_ref:
                project_ref = m_ref.group(1).strip()
            if line.strip().startswith('- Related Knowledge:') or line.strip().startswith('- 相关知识：'):
                in_related = True
                inline = line.split(':', 1)[1].strip() if ':' in line else line.split('：', 1)[1].strip()
                if inline and inline not in ('TBD', '待补充'):
                    m = re.match(r'^`([^`]+)`$', inline)
                    if m:
                        related.add(m.group(1).strip())
                continue
            if in_related:
                m_item = re.match(r'^\s*-\s+`([^`]+)`\s*$', line)
                if m_item:
                    related.add(m_item.group(1).strip())
                    continue
                if line.startswith('- ') or line.startswith('### '):
                    in_related = False
        if project_ref:
            result[project_ref] = related
    return result


def replace_projects_index_block(text: str, project_ref: str, paths: list[str]) -> str:
    lines = text.splitlines()
    start = None
    end = None
    for idx, line in enumerate(lines):
        if line.startswith('### '):
            j = idx
            found_ref = None
            while j < len(lines) and not (j > idx and lines[j].startswith('### ')):
                m_ref = re.search(r'`project_ref`:\s*`([^`]+)`', lines[j])
                if m_ref:
                    found_ref = m_ref.group(1).strip()
                    break
                j += 1
            if found_ref == project_ref:
                start = idx
                end = idx + 1
                while end < len(lines) and not lines[end].startswith('### '):
                    end += 1
                break
    if start is None:
        raise ValueError(f'project_ref not found in projects-index: {project_ref}')

    block = lines[start:end]
    new_block: list[str] = []
    i = 0
    replaced = False
    while i < len(block):
        line = block[i]
        if line.strip().startswith('- Related Knowledge:') or line.strip().startswith('- 相关知识：'):
            new_block.append('- Related Knowledge:' if 'Related Knowledge' in line else '- 相关知识：')
            new_block.extend([f'  - `{p}`' for p in paths] if paths else ['  - TBD'])
            replaced = True
            i += 1
            while i < len(block):
                nxt = block[i]
                if re.match(r'^\s+-\s+`', nxt) or nxt.strip() in ('- TBD', '- 待补充'):
                    i += 1
                    continue
                break
            continue
        new_block.append(line)
        i += 1

    if not replaced:
        new_block.append('- Related Knowledge:' if any('Related Knowledge' in l for l in lines) else '- 相关知识：')
        new_block.extend([f'  - `{p}`' for p in paths] if paths else ['  - TBD'])
    return '\n'.join(lines[:start] + new_block + lines[end:]).rstrip() + '\n'


def update_frontmatter(text: str, new_frontmatter: str) -> str:
    frontmatter, body = parse_frontmatter(text)
    if frontmatter is None:
        return f'---\n{new_frontmatter}---\n{body.lstrip()}'
    return f'---\n{new_frontmatter}---\n{body.lstrip()}'


def main() -> int:
    args = parse_args()
    brain_root = Path(args.brain_root).expanduser().resolve()
    projects_dir = brain_root / '05-PROJECTS'
    projects_index = projects_dir / 'projects-index.md'
    knowledge_roots = [brain_root / '03-KNOWLEDGE/01-READING', brain_root / '03-KNOWLEDGE/02-WORKING']

    if not projects_dir.exists() or not projects_index.exists():
        print('error: missing projects directory or projects-index.md', file=sys.stderr)
        return 1

    project_infos: dict[str, ProjectInfo] = {}
    alias_map: dict[str, str] = {}
    invalid_project_refs: list[str] = []
    invalid_paths: list[str] = []
    normalized_paths: list[str] = []
    knowledge_updates = 0
    project_brief_updates = 0
    projects_index_updates = 0

    for brief in projects_dir.rglob('project-brief.md'):
        text = read_text(brief)
        fm, body = parse_frontmatter(text)
        project_ref = extract_project_ref(fm)
        if not project_ref:
            continue
        section_title, related_paths = extract_paths_from_related_section(body)
        cleaned: set[str] = set()
        for raw in related_paths:
            norm = raw.strip().lstrip('./')
            if norm != raw:
                normalized_paths.append(f'{rel_brain(brief, brain_root)}: {raw} -> {norm}')
            target = brain_root / norm
            if not target.exists():
                invalid_paths.append(f'{rel_brain(brief, brain_root)} -> {norm}')
                continue
            cleaned.add(norm)
        project_infos[project_ref] = ProjectInfo(project_ref, brief, section_title, cleaned)
        alias_map[project_ref] = project_ref
        alias_map[project_ref.lower()] = project_ref
        if fm:
            for field in ('project_name',):
                m = re.search(rf'^{field}:\s*"?([^"\n]+)"?\s*$', fm, re.MULTILINE)
                if m:
                    name = m.group(1).strip()
                    alias_map[name] = project_ref
                    alias_map[name.lower()] = project_ref
            aliases = parse_yaml_list(fm, 'aliases')
            for alias in aliases:
                alias_map[alias] = project_ref
                alias_map[alias.lower()] = project_ref
        alias_map[brief.parent.name] = project_ref
        alias_map[brief.parent.name.lower()] = project_ref

    expected_by_project: dict[str, set[str]] = defaultdict(set)

    for root in knowledge_roots:
        if not root.exists():
            continue
        for note in root.rglob('*.md'):
            text = read_text(note)
            fm, body = parse_frontmatter(text)
            note_rel = rel_brain(note, brain_root)
            related_projects: list[str] = []
            project_ref = extract_project_ref(fm)
            if project_ref:
                related_projects.append(project_ref)
            if fm:
                related_projects.extend(parse_yaml_list(fm, 'related_projects'))
            canonical_refs: list[str] = []
            for ref in related_projects:
                canonical = alias_map.get(ref) or alias_map.get(ref.lower())
                if not canonical:
                    invalid_project_refs.append(f'{note_rel}: {ref}')
                    continue
                canonical_refs.append(canonical)
                expected_by_project[canonical].add(note_rel)
            if canonical_refs and fm is not None:
                desired_refs = sorted(set(canonical_refs))
                current_refs = parse_yaml_list(fm, 'related_projects')
                if current_refs != desired_refs:
                    new_fm = set_yaml_list(fm, 'related_projects', desired_refs)
                    if not args.dry_run:
                        note.write_text(update_frontmatter(text, new_fm), encoding='utf-8')
                    knowledge_updates += 1

    for project_ref, info in project_infos.items():
        desired = sort_knowledge_paths(expected_by_project.get(project_ref, set()) | info.related_paths)
        body_text = read_text(info.brief_path)
        _, body = parse_frontmatter(body_text)
        _, current = extract_paths_from_related_section(body, info.section_title)
        if current != desired:
            if not args.dry_run:
                info.brief_path.write_text(replace_related_section(body_text, info.section_title or '## Related Knowledge', desired), encoding='utf-8')
            project_brief_updates += 1

    index_text = read_text(projects_index)
    index_map = parse_projects_index(index_text)
    for project_ref, info in project_infos.items():
        desired = sort_knowledge_paths(expected_by_project.get(project_ref, set()) | info.related_paths)
        current = sort_knowledge_paths(index_map.get(project_ref, set()))
        if current != desired:
            if not args.dry_run:
                index_text = replace_projects_index_block(index_text, project_ref, desired)
            projects_index_updates += 1
    if not args.dry_run and projects_index_updates:
        projects_index.write_text(index_text, encoding='utf-8')

    print(f'knowledge_updates: {knowledge_updates}')
    print(f'project_brief_updates: {project_brief_updates}')
    print(f'projects_index_updates: {projects_index_updates}')
    print(f'invalid_project_refs: {len(invalid_project_refs)}')
    print(f'invalid_paths: {len(invalid_paths)}')
    print(f'normalized_paths: {len(normalized_paths)}')
    if invalid_project_refs:
        print('invalid_project_refs_detail:')
        for item in invalid_project_refs:
            print(f'  - {item}')
    if invalid_paths:
        print('invalid_paths_detail:')
        for item in invalid_paths:
            print(f'  - {item}')
    if normalized_paths:
        print('normalized_paths_detail:')
        for item in normalized_paths:
            print(f'  - {item}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
