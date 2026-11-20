#!/bin/sh
# agent-loop.sh — local, citation-grounded retrieval for the IEC vault.
#
# L1: find a note, read it, ask a local Ollama model.
# L2: L1 + structured lookup in index/index.json.
# L3: L1 + incoming links (Obsidian CLI when available, local scan otherwise).
#
# The tool works without Obsidian: it falls back to local file search.
# It never sends data to a cloud service.

set -eu

SCRIPT_DIR=$(CDPATH='' cd -- "$(dirname -- "$0")" && pwd)
VAULT_DIR=${VAULT_DIR:-$(CDPATH='' cd -- "$SCRIPT_DIR/.." && pwd)}
OBSIDIAN_BIN=${OBSIDIAN_BIN:-obsidian}
OLLAMA_BIN=${OLLAMA_BIN:-ollama}
OLLAMA_MODEL=${OLLAMA_MODEL:-qwen3.5:2b}
LEVEL=1

usage() {
  cat <<'EOF'
Usage: agent-loop.sh [-l 1|2|3] [-m MODEL] <question>

Environment:
  VAULT_DIR       Vault root (default: parent directory of this script)
  OBSIDIAN_BIN    Obsidian CLI binary (default: obsidian; optional)
  OLLAMA_BIN      Ollama binary (default: ollama)
  OLLAMA_MODEL    Model name (default: qwen3.5:2b)

Levels:
  1  Find a note, read it, answer (default)
  2  Level 1 + structured lookup in index/index.json
  3  Level 1 + incoming links

Examples:
  ./tools/agent-loop.sh "What are the ICS tags of IEC 62813:2025/COR1:2026?"
  ./tools/agent-loop.sh -l 2 "What is the price of IEC 62443-4-1:2018?"
  OLLAMA_MODEL=qwen3.5:2b ./tools/agent-loop.sh "What is IEC 62443-4-1?"
EOF
}

while getopts "l:m:h" opt; do
  case "$opt" in
    l) LEVEL=$OPTARG ;;
    m) OLLAMA_MODEL=$OPTARG ;;
    h) usage; exit 0 ;;
    *) usage; exit 2 ;;
  esac
done
shift $((OPTIND - 1))

if [ "$#" -eq 0 ]; then
  usage
  exit 2
fi

QUERY=$*

case "$LEVEL" in
  1|2|3) ;;
  *) echo "error: level must be 1, 2 or 3" >&2; exit 2 ;;
esac

if [ ! -f "$VAULT_DIR/index/index.json" ]; then
  echo "error: vault not found at $VAULT_DIR (missing index/index.json)" >&2
  exit 1
fi

if ! command -v "$OLLAMA_BIN" >/dev/null 2>&1; then
  echo "error: Ollama binary '$OLLAMA_BIN' not found." >&2
  echo "Install Ollama, or set OLLAMA_BIN to its path." >&2
  exit 127
fi

# Extract a standard-like reference from the question, e.g.
# "IEC 62443-4-1:2018", "IEC TR 63650:2026", "CISPR PAS 38:2025".
REF=$(printf '%s\n' "$QUERY" \
  | grep -oiE '(IEC|ISO|CISPR)([[:space:]]+(TR|TS|PAS|TRF|GUIDE))?[[:space:]]+[0-9][0-9A-Za-z./:_-]*' \
  | head -1 || true)

if [ -n "$REF" ]; then
  SEARCH_TERM=$REF
else
  SEARCH_TERM=$QUERY
fi

slugify() {
  printf '%s' "$1" \
    | sed 's/[[:space:]]\+/-/g; s/[:/]/-/g; s/[^A-Za-z0-9._-]//g'
}

