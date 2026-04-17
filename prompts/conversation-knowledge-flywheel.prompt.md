Read and follow the `conversation-knowledge-flywheel` skill.

> Superseded as a monolithic nightly wrapper by the split pipeline:
> - `article-notes-integration.prompt.md` (02:00)
> - `conversation-knowledge-mining.prompt.md` (03:00)
> - `knowledge-flywheel-amplifier.prompt.md` (04:00)
> Keep this file only as a legacy reference / ad-hoc manual wrapper.


Target date: yesterday in Asia/Shanghai unless explicitly provided.

Required workflow:
1. Read raw transcripts from `{{TRANSCRIPT_DIR}}`
2. Build a manifest of that day's transcripts
3. Group transcripts by project
4. When a project can be identified, resolve and read the corresponding Brain-side project brief from `05-PROJECTS/<slug>/project-brief.md` before final synthesis
5. Use QMD as the preferred high-recall layer (collection/update/embed/query) when runtime is healthy
6. Run a Surveillance-style fast scan over the recalled candidates
7. Do final personalized synthesis and produce:
   - 1-3 conversation-derived knowledge note drafts
   - 1 daily-learning-suggestions block
   - 0-2 optional research seeds
8. Only if a theme is clearly high-value and needs external reinforcement, prepare a NotebookLM context pack and constrained research seed before using NotebookLM deep research
9. Route Brain writes through the approved writer path
10. Report whether the result is actually Obsidian-visible (commit + hook), not just drafted

Constraints:
- Do not copy raw transcript dumps into {{BRAIN_NAME}}
- Do not force output when there is no real signal
- `05-PROJECTS/` is the default Brain-side project routing layer; use it for reading context anchors, not as the execution source of truth
- Do not auto-run heavy NotebookLM DeepResearch in Phase 1 without first preparing internal context pack + constrained research seed
- If QMD is broken locally, say so explicitly and fall back to non-QMD degraded mode
- NotebookLM is for externally amplified research grounded by internal context, not for replacing {{MAIN_AGENT_NAME}} judgment
- Keep cron thin; the logic belongs in the skill
