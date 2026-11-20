# Project Charter — Vision, Scope, Definition of Done

Status: 2026-11-20 — evidence-based (verified against the live vault, CLI, Ollama and the GUI plugin settings). This is the authoritative document for *why* this project exists, *what* it covers, and *when a piece of work is finished*.

---

## 1. Vision

A **small, local, offline-capable knowledge base for IEC standards** that lets a human or an agent ask precise questions (scope, type, ICS, committee, date, price, status, related processes) and get **short, source-grounded answers** — without copying copyrighted IEC document bodies and without sending data to a cloud service.

The vault is both:

1. a **human navigable Obsidian vault** (MOC, wikilinks, graph, backlinks, Dataview), and
2. a **machine-readable dataset + retrieval stack** (`index/index.json`, YAML frontmatter, Obsidian CLI, Ollama, RAG).

Guiding principles (derived from the work so far):

- **Metadata, not document bodies.** Only publicly available metadata, citations, links, process descriptions and freely available terminology (Electropedia). See [licensing.md](licensing.md).
- **Evidence over fluency.** Every factual answer must be traceable to a note/property/source URL. If the data is not in the vault, the answer must say so — not invent it.
- **Minimal stack.** Obsidian + Local LLM Helper + Ollama + a small CLI loop. No cloud, no browser automation, no REST API, no Git plugin, no unnecessary daemons.
- **One canonical dataset.** Frontmatter in notes ↔ `index/index.json` ↔ catalog/MOC tables must agree.

---

## 2. Problems / questions this project is designed to answer

These are the question classes the vault exists for. They are derived from the actual tests performed on this project (see [chat-optimization.md](chat-optimization.md)) and from standard engineering practice.

| # | Question class | Example | Where the answer comes from |
| --- | --- | --- | --- |
| Q1 | Identification / scope | "What is IEC 62443-4-1?" | Note description + title (`standards/`), Webstore source URL |
| Q2 | Commercial / availability | "What does IEC 62443-4-1 cost?" | `price_chf` in frontmatter + `index/index.json`; marked *as of crawl date* |
| Q3 | Classification | "What are the ICS tags of IEC 62813:2025/COR1:2026?" | `ics` property in `index/index.json` (e.g. 31.060.99) |
| Q4 | Lifecycle / status | "Is this an IS, TR, PAS, COR1 or AMD2? Which edition/year?" | `type`, `edition`, `published`, `status` |
| Q5 | Ownership | "Which technical committee owns this standard?" | `technical_committee` (TC/SC) |
| Q6 | Process / context | "How does a standard become published? What is consensus? Why is it slow?" | `processes/`, [iec-criticism.md](iec-criticism.md), [standards-bodies.md](standards-bodies.md) |
| Q7 | Comparison | "Compare IEC 62443-4-1 with IEC 61675-2" | Multiple notes + Dataview (`GROUP BY`, filters) |
| Q8 | Product-concept / compliance (future-facing) | "Which standard applies to my product? What must I verify? What information do I need?" | ICS/TC mapping + catalog; **requires** the engineer to map product → ICS/TC first (see §6 limits) |

**Question types engineers ask about their products (target taxonomy):**

1. **Applicability** — Which standard(s) apply to my device/system, given its function and market? (→ ICS, TC, title)
2. **Requirements orientation** — Which part of the series covers product development, system security, testing, marking, or installation? (→ part numbers, e.g. 62443-4-1 vs -4-2)
3. **Conformity evidence** — What documentation/test evidence is expected (test report forms, TRF, process requirements)? (→ TRF notes, type IS/TR/PAS)
4. **Scope boundary** — Who is addressed (developer, integrator, user) and what is explicitly *not* covered? (→ note descriptions, e.g. "-4-1 applies to developers/maintainers only")
5. **Status/timing** — Current edition, stability date, corrigenda/amendments, publication date. (→ frontmatter)
6. **Cost & access** — Price, where to obtain, what is free (Electropedia) vs paid (Webstore). (→ `price_chf`, licensing note)
7. **Terminology** — What does a term mean? (→ Electropedia/IEV, glossary)

