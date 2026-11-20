# Unofficial IEC Metadata Vault

A local-first, offline, independent knowledge base of **public metadata about
IEC/ISO standards**, plus a grounded CLI that answers questions with citations.

**NOT OFFICIAL IEC/ISO MATERIAL.** This is an unofficial aggregate of publicly
available information. It is **not official IEC or ISO communication, documentation,
catalog, or a source of record of any kind**, is not affiliated with or endorsed by
IEC/ISO, **may contain errors or outdated values**, and contains no standard
document bodies. Only the official IEC/ISO catalogs and current editions are
authoritative. See [`NOTICE.md`](NOTICE.md).

**Scope:** a small, verified subset of public catalog data — not a complete IEC
catalog. The internal review threshold before growing further is reported by
`python3 tools/config.py --show`.

## Vision, scope and Definition of Done

The goal is to help a human or agent navigate the IEC/ISO standards universe with
**short, source-grounded answers**, without copying copyrighted document bodies
and without sending data to a cloud service. The vault is both a human-navigable
Obsidian vault and a machine-readable dataset with a local retrieval stack.

- Vision, question classes (Q1–Q7), scope, architecture and DoD:
  [`meta/project-charter.md`](meta/project-charter.md)
- Data policy and what is never included: [`docs/data-policy.md`](docs/data-policy.md)
- Manual pre-release test and release gate: [`docs/testing.md`](docs/testing.md)
- Setup details and optional GUI extras: [`docs/setup.md`](docs/setup.md)

## Requirements

**Software**
- Python 3.9 or newer (standard library only; no pip dependencies).
- [Ollama](https://ollama.com/) 0.40.15 or newer, running locally.
- Optional: Obsidian desktop for browsing/editing the vault.

**Models** (pulled locally through Ollama)
- `qwen3.5:2b` — chat/reasoning, about 3.1 GB download.
- `nomic-embed-text` — embeddings, about 274 MB.

**Hardware**
- About 4 GB free disk for the two models plus the local index.
- Minimum ~8 GB RAM/unified memory; **16 GB recommended** (chat model ~3.2 GB at
  runtime plus KV-cache/context; runtime context is 98,304 tokens).
- CPU-only works but is slow. Apple Silicon/Metal or an NVIDIA GPU is recommended
  for reasonable answer latency. No GPU is strictly required.
- Network access is needed only to install Ollama, pull models and clone this repo;
  answering questions then runs fully offline.

## Installation

```sh
git clone https://github.com/mfahsold/unofficial-iec-metadata-vault.git
cd unofficial-iec-metadata-vault

# Install Ollama from https://ollama.com/ and start it, then:
ollama pull qwen3.5:2b
ollama pull nomic-embed-text

# Optional but recommended: isolated Python environment
python3 -m venv .venv
. .venv/bin/activate          # Windows: .venv\Scripts\activate

# Build the local RAG index (gitignored state, rebuild after note changes)
python3 tools/build-index.py
```

Ask a question:

```sh
python3 tools/agent-loop.py "What is the price of IEC 62443-4-1:2018?"
```

Optional GUI: open the repository as an Obsidian vault, start at
[`index/index.md`](index/index.md) (MOC). A terminal plugin profile and the
one-click “Ask vault” plugin are described in [`docs/setup.md`](docs/setup.md).

## Configuration

All defaults (models, URLs, budgets, chunking, fusion parameters) live in
[`tools/config.py`](tools/config.py) and can be overridden by environment
variables. Inspect the effective configuration and live data with:

```sh
python3 tools/config.py --show
```

## What is inside

- `standards/` — catalog notes with YAML frontmatter; `index/index.json` — machine-readable catalog.
- `processes/`, `electropedia/`, `guides/`, `news/` — public process and reference notes.
- `docs/` — data policy, setup, provenance, IEC engagement, email draft, takedown, testing.
- `meta/` — project charter and standards context.
- `tools/` — index builder, QA loop, config, evaluator, validators.
- `obsidian-plugin/` — optional one-click “Ask vault” wrapper (UI only).

## Rules in one paragraph

We store only public metadata, links and original summaries — no document bodies,
PDFs, direct quotations, scraped or purchased content. Prices and dates are
collection-time snapshots. Answers must cite a source and say “not in the vault”
rather than invent facts. Adding your own licensed documents locally is outside
this project's scope and your responsibility. Full rules:
[`docs/data-policy.md`](docs/data-policy.md).

## Validation and testing

```sh
python3 tools/validate_vault.py
python3 tools/evaluate.py
```

The complete manual test plan and release gate are in [`docs/testing.md`](docs/testing.md).

## Contributing and licensing

Contributions: [`CONTRIBUTING.md`](CONTRIBUTING.md). Code is MIT, original content
is CC BY 4.0; IEC/ISO material is not relicensed. “Non-commercial” describes our
intent, not a license restriction. See [`LICENSE`](LICENSE) and
[`NOTICE.md`](NOTICE.md).

This repository is informational only — no certification, legal, or conformity
advice. Verify everything against official sources.
