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

## Start here

Open this folder as an Obsidian vault and read [`index/index.md`](index/index.md)
(MOC), or use the CLI:

```sh
ollama pull qwen3.5:2b
ollama pull nomic-embed-text
python3 tools/build-index.py
python3 tools/agent-loop.py "What is the price of IEC 62443-4-1:2018?"
```

The pipeline retrieves note chunks and catalog records, checks whether the
evidence is sufficient, abstains when it is not, and answers with citations.
All settings live in [`tools/config.py`](tools/config.py) (environment-overridable).
Run `python3 tools/config.py --show` for the effective configuration and live
catalog/index statistics — no hardcoded counts in this documentation.

## What is inside

- `standards/` — catalog notes with YAML frontmatter; `index/index.json` — machine-readable catalog.
- `processes/`, `electropedia/`, `guides/`, `news/` — public process and reference notes.
- `docs/` — data policy, setup, provenance, IEC engagement, testing.
- `meta/` — project charter and standards context.
- `tools/` — index builder, QA loop, config, evaluator, validators.
- `obsidian-plugin/` — optional one-click “Ask vault” wrapper (UI only).

## Rules in one paragraph

We store only public metadata, links, original summaries, and short attributed
quotations — no document bodies, PDFs, scraped or purchased content. Prices and
dates are collection-time snapshots. Answers must cite a source and say “not in
the vault” rather than invent facts. Full rules: [`docs/data-policy.md`](docs/data-policy.md).

## Validation and testing

```sh
python3 tools/validate_vault.py
python3 tools/evaluate.py
```

For the complete manual pre-release plan: [`docs/testing.md`](docs/testing.md).
Setup details (including optional GUI extras): [`docs/setup.md`](docs/setup.md).

## Contributing and licensing

Contributions: [`CONTRIBUTING.md`](CONTRIBUTING.md). Code is MIT, original content
is CC BY 4.0; IEC/ISO material is not relicensed. “Non-commercial” describes our
intent, not a license restriction. See [`LICENSE`](LICENSE) and
[`NOTICE.md`](NOTICE.md).

This repository is informational only — no certification, legal, or conformity
advice. Verify everything against official sources.
