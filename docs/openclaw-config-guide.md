# OpenClaw Config Guide for Brain OS

> Chinese version: [docs/zh/openclaw-config-guide.md](zh/openclaw-config-guide.md)

Brain OS uses OpenClaw as the agent runtime, scheduler, and channel router. The main OpenClaw config file lives at:

```text
~/.openclaw/openclaw.json
```

This file can become complex because it combines model defaults, agent identities, channel credentials, Discord routing, and per-channel agent bindings. Brain OS provides starter examples under:

```text
examples/openclaw/openclaw.example.json
examples/openclaw/openclaw.multi-channel.example.json
```

Copy only the sections you need. Do not paste real tokens, user IDs, channel IDs, or private paths into files committed to git.

---

## Minimal setup

Use `examples/openclaw/openclaw.example.json` when you only need one main agent and one Discord server.

It demonstrates:

- one default `main` agent
- Discord bot token loaded from `DISCORD_BOT_TOKEN`
- one allowlisted Discord guild/server
- owner allowlist
- native slash command defaults
- a fallback route that sends all Discord guild traffic to `main`

Typical setup flow:

```bash
export DISCORD_BOT_TOKEN="your-token"
cp examples/openclaw/openclaw.example.json ~/.openclaw/openclaw.json
# edit placeholders before starting the gateway
openclaw gateway restart
openclaw status
```

Required placeholders:

| Placeholder | Meaning |
|---|---|
| `{{USER_HOME}}` | Your home directory |
| `{{TIMEZONE}}` | IANA timezone, e.g. `Asia/Shanghai` |
| `your-main-model` | Main model, e.g. `openai-codex/gpt-5.4` |
| `{{FALLBACK_MODEL}}` | Lower-cost fallback model |
| `{{DISCORD_GUILD_ID}}` | Discord server/guild ID |
| `{{DISCORD_OWNER_USER_ID}}` | Your Discord user ID |

---

## Multi-channel setup

Use `examples/openclaw/openclaw.multi-channel.example.json` when you want different Discord channels to route to different agents.

The example includes:

| Agent | Intended channel |
|---|---|
| `main` | fallback / general coordination |
| `knowledge` | knowledge processing, article notes, retrieval |
| `personalops` | daily briefing, todos, reminders |
| `chronicle` | passive channel history logging |

Routing is controlled by `bindings`:

```json
{
  "agentId": "knowledge",
  "match": {
    "channel": "discord",
    "guildId": "{{DISCORD_GUILD_ID}}",
    "peer": { "kind": "channel", "id": "{{KNOWLEDGE_CHANNEL_ID}}" }
  }
}
```

Ordering matters. Put specific channel bindings first, then a final guild-level fallback binding to `main`.

---

## Discord notes

1. Store your bot token as an environment variable or SecretRef. Do not hardcode it.
2. Keep `requireMention: true` for shared/team servers. Set it to `false` only in a private server where you want the bot to respond to every message.
3. Guild channels have separate sessions by channel, which helps prevent context bleed.
4. Long-term private memory is not automatically safe to expose in group channels. Use memory tools deliberately when needed.

---

## Cron delivery vs channel routing

`openclaw.json` routes inbound chat messages to agents. Cron jobs live separately under:

```text
~/.openclaw/cron/jobs.json
```

Brain OS cron templates are in:

```text
cron-examples/nightly-pipeline.json
cron-examples/personal-ops.json
cron-examples/governance.json
```

Each cron job can choose its delivery target independently:

```json
{
  "delivery": {
    "mode": "announce",
    "channel": "discord",
    "to": "{{CHANNEL_ID}}"
  }
}
```

Use different `{{CHANNEL_ID}}` values to send nightly pipeline, personal ops, and governance reports to different Discord channels.

---

## QMD boundary

QMD is not bundled with OpenClaw. It is a separately installed local retrieval engine.

Brain OS can use QMD as the recommended semantic retrieval backend when it is available, especially for conversation mining and large vault search. If QMD is not installed, Brain OS pipeline prompts should enter degraded mode and fall back to keyword search.

Practical setup rule:

1. Install QMD separately.
2. Verify the CLI works, for example `qmd status` or your installed QMD binary.
3. Put the QMD binary on `PATH`, or set `QMD_BIN` / `QMD_BIN_REAL` for Brain OS scripts that call QMD.
4. Do not tell users that QMD comes with OpenClaw by default.

See [QMD Semantic Search Setup](qmd-setup.md).

---

## Validation checklist

Before restarting OpenClaw:

```bash
# No unreplaced placeholders
rg "\{\{" ~/.openclaw/openclaw.json

# JSON is valid
python3 -m json.tool ~/.openclaw/openclaw.json >/dev/null

# Gateway can read config
openclaw status
```

After restart:

```bash
openclaw gateway restart
openclaw gateway status
```

Then send a test message in each Discord channel and confirm it routes to the expected agent.
