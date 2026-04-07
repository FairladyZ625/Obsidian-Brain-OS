# conversation-mining

把本地的 Claude Code、Codex、Antigravity 对话导出成 Markdown，并生成一个静态 HTML 查看器。

这个项目适合做本地回溯和取证：

- 全量或增量导出历史对话
- 在一个页面里统一浏览
- 深链定位某条会话
- 复制 `Conversation reference / prompt` 交给别的 AI 接手
- 当 Antigravity 留下本地产物时，直接查看对应 `task.md / implementation_plan.md / walkthrough.md`

它现在同时支持两种形态：

- 独立脚本 / 本地工具
- 可安装 skill，入口见 [SKILL.md](./SKILL.md)

## 复制给你的 AI

```text
请从 https://github.com/FairladyZ625/conversation-mining 安装并学习 `conversation-mining`。阅读仓库里的 README.md、SKILL.md 和 AI_INSTALL.md，按仓库说明在本地安装；如果支持的话，同时把它装成 skill 和 CLI。安装后用 `conversation-mining --no-open --days 1` 验证。
```

## 当前支持

- Claude Code
  - 读取 `{{CLAUDE_HOME}}/projects/*/*.jsonl`
  - 重建主会话和子代理关系
- Codex
  - 读取 `{{CODEX_HOME}}/sessions`、`history.jsonl`、`state_5.sqlite`
- Antigravity
  - 读取 `{{ANTIGRAVITY_PATH}}/.../state.vscdb`
  - 提取 trajectory summaries
  - 尝试把 AG 会话关联到 `{{ANTIGRAVITY_BRAIN_PATH}}/<uuid>/` 里的本地产物

## 现状说明

这是一个面向本地使用的实用工具，不是官方 SDK。

- Claude / Codex 一般能拿到比较完整的 transcript
- Antigravity 目前更像“任务摘要提取”，不是完整连续聊天还原
- AG 产物关联只在本地 brain workspace id 能稳定匹配时生效

## 快速开始

```bash
git clone git@github.com:FairladyZ625/conversation-mining.git
cd conversation-mining
python3 convs.py
```

默认会：

1. 导出最近的对话
2. 把 JSON 和 viewer 产物写到 `./exported_conversations`
3. 把给人读的 Markdown transcript 写到独立 transcript 目录
4. 生成 `./exported_conversations/index.html`
5. 在 macOS 上自动打开查看器

## 作为 CLI 安装

可编辑安装：

```bash
python3 -m pip install -e .
conversation-mining --no-open
```

按模块运行：

```bash
python3 -m conversation_mining --days 7
```

用 `pipx`：

```bash
pipx install .
conversation-mining --date 2026-03-19
```

## 作为 Skill 使用

仓库里已经包含 [SKILL.md](./SKILL.md)。

如果你的 agent 支持从 git 仓库安装 skill，那么装好以后就可以直接把它当 `conversation-mining` 来用，适合：

- 按日期或会话 id 定位原始对话
- 增量导出最近历史
- 打开本地 viewer
- 生成可交接给其他 AI 的 reference / prompt

## 常用命令

只导出今天并构建查看器：

```bash
python3 convs.py --no-open
```

回扫最近 7 天：

```bash
python3 convs.py --days 7
```

导出某一天：

```bash
python3 convs.py --date 2026-03-19
```

写到自定义目录：

```bash
python3 convs.py --output-dir ~/tmp/conversation-mining-output
```

把 Markdown transcript 写到指定目录：

```bash
python3 convs.py --markdown-dir {{TRANSCRIPT_DIR}}
```

高级用法：只导出 JSON / Markdown，不构建 viewer：

```bash
python3 export_all.py --days 7 --output-dir ./exported_conversations
```

## 产物结构

```text
exported_conversations/
  conversations.json
  index.html
```

独立的人类可读 transcript：

```text
{{TRANSCRIPT_DIR}}/
  2026-03-19/
    claude_*.md
    codex_*.md
    ag_*.md
```

## Viewer 功能

- 来源筛选：Claude / Codex / AG
- 支持按标题、消息、工作区、标签、AG 产物信息搜索
- 白天 / 夜间模式
- 阅读模式：
  - 主线
  - 主线 + 子代理
  - 全量
- 速览卡片：
  - Final answer
  - Key files
  - Commands
  - Signals
- 时间线回放
- 收藏、标签、分类
- 按工作区分组
- Related task threads
- AG `Artifacts` 卡片，可直接打开本地文件

## 已知限制

- AG 不保证本地一定有完整聊天记录
- AG 产物关联目前只是部分覆盖
- viewer 主要面向本地文件使用
- 收藏 / 标签 / 分类目前存储在浏览器 `localStorage`

## 隐私提醒

这个工具会读取本地应用状态和本地会话历史。

在发布导出结果前，请先检查：

- 对话内容里可能包含密钥或敏感信息
- transcript Markdown 里可能带有绝对路径
- AG artifact 路径会暴露你的本地工作区结构

## License

MIT
