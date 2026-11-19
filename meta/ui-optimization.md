# Optimierte Obsidian-UI — der IEC-Standards-Vault (Schlanke Form)

Stand: 2026-11-20 — „Nur notwendigste“: **Chat (Local LLM Helper v2.6.2)** + **Obsidian-Retrieval (Obsidian Search/CLI)** + **optimierte UI** — reduziert: dataview, obsidian-git, obsidian-local-rest-api entfernt (nicht notwendig).

## UI-Optimierung (2026-11-20)

- **Vault-Struktur als UI:** Obsidian-natives Layout — MOC-Hub `index/index.md` (Master Index & MOC — Erster Einstieg), `README.md` (Vault Home), `standards/` (18 Notes + classics), `processes/` (13), `electropedia/`, `guides/`, `news/`, `index/`, `meta/`, `templates/`.
- **Hotkeys (verifiziert per `obsidian hotkeys`):** `app:open-vault`, `app:toggle-left-sidebar`, Quick Switcher (`switcher` — Ctrl/Cmd+O), Global Search (`global-search` — Ctrl+Shift+F) — Clicken auf Notes → Backlinks.
- **Panel-Nutzung:** Backlinks (rechter Sidebar), Outgoing Links, Properties (Frontmatter — `obsidian properties` — verifiziert), Outline.
- **Graph (core):** aktiv — farbindexierte Clustern (Standards ↔ Prozesse ↔ Meta).

## Entfernte Plugins (nicht notwendig für Chat/Retrieval/UI)

- `dataview` (Queries — Komplexität — weg).
- `obsidian-git` (Repo-Versionierung — Repo ist privat, ohne Obsidian-GUI-Needed).
- `obsidian-local-rest-api` (REST-Interface — superseded by Obsidian CLI + Local LLM Helper; Port 27124 schließt).

## Chat-Einrichtung (Local LLM Helper)

- Plugin: `local-llm-helper` v2.6.2 — Community-Plugin („integrates local LLMs with Obsidian, text processing, interactive AI chat, ...").
- „There is no Local LLM Helper cloud service: requests go only to chat and embedding endpoints you configure.“ — Chat mit **Ollama** (http://localhost:11434 — läuft), Modell **qwen3.5:0.8b** (1.2 GB — neuestes Tiny).
- GUI: Obsidian → Community-Plugins → Local LLM Helper → Settings → Endpoints → `http://localhost:11434` (Ollama).
- Changelog: [meta/performance-optimizations.md](performance-optimizations.md).

## Retrieval-Einrichtung (Obsidian-Native)

- **Obsidian Search:** `obsidian search query="IEC 62443-4-1"` (CLI) / GUI — UI-Suche in Obsidian — [standards/IEC-62443-4-1-2018.md](../standards/IEC-62443-4-1-2018.md).
- **Agent-Loop (CLI):** `./meta/agent-loop.sh "Was ist IEC 62443-4-1?"` — L1/L2 — Retrieval via Obsidian CLI + Ollama (oben getestet).

## MASTER

→ [README.md](../README.md), [meta/agent-loop.sh](agent-loop.sh).
