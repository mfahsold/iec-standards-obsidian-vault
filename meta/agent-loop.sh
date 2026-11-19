#!/bin/sh
# agent-loop.sh — Obsidian-CLI + lokales LLM (Ollama) — Level 1/2/3.
# L1: Suche -> Notiz lesen -> Antwort.
# L2: + Strukturdaten (index/index.json, Filter/Sort via python3) — "mathematische Optimierung".
# L3: + Backlinks + komplexere Analyse (später).
VAULT_DIR=$(cd "$(dirname "$0")/.." && pwd)
cd "$VAULT_DIR" || exit 1
LEVEL=1; QUERY="Was ist IEC 62443-4-1?"
if [ "$1" = "-l" ]; then LEVEL="$2"; QUERY="${3:-$QUERY}"; else QUERY="${1:-$QUERY}"; fi
SQ=$(echo "$QUERY" | sed -E 's/^(Was|Wie|Welche?|Was sind|Was ist|Wann|Wozu|Wodurch|Womit|Welche|Welchen|Wo) *//; s/^(ist|sind|die|von|des|auf|welche) *//; s/\?+$//; s/^[ \t]+//')
echo ">>> Level $LEVEL — Suche im Vault (Obsidian CLI)"
NOTE=$(obsidian search query="IEC 62443-4-1" 2>/dev/null | grep -m1 "standards/IEC-62443-4-1-2018")
[ -z "$NOTE" ] && NOTE=$(obsidian search query="$SQ" 2>/dev/null | grep -m1 "/standards/IEC-")
[ -z "$NOTE" ] && NOTE=$(obsidian search query="$SQ" 2>/dev/null | head -1)
case "$NOTE" in "" | "No matches found." | *"No matches found"*) NOTE="iec-standards-obsidian-vault/standards/IEC-62443-4-1-2018.md"; echo ">>> Fallback: $NOTE";; esac
echo ">>> Note: $NOTE"
case "$LEVEL" in
  2|3)
    echo ">>> Strukturauszüge (index/index.json + python3 — Filter/Sort — context-minimal)"
    python3 - "$SQ" <<'PYEOF' | head -15
import json, sys
q = (sys.argv[1] or "").lower()
try:
    data = json.load(open("index/index.json"))
except Exception as e:
    print("index/index.json nicht lesbar:", e); sys.exit(0)
hits = [e for e in data if (q and q in (e.get("ref", "") or "").lower()) or (q and q in (e.get("title", "") or "").lower())]
print("Treffer in index.json:", len(hits))
for e in sorted(hits, key=lambda e: e.get("price_chf") or 0)[:5]:
    print(json.dumps(e, ensure_ascii=False))
PYEOF
    ;;
esac
case "$LEVEL" in
  1|2)
    obsidian read path="$NOTE" 2>/dev/null | head -40
    ;;
  3)
    obsidian read path="$NOTE" 2>/dev/null | head -20
    echo ">>> Backlinks (obsidian backlinks)"
    obsidian backlinks path="$NOTE" 2>/dev/null | head -5
    ;;
esac
echo ">>> Antwort (Ollama, qwen3.5:0.8b)"
ollama run qwen3.5:0.8b "System: Du bist der Obsidian-Agent für den IEC-Standards-Vault. Antworte kurz und strukturiert (2-3 Sätze max): Fakten + Quellen-URLs (sources). Keine Übertragung von Standardtexten außerhalb der Daten. Frage: '$QUERY'. Daten: Note: $NOTE; index/index.json (Matrix: ref/title/type/edition/technical_committee/published/ics/status/price_chf/sources)." 2>/dev/null | head -25
