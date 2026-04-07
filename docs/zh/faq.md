> 本文档为英文版的中译本。如有歧义，以英文原版为准。

# 常见问题

---

## 通用

### 什么是 Obsidian Brain OS？

一个构建在 Obsidian 上的 AI 增强个人上下文系统。它将结构化知识 vault、自动化 nightly 处理 pipeline 和 AI 驱动的个人事务管理整合为一个协调的系统。

### 我必须使用 OpenClaw 吗？

要获得**完整体验**（nightly pipeline、自动化简报）：需要，OpenClaw 处理调度。

仅**知识管理**：不需要。vault 结构、模板和 skills 可以与任何 AI 助手配合使用。只是没有自动化 cron jobs。

### 我必须使用 Agora 吗？

不需要。Agora 推荐用于任务管理但非必需。Brain OS 中的项目注册可以独立工作。参见 [项目管理](project-management.md) 了解替代方案。

### 我可以和 Claude、GPT 或其他 AI 助手一起使用吗？

可以。skills 和 prompts 以与大多数 AI 助手兼容的格式编写。OpenClaw 提供调度层，但知识结构和方法论在任何地方都可用。

---

## 设置

### 我可以使用已有的 Obsidian vault 吗？

可以，但建议用 Brain OS 模板从头开始。你可以逐步从旧 vault 迁移内容。

在现有 vault 中采用该结构：
1. 从 `vault-template/` 复制目录结构
2. 将现有笔记移到相应目录
3. 安装 skills 并配置 cron jobs

### 如果我不想用所有功能？

Brain OS 支持**模块化安装**。参见 [快速开始](getting-started.md) 中的三种配置：
- **仅知识系统** — vault 结构 + 文章处理
- **仅个人事务** — 待办管理 + 每日简报
- **完整系统** — 全部

### 如何更改时区？

1. 编辑 `scripts/config.env` → `TIMEZONE="Your/Timezone"`
2. 编辑 cron job 配置 → `schedule.tz`
3. 替换 skill 文件中的 `{{TIMEZONE}}`

---

## Nightly Pipeline

### Pipeline 一直说"no-op"——是不是坏了？

不是。"No-op" 表示没有新文章或对话需要处理。这在安静的日子是正常的。Pipeline 仍然会写一份报告确认它检查过了。

### 我可以更改 pipeline 调度时间吗？

可以。编辑 `cron-examples/` 中的 cron 调度：
```json
{
  "schedule": {
    "expr": "0 2 * * *",
    "tz": "America/New_York"
  }
}
```

### 如果某阶段失败了怎么办？

其他阶段继续独立运行。检查 `99-SYSTEM/03-INTEGRATION-REPORTS/` 中的运行报告查看具体错误。常见修复：
- 缺少转录 → 安装 `convs` CLI
- 缺少脚本 → 检查 `scripts/` 目录存在
- 权限错误 → `chmod +x scripts/*.sh`

### 我可以添加自定义 pipeline 阶段吗？

可以。在 `prompts/` 中创建新 prompt，添加引用它的 cron job，遵循交接协议：读取现有摘要 → 填充你的部分 → commit。

---

## 知识库

### 如何添加一篇文章？

使用文章笔记模板在 `03-KNOWLEDGE/02-WORKING/01-ARTICLE-NOTES/` 创建新文件。Nightly pipeline 会自动处理。

### 如何查找内容？

1. **从摘要开始**（`04-DIGESTS/`）— AI 告诉你什么新
2. **在 Obsidian 中搜索** — 内置搜索 + 反向链接
3. **Dataview 查询** — 跨 vault 的结构化查询
4. **QMD**（可选）— 大型 vault 的语义搜索

### 如何防止知识库变得太大？

- 每周运行 `knowledge-lint.sh` 检查问题
- 归档陈旧笔记（将状态改为 `archived`）
- 定期审查 `02-WORKING/` — 删除真正无关的草稿
- 让 pipeline 处理策展——它不会强制更新

---

## 个人事务

### AI 能删除我的待办吗？

不能。AI 只能重排、合并和降级事项。只有你能标记事项为完成或归档。

### 如何添加新待办？

追加到 `00-INBOX/todo-backlog.md`。AI 会在下次晨间简报中识别。

### 晨间简报与我的优先级不匹配——怎么修复？

1. 检查 `todo-backlog.md` 中的事项优先级是否正确
2. 确认紧急事项的 `截止` 字段已设置
3. 直接编辑简报——你的手动编辑优先，直到下次自动生成

---

## Skills

### 如何创建自定义 skill？

参见 [Skills 指南](skills-guide.md)。创建一个目录，编写带 frontmatter 格式的 `SKILL.md` 文件。

### 我可以使用其他来源的 skills 吗？

可以。只需复制到你的 skills 目录。Brain OS skills 与 OpenClaw 的 skill 系统兼容。

### 如何禁用 skill？

将 `SKILL.md` 重命名为 `SKILL.md.disabled` 或将目录移出 skills 路径。

---

## 故障排除

| 问题 | 解决方案 |
|------|----------|
| Obsidian 无法打开 vault | 检查路径是目录而非文件 |
| 脚本权限错误 | `chmod +x scripts/*.sh` |
| Cron jobs 未运行 | `openclaw gateway status` — 是否运行？ |
| Knowledge lint 找不到内容 | 检查配置中的 `BRAIN_PATH` |
| 摘要未生成 | 检查 `~/.openclaw/cron/runs/` 中的 cron job 日志 |
| 占位符未替换 | 在配置文件中搜索 `{{` |
| Git commit 失败 | 检查 `git status`，解决冲突 |
