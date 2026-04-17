# Obsidian Setup — Recommended Plugins and Configuration

---

Your Obsidian vault folder name is user-defined. Throughout Brain OS docs, `BRAIN_PATH` or `{{BRAIN_ROOT}}` means your own vault root path.

## Core Plugins

These Obsidian plugins are recommended for Brain OS. Install from **Settings → Community Plugins → Browse**.

### Essential

| Plugin | Purpose | Why |
|--------|---------|-----|
| **Dataview** | Query vault content like a database | Powers dynamic views in briefings and backlogs |
| **Templater** | Advanced template insertion | Better than default templates for dynamic content |
| **Calendar** | Navigate daily notes by calendar view | Quick access to daily briefs and digests |

### Recommended

| Plugin | Purpose | Why |
|--------|---------|-----|
| **Graph Analysis** | Enhanced graph view | Visualize knowledge connections |
| **Homepage** | Set a default landing page | Set `04-DIGESTS/` or `daily-briefing.md` as home |
| **Tag Wrangler** | Manage tags | Rename, merge, clean up tags across vault |
| **Linter** | Format markdown automatically | Keep consistent formatting |
| **Quick Add** | Quick capture from anywhere | Fast inbox entry without leaving current note |

### Optional (Power Users)

| Plugin | Purpose | Why |
|--------|---------|-----|
| **DB Folder** | Notion-like database views | If you want kanban/table views for todos |
| **Kanban** | Kanban boards | Visual project tracking |
| **Excalidraw** | Drawings and diagrams | For architecture sketches |
| **Tasks** | Task management with queries | If you use checkbox tasks extensively |
| **Periodic Notes** | Daily/weekly/monthly notes | If you want structured note creation |

---

## Configuration

### .obsidian/appearance.json

```json
{
  "cssTheme": "",
  "accentColor": "#4a9eff",
  "baseFontSize": 16,
  "translucency": false
}
```

### .obsidian/file-explorer.json

Recommended: Pin frequently accessed folders to the top of the file explorer:
1. `00-INBOX/`
2. `01-PERSONAL-OPS/01-DAILY-BRIEFS/`
3. `03-KNOWLEDGE/01-READING/04-DIGESTS/`
4. `05-PROJECTS/01-ACTIVE/`

### Homepage Setting

Set your homepage to the daily digest or daily briefing:
- Install **Homepage** plugin
- Settings → Homepage → Homepage file: `03-KNOWLEDGE/01-READING/04-DIGESTS/nightly-digest-{date}.md`

Or manually: always open the latest digest file when you start Obsidian.

---

## Vault Settings

### Editor

- **Default editing mode**: Source mode (better for AI-generated content)
- **Readable line length**: On
- **Spellcheck**: Your preference

### Files & Links

- **Default location for new notes**: `00-INBOX/`
- **New link format**: Shortest path when possible
- **Use [[Wikilinks]]**: On (Brain OS uses wikilinks throughout)

### Search

- **Sort search results by**: Last modified (most recent first)

---

## Tags

Brain OS uses tags for knowledge classification. Recommended tag structure:

```
#domain/ai-agent
#domain/engineering
#domain/product
#domain/management
#type/article-note
#type/pattern
#type/topic
#type/research-question
#status/pending
#status/integrated
#status/archived
```

Use **Tag Wrangler** plugin to manage these consistently.

---

## Performance Tips

### For Large Vaults (500+ notes)

1. **Disable unused plugins** — each plugin adds startup time
2. **Use `.obsidian/workspace.json` exclusions** — exclude `99-SYSTEM/` from search indexing
3. **Set Graph view filter** — exclude `99-SYSTEM/`, `memory/`, and `.git/` from graph
4. **Periodic cleanup** — run `knowledge-lint.sh` to find orphaned/stale notes

### Search Optimization

Add to `.obsidian/search.json` (if the file exists):
```json
{
  "exclude": [
    "99-SYSTEM/**",
    "node_modules/**",
    ".git/**"
  ]
}
```

---

## Mobile Setup

Brain OS works on Obsidian Mobile (iOS/Android):

1. Use **Obsidian Sync** or **iCloud** to sync your vault
2. Install the same essential plugins (Dataview, Templater)
3. Set homepage to daily briefing for quick mobile access
4. Use **Quick Add** widget for fast capture on mobile
