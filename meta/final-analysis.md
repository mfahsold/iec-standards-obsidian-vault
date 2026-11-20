# Fresh Analysis — IEC-Vault (Stand 2026-11-20) — Frisch/Compressed

## Current State (one view)

- **Repo:** mfahsold/iec-standards-obsidian-vault — private — 67 files (61 Markdown), `main` pushed — documentation in English.
- **Stack (minimal, verified 2026-11-20):** Obsidian 1.15.1 (GUI vault = parent `IEC_Agentic/`, repo = subfolder) + Local LLM Helper 2.6.2 + Ollama 0.40.15 — chat `qwen3.5:2b` (3.1 GB, thinking), embeddings `nomic-embed-text` (274 MB, 768 dims, 241 chunks) + Dataview + `agent-loop.sh` v6 (L1/L2/L3) — [meta/agent-loop.sh](agent-loop.sh), [meta/chat-optimization.md](chat-optimization.md)
- **Data:** 23 Standards (18 Notes + classics + 5 new: IEC 61643-11:2025/COR1:2026, IEC 60364-1:2025, IEC 62813:2025/COR1:2026, IEC 60286-1/AMD2:2026, ISO 14678:2005) + Glossar — [meta/glossary.md](glossary.md)

## Analysten (Kritik — Verkettung)

- **SLOW:** „Too Bureaucratic and Slow“ — means nothing for new VSs on the premise of IEC — [meta/iec-criticism.md](iec-criticism.md)
- **85% Dominanz:** „ISO and IEC — 85% of all international product standards“ — [meta/standards-bodies.md](standards-bodies.md)
- **Private SDO:** „two largest SDOs with global reach, the ISO and IEC“ — [meta/standards-bodies.md](standards-bodies.md)

## Optimierungen (implementiert)

- System-Prompts (agent-loop v4 — Kritik-Integration) — [meta/agent-loop.sh](agent-loop.sh)
- Dataview-Optimierungen — [meta/dataview.md](dataview.md)
- Glossar/structure — [meta/glossary.md](glossary.md)

## Status / nächste Schritte (2026-11-20)

1. **Chat GUI: verified** — general chat is ungrounded; **RAG chat** (`rag-chat`) retrieved the correct note as top-1 (IEC-62813-2025-COR1-2026, score 0.767) and answered ICS 31.060.99 with `qwen3.5:2b`. Settings fixed in the **GUI vault's** `data.json` (2b + nomic-embed-text + maxTokens 4096); RAG index rebuilt — [meta/chat-optimization.md](chat-optimization.md).
2. **`agent-loop.sh` v6:** all golden questions pass on L1/L2 (ICS 31.060.99, 335 CHF, definition).
3. **Governance:** [meta/project-charter.md](project-charter.md) — vision, scope, question taxonomy, definition of done.
4. Optional/open: Q8 product-concept workflow; deeper research on engineer question taxonomy; L3 multi-note stress test.

## MASTER
