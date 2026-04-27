#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';
import { spawnSync } from 'node:child_process';
import { readJson, writeJson, ensureDir, backupFile, copyDirMissingOnly, copyDirToEmptyTarget } from './merge-utils.mjs';

function arg(name) { const i = process.argv.indexOf(name); return i >= 0 ? process.argv[i + 1] : null; }
const scriptDir = path.dirname(new URL(import.meta.url).pathname);
const packDir = path.resolve(arg('--pack') || path.join(scriptDir, '..'));
const previewDir = path.resolve(arg('--preview') || '');
const answersPath = path.resolve(arg('--answers') || path.join(packDir, 'answers.example.json'));
const yes = process.argv.includes('--yes');
const force = process.argv.includes('--force');
if (!previewDir || !fs.existsSync(previewDir)) {
  console.error('Usage: apply.mjs --pack pack-dir --preview preview-dir --answers answers.json --yes [--force]');
  process.exit(2);
}
if (!yes) {
  console.error('Refusing to apply without --yes. Run --dry-run first and review the preview.');
  process.exit(2);
}
const answers = readJson(answersPath, {});
const manifest = readJson(path.join(packDir, 'manifest.json'), {});
const summary = readJson(path.join(previewDir, 'summary.json'), {});
const userHome = answers.userHome || process.env.HOME || '';
const openclawRoot = answers.openclawRoot || summary.paths?.openclawRoot || path.join(userHome, '.openclaw');
const skillsRoot = answers.skillsRoot || summary.paths?.skillsRoot || path.join(userHome, '.agents/skills');
const brainRoot = answers.brainRoot || summary.paths?.brainRoot || path.join(userHome, 'Documents/My-Brain');
const installId = new Date().toISOString().replace(/[:.]/g, '-');
const installStateDir = path.join(openclawRoot, '.brain-os-pack-installs', installId);
const backupDir = path.join(installStateDir, 'backups');
const changes = [];

ensureDir(openclawRoot);
ensureDir(path.join(openclawRoot, 'cron'));
ensureDir(skillsRoot);
ensureDir(installStateDir);

const openclawConfig = path.join(openclawRoot, 'openclaw.json');
const cronJobs = path.join(openclawRoot, 'cron', 'jobs.json');
backupFile(openclawConfig, backupDir, changes);
backupFile(cronJobs, backupDir, changes);

const mergedConfig = path.join(installStateDir, 'openclaw.merged.json');
const mergeConfig = spawnSync(process.execPath, [
  path.join(scriptDir, 'merge-openclaw-config.mjs'),
  '--patch', path.join(previewDir, 'openclaw.config-patch.json'),
  '--out', mergedConfig,
  ...(fs.existsSync(openclawConfig) ? ['--existing', openclawConfig] : []),
  ...(force ? ['--force'] : [])
], { encoding: 'utf8' });
if (mergeConfig.status !== 0) {
  fs.writeFileSync(path.join(installStateDir, 'merge-openclaw-config.error.log'), mergeConfig.stderr || mergeConfig.stdout || 'merge failed');
  console.error(mergeConfig.stderr || mergeConfig.stdout);
  process.exit(1);
}
fs.copyFileSync(mergedConfig, openclawConfig);
changes.push({ action: 'write', path: openclawConfig });

const mergedCron = path.join(installStateDir, 'cron.jobs.merged.json');
const mergeCron = spawnSync(process.execPath, [
  path.join(scriptDir, 'merge-cron-jobs.mjs'),
  '--patch', path.join(previewDir, 'cron.jobs-patch.json'),
  '--out', mergedCron,
  ...(fs.existsSync(cronJobs) ? ['--existing', cronJobs] : []),
  ...(force ? ['--force'] : [])
], { encoding: 'utf8' });
if (mergeCron.status !== 0) {
  fs.writeFileSync(path.join(installStateDir, 'merge-cron-jobs.error.log'), mergeCron.stderr || mergeCron.stdout || 'merge failed');
  console.error(mergeCron.stderr || mergeCron.stdout);
  process.exit(1);
}
fs.copyFileSync(mergedCron, cronJobs);
changes.push({ action: 'write', path: cronJobs });

const workspacePreview = path.join(previewDir, 'workspaces');
if (fs.existsSync(workspacePreview)) {
  for (const agent of fs.readdirSync(workspacePreview)) {
    copyDirMissingOnly(path.join(workspacePreview, agent), path.join(openclawRoot, 'agents', agent, 'agent'), changes);
  }
}

const canonicalVault = path.resolve(packDir, manifest.canonicalVaultTemplate || '../../vault-template');
if (!fs.existsSync(brainRoot) || fs.readdirSync(brainRoot).length === 0) {
  copyDirToEmptyTarget(canonicalVault, brainRoot, changes);
} else {
  changes.push({ action: 'skip-existing-vault', path: brainRoot });
}

const installState = { installId, pack: manifest.packName, packVersion: manifest.packVersion, appliedAt: new Date().toISOString(), paths: { openclawRoot, skillsRoot, brainRoot }, backupDir, changes };
writeJson(path.join(installStateDir, 'install-state.json'), installState);
writeJson(path.join(openclawRoot, '.brain-os-pack-last-install.json'), { installId, installStateDir });
console.log(JSON.stringify({ ok: true, installId, installStateDir, changes }, null, 2));
