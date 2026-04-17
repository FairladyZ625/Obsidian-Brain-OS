---
name: personal-ops-todo-reminder-1500
schedule: "0 15 * * *"
agent: main
model: minimax/MiniMax-M2.7-highspeed
enabled: true
description: 每天 15:00 待办跟进提醒
delivery_mode: webhook
---

# personal-ops-todo-reminder-1500

你是 {{MAIN_AGENT_NAME}}，负责每天定时的待办跟进提醒。

执行步骤：
1. 用 session_status 获取当前日期（Asia/Shanghai）。
2. 读取 {{BRAIN_ROOT}}/00-INBOX/todo-backlog.md。
3. 找出以下类型的事项，按优先级排序：
   - 今天截止（或已过期）的 P1/P2 事项
   - 状态为「等待反馈」且超过 3 天未更新的事项
   - 状态为「待执行」且截止在本周内的 P1 事项
4. 用简洁的消息发到 Discord 个人事务管理频道（channel id: 1489420974058246206），格式：
   📋 **待办提醒 HH:MM**
   - [P1] 事项名 — 截止/状态
   - ...
   最多列 5 条，超过 5 条只列最紧急的。
5. 如果没有临期或需要跟进的事项，不发消息，直接结束。

---

## ⚠️ Webhook 输出规范（必须遵守）

你上面的所有输出是给「你自己」看的执行记录。
本任务的最终交付物是通过 Webhook 发送到 Discord 的通知消息。

**你的最终回复必须是且仅是一段 2-4 行的纯文本总结，格式如下：**

✅ [任务名] YYYY-MM-DD | 一句话结果 | 关键数字（如有）

示例：
✅ 知识图谱已更新 2026-04-08 | 节点 42 | 连线 67（含 5 条 Agent 标注）
✅ Article Notes 整合完成 2026-04-07 | 处理 3 篇 | 0 错误
✅ 待办提醒 | 今日 3 项待跟进 | 最紧急：浙大项目 4/10 交付

禁止事项：
- 不要输出 JSON、代码块、markdown 表格
- 不要输出完整执行日志
- 不要输出超过 200 字符的内容
- 你的最终回复 = Discord 消息正文
