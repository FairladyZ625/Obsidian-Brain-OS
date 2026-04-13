# PII Deidentification Guide / PII 脱敏指南

> **English:** Complete guide to identifying, removing, and preventing PII (Personally Identifiable Information) in the Brain OS repository.
>
> **中文：** 在 Brain OS 仓库中识别、移除和防止 PII（个人身份信息）的完整指南。

---

## What Counts as PII? / 什么算 PII？

Brain OS's `check-pii.sh` scanner detects these categories:
Brain OS 的 `check-pii.sh` 扫描器检测以下类别：

| Category / 类别 | Pattern / 模式 | Example / 示例 | Risk / 风险 |
|---|---|---|---|
| Absolute paths with usernames / 含用户名的绝对路径 | `/Users/<name>/...` or `/home/<name>/...` | `/Users/alice/Documents/...` | 🔴 High |
| Unresolved template tokens (in scripts) / 脚本中未解析模板 token | `{{UPPER_CASE_TOKEN}}` | `{{BRAIN_ROOT}}` in a `.sh` file | 🟡 Medium |
| Discord-style IDs / Discord 风格 ID | 18-digit numbers | `123456789012345678` | 🟡 Medium |
| Real names / 真实姓名 | Personal names in content | "Alice", "李明" | 🔴 High |
| Internal channel IDs / 内部频道 ID | Discord channel snowflake IDs | `1475328660373372940` | 🔴 High |

### What is NOT PII / 什么不算 PII？

- `{{PLACEHOLDER}}` tokens in `.md` documentation files (these are intentional templates for users to fill in)
  `.md` 文档文件中的 `{{占位符}}`（这是故意留给用户填写的模板）
- Generic example paths like `/tmp/...`, `/home/user/...`, `~/`
  通用示例路径如 `/tmp/...`、`/home/user/...`、`~/`
- `$HOME` or environment variable references
  `$HOME` 或环境变量引用
- Public GitHub usernames in README / attribution
  README 或署名中的公开 GitHub 用户名

---

## The Scanner / 扫描工具

### Manual Run / 手动运行

```bash
bash scripts/check-pii.sh          # Normal mode: report only
bash scripts/check-pii.sh --strict # Strict mode: exits non-zero on any hit
```

### CI Integration / CI 集成

The `.github/workflows/pii-scan.yml` workflow runs `--strict` mode on every PR and push to main.
`.github/workflows/pii-scan.yml` 工作流在每次 PR 和 main 推送时以 `--strict` 模式运行。

**PII scan failure blocks merge.** This is by design — we never want private data reaching the public repo.
**PII 扫描失败会阻断合并。** 这是设计使然——我们绝不希望私有数据进入公开仓库。

---

## Deidentification Process / 脱敏流程

### Step 1: Identify / 识别

Run the scanner and review each hit:
运行扫描器并审查每条命中：

```bash
bash scripts/check-pii.sh --strict
```

### Step 2: Classify / 分类

For each hit, decide:
对每条命中，判断：

| Decision / 决定 | Action / 动作 |
|---|---|
| Real leak / 真实泄露 | Replace with placeholder immediately |
| Intentional template / 故意模板 | Exclude from scan (add to exclusion list) |
| False positive / 误报 | Update scanner rules if pattern is too broad |

### Step 3: Replace / 替换

Use these standard replacements:
使用以下标准替换：

| Original / 原始 | Replacement / 替换为 |
|---|---|
| `/Users/yourname/...` | `{{USER_HOME}}/...` or `$HOME/...` |
| `/home/yourname/...` | `{{USER_HOME}}/...` |
| Real name / 真实姓名 | `{{USER_NAME}}` or "you" / "用户" |
| Discord user ID / Discord 用户 ID | `{{DISCORD_USER_ID}}` |
| Discord channel ID / Discord 频道 ID | `{{CHANNEL_ID}}` |
| Agent name (internal) / Agent 名称（内部） | `{{MAIN_AGENT_NAME}}` etc. |
| Specific timezone / 特定时区 | System local timezone / 系统本地时区 |
| Private repo path / 私有仓库路径 | `{{BRAIN_ROOT}}` or `{{VAULT_PATH}}` |

### Step 4: Verify / 验证

```bash
bash scripts/check-pii.sh --strict
# Expected: ✅ PII scan passed — 0 hits
```

---

## Common PII Patterns & Fixes / 常见 PII 模式与修复

### Pattern 1: Hardcoded paths in scripts / 脚本中的硬编码路径

❌ Bad:
```bash
BRAIN_ROOT=/Users/alice/Documents/MyBrain
```

✅ Good:
```bash
BRAIN_ROOT="${BRAIN_ROOT:?Error: BRAIN_ROOT env var is required}"
```

### Pattern 2: Timezone hardcoding / 时区硬编码

❌ Bad:
```bash
TZ="Asia/Shanghai" date "+%Y-%m-%d"
```

✅ Good:
```bash
date "+%Y-%m-%d"  # Uses system local timezone
```

### Pattern 3: Internal identity references / 内部身份引用

❌ Bad:
```markdown
Notify Codex Main (ID: 1475340557059625222) in channel #main-hall
```

✅ Good:
```markdown
Notify {{MAIN_AGENT_NAME}} in {{MAIN_CHANNEL}}
```

### Pattern 4: Template tokens leaking into runtime scripts / 模板 token 泄漏到运行脚本

❌ Bad (in `.sh` file):
```bash
echo "Processing {{USER_NAME}}'s brain..."
```

✅ Good:
```bash
echo "Processing ${USER_NAME:-user}'s brain..."
```

---

## Exclusion Rules / 排除规则

The scanner excludes these patterns by default:
扫描器默认排除以下模式：

- Files matching `setup.sh`, `check-pii.sh` (intentional template hosts)
- Paths containing `prompts/`, `cron-examples/`, `skills/*/references/`
- Lines containing `/tmp/` or `/home/user/` (generic examples)

If you need to add exclusions, edit the `grep -vE` line in `scripts/check-pii.sh`.
如需添加排除规则，编辑 `scripts/check-pii.sh` 中的 `grep -vE` 行。

---

## Before Every PR / 每次 PR 前

Run this checklist:
运行此清单：

- [ ] `bash scripts/check-pii.sh --strict` → 0 hits
- [ ] No real names in any new/modified files
- [ ] No absolute paths with real usernames
- [ ] All `.sh`/`.py` files use env vars or placeholders
- [ ] Documentation uses `{{PLACEHOLDER}}` for user-configurable values
