# brain-os-release

**Purpose:** Standard release process for Obsidian Brain OS. Follow this skill every time you merge changes and publish a new version — whether you're the maintainer or a contributor.

## When to use

- You have changes ready to merge into `main`
- You want to cut a new version (patch / minor / major)
- You're preparing a PR for review

---

## Step 0: Determine version bump

Use [Semantic Versioning](https://semver.org):

| Change type | Bump |
|-------------|------|
| Bug fixes, doc updates, minor tweaks | `patch` (0.3.x) |
| New skill, new script, new cron prompt | `minor` (0.x.0) |
| Breaking change to vault structure, setup.sh, or core skill contracts | `major` (x.0.0) |

Read `CHANGELOG.md` to find the current version before deciding.

---

## Step 1: PII check (mandatory, never skip)

Run the PII scan script before committing anything:

```bash
bash scripts/check-pii.sh
```

The script checks for:
- Absolute paths with real usernames (`/Users/yourname`, `/home/yourname`)
- Real names, Discord IDs, internal channel IDs
- Unresolved template tokens (`{{BRAIN_ROOT}}`, `{{USER_NAME}}` etc.)

**If any hits are found: fix them before proceeding.** Use placeholder variables or generic examples.

---

## Step 2: Structure check

For every new skill added, verify:
- `skills/<name>/SKILL.md` exists
- SKILL.md has a `## When to use` section
- If scripts are included, they have a usage comment at the top

For every new script:
- Has `#!/usr/bin/env bash` or `#!/usr/bin/env python3` shebang
- Has a comment block explaining purpose and required env vars
- Does not hardcode absolute paths

### Step 2.5: Doc & installer sync check (new in v0.5)

When adding **new features**, also check if these need updating:
- **`setup.sh`** — Does the new feature need an install step or config var?
- **`skills/brain-os-installer/SKILL.md`** — Does the installer need a new phase or option?
- **`docs/getting-started.md`** — Does the onboarding guide need a new section?
- **`docs/architecture.md`** — Does the architecture diagram need a new component?
- **README.md / README_CN.md** — Does the top-level feature list need updating?

Rule of thumb: if a user would wonder "how do I set this up?" after reading current docs, something needs updating.
This check is manual for now — add it to your PR review checklist.

---

## Step 3: Update CHANGELOG（双语，必须两份都更新）

每次发版必须同时更新两个文件：

1. **`CHANGELOG.md`**（英文版）— 新增条目在文件顶部
2. **`CHANGELOG_CN.md`**（中文版）— 同步新增中文对照条目

格式：

```markdown
## [X.Y.Z] — YYYY-MM-DD

### Added / 新增
- **`path/to/file`** — English description / 中文说明

### Changed / 变更
- ...

### Fixed / 修复
- ...
```

Rules:
- Every PR that touches `skills/`, `scripts/`, `prompts/`, or `setup.sh` must update BOTH changelogs
- Use present tense, imperative mood for English; use Chinese natural phrasing for CN version
- 两份内容必须一一对应，不能有遗漏
- Link to relevant files with backtick paths

---

## Step 4: Create branch and commit

```bash
git checkout -b feat/<short-description>
git add -A
git commit -m "<type>(<scope>): <summary>

<body: what changed and why>"
```

Commit types: `feat` / `fix` / `docs` / `refactor` / `chore`

---

## Step 5: Push and open PR（中英双语，强制模板）

```bash
git push origin feat/<short-description>
```

PR title format: `feat: vX.Y.Z — <one-line English summary>`

PR body **必须使用以下中英双语模板**：

```markdown
## 📋 更新概览 / Overview

### 中文
本次更新包含 [一句话中文总结]。

### English
This update includes [one-line English summary].

---

### 变更详情 / Changes

#### 🆕 新增 / Added
- **`path/to/file`** — 中文说明 / English description

#### 🔄 变更 / Changed
- ...

#### 🐛 修复 / Fixed
- ...

---

### PII 检查结果 / PII Check Result
✅ PII scan passed — 0 hits
```

---

## Step 6: CI checks

GitHub Actions will automatically run on every PR:

- **PII scan** — fails if private paths or unresolved tokens found
- **Structure check** — fails if new skill missing SKILL.md
- **CHANGELOG check** — warns if `skills/` or `scripts/` changed without CHANGELOG update

All checks must pass before merging.

---

## Step 7: Merge and tag

After PR is approved and CI passes:

```bash
# Merge via GitHub UI (squash merge preferred)
# Then locally:
git checkout main && git pull origin main
git tag vX.Y.Z
git push origin vX.Y.Z
```

---

## Notes for contributors

- This repo contains no secrets or personal data by design. If you find any, open an issue.
- The `{{PLACEHOLDER}}` convention is used throughout — replace with your own values, never commit real paths.
- When in doubt about PII, run `bash scripts/check-pii.sh` and check the output.
- **Bilingual rule**: All public-facing content (PR body, CHANGELOG, release notes) MUST be bilingual (Chinese + English). Commit messages stay in English per git convention.
