# Contributing

Thanks for helping improve this independent, unofficial aggregate of public
IEC/ISO metadata. This repository is not official IEC/ISO material and may
contain errors; contributions must keep it copyright-safe and verifiable.

## Ground rules

1. **Public sources only.** Use official public pages or clearly labelled public
   catalogues. Never use paywalled, login-protected, scraped, or purchased content.
2. **No document bodies.** No standard texts, PDFs, long verbatim excerpts,
   figures, or reconstructed tables of contents.
3. **Own words.** Paraphrase descriptions; keep quotations under ~25 words with
   quotation marks and a source link.
4. **Cite every fact.** Add a source URL to frontmatter and a collection date to
   the note body. Use `null` for unknown values — never invent data.
5. **Prices are snapshots.** Mark them as of the collection date and link the
   official catalog.
6. **No personal data or secrets.**
7. **Queries are generated.** Add probe templates to `tools/probes.py`; do not
   hardcode question lists.

## Adding or updating a standard note

1. Copy `templates/standard-note.md` into `standards/`.
2. Fill required frontmatter: `ref`, `title`, `type`, `status`, `languages`,
   `price_chf`, `sources`, `tags`.
3. Write a short original description; add source URLs and the collection date.
4. Add the entry to `index/index.json`, `standards/index-standards.md`, and
   `index/index.md`.
5. Run:

   ```sh
   python3 tools/validate_vault.py
   python3 tools/evaluate.py
   python3 tools/build-index.py
   ```

## Code changes

- Keep tools dependency-free (Python standard library).
- Add runtime defaults to `tools/config.py`, not individual scripts.
- Do not introduce a service, port, or daemon.
- Run `python3 -m py_compile tools/*.py` and the evaluator.

## Pull requests

Explain what changed and cite the public source for every new fact. Confirm that
no standard body, long quotation, secret, or absolute path was added, and that
all checks pass. By contributing, you license code under MIT and original
content under CC BY 4.0.

## Reports

Open a GitHub issue for questions or bugs. Use GitHub's private vulnerability
reporting for security concerns; do not commit secrets. Rights holders can
request review/removal via an issue.
