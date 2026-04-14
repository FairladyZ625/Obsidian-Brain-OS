# 变更日志 / Changelog（中文版）

> 完整英文版见 [CHANGELOG.md](CHANGELOG.md)。本文件为中文对照版，内容与英文版一一对应。

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