This taxonomy is a **working model**, not a claim of exhaustive coverage. The vault currently answers Q1–Q7 reliably; Q8 is only partially supported (see §6).

---

## 3. Scope

### In scope

- Public metadata from official IEC Webstore product pages (title, ref, type, edition, dates, TC, ICS, price, stability date, languages, status, source URLs) — current: **23 entries** in `index/index.json`.
- IEC process/document-type knowledge (IS/TS/TR/PAS/ISH/IEV, development stages, SMB,Directives, Webstore terms).
- Freely available IEC terminology (Electropedia) and IEC Guides/newsletters.
- Critical perspective on standards bodies (SLOW, 85 % dominance, private SDO, strategic competition, PAS naming pattern) — [iec-criticism.md](iec-criticism.md), [standards-bodies.md](standards-bodies.md).
- Structured navigation: MOC, catalog, wikilinks, tags, Dataview queries, glossary.
- Local retrieval: `agent-loop.sh` (L1/L2/L3) and Local LLM Helper **RAG chat** with a local embedding model.
- Machine-readable index and note frontmatter as the single source of truth.

### Out of scope / non-goals

- **No IEC document bodies.** No full standard texts, no large verbatim excerpts (copyright).
- **No certification, legal or conformity advice.** The vault informs, it does not certify products.
- **No browser/Chrome automation, no cloud LLM, no hosted vector database.**
- **No attempt to cover all ~ tens of thousands of IEC publications.** Coverage is incremental and verified.
- **No silent writes.** All generated changes require human review (workflow approval pattern).
- The repository is private; "offen" preparation means licensing/data hygiene, not automatic publication.

---

## 4. Architecture (verified)

```
Active Obsidian GUI vault:  /Users/matthiasfahsold/Projects/IEC_Agentic
  └─ .obsidian/plugins/local-llm-helper/
       ├─ data.json        ← real chat settings (2b, nomic-embed-text)
       └─ embeddings.json  ← local RAG index (241 chunks, 768 dims)
  └─ iec-standards-obsidian-vault/   ← the Git repo (this vault's content)
       ├─ index/index.json          (machine-readable catalog, 23 entries)
       ├─ standards/                (standard notes + catalog + classics)
       ├─ processes/, electropedia/, guides/, news/
       ├─ meta/                     (charter, glossary, analysis, agent-loop.sh, ...)
       └─ README.md, index/index.md (human entry points)
```

**Two chat modes — important:**

- `llm-chat` = **general chat, NOT grounded in the vault.** It will answer "I cannot access external documents…" — do **not** use it for IEC facts.
- `rag-chat` = **grounded chat**: embeds the question, retrieves the top note chunks, sends them with the prompt. Commands: `local-llm-helper:rag-chat`, `rag-chat-current-note`, `rag-chat-current-folder`, `rag-diagnostics`.

**Verified stack (2026-11-20):**

| Component | State |
| --- | --- |
| Obsidian | 1.15.1 (GUI running; CLI v1.15.1) |
| Plugins | `local-llm-helper` 2.6.2, `dataview` enabled |
| Chat model | `qwen3.5:2b` (3.1 GB), thinking enabled (`reasoning` field), maxTokens 4096, temp 0.3 |
| Embedding model | `nomic-embed-text` (274 MB, 768 dims), RAG index built (241 chunks) |
| Endpoints | `http://localhost:11434` (Ollama 0.40.15, OpenAI-compatible `/v1/*`) |
| CLI loop | `agent-loop.sh` v6 — L1/L2/L3, REF-based note selection, ICS/price prompt guards |
| Repo | `mfahsold/iec-standards-obsidian-vault`, private, `main` → `origin/main`, clean |
| Health | 67 files (61 Markdown), 23 index entries, orphans = 1 (LICENSE, extensionless — expected) |

**Note:** `data.json` and `embeddings.json` live in the *GUI vault's* `.obsidian/` (git-ignored). A settings file placed in the repo's own `.obsidian/` has no effect — this caused the earlier "chat doesn't work" issue and was corrected.

---

## 5. Definition of Done

Work is "done" only at the level below that applies. Evidence, not intention, decides.

### 5.1 For a new/updated standard note

