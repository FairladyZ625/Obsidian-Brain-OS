> 本文档为英文版的中译本。如有歧义，以英文原版为准。

# Skills 指南 — 理解和自定义 Brain OS Skills

---

## 什么是 Skills？

Skills 是告诉 AI agent 如何执行特定任务的专门指令集。在 Brain OS 中，skills 驱动 nightly pipeline、个人事务和知识管理。

每个 skill 是一个目录，至少包含一个 `SKILL.md` 文件，内容有：
- **描述**：何时激活此 skill
- **指令**：逐步流程
- **模板**：输出格式和文件位置
- **护栏**：skill 不应该做什么

---

## 核心 Skills

### 1. `article-notes-integration`

**做什么：** 处理原始文章笔记并整合到知识库中。

**何时运行：** 每天 02:00（通过 cron）

**关键行为：**
- 从 `02-WORKING/01-ARTICLE-NOTES/` 读取新/待处理文章
- 提取关键概念并写入领域知识卡片
- 有理由时更新主题页
- 写入共享 nightly digest
- 没有信号时不强制更新

**读取的文件：**
- `02-WORKING/01-ARTICLE-NOTES/*.md`（状态：pending）
- `01-READING/01-DOMAINS/*.md`（现有知识作为上下文）

**写入的文件：**
- `01-READING/01-DOMAINS/*.md`（新建/更新知识卡片）
- `01-READING/02-TOPICS/*.md`（主题页更新）
- `01-READING/04-DIGESTS/nightly-digest-YYYY-MM-DD.md`
- `99-SYSTEM/03-INTEGRATION-REPORTS/run-reports/YYYY-MM-DD/article-integration-report-YYYY-MM-DD.md`

### 2. `conversation-knowledge-flywheel`

**做什么：** 从 AI 对话转录中挖掘可操作洞见。

**何时运行：** 每天 03:00（通过 cron）

**关键行为：**
- 通过 `scripts/export-conversations.sh` 导出最近对话
- 使用语义搜索（QMD）查找相关的过往知识
- 有理由时生成 1-3 条知识笔记草稿
- 永远不会将原始转录倒入 Brain

### 3. `knowledge-flywheel-amplifier`

**做什么：** 交叉引用知识条目，发现连接。

**何时运行：** 每天 04:00（通过 cron）

**关键行为：**
- 读取完整的 nightly digest（阶段 1 & 2 输出）
- 在相关笔记间添加交叉引用
- 生成"今日推荐阅读"
- 这是"大局"综合阶段

### 4. `personal-ops-driver`

**做什么：** 管理个人事务系统——待办、简报、计划。

**何时运行：** 每天 07:00（晨间简报）+ 临时触发

**关键行为：**
- 从 todo-backlog + 承诺 + 决策生成每日简报
- 永远不删除用户事项（只重排、合并、降级）
- 将更改提交到 Brain git 仓库

### 5. `deep-research`

**做什么：** 对主题进行深度研究，生成综合报告。

**何时运行：** 按需（用户触发）

**关键行为：**
- 接受研究问题作为输入
- 搜索网络、阅读来源、综合发现
- 生成结构化研究笔记
- 适当时将发现整合到 Brain

### 6. `notebooklm`

**做什么：** 与 Google NotebookLM 集成进行深度研究。

**何时运行：** 按需（用户触发）

---

## 推荐通用 Skills

这些 skills 增强核心系统但非必需：

| Skill | 用途 | 何时使用 |
|-------|------|----------|
| `planning-with-files` | 用 markdown 文件做持久化规划 | 开始复杂项目 |
| `brainstorming` | 构建前的创意探索 | 设计功能或方案 |
| `writing-plans` | 结构化执行计划 | brainstorming 之后，构建之前 |
| `writing-skills` | 创建新 skills | 想扩展 Brain OS |
| `humanizer` | 让 AI 文字更自然 | 打磨 AI 生成的内容 |
| `polish` | 最终质量检查 | 发布或分享前 |
| `critique` | 设计审查 | 审查架构或决策 |
| `extract` | 提取可复用组件 | 在现有工作中找模式 |
| `distill` | 简化复杂设计 | 降低复杂性 |
| `normalize` | 确保设计一致性 | 维护标准 |
| `clarify` | 改进 UX 文案和标签 | 让界面更清晰 |
| `arrange` | 改进布局和间距 | 视觉设计改进 |
| `optimize` | 性能优化 | 速度和效率 |
| `teach-impeccable` | 为 AI 收集上下文 | 准备全面的简报 |
| `skill-creator` | 从零创建新 skills | 扩展系统 |
| `skillshare` | 在 agent 间共享 skills | 团队协作 |

---

## 自定义 Skills

### 添加新 Skill

1. 创建目录：`skills/my-skill/`
2. 编写带 frontmatter 的 `SKILL.md`：

```yaml
---
name: my-skill
description: 何时激活此 skill
---
```

3. 添加指令、模板和护栏
4. 复制到 `~/.agents/skills/my-skill/`（或你的 skills 目录）

### 修改现有 Skills

直接编辑 `SKILL.md`。更改在下次激活该 skill 的 AI session 生效。

**重要：** 保持 frontmatter 格式。OpenClaw 使用 `name` 和 `description` 来匹配 skills 和用户请求。

### 禁用 Skill

将 `SKILL.md` 重命名为 `SKILL.md.disabled` 或将 skill 目录移出 skills 路径。

---

## Skill 文件结构

```
skills/my-skill/
├─ SKILL.md              # 主 skill 定义（必需）
├─ references/           # 支撑文件（可选）
│   ├─ guide.md
│   └─ examples.md
├─ scripts/              # 辅助脚本（可选）
│   └─ preflight.sh
└─ templates/            # 输出模板（可选）
    └─ output-template.md
```

---

## 编写好的 Skill 指令

### 要
- 明确文件路径（使用 `{{BRAIN_PATH}}` 保证可移植性）
- 包含护栏（不该做什么）
- 定义清晰的输出格式
- 指定 commit 要求
- 包含错误处理指令

### 不要
- 写模糊指令（"be helpful"）
- 跳过护栏部分
- 硬编码个人信息
- 假设 AI 有之前 session 的上下文
