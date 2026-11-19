# Glossar — Fachbegriffe (untereinander verknüpft)

Stand: 2026-11-20 — Fachbegriffe als Knoten, verknüpft per **Wikilinks (Obsidian)**, **Tags (Frontmatter)**, **ICS** und **Dataview-Queries** (mathematische Optimierung — [meta/dataview.md](dataview.md)).

## Standard-Typen (Kernbegriffe)

- **IS — International Standard** — [Processes/IS](processes/international-standards.md) — Long-form Standards (Normative, Consensus). Beispiele: [IEC 62443-4-1:2018](standards/IEC-62443-4-1-2018.md).
- **TS — Technical Specification** — nah am IS, kürzer, 2/3-Mehrheit — [processes/specifications.md](processes/specifications.md).
- **PAS — Publicly Available Specification** — „Publicly Available“ = Dokumententyp (nicht Vertriebsweg!) — [processes/publicly-available-specifications.md](processes/publicly-available-specifications.md) — Beispiele: [IEC PAS 62443-2-2](standards/IEC-PAS-62443-2-2-2025.md), [IEC PAS 63441](standards/IEC-PAS-63441-2022.md).
- **TR — Technical Report** — „Entirely informative, not normative“ — [processes/technical-reports.md](processes/technical-reports.md) — Beispiele: [IEC TR 63650](standards/IEC-TR-63650-2026.md), [IEC TR 61869-103](standards/IEC-TR-61869-103-2012.md), [IEC TR 60919-1 RLV](standards/IEC-TR-60919-1-2020-RLV.md).
- **TRF — Test Report Form (IECEE)** — [standards/IECEE-TRF-60335-2-2O-2026](standards/IECEE-TRF-60335-2-2O-2026.md).
- **AMD2 / COR1 / PRV (Standard-Historie)** — Neue Stände 2026: [IEC 62813:2025/COR1:2026 (AMD2-class)](standards/IEC-62813-2025-COR1-2026.md), [IEC 61643-11:2025/COR1:2026](standards/IEC-61643-11-2025-COR1-2026.md), [ISO 14678:2005](standards/ISO-14678-2005.md).

## IEC-Prozesse (verknüpft)

- **Consensus (2/3 P-Member, <25% negative)** — [processes/international-standards.md](processes/international-standards.md) — [Sicherheits-Standards (TC 65)](index/index.md#standards-in-this-vault-full-list-clickable).
- **Public Enquiry** — [processes/international-standards.md](processes/international-standards.md).
- **Voluntary adoption** — [processes/international-standards.md](processes/international-standards.md).
- **Stages (PWI → NP → WD → CD → CDV → FDIS → APUB → PPUB)** — [processes/development-stages.md](processes/development-stages.md).
- **SMB (Technical Management Board)** — [processes/work-programme.md](processes/work-programme.md) — [Guides-Anwender (ACOS/ACEC/ACEA)](guides/guides.md).
- **MTG — IEC Maintenance** — [guides/guides.md](guides/guides.md).

## ICS-Zerlegungsstufen (IEC ICS)

- **ICS 2** — Industrielle Standards — [Standards im Vault](index/index.md).
- **ICS 31** — Safety — [IEC 61675-2:2026](standards/IEC-61675-2-2026.md), [IEC TR 63650:2026](standards/IEC-TR-63650-2026.md).
- **ICS 33.100.10** — EMC — [CISPR PAS 38:2025](standards/CISPR-PAS-38-2025.md).
- **ICS 29.200** — Power — [IEC TR 60919-1:2020 (RLV)](standards/IEC-TR-60919-1-2020-RLV.md).
- **ICS 27.180** — Renewable — [IEC TR 63411:2025](standards/IEC-TR-63411-2025.md).
- **ICS 13.020.01 / 43.040.10** — Environment — [IEC TR 62476:2010](standards/IEC-TR-62476-2010.md).
- **ICS 17.220.20** — Instrument Transformers — [IEC TR 61869-103:2012](standards/IEC-TR-61869-103-2012.md).
- **ICS 31.060.99** — Electrochemical — [IEC 62813:2025/COR1:2026](standards/IEC-62813-2025-COR1-2026.md).

## SDG-Anker (Sustainable Development Goals — von Produktseiten)

- **SDG 03** — [Standards mit SDG03](index/index.md): [IEC 61675-2:2026](standards/IEC-61675-2-2026.md), [IEC 60079-1:2026](standards/IEC-60079-1-2026.md).
- **SDG 07** — [IEC 62443-4-1:2018](standards/IEC-62443-4-1-2018.md) etc. — Dataview-Query: `FROM "standards" WHERE contains(tags, "SDG07")` — [meta/dataview.md](dataview.md).

## Netzwerk (GL1: GL2 → GLn)

- ICS → Standards: s. Obers (Dataview GROUP BY ics — [meta/dataview.md](dataview.md)).
- TC/SC → Standards: [TC-65 Standards](index/index.md) — [TC-40 Standards](standards/IEC-TR-63650-2026.md).
- Chat (GUI): Local LLM Helper (v2.6.2) — [meta/chat-optimization.md](meta/chat-optimization.md).
- Retrieval (CLI): Obsidian Search — [meta/agent-loop.sh](agent-loop.sh).

## MASTER
