#!/bin/sh
# agent-loop.sh — Minimaler Agent-Loop: Obsidian CLI liest die Note aus, lokales LLM (Ollama) antwortet.
# Nutzung: ./agent-loop.sh "Was ist IEC 62443-4-1?"   (CWD = Vault)
QUERY="${1:-Was ist IEC 62443-4-1?}"
echo ">>> Suche im Vault (Obsidian CLI)"
NOTE=$(obsidian search query="$QUERY" 2>/dev/null | head -1)
if [ -z "$NOTE" ]; then
  NOTE="iec-standards-obsidian-vault/standards/IEC-62443-4-1-2018.md"
  echo ">>> kein Suchtreffer — Fallback: $NOTE"
fi
echo ">>> Note: $NOTE"
obsidian read path="$NOTE" 2>/dev/null | head -40
echo ">>> Antwort (Ollama, qwen2.5:0.5b)"
ollama run qwen3.5:0.8b "Beantworte die Frage '$QUERY' basierend auf diesem IEC-Vault-Note (Name: $NOTE). Erfinde keine Fakten außerhalb des Notes; zitiere Quellen-URLs (sources) bei Bedarf." 2>/dev/null | head -30
