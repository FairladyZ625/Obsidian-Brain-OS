# 变更日志 / Changelog（中文版）

> 完整英文版见 [CHANGELOG.md](CHANGELOG.md)。本文件为中文对照版，内容与英文版一一对应。

---

## [1.5.8] — 2026-04-29

### 新增 / Added
- **`skills/brain-os-open-source-sync/`** — 新增 Brain OS 开源同步专用 skill，固化完整安装包 / 方法论双轨模型、A/B/C 分类、系统升级识别、nightly 计划流程与 PR checklist。

### 变更 / Changed
- **`prompts/cron/brain-os-daily-sync.md`** — daily sync 现在先读取开源同步 skill，再按完整安装包与方法论两条轨道归类候选项，最后做 A/B/C 判断。
- **`docs/governance-sync-boundary.md`** / **`docs/zh/governance-sync-boundary.md`** — 补充两条公开同步轨道，帮助维护者区分可安装包资产与可复用方法论资产。

## [1.5.7] — 2026-04-27

### 新增 / Added
- **Install report** — pack dry-run 与 apply 现在会生成 `INSTALL_REPORT.md`，汇总所选 profile、路径、安装资产、备份、变更、下一步和 rollback 指引。
- **Profile guide** — 新增 `packs/openclaw-brain-os/PROFILE_GUIDE.md`，帮助用户选择 `minimal`、`knowledge`、`personal-ops`、`team` 或 `full`。
- **Post-install checklist** — 新增 `packs/openclaw-brain-os/POST_INSTALL_CHECKLIST.md`，用于启用 cron 前的安全检查。

### 变更 / Changed
- **`packs/openclaw-brain-os/manifest.json`** — pack preview 版本升到 `1.0.0-alpha.5`，对应 install-report 阶段。

## [1.5.6] — 2026-04-27

### 新增 / Added
- **OpenClaw Brain OS pack profiles** — 新增 minimal、knowledge、personal-ops、team、full 的 profile-specific cron patch templates，基于公开 `cron-examples/` 生成，并强制所有 jobs 默认 disabled。
- **Bundled skills** — 新增公开脱敏 skill bundles：Brain vault governance、article integration、conversation flywheel、knowledge amplifier、personal ops、observer、Brain OS release。
- **Skill installation support** — apply 阶段会按所选 profile 以 missing-only 模式复制 bundled skills。

### 变更 / Changed
- **`packs/openclaw-brain-os/manifest.json`** — pack preview 版本升到 `1.0.0-alpha.4`，并对齐 profile cron groups。

## [1.5.5] — 2026-04-27

### 新增 / Added
- **OpenClaw Brain OS pack safe apply** — 新增 config 冲突检测、保守 OpenClaw config merge、cron job merge、temp-safe apply flow、backup state 和 config rollback 脚本。
- **Apply smoke fixture** — pack smoke 现在会安装到隔离的临时 OpenClaw root，并验证 rollback，不触碰真实用户配置。

### 变更 / Changed
- **`packs/openclaw-brain-os/manifest.json`** — pack preview 版本升到 `1.0.0-alpha.3`，对应 safe-apply 阶段。

## [1.5.4] — 2026-04-27

### 新增 / Added
- **OpenClaw Brain OS pack dry-run installer** — 新增 `install.sh --check`、`install.sh --dry-run`、`verify.sh`、render / placeholder / secret-scan 辅助脚本、minimal/full dry-run fixtures，并把 preview 生成纳入 smoke test。
- **Multi-workspace templates** — 新增 writer、review、chronicle、observer workspace 模板，作为 dry-run preview 中的 available assets。

### 变更 / Changed
- **`packs/openclaw-brain-os/manifest.json`** — pack skeleton 版本升到 `1.0.0-alpha.2`，对应 dry-run preview 阶段。

## [1.5.3] — 2026-04-27

