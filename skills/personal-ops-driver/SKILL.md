---
name: personal-ops-driver
description: >
  {{USER_NAME}}个人事务管理执行技能。用于个人事务收件、待办/提醒/跟进项记录、backlog 状态更新、daily briefing 管理、当前承诺事项整理、00-INBOX/01-PERSONAL-OPS 分层治理。Use when: personal ops, daily briefing, todo management, commitment tracking, life management, 00-INBOX/01-PERSONAL-OPS governance. 遇到个人事务管理、排序、提醒、承诺跟踪、驾驶舱维护等请求时，应主动使用本技能。
---

# Personal Ops Driver

> {{USER_NAME}}个人事务管理技能（标准化版）

## 适用场景

当任务明显属于以下任一类时，优先使用本 skill：
- 个人事务收件
- 待办 / 提醒 / 跟进项记录
- backlog 状态更新
- daily briefing 管理
- 当前承诺事项整理
- 个人事务体系结构调整
- 00-INBOX / 01-PERSONAL-OPS 分层治理

## 使用方式

本 skill 本身只保留：
- 任务入口判断
- 最小执行规则
- references 导航

**不要把全部方法论硬塞进 SKILL.md。**
遇到个人事务任务时，先读本 skill，再按需要读取下列 references 文件。

## 必读 references（默认）

1. 执行基线：
- `./references/operating-model.md`

2. references 导航：
- `./references/reference-map.md`

3. 当前真相源：
- `{{BRAIN_PATH}}/00-INBOX/todo-backlog.md`

## 按需读取 references

### A. 方法论 / 哲学层
当需要判断轻重缓急、节奏、取舍时，读取：
- `./references/personal-ops-philosophy.md`
- `./references/personal-priority-rules.md`

### B. 决策锚点
当需要确认这套系统已经拍板过什么，读取：
- `{{BRAIN_PATH}}/01-PERSONAL-OPS/04-REVIEWS-AND-RETROS/decision-log.md`
- `./references/reference-map.md`

重点锚点：
- `DL-20260401-01` Personal Ops V1 改造
- `DL-20260401-02` 华夏 Wisdom 纳入 Personal Ops

### C. 历史证据源
当需要回查原始说法、语义变化、频道上下文时，读取：
- `{{BRAIN_PATH}}/01-PERSONAL-OPS/05-OPS-LOGS/channel-history/`

注意：
- 它是证据源，不是当前状态真相源

## 核心原则

1. **`00-INBOX/todo-backlog.md` 是个人事务唯一真相源（SSoT）**
2. **`01-PERSONAL-OPS/` 全部视为从 00 派生出的操作视图与整理层**
3. 新事项、状态变化、提醒、承诺更新，默认先落 `todo-backlog.md`
4. `channel-history/` 是证据源，不是当前状态真相源
5. 过往 `daily-briefing` 应归档，不应直接覆盖到历史消失
6. 不允许私自删除事项；只有用户明确说“已完成/可归档”才允许移出主面

## 最小执行动作

### 1. 收到新事项
- 先判断是否应进入 `todo-backlog.md`
- 补全：优先级、领域、截止、下一动作、是否必须本人、是否可委派、状态
- 必要时再同步派生视图

### 2. 收到状态变化
- 先更新 `todo-backlog.md`
- 再决定是否同步 `daily-briefing` / `本周排期` / `当前承诺事项`

### 3. 收到“提醒我”
- 写成明确提醒型事项
- 需要写清时间窗口或触发条件

### 4. 收到“已完成”
- 将 backlog 条目标记为 `已完成`
- 保留结果说明
- 暂不立即删除

## 查询顺序

1. `00-INBOX/todo-backlog.md`
2. `01-PERSONAL-OPS/05-OPS-LOGS/channel-history/`
3. `01-PERSONAL-OPS/` 其他派生视图
4. 方法论与决策 references
5. 相关项目/上下文文件

## 当前执行基线

在本 skill 与其他旧散落规则冲突时，优先级如下：
1. 用户最新明确指令
2. `references/operating-model.md`
3. skill 下的 `references/` 文档
4. Brain 中的决策锚点与历史证据
5. 本 SKILL.md
