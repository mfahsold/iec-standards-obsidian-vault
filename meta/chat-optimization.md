# Chat-Optimierungen — Local LLM Helper + Ollama (2026-11-20)

## Stack (minimal)

- **Chat:** `local-llm-helper` v2.6.2 (Community-Plugin, Obsidian GUI).
- **LLM:** `qwen3.5:0.8b` (Ollama 0.40.15, Server http://localhost:11434; capabilities: completion, vision, thinking, tools — per `api/tags`).
- **Settings (Obsidian → Settings → Community Plugins → Local LLM Helper):**
  - Endpoint: `http://localhost:11434` (Ollama-Native-API — verifiziert: `/api/version` → 0.40.15).
  - Model: `qwen3.5:0.8b` (genau wie in `api/tags` gelistet — string-equal — „The configured model was not found“-Fehler wenn falsch).
  - Temperature: 0.3–0.6 (kurze, präzise IEC-Fakten-Antworten).
  - Context Window (num_ctx): 4096 (Vault klein — ≤100 Files; größer, wenn Analyse stattfindet).
  - System-Prompt (empfohlen): „Du bist der Obsidian-Agent für den IEC-Standards-Vault. Antworte kurz und strukturiert: Fakten + Quellen-URLs (sources).“

## Wie das Modell Daten abruft und verarbeitet (aktuell)

- **Retrieval (CLI/agent-loop):** `obsidian search` (lexikalisch) → NOTE → `obsidian read` → Note-Body (frontmatter + Inhalt — kurz, <500 Token) → `ollama run qwen3.5:0.8b <Prompt>` → Antwort.
  - L2 (structured): `python3` Filter+Sort auf `index/index.json` (context-minimal) — [agent-loop.sh L2].
- **Chat (GUI — Local LLM Helper):** Benutzerfrage + Plugin-Settings → `http://localhost:11434` → Modell `qwen3.5:0.8b` → Antwort (Streaming, explizite „Thinking“-Phase).
- **Verarbeitung (Modell):** Input = System-Prompt + Frage + Context (Vault klein — ≤100 Files) — kurze Note-Bodies → direkte Antwort.

## Optimierungen (Diskussion + Implementiert)

1. **Agent-Loop Prompt v3** (implementiert — [meta/agent-loop.sh](agent-loop.sh)): Geänderter System-Prompt — „kurz und strukturiert (2–3 Sätze): Fakten + Quellen-URLs (sources). Keine Übertragung von Standardtexten außerhalb der Daten.“ — Fokus: Output-Qualität für IEC-Fakten.
2. **Chat-Settings + Optimierungsanalyse** (dokumentiert — dieser File): System-Prompt, Temperature, num_ctx, Endpoint/Model — GUI-Settings.

## Diskussionsliste (mit dir)

1. **Suche:** lexikalisch (Obsidian Search) vs. semantisch (Embeddings — z. B. `all-minilm` via Ollama — IEC-Retrieval)? — bei ~20 Standards reicht lexikalisch — Embedding-Wert bei Skalierung.
2. **Retrieval:** L3 (Multi-Note-Read) — [agent-loop.sh -l 3] ready — wann geben? (komplexe IEC-Fragen).
3. **Modell:** `qwen3.5:0.8b` (schnell) vs. `qwen3.5:2b/9b/27b` (präziser — bei 2.7–7.6 GB / 17–20 GB RAM — bei M2 Pro Passung)?
4. **Chat-GUI vs. CLI-Loop:** Redundanz reduzieren (einen Weg für interactive vs. automatisierte) — Chat für interactive, CLI für Automatisierung?
5. **Hardcoding-Reduktion:** Fallback-Note `IEC-62443-4-1-2018` hardgecodet — dynamisieren (`obsidian search` + Sort-Fallback)?
6. **Zukunft:** Semantische Suche (Embedding-Model in index.json → mdp embedding) — erst mit IEC-Zugang.

## MASTER

→ [meta/agent-loop.sh](agent-loop.sh), [meta/obsidian-usage.md](obsidian-usage.md), [meta/ui-optimization.md](ui-optimization.md).
