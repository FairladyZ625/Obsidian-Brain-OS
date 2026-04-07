# 夜间 Pipeline — AI 如何在你睡眠时处理你的知识

> 本文档为英文版的中译本。如有歧义，以英文原版为准。

---

## 概述

夜间 pipeline 通过 OpenClaw cron job 自动运行。三个阶段在凌晨 02:00 到 04:00 之间处理你的知识，每天早晨生成一份精筛摘要。

**核心原则：** 每个阶段相互隔离。一个失败不影响其他阶段。没有阶段依赖另一个的成功。

---

## 阶段一：文章整合（02:00）

**功能：** 将 `02-WORKING/01-ARTICLE-NOTES/` 中的原始文章笔记整合到知识库中。

**输入：**
- 新增/待处理文章笔记（状态：`pending`）
- 现有领域知识卡片（作为上下文）

**输出：**
- 更新后的领域知识卡片（位于 `01-READING/01-DOMAINS/`）
- 新增或更新的主题页面（位于 `01-READING/02-TOPICS/`）
- 模式候选（位于 `02-WORKING/02-PATTERN-CANDIDATES/`，如有检测到模式）
- 摘要小节：`## 02:00 Article Integration`
- 运行报告：`99-SYSTEM/03-INTEGRATION-REPORTS/run-reports/YYYY-MM-DD/article-integration-report-YYYY-MM-DD.md`

**行为：**
- 如无新文章：写入"无操作"报告和简短摘要说明
- 将文章笔记状态从 `pending` 更新为 `integrated`
- 仅在有充分理由时更新领域卡片（非强制）

---

## 阶段二：对话挖掘（03:00）

**功能：** 导出最近的 AI 对话并从中挖掘洞见、决策和知识。

**输入：**
- AI 对话记录（由 `scripts/export-conversations.sh` 导出）
- 今日摘要（了解阶段一已完成的内容）

**输出：**
- 1-3 份知识笔记草稿（如有充分理由）
- 模式候选或研究种子
- 摘要小节：`## 03:00 Conversation Mining`
- 运行报告：`99-SYSTEM/03-INTEGRATION-REPORTS/run-reports/YYYY-MM-DD/conversation-mining-report-YYYY-MM-DD.md`

**行为：**
- 需要 `convs` CLI 导出对话（不可用时优雅跳过）
- 有 QMD（query-memory-docs）时用于语义搜索
- 记录缺失时进入降级模式
- 绝不将原始对话记录转储到 Brain

---

## 阶段三：知识放大（04:00）

**功能：** 阅读完整夜间摘要，在知识条目之间建立关联，并生成推荐。

**输入：**
- 今日完整夜间摘要（阶段一和阶段二输出）
- 领域知识卡片
- 主题页面

**输出：**
- 向现有笔记添加交叉引用和关联
- 摘要中"今日推荐阅读"小节
- 摘要小节：`## 04:00 Knowledge Amplification`
- 运行报告：`99-SYSTEM/03-INTEGRATION-REPORTS/run-reports/YYYY-MM-DD/knowledge-amplifier-report-YYYY-MM-DD.md`

**行为：**
- 跨所有阶段综合分析——这是"全局视野"阶段
- 推荐今日值得阅读的内容
- 建议潜在的研究方向
- 绝不强制建立不存在的关联

---

## 辅助任务

### 知识 Lint（周一 01:00）

运行 `scripts/knowledge-lint.sh` 检查知识库健康状况：
- 缺失 frontmatter 字段
- 损坏的链接
- 孤立页面
- 停滞条目（活跃但 30 天以上未更新）
- 标签一致性

输出：`12-REVIEWS/KNOWLEDGEBASE/lint-YYYY-MM-DD.md`

### 每日知识画布（05:00）

可选任务，使用 `scripts/daily-knowledge-canvas.sh` 生成知识图谱可视化。

### 早间简报（07:00）

在 `01-PERSONAL-OPS/01-DAILY-BRIEFS/daily-briefing.md` 生成每日个人 ops 驾驶舱。

---

## 如何阅读摘要

每天早晨打开 `03-KNOWLEDGE/01-READING/04-DIGESTS/nightly-digest-YYYY-MM-DD.md`。

```
🌙 Nightly Digest — 2026-04-07

## 02:00 Article Integration
  处理了 3 篇文章。新增主题："AI Agent Architectures"。
  值得阅读：OpenAI function calling patterns 卡片。

## 03:00 Conversation Mining
  从昨天的编码会话中发现 2 个可执行的洞见。
  关键收获：API 速率限制的重试模式。

## 04:00 Knowledge Amplification
  建立了关联：function calling ↔ tool use patterns ↔ agent reliability。
  推荐阅读：function-calling-patterns.md

## 今日推荐阅读
  1. function-calling-patterns.md（新增，高相关性）
  2. ai-agent-architectures.md（已更新，新增关联）
```

**从这里开始。** 如果你对某些内容感兴趣，深入阅读链接的笔记。

---

## 自定义 Pipeline

### 更改调度时间

编辑 `cron-examples/` 中的 cron 配置文件：

```json
{
  "schedule": {
    "kind": "cron",
    "expr": "0 2 * * *",    // 改为你偏好的时间
    "tz": "America/New_York" // 改为你所在的时区
  }
}
```

### 禁用某个阶段

在 cron job 配置中设置 `"enabled": false`。

### 添加自定义阶段

1. 在 `prompts/` 中创建新的 prompt
2. 创建引用它的 cron job 条目
3. 遵循交接协议：读取现有摘要 → 填写你的小节 → 提交

---

## 故障排除

| 问题 | 解决方案 |
|------|----------|
| 摘要未生成 | 检查 cron 是否在运行（`openclaw gateway status`） |
| 每晚都是"无操作" | 没有新文章或对话——这是正常的 |
| 对话挖掘失败 | 安装 `convs` CLI 或在配置中设置 `CONVS_BIN` |
| 知识 lint 出错 | 检查 `BRAIN_PATH` 是否指向 vault 根目录 |
| Pipeline 覆盖了我的编辑 | Pipeline 只修改 `99-SYSTEM/` 和 `04-DIGESTS/`——除非启用自动更新，`01-READING/` 中的编辑是安全的 |
