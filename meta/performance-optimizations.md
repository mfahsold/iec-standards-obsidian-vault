# Performance-Optimierungen (neueste Erkenntnisse, 2026-11-20)

## Obsidian-Performance (2025-2026)

- **Obsidian 1.8.9+:** „introduces crucial performance optimizations and stability improvements, particularly benefiting users with large vaults“ (baizaar.tools — Obsidian 1.8.9 Update).
- **Lazy-Cached Vault Load (GitHub):** `d7sd6u/obsidian-lazy-cached-vault-load` — „Do you have a big vault (3k+ files)? Have you tried to open it in mobile Obsidian and it takes forever?“ — lazy-cached loading (Größen-Hinweis: Vault mit ~50 Dateien ist klein — Optimierung noch unproblematisch).
- **Performance-Tuning-Toolkit (10k+ Dateien):** „obsidian-performance-tuning — practical toolkit for tuning Obsidian plugin performance in large vaults“ (lobehub — Claude Code Plugins).
- **Obsidian Cost Tuning:** „Optimize Obsidian Sync storage, Publish bandwidth, and plugin API costs with caching and quotas“ (mcpmarket — obsidian-cost-tuning).
- **Power users (10k+ Dateien):** „What breaks first when your Obsidian vault gets big? — researching a local-first Rust engine API for large markdown/Obsidian vaults, focused only on faster indexing/search/retrieval“ (reddit — zukünftige Erweiterungsmöglichkeit).

## Dataview-Performance (2026)

- **Dataview 0.4.16+ (aktuell):** „Small performance release which substantially reduces the impact Dataview has on vault loading times (by spreading out file loading). The Dataview Index is now also eagerly initialized“ (Dataview Changelog — blacksmithgu.github.io).
- **Voll-Vault-Scan vermeiden:** Queries ohne `FROM`-Klausel oder mit sehr breitem `FROM` zwingen Dataview zum Vault-Scan (PKM Insights). Unser Design: `FROM "standards"` — präzise — Optimierungsbogenhaltung beibehalten.
- **Queries cachen:** „Persist the cache to improve startup performance — Instead of rebuilding the cache at each startup, persist the cache. Dataview can render from the cache“ (obsidian-dataview Issue #1064) — Erweiterungswürdigkeit.
- **Kleine Queries, Fokus:** „Dataview is faster with only images“ (reddit); „The most common cause of Dataview lag ... is the dreaded full-vault scan“ — Restriktionen: `LIMIT`, präzise `SORT`-Felder, `GROUP BY`.
- **Serializer-Perf:** `dsebastien/obsidian-dataview-serializer`: „Optimize the Obsidian Dataview Serializer plugin's query processing performance through caching, parallel processing, and regex compilation improvements.“

## Obsidian-LLM-Integration (2026)

- **Local LLM Helper** (community plugin — versucht installiert+aktiviert — „integrates local Large Language Models (LLMs) with Obsidian, offering a suite of tools for text processing, interactive AI chat, ..."): die offizielle Obsidian-Nutzungserfahrung für lokale LLMs. „There is no Local LLM Helper cloud service: requests go only to chat and embedding endpoints you configure.“
- **Andere (verifiziert):** Local GPT (pfrankov) — „Obsidian + Ollama: 5 Local LLM Plugins for Your Vault (2026)“; Smart Connections (semantic search), Copilot (chat with vault), Text Generator (AI writing).
- **XDA-Artikel:** „I fed my entire Obsidian vault into a local LLM, and now it actually understands my research“ (2026) — Filesystem-Server → lokaler LLM.
- **Plugin-Kosten:** obsidian-cost-tuning — caching/quotas (Sync, Publish).

## Einsatz in diesem Vault

- L2/L3 des Agent-Loops = **Context-Minimierung** (nur index.json-Strukturdaten; L3 + Backlinks) — immer relevant für lokale Tiny-Modelle (qwen3.5:0.8b).
- Obsidian: nur aktivierte Plugins (dataview, obsidian-git, templates, graph, properties, switcher, …) — Perf-Prinzip: Deaktivierungen, was nicht genutzt wird.
- Dataview-Queries (meta/dataview.md): `FROM "standards"` (präzise) + kleine Queries — Optimierungsrichtung; 0.4.16+ Features (eager index) zukünftig nutzbar.

## MASTER

→ [meta/agent-loop.sh](agent-loop.sh), [meta/dataview.md](dataview.md), [README.md](../README.md).
