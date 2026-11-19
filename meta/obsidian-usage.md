# Obsidian Usage — Best Practices for this Vault

Stand: 2026-11-19 (CLI enabled: Settings > General > Advanced → “Command line interface”).

## General principles

- **Wikilinks between notes** are the core of the vault: use `[[Note]]` / `[[Note|Alias]]` for vault-internal connections. Avoid markdown links for intra-vault navigation — Obsidian resolves wikilinks natively.
- **MOC (Map of Contents):** every vault has a hub: vault-root `README.md` + `index/index.md` (MOC with wikilinks to all sections and all standard notes).
- **Backlinks:** links are bidirectional in Obsidian — when you link two notes, both show the connection. Use this actively: catalog → standards (forward links), standards → catalog/licensing/terms (backward links), index → standards (forward).
- **Tags:** canonical categorization in frontmatter (`tags: [IEC, IS, TC-65, Security]` etc.) — for filtering/searching (`#security`), Dataview, and graph coloring.
- **Folder taxonomy:** `standards/`, `processes/`, `electropedia/`, `guides/`, `news/`, `index/`, `meta/`, `templates/`.

## Frontmatter (Properties) as the canonical data store

Per-standard notes — `ref`, `title`, `type`, `edition`, `technical_committee`, `published`, `status`, `languages`, `price_chf`, `sources`, `tags`, optional `ics`, `area`. Agent-readable mirror: `index/index.json`.

## Views & Panels

- **Backlinks panel** (right sidebar): check backlinks of each standard (→ catalog, MOC, `meta/iec-structure.md`, `meta/licensing.md`).
- **Outgoing links panel**: per-note link overview.
- **Graph view**: recommended; vault is fully linked → structured graph (standards cluster ↔ processes/index).
- **Quick Switcher** (Ctrl/Cmd+O): navigate to standard notes, index, meta pages.
- **Search** (Ctrl+Shift+F / Ctrl+P): full-text — e.g., “IEC 61675-2”.

## Dataview (community plugin — installed & enabled)

- Community plugin installed via CLI: `obsidian plugin:install id=dataview` → **Dataview v0.5.68**; enabled in Obsidian (`obsidian plugins:enabled`).
- `meta/dataview.md` — ready-made queries (paste into notes; query the vault from Obsidian).

## Templates (core plugin — enabled)

- `templates/standard-note.md` — note template for future standards (same frontmatter schema). Core Templates plugin is enabled by default (`obsidian plugins:enabled` includes `templates`).

## CLI (enabled in this environment)

- `obsidian --version`, `obsidian --help`, `obsidian plugins:enabled --format=json` — check `meta/obsidian-cli.md` for this machine’s results.
- `obsidian hotkeys format=json > meta/hotkeys.json` — hotkeys reference (generated).
- `obsidian tags format=json > meta/tags.json` — tag index (generated).

## Version Control

- **Obsidian Git** (community plugin — installed & enabled: v2.43.0) — the vault is a private git repo (see [README.md](README.md)); commit/push via Obsidian Git UI or the CLI (`git push`).

## Anti-patterns (avoid)

- Markdown links `[x](y)` to vault files — use wikilinks.
- Duplicated frontmatter and prose (keep one canonical home per data point).
- Hiding data in screenshots — keep data in text/frontmatter.

## MASTER

See [meta/obsidian-cli.md](obsidian-cli.md), [meta/iec-structure.md](iec-structure.md).