### 新增 / Added
- **`packs/openclaw-brain-os/`** — 新增可安装 OpenClaw Brain OS 分发包的第一版静态骨架，包含 manifest、限制 scope 的 OpenClaw config patch 模板、main workspace bootstrap、canonical vault-template 策略、skill manifest、默认 disabled 的 cron placeholder 和 smoke test。
- **`.github/workflows/pack-smoke.yml`** — 新增 pack CI 检查，覆盖 JSON 合法性、canonical vault-template、cron 默认 disabled、禁止配置 scope 和私有/密钥内容扫描。

### 变更 / Changed
- **`docs/feature-matrix.md`** / **`docs/zh/feature-matrix.md`** 与 README 入口 — 补充分发 pack 的发现入口。

## [1.5.2] — 2026-04-27

### 新增 / Added
- **`examples/agent-workspace/AGENTS.example.md`**、**`examples/agent-workspace/USER.example.md`** 与 **`examples/agent-workspace/references/`** — 新增脱敏、可复制的 agent workspace bootstrap 模板。
- **`examples/openclaw/openclaw.channel-prompts.example.json`** — 新增 OpenClaw 频道级 `systemPrompt` 示例，展示如何在 `channels.discord.accounts.<accountId>.guilds.<guildId>.channels` 下为不同 Discord 频道配置不同提示词。
- **`docs/agent-bootstrap-guide.md`** / **`docs/zh/agent-bootstrap-guide.md`** — 新增中英双语指南，说明如何编写短小的 `AGENTS.md`，以及如何组织按需读取的 `references/` 操作手册。

### 变更 / Changed
- **`docs/feature-matrix.md`** / **`docs/zh/feature-matrix.md`** — 将 Agent bootstrap + references 加入 Core 功能清单，并补充安装与验证方法；同时明确专用 Discord 频道可通过检查频道级 `systemPrompt` 条目来验证。
- **`README.md`**、**`README_EN.md`** 与 **`docs/zh/README.md`** — 补充 agent bootstrap guide 和示例入口。

## [1.5.1] — 2026-04-27

### 新增 / Added
- **`examples/openclaw/openclaw.example.json`** 与 **`examples/openclaw/openclaw.multi-channel.example.json`** — 新增脱敏后的 OpenClaw 配置示例，覆盖单 agent 和 Discord 多频道设置。
- **`docs/openclaw-config-guide.md`** / **`docs/zh/openclaw-config-guide.md`** — 新增中英双语 `openclaw.json` 配置指南，说明频道路由、cron 投递、占位符、密钥和 QMD 边界。
- **`docs/feature-matrix.md`** / **`docs/zh/feature-matrix.md`** — 新增功能清单 SSOT，方便用户和 agent 查看所有公开 Brain OS 能力、安装资产与验证方法。

### 变更 / Changed
- **`docs/qmd-setup.md`** / **`docs/zh/qmd-setup.md`** — 明确 QMD 是需要单独安装的检索引擎，不是 OpenClaw 默认内置组件。
- **`docs/openclaw-setup.md`**、**`docs/zh/openclaw-setup.md`**、**`docs/getting-started.md`**、**`docs/zh/getting-started.md`**、**`docs/component-guide.md`**、**`README.md`** 与 **`README_EN.md`** — 补充 OpenClaw 频道配置、QMD 独立安装和功能清单入口说明。
- **`scripts/config.env.example`** — 补充可选 `QMD_BIN` / `QMD_BIN_REAL` 环境变量，适配 QMD 不在 `PATH` 的部署。

### 修复 / Fixed
- 移除可能让用户或 agent 误以为“QMD 随 OpenClaw 默认安装”的表述。

## [1.5.0] — 2026-04-27

### 变更 / Changed
- **`prompts/cron/personal-ops-morning-brief.md`** 与 **`prompts/personal-ops-morning-brief.prompt.md`** — 新增 Insight Analysis / 洞察落地模块，在每日简报中使用 HV-lite 横纵分析法，把外部知识信号与 active projects、TODO、阻塞、截止日期和近期对话灵感连接起来。
- **`docs/personal-ops.md`** / **`docs/zh/personal-ops.md`** — 补充 Personal Ops 可运行轻量洞察分析，而不只是任务排序和提醒。

