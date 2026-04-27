#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';

function arg(name) { const i = process.argv.indexOf(name); return i >= 0 ? process.argv[i + 1] : null; }
const summaryPath = arg('--summary');
const statePath = arg('--state');
const outPath = arg('--out');
if (!summaryPath || !outPath) {
  console.error('Usage: generate-install-report.mjs --summary summary.json --out INSTALL_REPORT.md [--state install-state.json]');
  process.exit(2);
}
const summary = JSON.parse(fs.readFileSync(summaryPath, 'utf8'));
const state = statePath && fs.existsSync(statePath) ? JSON.parse(fs.readFileSync(statePath, 'utf8')) : null;
const changes = state?.changes || [];
const byAction = changes.reduce((acc, c) => { acc[c.action] = (acc[c.action] || 0) + 1; return acc; }, {});
function list(items) { return items?.length ? items.map((x) => `- ${x}`).join('\n') : '- none'; }
function table(obj) { return Object.entries(obj || {}).map(([k,v]) => `| ${k} | \`${v}\` |`).join('\n'); }
const report = `# OpenClaw Brain OS Pack Install Report

## Summary

| Field | Value |
|---|---|
| Pack | \`${summary.packName || state?.pack}\` |
| Pack version | \`${summary.packVersion || state?.packVersion}\` |
| Mode | \`${state ? 'applied' : summary.mode}\` |
| Profile | \`${summary.profile}\` |
| Install ID | \`${state?.installId || 'dry-run-preview'}\` |

## Paths

| Path | Value |
|---|---|
${table(summary.paths || state?.paths)}

## Selected assets

### Agents
${list(summary.selectedAgents)}

### Skills
${list(summary.selectedSkills)}

### Cron groups
${list(summary.selectedCronJobs)}

## Changes

${state ? Object.entries(byAction).map(([k,v]) => `- ${k}: ${v}`).join('\n') : '- Dry-run only. No user files were modified.'}

## Backups

${state?.backupDir ? `Backups were written to:\n\n\`${state.backupDir}\`` : 'No backups were created because this was a dry-run preview.'}

## Next steps

1. Review generated OpenClaw config and cron jobs.
2. Restart OpenClaw Gateway after confirming config changes.
3. Keep cron jobs disabled until channels, prompts, and models are verified.
4. If QMD is installed, record its path in the workspace \`TOOLS.md\`.
5. If anything looks wrong, run rollback before making more changes.

## Rollback

${state ? `\`OPENCLAW_ROOT=${state.paths.openclawRoot} bash rollback.sh ${path.dirname(statePath)}\`` : 'Rollback is only available after apply.'}
`;
fs.writeFileSync(outPath, report);
console.log(outPath);
