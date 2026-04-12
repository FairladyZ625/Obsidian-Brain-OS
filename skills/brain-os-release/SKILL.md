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

---

## Step 3: Update CHANGELOG.md

Add a new entry at the top of `CHANGELOG.md`:

```markdown
## [X.Y.Z] — YYYY-MM-DD

### Added
- ...

### Changed
- ...

### Fixed
- ...
```

Rules:
- Every PR that touches `skills/`, `scripts/`, `prompts/`, or `setup.sh` must update CHANGELOG
- Use present tense, imperative mood: "Add X", not "Added X" or "Adds X"
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

## Step 5: Push and open PR

```bash
git push origin feat/<short-description>
```

PR title format: `feat: vX.Y.Z — <one-line summary>`

PR body must include:
1. Version number
2. Summary of changes (grouped by Added / Changed / Fixed)
3. PII check result: `✅ PII scan passed` or list of items reviewed
4. Any breaking changes clearly marked

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
