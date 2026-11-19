# IEC Standards Obsidian Vault (Prototype)

Obsidian vault with publicly available IEC information — built for Obsidian, optimized for LLM/agent usage, and vault-internal navigation via Obsidian wikilinks.

> **Status: Prototype, Data Stand: 2026-11-19** — Repo is currently **private** (local, no push). See [meta/licensing.md](meta/licensing.md) for public-setup notes.

## Quick Start (Obsidian)

- Open the vault folder `iec-standards-obsidian-vault/` in Obsidian.
- **Home/Welcome:** this `README.md` (vault root) + `index/index.md` (MOC — fully linked).
- **Search** (Ctrl+Shift+F or Ctrl+P): full-text search.
- **Quick Switcher** (Ctrl/Cmd+O): jump to any note.
- **Graph View:** recommended; fully linked vault.

## Quick Links (navigation)

- 🏠 **Vault Home (you are here):** [README.md](README.md) — also the vault root.
- 📑 **MOC (Map of Contents):** [index/index.md](index/index.md) — master index + full standards table.
- 🔍 **Quick Switcher:** `Ctrl/Cmd + O` — jump to any note.
- 🌐 **Global Search:** `Ctrl + Shift + F` (or `Ctrl + P`) — full-text search.
- 🧭 **Graph View:** core plugin (`graph`) — enabled by default in this vault.
- ⚙️ **Backlinks / Outgoing Links:** right sidebar — see connections of the current note.

## Stats (2026-11-19)

- Files: 56 (47 Markdown); Notes: 47
- Standards: 18 product notes (+ classics set)
- Types: IS 7, ISO/IEC 1, TRF 1, PAS 3, TR 6
- Words: ~15.8k (`find . -name "*.md" -not -path "./.git/*" -print0 | xargs -0 wc -w | tail -1`)

## What is in this vault

- **`standards/` — IEC product catalog** with metadata: Ref (e.g., `IEC 62443-4-1:2018`), Type (IS/TS/TR/PAS/...), Technical Area, Technical Committee, Edition date, Publication date, ICS, Price (CHF), Stability date, Languages, and source links. **No document bodies** of the IEC standards (copyright IEC — see `meta/licensing.md`).
- **`processes/` — IEC processes and document types** (IS/TS/TR/PAS/ISH/IEV workflows, development stages, work programme, publication lifecycle, webstore AGBs, affiliate programme, OSD, Directives).
- **`electropedia/` — IEV Online** (free): 22,000+ terms, ~30 languages.
- **`guides/` — IEC Guides** (GUIDE 103, 104, 107, 108, 109, …).
- **`news/` — Free newsletter “IEC Just Published”** (monthly, 1st).
- **`index/` — Master index**: `index.md` (MOC), `index.json` (machine-readable).
- **`meta/` — sources, licensing, data provenance, IEC logic/structure, Obsidian usage, Obsidian CLI check.**
- **`templates/` — standard note template** (Obsidian Templates plugin).

## LLM/agent optimization

- Atomic notes with YAML frontmatter (`ref`, `type`, `edition`, `technical_committee`, `published`, `ics`, `status`, `price_chf`, `sources[]`, `tags`) — machine-readable.
- `index/index.json` — machine-readable index mirroring the frontmatter.

## Obsidian Best Practices used

- Wikilinks between notes (`[[Note]]`/`[[Note|Alias]]`), Backlinks panel, Outgoing links panel, Quick Switcher, Search, Graph view — see [meta/obsidian-usage.md](meta/obsidian-usage.md).
- Frontmatter (Properties) as the canonical data store.
- Tags on standard notes (`IEC`, `IS`, `TC-65`, `Security`, …).
- Dataview (optional plugin): [meta/dataview.md](meta/dataview.md) — ready queries.
- Templates (Obsidian Templates plugin): [templates/standard-note.md](templates/standard-note.md).

## IEC logic/structure (sorting)

- [meta/iec-structure.md](meta/iec-structure.md) — TC/SC names, ICS codes, SDG anchors, statuses, project stages, IEC views.
- Sorting rules: [meta/iec-structure.md](meta/iec-structure.md) §Sorting Rules (Type → TC/SC → ICS → Status → Edition → Date → Price).

## Scope ("all publicly available IEC standards")

- “All products” in the IEC Webstore: https://webstore.iec.ch/en/products/ (incl. “Just Published”, “Bestsellers”, “Products by technical area”).
- IEC Library Server (login): https://library.iec.ch/ — full catalog (all IEC publications incl. “Replaced / Withdrawn”) for members/appointees.
- Third-party aggregators: https://www.normfile.com/iec.html, https://www.bsbedge.com/free-downloads/international-electrotechnical-commission/ — large catalogs from foreign lists (references).
- This vault currently contains **verified data from official webstore pages (18 product notes + classics set)** — see [index/index.md](index/index.md) for the catalog table.

## Data Stand & Updates

- 2026-11-19: data retrieved from official webstore/IEC pages (manually, via browser) + IEC Webstore product pages (publication/33615, 63886, 106458, …).
- Prices and publication dates are marked “as of Crawl-Date”; details in [meta/crawl-notes.md](meta/crawl-notes.md).

## CLI

- Obsidian CLI: enabled (Settings > General > Advanced → “Command line interface”), version 1.15.1 — check: [meta/obsidian-cli.md](meta/obsidian-cli.md).
