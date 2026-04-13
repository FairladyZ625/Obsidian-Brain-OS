---
name: daily-knowledge-graph-canvas-0500
schedule: "0 5 * * *"
agent: main
model: zai/glm-5v-turbo
enabled: true
description: 每天05:00自动生成知识图谱Canvas并发送至知识库文章沉淀频道
delivery_mode: webhook
---

# daily-knowledge-graph-canvas-0500

每日知识图谱生成任务（05:00）。

步骤0：先执行系统日期命令（如 `date "+%Y-%m-%d %A %H:%M %Z"`）获取**今天日期、星期与时区**，后续所有 YYYY-MM-DD 都必须使用系统值，默认使用运行机器的本地时区。

步骤1：运行脚本生成今日知识图谱 Canvas：
python3 {{USER_HOME}}/.openclaw/workspace/scripts/knowledge-graph-canvas.py

步骤2：检查脚本输出（节点数、连线数、RQ匹配情况），若脚本失败记录错误并通知。

步骤3：读取以下目录最近7天新增文件，分析文章之间的跨主题语义关联：
- {{USER_HOME}}/Documents/ZeYu-AI-Brain/03-KNOWLEDGE/02-WORKING/01-ARTICLE-NOTES/
- {{USER_HOME}}/Documents/ZeYu-AI-Brain/03-KNOWLEDGE/01-READING/01-DOMAINS/

步骤4：对发现的跨主题关联（脚本无法自动识别的语义关联），直接编辑今日canvas文件，在edges数组末尾追加新连线。label格式：'[Agent] 关联说明'，color用'3'（黄色）区分。

步骤5：git add + git commit。
Brain仓库：{{USER_HOME}}/Documents/ZeYu-AI-Brain
commit message：auto: knowledge graph YYYY-MM-DD + agent annotations（YYYY-MM-DD 使用系统日期）

步骤6：向Discord频道1489421056379846716发送完成通知（2-3行）：
🧠 知识图谱已更新 YYYY-MM-DD | 节点 X | 连线 Y（含 Z 条Agent标注）| RQ XX/YY

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
