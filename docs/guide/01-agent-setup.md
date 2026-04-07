# 01 — OpenClaw Agent 配置指南

> 这是整套系统最关键的一步。Agent 配不好，后面的一切都不会正常工作。

---

## 为什么 Agent 配置这么重要

Brain OS 的所有自动化（Nightly Pipeline、每日驾驶舱、知识处理）都依赖 AI Agent。

Agent 的质量直接决定：
- 文章处理是否准确
- 每日驾驶舱是否有用
- 知识提取是否到位
- Cron Job 是否能正确执行

**一个配得好的 Agent 和一个配得差的 Agent，用同一套 Skill，效果天差地别。**

---

## OpenClaw 基础配置

### 1. 安装 OpenClaw

```bash
npm install -g @openclaw/cli
openclaw init
openclaw gateway start
openclaw status  # 确认运行正常
```

### 2. 创建 Agent

OpenClaw 的配置文件在 `~/.openclaw/openclaw.json`。

一个 Agent 的核心配置：

```json
{
  "agents": {
    "main": {
      "model": "openai/gpt-4o",
      "thinking": "medium",
      "tools": ["read", "write", "edit", "exec", "web_search", "web_fetch", "message"],
      "skills": ["personal-ops-driver", "article-notes-integration", "conversation-knowledge-flywheel"],
      "contextFiles": ["SOUL.md", "AGENTS.md", "USER.md", "MEMORY.md"]
    }
  }
}
```

### 3. 关键配置项解释

#### model（模型选择）

不是所有模型都适合做个人事务管理。推荐：

| 模型 | 适合场景 | 注意事项 |
|------|---------|---------|
| GPT-4o / GPT-5 | 日常主力，综合能力好 | 成本中等 |
| Claude Sonnet | 代码能力强，理解力好 | 长上下文能力强 |
| Claude Opus | 复杂推理、架构设计 | 成本高 |
| GLM-5 | 中文能力强 | 适合中文用户 |

**建议**：日常用中端模型（Sonnet / GPT-4o），复杂任务用高端模型（Opus / GPT-5）。

#### thinking（思考模式）

```json
"thinking": "medium"  // low / medium / high / off
```

- Nightly Pipeline 任务：`medium`（需要理解但不需深度推理）
- 每日驾驶舱：`medium`（需要判断优先级）
- 深度研究：`high`（需要深度分析）
- 简单提醒：`low` 或 `off`

#### tools（工具权限）

Agent 需要以下工具才能正常工作：

| 工具 | 用途 | 必须？ |
|------|------|--------|
| `read` | 读取知识库文件 | ✅ |
| `write` | 写入文件（驾驶舱、知识卡） | ✅ |
| `edit` | 编辑文件（更新待办） | ✅ |
| `exec` | 执行脚本（knowledge-lint、init-nightly-digest） | ✅ |
| `web_search` | 搜索外部信息（文章处理） | 推荐 |
| `web_fetch` | 获取网页内容 | 推荐 |
| `message` | 发送消息（提醒） | 推荐 |

#### contextFiles（上下文文件）

这些文件在每次会话开始时加载，定义了 Agent 的"人格"和"行为规则"：

| 文件 | 作用 | 类比 |
|------|------|------|
| `SOUL.md` | Agent 的性格和行为准则 | "你是谁" |
| `AGENTS.md` | 工作规则、安全边界、协作规范 | "你怎么工作" |
| `USER.md` | 用户信息、偏好、时区 | "你在帮谁" |
| `MEMORY.md` | 长期记忆 | "你记得什么" |

**这些文件是最重要的配置**。Agent 的行为由这些文件决定，比任何 Skill 都重要。

---

## 关键配置示例

### SOUL.md 示例

```markdown
# SOUL.md

你是用户的私人助理，负责个人事务管理和知识处理。

## 核心行为

- 先做后说。不要问"你需要我做什么"，直接做。
- 结论先行。先给结果，再给过程。
- 不删除用户事项。只允许重排、降级、标注状态。
- 保守外部操作。发消息、发邮件前先确认。

## 禁止事项

- 不泄露用户的私人信息
- 不执行高风险操作（删除、外发）未经确认
- 不在群聊中代替用户发言
```

### USER.md 示例

```markdown
# USER.md

- **Name**: 用户名
- **Timezone**: Asia/Shanghai (GMT+8)
- **Preferences**:
  - 先给结论，再给进度
  - 事务管理默认由你直接排序，不需要每次确认
  - 高风险操作先问
```

---

## Cron Job 配置

Cron Job 是让 Agent 定时执行任务的机制。

### 配置文件位置

`~/.openclaw/cron/jobs.json`

### 一个 Cron Job 的结构

```json
{
  "id": "unique-id",
  "agentId": "main",
  "name": "job-name",
  "description": "Job description",
  "enabled": true,
  "schedule": {
    "kind": "cron",
    "expr": "0 7 * * *",
    "tz": "Asia/Shanghai"
  },
  "sessionTarget": "isolated",
  "payload": {
    "kind": "agentTurn",
    "message": "你的指令...",
    "model": "openai/gpt-4o"
  },
  "delivery": {
    "mode": "announce",
    "channel": "discord",
    "to": "YOUR_CHANNEL_ID"
  }
}
```

### 关键字段

| 字段 | 说明 | 注意 |
|------|------|------|
| `agentId` | 用哪个 Agent 执行 | 对应 `openclaw.json` 中的 agent ID |
| `sessionTarget` | `"isolated"` 表示独立会话 | 不要用 `"main"`，避免污染主会话 |
| `model` | 指定模型 | 可以和 Agent 默认模型不同 |
| `delivery` | 结果发送到哪里 | Discord 频道 / Webhook / 静默 |

### 导入 Brain OS 的 Cron 配置

```bash
openclaw cron import cron-examples/nightly-pipeline.json
openclaw cron import cron-examples/personal-ops.json
```

导入后记得替换所有 `{{PLACEHOLDER}}`。

---

## 验证配置是否正确

### 1. 检查 Gateway

```bash
openclaw gateway status
# 应该显示 "running"
```

### 2. 手动触发一个 Cron Job

在 Discord 对应频道发送消息，看 Agent 是否正确响应。

### 3. 检查 Cron 执行日志

```bash
ls ~/.openclaw/cron/runs/
# 查看最近的执行记录
```

### 4. 测试一个 Pipeline Stage

手动在 Agent 会话中发送 article-integration 的 prompt 内容，看是否正确处理。

---

## 常见问题

### Agent 不响应 Cron Job
- 检查 `agentId` 是否正确
- 检查 Gateway 是否运行
- 检查 `delivery.to` 频道 ID 是否正确

### Agent 输出质量差
- 检查 `SOUL.md` 和 `AGENTS.md` 是否写清楚
- 检查 `thinking` 模式是否太低
- 检查 `model` 是否太弱

### Cron Job 超时
- 增加 `timeoutSeconds`
- 检查任务是否太复杂（Nightly Pipeline 的每个 Stage 应该 < 5 分钟）

### Agent 不读 Skill
- 检查 `skills` 配置是否包含正确路径
- 检查 Skill 的 `SKILL.md` frontmatter 是否正确
