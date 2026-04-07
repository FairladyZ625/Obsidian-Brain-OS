---
name: conversation-mining
description: 统一检索和使用 Claude Code / Codex / AntiGravity 的历史对话。支持按日期、关键词、会话 ID、Conversation Reference、Conversation Prompt 找回原文，也支持在用户明确要求时，对指定会话或某天会话做提炼、总结、笔记整理。
---

# Conversation Mining

## What This Skill Does

- 找回某天 / 某条 / 某组历史对话
- 读取 `Conversation Reference` / `Conversation Prompt`
- 打开或更新本地对话查看器
- 在用户明确要求时，对指定会话做总结、提炼、笔记整理
- 翻译 AI 对话为人类可读的结构化摘要（翻译模式）

## Modes

### 搜索模式

- 默认模式
- 优先保留原文，不抢先摘要
- 适合：找回灵感、找原句、找上下文、找某天讨论

### 提炼模式

- 只有用户明确说“总结 / 提炼 / 整理笔记”时使用
- 必须基于明确范围：
  - 会话 ID
  - 日期
  - Conversation Reference
  - Conversation Prompt
  - 用户指定的一组会话

### 翻译模式

- 触发条件：用户粘贴对话文本片段并说"翻译/看不懂/解释/人话"，或给对话 ID + 翻译请求
- 典型场景：用户在 Codex / Claude / AG 里看不懂一段对话，复制过来让你翻译

#### 流程

1. **导出最新对话**：运行 `python3 {{CLAUDE_HOME}}/skills/conversation-mining/export_all.py --days 7`，确保索引包含近一周内容（`--days 0` 会导出空列表，不要用）
2. **定位会话**（优先使用搜索索引）：
   - 先读 `{{CLAUDE_HOME}}/exported_conversations/search_index.json`，在 entries 中按 keywords/title 模糊匹配关键词（纯 JSON 读取，毫秒级）
   - 如果索引不够精确 → 再 fallback 到 `conversations.json` 的 messages 全文搜索，或在 `{{TRANSCRIPT_DIR}}/` 下的 md 文件中 Grep 搜索
   - 如果用户给了对话 ID（如 `codex-20260327-e35f554d`）→ 在 `conversations.json` 中按 id 字段查找
   - 取匹配度最高的会话
3. **读取完整 transcript**：从定位到的会话的 `transcript_path` 读取完整 markdown
4. **结合项目上下文翻译**：用 Grep/Read 查阅项目代码，理解术语实际含义

#### 输出结构

```markdown
## 核心意图
（一句话说清楚这段对话在做什么）

## 关键决策
| 决策 | 理由 | 状态 |
|------|------|------|
| ... | ... | 已确认/待定 |

## 架构图（如果涉及）
（用 Mermaid 或 ASCII 画图）

## 下一步行动
1. ...
2. ...

## 未决事项
- ...
```

#### 术语对照

- 项目特有术语（如 "106W" / "Nomos-era" / "projection primitives"）必须用 Grep/Read 查阅项目代码确认实际含义，不能猜测
- 在输出中附上：术语 → 实际对应的文件/函数/概念

## Main Files

- 导出脚本：`{{CLAUDE_HOME}}/skills/conversation-mining/export_all.py`
- 查看器：`{{CLAUDE_HOME}}/skills/conversation-mining/viewer.html`
- 索引：`{{CLAUDE_HOME}}/exported_conversations/conversations.json`

## Common Commands

```bash
python3 {{CLAUDE_HOME}}/skills/conversation-mining/export_all.py
python3 {{CLAUDE_HOME}}/skills/conversation-mining/export_all.py --date 2026-03-18
python3 {{CLAUDE_HOME}}/skills/conversation-mining/export_all.py --days 7
```

## Guidance

- 如果用户要”找”，先定位再给原文
- 如果用户要”总结”，先明确范围再总结
- 如果用户已经给了 `Conversation Reference` / `Conversation Prompt`，优先按它的 `conversation id` 和 transcript 路径处理
- AntiGravity 内容提取是尽力模式，部分会话可能只有标题或摘要

## 新增：增量导出 + 搜索索引

- 导出脚本现在支持增量模式：第二次运行 `--days 7` 只重写有变化的 transcript，不变化的不重写
- 每次导出自动生成 `search_index.json`（轻量关键词索引），搜索时优先用它而不是全量 Grep
- `--clean` 参数可清理 conversations.json 中不存在的孤立 transcript 文件
