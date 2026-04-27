#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';

function usage() {
  console.error('Usage: node scripts/render.mjs --answers answers.json --out preview-dir [--pack pack-dir]');
  process.exit(2);
}

function arg(name) {
  const i = process.argv.indexOf(name);
  return i >= 0 ? process.argv[i + 1] : null;
}

const scriptDir = path.dirname(new URL(import.meta.url).pathname);
const packDir = path.resolve(arg('--pack') || path.join(scriptDir, '..'));
const answersPath = arg('--answers');
const outDir = arg('--out');
if (!answersPath || !outDir) usage();

const answers = JSON.parse(fs.readFileSync(answersPath, 'utf8'));
const manifest = JSON.parse(fs.readFileSync(path.join(packDir, 'manifest.json'), 'utf8'));
const profileId = answers.profile || manifest.installDefaults.profile || 'minimal';
const profile = manifest.profiles.find((p) => p.id === profileId);
if (!profile) throw new Error(`Unknown profile: ${profileId}`);

const userHome = answers.userHome || '{{USER_HOME}}';
const openclawRoot = answers.openclawRoot || `${userHome}/.openclaw`;
const skillsRoot = answers.skillsRoot || `${userHome}/.agents/skills`;
const brainRoot = answers.brainRoot || `${userHome}/Documents/My-Brain`;
const replacements = {
  USER_HOME: userHome,
  OPENCLAW_ROOT: openclawRoot,
  SKILLS_ROOT: skillsRoot,
  BRAIN_ROOT: brainRoot,
  BRAIN_NAME: path.basename(brainRoot),
  TIMEZONE: answers.timezone || 'UTC',
  OWNER_NAME: answers.ownerName || '{{OWNER_NAME}}',
  MAIN_MODEL: answers.models?.main || '{{MAIN_MODEL}}',
  LIGHT_MODEL: answers.models?.light || '{{LIGHT_MODEL}}',
  DISCORD_GUILD_ID: answers.discord?.guildId || '{{DISCORD_GUILD_ID}}',
  DISCORD_OWNER_USER_ID: answers.discord?.ownerUserId || '{{DISCORD_OWNER_USER_ID}}',
  MAIN_CHANNEL_ID: answers.discord?.channels?.main || '{{MAIN_CHANNEL_ID}}',
  PERSONAL_OPS_CHANNEL_ID: answers.discord?.channels?.personalOps || '{{PERSONAL_OPS_CHANNEL_ID}}',
  KNOWLEDGE_INGEST_CHANNEL_ID: answers.discord?.channels?.knowledgeIngest || '{{KNOWLEDGE_INGEST_CHANNEL_ID}}',
  KNOWLEDGE_QUERY_CHANNEL_ID: answers.discord?.channels?.knowledgeQuery || '{{KNOWLEDGE_QUERY_CHANNEL_ID}}',
  OSS_SYNC_CHANNEL_ID: answers.discord?.channels?.ossSync || '{{OSS_SYNC_CHANNEL_ID}}',
  CRON_NOTIFICATION_CHANNEL_ID: answers.discord?.channels?.cronNotifications || '{{CRON_NOTIFICATION_CHANNEL_ID}}',
  QMD_BIN: answers.qmdBin || '{{QMD_BIN}}'
};

function renderText(text) {
  return text.replace(/\{\{([A-Z0-9_]+)\}\}/g, (m, key) => replacements[key] ?? m);
}

function ensureDir(dir) { fs.mkdirSync(dir, { recursive: true }); }
function writeRendered(src, dest) {
  ensureDir(path.dirname(dest));
  fs.writeFileSync(dest, renderText(fs.readFileSync(src, 'utf8')));
}
function copyRenderedDir(srcDir, destDir) {
  for (const entry of fs.readdirSync(srcDir, { withFileTypes: true })) {
    const src = path.join(srcDir, entry.name);
    const dest = path.join(destDir, entry.name);
    if (entry.isDirectory()) copyRenderedDir(src, dest);
    else writeRendered(src, dest);
  }
}

fs.rmSync(outDir, { recursive: true, force: true });
ensureDir(outDir);
writeRendered(path.join(packDir, 'openclaw.json.patch.template'), path.join(outDir, 'openclaw.config-patch.json'));
writeRendered(path.join(packDir, 'cron/jobs.patch.template'), path.join(outDir, 'cron.jobs-patch.json'));

const selectedAgents = profile.agents || ['main'];
for (const agent of selectedAgents) {
  const src = path.join(packDir, 'workspaces', agent);
  if (fs.existsSync(src)) copyRenderedDir(src, path.join(outDir, 'workspaces', agent));
}
// PR1b makes non-selected templates visible in preview for review, without declaring them enabled.
for (const agent of ['writer', 'review', 'chronicle', 'observer']) {
  const src = path.join(packDir, 'workspaces', agent);
  if (fs.existsSync(src)) copyRenderedDir(src, path.join(outDir, 'available-workspaces', agent));
}

const canonicalVault = manifest.canonicalVaultTemplate || '../../vault-template';
const summary = {
  packName: manifest.packName,
  packVersion: manifest.packVersion,
  mode: 'dry-run-preview',
  profile: profileId,
  selectedAgents,
  selectedSkills: profile.skills || [],
  selectedCronJobs: profile.cronJobs || [],
  paths: { openclawRoot, skillsRoot, brainRoot, canonicalVaultTemplate: canonicalVault },
  generatedFiles: [
    'openclaw.config-patch.json',
    'cron.jobs-patch.json',
    'workspaces/',
    'available-workspaces/'
  ],
  notes: [
    'This preview does not modify user files.',
    'Apply/rollback is planned for a later PR.',
    'Cron jobs remain disabled by default.'
  ]
};
fs.writeFileSync(path.join(outDir, 'summary.json'), JSON.stringify(summary, null, 2) + '\n');
fs.writeFileSync(path.join(outDir, 'diff-summary.md'), `# OpenClaw Brain OS Pack Dry-run Preview\n\n- Pack: ${manifest.packName} ${manifest.packVersion}\n- Profile: ${profileId}\n- OpenClaw root: \`${openclawRoot}\`\n- Skills root: \`${skillsRoot}\`\n- Brain root: \`${brainRoot}\`\n- Canonical vault template: \`${canonicalVault}\`\n\n## Would generate\n\n- \`openclaw.config-patch.json\`\n- \`cron.jobs-patch.json\`\n- \`workspaces/${selectedAgents.join('`, `workspaces/')}\`\n- \`available-workspaces/writer|review|chronicle|observer\`\n\nNo user files were modified.\n`);

console.log(outDir);
