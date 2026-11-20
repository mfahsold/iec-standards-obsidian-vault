# Chat-Optimierungen — Local LLM Helper + Ollama (2026-11-20)

## Stack (minimal)

- **Chat:** `local-llm-helper` v2.6.2 (Community-Plugin, Obsidian GUI).
- **LLM:** `qwen3.5:2b` (Ollama 0.40.15, Server http://localhost:11434; capabilities: completion, vision, thinking, tools — per `api/tags` — „The small qwen3.5 models just dropped" — 2b ~1.5 GB — eher Qualität als 0.8b).
- **Settings (Obsidian → Settings → Community Plugins → Local LLM Helper):**
  - Endpoint: `http://localhost:11434` (Ollama-Native-API — verifiziert: `/api/version` → 0.40.15).
  - Model: `qwen3.5:2b` (genau wie in `api/tags` gelistet — string-equal).
  - Temperature: 0.3–0.6 (kurze, präzise IEC-Fakten-Antworten).
  - Context Window (num_ctx): **16384** (vorgeschlagen — Phase N: „deutlich größeres Kontextfenster" — GUI: 0.8b-Notiz → 2b: Settings → Local LLM Helper → Context Window —EMP: 8192–16384 verwertbar; 16384 = maximal „available" bei diesem Host).
  - **Data-File:** `$V/.obsidian/plugins/local-llm-helper/data.json` (Batch N2a — aktualisiert: llmModel=`qwen3.5:2b`, endpoint, num_ctx=16384, temperature, maxTokens) — GUI-Pfad, falls GUI-Entry-Point geändert (Sandboxed-Plugin).
  - **Thinking:** Standard ON (Qwen3.5 — „mehr Thinking“ — Chunk N1 —beobachtet: Thinking + Content im Streaming-Response (Ollama 0.40 — `message.thinking`/`message.content`).
  - System-Prompt (empfohlen): „Du bist der Obsidian-Agent für den IEC-Standards-Vault. Antworte kurz und strukturiert: Fakten + Quellen-URLs (sources). Antworte auf ICS-Fragen mit den ICS-Werten aus `index/index.json` (z. B. IEC 62813:2025/COR1:2026 → ICS 31.060.99). Antworte bei Preisfragen mit `price_chf` aus `index/index.json` (z. B. IEC 62443-4-1:2018 → 335 CHF — „For prices, see current catalogue"; freie IEC-Standards gibt es nicht).“

## Wie das Modell Daten abruft und verarbeitet (aktuell)

- **Retrieval (CLI/agent-loop):** `obsidian search` (lexikalisch) → NOTE → `obsidian read` → Note-Body (frontmatter + Inhalt — kurz, <500 Token) → `ollama run qwen3.5:2b <Prompt>` → Antwort.
  - L2 (structured): `python3` Filter+Sort auf `index/index.json` (context-minimal) — [agent-loop.sh L2].
- **Chat (GUI — Local LLM Helper):** Benutzerfrage + Plugin-Settings → `http://localhost:11434` → Modell `qwen3.5:2b` (Settings — [chat-optimization.md](chat-optimization.md)) → Antwort (Streaming, „Thinking“-Phase — intern — 2b outputs visible-internal-Analysis).
- **Verarbeitung (Modell):** Input = System-Prompt + Frage + Context (Vault klein — ≤100 Files) — kurze Note-Bodies → direkte Antwort.

## Optimierungen (Diskussion + Implementiert)

1. **Agent-Loop Prompt v4** (implementiert — [meta/agent-loop.sh](agent-loop.sh)): System-Prompt — „kurz und strukturiert (2–3 Sätze): Fakten + Quellen-URLs (sources). Keine Übertragung von Standardtexten außerhalb der Daten. Nenne bei IEC-Kritik/Mustern (meta/iec-criticism.md): SLOW/Bureaucracy, 85%-Dominanz, Private SDO, Strategic Competition (ISO/IEC), Slow-Pattern — bei Kritik-Fragen: Kurz-Argument + Alternative (ANSI/ISO/ITU/Webstore-Preise, voluntary adoption)".
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
