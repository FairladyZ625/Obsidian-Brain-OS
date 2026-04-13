# Skill Authoring Guide / Skill 编写指南

> **English:** How to write a well-structured skill for Brain OS — conventions, required fields, and best practices.
>
> **中文：** 如何为 Brain OS 编写结构良好的 skill——规范、必填字段和最佳实践。

---

## What is a Skill? / 什么是 Skill？

A **skill** is a reusable instruction package that tells an AI agent how to perform a specific type of task. Each skill lives in its own directory under `skills/`.
**skill** 是一套可复用的指令包，告诉 AI agent 如何执行特定类型的任务。每个 skill 位于 `skills/` 下的独立目录中。

```
skills/
└── <skill-name>/
    ├── SKILL.md              # Required: the skill definition
    ├── references/           # Optional: reference docs, templates
    │   ├── template.md
    │   └── api-reference.md
    └── scripts/              # Optional: helper scripts
        └── do-something.sh
```

---

## SKILL.md Structure / SKILL.md 结构

Every skill MUST have a `SKILL.md` at its root. This is the only file the system reads automatically.
每个 skill 根目录**必须**有 `SKILL.md`。这是系统自动读取的唯一文件。

### Required Fields / 必填字段

```yaml
---
name: skill-name-here                    # Unique slug / 唯一标识
description: >
  What this skill does, in 1-3 sentences.
  Can span multiple lines with `>`.
---
```

### Recommended Sections / 推荐章节

```markdown
# <Skill Name>

## Purpose / 目的
One sentence: what problem does this solve?
一句话：这个 skill 解决什么问题？

## When to use / 使用时机
- When you need to [do X]
- When [condition Y] is true
- NOT when [condition Z] (anti-pattern)

## Prerequisites / 前置条件
- [Tool or service needed]
- [Environment variable required]
- [File or directory that must exist]

## Steps / 步骤
### Step 1: ...
### Step 2: ...

## Output / 输出
What the user/agent gets after running this skill.
用户/agent 运行此 skill 后得到什么。

## Notes / 注意事项
Common pitfalls, edge cases, tips.
常见陷阱、边界情况、技巧。
```

---

## Naming Conventions / 命名规范

| Item / 项目 | Convention / 规范 | Example / 示例 |
|---|---|---|
| Directory / 目录 | kebab-case | `daily-timesheet/` |
| File name (SKILL) / 文件名（SKILL） | `SKILL.md` (exact case) | `SKILL.md` |
| Reference files / 参考文件 | kebab-case `.md` | `feishu-bitable.md` |
| Scripts / 脚本 | kebab-case `.sh` or `.py` | `check-pii.sh` |
| Cron prompts / cron prompt | kebab-case + time | `daily-timesheet-1730.md` |

---

## Description Field / Description 字段

The `description` in frontmatter is the most important metadata — it's how the skill discovery system matches skills to tasks.
frontmatter 中的 `description` 是最重要的元数据——它是技能发现系统将技能与任务匹配的方式。

### Good descriptions / 好的 description

```yaml
# ✅ Specific and actionable
description: >
  Scan git commits daily, align work to OKR milestones,
  generate structured timesheet draft for human confirmation.
  Supports local file, Feishu Bitable, and DingTalk backends.

# ✅ Clear trigger conditions
description: >
  Agent self-evolution observer. Collects session data and gateway logs,
  analyzes patterns, updates .learnings/ ledger,
  generates iteration plan. Three-level safety mechanism.
```

### Bad descriptions / 差的 description

```yaml
# ❌ Too vague
description: A useful tool for managing things

# ❌ Only mentions name, not behavior
description: The daily timesheet skill
```

---

## references/ Directory / references/ 目录

Use `references/` for supplementary materials that are too detailed for the main SKILL.md:
用 `references/` 存放对主 SKILL.md 来说太详细的补充材料：

| Content type / 内容类型 | Put in / 放在 | Example / 示例 |
|---|---|---|
| API reference / API 参考 | `references/<service>-<type>.md` | `feishu-bitable.md` |
| Output templates / 输出模板 | `references/<name>-template.md` | `plan-template.md` |
| Schema definitions / Schema 定义 | `references/<name>-schema.md` | `index-schema.md` |
| Configuration examples / 配置示例 | `references/<name>-examples.md` | — |

**Rule:** If it's longer than 50 lines and isn't part of the core flow, put it in `references/`.
**规则：** 如果内容超过 50 行且不是核心流程的一部分，就放 `references/`。

---

## Scripts in Skills / Skill 中的脚本

If your skill includes shell or Python scripts:
如果你的 skill 包含 shell 或 Python 脚本：

### Must have / 必须有

```bash
#!/usr/bin/env bash   # or python3
#
# <script-name> — one-line purpose
#
# Required env vars:
#   VAR_NAME - what it does (default: ...)
#
# Usage:
#   bash <script-name>.sh [--flags] [args]
#
# Exit codes:
#   0 - success
#   1 - error (see stderr)
```

### Must NOT have / 绝不能有

- Hardcoded absolute paths (`/Users/...`, `/home/...`)
  硬编码绝对路径
- Unresolved template tokens (`{{BRAIN_ROOT}}`) in runtime code
  运行代码中未解析的模板 token
- Silent failures (always exit non-zero on error)
  静默失败（出错时一定要非零退出）
- Secrets or tokens (use environment variables)
  密码或 token（用环境变量）

---

## PII Safety for Skills / Skill 的 PII 安全

Since skills are committed to a public repo:
由于 skill 会提交到公开仓库：

1. **No real paths** — use `{{USER_HOME}}`, `${BRAIN_ROOT}`, or `$HOME`
   **无真实路径** — 用 `{{USER_HOME}}`、`${BRAIN_ROOT}` 或 `$HOME`
2. **No real names** — use `{{USER_NAME}}`, "you", or "the user"
   **无真实姓名** — 用 `{{USER_NAME}}`、"you" 或 "用户"
3. **No internal IDs** — use `{{CHANNEL_ID}}`, `{{AGENT_NAME}}`
   **无内部 ID** — 用 `{{CHANNEL_ID}}`、`{{AGENT_NAME}}`
4. **Test before committing**: `bash scripts/check-pii.sh --strict`
   **提交前测试**：`bash scripts/check-pii.sh --strict`

---

## CI Requirements / CI 要求

When you add or modify a skill, these CI checks apply:
当你新增或修改 skill 时，以下 CI 检查会生效：

| Check / 检查 | Enforced? / 强制？ | What it verifies / 验证什么 |
|---|:---:|---|
| PII scan / PII 扫描 | ✅ Block merge / 阻断合并 | No private data in any file |
| Structure check / 结构检查 | ✅ Block merge / 阻断合并 | SKILL.md exists, scripts have shebang |
| CHANGELOG check / 变更日志检查 | ⚠️ Warn only / 仅警告 | Changelog updated |

---

## Examples / 示例

See existing skills for reference:
参考现有 skill：

| Skill / Skill | Type / 类型 | Good for learning / 适合学习 |
|---|---|---|
| `brain-os-release` / 发版 SOP | Process / 流程型 | Multi-step workflow with checklist |
| `observer` / 观察者 | Monitor / 监控型 | Data collection + safety gates |
| `daily-timesheet` / 工时单 | Tool / 工具型 | Script integration + multiple backends |
| `english-tutor` / 英语辅导 | Interactive / 交互型 | Voice I/O with external tools |
