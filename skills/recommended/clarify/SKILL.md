---
name: clarify
description: 改进不清晰的 UX 文案、错误消息、微文案、标签和说明。让界面更容易理解和使用。Improve unclear UX copy, error messages, microcopy, labels, and instructions.
user-invokable: true
argument-hint: [TARGET=<value>]
---

识别并改进不清晰、令人困惑或写得不好的界面文本，让产品更容易理解和使用。

## 强制准备

使用 frontend-design skill——其中包含设计原则、反模式，以及**上下文收集协议**。在继续之前遵循该协议——如果没有现成的设计上下文，必须先运行 teach-impeccable。另外收集：用户技术水平和使用上下文中的心理状态。

---

## 评估当前文案

识别是什么让文本不清晰或无效：

1. **找出清晰度问题**：
   - **术语**：用户听不懂的技术术语
   - **歧义**：多种可能的解释
   - **被动语态**："Your file has been uploaded" vs "We uploaded your file"
   - **长度**：太啰嗦或太简洁
   - **假设**：假设用户没有的知识
   - **缺失上下文**：用户不知道该做什么或为什么
   - **语气不匹配**：太正式、太随意或不适合场景

2. **理解上下文**：
   - 受众是谁？（技术型？普通用户？新手？）
   - 用户的心理状态是什么？（错误时压力大？成功时自信？）
   - 要做什么？（我们希望用户做什么？）
   - 有什么限制？（字符限制？空间限制？）

**关键**：清晰的文案帮助用户成功。不清晰的文案造成挫折、错误和服务单。

## 规划文案改进

创建更清晰沟通的策略：

- **主要信息**：用户需要知道的**唯一**一件事是什么？
- **需要的行动**：用户接下来应该做什么（如果有的话）？
- **语气**：这应该感觉如何？（有帮助？道歉？鼓励？）
- **限制**：长度限制、品牌语气、本地化考虑

**重要**：好的 UX 文案是无形的。用户应该立即理解，不会注意到文字。

## 系统性改进文案

在以下常见领域精炼文本：

### 错误消息
**差**："Error 403: Forbidden"
**好**："You don't have permission to view this page. Contact your admin for access."

**差**："Invalid input"
**好**："Email addresses need an @ symbol. Try: name@example.com"

**原则**：
- 用通俗语言解释哪里出错了
- 建议如何修复
- 不要归咎于用户
- 适当包含示例
- 如有需要链接到帮助/支持

### 表单标签与说明
**差**："DOB (MM/DD/YYYY)"
**好**："Date of birth"（用占位符显示格式）

**差**："Enter value here"
**好**："Your email address" 或 "Company name"

**原则**：
- 使用清晰、具体的标签（不是通用占位符）
- 用示例显示格式期望
- 解释为什么问（不明显时）
- 在字段前而非后放说明
- 保持必填字段标识清晰

### 按钮与 CTA 文本
**差**："Click here" | "Submit" | "OK"
**好**："Create account" | "Save changes" | "Got it, thanks"

**原则**：
- 具体描述动作
- 使用主动语态（动词 + 名词）
- 匹配用户的心智模型
- 要具体（"Save" 比 "OK" 好）

### 帮助文本与工具提示
**差**："This is the username field"
**好**："Choose a username. You can change this later in Settings."

**原则**：
- 增加值（不要只是重复标签）
- 回答隐含问题（"这是什么？"或"为什么需要这个？"）
- 简短但完整
- 如有需要链接到详细文档

### 空状态
**差**："No items"
**好**："No projects yet. Create your first project to get started."

**原则**：
- 解释为什么是空的（不明显时）
- 清晰展示下一步操作
- 让它感觉友好，不是死胡同

### 成功消息
**差**："Success"
**好**："Settings saved! Your changes will take effect immediately."

**原则**：
- 确认发生了什么
- 解释接下来会发生什么（如相关）
- 要简短但完整
- 匹配用户的情感时刻（重大胜利要庆祝）

### 加载状态
**差**："Loading..."（30+ 秒）
**好**："Analyzing your data... this usually takes 30-60 seconds"

**原则**：
- 设定期望（多久？）
- 解释正在发生什么（不明显时）
- 尽可能显示进度
- 如适当提供退出方式（"Cancel"）

### 确认对话框
**差**："Are you sure?"
**好**："Delete 'Project Alpha'? This can't be undone."

**原则**：
- 声明具体动作
- 解释后果（尤其是破坏性动作）
- 使用清晰的按钮标签（"Delete project" 不是 "Yes"）
- 不要过度使用确认（只对有风险的动作）

### 导航与寻路
**差**：像 "Items" | "Things" | "Stuff" 这样的通用标签
**好**：像 "Your projects" | "Team members" | "Settings" 这样具体的标签

**原则**：
- 要具体和有描述性
- 使用用户能理解的语言（不是内部术语）
- 使层级清晰
- 考虑信息气味（面包屑、当前位置）

## 应用清晰度原则

每段文案都应遵循以下规则：

1. **要具体**："Enter email" 不是 "Enter value"
2. **要简洁**：删除不必要的词（但不要牺牲清晰度）
3. **要主动**："Save changes" 不是 "Changes will be saved"
4. **要人性化**："Oops, something went wrong" 不是 "System error encountered"
5. **要有帮助**：告诉用户做什么，不只是发生了什么
6. **要一致**：整个产品使用相同术语（不要为多样化而多样化）

**禁止**：
- 不解释就用术语
- 归咎于用户（"You made an error" → "This field is required"）
- 模糊（"Something went wrong" 没有解释）
- 不必要地使用被动语态
- 写过于冗长的解释（要简洁）
- 对错误使用幽默（要同理心）
- 假设技术知识
- 变换术语（选择一个并坚持）
- 重复信息（标题重述引言、冗余解释）
- 用占位符作为唯一标签（用户输入时它们就消失了）

## 验证改进

测试文案改进是否有效：

- **可理解性**：用户没有上下文能理解吗？
- **可操作性**：用户知道下一步做什么吗？
- **简洁性**：在保持清晰的同时尽可能短了吗？
- **一致性**：与别处的术语匹配吗？
- **语气**：适合场景吗？

记住：你是一个清晰度专家，拥有出色的沟通能力。写得就像在向一个不熟悉产品的聪明朋友解释。要清晰，要有帮助，要人性化。
