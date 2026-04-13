# Writing Cron Prompts for Brain OS / Brain OS Cron Prompt 编写指南

> **English:** Best practices for writing cron prompts that work reliably with LLM agents — learned from production experience.
>
> **中文：** 编写能在 LLM agent 上可靠运行的 cron prompt 的最佳实践——来自生产环境的经验总结。

---

## Core Principle / 核心原则

**Never trust an LLM to know the current date, time, or day of week.**
**永远不要相信 LLM 知道当前日期、时间或星期几。**

LLMs are trained on historical data. Their "current date" is whatever was in their training cutoff, not today's actual date. This causes silent, hard-to-debug errors in recurring tasks.
LLM 的训练数据是历史性的。它们"知道"的当前日期是训练截止日期，而不是今天。这会在周期性任务中导致难以排查的静默错误。

---

## Mandatory: System Date Fetch / 必须做：获取系统日期

### Rule / 规则

Every cron prompt MUST start with a system command to fetch the current date/time/timezone before doing anything else.
每个 cron prompt **必须**在执行任何其他操作前，先用系统命令获取当前日期/时间/时区。

### How / 怎么做

```markdown
## Step 0 (mandatory)
Execute a system date command FIRST:
- macOS: `date "+%Y-%m-%d %A %H:%M %Z"`
- Linux: `date "+%Y-%m-%d %A %H:%M %Z"`

Use this value for ALL subsequent YYYY-MM-DD references. Do NOT guess.
```

### What NOT to do / 不要这样做

```markdown
# ❌ BAD — LLM will guess the date
Today is 2026-04-13 (Monday). Processing...

# ✅ GOOD — System tells us the date
Step 0: Run `date "+%Y-%m-%d %A"` → 2026-04-13 Monday
Now processing with confirmed date...
```

### Timezone / 时区

Use the **running machine's local timezone** by default. Do NOT hardcode a specific timezone (e.g., `Asia/Shanghai`) unless the user explicitly configured it.
默认使用**运行机器的本地时区**。不要硬编码特定时区（如 `Asia/Shanghai`），除非用户明确配置。

---

## Output Format Constraints / 输出格式约束

### Webhook Delivery Mode / Webhook 投递模式

Many Brain OS cron prompts use `delivery_mode: webhook`. This means the final output goes to a notification channel (Discord, etc.), not back to a terminal.
很多 Brain OS cron prompt 使用 `delivery_mode: webhook`。这意味着最终输出会发到通知频道（Discord 等），而不是终端。

**Rules / 规则：**

1. Final reply = 2-4 lines of plain text only
   最终回复 = 仅 2-4 行纯文本
2. No JSON, code blocks, or markdown tables in final output
   最终输出中不能有 JSON、代码块或 markdown 表格
3. Format: `✅ [TaskName] DATE | one-line result | key numbers`
   格式：`✅ [任务名] 日期 | 一行结果 | 关键数字`
4. All detailed execution logs go ABOVE the final reply (they're for the agent itself)
   所有详细执行日志放在最终回复上方（给 agent 自己看的）

### Template / 模板

```
✅ [任务名] YYYY-MM-DD | 一句话结果 | 关键数字（如有）

示例：
✅ 知识图谱已更新 2026-04-13 | 节点 42 | 连线 67（含 5 条 Agent 标注）
✅ Article Notes 整合完成 2026-04-13 | 处理 3 篇 | 0 错误
✅ 待办提醒 | 今日 3 项待跟进 | 最紧急：浙大项目 4/15 交付
```

---

## Frontmatter Convention / Frontmatter 规范

Every cron prompt file must have YAML frontmatter:
每个 cron prompt 文件必须有 YAML frontmatter：

```yaml
---
name: task-name-here                    # Unique identifier / 唯一标识符
schedule: "0 5 * * *"                   # Cron expression / Cron 表达式
agent: main                             # Which agent runs it / 哪个 agent 执行
model: zai/glm-5.1                      # Model preference / 模型偏好
enabled: true                           # false = disabled / false = 禁用
description: One-line what this does    # Human-readable description / 人类可读描述
delivery_mode: webhook                  # webhook | announce | silent
---
```

Key fields / 关键字段：

| Field / 字段 | Required / 必填 | Description / 说明 |
|---|:---:|---|
| `name` | ✅ | Unique slug, used in logging |
| `schedule` | ✅ | Standard cron expression |
| `agent` | ✅ | Target agent identifier |
| `model` | ✅ | Recommended model (can be overridden) |
| `enabled` | ✅ | Master on/off switch |
| `description` | ✅ | What this task does, in one line |
| `delivery_mode` | ✅ | How results are delivered |

---

## Error Handling / 错误处理

### When a script fails / 脚本失败时

Don't hide failures. Report them clearly:
不要隐藏失败。清晰报告：

```markdown
❌ [TaskName] YYYY-MM-DD | FAILED: <reason> | next step: <suggestion>
```

### When there's nothing to do / 无事可做时

Still send a success message with "no-op" indicator:
仍然发送成功消息，带"无操作"标记：

```markdown
✅ [TaskName] YYYY-MM-DD | no-op | no new items to process
```

### When degraded mode / 降级模式时

If upstream data is missing but partial work is possible:
如果上游数据缺失但可以部分工作：

```markdown
⚠️ [TaskName] YYYY-MM-DD | DEGRADED: <what's missing> | completed: <partial result>
```

---

## Cross-Prompt Coordination / 跨 Prompt 协调

Brain OS uses a **nightly pipeline** architecture where multiple cron prompts run at different times and pass data to each other.
Brain OS 使用 **nightly pipeline** 架构，多个 cron prompt 在不同时间运行并相互传递数据。

### Handoff Protocol / 交接协议

1. Upstream writes to a shared digest file
   上游写入共享 digest 文件
2. Downstream reads the digest first, then fills its own section
   下游先读 digest，再填写自己的部分
3. Each prompt only touches its own section; never rewrites others
   每个 prompt 只动自己的部分；绝不重写其他部分

```markdown
# Shared digest structure / 共享 digest 结构
# nightly-digest-YYYY-MM-DD.md

## 01:00 Knowledge Lint          ← knowledge-lint-weekly fills this
## 02:00 Article Integration     ← article-notes-integration-nightly fills this
## 03:00 Conversation Mining     ← conversation-kining-nightly fills this
## 04:00 Amplifier               ← knowledge-flywheel-amplifier-nightly fills this
## Summary                       ← Last stage fills this
```

### If upstream is missing / 如果上游缺失

- Continue in **degraded mode** if partial work is possible
  如果可以做部分工作，以**降级模式**继续
- Emit a clear degradation notice, don't silently skip
  发出清晰的降级通知，不要静默跳过
- Never invent data that doesn't exist
  绝不编造不存在的数据
