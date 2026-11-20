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
- evaluator: retrieval `12/12`, decisions `10/12`.

The two known judge limitations (multi-standard comparison and open-ended
“name three patterns”) may show FAIL — record them, do not treat them as a
release blocker.

## 3. Critical CLI questions

Run these three and compare with the expected outcome:

```sh
python3 tools/agent-loop.py "What are the ICS tags of IEC 62813:2025/COR1:2026?"
python3 tools/agent-loop.py "What is the price of IEC 62443-4-1:2018?"
python3 tools/agent-loop.py "What is IEC 65000-1:2099? Give me its ICS and price."
```

| # | Expected |
| --- | --- |
| 1 | `31.060.99` with a `[Source: …]` citation |
| 2 | `335 CHF`, snapshot hint, with a citation |
| 3 | “Not in the vault …” — no invented standard, no unrelated note cited |

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
| Evaluator retrieval | 12/12 | |
| Evaluator decisions | 10/12 | |
| CLI #1 ICS | 31.060.99 + citation | |
| CLI #2 price | 335 CHF + citation | |
| CLI #3 abstention | Not in the vault | |
| Obsidian navigation | links/graph/search work | |
| Repo clean | clean, in sync | |
| Public decision | yes/no | |

## Release gate

Go public only if:

- all three critical CLI questions pass;
- validator reports 0 errors;
- the repo is clean and in sync;
- the two known judge limitations are recorded, not hidden.

If any critical CLI question fails, stop and report the exact question, mode and
answer before flipping visibility.
