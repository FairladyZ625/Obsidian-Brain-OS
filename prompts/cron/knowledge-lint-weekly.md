---
name: knowledge-lint-weekly
schedule: "0 1 * * 1"
agent: main
model: glm-5-turbo
enabled: true
description: 每周一 01:00 独立触发知识库内容级 Lint（作为 02:00 article-notes-integration lint pass 的备用独立入口）
delivery_mode: webhook
---

# knowledge-lint-weekly

Read and follow the `knowledge-lint` skill at {{USER_HOME}}/.agents/skills/knowledge-lint/SKILL.md.

First step (mandatory): run a system date command to get the **target date (yesterday, local machine timezone)**. On macOS, for example: `date -v-1d "+%Y-%m-%d"`. Then run `{{USER_HOME}}/Documents/ZeYu-AI-Brain/scripts/init-nightly-digest.sh {{USER_HOME}}/Documents/ZeYu-AI-Brain <target-date>` so the digest skeleton and run-report directory exist. Then only fill section `## 01:00 Knowledge Lint`.

Execute a full knowledge base content lint for ZeYu-AI-Brain:
- Brain root: {{USER_HOME}}/Documents/ZeYu-AI-Brain
- Run scripts/knowledge-lint.sh (or perform LLM-based equivalent if script is missing)
- Use the system-derived target date above, not a guessed date; default to the running machine's local timezone
- Write machine-facing report to 03-KNOWLEDGE/99-SYSTEM/03-INTEGRATION-REPORTS/run-reports/YYYY-MM-DD/knowledge-lint-YYYY-MM-DD.md
- Update human-facing digest at 03-KNOWLEDGE/01-READING/04-DIGESTS/nightly-digest-YYYY-MM-DD.md under section `## 01:00 Knowledge Lint`
- Commit to Brain git

Digest section should only tell {{USER_NAME}}：知识库健康是否正常 / 高优先级问题大概有多少 / 是否需要他关心。

Success = report written + digest updated + committed + Obsidian-visible.

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
