# Brain OS 的 OpenClaw 配置指南

> English version: [docs/openclaw-config-guide.md](../openclaw-config-guide.md)

Brain OS 使用 OpenClaw 作为 agent runtime、定时调度和频道路由层。OpenClaw 的主配置文件通常在：

```text
~/.openclaw/openclaw.json
```

这个文件会比较复杂，因为它同时管理模型默认值、agent 身份、频道凭证、Discord 路由和多频道 agent 绑定。Brain OS 提供了两个起步示例：

```text
examples/openclaw/openclaw.example.json
examples/openclaw/openclaw.multi-channel.example.json
```

只复制你需要的部分。不要把真实 token、用户 ID、频道 ID 或私有路径提交进 git。

---

## 最小配置

如果你只需要一个 main agent 和一个 Discord server，用：

```text
examples/openclaw/openclaw.example.json
```

它示范了：

- 一个默认 `main` agent
- Discord bot token 从 `DISCORD_BOT_TOKEN` 环境变量读取
- 一个 allowlist Discord server
- owner allowlist
- native slash command 默认配置
- 将该 server 的 Discord 消息兜底路由到 `main`

典型流程：

```bash
export DISCORD_BOT_TOKEN="your-token"
cp examples/openclaw/openclaw.example.json ~/.openclaw/openclaw.json
# 启动前先替换所有占位符
openclaw gateway restart
openclaw status
```

必须替换的占位符：

| 占位符 | 含义 |
|---|---|
| `{{USER_HOME}}` | 你的 home 目录 |
| `{{TIMEZONE}}` | IANA 时区，例如 `Asia/Shanghai` |
| `your-main-model` | 主模型，例如 `openai-codex/gpt-5.4` |
| `{{FALLBACK_MODEL}}` | 低成本 fallback 模型 |
| `{{DISCORD_GUILD_ID}}` | Discord server/guild ID |
| `{{DISCORD_OWNER_USER_ID}}` | 你的 Discord user ID |

---

## 多频道配置

如果你希望不同 Discord 频道路由到不同 agent，用：

```text
examples/openclaw/openclaw.multi-channel.example.json
```

示例包含：

| Agent | 适合频道 |
|---|---|
| `main` | 兜底 / 总协调 |
| `knowledge` | 知识处理、文章沉淀、检索 |
| `personalops` | Daily Briefing、待办、提醒 |
| `chronicle` | 被动频道历史记录 |

路由由 `bindings` 控制：

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

顺序很重要：先写具体频道绑定，最后再写 guild 级兜底绑定到 `main`。

---

## Discord 注意事项

1. Bot token 放在环境变量或 SecretRef，不要硬编码。
2. 团队 / 共享 server 建议保留 `requireMention: true`。只有私有 server 且希望 bot 回复每条消息时，才改成 `false`。
3. Discord guild channel 默认是按频道隔离 session，有助于减少上下文串台。
4. 长期私有记忆不应该默认暴露到群频道；需要时用 memory tools 按需检索。

---

## Cron 投递和频道路由是两件事

`openclaw.json` 负责把聊天消息路由到 agent。Cron jobs 在单独文件里：

```text
~/.openclaw/cron/jobs.json
```

Brain OS 的 cron 模板在：

```text
cron-examples/nightly-pipeline.json
cron-examples/personal-ops.json
cron-examples/governance.json
```

每个 cron job 可以单独指定投递频道：

```json
{
  "delivery": {
    "mode": "announce",
    "channel": "discord",
    "to": "{{CHANNEL_ID}}"
  }
}
```

你可以给 nightly pipeline、personal ops、governance report 分别配置不同的 Discord channel ID。

---

## QMD 边界

QMD 不是 OpenClaw 自带组件。它是需要单独安装和配置的本地检索引擎。

Brain OS 推荐在 QMD 可用时，把它作为语义检索后端，尤其适合 conversation mining 和大型 vault 检索。如果 QMD 没装，Brain OS pipeline prompt 应该进入 degraded mode，并回退到关键词检索。

实用配置规则：

1. 先单独安装 QMD。
2. 验证 CLI 可用，例如 `qmd status` 或你的 QMD 二进制命令。
3. 把 QMD binary 放进 `PATH`，或为 Brain OS 脚本设置 `QMD_BIN` / `QMD_BIN_REAL`。
4. 不要告诉用户“QMD 随 OpenClaw 默认安装”。

见 [QMD 向量检索配置指南](qmd-setup.md)。

---

## 验证清单

重启 OpenClaw 前：

```bash
# 不应残留未替换占位符
rg "\{\{" ~/.openclaw/openclaw.json

# JSON 有效
python3 -m json.tool ~/.openclaw/openclaw.json >/dev/null

# Gateway 能读取配置
openclaw status
```

重启后：

```bash
openclaw gateway restart
openclaw gateway status
```

然后在每个 Discord 频道发一条测试消息，确认路由到了预期 agent。
