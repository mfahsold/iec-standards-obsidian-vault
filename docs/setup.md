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

The CLI tool uses Ollama’s native `/api/chat`, where `think` is a supported
top-level field. The Obsidian plugin uses the OpenAI-compatible endpoint, which
does not expose `think`; this is why the GUI and CLI are configured differently.
The RAG index is produced by the plugin and consumed by the CLI tool.

## Open the vault

1. Clone the repository.
2. Open the repository folder as an Obsidian vault.
3. Start at `README.md` or `index/index.md` (MOC).

The vault works without community plugins. Dataview is optional; example
queries are in the charter's context note only if needed. Frontmatter is the
canonical data store.

## CLI retrieval (portable)

Requirements: Python 3.9+, Ollama with `qwen3.5:2b` and `nomic-embed-text`, and
a RAG index built by the Obsidian plugin (the default path is the sibling GUI
vault’s `.obsidian/plugins/local-llm-helper/embeddings.json`).

```sh
ollama pull qwen3.5:2b
ollama pull nomic-embed-text

python3 tools/agent-loop.py "What is the price of IEC 62443-4-1:2018?"
python3 tools/agent-loop.py "What is IEC 65000-1:2099? Give me its ICS and price."
```

The tool implements the standard grounded-QA pipeline:

1. **Retrieve** the top-5 note chunks from the RAG index by cosine similarity.
2. **Judge sufficiency** with a structured, non-thinking call. If the evidence
   does not contain the requested fact, the tool abstains — no model-generated
   guess, no irrelevant notes.
3. **Answer** with thinking enabled and Qwen’s recommended sampling
   (`temperature 0.6`, `top_p 0.95`, `top_k 20`, `min_p 0`), citing each claim.

Because the chunker omits YAML frontmatter, the tool also adds matching records
from `index/index.json` so that `price_chf` and `ics` are available as evidence.
This is hybrid retrieval over the project’s single canonical dataset.

Environment variables: `OLLAMA_URL`, `OLLAMA_MODEL`, `EMBED_MODEL`, `RAG_INDEX`,
`TOP_K`, `NUM_CTX`, `NUM_PREDICT`.

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
python3 -m py_compile tools/*.py
```

CI runs the validator on every push and pull request. It checks JSON,
frontmatter, index/note consistency, links, and public-safety rules.

## Related

- `docs/data-policy.md` — what may be stored and quoted
- `docs/provenance.md` — sources and licensing status
- `meta/project-charter.md` — scope and definition of done
