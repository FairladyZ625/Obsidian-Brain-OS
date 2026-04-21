# Obsidian Brain OS 入门指南

> 本文档为英文版的中译本。如有歧义，以英文原版为准。

> 你的 AI 增强型个人上下文系统。从零到运行，30 分钟搞定。

---

## 你将要构建什么

Brain OS 将 Obsidian 打造为一个**活的个人上下文系统**——不仅仅是一个笔记应用，而是一个 AI agent 能够主动处理、关联和呈现你知识的工作空间。

完成设置后：
- 你只需捕获一次（文章、想法、待办）
- AI 不只是帮你生产知识，也可以持续帮你保鲜、整理和治理知识系统
- 你醒来时看到的是精筛摘要、有序知识库和每日简报

---

## 前置要求

| 工具 | 用途 | 是否必需 |
|------|------|----------|
| [Obsidian](https://obsidian.md) | Vault 界面 | ✅ 必需 |
| [OpenClaw](https://docs.openclaw.ai) | AI 调度 + cron | ✅ 用于夜间 pipeline |
| Git | Vault 版本控制 | ✅ 推荐 |
| Python 3.8+ | 部分脚本 | ✅ 用于完整 pipeline |
| `convs` CLI | 导出 AI 对话 | 可选 |

---

## 第零步建议：先走最小成功路径

如果你是第一次安装，不要一上来就启完整系统。

建议：
- **Minimal**：先跑通知识系统最小版
- **Standard**：如果你还想尽快接上个人事务管理
- **Advanced**：只有在你明确要完整多 Agent / nightly / 治理系统时再选

先看：[安装档位说明](../install-profiles.md)

---

## 第一步：克隆仓库

```bash
git clone https://github.com/FairladyZ625/Obsidian-Brain-OS.git
cd Obsidian-Brain-OS
```

如果你希望让 AI Agent 帮你安装，到这里就可以切到：
- [INSTALL_FOR_AGENTS.md](../../INSTALL_FOR_AGENTS.md)

---

## 第二步：优先运行 setup

推荐路径：

```bash
bash setup.sh
```

如果你要走更适合 Agent 编排的无人值守路径，也可以用：

```bash
bash setup.sh --non-interactive --profile minimal
```

它会引导你完成：
- vault 路径
- 用户信息
- workspace 路径
- skills 路径
- 可选扩展
- 基础验证

如果你想先理解安装分层，再运行 setup，请看：[安装档位说明](../install-profiles.md)

---

## 第三步：打开你的 Vault

安装完成后，打开 Obsidian → **File → Open Vault** → 选择你刚创建的 vault 路径。

---

## 第四步：验证安装

运行：

```bash
bash scripts/verify-install.sh
```

它会检查：
- config 是否存在
- 关键值是否已写入
- vault 结构是否完整
- 选中的 skills 是否已安装
- 核心脚本是否能跑
- PII 扫描是否通过

如果验证失败，先修复失败项，再继续启高级模块。

---

## 第五步：选择你的安装配置

### 🧠 配置 A：仅知识系统
适用场景：构建个人上下文库、整理研究资料

安装以下 skills：
- `skills/article-notes-integration/`
- `skills/deep-research/`
- `skills/recommended/planning-with-files/`
- `skills/recommended/brainstorming/`

设置以下 cron job（来自 `cron-examples/nightly-pipeline.json`）：
- `article-notes-integration-nightly` (02:00)
- `knowledge-lint-weekly` (周一 01:00)

### 📋 配置 B：仅个人 Ops
适用场景：AI 驱动的每日规划、待办管理

安装以下 skills：
- `skills/personal-ops-driver/`

设置以下 cron job（来自 `cron-examples/personal-ops.json`）：
- `personal-ops-morning-brief` (07:00 每日)
- `personal-ops-todo-reminder-1500` (15:00 每日)
- `personal-ops-weekly-plan` (周一 05:10)

### 🌙 配置 C：完整夜间 Pipeline
适用场景：最大化自动化、知识持续复合增长

安装所有 skills + 所有 cron job。详见 [夜间 Pipeline 文档](nightly-pipeline.md)。

---

## 第六步：安装或扩展 Skills

如果你已经运行了 `bash setup.sh`，所选 skills 可能已经安装好了。

如果你要手动补装，只复制你真正需要的 skills：

```bash
cp -r skills/article-notes-integration/ ~/.agents/skills/
cp -r skills/personal-ops-driver/ ~/.agents/skills/
```

不要默认一上来安装整棵 skills 树，除非你明确要完整系统。

---

## 第七步：设置 Cron Jobs（OpenClaw）

```bash
# 导入夜间 pipeline 任务
openclaw cron import cron-examples/nightly-pipeline.json

# 导入个人 ops 任务
openclaw cron import cron-examples/personal-ops.json
```

或手动编辑 `~/.openclaw/cron/jobs.json`，参考 `cron-examples/` 中的格式。

> ⚠️ 启用前：请替换 cron 配置文件中的所有 `{{PLACEHOLDER}}` 值。

---

## 第八步：先拿到一个小成功后，再加治理层

当最小安装跑通后，你可以把 Brain OS 从“知识生产”继续扩展到更完整的知识系统：

- `prompts/cron/qmd-index-refresh-daily.md` 负责检索保鲜
- `prompts/cron/knowledge-librarian-3day.md` 负责周期整理
- `prompts/cron/knowledge-governance-10day.md` 负责周期治理复核

推荐顺序：
- 先跑创建
- 再加保鲜
- 再加整理
- 最后加治理

这样更容易让新用户先拿到一个确定成功，再逐层上治理能力。

## 第九步：先拿到一个小成功

推荐的第一个成功点：
- 在 Obsidian 里打开 vault
- 跑通 `bash scripts/verify-install.sh`
- 加一条文章 note
- 只启一个相关 cron profile

拿到第一个成功之后，再决定是否启用 Observer、CI/CD、QMD 或完整 nightly system。

---

## 第一周行动计划

**第一天：** 打开 Obsidian，探索 vault 结构，阅读 `00-INBOX/README.md`

**第二天：** 在 `03-KNOWLEDGE/02-WORKING/01-ARTICLE-NOTES/` 中添加 3-5 篇文章链接。让 AI 当晚处理。

**第三天：** 在 `03-KNOWLEDGE/01-READING/04-DIGESTS/` 查看你的第一个夜间摘要。

**第四到七天：** 在 `00-INBOX/todo-backlog.md` 添加待办。在 `01-PERSONAL-OPS/01-DAILY-BRIEFS/` 查看你的早间简报。

---

## 故障排除

常见问题见 [FAQ](faq.md)。

- Obsidian 不显示 vault → 检查 vault 路径是目录而非文件
- 脚本运行失败 → 先执行 `source scripts/config.env`
- Cron job 不运行 → 验证 OpenClaw 正在运行（`openclaw gateway status`）
- 知识 lint 无发现 → 确认 `BRAIN_PATH` 指向 vault 根目录
- 想先看安装分层 → 读 [install-profiles.md](../install-profiles.md)
- 想让 AI Agent 帮你装 → 读 [INSTALL_FOR_AGENTS.md](../../INSTALL_FOR_AGENTS.md)
