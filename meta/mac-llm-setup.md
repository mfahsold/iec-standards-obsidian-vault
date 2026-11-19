# Mac + Ollama / LM Studio — Setup 2026 — Expert (Job)

Stand: 2026-11-20 — Expert-Referenz (Promptquorum/Starmorph/Llmhardware/Medium/Dev.to).

## Apps (M-Series, macOS 14+)

- **LM Studio** — „Best Local LLM Apps for Mac in 2026: LM Studio, Ollama, Jan and 5 More — LM Studio (free, Apple Silicon, macOS 14+)“.
- **Ollama** — „Fastest path to running local LLMs (one command to install, one to run)“ — „the terminal, LM Studio — visuals“ (Starmorph).
- **MLX** — Apple Silicon native — `mlx-lm serve` — for bigger models (Qwen 3.8/3.6 — „Ollama runs Qwen 3.8, Qwen 3.6, Qwen 3.5 and Gemma 4 on MLX by default“).

## Quick Takeaway (Job — Performance-Config)

- Memory Allocation — set max RAM from available memory.
- Thread Count — CPU cores.
- Model Storage Path.

## Setup (M2 Pro — Ollama, 2026)

1. `brew install --cask ollama` (App + CLI — /opt/homebrew/bin/ollama).
2. `ollama pull qwen3.5:0.8b` (M2 Pro — 1.2 GB — oder qwen3.5:2b/9b — für mehr Qualität).
3. Server: `http://localhost:11434` (verifiziert: `curl -s http://localhost:11434/api/version` → 0.40.15).
4. Optional: `ollama pull lfm3` (LiquidAI LFM3-1.7B — „Small models built to run anywhere“).

## Job-Erkenntnisse (Patterns)

- 0.8B — „suggestion to download Ollama … probably the 0.8b if it actually works reasonably well“ (Reddit r/LocalLLaMA — Breaking — Qwen3.5 small models).
- 2B (turintech artemis) — „Ollama Recommendation — Qwen3.5 from 0.8B to 9B, in smaller files“.
- Qwen3.5 small models: 0.8b ~500MB, 2b ~1.5GB — „Small models (run on almost anything)“ (Substack).
- CedarModel routing — mention.

## MASTER

→ [meta/chat-optimization.md](chat-optimization.md).
