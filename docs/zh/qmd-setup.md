# QMD 向量检索配置指南

> QMD（Query-Memory-Docs）是 OpenClaw 内置的本地向量/混合检索层，用于在大型知识库中做语义搜索。

---

## 什么是 QMD？

QMD 是 OpenClaw 提供的本地向量检索引擎，它能：

- **语义搜索**：用自然语言找内容，不依赖关键词精确匹配
- **混合检索**（hybrid）：向量检索 + BM25 全文检索结合，召回率更高
- **rerank**：对候选结果二次排序，提升精度
- **本地运行**：所有数据留在本地，无需外部 API

在 Brain OS 的 Nightly Pipeline 中，QMD 是对话挖掘（conversation-knowledge-flywheel）的**主要召回层**。

---

## 什么时候需要 QMD？

| 场景 | 是否需要 QMD |
|------|------------|
| vault < 200 条笔记 | ❌ 不需要，手动搜索够用 |
| vault 200-500 条笔记 | 🟡 可选，有 QMD 效果更好 |
| vault > 500 条笔记 | ✅ 推荐，语义检索优势明显 |
| 运行对话挖掘 Pipeline | ✅ 推荐，QMD 是主召回层 |
| 只做知识整理，不跑 Pipeline | ❌ 不需要 |

**结论：如果你只用 Brain OS 的知识层 + 个人事务，不跑 Nightly Pipeline，可以跳过 QMD。**

---

## 安装 QMD

QMD 是 OpenClaw 的内置功能，随 OpenClaw 安装一起提供。

```bash
# 确认 OpenClaw 已安装
openclaw --version

# 查看 QMD 配置选项
openclaw qmd --help
```

---

## 配置 QMD for Brain OS

在 OpenClaw 配置文件（`~/.openclaw/openclaw.json` 或 `openclaw.yaml`）中添加 QMD 配置：

```json
{
  "qmd": {
    "provider": "openai",
    "model": "text-embedding-3-small",
    "mode": "hybrid",
    "sources": [
      {
        "path": "/tmp/brain-os-test/vault/03-KNOWLEDGE",
        "watch": true,
        "embedInterval": "6h"
      },
      {
        "path": "{{TRANSCRIPT_DIR}}",
        "watch": false,
        "embedInterval": "1d"
      }
    ]
  }
}
```

**配置说明：**

| 字段 | 说明 | 推荐值 |
|------|------|--------|
| `provider` | embedding 提供商 | `openai` / `local`（本地模型） |
| `model` | embedding 模型 | `text-embedding-3-small`（OpenAI）或 `qwen3-embedding-4b`（本地） |
| `mode` | 检索模式 | `hybrid`（推荐）/ `vector` / `bm25` |
| `sources[].path` | 要索引的目录 | Brain vault 的 03-KNOWLEDGE 目录 |
| `sources[].watch` | 是否实时监听文件变化 | 知识库用 `true`，对话目录用 `false` |
| `embedInterval` | 重新 embed 间隔 | `6h`（知识库），`1d`（对话） |

---

## 本地模型（无 OpenAI API）

如果你想完全本地化运行，可以使用本地 embedding 模型：

```json
{
  "qmd": {
    "provider": "local",
    "model": "qwen3-embedding-4b",
    "mode": "hybrid"
  }
}
```

**本地模型要求：** 需要 Ollama 或兼容的本地推理服务。参考 [OpenClaw 本地模型文档](../openclaw-setup.md)。

---

## 在 Brain OS 中使用 QMD

QMD 在 Brain OS 中主要用于两个场景：

### 场景 1：对话挖掘（Nightly Pipeline）

`conversation-knowledge-flywheel` skill 会自动使用 QMD 做对话内容的语义召回：

```bash
# 手动触发 QMD 更新（Nightly Pipeline 会自动做这步）
openclaw qmd update --path "/tmp/brain-os-test/vault/03-KNOWLEDGE"
openclaw qmd embed --path "{{TRANSCRIPT_DIR}}"
```

### 场景 2：知识检索（日常使用）

配置好 QMD 后，你可以用自然语言搜索 vault：

```bash
# 语义搜索示例
openclaw qmd query "关于 AI Agent 架构设计的笔记"

# 混合检索（推荐）
openclaw qmd query --mode hybrid "如何做对话挖掘"
```

---

## 健康检查与故障排查

```bash
# 检查 QMD 状态
openclaw qmd status

# 强制重建索引
openclaw qmd rebuild --path "/tmp/brain-os-test/vault/03-KNOWLEDGE"
```

**常见问题：**

| 问题 | 原因 | 解决方案 |
|------|------|---------|
| `QMD unhealthy` | 索引损坏或模型 ABI 不匹配 | `openclaw qmd rebuild` |
| 搜索结果不相关 | embedding 模型与内容语言不匹配 | 换用 `qwen3-embedding-4b`（中文更好）|
| `native module mismatch` | Node.js 版本升级后 QMD 未重新编译 | 重装 OpenClaw 或 `openclaw repair` |
| 索引速度慢 | vault 文件太多 | 调大 `embedInterval` 或缩小 `sources.path` |

---

## 降级模式

如果 QMD 不可用，`conversation-knowledge-flywheel` skill 会自动进入降级模式：

- 用 `grep` / `ripgrep` 做关键词搜索替代语义搜索
- 召回率下降，但 Pipeline 仍然可以运行
- 会在产出报告中明确标注 "degraded mode (QMD unavailable)"

**QMD 是可选增强，不是必须项。**

---

## 相关文档

- [OpenClaw 配置指南](openclaw-setup.md)
- [Nightly Pipeline 详解](nightly-pipeline.md)
- [知识库架构](knowledge-architecture.md)
