# Manual Test Sheet

Work through the checks in order and tick them. Live values come from
`python3 tools/config.py --show`; nothing here hardcodes counts or versions.

## A. Local data and code

```sh
cd <repo-folder>    # new clones: unofficial-iec-metadata-vault; this workspace: iec-standards-obsidian-vault
python3 tools/build-index.py
python3 tools/config.py --show
python3 -m py_compile tools/*.py
python3 tools/validate_vault.py
python3 tools/evaluate.py
```

- [ ] Index rebuilt; chunk/file count matches the live catalog view.
- [ ] Python compile produces no errors.
- [ ] Validator: `0 error(s), 0 warning(s)`.
- [ ] Evaluator: all generated probes pass; scores recorded below.

## B. Answer quality (generated questions, nothing hardcoded)

```sh
python3 tools/probes.py --cli | head -3 | sh    # ANSWER probes
python3 tools/probes.py --cli | tail -1 | sh    # REFUSE probe
```

- [ ] ANSWER probes: correct catalog value, 2–3 sentences, `[Source: …]` citation.
- [ ] REFUSE probe: “Not in the vault …”, no invented standard, no unrelated source.
- [ ] Optional full check: `python3 tools/evaluate.py --generate`.

Record: retrieval ____/____ · decisions ____/____ · answers ____/____

## C. Obsidian / optional GUI

- [ ] Vault opens; `index/index.md` (MOC) works; links, graph, backlinks and search respond.
- [ ] Optional terminal profile **IEC Vault** starts in the repo folder.
- [ ] Optional “Ask vault” plugin ribbon icon works and its answer matches the CLI.
- [ ] GUI output is treated as non-authoritative.

## D. Documentation and legal boundary

- [ ] README has: description, disclaimer, scope, Vision/Scope/DoD, Requirements, Installation, Configuration, licensing.
- [ ] `docs/data-policy.md` contains the **Bring-your-own documents** boundary.
- [ ] No direct IEC quotations anywhere (`git grep -n '^> ' -- '*.md'` shows only the template TL;DR).
- [ ] `NOTICE.md`, `LICENSE`, `docs/takedown.md`, `docs/iec-email.md` exist and are linked.
- [ ] All documentation is in English; “non-commercial” is explained as intent, not a CC BY restriction.
- [ ] Project/repo name is “Unofficial IEC Metadata Vault” / `unofficial-iec-metadata-vault`.

## E. Repository and release

```sh
git status --short --branch
git diff --check
gh repo view --json description,homepageUrl,repositoryTopics,visibility
git ls-remote --tags origin v0.1.0
```

- [ ] `main` clean and in sync with `origin/main`; no whitespace errors.
- [ ] GitHub About has description, homepage and topics; repository is PUBLIC.
- [ ] Tag `v0.1.0` points to the current release commit.
- [ ] No PDFs, secrets, absolute paths, or `index/embeddings*.json` tracked.

## Release gate

Only publish a new tag/release if sections A, B, D and E are fully ticked. If a
probe fails, stop and report the exact generated question, mode and answer.
