# IEC Standards Knowledge Vault

A local-first, open-source Obsidian vault and retrieval stack for **public
metadata about IEC/ISO standards** — built for humans, agents, and
citation-grounded question answering.

**NOT OFFICIAL IEC/ISO MATERIAL.** This is an independent, unofficial aggregate of
publicly available information. It is **not official IEC or ISO communication,
documentation, catalog, or a source of record of any kind**, is not affiliated with
or endorsed by IEC/ISO, **may contain errors or outdated values**, and contains
**no standard document bodies**, PDFs, or long verbatim excerpts. Only the official
IEC/ISO catalogs and current editions are authoritative. See [`NOTICE.md`](NOTICE.md)
and [`docs/data-policy.md`](docs/data-policy.md).

## Why this exists

IEC catalog data is public but scattered across product pages, PDFs, and
process documents. Engineers and agents often need precise answers to narrow
questions:

- What is the ICS code of this standard?
- Which TC/SC owns it?
- Is it an IS, TR, PAS, COR1, or AMD2?
- What did it cost at the time of cataloging?
- How does the IEC development process work?
- Which standard applies to a given product category?

This project turns that public metadata into a navigable Obsidian vault and a
machine-readable index, then adds a local retrieval loop that answers with
citations — without copying the standards themselves.

## What is inside

| Path | Purpose |
| --- | --- |
| `standards/` | 23 catalog notes with YAML frontmatter (ref, type, edition, TC/SC, ICS, dates, price snapshot, sources). |
| `processes/` | Public IEC process and document-type notes (IS, TS, TR, PAS, stages, workflows, terms). |
| `electropedia/` | Electropedia / IEV reference note (links + short attributed quotes). |
| `guides/`, `news/` | IEC Guides and newsletter references. |
| `index/index.json` | Machine-readable catalog for tools and agents. |
| `index/index.md` | Master index / map of contents (MOC). |
| `meta/` | Project charter, provenance, source list, setup notes, design history. |
| `tools/agent-loop.py` | Grounded CLI retrieval loop via Ollama’s native API (stdlib only). |
| `tools/validate_vault.py` | Data, link, and public-safety validator used in CI. |
| `docs/` | Data policy, IEC engagement questionnaire. |

## Quick start (Obsidian)

1. Clone the repository.
2. Open the repository folder as an Obsidian vault.
3. Start at [`README.md`](README.md) or [`index/index.md`](index/index.md).
4. Use Quick Switcher (`Cmd/Ctrl+O`), search (`Cmd/Ctrl+Shift+F`), backlinks,
   and graph view to navigate.

The vault is designed to work without community plugins. Dataview queries in
[`docs/setup.md`](docs/setup.md) are optional.

## Quick start (CLI)

Requirements:

- Python 3.9+
- [Ollama](https://ollama.com/) with a local model, e.g.
  `ollama pull qwen3.5:2b`
- Optional: the Obsidian CLI for backlinks (the loop falls back to local search)

```sh
# Level 1: find a note, read it, answer with a citation
python3 tools/agent-loop.py "What is the price of IEC 62443-4-1:2018?"
python3 tools/agent-loop.py "What is IEC 65000-1:2099? Give me its ICS and price."
```

Environment variables:

```sh
OLLAMA_URL=http://localhost:11434 \
OLLAMA_MODEL=qwen3.5:2b \
python3 tools/agent-loop.py "What are the ICS tags of IEC 62813:2025/COR1:2026?"
```

The prompt is deliberately strict: use only the supplied note/index data, cite
the source note, and say “Not in the vault” instead of inventing facts.

## Data policy in one paragraph

We include public metadata (references, titles, editions, dates, committees,
ICS codes, price snapshots, links) and our own short summaries. We do not
include IEC/ISO document bodies, PDFs, long verbatim excerpts, paywalled
content, or scraped content. Prices are snapshots, not authoritative. Short
quotations from public pages are attributed and linked. See
[`docs/data-policy.md`](docs/data-policy.md).

## Validation

```sh
python3 tools/validate_vault.py
python3 -m py_compile tools/*.py
```

For a manual pre-release check, follow [`docs/testing.md`](docs/testing.md).

The validator checks:

- JSON validity and index/note consistency;
- required frontmatter fields and source URLs;
- catalog/MOC coverage;
- broken Markdown links and unresolved wikilinks;
- absolute local paths, secrets, PDFs, and overly long block quotes.

CI runs the same checks on every push and pull request.

## Contributing

Contributions are welcome. Please read [`CONTRIBUTING.md`](CONTRIBUTING.md) for
the workflow and data rules. The short version: public sources only, paraphrase
descriptions, cite every fact, never paste standard bodies, and run the
validator. Report security concerns privately via GitHub, not in a public
issue.

## Licensing

- **Code** (scripts, CI, tooling): MIT — see [`LICENSES/MIT.txt`](LICENSES/MIT.txt).
- **Original content** (notes, documentation, metadata compilation): CC BY 4.0
  — see [`LICENSES/CC-BY-4.0.txt`](LICENSES/CC-BY-4.0.txt).
- **Third-party material**: not covered; see [`NOTICE.md`](NOTICE.md).

IEC/ISO names, standard references, and titles remain the property of their
respective owners. This project claims no rights in them and includes no
document bodies. The maintainers are clarifying reuse terms for IEC-derived
metadata with the IEC; see [`docs/iec-engagement.md`](docs/iec-engagement.md).

## Status and roadmap

- **Status:** prototype; 23 verified catalog entries across 52 Markdown notes.
- **Verified:** data-generated probes (ICS, price, committee, type, abstention),
  RAG retrieval, validator/CI.
- **Next:** expand verified coverage, add more probe templates, improve
  product→ICS→standard mapping, and complete the IEC clarification.

## Disclaimer

This repository is an independent, unofficial aggregate of publicly available
information. It is **not official IEC or ISO communication or documentation of any
kind**, is not affiliated with or endorsed by IEC/ISO, and may contain errors,
omissions, or outdated data. It is informational only and provides no
certification, legal, or conformity advice. Always verify against the official
IEC/ISO catalog and the current edition of a standard before making commercial or
safety-critical decisions.
