#!/usr/bin/env node
import { readJson, stable, diffObjects, writeJson } from './merge-utils.mjs';

function arg(name) { const i = process.argv.indexOf(name); return i >= 0 ? process.argv[i + 1] : null; }
const existingPath = arg('--existing');
const patchPath = arg('--patch');
const reportPath = arg('--report');
if (!patchPath) {
  console.error('Usage: detect-openclaw-conflicts.mjs --patch patch.json [--existing openclaw.json] [--report report.json]');
  process.exit(2);
}
const existing = existingPath ? readJson(existingPath, {}) : {};
const patch = readJson(patchPath, {});
const blockers = [];
const warnings = [];
const additions = [];

const existingAgents = new Map((existing.agents?.list || []).map((a) => [a.id, a]));
for (const agent of patch.agents?.list || []) {
  const current = existingAgents.get(agent.id);
  if (!current) additions.push({ type: 'agent', id: agent.id });
  else if (diffObjects(current, agent)) blockers.push({ type: 'agent', id: agent.id, reason: 'same agent id exists with different config' });
}

const existingBindings = new Set((existing.bindings || []).map(stable));
for (const binding of patch.bindings || []) {
  if (!existingBindings.has(stable(binding))) additions.push({ type: 'binding', agentId: binding.agentId });
}

const accounts = patch.channels?.discord?.accounts || {};
for (const [accountId, account] of Object.entries(accounts)) {
  for (const [guildId, guild] of Object.entries(account.guilds || {})) {
    for (const [channelId, channel] of Object.entries(guild.channels || {})) {
      const wanted = channel.systemPrompt;
      const current = existing.channels?.discord?.accounts?.[accountId]?.guilds?.[guildId]?.channels?.[channelId]?.systemPrompt;
      if (current && wanted && current !== wanted) {
        blockers.push({ type: 'channel-systemPrompt', accountId, guildId, channelId, reason: 'existing non-empty systemPrompt differs' });
      } else if (!current && wanted) {
        additions.push({ type: 'channel-systemPrompt', accountId, guildId, channelId });
      }
    }
  }
}

const forbidden = ['auth','models','memory','talk','meta','wizard','tools','commands','approvals','session','hooks','gateway','plugins','credentials'];
for (const key of forbidden) {
  if (Object.prototype.hasOwnProperty.call(patch, key)) blockers.push({ type: 'forbidden-scope', key, reason: 'patch contains forbidden top-level key' });
}

const report = { ok: blockers.length === 0, blockers, warnings, additions };
if (reportPath) writeJson(reportPath, report);
console.log(JSON.stringify(report, null, 2));
process.exit(blockers.length ? 1 : 0);