### 修复 / Fixed
- 当当天没有 high-confidence 洞察时，要求简报仍展示候选观察与排除原因，避免静默省略洞察板块导致用户误以为链路未运行。

## [1.4.0] — 2026-04-27

### 变更 / Changed
- **`tools/conversation-mining/`** — 已同步 `FairladyZ625/conversation-mining` 上游最新实现，包括新版导出器、viewer 资产、Codex 会话时间排序修复、transcript 导出辅助逻辑与 CLI 行为。
- **`tools/conversation-mining/pyproject.toml`** — 内嵌工具版本从 `0.1.0` 提升到 `0.2.0`，方便下游 agent 安装器识别新的聊天记录挖掘能力。

### 修复 / Fixed
- 确保用户通过 Obsidian Brain OS 安装或 vendor Conversation Mining 时，拿到的是最新版 Agent 聊天记录导出 / 挖掘脚本，而不是旧的内嵌副本。

## [1.3.0] — 2026-04-26

### 新增 / Added
- **`skills/brain-vault-governance/`** — 新增可复用 vault 治理 skill，供 agent 在写入、移动、分类、巡检 Brain OS vault 持久文件前使用。
- **`docs/governance-sync-boundary.md`** / **`docs/zh/governance-sync-boundary.md`** — 新增中英双语同步边界文档，用于判断私有 Brain OS 部署中的哪些资产适合进入公开仓库。
- **`docs/release-versioning.md`** / **`docs/zh/release-versioning.md`** — 新增中英双语版本号指南，说明 patch / minor / major 判定与 changelog 要求。
- **`docs/governance-cron-guide.md`** / **`docs/zh/governance-cron-guide.md`** — 新增中英双语治理巡检 cron 指南。
- **`prompts/cron/brain-governance-audit.prompt.md`** 与 **`cron-examples/governance.json`** — 新增匿名化治理巡检 prompt 与可导入 OpenClaw cron 示例。

### 变更 / Changed
- **`README.md`**、**`README_EN.md`**、**`docs/getting-started.md`**、**`docs/zh/getting-started.md`**、**`docs/skills-guide.md`**、**`docs/zh/skills-guide.md`**、**`docs/zh/README.md`**、**`INSTALL_FOR_AGENTS.md`** 与 **`cron-examples/README.md`** — 补充 vault 治理能力的入口与安装使用说明。

## [1.2.0] — 2026-04-23

### 新增 / Added
- **`docs/friction-report-template.md`** / **`docs/zh/friction-report-template.md`** — 结构化摩擦报告模板（中英双语）
- **`docs/references/friction-bucket-guide.md`** / **`docs/zh/friction-bucket-guide.md`** — 标准摩擦归桶分类法（中英双语）
- **`docs/references/friction-writeback-matrix.md`** / **`docs/zh/friction-writeback-matrix.md`** — 回写层级决策矩阵（中英双语）
- **`schemas/friction-event.schema.json`** — 单条摩擦信号的 JSON schema
- **`schemas/friction-report.schema.json`** — 聚合摩擦报告的 JSON schema
- **`examples/friction-log.sample.jsonl`** — 5 条示例摩擦信号（JSONL 格式）

### 变更 / Changed
- **`INSTALL_FOR_AGENTS.md`** — Advanced 档位和安装路由已加入 friction-to-governance loop
- **`docs/install-profiles.md`** — Advanced 档位现已包含治理栈 + 摩擦循环
- **`docs/component-guide.md`** — 从 v0.5 更新至 v1.1.0；新增治理栈 + 摩擦循环完整章节

## [1.1.0] — 2026-04-23

### 新增 / Added
- **`docs/zh/friction-to-governance-loop.md`** — 新增 friction-to-governance loop 的中文版文档，让这套治理模式具备中英双语入口。
- **`prompts/friction-to-governance-loop.prompt.md`** — 新增可复用 prompt 模板，用于诊断重复摩擦并把它转化为治理回写。
- **`docs/references/system-governance-guide.md`** — 新增 system governance guide，说明重复问题应回写到系统的哪一层。

