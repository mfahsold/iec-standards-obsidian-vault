# Data Policy — Public, Copyright-Safe Metadata

This project is a **metadata and retrieval** knowledge base. It is not a
replacement for the official standards, and it does not distribute standard
texts.

## What we include

- Standard references, titles, document types, editions, publication dates,
  stability dates, technical committees, ICS codes, languages, and status.
- Price snapshots from public product pages, marked with the collection date.
- Links to official product pages and public process documents.
- Our own short summaries of scope and context.
- Short quotations from public pages, with quotation marks, attribution, and a
  link.
- Public terminology references (e.g., Electropedia) with attribution.

## What we never include

- PDFs or full texts of IEC, ISO, CISPR or other standards.
- Long verbatim excerpts, reconstructed tables of contents, figures, or
  translated document bodies.
- Content obtained by scraping paywalled, login-protected, or prohibited
  sources.
- Purchased standards content.
- Personal data, credentials, API keys, or machine-specific paths.

## Source rules

1. Prefer official public sources: IEC Webstore product pages, IEC website
   pages, public IEC Open PDFs, ISO pages, Electropedia.
2. Third-party aggregators may be used only for references/titles, not as
   authoritative sources for prices or technical details. Label them clearly.
3. Record the source URL in the note's `sources` frontmatter.
4. Record the collection date in the note body (e.g., “Data as of 2026-11-20”).
5. If a fact cannot be verified from a public source, use `null` or omit it.
   Never fill gaps with plausible-sounding data.

## Quotation rules

- Keep quotations short — aim for **25 words or fewer**.
- Use quotation marks and attribute the source inline.
- Do not reproduce a complete paragraph, section, abstract, or table from a
  standards body.
- Paraphrase in your own words whenever possible.
- When in doubt, link instead of quoting.

## AI / RAG rules

- Index only the notes in this repository.
- Do not feed purchased or paywalled IEC/ISO documents into a model, embedding
  index, or retrieval system.
- Answers must cite the note they came from.
- If the vault does not contain the answer, the correct answer is “not in the
  vault” — not an invented fact.
- Treat contributed notes as untrusted input; review them before indexing.

## Prices and dates

Prices change. Every price in this repository is a snapshot from the date shown
and is **not authoritative**. The official catalog is the only current source.
The same applies to publication dates, stability dates, and status values.

## Trademarks and affiliation

IEC, ISO, CISPR and related names are trademarks of their respective owners.
They are used here only to identify the standards being discussed. This project
is independent and is not affiliated with or endorsed by any standards body.

## Review checklist for contributors

- [ ] The note contains no standard body text, PDF, or long verbatim excerpt.
- [ ] The description is an original paraphrase.
- [ ] Every fact has a public source URL.
- [ ] The collection date is recorded.
- [ ] Prices are marked as snapshots.
- [ ] No personal data, secrets, or absolute local paths.
- [ ] The note is linked from the catalog and MOC.
- [ ] `python3 tools/validate_vault.py` passes.

## Rights-holder requests

If you are a rights holder and believe content in this repository exceeds
acceptable use, please open an issue or contact the maintainers. We will review
and remove or amend the material promptly.

## Further reading

- [`NOTICE.md`](../NOTICE.md) — third-party notices and disclaimers.
- [`docs/iec-engagement.md`](iec-engagement.md) — questions prepared for IEC.
- [`docs/provenance.md`](../docs/provenance.md) — summary of IEC terms.
- [`docs/provenance.md`](../docs/provenance.md) — source list.
