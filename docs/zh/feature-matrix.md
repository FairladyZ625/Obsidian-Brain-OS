# Brain OS 功能清单（SSOT）

> English version: [docs/feature-matrix.md](../feature-matrix.md)

这是 Brain OS 功能的单一事实源：系统有哪些能力、每个能力由哪些仓库资产实现、如何安装启用、以及 AI agent 怎么判断本地部署是否已经装好。

适用场景：

- 不想一次复制整仓库，而是分阶段安装 Brain OS
- 让 agent 对比本地部署和开源框架，找出缺失能力
- 判断哪些功能是 core，哪些是 optional / advanced
- 给新 agent 一张“照着装、照着验”的总表

---

## 安装层级

| 层级 | 含义 |
|---|---|
| **Core** | 几乎所有 Brain OS 部署都建议安装 |
| **Standard** | 基础 vault + agent loop 跑通后建议启用 |
| **Advanced** | 能力强，但建议拿到第一个成功 workflow 后再启用 |
| **Optional** | 领域特定或集成特定 |
| **Maintainer** | 主要给仓库维护者 / 贡献者使用 |

---

## 功能矩阵

| 功能 | 层级 | 作用 | 主要资产 | 安装 / 启用 | Agent 如何检查 |
|---|---|---|---|---|---|
| Vault 模板 | Core | 提供 Obsidian 基础目录结构 | `vault-template/` | `bash setup.sh` 或复制模板 | 检查 vault 中存在 `00-INBOX/`、`03-KNOWLEDGE/`、`05-PROJECTS/` |
| 安装器 | Core | 交互式 / 非交互式初始化 vault、config、skills | `setup.sh`、`skills/brain-os-installer/SKILL.md`、`INSTALL_FOR_AGENTS.md` | 运行 `bash setup.sh`；agent 从 `INSTALL_FOR_AGENTS.md` 开始 | 带 `BRAIN_OS_CONFIG` 运行 `bash scripts/verify-install.sh` |
| OpenClaw Brain OS install pack | Core | 提供可安装的 OpenClaw 分发包，包含 config patch 模板、workspace bootstrap、skill manifest 和 canonical vault-template 接入 | `packs/openclaw-brain-os/` | 从 `packs/openclaw-brain-os/README.md` 开始；PR1b 支持 --check/--dry-run preview，后续 PR 增加 safe apply/rollback | 运行 `bash packs/openclaw-brain-os/tests/smoke.sh`；验证 JSON 模板和无私有信息 |
| 配置环境 | Core | 保存用户路径和运行变量 | `scripts/config.env.example` | 复制为 `scripts/config.env` 或由 setup 生成 | 检查 `BRAIN_PATH`、`WORKSPACE_PATH`、`SKILLS_PATH`、`USER_NAME`、`TIMEZONE` |
| 安装验证器 | Core | 验证 vault、config、skills、lint、PII 检查 | `scripts/verify-install.sh` | setup 后运行 | 命令 exit 0；故意跳过的 optional feature 有 warning 可接受 |
| PII / 私有路径扫描 | Core | 防止私有数据进入提交 | `scripts/check-pii.sh`、`.github/workflows/pii-scan.yml`、`docs/references/pii-deidentification-guide.md` | commit / PR 前运行 | `bash scripts/check-pii.sh --strict` 返回 0 |
| Brain config leak scan | Core | 扫描已知私有 Brain OS 配置泄露 | `scripts/check-brain-config-leaks.sh`、`.github/workflows/brain-config-scan.yml` | PR 前运行 | `bash scripts/check-brain-config-leaks.sh --strict` 返回 0 |
| Article notes integration | Core | 把外部文章整理成结构化知识笔记 | `skills/article-notes-integration/`、`prompts/article-notes-integration.prompt.md`、`prompts/article-integration.prompt.md` | 安装 skill 到 agent skills 目录；配置 vault 路径 | `~/.agents/skills/article-notes-integration/` 存在，并能写入 `03-KNOWLEDGE` |
| 知识库架构 | Core | 定义 Reading / Working / System 三层知识结构 | `docs/knowledge-architecture.md`、`docs/zh/knowledge-architecture.md`、`vault-template/03-KNOWLEDGE/` | 阅读文档；保持 vault 结构 | 检查 `03-KNOWLEDGE` 预期子目录存在 |
| OpenClaw agent runtime | Core | 运行 agents、sessions、channels、cron jobs 和频道级 systemPrompt | `docs/openclaw-setup.md`、`docs/openclaw-config-guide.md`、`examples/openclaw/` | 用 examples 配置 `~/.openclaw/openclaw.json` | `openclaw status`；在每个配置频道发测试消息；确认专用 Discord 频道存在对应 `systemPrompt` |
| Agent 团队配置 | Core | 定义 main / specialized agents 和 skills | `docs/agents.md`、`docs/zh/agents.md` | 在 OpenClaw 或你的 runtime 中配置 agents | 检查 agent IDs、workspaces、models、skills 已配置 |
| Agent bootstrap + references | Core | 提供可复制的 `AGENTS.md`、`USER.md` 和按需读取 reference 模板，帮助安全搭建 agent workspace | `docs/agent-bootstrap-guide.md`、`docs/zh/agent-bootstrap-guide.md`、`examples/agent-workspace/` | 复制示例到 agent workspace，替换占位符，并把长流程放进 `references/` | 检查 `AGENTS.md` 有 reference 索引、`USER.md` 不含密钥、索引文件存在 |
| OpenClaw cron examples | Standard | 可导入的 recurring Brain OS jobs 模板 | `cron-examples/*.json`、`cron-examples/README.md` | `openclaw cron import cron-examples/<profile>.json` | 检查 `~/.openclaw/cron/jobs.json` 有导入任务且占位符已替换 |
| Nightly pipeline | Standard | 运行文章整合、对话挖掘、知识放大、摘要 | `docs/nightly-pipeline.md`、`docs/nightly-pipeline-guide.md`、`cron-examples/nightly-pipeline.json`、`prompts/cron/*nightly*.md` | 导入 cron profile；替换占位符；逐层启用 | 检查 nightly jobs 存在、已启用，并写出预期 digest |
| Conversation knowledge flywheel | Standard | 从对话中挖掘可复用知识模式 | `skills/conversation-knowledge-flywheel/`、`prompts/conversation-knowledge-flywheel.prompt.md`、`prompts/cron/conversation-knowledge-flywheel-nightly.md` | 安装 skill；配置 transcript 来源和 vault 路径 | 检查 transcript 输入目录和输出 notes / digests |
| 内嵌 conversation-mining 工具 | Standard | 导出和查看 agent 对话 transcript | `tools/conversation-mining/` | 从 tool 目录安装或运行 | `python tools/conversation-mining/convs.py --help` 或对应 CLI 可运行 |
| Knowledge flywheel amplifier | Standard | 跨来源综合 pattern 和 weak signals | `skills/knowledge-flywheel-amplifier/`、`prompts/knowledge-flywheel-amplifier.prompt.md`、`prompts/cron/knowledge-flywheel-amplifier-nightly.md` | 安装 skill；等 article / conversation 输入存在后启用 | 检查 synthesis / digest notes 是否生成 |
| Personal Ops | Standard | 每日 dashboard、待办、提醒、commitment、morning brief | `skills/personal-ops-driver/`、`docs/personal-ops.md`、`cron-examples/personal-ops.json`、`prompts/personal-ops-*.prompt.md` | 安装 skill；导入 personal ops cron profile | 检查 daily brief 文件和 todo backlog 存在 |
| Morning brief insight analysis | Standard | 把知识信号与 active projects / todos 连接起来 | `prompts/personal-ops-morning-brief.prompt.md`、`prompts/cron/personal-ops-morning-brief.md`、`docs/personal-ops.md` | 使用当前 personal ops prompts | 检查 brief 中有 insight candidates 或明确 rejection reasons |
| Apple Reminders sync | Optional | Brain todos 与 Apple Reminders 双向同步 | `scripts/brain-to-reminders.sh`、`scripts/reminders-to-brain.sh`、`prompts/cron/brain-to-reminders-0730.md`、`prompts/cron/reminders-to-brain-2100.md` | 配置 macOS Reminders 权限和 `BRAIN_ROOT` | 手动运行脚本，验证 todo 状态能 round-trip |
| Daily timesheet | Optional | 根据 commits 和项目上下文生成工时草稿 | `skills/daily-timesheet/`、`prompts/cron/daily-timesheet-1730.md` | 安装 skill，按需配置 backend | 检查 timesheet draft 输出；如用 backend，确认集成已配置 |
| Chronicle / channel historian | Optional | 定期总结有价值的频道历史 | `docs/chronicle-agent.md`、`docs/zh/chronicle-agent.md`、`prompts/cron/chronicle-every-2h-log.md` | 配置频道访问和 cron delivery | 检查 history logs 是否写入，必要时是否 commit |
| NotebookLM / deep research | Optional | 支持 research seeds 和外部研究工作流 | `skills/notebooklm/`、`skills/deep-research/`、`docs/notebooklm.md` | 安装对应 skill 并配置凭证 / 工具 | 检查 skill 已安装且所需凭证 / 工具可用 |
| QMD 语义检索 | Optional / Advanced | 为大型 vault 和 transcript mining 提供本地语义 / 混合检索 | `docs/qmd-setup.md`、`docs/zh/qmd-setup.md`、`prompts/cron/qmd-index-refresh-daily.md` | 单独安装 QMD；设置 `QMD_BIN` 或把 `qmd` 放入 `PATH` | `qmd status` 或 `$QMD_BIN status`；pipeline 不应声称 QMD 是 OpenClaw 内置 |
| 知识库治理栈 | Advanced | 长期保持 vault 新鲜、整洁、可治理 | `skills/brain-vault-governance/`、`docs/governance-cron-guide.md`、`cron-examples/governance.json`、`prompts/cron/knowledge-*.md` | 分阶段启用：refresh → librarian → governance | 检查 governance cron jobs 和只读 audit 输出 |
| Friction-to-governance loop | Advanced | 把重复运营摩擦转化为持久系统修复 | `docs/friction-to-governance-loop.md`、`prompts/friction-to-governance-loop.prompt.md`、`schemas/friction-*.schema.json`、`examples/friction-log.sample.jsonl` | 阅读方法论；手动或定期运行 prompt | 检查 friction reports 能通过 schema，并产出 write-back 决策 |
| Observer | Advanced | AI team health monitor 和改进建议循环 | `skills/observer/`、`docs/agent-playbooks/observer-playbook.md`、`prompts/cron/observer-daily-0001.md` | 初始化 `.learnings/observer/`；启用 observer cron | 检查 observer 输出和 `.learnings/observer/` ledger |
| Vault governance skill | Advanced | 帮 agent 判断持久 vault 文件应该写在哪里 | `skills/brain-vault-governance/`、`docs/references/vault-governance-guide.md` | 给会写 vault 的 agent 安装 skill | 检查 agent 写 / 移动正式文档前读取该 skill |
| Soft-link sync | Advanced | 维护本地文件和 vault references 之间的轻量链接 | `scripts/sync-knowledge-soft-links.py`、`prompts/cron/knowledge-soft-link-sync-nightly.md` | 启用前配置 source / target paths | dry-run 脚本并检查生成链接 |
| Release workflow | Maintainer | 版本号、changelog、PR、release、tag SOP | `skills/brain-os-release/`、`docs/agent-playbooks/release-playbook.md`、`docs/release-versioning.md` | 维护者 release PR 前安装 / 阅读 | 检查 PR title 带版本号、changelog 已更新、扫描通过 |
| GitHub CI | Maintainer | PR 自动保护：泄露扫描、结构检查、install smoke、changelog | `.github/workflows/*.yml` | GitHub PR 自动运行 | PR checks 全绿 |
| Contributor docs | Maintainer | 编写 skill、cron prompt、release notes、architecture 的指南 | `docs/skill-authoring-guide.md`、`docs/writing-cron-prompts.md`、`docs/architecture.md` | 贡献前阅读 | docs 存在并从 README / component guide 链接 |

---

## Agent 审计 Prompt

当你想让本地 AI agent 检查“哪些功能没装”时，可以直接给它这段：

```text
Read docs/feature-matrix.md in the Obsidian Brain OS repo.
Compare every feature row against my local deployment.
For each row, report one of: installed, partially installed, missing, intentionally skipped, or blocked.
Use the "How an agent checks it" column as the verification method.
Do not install optional or advanced features without asking.
Do not claim QMD is bundled with OpenClaw; verify QMD separately.
Return a prioritized install plan with Core gaps first, then Standard, then Optional/Advanced.
```

---

## 维护规则

以后给 Brain OS 增加新的用户可见功能时，必须在同一个 PR 更新本文件：

1. 在矩阵里增加一行
2. 链接主要资产
3. 说明如何启用
4. 说明 agent 如何验证
5. 同步更新英文版

如果某个能力只是内部运营物，不属于公开框架，不要列进这里。
