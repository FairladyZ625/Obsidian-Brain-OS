# Brain OS Agent 团队配置指南

> 这是 Brain OS 最核心的文档之一。**装完系统后，第一件事就是配好你的 Agent 团队。**

---

## 为什么需要多个 Agent？

Brain OS 不是单打独斗的系统。它像一个团队：

- **主 Agent（大总管）**：负责日常对话、分诊、排序、推进、写知识库
- **Writer Agent**：唯一写入者，保证知识库写入一致性
- **Chronicle Agent（史官）**：默默记录频道历史，不参与讨论
- **Review/巡检 Agent**：定期审计知识库质量

每个 Agent 有明确的职责边界，互不越权。

---

## 必备 Agent 清单

### 1. 主 Agent（大总管 / Main Orchestrator）

**角色**：你的个人 AI 总管，一切事务的入口和协调者。

**核心职责**：
- 接收你的口述交办 → 进入 INBOX → 分诊排序 → 推进闭环
- 生成每日驾驶舱（morning brief）、周计划、月度里程碑
- 执行 Nightly Pipeline 的各阶段（文章整合 / 对话挖掘 / 知识放大）
- 管理待办提醒（15:00 + 20:00）
- 协调其他 Agent 的工作

**行为准则**：
- 先给结论，再给进度；少空话，多可执行动作
- 可以整理、重排、降级事项，但**不能私自删除事项**
- 只有用户明确说"已完成/可归档"时，才允许移出主面
- 高风险操作（删除/外发/改权限）必须先确认

**模型要求：⚠️ 必须是多模态模型**

为什么？因为你的知识来源不只有文字：
- 小红书 / 微信公众号文章 → 图片+文字混合
- PDF 截图、网页截图
- Obsidian 里的图片笔记

如果主 Agent 不支持多模态（只能读纯文本），它就无法处理这些来源。**这是硬性要求，不是建议。**

推荐模型（按优先级）：
- GPT-5.3 Codex / GPT-5.4（OpenAI）
- multimodal models with vision（Anthropic）
- Chinese-optimized multimodal models，中文场景优秀）

**不推荐**：纯文本模型（如某些轻量 embedding-only 模型）作为主 Agent。

**Cron 任务**（由主 Agent 执行）：
| 任务 | 时间 | 说明 |
|------|------|------|
| morning-brief | 每天 07:00 | 今日驾驶舱 |
| weekly-plan | 每周一 05:10 | 本周排期 |
| monthly-milestones | 每月1号 06:20 | 月度里程碑 |
| todo-reminder | 15:00 + 20:00 | 待办跟进 |

---

### 2. Writer Agent（知识库写入者）

**角色**：Brain 知识库的唯一正式写入者。

**为什么需要独立 Writer？**
- 避免多 Agent 并发写入导致冲突
- 保证写入格式一致、符合治理规范
- 所有知识库改动有单一审计入口

**核心职责**：
- 接收主 Agent 的写入请求（知识笔记、文章处理结果、daily digest 等）
- 按 Brain OS 的目录规范写入正确位置
- 执行 git commit，确保 Obsidian 可见
- 冲突仲裁：如果两个请求要写同一个文件，Writer 决定怎么合并

**模型要求**：中低即可（your-light-model (e.g., Haiku, GLM-4.7-flash) 级别），主要是机械写入+格式化。

**Cron 任务**：无（按需被调用，不需要定时触发）。

---

### 3. Chronicle Agent（史官）

**角色**：频道历史的沉默记录者。只记录，不评论，不干预。

**详细文档**：→ [Chronicle 史官系统](chronicle-agent.md)

**核心职责**：
- 每 2 小时扫描一次 Discord 频道消息
- 提取有实质内容的事件、决策、承诺、讨论
- 写入 `01-PERSONAL-OPS/05-OPS-LOGS/channel-history/`
- 作为个人事务系统的"历史证据层"

**行为准则**：
- **不在频道发言**——安静完成记录
- 过滤掉闲聊、表情包、无意义插话
- 只记录：决策、任务分配、技术讨论、重要结论、承诺变更

**模型要求**：低成本模型即可（your-light-model / Haiku）。这是结构化记录工作，不需要深度推理。