### 变更 / Changed
- **`README.md`** — friction-to-governance 入口更新为同时指向中英文文档。

## [1.0.1] — 2026-04-23

### 新增 / Added
- **`docs/friction-to-governance-loop.md`** — 新增治理模式文档，说明如何把重复摩擦信号转化为 prompt、reference、AGENTS、工作流与 onboarding 的持续改进。

### 变更 / Changed
- **`README.md`** — 新增 friction-to-governance loop 的直接入口，让维护者和贡献者能从主文档面更快找到这套治理模式。

## [1.0.0] — 2026-04-21

### 新增 / Added
- **`prompts/cron/qmd-index-refresh-daily.md`** — 新增每日 QMD 索引刷新 cron 模板，用于保持知识库与工作区检索新鲜度。
- **`prompts/cron/knowledge-librarian-3day.md`** — 新增每 3 天一次的知识库整理 cron 模板，覆盖 frontmatter 修复、链接审计、tag 归一化、重复检测与 digest 合并。
- **`prompts/cron/knowledge-governance-10day.md`** — 新增每 10 天一次的知识库治理 cron 模板，覆盖 domain 健康评估、语义漂移检测、过时内容识别、归档建议与 MOC 复核。

### 变更 / Changed
- 开源版知识工作流不再只覆盖知识生产，也开始把保鲜、整理与治理作为可复用的运行模式纳入主线。
- **`docs/getting-started.md`**、**`docs/zh/getting-started.md`** 与 **`INSTALL_FOR_AGENTS.md`** — 补充安装与 onboarding 说明，明确新的治理栈是“最小成功之后的分阶段扩展”，不是默认首装即全开。

## [0.7.0] — 2026-04-20

### 新增 / Added
- **`INSTALL_FOR_AGENTS.md`** — 新增专门面向 AI Agent 的安装指南，提供单一线性 happy path，并默认推荐 Minimal 安装档。
- **`docs/install-profiles.md`** — 新增 Minimal / Standard / Advanced 三档安装分层，让首次上手与完整系统落地可以分阶段推进。
- **`scripts/verify-install.sh`** — 新增安装后验证脚本，统一检查 config、vault 结构、skills 安装、lint 执行与 PII 扫描结果。
- **`.github/workflows/install-smoke.yml`** — 新增 CI 安装冒烟测试，覆盖 `setup.sh --non-interactive --profile minimal` 与后续 `verify-install.sh`。

### 变更 / Changed
- **`setup.sh`** — 新增非交互 CLI 参数、按 profile 控制技能安装、跨平台占位符替换，以及更聚焦 day-one 的下一步指引。
- **`README.md`**、**`README_EN.md`**、**`docs/getting-started.md`**、**`docs/zh/getting-started.md`**、**`docs/component-guide.md`** — 重构安装入口，围绕 agent 安装、安装分层、安装验证与最小成功路径展开。
- **`skills/brain-os-installer/SKILL.md`** — 重新对齐当前文档树，移除暗示仓库尚未支持的安装路径说明。

### 修复 / Fixed
- 修复了“文档在讲安装分层，但 setup 实际仍像一把全装”的 onboarding 漂移问题。
- 移除了 `setup.sh` 中仅适配 macOS 的原地替换行为，提升 Linux 环境和 CI 中的 agent 安装兼容性。

## [0.6.1] — 2026-04-18

### 新增 / Added
- **`prompts/cron/knowledge-soft-link-sync-nightly.md`** — 新增独立 nightly prompt，用于执行 Knowledge ↔ Project 软关联双向同步，让 project 引用修复与主 02:00–04:00 pipeline 解耦。
- **`scripts/sync-knowledge-soft-links.py`** — 新增可复用脚本，用于在 knowledge notes、project briefs 与 projects index 之间同步显式声明的 Knowledge ↔ Project 关系。

