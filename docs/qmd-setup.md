# QMD Semantic Search Setup

> Configure QMD (vector/hybrid search) for your Brain OS vault.
> **Chinese version**: [docs/zh/qmd-setup.md](zh/qmd-setup.md)

---

## What is QMD?

QMD (Query-Memory-Docs) is a separately installed local retrieval engine for vector / hybrid search. It enables semantic search across your knowledge base using natural language queries.

**Important boundary:** QMD is not bundled with OpenClaw. Brain OS can use QMD as the recommended semantic retrieval backend for OpenClaw agents when QMD is installed and available, but users still need to install and configure QMD separately.

QMD can provide:

- **Semantic search**: find content by meaning, not only exact keywords
- **Hybrid retrieval**: vector search + BM25 keyword search
- **Reranking**: better ordering of candidate results
- **Local-first indexing**: keep vault and transcript indexes on your machine

In the Brain OS Nightly Pipeline, QMD is the preferred recall layer for conversation mining when available.

---

## When Do You Need QMD?

| Vault Size / Use Case | Need QMD? |
|---|---|
| < 200 notes | ❌ Manual search is usually enough |
| 200-500 notes | 🟡 Optional, helps noticeably |
| > 500 notes | ✅ Recommended |
| Running conversation mining / nightly pipeline | ✅ Recommended as primary recall layer |
| Knowledge org + personal ops only | ❌ Optional; you can skip it |

If QMD is unavailable, Brain OS prompts should enter degraded mode and fall back to `grep` / `ripgrep`. Recall is weaker, but the pipeline remains functional.

---

## Install QMD Separately

Install QMD using the package or repository instructions for your environment. After installation, verify that a QMD CLI is available:

```bash
qmd status
# or, if installed under a custom path:
/path/to/qmd status
```

Then make it available to Brain OS scripts in one of two ways:

```bash
# Option A: put qmd on PATH
export PATH="/path/to/qmd/bin:$PATH"

# Option B: point Brain OS scripts at the binary
export QMD_BIN="/path/to/qmd"
export QMD_BIN_REAL="/path/to/qmd"
```

Do not assume `openclaw qmd ...` exists in every OpenClaw installation. Use the installed QMD binary unless your own OpenClaw distribution explicitly provides a QMD wrapper.

---

## Recommended Brain OS Sources

After QMD is installed, index the parts of your system that need semantic recall:

| Source | Why |
|---|---|
| `{{BRAIN_ROOT}}/03-KNOWLEDGE` | formal knowledge notes |
| `{{BRAIN_ROOT}}/05-PROJECTS` | project briefs and plans |
| `{{TRANSCRIPT_DIR}}` | exported conversation transcripts |
| `{{WORKSPACE_ROOT}}` | optional workspace docs / prompts |

Example commands vary by QMD distribution, but the pattern is usually:

```bash
qmd update
qmd embed
qmd query "agent architecture decisions"
```

For Brain OS scripts, prefer using `QMD_BIN` so users can choose their installed binary path.

---

## Usage in Brain OS

QMD is used in two main places:

1. **Nightly Pipeline**: `conversation-knowledge-flywheel` can use QMD as high-recall candidate retrieval.
2. **Daily search**: agents can use QMD to search large vaults and workspaces before answering.

When writing agent instructions, use conditional language:

- ✅ “Use QMD when available.”
- ✅ “If QMD is missing or unhealthy, report degraded mode and fall back to keyword search.”
- ❌ “OpenClaw includes QMD by default.”

---

## OpenClaw Config Boundary

OpenClaw routes agents, channels, models, and cron delivery. QMD is a separate retrieval engine.

For OpenClaw configuration examples, see:

- [OpenClaw Config Guide](openclaw-config-guide.md)
- `examples/openclaw/openclaw.example.json`
- `examples/openclaw/openclaw.multi-channel.example.json`

For cron jobs, configure `QMD_BIN` / `QMD_BIN_REAL` in the environment that runs OpenClaw if your Brain OS scripts need a non-default QMD path.

---

## Troubleshooting

| Issue | Fix |
|---|---|
| `qmd: command not found` | Install QMD separately, add it to `PATH`, or set `QMD_BIN` |
| `QMD unhealthy` | Rebuild or repair the QMD index using your QMD CLI |
| Poor results | Use a multilingual / Chinese-capable embedding model if your vault is Chinese-heavy |
| Native module mismatch | Reinstall or rebuild QMD for the active Node/runtime version |
| Pipeline says degraded mode | Check transcript paths, QMD binary path, and QMD index health |

---

## Related

- [OpenClaw Config Guide](openclaw-config-guide.md)
- [OpenClaw Setup](openclaw-setup.md)
- [Nightly Pipeline](nightly-pipeline.md)
- [Knowledge Architecture](knowledge-architecture.md)
