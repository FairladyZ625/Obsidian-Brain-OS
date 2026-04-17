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

## Step 1: Clone and Set Up Your Vault

```bash
# Clone the repo
git clone https://github.com/FairladyZ625/Obsidian-Brain-OS.git
cd Obsidian-Brain-OS

# Copy the vault template to your preferred location
cp -r vault-template ~/my-brain

# Initialize your vault as a git repo
cd ~/my-brain
git init
git add .
git commit -m "init: Brain OS vault"
```

Then open Obsidian → **File → Open Vault** → select `~/my-brain`.

---

## Step 2: Configure Your Paths

```bash
# Copy the config template
cp scripts/config.env.example scripts/config.env

# Edit with your actual values
nano scripts/config.env
```

The key values to set:

```bash
BRAIN_PATH="$HOME/my-brain"          # Your vault location (user-defined, any folder name is fine)
USER_NAME="Your Name"                 # How AI refers to you
TIMEZONE="America/New_York"           # Your timezone (for nightly scheduling)
TRANSCRIPT_DIR="$HOME/transcripts"    # Where AI conversations are exported
```

`BRAIN_PATH` is your vault root. It does not need to be named `ZeYu-AI-Brain`.

---

## Step 3: Choose Your Installation Profile

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

## Step 4: Install Skills

Copy the skills you need to your OpenClaw skills directory:

```bash
# Copy core skills
cp -r skills/article-notes-integration/ ~/.agents/skills/
cp -r skills/personal-ops-driver/ ~/.agents/skills/

# Or install all recommended skills
cp -r skills/recommended/*/ ~/.agents/skills/
```

Then update the placeholder values in each `SKILL.md`:
- `/tmp/brain-os-test/vault` → your vault path
- `Alex` → your name
- `CST` → your timezone

---

## Step 5: Set Up Cron Jobs (OpenClaw)

```bash
# Import nightly pipeline jobs
openclaw cron import cron-examples/nightly-pipeline.json

# Import personal ops jobs
openclaw cron import cron-examples/personal-ops.json
```

Or manually edit `~/.openclaw/cron/jobs.json` following the format in `cron-examples/`.

> ⚠️ Before enabling: replace all `{{PLACEHOLDER}}` values in the cron config files.

---

## Step 6: Verify

```bash
# Test knowledge lint
bash scripts/knowledge-lint.sh ~/my-brain

# Test nightly digest initialization
bash scripts/init-nightly-digest.sh ~/my-brain

# Test PII scanner (v0.5+)
bash scripts/check-pii.sh --strict
# Expected: ✅ PII scan passed — 0 hits
```

---

## Step 7: Enable Observer (Optional, v0.5+)

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

## Step 8: Set Up CI/CD (Optional, v0.5+)

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
- Want to contribute? → read [Release Playbook](agent-playbooks/release-playbook.md)
