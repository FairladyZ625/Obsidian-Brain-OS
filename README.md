# 🧠 Obsidian Brain OS

> 我们长期实践这套系统之后，才发现它和 [Karpathy 提出的 LLM Wiki](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) 在核心思想上高度一致。  
> **但 Brain OS 不止是 LLM Wiki，它是一个数字分身操作系统**：把你的知识、任务、对话、团队上下文和行动建议，持续编译成一个 AI 可运行、可代理、可协作的系统。

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

中文（默认） | [English](README_EN.md)

---

## 先用一句人话讲清楚

很多人第一次看这个项目会困惑：

> 这到底是个知识库？任务系统？Agent 框架？第二大脑？还是数字分身？

答案是：**它全都是，但核心不是“工具合集”，而是“把你长期上下文编译成一个能持续替你工作的系统”。**

如果只用一句话说：

> **Brain OS = LLM Wiki + 第二大脑 + 24 小时贴身管家 + 有边界的数字分身。**

我们会借用 **LLM Wiki** 这个概念来帮助别人快速理解，因为那是一个很好的认知入口：
- AI 不再临时从原始资料里现查现答
- 而是持续维护一个结构化、可检索、可迭代的个人知识世界

但 Brain OS 往前又多走了几步：
- 不只是“维护 wiki”
- 而是让 Agent **理解你的长期上下文**
- 帮你**安排今天要做什么**
- 帮你**总结昨天学到了什么**
- 帮你**隔离个人 / 工作 / 团队边界**
- 甚至在授权范围内，变成一个**能代表你工作的工作分身**

所以如果你把它理解成：
- **一个更强的 LLM Wiki** → 对
- **一个第二大脑系统** → 也对
- **一个数字分身系统** → 也对
- **一个个人与团队上下文操作系统** → 最接近

---

## 我们到底在做什么？

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

## 从“我们自己的长期实践”到数字分身 OS

我们不是先看见 LLM Wiki 才去做这个项目。  
更接近真实的顺序是：

1. 我们先长期把这套系统跑起来
2. 在实践里一步步长出知识库、任务系统、Agent 协作、边界控制、夜间自动化
3. 后来再看到 Karpathy 的 LLM Wiki，发现**核心方向其实是相通的**

也就是说：

> **LLM Wiki 不是 Brain OS 的起点，更像是一个后来出现的、可以帮助外界快速理解我们的参照系。**

所以 Brain OS 不是“从 LLM Wiki 派生出来的项目”，而是一个在长期实践里自然长出来、后来发现与 LLM Wiki 高度同构的系统。

而在这个基础上，我们又继续把它做成了一个**可运行的数字分身系统**：

| 层级 | LLM Wiki | Brain OS |
|---|---|---|
| 知识层 | 持续维护 wiki | 持续维护知识库 + 索引 + digest |
| 行动层 | 基本没有 | 每日驾驶舱 / 提醒 / 工时 / 待办推进 |
| 协作层 | 基本没有 | 多 Agent 分工、Writer / Chronicle / Observer |
| 边界层 | 不强调 | 个人 / 工作 / 团队上下文隔离 |
| 代理层 | 偏被动问答 | 在边界内替你工作、替你响应、替你协调 |

所以我们借用 LLM Wiki 这个词，不是为了“蹭概念”，而是因为：

**它能帮助别人快速理解我们已经做出来的那一部分。**  
但 Brain OS 的实际落点，不再只是一个 wiki，而是一个**数字分身操作系统**。

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

## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=FairladyZ625/Obsidian-Brain-OS&type=Date)](https://star-history.com/#FairladyZ625/Obsidian-Brain-OS&Date)

---

## 许可证

MIT © [FairladyZ](https://github.com/FairladyZ625)
