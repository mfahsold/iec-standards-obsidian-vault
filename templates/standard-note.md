---
title: Standard Note Template (Obsidian — Templates Plugin / Copy-Paste)
type: "template"
description: "Frontmatter schema + body skeleton for new standard notes in standards/"
---

# Standard Note — Template

Copy this template into `standards/` when adding a new IEC standard (or edit this file with the Templates plugin enabled).

## frontmatter (Properties)

```yaml
---
ref: ""                  # e.g. "IEC 62443-4-1:2018"
title: ""                # full standard title
type: "IS"               # IS | TS | TR | PAS | ISH | IEV | TRF | ISO/IEC
part: ""                 # e.g. "-1:1" (optional)
edition: ""              # e.g. "1.0" (RLV: append " (RLV)")
technical_committee: ""  # e.g. "TC 65"
published: ""            # IEC publication date (YYYY-MM-DD)
stability_date: ""       # IEC stability date (YYYY)
status: "active"         # active | replaced | withdrawn
languages: ["English"]
price_chf: null          # CHF — null if unknown/not sold
ics: ""                  # IEC ICS codes (from Webstore product page)
area: ""                 # Technical area (Webstore: Electrical/Health/...)
sources:
  - ""                   # Webstore product page URL
tags:
  - "IEC"
  - "IS"
  - "TC-65"
  - "Security"
---
```

## body

# <Standard title (ref)>

> [!note] TL;DR
> One-sentence summary of the standard.

## Description

Factual scope from the official product page/Webstore text.

## Editions / Technical Committee

- TC: <...>
- ICS: <...>
- Publication date: <...>
- Stability date: <...>
- Pages: <...> (if known)

## Metadata

- **Stand:** 2026-11-19 — data from official IEC Webstore pages (manual crawl).
- **Price:** CHF <...> — “as of Crawl-Date” (see [meta/crawl-notes.md](../meta/crawl-notes.md)).
- **Languages:** English.

## Notes

- Preis dynamic — check current catalogue: [Webstore “All products”](https://webstore.iec.ch/en/products/).
- [[standards/index-standards.md|Standards in this Vault]]
- [[processes/webstore-terms.md|IEC Webstore AGBs]]
- [[meta/licensing.md|Licensing & approach to IEC]]
