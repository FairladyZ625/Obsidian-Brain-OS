import fs from 'node:fs';
import path from 'node:path';

export function readJson(file, fallback = null) {
  if (!fs.existsSync(file)) return fallback;
  return JSON.parse(fs.readFileSync(file, 'utf8'));
}

export function writeJson(file, value) {
  fs.mkdirSync(path.dirname(file), { recursive: true });
  fs.writeFileSync(file, JSON.stringify(value, null, 2) + '\n');
}

export function stable(value) {
  if (Array.isArray(value)) return `[${value.map(stable).join(',')}]`;
  if (value && typeof value === 'object') {
    return `{${Object.keys(value).sort().map((k) => `${JSON.stringify(k)}:${stable(value[k])}`).join(',')}}`;
  }
  return JSON.stringify(value);
}

export function deepClone(value) {
  return JSON.parse(JSON.stringify(value));
}

export function isObject(value) {
  return value && typeof value === 'object' && !Array.isArray(value);
}

export function diffObjects(a, b) {
  return stable(a) !== stable(b);
}

export function ensureDir(dir) {
  fs.mkdirSync(dir, { recursive: true });
}

export function copyDirMissingOnly(srcDir, destDir, changes = []) {
  if (!fs.existsSync(srcDir)) return changes;
  ensureDir(destDir);
  for (const entry of fs.readdirSync(srcDir, { withFileTypes: true })) {
    const src = path.join(srcDir, entry.name);
    const dest = path.join(destDir, entry.name);
    if (entry.isDirectory()) {
      copyDirMissingOnly(src, dest, changes);
    } else if (!fs.existsSync(dest)) {
      ensureDir(path.dirname(dest));
      fs.copyFileSync(src, dest);
      changes.push({ action: 'copy', path: dest });
    } else {
      changes.push({ action: 'skip-existing', path: dest });
    }
  }
  return changes;
}

export function copyDirToEmptyTarget(srcDir, destDir, changes = []) {
  if (!fs.existsSync(srcDir)) return changes;
  ensureDir(destDir);
  copyDirMissingOnly(srcDir, destDir, changes);
  return changes;
}

export function backupFile(file, backupDir, changes = []) {
  if (!fs.existsSync(file)) return null;
  ensureDir(backupDir);
  const backup = path.join(backupDir, path.basename(file));
  fs.copyFileSync(file, backup);
  changes.push({ action: 'backup', from: file, to: backup });
  return backup;
}
