# 🧠 Obsidian Brain OS

> 不是一个普通笔记库，也不只是“第二大脑”。  
> **它是你的数字分身操作系统**：帮你管理上下文、沉淀知识、驱动任务、协作团队，并在边界内代表你工作。

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

中文（默认） | [English](README_EN.md)

---

## 我们到底在做什么？

如果只用一句话说：

> **Brain OS = 你的第二大脑 + 24 小时贴身管家 + 可控边界内的数字分身。**

它不是单纯帮你“记笔记”，而是让 AI 真正理解你的**个人上下文**：
- 你最近在推进什么
- 你昨天学到了什么
- 你有哪些待办快到期了
- 你团队里每个人在做什么
- 哪些信息可以对外说，哪些只能内部知道

当这套系统真正跑起来之后，它可以做到：
- 早上起来，先把你今天最该做的事排好
- 昨天学到的东西自动总结出来
- 把零散对话、文章、会议、任务沉淀成长期知识
- 帮你区分**个人信息**、**工作信息**、**团队协作信息**
- 让你的“工作分身”只暴露该暴露的上下文，不泄露你的私人内容
- 在团队协作里，别人问你们组在做什么、某个项目现在是什么状态，可以先问你的 Agent，而不一定每次都来找你本人

这不是“装上就会”的软件。  
它更像是一套**要慢慢养出来的数字分身系统**。你每天投入，它每天变懂你，最后形成复利。

---

## 你可以把它理解成什么？

### 1. 第二大脑
它帮你把：
- 文章
- 想法
- 项目
- 对话
- 每日行动

从零散信息变成结构化知识。

### 2. 数字分身
它知道你的工作方式、团队结构、习惯、边界和优先级。  
在设定好的权限范围内，它可以替你回答问题、整理信息、做初步决策建议。

### 3. 24 小时贴身管家
你睡觉时，它跑夜间流水线；你醒来时，它给你摘要、提醒、工时、待办、建议。

### 4. 团队协作代理系统
你不止有一个 Agent。你可以有：
- **主 Agent**：最懂你、负责总调度
- **工作 Agent**：只暴露工作相关知识，服务同事 / 跨部门协作
- **Observer**：每天观察整个系统哪里出问题、给出改进建议
- **Writer / Chronicle / Review**：负责写入、记录、巡检

也就是说，Brain OS 不是一个 bot，而是一套**多 Agent 的个人与团队上下文操作系统**。

---

## 为什么很多人装了还不太会用？

因为 Brain OS 不是“下载即满血”的现成产品，而是：

- 一套 **模板**
- 一套 **方法论**
- 一套 **Agent 协作框架**
- 一套 **你要按自己情况慢慢配置出来的系统**

仓库里给的是：
- 目录结构模板
- 安装脚本
- skills
- cron prompts
- CI / PII / release SOP
- 完整文档

但你仍然要自己理解：
- 哪些任务该交给哪个 Agent
- 哪些上下文可以共享，哪些必须隔离
- 哪些 cron 要开，哪些不该开
- 你的工作流里真正需要哪一层能力

**模板全给了，但系统要靠你自己养。**
这也是为什么真正跑起来之后，它的提升会非常大——因为它会越来越像你，而不是一个通用聊天机器人。

---

## Brain OS 的核心能力

- 🤖 **多 Agent 团队**：主调度 + 写入者 + 史官 + 巡检官 + 可继续扩展的角色体系
- 🔭 **Observer（自我进化观察者）**：每天检查系统运行状态、找重复错误、提出改进建议，维护系统的“运行记忆”
- ⏰ **夜间自动化**：文章整合 → 对话知识挖掘 → 知识放大 → 摘要输出
- 📋 **个人事务系统**：每日驾驶舱、待办管理、到期提醒、承诺跟踪
- 🍎 **提醒事项集成**：Brain 与 Apple Reminders 双向同步
- 📋 **自动工时整理**：扫描提交、对齐项目、辅助填工时
- 🔬 **深度研究能力**：NotebookLM / deep-research 结合
- 🔒 **边界与治理**：控制谁能看到什么上下文，避免个人信息泄露
- 🚀 **一键安装**：`bash setup.sh`

---

## 一个真实的使用场景

比如你有一个专门的“工作龙虾 / 工作 Agent”：

