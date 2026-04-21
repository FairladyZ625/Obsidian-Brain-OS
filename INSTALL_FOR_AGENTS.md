# Brain OS Installation Guide for AI Agents

Read this file first, then install Brain OS step by step.

Goal: get the user to a **working minimal setup first**, then expand only if needed.

This repo is a **digital twin + second brain + multi-agent workflow system** built around:
- an Obsidian vault template
- OpenClaw-compatible skills and cron examples
- scripts for setup, validation, and ongoing operation

Do **not** start by explaining the full architecture. Install the minimum working version first.

---

## Default rule

Unless the user explicitly asks for the full system, choose:

> **Profile: Minimal**

Minimal means:
- create the vault from `vault-template/`
- write config values
- install only core skills
- verify the install
- point the user to the next 1-2 docs only

Do **not** enable advanced modules by default:
- Observer
- CI/CD workflows
- conversation-mining
- full nightly pipeline
- QMD setup
- governance cron stack

These come later.

---

## Step 1: Ask 4 short questions

Ask these one by one, not as a giant form.

1. **What do you want first?**
   - knowledge system
   - personal ops
   - nightly automation
   - full system

2. **Do you already have an Obsidian vault?**
   - yes, I already have one
   - no, start fresh

3. **Will you use OpenClaw cron now?**
   - yes
   - not yet

4. **How hands-on do you want this install to be?**
   - agent does most of it
   - guide me step by step

Then map to an install profile.

---

## Step 2: Pick an install profile

Use `docs/install-profiles.md`.

### Default
- if unclear: **Minimal**

### If the user mainly wants a personal knowledge base
- choose **Minimal**

### If the user clearly wants daily planning and reminders too
- choose **Standard**

### If the user explicitly asks for the full multi-agent / nightly / governance setup
- choose **Advanced**

Do not silently upgrade them to a larger profile.

---

## Step 3: Clone the repo

```bash
git clone https://github.com/FairladyZ625/Obsidian-Brain-OS.git
cd Obsidian-Brain-OS
```

Verify:
- the repo exists locally
- `README.md`, `setup.sh`, `vault-template/`, `skills/`, and `docs/` are present

---

## Step 4: Collect required values

You need these values before setup:

- `BRAIN_PATH` - where the user's vault should live
- `USER_NAME` - how the system refers to the user
- `TIMEZONE` - e.g. `Asia/Shanghai`
- `WORKSPACE_PATH` - usually `~/.openclaw/workspace`
- `SKILLS_PATH` - usually `~/.agents/skills`

Optional:
- language
- transcript directory
- whether to install Observer later
- whether to enable cron later

Important:
- the vault folder name is user-defined
- it does **not** need to match the maintainer's personal vault naming

---

## Step 5: Run setup

### Recommended path today

Run the installer:

```bash
bash setup.sh
```

If the repo version supports non-interactive install, prefer:

```bash
bash setup.sh --non-interactive --profile minimal
```

If you are acting as an agent, help the user answer the prompts clearly and keep the install moving.

### What setup should accomplish

It should:
- copy `vault-template/` into the target vault path
- write `scripts/config.env`
- install selected skills
- optionally prepare extras
- run install checks

If setup fails, do not guess. Read the error and fix the broken step directly.

---

## Step 6: Install only the right amount of skills

Use the selected profile from `docs/install-profiles.md`.

### Minimal
Install only the smallest useful set.

Suggested default:
- `skills/brain-os-installer/`
- `skills/article-notes-integration/`
- `skills/personal-ops-driver/` only if the user asked for planning / todo support

### Standard
Install the core knowledge + personal ops skills.

### Advanced
Install the full set only when the user actually wants the full operating system.

Avoid “install everything” unless explicitly requested.

---

## Step 7: Configure only one small workflow first

Important: do not jump straight from install to the full governance stack.

The governance cron stack is:
- `prompts/cron/qmd-index-refresh-daily.md`
- `prompts/cron/knowledge-librarian-3day.md`
- `prompts/cron/knowledge-governance-10day.md`

Only introduce these after the user already has a working minimal knowledge workflow.

The user should feel one success quickly.

### Good first wins
- open the vault in Obsidian
- add one article note
- run one knowledge script
- enable one cron profile

If the user is on OpenClaw and wants scheduling, import only the smallest relevant cron example first.

Examples live in:
- `cron-examples/`

Do not enable the whole nightly system by default.

---

## Step 8: Verify

After install, verify at least these:

1. the vault exists and contains the template folders
2. `scripts/config.env` exists and has real values
3. the selected skills were copied into the skills directory
4. the user can open the vault in Obsidian
5. at least one script or workflow runs without immediate failure

For manual verification, use:

```bash
bash scripts/knowledge-lint.sh <vault-path>
bash scripts/check-pii.sh --strict
```

If a dedicated install verifier exists, run that too.

---

## Step 9: Hand off the next 2 docs only

If the user asks how Brain OS grows beyond ingestion, point them to docs that explain staged expansion, not just installation.

Do not dump the whole docs tree on the user.

After a successful minimal install, point them to:

1. `docs/component-guide.md`
2. one of:
   - `docs/getting-started.md`
   - `docs/agents.md`
   - `docs/personal-ops.md`
   - `docs/nightly-pipeline-guide.md`

Choose based on what they asked for.

---

## Profile-specific routing

### If the user wants mainly knowledge capture and organization
Read next:
- `docs/getting-started.md`
- `docs/component-guide.md`

### If the user wants daily planning / todo / reminders
Read next:
- `docs/personal-ops.md`
- `docs/agents.md`

### If the user wants multi-agent coordination and boundaries
Read next:
- `docs/agents.md`
- `docs/architecture.md`

### If the user wants nightly automation
Read next:
- `docs/nightly-pipeline-guide.md`
- `docs/nightly-pipeline.md`

---

## What not to do

Do not:
- start with a long theory lecture
- install advanced modules without asking
- enable every cron job at once
- tell the user to read 10 docs before first success
- assume they need the full system because it exists

---

## Success criteria

The install is successful when:
- the vault exists
- config is written
- the right skills are installed
- one small workflow works
- the user knows the next 1-2 docs to read

That is enough for day one.