- [ ] YAML frontmatter contains: `ref`, `title`, `type`, `edition`, `technical_committee`, `published`, `ics`, `status`, `price_chf` (or `null`), `sources[]`, `tags`.
- [ ] Body contains: stand/date line, Description, Notes; **no IEC document bodies**; licensing/links present.
- [ ] Price/date marked "as of crawl date" with source URL; no invented values.
- [ ] Entry added to **all three**: `index/index.json`, `standards/index-standards.md`, `index/index.md` (MOC).
- [ ] Wikilinks to catalog/MOC/licensing; note is **not an orphan** (linked from MOC/catalog).
- [ ] `python3 -c "import json; json.load(open('index/index.json'))"` succeeds; entry count matches expectation.
- [ ] RAG index rebuilt: `obsidian command id=local-llm-helper:index-notes-rag`.

### 5.2 For a prompt / retrieval / configuration change

- [ ] At least one **golden question** with an evidence-backed expected answer is defined (see §2 table).
- [ ] It passes on **both paths**: CLI (`agent-loop.sh` L1/L2) and GUI (`rag-chat`).
- [ ] Answer is checked against `index/index.json` / note frontmatter (e.g. ICS 31.060.99, price 335 CHF).
- [ ] Wrong-answer patterns are explicitly guarded in the prompt (e.g. "IEC standards are free" → price directive).
- [ ] Documentation updated (`meta/chat-optimization.md`, this charter if behavior changed).
- [ ] Settings edited in the **GUI vault's** plugin `data.json`, followed by `obsidian plugin:reload id=local-llm-helper`.

### 5.3 For a commit / release

- [ ] `git status` clean; `main` equal to `origin/main` after push.
- [ ] `obsidian orphans total` = 1 (LICENSE only) — no new orphans.
- [ ] Plugins enabled: `dataview`, `local-llm-helper`.
- [ ] Commit message states the evidence/test result, not just the intent.

### 5.4 Project-level "done" (definition of complete for the prototype)

The prototype is considered **functionally complete** when:

1. All Q1–Q7 question classes in §2 return correct, cited answers on both CLI and GUI paths, using the golden-question set.
2. Catalog, notes and index are consistent; no orphans beyond LICENSE.
3. RAG index is current and retrieval top-1 is the expected note for the golden questions.
4. The full stack is documented here and in [chat-optimization.md](chat-optimization.md), with setup reproducible from this charter.
5. Licensing boundaries are respected (no document bodies) and the repo is push-clean.

Q8 (product-concept / conformity) is **stretch**: it needs a documented product→ICS→standard mapping workflow and is not required for prototype completion.

---

## 6. Known limitations (honest state)

- **Coverage**: 23 verified entries out of a very large standards universe. Absence from the vault is not evidence that a standard does not exist.
- **GUI pitfall**: the *general* chat is ungrounded; only RAG chat uses the notes. This is a plugin behavior, not a bug in the data.
- **Vault split**: the repo is a subfolder of the GUI vault; settings and RAG index are outside git. Backups must include both locations.
- **Prices/date** are crawl-time snapshots ("as of Crawl-Date") — always re-check the Webstore before relying on them commercially.
- **Critical content** (85 % dominance, SLOW, etc.) is sourced commentary, consensus-view — see the linked notes for provenance.
- **No conformity advice**: answering "which standard applies to my product" requires an engineering judgement the vault can support but not replace.

---

## 7. Key documents

- [README.md](../README.md) — quick start / stats.
- [index/index.md](../index/index.md) — MOC + full standards table.
- [final-analysis.md](final-analysis.md) — current analysis snapshot.
- [chat-optimization.md](chat-optimization.md) — chat/RAG configuration and test history.
- [glossary.md](glossary.md) — terminology network.
- [iec-criticism.md](iec-criticism.md), [standards-bodies.md](standards-bodies.md) — critical context.
- [licensing.md](licensing.md), [crawl-notes.md](crawl-notes.md) — legal/data provenance.
- [agent-loop.sh](agent-loop.sh) — CLI retrieval loop.

## MASTER

→ [index/index.md](../index/index.md)
