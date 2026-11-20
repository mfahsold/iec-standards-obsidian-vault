# Manual Test Plan (before going public)

Keep this simple. Work through the steps in order and record the results in the
table at the end. Expected total time: ~15 minutes.

## 0. Prerequisites

- Ollama is running and both models are present:

  ```sh
  ollama list | grep -E 'qwen3.5:2b|nomic-embed-text'
  ```

- Obsidian opens this repository as a vault.
- You are in the repository root in your terminal.

## 1. Rebuild the index

```sh
python3 tools/build-index.py
```

Expected: a line like `Indexed 300 chunks from 52 files`. If note files changed,
this is required before any question test.

## 2. Automated checks

```sh
python3 -m py_compile tools/*.py
python3 tools/validate_vault.py
python3 tools/evaluate.py
```

Expected:
- compile: no output;
- validator: `0 error(s), 0 warning(s)`;
- evaluator: retrieval `13/13`, decisions `13/13`.

Probes are generated from `index/index.json`; no hardcoded question list exists.
If a probe fails, report the generated question and the catalog entry it came
from.

## 3. Critical CLI questions

Questions are generated from the catalog — nothing to hardcode:

```sh
python3 tools/probes.py --cli | head -3 | sh
```

This runs the first three generated probes (currently ICS and price questions).
For the abstention check, run one generated `REFUSE` probe:

```sh
python3 tools/probes.py --cli | tail -1 | sh
```

Expected: the value from `index/index.json` with a `[Source: …]` citation for
`ANSWER` probes; “Not in the vault …” with no invented data for `REFUSE` probes.

Pass rule: 2–3 sentences, correct value, citation present, no invented facts.

Optional full answer check (slow, ~2 minutes):

```sh
python3 tools/evaluate.py --generate
```

## 4. Obsidian GUI check

- Open the vault; start at `README.md` and `index/index.md` (MOC).
- Confirm links, graph view, backlinks and search work.
- Optional: install a terminal plugin with the **IEC Vault** profile from
  `docs/setup.md`, then run one CLI question from inside Obsidian.
- Optional: copy `obsidian-plugin/` into the GUI vault and enable **IEC Vault
  Ask**; click the ribbon icon and ask one question. The answer must match the
  CLI result — the plugin is only a wrapper.

There is no chat authority in the GUI; any GUI answer must be re-verified with
the CLI.

## 5. Repository readiness

```sh
git status --short --branch
git diff --check
```

Expected: clean tree, on `main`, in sync with `origin/main`.

Also confirm:
- `LICENSE`, `NOTICE.md`, `CONTRIBUTING.md` exist;
- no `*.pdf`, no `.env`, no absolute `/Users/…` paths in tracked files;
- `index/embeddings*.json` is gitignored;
- all documentation is in English.

## 6. Result record

| Check | Expected | Result (OK / FAIL) |
| --- | --- | --- |
| Index rebuild | chunks from 52 files | |
| Compile + validator | 0 errors | |
| Evaluator retrieval | 13/13 | |
| Evaluator decisions | 13/13 | |
| First 3 generated ANSWER probes | catalog value + citation | |
| One generated REFUSE probe | Not in the vault | |
| Obsidian navigation | links/graph/search work | |
| Repo clean | clean, in sync | |
| Public decision | yes/no | |

## Release gate

Go public only if:

- the generated ANSWER and REFUSE probes pass;
- validator reports 0 errors;
- the evaluator reports 13/13 retrieval and 13/13 decisions;
- the repo is clean and in sync.

If any critical CLI question fails, stop and report the exact question, mode and
answer before flipping visibility.
