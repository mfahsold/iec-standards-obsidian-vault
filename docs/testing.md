# Manual Test Plan (before going public)

Work through these steps and record the results below. No counts or settings are
hardcoded here — get live values from `python3 tools/config.py --show`.

## 1. Rebuild local state

```sh
python3 tools/build-index.py
python3 tools/config.py --show
```

Confirm the RAG index was rebuilt and the catalog entries match `index/index.json`.

## 2. Automated checks

```sh
python3 -m py_compile tools/*.py
python3 tools/validate_vault.py
python3 tools/evaluate.py
```

Expect: no compile errors, `0 error(s), 0 warning(s)`, and all generated probes
passing. The evaluator prints the current scores; record them.

## 3. Generated CLI smoke tests

Questions are generated from the catalog, not hardcoded:

```sh
python3 tools/probes.py --cli | head -3 | sh    # ANSWER probes
python3 tools/probes.py --cli | tail -1 | sh    # REFUSE probe
```

Expect: catalog values with `[Source: …]` citations for ANSWER probes; “Not in
the vault …” with no invented data for REFUSE probes. Pass rule: 2–3 sentences,
correct value, citation present, no invented facts.

## 4. Obsidian GUI

Open the vault; check the MOC, links, graph, backlinks, and search. Optional: test
the IEC Vault terminal profile or the “Ask vault” plugin; its answer must match
the CLI. GUI answers are not authoritative.

## 5. Repository readiness

```sh
git status --short --branch
git diff --check
```

Expect clean tree, in sync with `origin/main`. Confirm license/notice files, no
PDFs/secrets/absolute paths, `index/embeddings*.json` gitignored, English-only
docs, and the non-official disclaimer present.

## 6. Result record

| Check | Expected | Result |
| --- | --- | --- |
| Index rebuild + config view | matches catalog | |
| Compile + validator | 0 errors | |
| Evaluator | all probes pass | |
| Generated ANSWER probes | values + citations | |
| Generated REFUSE probe | Not in the vault | |
| Obsidian navigation | links/graph/search work | |
| Repo clean | clean, in sync | |
| Public decision | yes/no | |

## Release gate

The release gate is: all generated probes pass, the validator reports 0 errors,
the repo is clean, and results are recorded. If anything fails, stop and report
the exact generated question and answer before publishing a new tag or release.
