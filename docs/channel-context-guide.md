# Channel Context Guide

> Why the same agent can behave differently across channels, and how to design that on purpose.
>
> 为什么同一个 agent 在不同频道里会表现不一样，以及如何有意识地设计这种能力。

---

## What this is / 这是什么

In Brain OS and OpenClaw-style systems, a channel is not just a chat window.

It is usually a **workbench** with its own:
- responsibility boundary
- initial context
- writing style
- allowed actions
- memory and retrieval expectations

在 Brain OS 和 OpenClaw 这类系统里，一个频道不只是一个聊天窗口。

它更像是一个有独立配置的**工作台**，拥有自己的：
- 职责边界
- 初始上下文
- 输出风格
- 可执行动作范围
- 记忆与检索预期

That is why the same agent may look different in different channels.

这就是为什么同一个 agent 在不同频道里看起来像“不同的人”。

---

## Core principle / 核心原则

**Channel = workbench = scoped context.**

Do not think of multi-channel setup as “one bot with random mood changes”.
Think of it as **one core agent entering different work environments**.

**频道 = 工作台 = 有边界的上下文。**

不要把多频道理解成“同一个 bot 在随机变人格”。
更准确的理解是：**同一个核心 agent，进入了不同的工作环境。**

Examples:
- Main hall: coordination, routing, high-level decisions
- Knowledge channel: note capture, knowledge extraction, vault governance
- Writing channel: drafting, editing, polishing
- Project channel: project-local context, execution details, issue follow-up
- Review channel: audits, checks, exception handling

例如：
- 主频道：总协调、分诊、决策
- 知识库频道：知识沉淀、入库、治理
- 写作频道：起稿、改稿、润色
- 项目频道：项目局部上下文、执行细节、问题跟踪
- 巡检频道：审查、检查、异常处理

---

## Where the configuration usually lives / 这些配置通常在哪里

The exact mechanism depends on your setup, but in practice channel-specific behavior usually comes from a combination of:

1. **Gateway / runtime JSON config**
   - channel bindings
   - delivery targets
   - default routing
   - per-channel startup instructions

2. **Workspace context files**
   - global rules
   - team conventions
   - user preferences
   - memory rules

3. **Channel-specific prompt or guide files**
   - local mission
   - local tone
   - allowed write targets
   - local safety boundaries

4. **Tooling and retrieval policy**
   - what memory can be read
   - what docs are preferred
   - what repo or vault area is relevant

具体机制取决于你的系统接法，但实操里，频道差异通常来自这几层的组合：

1. **Gateway / runtime JSON 配置**
   - 频道绑定
   - 投递目标
   - 默认路由
   - 每频道启动指令

2. **Workspace 上下文文件**
   - 全局规则
   - 团队约定
   - 用户偏好
   - 记忆规则

3. **频道专属 prompt / guide 文件**
   - 本地使命
   - 本地语气
   - 允许写入的目标
   - 本地安全边界

4. **工具与检索策略**
   - 能读哪些记忆
   - 优先读哪些文档
   - 关联哪个 repo / vault 区域

---

## Recommended channel strategy / 推荐的分频道策略

Start simple. Most teams do not need 20 channels.

A strong starting point is:

### 1. Main channel / 主频道
Use for:
- coordination
- triage
- routing work to the right place
- high-level updates

Avoid:
- stuffing it with every local detail
- using it as the only knowledge workspace

### 2. Knowledge channel / 知识库频道
Use for:
- article capture
- knowledge extraction
- note governance
- structure decisions

Avoid:
- personal ops clutter
- unrelated project execution chatter

### 3. Writing channel / 写作频道
Use for:
- article drafting
- rewriting
- tone adjustment
- content packaging

Avoid:
- mixing with raw technical debugging

### 4. Project channel / 项目频道
Use for:
- project-specific execution
- issue context
- branch / task / review flow

Avoid:
- treating project-local assumptions as global truth

### 5. Review / observer channel / 巡检频道
Use for:
- audits
- health checks
- review findings
- exception escalation

Avoid:
- turning it into a second main hall

从简单开始，多数团队并不需要 20 个频道。

