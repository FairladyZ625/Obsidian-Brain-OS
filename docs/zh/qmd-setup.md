# QMD 向量检索配置指南

> QMD（Query-Memory-Docs）用于为 Brain OS vault 配置向量 / 混合检索。

---

## 什么是 QMD？

QMD（Query-Memory-Docs）是一个需要单独安装的本地检索引擎，用于向量检索 / 混合检索。它能让你用自然语言在知识库中做语义搜索。

**重要边界：QMD 不是 OpenClaw 默认内置组件。** Brain OS 推荐在 QMD 已安装且可用时，把它作为 OpenClaw Agent 的优先语义检索后端；但用户仍然需要单独安装和配置 QMD。

QMD 可以提供：

- **语义搜索**：用自然语言找内容，不依赖关键词精确匹配
- **混合检索**：向量检索 + BM25 全文检索结合，召回率更高
- **rerank**：对候选结果二次排序，提升精度
- **本地优先索引**：vault 和 transcript 索引留在本机

在 Brain OS 的 Nightly Pipeline 中，QMD 是 conversation mining 在可用时的优先召回层。

---

## 什么时候需要 QMD？

| 场景 | 是否需要 QMD |
|---|---|
| vault < 200 条笔记 | ❌ 通常手动搜索够用 |
| vault 200-500 条笔记 | 🟡 可选，有 QMD 效果更好 |
| vault > 500 条笔记 | ✅ 推荐 |
| 运行 conversation mining / nightly pipeline | ✅ 推荐作为主召回层 |
| 只做知识整理 + 个人事务 | ❌ 可选，可以跳过 |

如果 QMD 不可用，Brain OS prompt 应该进入 degraded mode，并回退到 `grep` / `ripgrep`。召回率会下降，但 pipeline 仍然可以运行。

---

## 单独安装 QMD

请根据你使用的 QMD 包或仓库说明安装。安装后，先确认 QMD CLI 可用：

```bash
qmd status
# 或者如果安装在自定义路径：
/path/to/qmd status
```

然后用以下任一方式让 Brain OS 脚本能找到它：

```bash
# 方式 A：把 qmd 放进 PATH
export PATH="/path/to/qmd/bin:$PATH"

# 方式 B：为 Brain OS 脚本指定 binary
export QMD_BIN="/path/to/qmd"
export QMD_BIN_REAL="/path/to/qmd"
```

不要假设每个 OpenClaw 安装都有 `openclaw qmd ...` 命令。除非你的 OpenClaw 发行版明确提供了 QMD wrapper，否则请直接使用已安装的 QMD binary。

---

## Brain OS 推荐索引范围

安装 QMD 后，建议索引这些目录：

| 来源 | 作用 |
|---|---|
| `{{BRAIN_ROOT}}/03-KNOWLEDGE` | 正式知识笔记 |
| `{{BRAIN_ROOT}}/05-PROJECTS` | 项目 brief 和计划 |
| `{{TRANSCRIPT_DIR}}` | 导出的对话 transcript |
| `{{WORKSPACE_ROOT}}` | 可选 workspace 文档 / prompts |

不同 QMD 发行版的命令可能不同，但常见模式是：

```bash
qmd update
qmd embed
qmd query "agent architecture decisions"
```

Brain OS 脚本中优先使用 `QMD_BIN`，这样用户可以自己决定 QMD binary 路径。

---

## 在 Brain OS 中使用 QMD

QMD 主要用于两个场景：

1. **Nightly Pipeline**：`conversation-knowledge-flywheel` 可以使用 QMD 做高召回候选检索。
2. **日常知识检索**：agent 在回答前可以用 QMD 搜大型 vault / workspace。

写 agent 指令时应使用条件式口径：

- ✅ “QMD 可用时优先使用。”
- ✅ “如果 QMD 缺失或不健康，明确报告 degraded mode，并回退到关键词检索。”
- ❌ “OpenClaw 默认自带 QMD。”

---

## OpenClaw 配置边界

OpenClaw 负责 agent、频道、模型和 cron 投递路由。QMD 是独立检索引擎。

OpenClaw 配置示例见：

- [OpenClaw 配置指南](openclaw-config-guide.md)
- `examples/openclaw/openclaw.example.json`
- `examples/openclaw/openclaw.multi-channel.example.json`

如果 Brain OS 脚本需要非默认 QMD 路径，请在运行 OpenClaw 的环境中设置 `QMD_BIN` / `QMD_BIN_REAL`。

---

## 常见问题

| 问题 | 解决方案 |
|---|---|
| `qmd: command not found` | 先单独安装 QMD，再加入 `PATH` 或设置 `QMD_BIN` |
| `QMD unhealthy` | 用你的 QMD CLI 重建或修复索引 |
| 搜索结果不相关 | 如果中文内容多，换用更适合中文 / 多语言的 embedding 模型 |
| native module mismatch | 为当前 Node/runtime 版本重装或重建 QMD |
| Pipeline 报 degraded mode | 检查 transcript 路径、QMD binary 路径和 QMD 索引健康 |

---

## 相关文档

- [OpenClaw 配置指南](openclaw-config-guide.md)
- [OpenClaw 配置](openclaw-setup.md)
- [Nightly Pipeline 详解](nightly-pipeline.md)
- [知识库架构](knowledge-architecture.md)
