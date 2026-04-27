# OpenClaw Setup — AI Scheduling and Cron Configuration

---

## What OpenClaw Provides

[OpenClaw](https://docs.openclaw.ai) is the AI scheduling layer that powers Brain OS's nightly pipeline and personal ops automation.

With OpenClaw:
- **Cron jobs** run AI tasks on schedule (02:00-04:00 pipeline, 07:00 morning brief)
- **Isolated sessions** prevent pipeline runs from polluting your main conversation
- **Skills** give AI agents specialized instructions for each task
- **Channel routing** maps Discord/Slack/etc. channels to the right agent
- **Retrieval integration** lets agents use external search backends such as QMD when installed

---

## Installation

```bash
# Install OpenClaw (macOS / Linux)
npm install -g @openclaw/cli

# Initialize
openclaw init

# Start the gateway daemon
openclaw gateway start

# Verify
openclaw status
```

---

## Skills Setup

Before you start: your vault name is user-defined. In Brain OS docs, `BRAIN_PATH` or `{{BRAIN_ROOT}}` means your own vault root path, not a fixed folder name.

Copy the Brain OS skills to your OpenClaw skills directory:

```bash
# Core skills (required for nightly pipeline)
cp -r skills/article-notes-integration/ ~/.agents/skills/
cp -r skills/conversation-knowledge-flywheel/ ~/.agents/skills/
cp -r skills/knowledge-flywheel-amplifier/ ~/.agents/skills/
cp -r skills/personal-ops-driver/ ~/.agents/skills/

# Optional skills
cp -r skills/deep-research/ ~/.agents/skills/
cp -r skills/notebooklm/ ~/.agents/skills/

# Recommended general-purpose skills
cp -r skills/recommended/*/ ~/.agents/skills/
```

### Replace Placeholders

After copying, replace `{{PLACEHOLDER}}` values in each skill:

```bash
# Example: replace all placeholders in a skill
cd ~/.agents/skills/article-notes-integration/
sed -i '' 's|/tmp/brain-os-test/vault|/path/to/your/vault|g' SKILL.md
sed -i '' 's|Alex|Your Name|g' SKILL.md
sed -i '' 's|CST|America/New_York|g' SKILL.md
```

---

## OpenClaw Config Examples

Before importing cron jobs, configure your agents and channels in `~/.openclaw/openclaw.json`.

Brain OS provides starter examples:

```text
examples/openclaw/openclaw.example.json
examples/openclaw/openclaw.multi-channel.example.json
```

Read [OpenClaw Config Guide](openclaw-config-guide.md) for multi-channel Discord routing, agent bindings, delivery targets, and QMD boundary notes.

---

## Cron Configuration

### Import Pre-built Configs

```bash
# Import nightly pipeline jobs
openclaw cron import cron-examples/nightly-pipeline.json

# Import personal ops jobs
openclaw cron import cron-examples/personal-ops.json
```

### Manual Setup

Edit `~/.openclaw/cron/jobs.json` directly. See `cron-examples/` for the full format.

### Required Placeholders

Before enabling any cron job, replace these in the config files. If you see `BRAIN_PATH` or `{{BRAIN_ROOT}}`, both refer to your own vault root path.

| Placeholder | Replace With | Example |
|-------------|-------------|---------|
| `/tmp/brain-os-test/vault` | Your vault path | `/home/user/my-brain` |
| `Alex` | Your display name | `Alex` |
| `CST` | Your timezone | `America/New_York` |
| `{{DISCORD_WEBHOOK_URL}}` | Your webhook URL | `https://discord.com/api/webhooks/...` |
| `{{DISCORD_CHANNEL_ID}}` | Your channel ID | `123456789012345678` |
| `{{AGENT_ID}}` | Your agent ID | Depends on your setup |

---

## Cron Job Reference

### Nightly Pipeline

| Job | Schedule | Timezone | Description |
|-----|----------|----------|-------------|
| `knowledge-lint-weekly` | `0 1 * * 1` | Your TZ | Weekly knowledge health check |
| `article-notes-integration-nightly` | `0 2 * * *` | Your TZ | Process new article notes |
| `conversation-knowledge-mining-nightly` | `0 3 * * *` | Your TZ | Mine AI conversations |
| `knowledge-flywheel-amplifier-nightly` | `0 4 * * *` | Your TZ | Cross-reference and amplify |
| `daily-knowledge-graph-canvas-0500` | `0 5 * * *` | Your TZ | Generate knowledge graph |

### Personal Ops

| Job | Schedule | Timezone | Description |
|-----|----------|----------|-------------|
| `personal-ops-morning-brief` | `0 7 * * *` | Your TZ | Generate daily cockpit |
| `personal-ops-todo-reminder-1500` | `0 15 * * *` | Your TZ | Afternoon progress check |
| `personal-ops-todo-reminder-2000` | `0 20 * * *` | Your TZ | Evening review prompt |
| `personal-ops-weekly-plan` | `10 5 * * 1` | Your TZ | Weekly plan (Monday) |
| `personal-ops-monthly-milestones` | `20 6 1 * *` | Your TZ | Monthly milestone review |

### Cron Schedule Order

```
01:00  Knowledge lint (weekly, Monday only)
02:00  Article integration
03:00  Conversation mining (reads Stage 1 output)
04:00  Knowledge amplification (reads Stages 1+2 output)
05:00  Knowledge canvas (optional visualization)
07:00  Morning brief
15:00  Afternoon reminder
20:00  Evening review
```

---

## Delivery Configuration

Cron jobs can deliver results to various channels:

### Discord (Webhook)
```json
{
  "delivery": {
    "mode": "webhook",
    "to": "https://discord.com/api/webhooks/YOUR_WEBHOOK_URL",
    "bestEffort": true
  }
}
```

### Discord (Channel)
```json
{
  "delivery": {
    "mode": "announce",
    "channel": "discord",
    "to": "YOUR_CHANNEL_ID"
  }
}
```

### No Delivery (Silent)
```json
{
  "delivery": {
    "mode": "silent"
  }
}
```

---

## Retrieval / QMD Configuration

QMD is not bundled with OpenClaw. Install QMD separately if you want semantic / hybrid retrieval for large vaults or conversation mining.

Brain OS agents can use QMD as the recommended retrieval backend when it is available. If QMD is missing, prompts should report degraded mode and fall back to keyword search.

See [QMD Semantic Search Setup](qmd-setup.md) and [OpenClaw Config Guide](openclaw-config-guide.md).

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| `openclaw: command not found` | Reinstall with `npm install -g @openclaw/cli` |
| Gateway won't start | Run `openclaw doctor` to diagnose |
| Cron jobs not firing | Check `openclaw gateway status` is running |
| Job fails with timeout | Increase `timeoutSeconds` in job config |
| Placeholder not replaced | Search for `{{` in cron config files |
