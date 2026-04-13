# Observer Playbook / 观察者使用手册

> **English:** Guide to configuring and running the Observer skill — the daily AI team health monitor built into Brain OS.
>
> **中文：** Observer skill 配置与运行指南——Brain OS 内置的每日 AI 团队健康监控。

---

## What is Observer? / 什么是 Observer？

Observer is a skill that monitors your AI agent team's daily operations. It collects data from two sources:
Observer 是一个监控 AI agent 团队日常运行的 skill。它从两个数据源采集信息：

1. **Agent Session Data** — Active sessions, completion status, errors, timeouts
   **Agent 会话数据** — 活跃 session、完成状态、错误、超时
2. **Gateway Logs** — Error logs, fallback events, infrastructure issues
   **网关日志** — 错误日志、fallback 事件、基础设施问题

It then produces three outputs:
然后产出三样东西：

- `.learnings/observer/` internal ledger (machine-readable)
  `.learnings/observer/` 内部账本（机器可读）
- Daily iteration plan (human-readable)
  每日迭代计划（人类可读）
- Announcement to observer channel (if configured)
  观察者频道通知（如已配置）

---

## The 6-Step Process / 六步流程

### Step 1: Collect Session Data / 收集会话数据

Use `sessions_list` to find all active sessions, then `sessions_history(sessionKey)` for details.
用 `sessions_list` 找到所有活跃 session，再用 `sessions_history(sessionKey)` 获取详情。

Key metrics to collect:
关键采集指标：

| Metric / 指标 | Meaning / 含义 |
|---|---|
| Total sessions / 总 session 数 | How many agents ran today |
| Success rate / 成功率 | `% completed without error` |
| Fail count / 失败数 | Sessions with isError=true |
| Fallback count / fallback 次数 | Model fallback triggered |

### Step 2: Scan Gateway Logs / 扫描网关日志

Check these log files:
检查以下日志文件：

- `~/.openclaw/logs/gateway.err.log` (errors)
- `~/.openclaw/logs/gateway.out.log` (output)

Look for patterns like:
寻找以下模式：

- Repeated errors (same message 3+ times) → flag as recurring
  重复错误（同一条消息出现 3+ 次）→ 标记为持续反复
- New error types not seen before → flag as novel
  之前未见过的新错误类型 → 标记为新型
- Rate limit or auth failures → flag as infrastructure
  限流或认证失败 → 标记为基础设施问题

### Step 3: Update .learnings/ Ledger / 更新内部账本

Write findings to `.learnings/observer/YYYY-MM-DD.md`:
将发现写入 `.learnings/observer/YYYY-MM-DD.md`：

```markdown
## YYYY-MM-DD Observations

### Patterns
- [pattern description] → count: N → status: new/recurring/resolved

### Decisions
- [decision made based on observations]

### Open Questions
- [unresolved question for future investigation]
```

This ledger accumulates over time and becomes your team's operational memory.
这个账本随时间累积，成为团队的运行记忆。

### Step 4: Generate Iteration Plan / 生成迭代计划

Based on today's observations + historical ledger, generate a prioritized improvement plan.
基于今日观察 + 历史账本，生成优先级排序的改进计划。

Use the template at `skills/observer/references/plan-template.md`.
使用 `skills/observer/references/plan-template.md` 中的模板。

The plan should include:
计划应包含：

- System stability issues (if any) / 系统稳定性问题（如有）
- Agent execution anomalies (if any) / Agent 执行异常（如有）
- Top 3 improvement suggestions / 前 3 条改进建议
- Learning carry-forward from yesterday / 昨日经验延续

### Step 5: Safety Gate / 安全门控

Before executing any auto-fix action, apply the **three-level safety mechanism**:
在执行任何自动修复动作前，应用**三级安全机制**：

| Level / 级别 | Action / 动作 | Example / 示例 |
|---|---|---|
| 🟢 Info / 信息 | Just report, don't act | "Gateway had 5 auth errors" |
| 🟡 Suggest / 建议 | Recommend action, wait for human | "Consider restarting gateway" |
| 🔴 Execute / 执行 | Take action WITH human confirmation | "Restarting gateway (confirmed)" |

**Default to 🟢 or 🟡. Never 🔴 without explicit human approval.**
**默认用 🟢 或 🟡。未经明确人工批准绝不 🔴。**

### Step 6: Announce / 通知

If an observer channel is configured, send a brief summary (2-4 lines).
如果配置了观察者频道，发送简短摘要（2-4 行）。

Format:
格式：

```
✅ Observer YYYY-MM-DD | sessions: N | errors: N | top issue: <one line>
```

---

## Configuration / 配置

| Setting / 设置 | Default / 默认 | Description / 说明 |
|---|---|---|
| Schedule / 执行频率 | Daily 00:01 / 每日 00:01 | Via cron prompt `prompts/cron/observer-daily-0001.md` |
| Output dir / 输出目录 | `.learnings/observer/` | Internal ledger location |
| Channel / 频道 | Configurable / 可配置 | Where to send announcements |
| Model / 模型 | Any / 任意 | Observer doesn't need a specific model |

To enable: set `enabled: true` in the cron prompt frontmatter.
启用方式：在 cron prompt 的 frontmatter 中设置 `enabled: true`。

---

## When to Use / 使用时机

- You want daily visibility into your AI team's health
  你希望每天了解 AI 团队的健康状况
- You're debugging intermittent agent failures
  你在排查间歇性 agent 故障
- You want to build operational memory over time
  你希望建立随时间累积的运行记忆
- You're onboarding a new team member who needs context
  你在让新成员了解团队运行上下文
