---
name: skillshare
version: v0.17.5
description: 从单一源管理并同步 50+ 工具的 AI CLI skills。支持全局（~/.config/skillshare/）和项目（.skillshare/）模式，用于安装、更新、卸载、同步、审计、检查、差异、搜索、排除规则、符号链接目标、复制与同步模式、备份恢复、CI/CD 审计以及 hub 构建与分享。Manages and syncs AI CLI skills across 50+ tools from a single source.
argument-hint: "[command] [target] [--json] [--dry-run] [-p|-g]"
---

# Skillshare CLI

全局模式：`~/.config/skillshare/skills/` → 所有 AI CLI。项目模式：`.skillshare/skills/` → 仓库本地。
当 `.skillshare/config.yaml` 存在时自动检测项目模式。用 `-p` 或 `-g` 强制指定。

## 常用配方

### 快速开始
```bash
skillshare init --no-copy --all-targets --git --skill  # 全新全局设置
skillshare init -p --targets "Codex,cursor"            # 全新项目设置
skillshare init --copy-from Codex --all-targets --git  # 从现有 CLI 导入
skillshare init --discover --select "windsurf"          # 稍后添加新 AI 工具
```
### 安装 Skills
```bash
skillshare install user/repo -s pdf,commit       # 选择特定 skills
skillshare install user/repo --all               # 安装所有
skillshare install user/repo --into frontend     # 放入子目录
skillshare install gitlab.com/team/repo          # 任何 Git 托管
skillshare install user/repo --track             # 启用后续更新
skillshare install user/repo -s pdf -p           # 安装到项目
skillshare install                               # 从配置重新安装所有追踪的远程
skillshare sync                                  # 安装后总是同步
```
### 额外内容（规则、命令、提示词）
```bash
skillshare extras init rules --target ~/.Codex/rules --target ~/.cursor/rules
skillshare extras init commands --target ~/.Codex/commands --mode copy
skillshare extras init                               # 交互式 TUI 向导
skillshare extras list                               # 显示每个目标的状态
skillshare extras list --json                        # JSON 输出
skillshare extras collect rules                      # 将本地文件拉取到源
skillshare extras remove rules                       # 从配置移除（源保留）
skillshare extras rules --mode copy                  # 更改目标同步模式
skillshare sync extras                               # 同步所有额外内容到目标
skillshare sync extras --dry-run --force             # 预览 / 覆盖冲突
skillshare sync --all                                # 同时同步 skills + 额外内容
```
详见 [extras.md](references/extras.md)。

### 创建和发现 Skills
```bash
skillshare new my-skill                          # 使用交互式模式选择创建
skillshare new my-skill -P reviewer              # 直接使用 reviewer 模式
skillshare search "react testing"                # 在 GitHub 搜索 skills
skillshare collect                               # 将目标本地更改拉回源
```
### 移除 Skills
```bash
skillshare uninstall my-skill                    # 移除一个（移至回收站）
skillshare uninstall skill-a skill-b             # 移除多个
skillshare uninstall -G frontend                 # 移除整个组
skillshare sync                                  # 移除后总是同步
```
### 团队 / 组织
```bash
# 创建者：初始化项目（见快速开始）→ 添加 skills → 提交 .skillshare/
skillshare install -p && skillshare sync                  # 成员：克隆 → 安装 → 同步
skillshare install github.com/team/repo --track -p        # 追踪共享仓库
skillshare push                                           # 跨机器：在 A 上推送
skillshare pull                                           # 跨机器：在 B 上拉取
```
### Skill Hub
```bash
skillshare hub add https://example.com/hub.json          # 保存 hub 源
skillshare hub add https://example.com/hub.json --label my-hub  # 带自定义标签
skillshare hub list                                      # 列出已保存的 hub
skillshare hub default my-hub                            # 设置默认 hub
skillshare hub remove my-hub                             # 移除 hub
skillshare hub index --source ~/.config/skillshare/skills/ --full --audit  # 构建 hub 索引
```
### 控制 Skills 的去向
```bash
# SKILL.md frontmatter: targets: [Codex]        → 只同步到 Codex
skillshare target Codex --add-include "team-*"   # glob 过滤器
skillshare target Codex --add-exclude "_legacy*"  # 排除模式
skillshare target codex --mode copy && skillshare sync --force  # 复制模式
# .skillignore — 从发现中隐藏 skills/目录（gitignore 语法）
#   根级：<source>/.skillignore（影响所有命令）
#   仓库级：<source>/_repo/.skillignore（限于该仓库）
#   .skillignore.local — 本地覆盖（不提交），否定覆盖基础
```
详见 [targets.md](references/targets.md)。

