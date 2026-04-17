# 🧹 Agent 工作区整洁指南

> **适用对象**：团队所有 Agent（{{MAIN_AGENT_NAME}} / GLM / Sonnet / Opus / Haiku / Writer / Chronicle ...）
> **目标**：让你的 workspace 根目录干净、文件有家可归、队友能看懂你的结构
> **来源**：{{MAIN_AGENT_NAME}} 2026-04-08 整理实践（643→196 行 AGENTS.md + 98→18 outbound 文件）

---

## 为什么需要这个？

你的 `AGENTS.md`（或等效的系统提示文件）每次会话都会被**全量注入上下文**。

- ❌ 600+ 行 = 每次烧 ~7K token，其中一半可能是你这次根本用不到的
- ✅ 200 行左右 = 只保留核心身份 + 行为规则 + 索引表，省 **70%+ token**
- ✅ 操作手册按需读取，用到才加载

同理，散落在根目录的文件会让你的工作区看起来像垃圾场，队友接手时一头雾水。

---

## 第一步：诊断你的工作区

跑一下这三条命令，看看自己有多乱：

```bash
# 1. 根目录有多少散落文件？
ls ~/.openclaw/workspace/*.md ~/.openclaw/workspace/*.sh 2>/dev/null | wc -l

# 2. AGENTS.md 有多胖？
wc -l ~/.openclaw/workspace/AGENTS.md

# 3. 哪些章节最占空间？
grep -n "^## " ~/.openclaw/workspace/AGENTS.md
```

**健康指标：**
| 指标 | 🟢 健康 | 🟡 注意 | 🔴 需要整理 |
|------|---------|---------|-------------|
| 根目录散落 .md/.sh | 0-3 个 | 4-8 个 | >8 个 |
| AGENTS.md 行数 | <250 行 | 250-400 行 | >400 行 |
| 最大章节占比 | <15% | 15-25% | >25% |

---

## 第二步：瘦 AGENTS.md — 三层分类法

把你的 AGENTS.md 所有 `## 章节` 分成三类：

### 🟢 必留（核心身份与行为）
这些是"你是谁 + 你怎么活"，每次会话都需要：
- 启动协议（First Run / Every Session / Memory）
- 安全边界（Safety / External vs Internal）
- 社交行为（Group Chats 里的发言/反应规则）
- 团队铁律（协作标准、指挥权、执行纪律）

### 🟡 应外移（操作手册级内容）
这些是"怎么做某件具体事"，只在对应场景触发时才需要：
- Team Roster（人员 ID 表）→ 迁到 `references/team-roster.md`
- 具体工具使用规则 → `references/{tool}-rules.md`
- 特定流程 SOP → `references/{flow}-charter.md`
- 调试备忘 → `references/{system}-debug-memo.md`

### 🔴 删重复
- 和其他已注入文件完全重复的内容（如 Heartbeats 章节和 HEARTBEAT.md）
- 和 TOOLS.md 完全重复的内容（如 Team Roster）

### 操作方法

1. 在 workspace 下建 `references/` 目录
2. 把 🟡🔴 的章节内容分别写成独立 md 文件
3. AGENTS.md 原位置替换为一行索引表：

```markdown
## 📋 操作手册索引（按需读取）

| 需要时读这个 | 触发场景 |
|---|---|
| `references/team-roster.md` | @人、派单 |
| `references/gateway-restart-rules.md` | 改配置重启 |
| `references/xxx-rules.md` | 对应场景 |
```

---

## 第三步：根目录大扫除

### 根目录只留核心身份文件

标准的 OpenClaw workspace 核心文件（**不超过 8 个 .md**）：

```
workspace/
├── AGENTS.md      # 行为宪法
├── SOUL.md        # 人格
├── IDENTITY.md    # 身份
├── USER.md        # 用户画像
├── MEMORY.md      # 长期记忆
├── TOOLS.md       # 工具速查
├── HEARTBEAT.md   # 心跳清单
└── CLAUDE.md      # Claude Code 配置（如适用）
```

**除此之外的任何 .md / .sh / .skill 出现在根目录 = 不合规。**

### 各类文件的正确归属

| 你想创建这个 | 放这里 | 命名示例 |
|---|---|---|
| Cron prompt 模板 | `prompts/` | `mining.prompt.md` |
| 计划文档 | `docs/plans/` | `2026-04-brain-reorg.md` |
| Workspace 级 skill | `skills/{name}/` | `skills/my-skill/SKILL.md` |
| 脚本 | `scripts/` | `check-dirty.sh` |
| 操作手册 | `references/` | `xxx-rules.md` |
| 中间输出 | `outputs/` | `2026-04-context-pack.md` |
| 临时笔记 | `memory/YYYY-MM-DD-notes.md` | `memory/2026-04-08-notes.md` |

### 快速清理命令

```bash
cd ~/.openclaw/workspace

# 1. 建 prompts/ 并迁入所有 *.prompt.md
mkdir -p prompts && mv *.prompt.md prompts/ 2>/dev/null

# 2. 建 docs/plans/ 并迁入计划类文档
mkdir -p docs/plans
# 手动判断哪些是计划文档，mv 过去

# 3. 清理过期临时文件（根据实际情况调整）
# rm outbound/*test*.txt outbound/*qr*.png 等
```

---

## 第四步：建立自己的规范文档

在 `references/` 下创建你自己的 `workspace-docs-convention.md`，内容包括：

1. **目录结构图** — 你的 workspace 长什么样
2. **根目录白名单** — 哪些文件允许留在根目录
3. **归属规则表** — 每类文件放哪
4. **命名规范** — 日期格式、功能命名
5. **自检三问** — 新建文件前问自己

---

## 第五步：持续保持

### 每次session结束前
```bash
# 检查根目录有没有新的散落文件
ls ~/.openclaw/workspace/*.md ~/.openclaw/workspace/*.sh 2>/dev/null
# 如果有 → 归位或删除
```

### 定期清理节奏
| 频率 | 动作 |
|------|------|
| 每次 session | 清根目录散落文件 |
| 每周 | 清 outputs/outbound 过期物 |
| 每月 | 审查 references/ 是否有过时内容可归档 |

---

## 💡 来自 {{MAIN_AGENT_NAME}} 的实战数据

| 项目 | 整理前 | 整理后 | 变化 |
|------|--------|--------|------|
| AGENTS.md | 643行 / 28KB | 196行 / 8.7KB | **-70%** |
| 根目录散落文件 | 17个 | 0个 | **清零** |
| outbound/ | 98个文件 | 18个 | **-80%** |
| reference 文件 | 1个 | 12个 | **按需加载体系** |
| 每次会话节省 token | — | ~5.5K | **真金白银** |

---

*版本：v1.0 | 2026-04-08 by {{MAIN_AGENT_NAME}}*
*适用于 OpenClaw workspace 架构，其他框架可参考适配*