一个比较强的起步配置是：
- 1 个主频道
- 1 个知识库频道
- 1 个写作频道
- 1 个项目频道
- 1 个巡检频道

---

## Good design pattern / 好的设计模式

A good multi-channel setup does **not** mean copying the full global context into every channel.

A better pattern is:
- keep a small shared core
- add local context only where needed
- let each channel specialize

**Shared core / 共享核心**
- who the user is
- stable preferences
- safety rules
- global coordination rules

**Local layer / 局部层**
- channel mission
- local vocabulary
- local files and tools
- local write targets

好的多频道设计，不是把一大坨全局上下文复制到每个频道。

更好的模式是：
- 共享核心保持小而稳
- 局部上下文按频道补充
- 每个频道都承担清晰职责

---

## Anti-patterns / 常见反模式

### 1. Same giant prompt everywhere
This makes every channel noisy and unfocused.

### 2. Full private memory in every channel
This increases leakage risk and confuses relevance.

### 3. No responsibility boundary
If all channels can do everything, none of them stay sharp.

### 4. Treating local chat context as global truth
A project channel may contain temporary assumptions. Do not let it silently overwrite durable records.

### 5. Solving everything by adding more agents
Often the real problem is weak context design, not insufficient agent count.

### 1. 所有频道都塞同一个巨型 prompt
会让每个频道都变得吵、散、失焦。

### 2. 每个频道都加载完整私人记忆
会提高泄露风险，也会让检索相关性变差。

### 3. 没有职责边界
如果每个频道什么都做，最后哪个频道都做不好。

### 4. 把局部聊天当成全局真相源
项目频道里很多只是临时判断，不能悄悄覆盖长期记录。

### 5. 一有问题就加更多 agent
很多时候问题不在 agent 数量，而在上下文设计太弱。

---

## A simple config sketch / 一个简化配置示意

This is only a sketch, not a required exact schema:

```json
{
  "channels": {
    "main-hall": {
      "role": "coordination",
      "contextProfile": "global-core",
      "prompt": "prompts/main-coordination.md"
    },
    "obsidian-brain": {
      "role": "knowledge",
      "contextProfile": "knowledge-core",
      "prompt": "prompts/knowledge-ops.md"
    },
    "writing-room": {
      "role": "writing",
      "contextProfile": "writing-core",
      "prompt": "prompts/writing-room.md"
    }
  }
}
```

Meaning:
- same underlying agent runtime
- different channel bindings
- different local instructions
- different retrieval and execution priorities

这里只是示意，不代表必须完全按这个 schema 配。

它表达的是：
- 底层是同一个 agent runtime
- 但不同频道绑定不同职责
- 读不同局部说明
- 检索和执行优先级也不同

---

## Why this matters / 为什么这很重要

A strong agent is usually not built by piling up more models or more bots.

It is built by:
- stable memory
- clear workbenches
- scoped context
- explicit boundaries
- repeated iteration

一个强 agent，通常不是靠堆更多模型、更多 bot 养出来的。

它更像是靠这些东西长出来的：
- 稳定记忆
- 清晰工作台
- 有边界的上下文
- 明确职责
- 持续迭代

In that sense, channel strategy is not a UI detail.
It is part of the operating system.

从这个角度看，分频道策略不是界面小技巧。
它其实是系统设计的一部分。

---

## Practical advice / 实操建议

If you are just starting:

1. Start with one strong main channel
2. Add one specialized channel only when a real recurring job appears
3. Write down the mission of that channel in one paragraph
4. Keep the local context short and task-shaped
5. Revisit after one week of use

如果你刚开始搭：

1. 先把一个主频道养强
2. 只有当某种工作真的反复出现时，再拆出专门频道
3. 先用一段话写清楚这个频道到底负责什么
4. 局部上下文保持短、小、任务化
5. 用一周后再复盘，而不是一开始就设计得过重

---

## Bottom line / 最后一句

A channel-specific agent strategy is not about making one bot feel magical.
It is about giving the same agent the right room, for the right job, with the right context.

分频道 agent 策略，不是为了让一个 bot 看起来更神秘。
而是为了让同一个 agent，在合适的房间里，用合适的上下文，做合适的事。
