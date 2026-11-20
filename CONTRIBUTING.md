# Contributing

Thanks for your interest in improving the IEC Standards Knowledge Vault. This
project is a public, local-first knowledge base for **metadata about** IEC/ISO
standards — not a copy of the standards themselves.

## Ways to contribute

- Add or correct a standard note in `standards/`.
- Improve the process documentation in `processes/`.
- Fix a broken link, typo, or inconsistent metadata field.
- Improve the retrieval tools in `tools/`.
- Add a golden question with an evidence-backed expected answer.

## Ground rules (important)

This project is built to be copyright-safe. By contributing, you agree that:

1. **No document bodies.** Do not paste IEC/ISO/CISPR standard texts, PDFs,
   tables of contents, figures, or long verbatim excerpts.
2. **Public sources only.** Use official public pages (IEC Webstore, IEC
   website, public IEC Open PDFs, Electropedia, ISO pages) or clearly identified
   public third-party catalogs. Do not use paywalled, login-protected, or
   scraped content.
3. **Write your own summaries.** Descriptions must be paraphrases in your own
   words. Short quotations are allowed only when necessary: keep them under
   about 25 words, put them in quotation marks, and link the source.
4. **Cite every fact.** Add the source URL to the note's `sources` frontmatter
   and record the collection date.
5. **Prices are snapshots.** Mark them “as of” the collection date and link the
   official product page. Never present a price as current or authoritative.
6. **No personal data or secrets.** Do not commit API keys, tokens, local
   absolute paths, email addresses, or machine-specific configuration.

The full policy is in [`docs/data-policy.md`](docs/data-policy.md). The
maintainers may remove content that does not meet these rules.

## Adding or updating a standard note

1. Copy [`templates/standard-note.md`](templates/standard-note.md) into
   `standards/` and name it after the reference, e.g.
   `standards/IEC-62443-4-1-2018.md`.
2. Fill in the frontmatter. Required fields:
   `ref`, `title`, `type`, `status`, `languages`, `price_chf`, `sources`,
   `tags`.
3. Write a short, original description (2–4 sentences) and a “Notes” section.
4. Add the entry to **all three** places:
   - `index/index.json`
   - `standards/index-standards.md`
   - `index/index.md`
5. Link the note from at least one other note (the catalog/MOC links count).
6. Run the validator:

   ```sh
   python3 tools/validate_vault.py
   ```

7. Rebuild the RAG index after adding files:
   `python3 tools/build-index.py`. See [`docs/setup.md`](docs/setup.md).

## Frontmatter schema

See [`templates/standard-note.md`](templates/standard-note.md) for the
authoritative schema. Keep field names and value formats consistent with the
existing notes. Dates use `YYYY-MM-DD`; unknown values use `null` or an empty
string, never invented data.

## Code contributions

- Keep the CLI loop POSIX `sh` compatible.
- Prefer the Python standard library; do not add dependencies without a clear
  reason.
- Run `python3 tools/validate_vault.py` and `python3 -m py_compile tools/*.py`.
- Keep prompts grounded: answers must cite the source note and must refuse to
  invent standards, ICS codes, prices, or citations.

## Pull requests

A good PR:

- explains **what** changed and **why**;
- states the evidence/source for any new or changed fact;
- keeps unrelated changes out;
- passes CI (`Validate vault`);
- confirms that no copyrighted standard body or long verbatim excerpt was
  added.

Use clear commit messages. Small, focused commits are preferred.

## Licensing of contributions

By submitting a contribution, you agree that:

- code contributions are licensed under the MIT License;
- original content contributions are licensed under CC BY 4.0;

as described in [`LICENSE`](LICENSE). You confirm that you have the right to
submit the material and that it does not violate third-party rights.

## Questions and reports

Open a GitHub issue for questions and non-sensitive bug reports. For security
concerns, use GitHub's private vulnerability reporting for this repository (or
contact the maintainers privately through their GitHub profile). Do not commit
secrets, tokens, or personal paths.
