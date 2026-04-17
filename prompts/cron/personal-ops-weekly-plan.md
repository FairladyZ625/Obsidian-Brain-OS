---
name: personal-ops-weekly-plan
schedule: "10 5 * * 1"
agent: main
model: zai/glm-5v-turbo
enabled: true
description: Generate Personal Ops weekly plan every Monday 05:10 Asia/Shanghai
delivery_mode: webhook
---

# personal-ops-weekly-plan

你是 {{MAIN_AGENT_NAME}}，负责每周生成 Personal Ops 的正式本周推进盘。

目标文件：
`{{BRAIN_ROOT}}/01-PERSONAL-OPS/02-PLANS-AND-SCHEDULES/本周排期.md`

工作规则：
1. 先用 `session_status` 获取当前日期、时间、星期，按 Asia/Shanghai 口径处理。
2. 读取以下文件作为唯一事实来源：
   - `00-INBOX/todo-backlog.md`
   - `01-PERSONAL-OPS/01-DAILY-BRIEFS/daily-briefing.md`
   - `01-PERSONAL-OPS/03-TODOS-AND-FOLLOWUPS/当前承诺事项.md`
   - `01-PERSONAL-OPS/03-TODOS-AND-FOLLOWUPS/progress-board.md`
   - `01-PERSONAL-OPS/03-TODOS-AND-FOLLOWUPS/decision-queue.md`
   - `01-PERSONAL-OPS/02-PLANS-AND-SCHEDULES/截止日期汇总.md`
3. 必须覆盖并更新 `本周排期.md`，保证 `week` 与 `updated` 为当前周口径。
4. 内容只保留真正能指导本周行动的事项，默认结构：
   - 一、本周最重要的 3 件事
   - 二、本周必须完成
   - 三、本周必须推进（不要求完成）
   - 四、本周等待反馈
   - 五、本周可委派
   - 六、本周低优先级事项
   - 七、本周明确不做
   - 八、周中调整记录
5. 优先级判断：先看本周硬截止和外部交付，再看高杠杆但未启动事项。
6. 已完成、已关闭、无限期推迟的事项不要伪装成进行中；必要时只做简短状态说明。
7. 禁止新建第二份周计划副本。
8. 输出风格：简洁、能执行、少空话。
9. 完成后必须提交知识库修改：
   - `git add 01-PERSONAL-OPS/02-PLANS-AND-SCHEDULES/本周排期.md`
   - `git commit -m "chore(personal-ops): refresh weekly plan for YYYY-Www"`
   - 回执默认附 `commit hash` + `git status --short`
10. 核心目标：写完就 commit，让{{USER_NAME}}能在手机 Obsidian 上看到。

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
