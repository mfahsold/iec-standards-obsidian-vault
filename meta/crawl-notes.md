# Erfassungs- und Staleness-Hinweise (Crawl-Log)

Stand: 2026-11-19 — manuell recherchiert (Browser; offizielle Webseiten).

## Verfahren

- **Kein automatisierter Crawl des IEC Webstores**: die IEC Webstore AGBs (vgl. `meta/licensing.md`) verbieten „data mining or scraping IEC Products without express written permission by IEC“.
- Datenquellen: offizielle Webstore-Produktseiten, offizielle IEC-Seiten (Produkt-Übersichten/FAQ/Definitionen), IEC Open-PDFs (Directives), Elektropedia (kostenlos), third-party Aggregatoren (normfile.com, bsbedge.com) — Referenzen/Titel für classics.

## Verifizierte Produkte im Vault (18)

| Nr | Referenz | Typ | TC | Preis CHF | Quellen |
| --- | --- | --- | --- | --- | --- |
| 1 | IEC 62443-4-1:2018 | IS | 65 | 335 | webstore/33615, bestsellers |
| 2 | IEC 62443-4-2:2019 | IS | 65 | 405 | webstore/34421, bestsellers |
| 3 | IEC 62443-3-3:2013 | IS | 65 | 380 | webstore/7033, bestsellers |
| 4 | IEC 60079-1:2026 | IS | 31 | 430 | webstore/71515, just-published |
| 5 | IEC 61675-2:2026 | IS | 62 | 380 | webstore/85053, just-published |
| 6 | IEC 61675-2:2026 RLV | IS | 62 | 646 | webstore/117958 |
| 7 | IEC 61800-9-1:2026 RLV | IS | — | — | webstore/117763 (Preis nicht verifiziert) |
| 8 | ISO/IEC 25791-2:2026 | ISO/IEC | — | 135 | webstore/117975 |
| 9 | IECEE TRF 60335-2-2O:2026 | TRF | — | 1600 | webstore/117974 |
| 10 | IEC PAS 62443-2-2:2025 | PAS | 65 | 295 | webstore/63886 |
| 11 | IEC PAS 63441:2022 | PAS | — | 260 | webstore/75170 |
| 12 | CISPR PAS 38:2025 | PAS | — | 115 | webstore/67222 |
| 13 | IEC TR 63650:2026 | TR | 40 | 260 | webstore/106458 |
| 14 | IEC TR 61869-103:2012 | TR | 38 | 380 | webstore/6049 |
| 15 | IEC TR 62476:2010 | TR | 111 | 115 | webstore/7079 |
| 16 | IEC TR 60919-1:2020 RLV | TR | 22/SC 22F | 689 | webstore/66917 |
| 17 | IEC TR 63411:2025 | TR | 8/SC 8A | 380 | webstore/66463 |
| 18 | IEC TR 62380 | TR | — | — | normservis.cz (mirror, © IEC 2004) |

## Classics (Third-Party-Aggregator)

7 Produkte aus https://www.normfile.com/iec.html (CSV-Listen; Referenzen/Titel, keine rekonstruierten Preise/Details):

- IEC 60335-2-76-2002+AMD1-2006
- IEC 60601-2-66-2015
- IEC 60748-1-1984+AMD2-1993
- IEC 60335-2-54-2002+AMD1-2004
- IEC 60335-2-10-2002
- IEC 60794-3-20-2009
- IEC 60614-2-6-1992

## Preisnoten

- Preise „as of Crawl-Date“; Preise werden dynamisch — „For prices, see current catalogue“ (webstore/bestsellers/just-published).
- RLV = Redline Version („Redline version (RLV)“ — official standard + redline).
- ISO/IEC 25791-2:2026 ist ein **ISO/IEC**-Standard (TDB 1 JTC 1) — in vault zusammengefasst unter standards/.

## Links

- [meta/licensing.md](licensing.md) — AGBs & rules (no scraping, no AI use of IEC products, affiliate).
- [meta/iec-structure.md](iec-structure.md) — TC/SC, ICS, SDG anchors, statuses, sorting.
- [meta/sources.md](sources.md) — all used URLs + origin.
- [standards/index-standards.md](../standards/index-standards.md) — catalog of vault standards (wikilinks).
- [meta/obsidian-usage.md](obsidian-usage.md), [meta/dataview.md](dataview.md), [meta/obsidian-cli.md](obsidian-cli.md).

## Updates

```
./iec-standards-obsidian-vault/meta/crawl-notes.md — letzter Crawl: 2026-11-19
```
