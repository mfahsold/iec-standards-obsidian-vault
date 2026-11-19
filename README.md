# IEC Standards Obsidian Vault (Prototyp)

Vault mit öffentlich verfügbaren IEC-Informationen, angelegt für Obsidian und für LLM/Agent-Nutzung optimiert.

> **Status: Prototyp, Datenstand 2026-11-19** – Das Repo ist noch **privat** (lokal, kein Push). Zum Public-Setup siehe `meta/licensing.md`.

## Was in diesem Vault enthalten ist

- **`standards/` – Katalog von IEC-Produkten** mit Metadaten: Referenz (z. B. `IEC 62443-4-1:2018`), Typ (IS/TS/TR/PAS/…), Technischer Bereich, Technischer Ausschuss, Editionsdatum, Preis (CHF), Sprachen und Quelllinks. Enthält **keine Volltexte** der IEC-Dokumente (Urheberrecht IEC – siehe `LICENSE`, `meta/licensing.md`); für 18 abgedeckte Produkte auch kurze Beschreibungen, die aus den öffentlichen Webstore-Seiten stammen.
- **`processes/` – IEC-Prozesse und -Typen**: IS-Definition (abgeschlossene Definition, Consensus, Public Enquiry, Approval, voluntary adoption), TS- und PAS-Definitionen (TS, PAS, Workflows IS/TS/TR/ISH/PAS/IEV), Entwicklungsabfolge (PWI → NP → WD → CD → CDV → FDIS → IS), Workprogramm von TC/SC, AGB/AGBs, Affiliate-Programm, Online-Standards-Development (OSD), Directives (öffentliche PDFs).
- **`electropedia/` – IEV Online**: IEC 60050-Vokabular, kostenlos, mehrsprachig, offizielle Nutzungsbedingungen.
- **`guides/` – IEC Guides** (GUIDE 103, 104, 107, 108, 109, …).
- **`news/` – Free-Newsletter „IEC Just Published“** (jeden 1. des Monats, 12×/Jahr).
- **`index/` – Master-Index**: `index.md` (lesbar), `index.json` (für Agents).
- **`meta/` – Quellen, Lizenzierung, Erfassungs-/Staleness-Hinweise**.

## LLM-/Agent-Optimierung

- Atomare Notes mit YAML-Frontmatter (`ref`, `type`, `edition`, `technical_committee`, `status`, `price_chf`, `sources[]`, …).
- `index/index.json` – maschinenlesbarer Index (Referenzen, ICS/TC, Status, Links) – direkt für Search/Retrieval/Tools nutzbar.
- Kurze „Scope“-Bloecks pro Standard (Was deckt das Standard ab? falls bekannt).
- Keine IEC-Volltexte (Urheberrecht), aber klare, kurze, facts-based Zusammenfassungen + offizielle Links.

## Umfang („alle öffentlich verfügbaren IEC-Standards“)

- „All products“ im IEC Webstore: https://webstore.iec.ch/en/products/ (incl. „Just Published“, „Bestsellers“, „Products by technical area“).
- IEC Library Server (Login): https://library.iec.ch/ – Vollkatalog (alle IEC-Publikationen incl. „Replaced / Withdrawn“) für Mitglieder/Apointiesten.
- Third-party Aggregatoren: https://www.normfile.com/iec.html, https://www.bsbedge.com/free-downloads/international-electrotechnical-commission/ – sehr große Kataloge aus fremden Listen (Referenzen).
- Das Vault enthält derzeit **verifizierte Daten von offiziellen Webstore-Seiten + Classic-Sets** (≈20 abgedeckte Produkte). Für den vollständigen Katalog muss IEC-Webstore „All products“ eingelesen werden (mit schriftlicher Erlaubnis von IEC – siehe `meta/licensing.md`).

## Verwendung in Obsidian

- Vault-Ordner öffnen (`iec-standards-obsidian-vault/`).
- Backlinks/Graph anschauen; Standard-Notes verlinken auf die Webstore-Produktseiten (Click zum Lesen bei Abonnement).
- Erweiterungsvorschlag für später: `obsidian-mcp-tools` / Dataview-Indizes für API-Exposure.

## Datenstand & Aktualisierung

- 2026-11-19: Daten aus offiziellen Webstore-/IEC-Seiten abgerufen (manuell, Browser).
- Preise und Publikationsdaten werden „aktuell“ gemarkt; Details in `meta/crawl-notes.md`.