### 更新与维护
```bash
skillshare check                              # 查看有什么需要更新
skillshare update my-skill && skillshare sync  # 更新一个
skillshare update --all && skillshare sync     # 更新所有
skillshare update --all --diff                 # 显示更改了什么
```
### 脚本化与 CI/CD
```bash
skillshare status --json                       # 完整状态为 JSON
skillshare check --json                        # 更新状态为 JSON
skillshare sync --json                         # 同步结果为 JSON
skillshare diff --json                         # 差异结果为 JSON
skillshare install user/repo --json            # 安装结果为 JSON（隐含 --force --all）
skillshare update --all --json                 # 更新结果为 JSON
skillshare uninstall my-skill --json           # 卸载结果为 JSON（隐含 --force）
skillshare collect Codex --json               # 收集结果为 JSON（隐含 --force）
skillshare target list --json                  # 目标列表为 JSON
skillshare list --json                         # Skills 列表为 JSON
skillshare search react --json                 # 搜索结果为 JSON
skillshare audit --format json                 # 审计结果为 JSON
skillshare doctor --json                       # 健康检查为 JSON（出错时退出 1）
```
### 恢复与故障排除
```bash
skillshare trash restore <name> && skillshare sync  # 撤销删除
skillshare sync                                     # Skill 缺失？重新同步
skillshare doctor && skillshare status              # 诊断问题
skillshare install user/repo --force                 # 覆盖审计阻止
skillshare install user/repo --skip-audit            # 完全绕过扫描
```
详见 [TROUBLESHOOTING.md](references/TROUBLESHOOTING.md)。

## 快速查询
| 命令 | 项目模式？ | `--json`？ |
|----------|:--------:|:---------:|
| `status`, `diff`, `list`, `doctor` | ✓（自动） | ✓ |
| `sync`, `collect` | ✓（自动） | ✓ |
| `install`, `uninstall`, `update`, `check`, `search`, `new` | ✓（`-p`） | ✓（new 除外） |
| `target`, `audit`, `trash`, `log`, `hub` | ✓（`-p`） | ✓（target list, audit, log） |
| `extras init/list/remove/collect/mode` | ✓（`-p`） | ✓（list, mode） |
| `push`, `pull`, `backup`, `restore` | ✗ | ✗ |
| `tui`, `upgrade` | ✗ | ✗ |
| `ui` | ✓（`-p`） | ✗ |

## AI 调用者规则
1. **非交互式** — AI 无法回答提示。使用 `--force`、`--all`、`-s`、`--targets`、`--no-copy`、`--all-targets`、`--yes`。
2. **变更后同步** — `install`、`uninstall`、`update`、`collect`、`target` 都需要 `sync`。
3. **审计** — `install` 自动扫描；CRITICAL 阻止。用 `--force` 覆盖，`--skip-audit` 绕过。检测硬编码密钥（API 密钥、token、私钥）。
4. **安全卸载** — 移至回收站（7 天）。`trash restore <name>` 撤销。**永远不要** `rm -rf` 符号链接。
5. **输出** — `--json` 用于结构化数据（12 个命令支持，见快速查询）。`--no-tui` 用于 TUI 命令的纯文本（`list`、`log`、`audit`、`diff`、`trash list`、`backup list`、`target list`）。`tui off` 全局禁用 TUI。`--dry-run` 预览。

## 参考
| 主题 | 文件 |
|-------|------|
| Init 参数 | [init.md](references/init.md) |
| 同步/收集/推送/拉取 | [sync.md](references/sync.md) |
| 安装/更新/卸载/新建 | [install.md](references/install.md) |
| 状态/差异/列表/搜索/检查 | [status.md](references/status.md) |
| 安全审计 | [audit.md](references/audit.md) |
| 回收站 | [trash.md](references/trash.md) |
| 操作日志 | [log.md](references/log.md) |
| 目标 | [targets.md](references/targets.md) |
| 额外内容（规则/命令/提示词） | [extras.md](references/extras.md) |
| 备份/恢复 | [backup.md](references/backup.md) |
| 故障排除 | [TROUBLESHOOTING.md](references/TROUBLESHOOTING.md) |