- 它知道你们组最近在做哪些产品
- 它知道每个项目当前进度
- 它知道团队成员分工和一些沟通习惯
- 但它**只能回答工作相关内容**
- 它不能访问你的私人日记、私人想法、私人任务

于是其他同事、其他部门的人，有问题时可以**先问你的工作 Agent**。  
它回答不了，或者涉及敏感边界，再来找你本人。

这就是 **“数字分身有边界”** 的价值：
不是把你所有信息全丢给 AI，而是在**清晰权限边界**下，把可以被代理的部分交给系统。

---

## 快速开始

```bash
git clone https://github.com/FairladyZ625/Obsidian-Brain-OS.git
cd Obsidian-Brain-OS
bash setup.sh
```

`setup.sh` 会交互式完成：
- vault 路径
- 用户信息
- skills 安装
- Observer `.learnings/` 初始化
- cron 配置生成
- PII 扫描验证
- 安装检查

无痕测试：

```bash
bash setup.sh --test
```

---

## 给你的 AI Agent 的一句话安装指令

你可以直接把下面这段话发给你的 AI Agent：

```text
你好，我想安装 Obsidian Brain OS。请把它当成一个“数字分身 + 第二大脑 + 多 Agent 协作系统”来帮我配置。请你：
1. 克隆仓库
2. 阅读 skills/brain-os-installer/SKILL.md
3. 问我 vault 放哪、我叫什么、时区是什么、我想先开哪些能力
4. 运行 setup.sh 或手动一步步帮我配置
5. 配完后再带我理解 docs/component-guide.md、docs/agents.md、Observer 和 nightly pipeline 是怎么跑的
6. 最后帮我确认：我不是只“装上了”，而是真的知道怎么用
```

---

## 新用户最该先读什么？

### 先读这 4 篇

1. **[组件全览指南](docs/component-guide.md)** ⭐ 先看全貌
2. **[快速开始](docs/getting-started.md)** ⭐ 安装与首次运行
3. **[Agent 团队配置](docs/agents.md)** ⭐ 真正把系统跑起来的关键
4. **[Observer 使用手册](docs/agent-playbooks/observer-playbook.md)** ⭐ 理解系统如何自我进化

### 如果你想理解“怎么长期养出来”

- [Nightly Pipeline 全景指南](docs/nightly-pipeline-guide.md)
- [发版操作手册](docs/agent-playbooks/release-playbook.md)
- [PII 脱敏指南](docs/references/pii-deidentification-guide.md)
- [Cron Prompt 编写指南](docs/writing-cron-prompts.md)
- [Skill 编写指南](docs/skill-authoring-guide.md)

---

## 仓库里有什么？

| 模块 | 作用 |
|------|------|
| `vault-template/` | Brain 的基础目录结构模板 |
| `setup.sh` | 安装和初始化脚本 |
| `skills/` | Agent 的能力包 |
| `prompts/` | Nightly / cron / pipeline 的模板 |
| `scripts/` | 自动化脚本 |
| `docs/` | 文档与 playbooks |
| `cron-examples/` | OpenClaw cron 配置示例 |
| `CHANGELOG.md` / `CHANGELOG_CN.md` | 英文 / 中文变更日志 |

---

## 设计理念

> **上下文是基础设施。知识是复利。分身是边界内的代理。**

1. **Capture / 捕获** → 所有东西先进入系统
2. **Process / 处理** → 夜间流水线把原始输入变成结构化知识
3. **Compound / 复利** → 越跑越懂你，越跑越有价值
4. **Delegate / 代理** → 在可控边界内，让 Agent 替你工作
5. **Guard / 守边界** → 个人、工作、团队信息明确分层，防止泄露

---

## 这套系统适合谁？

适合：
- 想把 AI 从“聊天工具”升级成“长期系统”的人
- 想让 Agent 真正理解自己上下文的人
- 想做个人知识库 + 任务系统 + 团队协作代理的人
- 愿意长期投入、持续迭代、接受它需要“养”的人

不适合：
- 想装完立刻 100% 自动化的人
- 不愿意配置、不了解自己的工作流、也不想理解系统结构的人
- 只想要一个简单笔记软件的人

---

## 相关项目

- **[Agora](https://github.com/FairladyZ625/Agora)** — 多 Agent 治理框架。Brain OS 提供知识与上下文层，Agora 提供协作与治理层。

---

## 许可证

MIT © [FairladyZ](https://github.com/FairladyZ625)
