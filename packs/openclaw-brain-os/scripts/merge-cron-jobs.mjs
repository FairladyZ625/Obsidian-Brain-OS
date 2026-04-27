#!/usr/bin/env node
import { readJson, writeJson, stable, diffObjects } from './merge-utils.mjs';
function arg(name) { const i = process.argv.indexOf(name); return i >= 0 ? process.argv[i + 1] : null; }
const existingPath = arg('--existing');
const patchPath = arg('--patch');
const outPath = arg('--out');
const force = process.argv.includes('--force');
if (!patchPath || !outPath) {
  console.error('Usage: merge-cron-jobs.mjs --patch jobs.patch.json --out jobs.json [--existing jobs.json] [--force]');
  process.exit(2);
}
const existing = readJson(existingPath, { jobs: [] }) || { jobs: [] };
const patch = readJson(patchPath, { jobs: [] }) || { jobs: [] };
const result = Array.isArray(existing) ? { jobs: existing } : existing;
result.jobs = result.jobs || [];
const byId = new Map(result.jobs.map((j) => [j.id, j]));
const blockers = [];
const changes = [];
for (const job of patch.jobs || []) {
  const safeJob = { ...job, enabled: false };
  const current = byId.get(safeJob.id);
  if (!current) {
    result.jobs.push(safeJob);
    changes.push({ action: 'add-cron-job', id: safeJob.id, enabled: false });
  } else if (diffObjects(current, safeJob)) {
    blockers.push({ type: 'cron-job', id: safeJob.id, reason: 'same cron id exists with different config' });
    if (force) Object.assign(current, safeJob, { enabled: false });
  }
}
if (blockers.length && !force) {
  console.error(JSON.stringify({ ok: false, blockers, changes }, null, 2));
  process.exit(1);
}
writeJson(outPath, result);
console.log(JSON.stringify({ ok: true, blockers, changes, out: outPath }, null, 2));
