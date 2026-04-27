> 本文档为英文版的中译本。如有歧义，以英文原版为准。

# OpenClaw 配置 — AI 调度和 Cron 设置

---

## OpenClaw 提供什么

[OpenClaw](https://docs.openclaw.ai) 是驱动 Brain OS nightly pipeline 和个人事务自动化的 AI 调度层。

使用 OpenClaw：
- **Cron jobs** 按计划运行 AI 任务（02:00-04:00 pipeline、07:00 晨间简报）
- **隔离 session** 防止 pipeline 运行污染你的主对话
- **Skills** 给 AI agent 每个任务的专门指令
- **频道路由** 把 Discord / Slack 等频道映射到对应 agent
- **检索集成** 让 agent 在外部检索后端（如 QMD）已安装时使用它们

---

## 安装

```bash
# 安装 OpenClaw（macOS / Linux）
npm install -g @openclaw/cli

# 初始化
openclaw init

# 启动 gateway 守护进程
openclaw gateway start

# 验证
openclaw status
```

---

## Skills 设置

将 Brain OS skills 复制到你的 OpenClaw skills 目录：

```bash
# 核心 skills（nightly pipeline 必需）
cp -r skills/article-notes-integration/ ~/.agents/skills/
cp -r skills/conversation-knowledge-flywheel/ ~/.agents/skills/
cp -r skills/knowledge-flywheel-amplifier/ ~/.agents/skills/
cp -r skills/personal-ops-driver/ ~/.agents/skills/

# 可选 skills
cp -r skills/deep-research/ ~/.agents/skills/
cp -r skills/notebooklm/ ~/.agents/skills/

# 推荐的通用 skills
cp -r skills/recommended/*/ ~/.agents/skills/
```

### 替换占位符

复制后，替换每个 skill 中的 `{{PLACEHOLDER}}` 值：

```bash
# 示例：替换 skill 中的所有占位符
cd ~/.agents/skills/article-notes-integration/
sed -i '' 's|/tmp/brain-os-test/vault|/path/to/your/vault|g' SKILL.md
sed -i '' 's|Alex|Your Name|g' SKILL.md
sed -i '' 's|CST|America/New_York|g' SKILL.md
```

---

## OpenClaw 配置示例

导入 cron jobs 之前，先在 `~/.openclaw/openclaw.json` 中配置 agents 和 channels。

Brain OS 提供起步示例：

```text
examples/openclaw/openclaw.example.json
examples/openclaw/openclaw.multi-channel.example.json
```

多频道 Discord 路由、agent bindings、投递目标和 QMD 边界说明见 [OpenClaw 配置指南](openclaw-config-guide.md)。

---

## Cron 配置

### 导入预构建配置

```bash
# 导入 nightly pipeline jobs
openclaw cron import cron-examples/nightly-pipeline.json

# 导入个人事务 jobs
openclaw cron import cron-examples/personal-ops.json
```

### 手动设置

直接编辑 `~/.openclaw/cron/jobs.json`。完整格式参见 `cron-examples/`。

### 必需的占位符

启用任何 cron job 之前，在配置文件中替换这些：

| 占位符 | 替换为 | 示例 |
|--------|--------|------|
| `/tmp/brain-os-test/vault` | 你的 vault 路径 | `/home/user/my-brain` |
| `Alex` | 你的显示名 | `Alex` |
| `CST` | 你的时区 | `America/New_York` |
| `{{DISCORD_WEBHOOK_URL}}` | 你的 webhook URL | `https://discord.com/api/webhooks/...` |
| `{{DISCORD_CHANNEL_ID}}` | 你的频道 ID | `123456789012345678` |
| `{{AGENT_ID}}` | 你的 agent ID | 取决于你的设置 |

---

## Cron Job 参考

### Nightly Pipeline

| Job | 调度 | 时区 | 描述 |
|-----|------|------|------|
| `knowledge-lint-weekly` | `0 1 * * 1` | 你的时区 | 每周知识健康检查 |
| `article-notes-integration-nightly` | `0 2 * * *` | 你的时区 | 处理新文章笔记 |
| `conversation-knowledge-mining-nightly` | `0 3 * * *` | 你的时区 | 挖掘 AI 对话 |
| `knowledge-flywheel-amplifier-nightly` | `0 4 * * *` | 你的时区 | 交叉引用和放大 |
| `daily-knowledge-graph-canvas-0500` | `0 5 * * *` | 你的时区 | 生成知识图谱 |

### 个人事务

| Job | 调度 | 时区 | 描述 |
|-----|------|------|------|
| `personal-ops-morning-brief` | `0 7 * * *` | 你的时区 | 生成每日驾驶舱 |
| `personal-ops-todo-reminder-1500` | `0 15 * * *` | 你的时区 | 午后进展检查 |
| `personal-ops-todo-reminder-2000` | `0 20 * * *` | 你的时区 | 晚间回顾提示 |
| `personal-ops-weekly-plan` | `10 5 * * 1` | 你的时区 | 周计划（周一） |
| `personal-ops-monthly-milestones` | `20 6 1 * *` | 你的时区 | 月里程碑审查 |

### Cron 调度顺序

```
01:00  Knowledge lint（每周，仅周一）
02:00  文章整合
03:00  对话挖掘（读取阶段 1 输出）
04:00  知识放大（读取阶段 1+2 输出）
05:00  知识画布（可选可视化）
07:00  晨间简报
15:00  午后提醒
20:00  晚间回顾
```

---

## 投递配置

Cron jobs 可以将结果投递到各种渠道：

### Discord（Webhook）
```json
{
  "delivery": {
    "mode": "webhook",
    "to": "https://discord.com/api/webhooks/YOUR_WEBHOOK_URL",
    "bestEffort": true
  }
}
```

### Discord（频道）
```json
{
  "delivery": {
    "mode": "announce",
    "channel": "discord",
    "to": "YOUR_CHANNEL_ID"
  }
}
```

### 无投递（静默）
```json
{
  "delivery": {
    "mode": "silent"
  }
}
```

---

## 检索 / QMD 配置

QMD 不是 OpenClaw 默认内置组件。如果你需要大型 vault 或 conversation mining 的语义 / 混合检索，请单独安装 QMD。

当 QMD 可用时，Brain OS agent 可以优先使用它作为检索后端。如果 QMD 缺失，prompt 应明确进入 degraded mode，并回退到关键词检索。

见 [QMD 向量检索配置指南](qmd-setup.md) 和 [OpenClaw 配置指南](openclaw-config-guide.md)。

---

## 故障排除

| 问题 | 解决方案 |
|------|----------|
| `openclaw: command not found` | 用 `npm install -g @openclaw/cli` 重新安装 |
| Gateway 启动失败 | 运行 `openclaw doctor` 诊断 |
| Cron jobs 未触发 | 检查 `openclaw gateway status` 是否运行 |
| Job 超时失败 | 在 job 配置中增加 `timeoutSeconds` |
| 占位符未替换 | 在 cron 配置文件中搜索 `{{` |