### 变更 / Changed
- **`scripts/knowledge-lint.sh`** — 升级为 project-aware 的 lint 脚本：新增 `project_ref` / `related_projects` 校验、project 侧知识路径检查，并同时写出 review report 与 run-report，适合接入 nightly 运维。


## [0.6.0] — 2026-04-17

### 新增 / Added

### 变更 / Changed
- **`scripts/knowledge-lint.sh`** — 升级为 project-aware 的 lint 脚本：新增 `project_ref` / `related_projects` 校验、project 侧知识路径检查，并同时写出 review report 与 run-report，适合接入 nightly 运维。


### 新增 / Added
- **`scripts/check-brain-config-leaks.sh`** — 新增专门的配置泄露扫描脚本，用于在进入 OSS 前拦截作者私有 vault 名、绝对路径、内部称呼和固定 ID。
- **`.github/workflows/brain-config-scan.yml`** — 新增 CI 工作流，在 PR 和 main push 上自动执行配置泄露扫描。
- **`prompts/cron/brain-os-daily-sync.md`** — 新增面向 OSS 的 Brain OS 每日同步 prompt，用于判断本地升级并生成同步计划。
- **`docs/references/knowledge-asset-boundaries.md`** — 新增面向 OSS 的知识资产边界治理文档，明确正式知识产物与原始抓取资产的分层。
- **`docs/references/vault-governance-guide.md`** — 新增面向 OSS 的 vault 治理文档，覆盖目录纪律、计划归位与结构演进规则。

### 变更 / Changed
- **`README.md`**、**`README_EN.md`**、**`docs/getting-started.md`**、**`docs/openclaw-setup.md`**、**`docs/obsidian-setup.md`**、**`setup.sh`** — 明确说明 vault 名字由用户自定义，并统一 `BRAIN_PATH` / `{{BRAIN_ROOT}}` 的对外语义为“用户自己的知识库根路径”。
- **多处 prompts、skills 与辅助脚本** — 将作者私有 vault 名称、绝对路径、内部 agent 名称和固定 ID 替换为可复用占位符或基于环境变量的路径解析。
- **`scripts/scan-today-changes.sh`** — 将 Brain 路径发现方式从写死的 vault 名改为优先读取 `BRAIN_ROOT`，并提供安全 fallback。
- **`scripts/check-pii.sh`** — 调整与新的配置泄露扫描器对齐，避免两套检查规则互相冲突。

### 修复 / Fixed
- 移除了仓库中残留的误导性假设，避免让 OSS 用户以为自己的 vault 必须命名为 `ZeYu-AI-Brain`，或必须匹配维护者本机环境。
- 降低了安装与理解成本，让安装脚本、文档、prompts 与 CI 使用同一套路径和命名模型。

---

## [0.5.3] — 2026-04-14

### 变更 / Changed
- **`README.md`** — 将 GitHub 默认首页切换为中文，保留 Karpathy / LLM Wiki 作为外部参照系而非项目起点，并把项目第一屏定位重写为“数字分身 / 第二大脑 / 24 小时贴身管家 / 有边界的工作分身”；同时恢复 Star History 到默认首页。
- **`README_EN.md`** — 保留原英文 README，作为英文入口页。
- **`README_CN.md`** — 改为兼容跳转页，统一指向新的默认中文 `README.md`。

---

## [0.5.2] — 2026-04-14

### 新增 / Added
- **`docs/nightly-knowledge-flywheel-ops.md`** — Nightly knowledge flywheel 三阶段（02:00 / 03:00 / 04:00）运维手册：成功定义、重跑规则、告警条件，以及为什么 no-op 也是有效结果。

### 变更 / Changed
- **`skills/article-notes-integration/SKILL.md`** — 新增 Raw Asset Storage Rule，明确区分正式知识产物与原始抓取资产，要求截图 / OCR 图包 / PDF / raw 响应统一进入 `LOCAL-LARGE-FILES/knowledge-sources/`，不进入 Brain Git。
- **`prompts/article-notes-integration.prompt.md`** — 同步新增原始资产 guardrails，防止 nightly 02:00 阶段把 `_images-*`、`images/`、`.raw/`、`raw/` 或其他源附件提交进正式知识层。
- **`skills/deep-research/skill.md`** — 社区版本回退为英文版，提升通用可读性。

