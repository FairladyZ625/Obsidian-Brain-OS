# Release Playbook / 发版操作手册

> **English:** This is the complete release SOP for Obsidian Brain OS maintainers and contributors. Follow this playbook every time you publish a new version.
>
> **中文：** 这是 Obsidian Brain OS 维护者和贡献者的完整发版 SOP。每次发版都按此手册执行。

---

## Overview / 概览

Brain OS uses **Semantic Versioning** (`MAJOR.MINOR.PATCH`). The release process ensures every change goes through PII scanning, structure validation, bilingual documentation, and CI verification before reaching users.

Brain OS 使用**语义化版本号**（`MAJOR.MINOR.PATCH`）。发版流程确保每个变更都经过 PII 扫描、结构验证、双语文档和 CI 验证后才能触达用户。

---

## Version Bump Rules / 版本号规则

| Change type / 变更类型 | Bump / 升级 | Example / 示例 |
|------------------------|-------------|----------------|
| Bug fixes, doc updates, minor tweaks / Bug 修复、文档更新、小调整 | `patch` (0.x.x) | 0.4.0 → 0.4.1 |
| New skill, script, cron prompt / 新增 skill、脚本、cron prompt | `minor` (x.X.0) | 0.4.0 → 0.5.0 |
| Breaking change to vault structure, setup.sh, or core contracts / vault 结构、setup.sh 或核心契约的重大变更 | `major` (X.0.0) | 0.x.0 → 1.0.0 |

Read `CHANGELOG.md` first to determine current version.

先读 `CHANGELOG.md` 确认当前版本。

---

## Release Steps / 发版步骤

### Step 1: PII Scan / PII 扫描（必做，不可跳过）

```bash
bash scripts/check-pii.sh
```

If any hits found → fix before proceeding.
如有命中 → 先修复再继续。

### Step 2: Structure Check / 结构检查

- Every new skill must have `skills/<name>/SKILL.md`
- Every new script must have a shebang (`#!/usr/bin/env bash` or python3)
- No hardcoded absolute paths in scripts
- 每个 skill 必须有 SKILL.md
- 每个脚本必须有 shebang
- 脚本中不能硬编码绝对路径

### Step 3: Update CHANGELOG / 更新变更日志（双语）

Update BOTH files:
同时更新两个文件：

1. `CHANGELOG.md` (English)
2. `CHANGELOG_CN.md` (中文)

Each entry must be bilingual: English line + Chinese line for every item.
每条目必须中英对照。

### Step 4: Commit & Push / 提交与推送

```bash
git checkout -b feat/<short-description>
git add -A
git commit -m "<type>(<scope>): <summary>"
git push origin feat/<short-description>
```

### Step 5: Open PR / 创建 PR（强制中英双语模板）

PR body MUST use the bilingual template (see `brain-os-release` Skill Step 5).
PR body 必须使用中英双语模板（见 `brain-os-release` Skill 步骤 5）。

### Step 6: Wait for CI / 等待 CI 通过

Three checks run automatically:
三个检查自动运行：

| Check / 检查 | Block merge? / 阻断合并？ |
|---|:---:|
| PII scan / PII 扫描 | ✅ Yes / 是 |
| Structure check / 结构检查 | ✅ Yes / 是 |
| CHANGELOG check / 变更日志检查 | ⚠️ Warn only / 仅警告 |

All blocking checks must pass.
所有阻断性检查必须通过。

### Step 7: Merge & Tag / 合并与打标签

```bash
# Merge via GitHub UI (squash merge recommended)
# Then locally:
git checkout main && git pull origin main
git tag vX.Y.Z
git push origin vX.Y.Z
```

---

## Common Pitfalls / 常见陷阱

1. **Forgetting CHANGELOG_CN.md** — Always update both changelogs. CI won't catch this yet; it's a manual discipline.
   **忘记更新 CHANGELOG_CN.md** — 两个 changelog 都要更新。CI 目前不自动检测，靠自觉。
2. **PII in docs** — Documentation files can contain example paths that look like real paths. Use `/tmp/`, `/home/user/`, or `{{PLACEHOLDER}}`.
   **文档中的 PII** — 文档里的示例路径可能像真实路径。用 `/tmp/`、`/home/user/` 或 `{{占位符}}`。
3. **Template tokens in scripts** — `{{BRAIN_ROOT}}` etc. are fine in `.md` files but NOT in `.sh`/`.py` runtime scripts. The PII scanner enforces this.
   **脚本中的模板 token** — `{{BRAIN_ROOT}}` 等在 `.md` 文件里没问题，但在 `.sh`/`.py` 运行脚本里不行。PII 扫描器会强制检查。
4. **Monolingual PR descriptions** — Community is international. Always write PR bodies in both Chinese and English.
   **单语 PR 描述** — 社区是国际化的。PR 描述必须中英双语。
