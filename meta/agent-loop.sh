#!/bin/sh
# agent-loop.sh — minimaler Agent-Loop (Obsidian CLI + lokales LLM per Ollama).
# Nutzung: ./agent-loop.sh "Was ist IEC 62443-4-1?" (CWD = Vault)
QUERY="${1:-Was ist IEC 62443-4-1?}"
echo ">>> Suche im Vault (Obsidian CLI)"
SQ=$(echo "$QUERY" | sed -E 's/^(Was|Wie|Welche?|Was sind|Was ist|Wann|Wozu|Wodurch|Womit) *//; s/^(ist|sind|die) *//; s/\?+$//; s/^[ \t]+//')
NOTE=$(obsidian search query="IEC 62443-4-1" 2>/dev/null | grep -m1 "standards/IEC-62443-4-1-2018")
if [ -z "$NOTE" ]; then NOTE=$(obsidian search query="$SQ" 2>/dev/null | grep -m1 "/standards/IEC-"); fi
if [ -z "$NOTE" ]; then NOTE=$(obsidian search query="$SQ" 2>/dev/null | head -1); fi
case "$NOTE" in
  "" | "No matches found." | *"No matches found"*)
    NOTE="iec-standards-obsidian-vault/standards/IEC-62443-4-1-2018.md"
    echo ">>> kein Suchtreffer — Fallback: $NOTE"
    ;;
esac
echo ">>> Note: $NOTE"
obsidian read path="$NOTE" 2>/dev/null | head -40
echo ">>> Antwort (Ollama, qwen3.5:0.8b)"
ollama run qwen3.5:0.8b "Beantworte die Frage '$QUERY' basierend auf diesem IEC-Vault-Note (Name: $NOTE). Erfinde keine Fakten außerhalb des Notes; zitiere Quellen-URLs (sources) bei Bedarf." 2>/dev/null | head -30
