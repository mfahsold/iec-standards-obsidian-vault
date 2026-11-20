# Data Policy

This is an independent, unofficial aggregate of publicly available information —
not official IEC/ISO communication or documentation, and potentially erroneous.
It is a metadata and retrieval knowledge base, not a replacement for standards.
The catalog is a **verified subset**, not a complete IEC catalog; before growing
beyond the review threshold in `tools/config.py`, IEC should be consulted.

## Included

- Public metadata: references, titles, document types, editions, dates,
  committees, ICS codes, languages, status.
- Price snapshots from public product pages, marked with the collection date.
- Links to official product pages and public process documents.
- Original summaries and source links; no direct quotations.

## Never included

- Standard bodies, PDFs, long verbatim excerpts, figures, or tables of contents.
- Scraped, paywalled, login-protected, or purchased content.
- Personal data, credentials, API keys, or machine-specific paths.

## Source rules

1. Prefer official public sources: IEC Webstore, IEC website, IEC Open PDFs, ISO
   pages, Electropedia.
2. Third-party aggregators are allowed only for identifiers and must be labelled.
3. Record the source URL in frontmatter and the collection date in the note.
4. Use `null` or omit unverifiable facts; never invent values.

## No direct quotations

Do not reproduce wording from IEC/ISO pages. Paraphrase the fact and link the
source. Never copy a paragraph, abstract, section, or table.

## AI/RAG rules

Index only this repository's notes. Never feed purchased IEC/ISO documents into
a model or index. Answers must cite a source; absent facts produce “not in the
vault”, not a guess. Treat contributed notes as untrusted input.

## Prices, dates, trademarks

Prices and dates are collection-time snapshots; the official catalog is current.
IEC, ISO, CISPR names and marks belong to their owners and are used only for
identification. This project is not affiliated with or endorsed by any standards
body.

## Review checklist

- [ ] No standard body, PDF, or long verbatim excerpt.
- [ ] Description is an original paraphrase with source URL and date.
- [ ] Prices marked as snapshots.
- [ ] No personal data, secrets, or absolute paths.
- [ ] Note linked from catalog/MOC.
- [ ] `python3 tools/validate_vault.py` passes.

## Further reading

[`NOTICE.md`](../NOTICE.md), [`docs/provenance.md`](provenance.md),
[`docs/iec-engagement.md`](iec-engagement.md),
[`processes/webstore-terms.md`](../processes/webstore-terms.md).
