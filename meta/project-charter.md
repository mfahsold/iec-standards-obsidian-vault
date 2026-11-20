# Project Charter

Status: 2026-11-20. This is the single source of truth for purpose, scope and
definition of done. Setup details are in `docs/setup.md`; provenance is in
`docs/provenance.md`.

## 1. Vision

A small, local, offline-capable knowledge base for IEC/ISO **metadata** that
answers precise questions with short, source-grounded answers — without copying
copyrighted document bodies and without sending data to a cloud service.

The vault is both:

1. a human-navigable Obsidian vault (MOC, wikilinks, backlinks, graph);
2. a machine-readable dataset and retrieval stack (`index/index.json`,
   frontmatter, CLI loop, RAG).

Principles: metadata not document bodies; evidence over fluency; minimal stack;
one canonical dataset.

## 2. Questions this vault answers

| # | Class | Example | Source |
| --- | --- | --- | --- |
| Q1 | Identification | What is IEC 62443-4-1? | Note description + title |
| Q2 | Commercial | What does it cost? | `price_chf`, marked as snapshot |
| Q3 | Classification | ICS tags? | `ics` in note/index |
| Q4 | Lifecycle | IS, TR, PAS, COR1? Edition? | `type`, `edition`, `published` |
| Q5 | Ownership | Which TC/SC? | `technical_committee` |
| Q6 | Process | How is a standard published? | `processes/`, `meta/context.md` |
| Q7 | Comparison | Compare two standards | Multiple notes, `index/index.json` |

Q8 (product-to-standard mapping) remains a stretch goal: it requires an
engineering product→ICS→TC mapping the vault does not provide.

## 3. Scope

**In scope:** public catalog metadata; IEC process and document-type knowledge;
Electropedia references; structured navigation; local CLI and RAG retrieval;
machine-readable index and frontmatter as the single source of truth.

**Out of scope:** IEC/ISO document bodies; certification, legal or conformity
advice; browser automation, cloud LLMs or hosted vector databases; exhaustive
coverage of the standards universe; silent writes without human review.

## 4. Architecture

```text
repository/
├─ index/index.json          machine-readable catalog (23 entries)
├─ index/index.md            MOC
├─ standards/                23 standard notes + catalog + classics
├─ processes/, electropedia/, guides/, news/
├─ docs/                     data policy, IEC engagement, setup, provenance
├─ meta/                     charter, context
└─ tools/                    agent-loop.py, validate_vault.py
```

The CLI tool uses hybrid retrieval (RAG chunks + `index/index.json`), a
structured sufficiency check with explicit abstention, and grounded generation
with thinking enabled. `tools/build-index.py` produces the local index from the
vault notes; no chat plugin is required.

Verified stack: Obsidian 1.15.1 (navigation only), Ollama 0.40.15,
`qwen3.5:2b` (8,192 tokens), `nomic-embed-text` (768 dims). The RAG index at
`index/embeddings.json` is gitignored and rebuilt after note changes.

## 5. Definition of Done

### A standard note

- Required frontmatter fields present; `sources` URLs valid.
- Original description; no document bodies or long verbatim excerpts.
- Price/date marked as snapshot with source URL.
- Entry present in `index/index.json`, `standards/index-standards.md`, and
  `index/index.md`.
- Note is linked from the catalog/MOC; `python3 tools/validate_vault.py` passes.
- RAG index rebuilt with `python3 tools/build-index.py` if files were added.

### A prompt, retrieval or configuration change

- A data-generated probe covers the changed behavior (`docs/setup.md`).
- Passes on the **CLI path**, the only QA implementation (hybrid retrieval,
  sufficiency judgement, abstention, thinking generation).
- Obsidian has no chat role; it is used for navigation and editing only.
- Answer checked against `index/index.json` / frontmatter.
- Known failure patterns guarded (no invented data, no "IEC standards are
  free", no missing citations).
- Out-of-vault questions abstain before generation; unrelated notes are never
  substituted for a missing answer.

### A release

- Validator and Python compile check pass; working tree clean.
- No new orphans in Obsidian.
- Documentation in English and consistent with the verified stack.
- Commit message states the evidence, not the intention.

## 6. Known limits

- Coverage is 23 verified entries; absence is not evidence that a standard does
  not exist.
- No GUI chat is provided; all QA goes through `tools/agent-loop.py`.
- Prices and dates are collection-time snapshots.
- External commentary in `meta/context.md` is attributed, not a project position.
- No conformity advice.

## 7. Key documents

- `README.md` — entry point
- `docs/setup.md` — toolchain, CLI, RAG, evaluation probes, validation
- `docs/data-policy.md` — what may be stored and quoted
- `docs/provenance.md` — sources and licensing status
- `docs/iec-engagement.md` — open questions for IEC
- `meta/context.md` — publication types, committees, ICS, bodies, terms
