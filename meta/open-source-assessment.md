# Open Source Eligibility — Assessment (2026-11-19)

## Question

Can this Obsidian Vault be published open source?

## Answer (summary)

**Yes — with conditions.** The Vault contains **no IEC document bodies/texts** (no PDFs, no full standard texts, no verbatim IEC publications). What it contains:

1. **Catalog facts** — refs, titles, editions, TCs/SCs, ICS codes, publication/stability dates, languages, prices, SDG tags, URLs. Factual data, consistent with what is published by IEC Webstore and by aggregators (e.g., normfile.com, bsbedge.com list thousands of IEC standards with titles/links). Low risk — IEC product data is made available via the Webstore; the facts (ref + title + edition) are the IEC standard identifiers.
2. **Short descriptive text** — short factual descriptions; the long product-page descriptions were paraphrased in chunk G (2026-11-19); remaining verbatim strings are title-level (see below).
3. **Process documentation** — IEC workflows/procedures — quoted with links, public information.
4. **Electropedia facts** — descriptive facts about Electropedia (22,000+ terms etc.), with attribution (Electropedia encourages citing IEC as source; bulk duplication needs IEC contact).

## Licensing strategy for publication

- **Vault license:** CC0 1.0 (public domain) — for metadata, catalog data, processes, our summaries, links.
- **Electropedia-derived parts:** CC BY 4.0 — attribution required ("We only ask that IEC is referenced as the source" per Electropedia rules — `meta/licensing.md`).
- **Attribution:** `meta/sources.md` lists all URLs + origin for every data point.
- **Verified:** no IEC document bodies embedded (verbatim check below).
- **Visibility:** flipping the GitHub repo from private → public is a separate user decision (not done automatically).

## Verbatim excerpts in current state (review)

- `standards/IECEE-TRF-60335-2-2O-2026.md` — Description: standard ID + scope title ("vacuum cleaners and water-suction cleaning appliances") — factual, OK.
- `standards/ISO-IEC-25791-2-2026.md` — Description: title + edition + committee — factual, OK.
- `standards/CISPR-PAS-38-2025.md` — Description: compact factual scope sentences (~2 sentences, covers range + scope) — OK.
- All other long verbatim product-page descriptions in Notes were replaced by paraphrases in chunk G (2026-11-19): IEC-61675-2-2026, IEC-62443-4-1-2018, IEC-60079-1-2026, IEC-TR-63650-2026, IEC-TR-62476-2010, IEC-TR-61869-103-2012, IEC-TR-60919-1-2020-RLV, IEC-TR-63411-2025, IEC-PAS-62443-2-2-2025, IEC-PAS-63441-2022, IEC-61800-9-1-2026-RLV, IEC-TR-62380-2004.

## Action list before "go public"

1. [x] Paraphrase/shorten the verbatim Description sections (done).
2. [x] Update `LICENSE` (CC0 + CC BY-4.0 for Electropedia parts).
3. [ ] Quick grep check — expect only title-level mentions:
   `grep -rn "flameproof enclosure\|vacuum cleaners\|water-suction" --include=*.md standards/` (IEC-60079-1:2026 title contains "flameproof enclosure"; IECEE TRF scope contains "vacuum cleaners").
4. [ ] Optional: contact IEC per AGB for written permission (webstore data/AI use) — reduces risk; link in this file.
5. [ ] User decision: flip repo private → public (`gh repo edit mfahsold/iec-standards-obsidian-vault --visibility public`).
6. [ ] Update this file after actions (status).

## Risk notes (honest)

- IEC AGBs: "You shall not copy... from IEC Products, or any portion thereof, without permission in writing from IEC" — paraphrased descriptions mitigate the main risk.
- Prices are dynamic ("For prices, see current catalogue") — marked "as of Crawl-Date".
- IEC assigns titles/IDs — factual; aggregators (normfile.com, bsbedge.com) resell IEC standard lists — precedent exists.

## MASTER
