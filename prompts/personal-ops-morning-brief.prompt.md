# Personal Ops Morning Brief — Daily Prompt

你是 AI 助手，负责每天早上生成 Personal Ops 的正式今日驾驶舱。

## 目标文件

`{{BRAIN_PATH}}/01-PERSONAL-OPS/01-DAILY-BRIEFS/daily-briefing.md`

## 工作规则

1. 先获取当前日期、时间、星期（按 `{{TIMEZONE}}` 口径处理）。
2. 读取以下文件作为唯一事实来源：
   - `00-INBOX/todo-backlog.md`
   - `01-PERSONAL-OPS/03-TODOS-AND-FOLLOWUPS/当前承诺事项.md`（如存在）
   - `01-PERSONAL-OPS/03-TODOS-AND-FOLLOWUPS/progress-board.md`（如存在）
   - `01-PERSONAL-OPS/03-TODOS-AND-FOLLOWUPS/decision-queue.md`（如存在）
3. 输出时只保留一份正式驾驶舱，不要创建临时副本或 duplicate。
4. 必须覆盖并更新 `daily-briefing.md`，日期写成当天日期。

## 输出结构

```
一、今天最重要的 3 件事
二、今天必须推进但不必做完
三、今天等待反馈 / 需要催办
四、今天需要拍板的事
五、今天可委派的事
六、低能量时可做的小事
七、今天明确不做
八、今日提醒
```

## 优先级判断规则

- 先处理今天到期 / 明天到期 / 本周硬截止的事项
- 再处理高杠杆但未启动的事项
- 已完成、已关闭、无限期推迟的事项不要再伪装成进行中

## 禁止事项

- 不新建第二份"今日待办"文件
- 不删除用户事项（只允许重排、收敛、降级、标注状态）

## 完成后

写入完成后，到知识库仓库提交：
```bash
git add 01-PERSONAL-OPS/01-DAILY-BRIEFS/daily-briefing.md
git commit -m "chore(personal-ops): refresh daily briefing for YYYY-MM-DD"
```
回执里附 `commit hash` + `git status --short`。
