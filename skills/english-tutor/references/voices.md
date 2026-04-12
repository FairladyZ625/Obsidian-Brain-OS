# English Tutor — Voice Reference Guide

## 推荐声音（按场景）

### 🇺🇸 美式英语

| 声音 ID | 性别 | 特点 | 推荐场景 |
|----------|------|------|----------|
| `en-US-GuyNeural` | 男 | 自然、亲切、年轻 | **默认选择**，日常对话、播客 |
| `en-US-EricNeural` | 男 | 成熟、稳重 | 新闻、正式内容 |
| `en-US-AndrewNeural` | 男 | 温和、清晰 | 慢速教学 |
| `en-US-BrianNeural` | 男 | 活泼、有活力 | 轻松话题 |
| `en-US-JennyNeural` | 女 | 自然、友好 | 女声偏好时首选 |
| `en-US-AriaNeural` | 女 | 专业、流畅 | 商务/学术 |
| `en-US-EmmaNeural` | 女 | 温暖、柔和 | 故事/情感类 |
| `en-US-MichelleNeural` | 女 | 活泼、有表现力 | 生动内容 |

### 🇬🇧 英式英语

| 声音 ID | 性别 | 特点 | 推荐场景 |
|----------|------|------|----------|
| `en-GB-RyanNeural` | 男 | 标准 RP 口音 | **英式首选**，BBC 风格 |
| `en-GB-WilliamNeural` | 男 | 成熟、权威 | 正式英式内容 |
| `en-GB-OliverNeural` | 男 | 年轻、现代 | 现代英式口语 |
| `en-GB-SoniaNeural` | 女 | 标准 RP 口音 | 女声英式首选 |
| `en-GB-LibbyNeural` | 女 | 温和、友好 | 日常英式 |
| `en-GB-MaisieNeural` | 女 | 年轻、活泼 | 轻松英式 |

### 🌏 其他口音（可选）

| 声音 ID | 口音 | 场景 |
|----------|------|------|
| `en-AU-WilliamNeural` | 澳式 | 澳洲英语练习 |
| `en-IN-PrabhatNeural` | 印式 | 印度英语了解 |

## 语速建议

| 语速 | rate 参数 | 适用场景 |
|------|-----------|----------|
| 慢速 | `-15%` ~ `-10%` | 初学者、长难句、新闻 |
| 正常偏慢 | `-5%` | 日常学习（推荐起点） |
| 正常 | `+0%` | 已适应后提升 |
| 快速 | `+10%` | 挑战模式、真实语速 |

## 使用示例

```bash
# 美式男声，慢速
python3 speak.py "Hello, this is BBC Learning English." --voice en-US-GuyNeural --rate -10%

# 英式女声，正常速度
python3 speak.py "The weather is lovely today." --voice en-GB-SoniaNeural --rate +0%

# 快速挑战
python3 speak.py "I grind pepper on to everything." --voice en-US-BrianNeural --rate +10%
```
