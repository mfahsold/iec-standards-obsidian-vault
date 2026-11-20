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

## Optional: one-click “Ask vault” button (custom plugin)

`obsidian-plugin/` contains a minimal Obsidian plugin that wraps the same CLI
engine in a modal (input → answer). It does not add QA logic, a service, or a
port; it only calls `tools/agent-loop.py` in this repository.

Install manually in the GUI vault:

```sh
mkdir -p <GUI-vault>/.obsidian/plugins/iec-vault-ask
cp obsidian-plugin/manifest.json obsidian-plugin/main.js \
   <GUI-vault>/.obsidian/plugins/iec-vault-ask/
```

Then enable **IEC Vault Ask** under Settings → Community plugins and use the
ribbon icon or Cmd+P → “Ask IEC vault”. The CLI remains the authoritative
answer path.

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

1. **Retrieve** the top-5 chunks with hybrid search: dense cosine similarity
   plus a BM25 lexical leg (distinctive tokens only), merged with Reciprocal
   Rank Fusion (`RRF_K=60`). Set `HYBRID=0` for dense-only comparison.
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

Chunks follow Markdown headings (~800 characters, 100 overlap). Each embedded
chunk receives a deterministic header (`Document: <ref> / Section: <heading>`);
the clean text is kept separately for display. Nomic task prefixes
(`search_document:` / `search_query:`) and an 8K embedding context are applied;
chat calls keep the model resident for 10 minutes. Output is gitignored local
state.

## Evaluation

The golden set lives in `tools/golden-questions.json` (9 answerable + 3
out-of-vault probes). Run the fast check — retrieval and sufficiency decisions:

```sh
python3 tools/evaluate.py
```

For the full check, including generated answers and citations (slow):

```sh
python3 tools/evaluate.py --generate
```

The harness reports retrieval hit rate, decision accuracy, and — with
`--generate` — answer accuracy. Every change to chunking, embeddings, or prompts
should be re-evaluated with this command.

Current baseline: retrieval **12/12**, sufficiency decisions **10/12**. Two
open-ended/multi-part cases are a known limitation of the 2B judge and are
tracked; factual and out-of-vault cases are correct. If generation returns no
content, the model's thinking consumed the output budget; raise `NUM_PREDICT`
(e.g. 16384). Under Ollama contention, stop unused models with `ollama stop`.

### Embedding model A/B

The index builder can write an alternative index for comparison:

```sh
ollama pull qwen3-embedding:0.6b
EMBED_MODEL=qwen3-embedding:0.6b RAG_INDEX=index/embeddings-qwen3.json \
  python3 tools/build-index.py
RAG_INDEX=index/embeddings-qwen3.json EMBED_MODEL=qwen3-embedding:0.6b \
  python3 tools/evaluate.py
```

Compare retrieval hit rate and decision accuracy against the nomic baseline
before switching. Both index files are gitignored.

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
