# Vault Template Strategy

The canonical Brain OS vault template lives at the repository root:

```text
vault-template/
```

The pack installer should copy that directory into the user's chosen Brain vault path.

This folder exists only for pack-specific notes, overlays, and checks. It must not become a second full copy of the vault template unless the project intentionally migrates the root template into the pack in the same PR.

## Installer expectation

Future installer flow:

1. Read `manifest.json`.
2. Resolve `canonicalVaultTemplate` (`../../vault-template`).
3. Copy the canonical template into `{{BRAIN_ROOT}}` if the target is empty.
4. If the target already exists, run structure checks and report conflicts instead of overwriting.
5. Apply optional overlays only after preview and confirmation.
