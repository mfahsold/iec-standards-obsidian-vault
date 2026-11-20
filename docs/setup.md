# Setup and Toolchain

This is the single setup reference. It records the verified stack and the one
supported QA path.

## Verified versions and capabilities

| Component | Version | Role |
| --- | --- | --- |
| Obsidian | 1.15.1 | Vault GUI for navigation; no chat plugin required |
| Ollama | 0.40.15 | Local inference and embedding server (`localhost:11434`) |
| Chat model | `qwen3.5:2b` | Thinking enabled; 8,192-token budget |
| Embedding model | `nomic-embed-text` | 768 dimensions |
| RAG index | `index/embeddings.json` (gitignored) | Built by `tools/build-index.py` |
| Python | 3.9+ | All tools use the standard library only |

There is no third-party chat plugin. The CLI tool is the only QA path: it
retrieves from the local index, judges sufficiency, abstains when evidence is
missing, and generates cited answers with Ollama’s native API. Obsidian is used
only for navigation and editing the vault.

## Open the vault

1. Clone the repository.
2. Open the repository folder as an Obsidian vault.
3. Start at `README.md` or `index/index.md` (MOC).

The vault works without community plugins. Frontmatter is the canonical data
store.

## Optional: terminal inside Obsidian

Obsidian core has no terminal, but community plugins can embed a real system
shell in the workspace. Established options (desktop only):

- **Terminal** — integrated or external terminals, profiles, saved history;
  Obsidian 1.4.11+, widely used.
- **Lean Terminal** — embedded xterm.js + node-pty panel; Obsidian 1.7.2+.
- **Terminal Tabs** — terminal as a docked tab, no network or telemetry;
  Obsidian 1.14.4+, needs Python 3 for its PTY bridge.

This is **UI convenience only**: it does not change the QA path or add a repo
dependency. The plugin lives in the GUI vault's `.obsidian/plugins/`, not in this
repository.

### Vault-specific profile

Configure one profile so the terminal opens directly in the repository:

| Plugin | Setting | Value |
| --- | --- | --- |
| Terminal | Profile shell | `zsh --login` (or your shell) |
| Terminal | Startup command | `cd iec-standards-obsidian-vault` |
| Lean Terminal | Startup command | `cd iec-standards-obsidian-vault` |
| Terminal Tabs | Custom working folder | `iec-standards-obsidian-vault` |

Name the profile **IEC Vault** and bind it to a hotkey/command-palette entry. You
then get a one-click terminal in the right place, with no extra code in this
repository. From there the normal commands apply:

```sh
python3 tools/build-index.py
python3 tools/agent-loop.py "What is the price of IEC 62443-4-1:2018?"
```

A terminal runs with your user permissions; run only commands you understand.

## CLI retrieval (portable)

Requirements: Python 3.9+, Ollama with `qwen3.5:2b` and `nomic-embed-text`, and
the local index at `index/embeddings.json` (build it as shown below).

```sh
ollama pull qwen3.5:2b
ollama pull nomic-embed-text
python3 tools/build-index.py

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

## Rebuild the index

After adding or changing notes:

```sh
python3 tools/build-index.py
```

The builder chunks every Markdown file (800 characters, 100 overlap), embeds the
chunks with `nomic-embed-text`, and writes `index/embeddings.json`. The file is
gitignored; it is local state derived from the notes.

## Golden questions

| Question | Expected |
| --- | --- |
| What are the ICS tags of IEC 62813:2025/COR1:2026? | 31.060.99, cited to that note |
| What is the price of IEC 62443-4-1:2018? | 335 CHF, "as of collection date", catalog link |
| What is IEC 65000-1:2099? Give its ICS and price. | "Not in the vault"; no invented data |

Only `tools/agent-loop.py` results are valid evidence.

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
