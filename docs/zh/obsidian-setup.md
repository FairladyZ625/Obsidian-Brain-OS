> 本文档为英文版的中译本。如有歧义，以英文原版为准。

# Obsidian 配置 — 推荐插件和设置

---

## 核心插件

这些 Obsidian 插件推荐用于 Brain OS。从 **设置 → 社区插件 → 浏览** 安装。

### 必装

| 插件 | 用途 | 为什么 |
|------|------|--------|
| **Dataview** | 像数据库一样查询 vault 内容 | 驱动简报和 backlog 中的动态视图 |
| **Templater** | 高级模板插入 | 比默认模板更适合动态内容 |
| **Calendar** | 按日历视图导航每日笔记 | 快速访问每日简报和摘要 |

### 推荐

| 插件 | 用途 | 为什么 |
|------|------|--------|
| **Graph Analysis** | 增强图谱视图 | 可视化知识连接 |
| **Homepage** | 设置默认落地页 | 将 `04-DIGESTS/` 或 `daily-briefing.md` 设为首页 |
| **Tag Wrangler** | 管理 tag | 在整个 vault 中重命名、合并、清理 tag |
| **Linter** | 自动格式化 markdown | 保持一致的格式 |
| **Quick Add** | 从任何地方快速捕捉 | 不离开当前笔记即可快速 inbox |

### 可选（高级用户）

| 插件 | 用途 | 为什么 |
|------|------|--------|
| **DB Folder** | Notion 风格的数据库视图 | 如果你想要看板/表格视图管理待办 |
| **Kanban** | 看板 | 可视化项目跟踪 |
| **Excalidraw** | 绘图和图表 | 用于架构草图 |
| **Tasks** | 带查询的任务管理 | 如果你大量使用复选框任务 |
| **Periodic Notes** | 日/周/月笔记 | 如果你想要结构化的笔记创建 |

---

## 配置

### .obsidian/appearance.json

```json
{
  "cssTheme": "",
  "accentColor": "#4a9eff",
  "baseFontSize": 16,
  "translucency": false
}
```

### .obsidian/file-explorer.json

推荐：将常用文件夹固定在文件资源管理器顶部：
1. `00-INBOX/`
2. `01-PERSONAL-OPS/01-DAILY-BRIEFS/`
3. `03-KNOWLEDGE/01-READING/04-DIGESTS/`
4. `04-PROJECTS/01-ACTIVE/`

### 首页设置

将首页设为每日摘要或每日简报：
- 安装 **Homepage** 插件
- 设置 → Homepage → Homepage 文件：`03-KNOWLEDGE/01-READING/04-DIGESTS/nightly-digest-{date}.md`

或手动方式：启动 Obsidian 时始终打开最新的摘要文件。

---

## Vault 设置

### 编辑器

- **默认编辑模式**：源码模式（更适合 AI 生成的内容）
- **可读行长度**：开启
- **拼写检查**：按你的偏好

### 文件与链接

- **新笔记默认位置**：`00-INBOX/`
- **新链接格式**：尽可能使用最短路径
- **使用 [[Wikilinks]]**：开启（Brain OS 全部使用 wikilinks）

### 搜索

- **搜索结果排序**：最后修改（最近的优先）

---

## Tag

Brain OS 使用 tag 进行知识分类。推荐的 tag 结构：

```
#domain/ai-agent
#domain/engineering
#domain/product
#domain/management
#type/article-note
#type/pattern
#type/topic
#type/research-question
#status/pending
#status/integrated
#status/archived
```

使用 **Tag Wrangler** 插件来一致地管理这些 tag。

---

## 性能提示

### 大型 Vault（500+ 笔记）

1. **禁用未使用的插件** — 每个插件增加启动时间
2. **使用 `.obsidian/workspace.json` 排除** — 将 `99-SYSTEM/` 从搜索索引中排除
3. **设置图谱视图过滤** — 在图谱中排除 `99-SYSTEM/`、`memory/` 和 `.git/`
4. **定期清理** — 运行 `knowledge-lint.sh` 查找孤立/陈旧笔记

### 搜索优化

添加到 `.obsidian/search.json`（如果文件存在）：
```json
{
  "exclude": [
    "99-SYSTEM/**",
    "node_modules/**",
    ".git/**"
  ]
}
```

---

## 移动端配置

Brain OS 在 Obsidian Mobile（iOS/Android）上也能工作：

1. 使用 **Obsidian Sync** 或 **iCloud** 同步你的 vault
2. 安装同样的必装插件（Dataview、Templater）
3. 将首页设为每日简报以便移动端快速访问
4. 使用 **Quick Add** 小组件在移动端快速捕捉
