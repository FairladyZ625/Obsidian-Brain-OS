#!/usr/bin/env node
import { readJson, writeJson, deepClone, stable, diffObjects } from './merge-utils.mjs';

function arg(name) { const i = process.argv.indexOf(name); return i >= 0 ? process.argv[i + 1] : null; }
const existingPath = arg('--existing');
const patchPath = arg('--patch');
const outPath = arg('--out');
const force = process.argv.includes('--force');
if (!patchPath || !outPath) {
  console.error('Usage: merge-openclaw-config.mjs --patch patch.json --out out.json [--existing openclaw.json] [--force]');
  process.exit(2);
}
const existing = existingPath ? readJson(existingPath, {}) : {};
const patch = readJson(patchPath, {});
const result = deepClone(existing || {});
const changes = [];
const blockers = [];

function ensureObject(root, key) {
  if (!root[key] || typeof root[key] !== 'object' || Array.isArray(root[key])) root[key] = {};
  return root[key];
}

// agents.list append missing, never overwrite conflicting id unless --force.
if (patch.agents?.list?.length) {
  result.agents = result.agents || {};
  result.agents.list = result.agents.list || [];
  const byId = new Map(result.agents.list.map((a) => [a.id, a]));
  for (const agent of patch.agents.list) {
    const current = byId.get(agent.id);
    if (!current) {
      result.agents.list.push(agent);
      changes.push({ action: 'add-agent', id: agent.id });
    } else if (diffObjects(current, agent)) {
      blockers.push({ type: 'agent', id: agent.id, reason: 'same agent id exists with different config' });
      if (force) Object.assign(current, agent);
    }
  }
}

// agents other keys: only add missing defaults; do not overwrite.
if (patch.agents) {
  result.agents = result.agents || {};
  for (const [k, v] of Object.entries(patch.agents)) {
    if (k === 'list') continue;
    if (result.agents[k] === undefined) {
      result.agents[k] = v;
      changes.push({ action: 'add-agents-key', key: k });
    }
  }
}

// bindings append unique by stable JSON.
if (patch.bindings?.length) {
  result.bindings = result.bindings || [];
  const seen = new Set(result.bindings.map(stable));
  for (const binding of patch.bindings) {
    const key = stable(binding);
    if (!seen.has(key)) {
      result.bindings.push(binding);
      seen.add(key);
      changes.push({ action: 'add-binding', agentId: binding.agentId });
    }
  }
}

// skills.paths append missing.
if (patch.skills?.paths?.length) {
  result.skills = result.skills || {};
  result.skills.paths = result.skills.paths || [];
  for (const p of patch.skills.paths) {
    if (!result.skills.paths.includes(p)) {
      result.skills.paths.push(p);
      changes.push({ action: 'add-skill-path', path: p });
    }
  }
}

// channels.discord: add safe fields, add systemPrompt only if empty/missing.
if (patch.channels?.discord) {
  result.channels = result.channels || {};
  result.channels.discord = result.channels.discord || {};
  const rd = result.channels.discord;
  const pd = patch.channels.discord;
  for (const key of ['enabled', 'token', 'groupPolicy']) {
    if (pd[key] !== undefined && rd[key] === undefined) {
      rd[key] = pd[key];
      changes.push({ action: 'add-discord-key', key });
    }
  }
  if (pd.guilds) {
    rd.guilds = rd.guilds || {};
    for (const [guildId, guildPatch] of Object.entries(pd.guilds)) {
      rd.guilds[guildId] = rd.guilds[guildId] || {};
      for (const [k, v] of Object.entries(guildPatch)) if (rd.guilds[guildId][k] === undefined) rd.guilds[guildId][k] = v;
    }
  }
  if (pd.accounts) {
    rd.accounts = rd.accounts || {};
    for (const [accountId, accountPatch] of Object.entries(pd.accounts)) {
      const account = rd.accounts[accountId] = rd.accounts[accountId] || {};
      account.guilds = account.guilds || {};
      for (const [guildId, guildPatch] of Object.entries(accountPatch.guilds || {})) {
        const guild = account.guilds[guildId] = account.guilds[guildId] || {};
        guild.channels = guild.channels || {};
        for (const [channelId, channelPatch] of Object.entries(guildPatch.channels || {})) {
          const channel = guild.channels[channelId] = guild.channels[channelId] || {};
          if (channelPatch.systemPrompt && channel.systemPrompt && channel.systemPrompt !== channelPatch.systemPrompt) {
            blockers.push({ type: 'channel-systemPrompt', accountId, guildId, channelId, reason: 'existing non-empty systemPrompt differs' });
            if (force) channel.systemPrompt = channelPatch.systemPrompt;
          } else if (channelPatch.systemPrompt && !channel.systemPrompt) {
            channel.systemPrompt = channelPatch.systemPrompt;
            changes.push({ action: 'add-channel-systemPrompt', accountId, guildId, channelId });
          }
        }
      }
    }
  }
}

if (blockers.length && !force) {
  console.error(JSON.stringify({ ok: false, blockers, changes }, null, 2));
  process.exit(1);
}
writeJson(outPath, result);
console.log(JSON.stringify({ ok: true, blockers, changes, out: outPath }, null, 2));
