# QMD Semantic Search Setup

> Configure QMD (vector/hybrid search) for your Brain OS vault.
> **Chinese version**: [docs/zh/qmd-setup.md](docs/zh/qmd-setup.md)

---

## What is QMD?

QMD is OpenClaw's built-in local vector/hybrid search engine. It enables semantic search across your knowledge base using natural language queries.

### When Do You Need QMD?

| Vault Size | Need QMD? |
|-----------|-----------|
| < 200 notes | ❌ Manual search is enough |
| 200-500 notes | 🟡 Optional, helps noticeably |
| > 500 notes | ✅ Recommended |
| Running Nightly Pipeline | ✅ Recommended (primary recall layer) |

**If you only use Brain OS for knowledge org + personal ops (no Pipeline), you can skip QMD.**

---

## Quick Config

Add to your OpenClaw config (`~/.openclaw/openclaw.json`):

```json
{
  "qmd": {
    "provider": "openai",
    "model": "text-embedding-3-small",
    "mode": "hybrid",
    "sources": [
      {
        "path": "{{BRAIN_PATH}}/03-KNOWLEDGE",
        "watch": true,
        "embedInterval": "6h"
      }
    ]
  }
}
```

| Field | Recommended |
|-------|-------------|
| `provider` | `openai` or `local` |
| `model` | `text-embedding-3-small` (OpenAI) or `qwen3-embedding-4b` (local) |
| `mode` | `hybrid` (best) / `vector` / `bm25` |

---

## Local Models (no API key needed)

```json
{
  "qmd": {
    "provider": "local",
    "model": "qwen3-embedding-4b",
    "mode": "hybrid"
  }
}
```

Requires Ollama or compatible local inference.

---

## Usage in Brain OS

1. **Nightly Pipeline**: `conversation-knowledge-flywheel` uses QMD as primary recall
2. **Daily search**: `openclaw qmd query "your natural language query"`

---

## Degraded Mode

If QMD is unavailable, the pipeline falls back to `grep`/`ripgrep`. Lower recall but still functional. **QMD is optional enhancement.**

---

## Troubleshooting

| Issue | Fix |
|-------|-----|
| `QMD unhealthy` | `openclaw qmd rebuild` |
| Poor results | Switch to `qwen3-embedding-4b` (better for Chinese) |
| `native module mismatch` | Reinstall OpenClaw or `openclaw repair` |

---

## Related

- [OpenClaw Setup](openclaw-setup.md)
- [Nightly Pipeline](nightly-pipeline.md)
- [Knowledge Architecture](knowledge-architecture.md)
