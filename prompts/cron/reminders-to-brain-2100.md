---
name: reminders-to-brain-2100
schedule: "0 21 * * *"
agent: main
model: zai/glm-5.1
enabled: true
---

# reminders-to-brain-2100

每天 21:00 执行，从 Apple 提醒事项读取完成状态，反向 double-check Brain 待办。

第一步执行：`TZ="Asia/Shanghai" date "+%Y-%m-%d %A %H:%M"` 获取系统日期。脚本默认也会自动取今天日期，但这里要求先显式确认一次日期口径。

## 执行步骤

1. 运行脚本：
   ```
   bash {{BRAIN_ROOT}}/scripts/reminders-to-brain.sh
   ```

2. 读取脚本输出，找出：
   - `completed=N`：今日已完成事项数
   - `overdue=N`：过期未完成事项数
   - `OVERDUE_ITEMS:` 后面的具体事项列表

3. 如果有过期未完成事项（overdue > 0），在 Discord 频道 `1489420974058246206` 向{{USER_NAME}}追问：
   > {{USER_NAME}}，以下事项在提醒事项里已过期但未标记完成，请确认：
   > - [事项名]
   > 是忘记点完成了，还是确实还没做？

4. 读取今日同步报告：`01-PERSONAL-OPS/05-OPS-LOGS/reminders-sync-YYYY-MM-DD.md`

5. 将已完成事项与 `00-INBOX/todo-backlog.md` 交叉比对：
   - 如果提醒事项里标记完成，但 Brain 里还是待办状态 → 在 Discord 提示{{USER_NAME}}确认是否可以在 Brain 里也标记完成

## 成功标准

- 报告文件已生成
- 过期事项已追问（如有）
- 无报错退出

---

## ⚠️ Webhook 输出规范

**你的最终回复必须是且仅是一段 2-3 行的纯文本总结：**

✅ 提醒事项→Brain同步 YYYY-MM-DD | 完成 N 条 | 过期 N 条（已追问）

如有过期事项，追问消息单独发送到个人事务管理频道。
禁止输出 JSON、代码块、完整日志。
