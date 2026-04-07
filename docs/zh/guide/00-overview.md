# 📖 Brain OS 使用指南 — 总览

> 这套系统不是装好就能用的。它需要你理解方法论、配置好 Agent、然后持续迭代。
> 这份指南帮你从零到一。

---

## 阅读顺序

按顺序阅读。每篇文档都引用前一篇的概念。

| 顺序 | 文档 | 主题 | 读完后你能做什么 |
|------|------|------|-----------------|
| 1 | [00-philosophy.md](00-philosophy.md) | 核心方法论 | 理解为什么要这样设计 |
| 2 | [01-agent-setup.md](01-agent-setup.md) | OpenClaw Agent 配置 | 搭建你自己的 AI Agent |
| 3 | [02-channel-design.md](02-channel-design.md) | 频道设计 | 设计频道分工，防止上下文污染 |
| 4 | [03-daily-workflow.md](03-daily-workflow.md) | 日常工作流 | 日常怎么用这套系统 |
| 5 | [04-iteration-guide.md](04-iteration-guide.md) | 迭代指南 | 持续优化你的系统 |

---

## 核心认知

### 这不是一个"装完就用"的工具

Brain OS 提供的是：
- **方法论**：怎么组织个人知识、怎么管理事务
- **模板**：我们验证过的目录结构、文档模板、脚本
- **Skill**：AI Agent 的专用指令集
- **教程**：告诉你怎么配、怎么用、怎么改

**你需要自己做的**：
- 配置你的 OpenClaw Agent（JSON 配置）
- 设计你的频道分工
- 按你的习惯调整 Prompt 和 Skill
- 持续迭代，让系统越来越适合你

### Agent 的质量决定系统的质量

如果你的 AI Agent 配得不好：
- Nightly pipeline 不会正确处理文章
- 每日驾驶舱会生成垃圾内容
- Todo 管理会混乱

所以，先花时间把 Agent 配好，再启用自动化。

### 分频道是关键设计

不要把所有事情都扔给一个频道。频道分工的核心目的：**防止上下文污染**。

- 事务管理频道 → Agent 只看事务相关的上下文
- 文章沉淀频道 → Agent 只处理文章相关的工作
- 知识检索频道 → Agent 专注于检索和回答

这样每个 Agent 的上下文都是干净的，判断更准确。

---

## 快速路径

如果你已经很熟悉 OpenClaw 和 AI Agent：

1. Clone 仓库
2. 复制 vault-template 到你的 Obsidian vault
3. 安装 skills
4. 导入 cron 配置
5. 参考 [01-agent-setup.md](01-agent-setup.md) 配置 Agent
6. 参考 [02-channel-design.md](02-channel-design.md) 设计频道
7. 启用 cron jobs

详细步骤见 [getting-started.md](../getting-started.md)。

---

## 给你的 Agent 看的

如果你的 AI Agent 需要理解 Brain OS 的安装和使用：
- 让它先读这篇总览
- 然后按顺序阅读 `docs/zh/guide/` 下的文档
- 安装时让它参考 `skills/brain-os-installer/SKILL.md`