---

## [0.5.1] — 2026-04-13

### 新增 / Added
- **`docs/component-guide.md`** — 完整组件指南：v0.5 包含的所有内容、每个组件的作用、5 分钟快速上手。中英双语。
- **README.md** + **`README_CN.md`** — 在贡献者文档板块首位添加组件指南链接。

---

## [0.5.0] — 2026-04-13

### 新增 / Added
- **`CHANGELOG_CN.md`** — 中文版变更日志，与英文版一一对应（双语）。
- **`docs/agent-playbooks/release-playbook.md`** — 完整发版 SOP：7 步流程、中英双语 PR 模板、常见陷阱。
- **`docs/agent-playbooks/observer-playbook.md`** — Observer 使用指南：6 步流程、三级安全机制、配置说明。
- **`docs/references/pii-deidentification-guide.md`** — PII 脱敏完整指南：4 类 PII 模式、标准替换表、常见错误修复。
- **`docs/writing-cron-prompts.md`** — Cron Prompt 编写最佳实践：系统日期获取、输出格式约束、跨 prompt 协调。
- **`docs/skill-authoring-guide.md`** — Skill 编写规范：SKILL.md 结构、命名约定、CI 要求。
- **`docs/nightly-pipeline-guide.md`** — Nightly Pipeline 全景指南：4 阶段架构、交接协议、故障处理。

### 变更 / Changed
- **`skills/brain-os-release/SKILL.md`** — Step 3 改为必须同时更新两个 CHANGELOG；Step 5 加入强制中英双语 PR 模板。
- **`.github/workflows/changelog-check.yml`** — CI 检查覆盖 `CHANGELOG_CN.md`；docs/ 变更为可选提醒。
- **`scripts/check-pii.sh`** — 排除 PII 脱敏指南本身（含教学用示例路径）。
- **`README.md`** + **`README_CN.md`** — 新增「贡献者与维护者文档」板块，引用全部新文档。

---

## [0.4.1] — 2026-04-13

### 修复 / Fixed

- **`prompts/cron/chronicle-every-2h-log.md`** — 新增强制系统日期获取步骤，确保 `YYYY-MM-DD` 始终来自系统时钟而非模型猜测，使用运行机器本地时区。
- **`prompts/cron/daily-knowledge-graph-canvas-0500.md`** — 新增步骤 0：在生成每日画布前先获取系统日期/星期/时区；commit message 明确要求使用系统日期。
- **`prompts/cron/knowledge-lint-weekly.md`** — 新增强制目标日期（昨天）获取命令，明确下游 lint/报告路径必须使用系统派生的日期。

---

## [0.4.0] — 2026-04-12

### 新增 / Added

- **`skills/brain-os-release/SKILL.md`** — 发版 SOP skill：版本号规则、PII 检查、CHANGELOG 更新、PR 模板、合并与打 tag 步骤。
- **`scripts/check-pii.sh`** — PII 扫描脚本：检查绝对路径、未解析 `{{占位符}}`、Discord 风格 ID。支持手动运行或 CI 调用。
- **`.github/workflows/pii-scan.yml`** — CI：每次 PR 和 main 推送时执行 `check-pii.sh --strict`，发现 PII 则阻断。
- **`.github/workflows/structure-check.yml`** — CI：验证每个 skill 有 `SKILL.md`、每个脚本有 shebang。
- **`.github/workflows/changelog-check.yml`** — CI：当 `skills/`、`scripts/` 或 `prompts/` 变更但未更新 CHANGELOG 时发出警告（非阻塞）。
- **`skills/observer/SKILL.md`** — Observer skill：每日 AI 团队健康监控。采集 session 数据 + 网关日志，更新 `.learnings/` 账本，生成迭代计划并通知观察者频道。三级安全机制（告警 / 建议 / 经人工确认后执行）。
- **`skills/observer/references/plan-template.md`** — Observer 输出用的迭代计划模板。
- **`prompts/cron/observer-daily-0001.md`** — Observer 每日 00:01 cron prompt 模板（默认禁用）。
- **`README.md`** — 新增 Star History 图表。

