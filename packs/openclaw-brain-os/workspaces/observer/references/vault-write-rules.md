# Vault Write Rules

## When to read this

Read before creating, moving, renaming, or classifying durable files inside a Brain OS vault.

## Core rule

Do not treat the vault as a dumping ground. Raw inputs, tasks, plans, knowledge notes, project docs, and system references are different objects with different homes.

## Procedure

1. Inspect the current vault structure before creating folders.
2. Decide the object type:
   - raw capture
   - task / todo
   - project plan
   - knowledge note
   - system reference
   - generated digest/report
3. Prefer an existing directory over creating a new top-level category.
4. Use placeholders in public examples.
5. If the file is important, include enough metadata for future agents to understand source and status.
6. If the vault is git-backed, commit durable changes with a clear message.

## Common mistakes

- Creating duplicate numbered directories without checking existing structure.
- Putting prompts and plans in the same folder.
- Treating a chat message as the source of truth after a formal note exists.
- Writing private paths or names into public templates.

## Related public docs

- `docs/knowledge-architecture.md`
- `docs/references/vault-governance-guide.md`
- `skills/brain-vault-governance/SKILL.md`
