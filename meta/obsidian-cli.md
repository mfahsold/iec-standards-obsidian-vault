# Obsidian CLI — Check on this Machine

Stand: 2026-11-19.

## Environment

- Binary: /opt/homebrew/bin/obsidian (installed via brew).
- Version: 1.15.1 (installer 1.15.0) — `obsidian version`.
- Enabled in: Settings > General > Advanced → “Command line interface” (the user enabled it: “the command line interface is on now”).
- Obsidian app running (pgrep -af -i obsidian → PIDs found).
- CLI context: commands run from the vault directory (`cd /Users/matthiasfahsold/Projects/IEC_Agentic/iec-standards-obsidian-vault`); `obsidian files` lists paths as `iec-standards-obsidian-vault/...` — i.e., vault-relative paths (folder/note.md).

## Command surface (`obsidian --help`, full)

Command families: aliases, append, backlinks, base:*, bookmark(s), command(s), create, delete, diff, file, files, folders, folder, help, history*, hotkey(s), links, move, open, orphans, outline, plugin*, plugins*, prepend, properties, property:*, random*, read, recents, reload, rename, restart, search, search:context, search:open, snippet:*, snippets, snippets:enabled, sync*, tab:open, tabs, tag, tags, task, tasks, template:insert, template:read, templates, theme.

## Tests on this vault

1. `obsidian backlinks path="iec-standards-obsidian-vault/standards/IEC-62443-4-1-2018.md"` → backlinks: [`iec-standards-obsidian-vault/meta/iec-structure.md`] — the Markdown-style link in `meta/iec-structure.md` (Obsidian recognizes Markdown links as well as wikilinks).
2. `obsidian read path="iec-standards-obsidian-vault/standards/IEC-62443-4-1-2018.md"` → returns file contents (frontmatter + body).
3. `obsidian orphans total` → 10; `obsidian orphans all` → the 10 files with no incoming links:
   - iec-standards-obsidian-vault/LICENSE
   - iec-standards-obsidian-vault/meta/obsidian-usage.md
   - iec-standards-obsidian-vault/news/just-published-newsletter.md
   - iec-standards-obsidian-vault/README.md
   - iec-standards-obsidian-vault/standards/classics.md
   - iec-standards-obsidian-vault/standards/IEC-61675-2-2026-RLV.md
   - iec-standards-obsidian-vault/standards/IEC-62443-3-3-2013.md
   - iec-standards-obsidian-vault/standards/IEC-62443-4-2-2019.md
   - iec-standards-obsidian-vault/standards/ISO-IEC-25791-2-2026.md
   - iec-standards-obsidian-vault/templates/standard-note.md
4. `obsidian files` → 45 files.
5. `obsidian backlinks path="standards/IEC-62443-4-1-2018.md"` (without vault prefix) → Error — path must be vault-relative: `iec-standards-obsidian-vault/...`.

→ Recheck after adding backlinks (MOC + catalog links, next chunks).
