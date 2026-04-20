# Getting Started with Obsidian Brain OS

> Your AI-augmented personal context system. From zero to running in 30 minutes.

---

## What You're Building

Brain OS turns Obsidian into a **living personal context system** — not just a note-taking app, but a workspace where AI agents actively process, connect, and surface your knowledge overnight.

After setup:
- You capture things once (articles, thoughts, todos)
- AI processes them while you sleep (nightly pipeline at 02:00-04:00)
- You wake up to a curated digest, organized knowledge, and a daily briefing

---

## Prerequisites

| Tool | Purpose | Required? |
|------|---------|-----------|
| [Obsidian](https://obsidian.md) | Your vault UI | ✅ Yes |
| [OpenClaw](https://docs.openclaw.ai) | AI scheduling + cron | ✅ For nightly pipeline |
| Git | Version control for vault | ✅ Recommended |
| Python 3.8+ | Some scripts | ✅ For full pipeline |
| `convs` CLI | Export AI conversations | Optional |

---

## Day-one recommendation

If this is your first time, do **not** start with the full system.

Use:
- **Minimal** if you mainly want knowledge capture and organization
- **Standard** if you also want personal ops soon
- **Advanced** only if you explicitly want the full multi-agent operating system

See [install profiles](install-profiles.md).

---

## Step 1: Clone the repo

```bash
git clone https://github.com/FairladyZ625/Obsidian-Brain-OS.git
cd Obsidian-Brain-OS
```

If you want an AI agent to do the install for you, stop here and use:
- [INSTALL_FOR_AGENTS.md](../INSTALL_FOR_AGENTS.md)

---

## Step 2: Run setup first

The recommended path is:

```bash
bash setup.sh
```

Or, if you want an agent-friendly unattended path:

```bash
bash setup.sh --non-interactive --profile minimal
```

This will guide you through:
- vault path
- user info
- workspace path
- skills path
- optional extras
- basic verification

If you prefer to inspect profiles before running setup, read [install profiles](install-profiles.md).

---

## Step 3: Open your vault

After setup completes, open Obsidian → **File → Open Vault** → select your chosen vault path.

---

## Step 4: Verify the install

Run:

```bash
bash scripts/verify-install.sh
```

This checks:
- config exists
- required values are set
- vault structure exists
- selected skills are present
- core scripts run
- PII scan passes

If verification fails, fix the failing step before enabling more modules.

---

## Step 5: Choose Your Installation Profile

### 🧠 Profile A: Knowledge System Only
Best for: building a personal knowledge base, organizing research

Install these skills:
- `skills/article-notes-integration/`
- `skills/deep-research/`
- `skills/recommended/planning-with-files/`
- `skills/recommended/brainstorming/`

Set up these cron jobs (from `cron-examples/nightly-pipeline.json`):
- `article-notes-integration-nightly` (02:00)
- `knowledge-lint-weekly` (Monday 01:00)

### 📋 Profile B: Personal Ops Only
Best for: AI-powered daily planning, todo management

Install these skills:
- `skills/personal-ops-driver/`

Set up these cron jobs (from `cron-examples/personal-ops.json`):
- `personal-ops-morning-brief` (07:00 daily)
- `personal-ops-todo-reminder-1500` (15:00 daily)
- `personal-ops-weekly-plan` (Monday 05:10)

### 🌙 Profile C: Full Nightly Pipeline
Best for: maximum automation, compound knowledge growth

Install all skills + all cron jobs. See [Nightly Pipeline docs](nightly-pipeline.md) for details.

---

## Step 6: Install or expand skills

If you used `bash setup.sh`, your chosen skills may already be installed.

If you want to add more manually, copy only the skills you actually need:

```bash
cp -r skills/article-notes-integration/ ~/.agents/skills/
cp -r skills/personal-ops-driver/ ~/.agents/skills/
```

Avoid installing the entire tree unless you know you want the full system.

---

## Step 7: Set Up Cron Jobs (OpenClaw)

```bash
# Import nightly pipeline jobs
openclaw cron import cron-examples/nightly-pipeline.json

# Import personal ops jobs
openclaw cron import cron-examples/personal-ops.json
```

Or manually edit `~/.openclaw/cron/jobs.json` following the format in `cron-examples/`.

> ⚠️ Before enabling: replace all `{{PLACEHOLDER}}` values in the cron config files.

---

## Step 8: Expand only after one success

Good first successes:
- open the vault in Obsidian
- run `bash scripts/verify-install.sh`
- add one article note
- enable one relevant cron profile

Only after that should you decide whether to enable Observer, CI/CD, QMD, or the full nightly system.

---

## Step 9: Enable Observer (Optional, v0.5+)

Observer is your AI team's daily health monitor. It runs automatically and produces improvement suggestions.

```bash
# 1. Edit the observer cron prompt
nano prompts/cron/observer-daily-0001.md

# 2. Set enabled: true
# 3. Replace {{YOUR_CHANNEL_ID}} with your Discord channel (or remove announce)
# 4. Add to OpenClaw cron jobs
openclaw cron import prompts/cron/observer-daily-0001.md
```

Read [Observer Playbook](agent-playbooks/observer-playbook.md) for full configuration details.

---

## Step 10: Set Up CI/CD (Optional, v0.5+)

If you host your vault on GitHub, enable automatic quality checks:

```bash
# After pushing to GitHub:
# 1. Go to Settings → Branches → main → Branch protection
# 2. Require: PII scan + Structure check pass before merge
# 3. These workflows run automatically on every PR:
#    - .github/workflows/pii-scan.yml
#    - .github/workflows/structure-check.yml
#    - .github/workflows/changelog-check.yml
```

Read [Release Playbook](agent-playbooks/release-playbook.md) for the complete release process.

---

## Your First Week

**Day 1:** Open Obsidian, explore the vault structure, read `00-INBOX/README.md`

**Day 2:** Add 3-5 article links to `03-KNOWLEDGE/02-WORKING/01-ARTICLE-NOTES/`. Let the AI process them that night.

**Day 3:** Check `03-KNOWLEDGE/01-READING/04-DIGESTS/` for your first nightly digest.

**Day 4-7:** Add todos to `00-INBOX/todo-backlog.md`. Check your morning briefing in `01-PERSONAL-OPS/01-DAILY-BRIEFS/`.

---

## Troubleshooting

See [FAQ](faq.md) for common issues.

- Obsidian doesn't show vault → check vault path is a directory, not a file
- Scripts fail → source `scripts/config.env` first
- Cron jobs not running → verify OpenClaw is running (`openclaw gateway status`)
- Knowledge lint finds nothing → confirm `BRAIN_PATH` points to vault root
- PII scan fails → read [PII Deidentification Guide](references/pii-deidentification-guide.md)
- Want to see everything included? → read [Component Guide (⭐)](component-guide.md)
- Want to understand installation layers first? → read [install profiles](install-profiles.md)
- Want an AI agent to do the install? → read [INSTALL_FOR_AGENTS.md](../INSTALL_FOR_AGENTS.md)
- Want to contribute? → read [Release Playbook](agent-playbooks/release-playbook.md)
