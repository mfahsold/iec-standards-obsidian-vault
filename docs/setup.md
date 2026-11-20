# Setup and Toolchain

This is the single setup reference. Runtime values are centralized in
[`tools/config.py`](../tools/config.py) and overridable by environment variables.
To see the effective configuration and live data statistics:

```sh
python3 tools/config.py --show
```

Do not rely on hardcoded versions or counts in documentation — use that command.

## Prerequisites

- Obsidian (desktop) for browsing/editing the vault; no community plugin is required.
- Ollama with a chat model and an embedding model, e.g.:

  ```sh
  ollama pull qwen3.5:2b
  ollama pull nomic-embed-text
  ```

- Python 3.9+; all tools use the standard library only.
- Hardware: ~4 GB disk for models/index, minimum ~8 GB RAM (16 GB recommended),
  CPU works but GPU/Metal is recommended. Details: [`../README.md`](../README.md#requirements).

## CLI question answering

```sh
python3 tools/build-index.py
python3 tools/agent-loop.py "What is the price of IEC 62443-4-1:2018?"
```

The pipeline:

1. **Retrieve** top-k chunks with hybrid search: dense cosine plus a BM25 lexical
   leg (distinctive tokens only), merged with Reciprocal Rank Fusion.
2. **Judge sufficiency** with a non-thinking structured call; if evidence is
   missing, abstain instead of guessing.
3. **Answer** with thinking enabled and Qwen sampling settings from `config.py`,
   citing each claim.

The index (`index/embeddings.json`) is gitignored local state, rebuilt from the
notes. `tools/config.py` holds all defaults (models, URLs, budgets, chunk size,
fusion parameters).

## Evaluation

Questions and expected values are generated from `index/index.json` by
`tools/probes.py`; nothing is hardcoded. Fast check (retrieval + decisions):

```sh
python3 tools/evaluate.py
```

Full check, including generated answers and citations (slow):

```sh
python3 tools/evaluate.py --generate
```

Re-run after any change to chunking, embeddings, prompts, or data. The current
baseline is printed by the evaluator itself. A historical embedding comparison
found nomic-embed-text superior to qwen3-embedding:0.6b on this corpus; nomic
remains the default.

## Optional GUI extras

- **Terminal in Obsidian:** community plugins can embed a real shell. Configure a
  profile named **IEC Vault** that starts in `iec-standards-obsidian-vault`.
- **One-click “Ask vault”:** copy `obsidian-plugin/manifest.json` and `main.js`
  into the GUI vault's `.obsidian/plugins/iec-vault-ask/` and enable it in
  Settings → Community plugins. It only wraps the CLI; GUI answers are not an
  independent QA path.

## Validation

```sh
python3 tools/validate_vault.py
python3 -m py_compile tools/*.py
```

CI runs the vault validator on every push and pull request. Full manual checks:
[`docs/testing.md`](testing.md).
