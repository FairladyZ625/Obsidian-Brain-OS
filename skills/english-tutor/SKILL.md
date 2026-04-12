---
name: english-tutor
description: Interactive English listening tutor using audio transcription (faster-whisper) and text-to-speech (edge-tts). Use when user sends English audio for learning, wants to practice listening comprehension, do dictation exercises, or study from podcasts/audiobooks/BBC content. Triggers on phrases like "学英语", "练听力", "听这段", "英语学习", "next segment", "下一段", or when user sends audio files asking for transcription/practice.
---

# English Tutor — 交互式英语听力教练

## 核心流程

```
用户发音频 → whisper 转写 → 分段播放(edge-tts) → 用户复述 → 批改反馈 → 下一段
```

## 第一步：接收音频并转写

当用户发送音频文件（mp3/m4a/wav 等）：

1. 从 inbound media 路径获取音频文件
2. 运行转写脚本：

```bash
python3 ~/.agents/skills/english-tutor/scripts/transcribe.py <audio_path> [--lang en] [--model tiny]
```

- 默认语言：`en`（英文）
- 默认模型：`tiny`（快，适合长音频）；可选 `small`/`medium`（更准）
- 输出：JSON 格式转写结果 + 纯文本

3. 向用户展示**内容概要**（话题、主持人、核心信息），**不要一次性全文展示**

## 第二步：分段播放（Listen & Repeat）

1. 将转写文本按**语义段落**切分（每段 3-5 句话，约 15-30 秒）
2. 用 edge-tts 生成每段语音并发送给用户：

```bash
python3 ~/.agents/skills/english-tutor/scripts/speak.py "<text>" --voice en-US-GuyNeural --rate -10% --output /tmp/english_tutor_segment.mp3
```

3. 通过 `message` tool 发送音频到当前频道
4. 提示用户听完复述

### 语音选择参考

见 `references/voices.md` — 按场景选声音：
- **男声美式**：`en-US-GuyNeural`（默认，自然亲切）
- **女声美式**：`en-US-JennyNeural`
- **男声英式**：`en-GB-RyanNeural`
- **女声英式**：`en-GB-SoniaNeural`

语速建议：
- 学习用 `-10%` 或 `-5%`（稍慢）
- 正常语速 `+0%`
- 快速挑战 `+10%`

## 第三步：批改与反馈

用户复述后，对照原文做**三档评价**：

| 档位 | 标准 | 示例反馈 |
|------|------|----------|
| ✅ 核心信息全对 | 主要事实、数字、人名正确 | "完全正确！补充：xxx" |
| ⚠️ 大意对但缺细节 | 抓住了主旨但漏了关键细节 | "方向对！还提到了：xxx" |
| ❌ 偏离较大 | 遗漏主要信息或理解错误 | "再听一遍？关键点是：xxx" |

反馈原则：
- **先肯定**，再补充或纠正
- 标注**关键词汇/短语**（每段挑 1-2 个值得学的表达）
- 不纠结语法小错，专注**听力理解**

## 第四步：推进与循环

- 用户说"下一段"/"继续"/"next" → 播放下一段
- 用户说"重复"/"再来一遍" → 重播当前段
- 用户说"跳过" → 跳到下一段
- 全部完成后，生成**本课词汇总结**（所有出现的关键短语汇总）

## 高级功能

### 词汇模式
用户说"词汇总结"或"vocabulary"时，输出本课所有重点词汇表：
- 英文短语 | 中文释义 | 原文例句

### 速度递进
建议从 `-10%` 开始，用户适应后逐步提升到 `+0%` 甚至 `+10%`。

### 自定义材料
用户可以发任何英文音频（播客、新闻、演讲、视频截图），不限于 BBC。

## 注意事项

- faster-whisper 和 edge-tts 必须已安装：`pip install faster-whisper edge-tts`
- 首次运行 whisper 会自动下载模型（tiny 约 75MB）
- 音频文件通过 Discord inbound media 接收，路径格式：`{{OPENCLAW_MEDIA_DIR}}/inbound/<uuid>.<ext>`
- 生成的临时语音文件存 `/tmp/` 或 workspace `temp_` 前缀，用完可清理
