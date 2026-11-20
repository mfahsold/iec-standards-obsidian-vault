# Setup and Toolchain

This is the single setup reference. It records the verified stack and the two
supported ways to query the vault.

## Verified versions and capabilities

| Component | Version | Role |
| --- | --- | --- |
| Obsidian | 1.15.1 | Vault GUI; CLI available |
| Local LLM Helper | 2.6.2 | Community plugin; general chat + grounded RAG chat |
| Ollama | 0.40.15 | Local inference and embedding server (`localhost:11434`) |
| Chat model | `qwen3.5:2b` | Thinking enabled; 8,192-token budget |
| Embedding model | `nomic-embed-text` | 768 dimensions |
| RAG index | Local, derived from the notes | Rebuild after note changes; counts vary with content |
| Python | 3.9+ | Validator uses the standard library only |

Thinking cannot be disabled through this plugin's OpenAI-compatible endpoint;
allow enough output tokens. The model is used because it is the smallest local
model that answered the golden questions reliably with citations.

## Open the vault

1. Clone the repository.
2. Open the repository folder as an Obsidian vault.
3. Start at `README.md` or `index/index.md` (MOC).

The vault works without community plugins. Dataview is optional; example
queries are in the charter's context note only if needed. Frontmatter is the
canonical data store.

## CLI retrieval (portable)

Requirements: Python 3.9+, Ollama with `qwen3.5:2b`. The Obsidian CLI is
optional; the loop falls back to local file search.

```sh
ollama pull qwen3.5:2b

./tools/agent-loop.sh "What is IEC 62443-4-1?"
./tools/agent-loop.sh -l 2 "What is the price of IEC 62443-4-1:2018?"
./tools/agent-loop.sh -l 3 "Which TC owns IEC 62813:2025/COR1:2026?"
```

Environment variables: `VAULT_DIR`, `OBSIDIAN_BIN`, `OLLAMA_BIN`,
`OLLAMA_MODEL`. The prompt is grounded: use only the supplied note and index
data, cite the source note, and answer "Not in the vault" instead of inventing
facts.

## RAG chat in Obsidian

Install the Local LLM Helper plugin and configure:

- Endpoint: `http://localhost:11434`
- Model: `qwen3.5:2b`
- Embedding model: `nomic-embed-text`
- Max tokens: `8192`
- Temperature: `0.3`

Settings live in the **GUI vault's** `.obsidian/plugins/local-llm-helper/data.json`,
not in the repository's `.obsidian/`.

Use **Notes/RAG chat**, never **General chat**:

- Command palette: `Chat: Notes (RAG)` (`local-llm-helper:rag-chat`)
- Panel: the **Notes** toggle (not "General")
- Ribbon: `Chat with notes (RAG)`

General chat sends no note context and will fabricate answers. RAG chat retrieves
note chunks and cites them.

### Rebuild the index

After adding or changing notes:

```sh
obsidian plugin:reload id=local-llm-helper
obsidian command id=local-llm-helper:index-notes-rag
```

The reload is required first: the plugin caches the file list and silently skips
new notes otherwise.

### Golden questions

| Question | Expected |
| --- | --- |
| What are the ICS tags of IEC 62813:2025/COR1:2026? | 31.060.99, cited to that note |
| What is the price of IEC 62443-4-1:2018? | 335 CHF, "as of collection date", catalog link |
| What is IEC 65000-1:2099? Give its ICS and price. | "Not in the vault"; no invented data |

A General-mode result is not a valid test.

## Validation

```sh
python3 tools/validate_vault.py
shellcheck tools/agent-loop.sh   # optional
```

CI runs the validator on every push and pull request. It checks JSON,
frontmatter, index/note consistency, links, and public-safety rules.

## Related

- `docs/data-policy.md` — what may be stored and quoted
- `docs/provenance.md` — sources and licensing status
- `meta/project-charter.md` — scope and definition of done
