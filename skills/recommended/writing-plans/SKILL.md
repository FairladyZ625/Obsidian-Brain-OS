---
name: writing-plans
description: >
  实现计划编写技能。当你有规格说明或多步骤任务需求、准备动手写代码之前使用。Use when: writing implementation plans, spec to tasks, breaking down features, task planning, TDD workflow, multi-step implementation. 拥有规格说明或多步骤任务需求，在碰代码之前使用。
---

# Writing Plans

## 概述

编写全面的实现计划，假设工程师对你的代码库零上下文且品味存疑。记录他们需要知道的一切：每个任务要碰哪些文件、代码、可能需要查阅的文档、如何测试。将完整计划以小粒度任务呈现。DRY。YAGNI。TDD。频繁 commit。

假设他们是有技能的开发者，但几乎不了解我们的工具集或问题域。假设他们不太擅长测试设计。

**开始时宣布：** "我正在使用 writing-plans 技能创建实现计划。"

**上下文：** 应在专用 worktree 中运行（由 brainstorming 技能创建）。

**保存计划到：** `docs/plans/YYYY-MM-DD-<功能名>.md`

## 任务粒度

**每个步骤是一个动作（2-5 分钟）：**
- "写失败的测试" — 一个步骤
- "运行确认它失败" — 一个步骤
- "写最小实现让测试通过" — 一个步骤
- "运行测试确认通过" — 一个步骤
- "Commit" — 一个步骤

## 计划文档头部

**每个计划必须以此头部开始：**

```markdown
# [功能名] 实现计划

> **For Claude：** 必需子技能：使用 superpowers:executing-plans 逐步实现此计划。

**目标：** [一句话描述要构建什么]

**架构：** [2-3 句话说明方法]

**技术栈：** [关键技术/库]

---
```

## 任务结构

````markdown
### 任务 N：[组件名]

**文件：**
- 创建：`exact/path/to/file.py`
- 修改：`exact/path/to/existing.py:123-145`
- 测试：`tests/exact/path/to/test.py`

**步骤 1：写失败的测试**

```python
def test_specific_behavior():
    result = function(input)
    assert result == expected
```

**步骤 2：运行测试确认失败**

运行：`pytest tests/path/test.py::test_name -v`
预期：FAIL，提示 "function not defined"

**步骤 3：写最小实现**

```python
def function(input):
    return expected
```

**步骤 4：运行测试确认通过**

运行：`pytest tests/path/test.py::test_name -v`
预期：PASS

**步骤 5：Commit**

```bash
git add tests/path/test.py src/path/file.py
git commit -m "feat: add specific feature"
```
````

## 注意事项
- 始终使用精确文件路径
- 计划中包含完整代码（不是"添加验证"）
- 包含精确命令和预期输出
- 用 @ 语法引用相关技能
- DRY、YAGNI、TDD、频繁 commit

## 执行交接

保存计划后，提供执行选择：

**"计划已完成并保存到 `docs/plans/<文件名>.md`。两种执行方式：**

**1. 子代理驱动（当前会话）** — 我为每个任务派发新子代理，任务间 review，快速迭代

**2. 并行会话（独立）** — 在 worktree 中打开新会话，使用 executing-plans 批量执行带检查点

**选哪种？****

**若选择子代理驱动：**
- **必需子技能：** 使用 superpowers:subagent-driven-development
- 留在当前会话
- 每个任务新子代理 + 代码 review

**若选择并行会话：**
- 引导他们在 worktree 中打开新会话
- **必需子技能：** 新会话使用 superpowers:executing-plans