**Cron 任务**：
| 任务 | 时间 | 说明 |
|------|------|------|
| channel-history | 每 2 小时 | 频道历史记录 |

---

### 4. Review / 巡检 Agent

**角色**：知识库质量守门员。

**核心职责**：
- 定期巡检知识库：脏文件、格式违规、孤儿笔记、断链
- 运行 knowledge-lint.sh 脚本
- 自动补提交未提交的改动（commit patrol，每 30 分钟）
- 产出巡检报告，标记需要人工介入的问题

**模型要求**：低成本模型（your-light-model）。巡检是规则检查，不是创意工作。

**Cron 任务**：
| 任务 | 时间 | 说明 |
|------|------|------|
| knowledgebase-commit-patrol | 每 30 分钟 | 自动提交知识库改动 |
| knowledge-lint-weekly | 每周一次 | 知识库质量审计 |

---

## Agent 配置方式

### 方式 A：OpenClaw（推荐，功能最全）

如果你用 OpenClaw，Agent 就是"session/gateway"配置下的不同身份：

```bash
# 在 openclaw.json 中配置多个 agent
# 每个 agent 有独立的 model、system prompt、skill set
openclaw agent add main --model "gpt-5.3-codex"
openclaw agent add writer --model "glm-4.7"
openclaw agent add chronicle --model "minimax-M2.7-highspeed"
openclaw agent add review --model "minimax-M2.7-highspeed"
```

然后导入 cron 配置：
```bash
openclaw cron import cron-examples/personal-ops.json
openclaw cron import cron-examples/nightly-pipeline.json
```

详见 → [OpenClaw 配置指南](openclaw-setup.md)

### 方式 B：其他 AI 平台（Claude / GPT / Cursor 等）

如果你不用 OpenClaw，原理一样，只是实现不同：

1. **主 Agent**：你日常对话的那个 AI（Claude Code / ChatGPT / Cursor Agent）
   - 把 `skills/` 目录下的 SKILL.md 内容注入到 system prompt 或 rules 文件
   - 重点注入：`personal-ops-driver`、`article-notes-integration`
2. **Writer Agent**：可以是一个独立的 AI 实例，或者就由主 Agent 兼任（简单场景下）
3. **Chronicle Agent**：用一个便宜的定时任务触发（cron job + API 调用）
4. **定时任务**：用系统 crontab + API 调用来替代 OpenClaw cron

**关键差异**：不用 OpenClaw 时，你需要自己搭建定时任务机制（crontab / GitHub Actions / Zapier 等）。

---

## 频道设计（Discord / Slack / 其他）

如果你的 AI 团队在群聊平台协作，频道设计至关重要：

### 推荐频道结构

```
你的 Server
├── #主频道          ← 日常对话，所有 Agent 都能看到
├── #个人事务管理     ← 主 Agent 专属，待办/驾驶舱/提醒
├── #知识库           ← Writer Agent 工作区，知识写入确认
├── #巡检告警         ← Review Agent 输出巡检结果
└── #general         ← 闲聊/测试，不影响主流程
```

### 核心原则

1. **@才响应**：Agent 只在被 @ 时回复，避免刷屏
2. **频道隔离**：个人事务不和闲聊混在一起（上下文污染）
3. **主 Agent 是协调者**：跨 Agent 协调通过主 Agent 中转，不直接互聊

详细设计 → [频道设计指南](guide/02-channel-design.md)

---

## Skills 全览

### 核心 Skills（必装）

这些 Skill 定义了 Agent 的能力边界和工作流：

| Skill | 谁用 | 做什么 |
|-------|------|--------|
| **brain-os-installer** | 安装向导 | 苏格拉底式引导新用户安装 |
| **personal-ops-driver** | 主 Agent | 个人事务驾驶系统：分诊、排序、推进、提醒 |
| **article-notes-integration** | 主 Agent / Nightly | 文章处理流水线：读文章→提取→归入领域知识 |
| **conversation-knowledge-flywheel** | 主 Agent / Nightly | 对话挖掘：从 AI 对话中提取知识和洞察 |
| **knowledge-flywheel-amplifier** | 主 Agent / Nightly | 跨源合成：合并文章+对话结果→模式提炼 |
| **notebooklm** | 主 Agent | NotebookLM 深度研究集成：建 notebook、上传 source、跑 research |
| **deep-research** | 主 Agent | 多来源深度研究：自动搜索+综合+产出报告 |

