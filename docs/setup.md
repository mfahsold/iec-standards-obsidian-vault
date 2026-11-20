# Setup and Toolchain

This is the single setup reference. Runtime values are centralized in
[`tools/config.py`](../tools/config.py) and overridable by environment variables.
To see the effective configuration and live data statistics:

```sh
python3 tools/config.py --show
```

Do not rely on hardcoded versions or counts in documentation — use that command.

**Context window:** `NUM_CTX` defaults to 16384 tokens. This is a deliberate
fixed value, not a dynamic per-request calculation: our prompts are a system
message plus five retrieved chunks (well under 8K tokens), and 16K is the
common RAG floor. Ollama allocates the KV cache when the model is loaded — a
changing `num_ctx` per request forces a model reload and adds seconds of
latency, so one standardised value is the current best practice for this
workload. It also cut observed peak memory from ~6.3 GiB at 98K context.
Setting `OLLAMA_CONTEXT_LENGTH` server-side or baking `PARAMETER num_ctx` into a
derived model are alternatives if every client must share the same window.

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

- **One-click “Ask vault” (our own plugin):** `obsidian-plugin/` contains a small
  plugin that wraps `tools/agent-loop.py` in a modal.

  Install on any machine:

  ```sh
  cp obsidian-plugin/manifest.json obsidian-plugin/main.js \
     <GUI-vault>/.obsidian/plugins/iec-vault-ask/
  ```

  Then enable **IEC Vault Ask** in Settings → Community plugins and restart
  Obsidian once (or use `obsidian plugin:reload id=iec-vault-ask`).

  Use it:

  1. Click the ribbon icon **Ask IEC vault** (message icon), or press `Cmd+P`
     and run **“Ask IEC vault”**.
  2. Type a question in the modal, e.g.
     `What is the price of IEC 62443-4-1:2018?`
  3. Click **Ask** and wait roughly 60–90 seconds (thinking mode).
  4. The answer appears in the modal with `[Source: …]` labels.

  The plugin discovers the repo folder by looking for `tools/agent-loop.py` in
  the vault's subfolders, then runs the CLI with a 180 s timeout. If it reports
  “no vault repo with tools/agent-loop.py found”, check that the repo folder is
  directly inside the vault. No service or port is involved. GUI answers are a
  convenience only — verify anything used as evidence with the CLI.
- **Terminal in Obsidian (optional, third-party):** community plugins such as
  Terminal, Lean Terminal or Terminal Tabs can embed a real shell. This project
  does not ship a terminal plugin. If you install one, configure a profile named
  **IEC Vault** that starts in the repo folder (`iec-standards-obsidian-vault`
  in this workspace).
- **Local LLM Helper is not used.** If it was enabled previously, disable and
  remove it from the GUI vault; it is not part of this stack and cannot run our
  abstention stage.

## Validation

```sh
python3 tools/validate_vault.py
python3 -m py_compile tools/*.py
```

CI runs the vault validator on every push and pull request. Full manual checks:
[`docs/testing.md`](testing.md).
