---
name: conversation-knowledge-mining-nightly
schedule: "0 3 * * *"
agent: main
model: zai/glm-5v-turbo
enabled: true
description: conversation-knowledge-mining-nightly
delivery_mode: webhook
---

# conversation-knowledge-mining-nightly

First run `{{BRAIN_ROOT}}/scripts/init-nightly-digest.sh {{BRAIN_ROOT}} <target-date>` so the digest skeleton and run-report directory exist. Then run `{{USER_HOME}}/.openclaw/workspace/scripts/export-conversations-for-nightly.sh 3` to export recent AI conversations into `{{TRANSCRIPT_DIR}}` before mining. Then run `{{USER_HOME}}/.agents/skills/conversation-knowledge-flywheel/scripts/preflight.sh <target-date>` to verify transcript availability and QMD health. Then read and follow {{USER_HOME}}/.openclaw/workspace/conversation-knowledge-mining.prompt.md. Use the conversation-knowledge-flywheel skill as the governing protocol for the 03:00 conversation stage. Read the existing digest first, then only fill section `## 03:00 Conversation Mining`. Upstream read order is fixed: shared nightly digest -> `03-KNOWLEDGE/99-SYSTEM/03-INTEGRATION-REPORTS/run-reports/YYYY-MM-DD/` -> stable indexes if needed. Do not rely on legacy report paths under `12-REVIEWS/KNOWLEDGEBASE/`. Target date is yesterday in Asia/Shanghai unless explicitly provided. Produce transcript-derived knowledge only when there is real signal, but even no-op / degraded runs must leave both digest and machine report. Success means Brain write + git commit + post-commit sync + Obsidian visible.

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