find_note() {
  term=$1
  slug=$(slugify "$term")

  # 1. Exact filename match (case-insensitive), e.g. IEC-62443-4-1-2018.md
  for f in "$VAULT_DIR"/standards/*.md; do
    [ -f "$f" ] || continue
    base=$(basename "$f" .md)
    lower_base=$(printf '%s' "$base" | tr '[:upper:]' '[:lower:]')
    lower_slug=$(printf '%s' "$slug" | tr '[:upper:]' '[:lower:]')
    if [ "$lower_base" = "$lower_slug" ]; then
      printf '%s\n' "$f"
      return 0
    fi
  done

  # 2. Filename contains the slug
  for f in "$VAULT_DIR"/standards/*.md; do
    [ -f "$f" ] || continue
    base=$(basename "$f" .md)
    lower_base=$(printf '%s' "$base" | tr '[:upper:]' '[:lower:]')
    lower_slug=$(printf '%s' "$slug" | tr '[:upper:]' '[:lower:]')
    case "$lower_base" in
      *"$lower_slug"*) printf '%s\n' "$f"; return 0 ;;
    esac
  done

  # 3. Full-text fallback in standards/
  grep -ril --include='*.md' -- "$term" "$VAULT_DIR/standards" 2>/dev/null | head -1
}

NOTE_ABS=$(find_note "$SEARCH_TERM")

if [ -z "$NOTE_ABS" ] || [ ! -f "$NOTE_ABS" ]; then
  echo "No matching note found for: $SEARCH_TERM" >&2
  echo "Try a standard reference such as 'IEC 62443-4-1:2018', or add a note first." >&2
  exit 2
fi

NOTE_REL=${NOTE_ABS#"$VAULT_DIR"/}
NOTE_TEXT=$(sed -n '1,80p' "$NOTE_ABS")

echo ">>> Level $LEVEL — vault: $VAULT_DIR"
echo ">>> Note: $NOTE_REL"

STRUCTURED=""
if [ "$LEVEL" -ge 2 ]; then
  echo ">>> Structured lookup: index/index.json"
  STRUCTURED=$(python3 - "$VAULT_DIR/index/index.json" "$SEARCH_TERM" <<'PY'
import json
import sys

path, query = sys.argv[1], sys.argv[2].lower()
try:
    with open(path, encoding="utf-8") as handle:
        data = json.load(handle)
except Exception as exc:  # noqa: BLE001 - show a useful message
    print(f"index/index.json not readable: {exc}")
    raise SystemExit(0)

hits = [
    entry for entry in data
    if query in str(entry.get("ref", "")).lower()
    or query in str(entry.get("name", "")).lower()
    or query in str(entry.get("title", "")).lower()
]

print(f"Structured hits: {len(hits)}")
for entry in hits[:5]:
    print(json.dumps(entry, ensure_ascii=False, sort_keys=True))
PY
)
  printf '%s\n' "$STRUCTURED"
fi

if [ "$LEVEL" -ge 3 ]; then
  echo ">>> Incoming links"
  if command -v "$OBSIDIAN_BIN" >/dev/null 2>&1; then
    "$OBSIDIAN_BIN" backlinks path="$NOTE_REL" 2>/dev/null | head -10 || true
  else
    base=$(basename "$NOTE_ABS" .md)
    grep -rl --include='*.md' -- "$base" "$VAULT_DIR" 2>/dev/null \
      | grep -v "^$NOTE_ABS$" \
      | sed "s#^$VAULT_DIR/##" \
      | head -10 || true
  fi
fi

PROMPT=$(cat <<EOF
System: You are a retrieval assistant for a public IEC/ISO metadata vault.
Answer in 2-3 short sentences. Use ONLY the note and structured data below.
Cite the source note path in square brackets, e.g. [Source: standards/IEC-62443-4-1-2018.md].
If the answer is not in the data, say "Not in the vault" and do not invent facts.
Never invent standard references, ICS codes, prices, dates, committees, or citations.
Prices are snapshots from the catalog date; say so and point to the official catalog for current prices.

Question: $QUERY

Note path: $NOTE_REL
Note:
$NOTE_TEXT

Structured data:
$STRUCTURED
EOF
)

echo ">>> Answer ($OLLAMA_MODEL)"
printf '%s\n' "$PROMPT" | "$OLLAMA_BIN" run "$OLLAMA_MODEL" 2>/dev/null | head -40
