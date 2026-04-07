# Chronicle 史官系统

> 频道历史记录 Agent——默默记录，不参与讨论。

---

## 概念

**Chronicle（史官）** 是 Brain OS 中的一个独立 Agent 角色，专门负责记录 Discord 频道的历史对话。它像古代的史官一样：**只记录，不评论，不干预**。

### 为什么需要史官？

1. **AI 的记忆是短暂的**——每次会话重启后，Agent 丢失所有上下文
2. **频道讨论是宝贵的知识来源**——决策、方案、经验都散落在聊天记录中
3. **需要结构化的证据源**——`channel-history/` 作为个人事务系统的"历史证据层"
4. **降低主 Agent 负担**——让 Codex Main 专注执行，不用分心做记录

---

## 工作机制

```
每 2 小时触发一次
       ↓
Chronicle Agent 读取最近 2 小时的频道消息
       ↓
按结构化模板写入 channel-history/YYYY-MM-DD-HH.md
       ↓
Git commit → Obsidian 可见
```

### 记录内容

每次记录包含：

```markdown
# 频道历史记录 YYYY-MM-DD HH:00

## 基本信息
- 时间范围：HH:00 - (HH+2):00
- 主要参与者：
- 活跃频道：

## 关键事件
- [时间] 事件描述

## 决策与结论
- 决策1：...

## 待办与承诺
- 承诺1（谁/截止/状态）

## 值得回溯的讨论
- 话题摘要 + 相关消息 ID 引用
```

### 不记录什么

- 纯闲聊、表情包、无意义的插话
- 已被其他系统捕获的内容（如 todo-backlog 已有的条目）
- 敏感个人信息（除非用户明确要求记录）

---

## 配置

### Cron 配置示例

在 `cron-examples/personal-ops.json` 中添加以下 job：

```json
{
  "id": "chronicle-agent-{uuid}",
  "agentId": "chronicle",
  "name": "chronicle-channel-history",
  "description": "每 2 小时记录一次频道历史",
  "enabled": true,
  "schedule": {
    "kind": "cron",
    "expr": "0 */2 * * *",
    "tz": "Asia/Shanghai"
  },
  "sessionTarget": "isolated",
  "wakeMode": "now",
  "payload": {
    "kind": "agentTurn",
    "message": "你是 Chronicle（史官），负责记录 Discord 频道的历史。\n\n规则：\n1. 用 session_status 获取当前时间（Asia/Shanghai）。\n2. 读取最近 2 小时的频道消息（通过 message search 或 channel history）。\n3. 只记录有实质内容的消息：决策、任务分配、技术讨论、重要结论。\n4. 过滤掉纯闲聊、单句回复、无上下文的插话。\n5. 写入文件：/tmp/brain-os-test/vault/01-PERSONAL-OPS/05-OPS-LOGS/channel-history/YYYY-MM-DD-HH.md\n6. 格式见 skills/chronicle-agent/SKILL.md\n7. 写入后 git commit：git add && git commit -m \"chore(chronicle): channel history YYYY-MM-DD-HH\"\n8. 不要在频道发言，安静完成即可。",
    "model": "minimax/MiniMax-M2.7-highspeed",
    "timeoutSeconds": 300
  }
}
```

### 推荐配置

| 配置项 | 推荐值 | 说明 |
|--------|--------|------|
| 执行频率 | 每 2 小时 | 平衡覆盖率和成本 |
| Agent 模型 | MiniMax M2.7 Highspeed | 成本低，适合结构化记录 |
| 存储路径 | `01-PERSONAL-OPS/05-OPS-LOGS/channel-history/` | 与个人事务系统集成 |
| 文件格式 | `YYYY-MM-DD-HH.md` | 按日期+时段命名 |

---

## Agent 选择建议

| Agent | 适用场景 | 成本 |
|-------|---------|------|
| GLM-4.7 / Haiku | 推荐，中文好，成本低 | 低 |
| MiniMax M2.7 Highspeed | 最便宜，适合纯记录 | 最低 |
| GLM-5 | 需要深度总结时 | 中 |

**推荐用低成本模型**——史官的工作是结构化记录，不需要深度推理。

---

## 与其他系统的关系

```
Discord 频道消息
    ↓
Chronicle Agent（每 2h 记录）
    ↓
channel-history/（历史证据层）
    ↓
Personal Ops Driver（读取作为参考）
    ↓
daily-briefing.md / decision-queue.md
```

- **Chronicle 是生产者**：写 `channel-history/`
- **Personal Ops Driver 是消费者**：读 `channel-history/` 作为决策依据
- **Codex Main 是协调者**：两者之间不直接通信，通过文件耦合

---

## 存储策略

### 文件保留

- `channel-history/` 目录下的文件保留 **30 天**
- 超过 30 天的文件归档到 `09-ARCHIVE/channel-history/`
- 或者直接删除（取决于你的存储偏好）

### 索引维护

在 `channel-history/` 下维护一个 `index.md`：

```markdown
# 频道历史索引

## 2026-04
- [0709](2026-04-07-07.md) — 开源仓库搭建讨论
- [0912](2026-04-07-09.md) — 公众号文章写作
- ...
```

---

## 快速开始

1. 在 OpenClaw 中创建一个 Chronicle Agent（或复用现有低成本的 Agent）
2. 将上面的 cron 配置导入 OpenClaw
3. 确保 `01-PERSONAL-OPS/05-OPS-LOGS/channel-history/` 目录存在
4. 等待第一次运行，检查输出格式是否符合预期

---

## 相关文档

- [Personal Ops System](personal-ops.md)
- [Nightly Pipeline](nightly-pipeline.md)
- [Cron 配置说明](../cron-examples/README.md)