### 变更 / Changed

- **`prompts/cron/brain-os-daily-sync.md`**（私有，不在仓库中）— 新增步骤 7：当 A 类同步 >= 3 时自动建议文章方向。

---

## [0.3.0] — 2026-04-12

### 新增 / Added

- **`skills/daily-timesheet/`** — 新 skill：每日扫描 git 提交，对齐 OKR 里程碑，生成结构化工时草稿供人工确认。支持三种写入后端：本地文件、飞书多维表格、钉钉 AI 表格。
- **`skills/daily-timesheet/references/feishu-bitable.md`** — 飞书多维表格 API 参考（字段映射与鉴权流程）。
- **`skills/daily-timesheet/references/dingtalk-bitable.md`** — 钉钉 AI 表格 API 参考。
- **`prompts/cron/daily-timesheet-1730.md`** — 工作日 17:30 cron prompt 模板（默认禁用；配置 `TIMESHEET_REPOS` 和 `BRAIN_ROOT` 后启用）。
- **`scripts/brain-to-reminders.sh`** — 07:30 将 Brain 待办推送到 Apple Reminders。
- **`scripts/reminders-to-brain.sh`** — 21:00 从 Apple Reminders 拉取完成状态回写 Brain。
- **`prompts/cron/brain-to-reminders-0730.md`** — 早晨 Reminders 推送的 cron prompt。
- **`prompts/cron/reminders-to-brain-2100.md`** — 晚上 Reminders 回写的 cron prompt。
- **`skills/english-tutor/`** — 交互式英语听力辅导 skill，使用 Whisper 转录和 edge-tts 语音合成。

### 变更 / Changed

- **`skills/conversation-knowledge-flywheel/SKILL.md`** — 升级为 transcript-first 三层拆分 nightly pipeline 架构，含明确的上下游交接协议。
- **`skills/article-notes-integration/SKILL.md`** — 刷新为英文结构、交叉引用协议和 02:00 阶段契约。
- **`skills/knowledge-flywheel-amplifier/SKILL.md`** — 刷新为跨源综合协议和 04:00 阶段契约。
- **`prompts/cron/conversation-knowledge-mining-nightly.md`** — 对齐拆分 pipeline（预检检查、digest 优先读取、双层输出）。
- **`prompts/conversation-knowledge-mining.prompt.md`** + **`conversation-knowledge-flywheel.prompt.md`** — 对齐措辞与新 skill 契约。

### 修复 / Fixed

- **`scripts/brain-to-reminders.sh`** — `BRAIN_ROOT` 改为必填环境变量；未设置时报错退出（之前会静默使用字面量 `{{BRAIN_ROOT}}` 作为路径）。
- **`scripts/reminders-to-brain.sh`** — 同上修复：`BRAIN_ROOT` 必填，缺失时清晰报错。
- **`scripts/brain-to-reminders.sh`** — 提取正则扩展支持清单/勾选项格式（`- task`、`- [ ] task`），不仅匹配编号列表。

---

## [0.2.0] — 2026-04-08

### 新增 / Added

- `skills/conversation-knowledge-flywheel/` — 夜间对话挖掘与知识综合 skill。
- `skills/article-notes-integration/` — 文章摄取与知识图谱集成 skill。
- `skills/knowledge-flywheel-amplifier/` — 跨源知识放大 skill。
- `prompts/cron/conversation-knowledge-mining-nightly.md` — 夜间对话挖掘 cron prompt。
- `cron-examples/` — 7 个 OpenClaw cron job 配置示例。

---

## [0.1.0] — 2026-03-15

### 新增 / Added

- 初始发布：vault 模板、setup.sh、核心 skills、nightly pipeline prompts、文档。