### 推荐 Skills（按需安装）

这些是通用能力增强，不限于 Brain OS：

| Skill | 做什么 | 场景 |
|-------|--------|------|
| **agent-reach** | 跨平台内容抓取（13+ 平台） | 读小红书/微信公众号/Twitter 等 |
| **arrange** | 信息整理与结构化 | 整理杂乱信息 |
| **brainstorming** | 头脑风暴 | 需要创意时 |
| **clarify** | 需求澄清 | 用户需求模糊时 |
| **critique** | 审查评审 | 审查文档/代码/方案 |
| **distill** | 精炼压缩 | 长文变短文 |
| **extract** | 信息提取 | 从长文中提取关键信息 |
| **humanizer** | 人性化润色 | 让 AI 文本更像人写的 |
| **normalize** | 格式统一 | 统一不同来源的格式 |
| **optimize** | 性能优化 | 优化任何东西 |
| **planning-with-files** | 文件驱动规划 | 基于文件做计划 |
| **polish** | 语言润色 | 改善表达 |
| **skillshare** | Skill 分享 | 管理 skill 库 |
| **teach-impeccable** | 教学 | 教 AI 教用户 |
| **writing-plans** | 写作规划 | 规划写作任务 |
| **writing-skills** | 写作技巧 | 写作方法论 |

**特别注意：`agent-reach` 强烈推荐安装**

因为它是主 Agent 读取外部图文内容的桥梁。没有它，主 Agent 无法访问小红书、微信公众号等平台的内容。而主 Agent 又必须是多模态模型才能理解 agent-reach 抓回来的图文混合内容。**这两者是配套的。**

---

## 最小可用配置（MVP）

如果你不想一开始就配全套，最低限度需要：

**✅ 必须有：**
1. **一个多模态主 Agent** + `personal-ops-driver` skill
2. **一套 vault 结构**（`setup.sh` 一键生成）
3. **一个 todo-backlog.md**（主 Agent 的待办真相源）

**有了这三样，你已经可以：**
- 让 AI 帮你管理每日待办
- 生成每日驾驶舱
- 做知识捕获和整理

**🟡 进阶（建议尽快加上）：**
4. Writer Agent（知识库写入一致性）
5. Chronicle Agent（频道历史记录）
6. Review Agent（自动提交巡检）
7. Nightly Pipeline（睡觉时自动处理知识）

**🔵 完整（长期目标）：**
8. 全部核心 skills + 推荐 skills
9. QMD 语义搜索
10. Agora 多 Agent 治理框架（→ [Agora](https://github.com/FairladyZ625/Agora)）

---

## 快速配置 Checklist

装完 `setup.sh` 后，按这个顺序配置：

- [ ] **Step 1**: 确认主 Agent 是多模态模型
- [ ] **Step 2**: 安装核心 skills 到主 Agent 的 skills 目录
- [ ] **Step 3**: 配置 Writer Agent（可以是独立实例或主 Agent 兼任）
- [ ] **Step 4**: 导入 personal-ops cron（morning-brief + reminders）
- [ ] **Step 5**: 配置 Chronicle Agent + cron
- [ ] **Step 6**: 配置 Review Agent + commit-patrol cron
- [ ] **Step 7**: （可选）导入 nightly-pipeline cron
- [ ] **Step 8**: 安装推荐 skills（至少装 `agent-reach`）
- [ ] **Step 9**: 设计频道结构（如果用 Discord/Slack）
- [ ] **Step 10**: 跑一遍 morning-brief 测试
- [ ] **Step 11**: 读 `docs/zh/guide/03-daily-workflow.md` 了解日常使用

---

## 相关文档

- [Agent 详细配置指南](guide/01-agent-setup.md)
- [频道设计指南](guide/02-channel-design.md)
- [Chronicle 史官系统](chronicle-agent.md)
- [Personal Ops 系统](personal-ops.md)
- [Nightly Pipeline](nightly-pipeline.md)
- [Skills 使用指南](skills-guide.md)
- [QMD 语义搜索](qmd-setup.md)
- [OpenClaw 配置](openclaw-setup.md)
