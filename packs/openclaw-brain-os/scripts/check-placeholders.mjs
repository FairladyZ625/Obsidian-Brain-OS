#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';
const root = path.resolve(process.argv[2] || '.');
const allow = new Set((process.env.ALLOW_PLACEHOLDERS || '').split(',').filter(Boolean));
let hits = [];
function walk(p) {
  for (const e of fs.readdirSync(p, { withFileTypes: true })) {
    const f = path.join(p, e.name);
    if (e.isDirectory()) walk(f);
    else {
      const text = fs.readFileSync(f, 'utf8');
      for (const m of text.matchAll(/\{\{([A-Z0-9_]+)\}\}/g)) {
        if (!allow.has(m[1])) hits.push(`${f}:${m[1]}`);
      }
    }
  }
}
walk(root);
if (hits.length) {
  console.error('Unresolved placeholders found:');
  console.error(hits.join('\n'));
  process.exit(1);
}
console.log('placeholder check ok');
