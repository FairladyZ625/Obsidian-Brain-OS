#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';
const root = path.resolve(process.argv[2] || '.');
const patterns = [
  /\/Users\/[A-Za-z0-9._-]+/,
  /discord[.]com\/api\/webhooks/,
  /sk-[A-Za-z0-9_-]{12,}/,
  /xoxb-/,
  /Bot [A-Za-z0-9._-]{20,}/,
  /[0-9]{18,20}/
];
let hits = [];
function walk(p) {
  for (const e of fs.readdirSync(p, { withFileTypes: true })) {
    const f = path.join(p, e.name);
    if (e.isDirectory()) walk(f);
    else if (!f.endsWith('scan-secrets.mjs') && !f.endsWith('smoke.sh')) {
      const text = fs.readFileSync(f, 'utf8');
      for (const re of patterns) if (re.test(text)) hits.push(f);
    }
  }
}
walk(root);
if (hits.length) {
  console.error('secret/private-looking material found:');
  console.error([...new Set(hits)].join('\n'));
  process.exit(1);
}
console.log('secret scan ok');
