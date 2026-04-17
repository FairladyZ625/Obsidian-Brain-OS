---
name: brain-to-reminders-0730
schedule: "30 7 * * *"
agent: main
model: zai/glm-5.1
enabled: true
---

# brain-to-reminders-0730

每天 07:30 执行，把今日 daily briefing 中的重要事项同步到 Apple 提醒事项。

第一步执行：`TZ="Asia/Shanghai" date "+%Y-%m-%d %A %H:%M"` 获取系统日期。脚本默认也会自动取今天日期，但这里要求先显式确认一次日期口径。

## 执行步骤

1. 运行脚本：
   ```
   bash {{BRAIN_ROOT}}/scripts/brain-to-reminders.sh
   ```

2. 检查输出，确认事项已写入「{{REMINDERS_LIST}}」列表。

3. 如果脚本报错，检查：
   - `remindctl` 是否有权限（`remindctl status`）
   - `daily-briefing.md` 是否存在

## 成功标准

- 至少 1 条事项写入 Apple 提醒事项
- 无报错退出

---

## ⚠️ Webhook 输出规范

**你的最终回复必须是且仅是一段 1-2 行的纯文本总结：**

✅ Brain→提醒事项同步 YYYY-MM-DD | 写入 N 条 | 列表：{{REMINDERS_LIST}}

禁止输出 JSON、代码块、完整日志。
