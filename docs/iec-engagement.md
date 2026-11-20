# IEC Engagement — Questions for Clarification

Status: **pending** (the maintainers are clarifying reuse terms with the IEC).
This document is a preparation aid, not legal advice.

The goal is to publish a public, non-commercial, local-first knowledge base that
contains **metadata about** IEC publications and **original summaries**, but no
standard bodies. We want to confirm that this use is acceptable and to follow
any attribution or permission requirements IEC specifies.

## What the project does

- Publishes a catalog of IEC standards with factual metadata: reference, title,
  type, edition, publication date, technical committee, ICS codes, language,
  status, and a price snapshot with the collection date.
- Links every entry to the official IEC Webstore product page.
- Provides original, short summaries of scope and context.
- Uses the metadata in a **local** retrieval/LLM tool that answers questions and
  cites the vault note. No purchased IEC content is ingested.
- Includes no IEC PDFs, no full texts, and no long verbatim excerpts.

## Questions for IEC

### 1. Catalog metadata

May we publish and maintain a public catalog containing references, titles,
editions, publication dates, technical committees, ICS codes, languages,
status, and price snapshots (with source links and collection dates)?

### 2. AI / retrieval use

May we use this **metadata** (not IEC document bodies) in a local
retrieval-augmented generation (RAG) tool that answers user questions and cites
the metadata note? The tool runs locally; no IEC content is sent to a cloud
service.

### 3. Attribution

What attribution wording and placement would IEC prefer? For example:

> “IEC standard references and metadata are used for identification only.
> Source: IEC Webstore. This project is not affiliated with or endorsed by IEC.”

### 4. Names and marks

May we use “IEC”, standard references, and committee names in a nominative
way (to identify the standards), together with a clear “not affiliated”
disclaimer? We do not use IEC logos.

### 5. Price display

Are there restrictions on displaying price snapshots from public product pages?
We mark them “as of [date]” and link the official page, but we can remove prices
entirely if preferred.

### 6. Short quotations

May we include occasional short quotations (target: 25 words or fewer) from
public IEC web pages, with quotation marks, attribution, and a link? If not, we
will paraphrase everything.

### 7. Electropedia / IEV

For Electropedia terms, is linking plus short attributed term/definition
quotations acceptable? We do not plan a bulk import. If a license is required
for a larger term index, what is the process?

### 8. Public process documents

May we summarize and link public IEC Open PDFs (e.g., ISO/IEC Directives,
stage codes) with short quotations? We currently link rather than copy.

### 9. Takedown / review

If any content is not acceptable, what is the preferred contact and process for
review or removal?

## Suggested message

```text
Hello IEC Webstore team,

We maintain an independent, non-commercial open-source knowledge base that
catalogs public metadata about IEC standards (references, titles, editions,
committees, ICS codes, dates, prices with source links) and provides original
short summaries. It contains no IEC document bodies, PDFs, or long excerpts.
The metadata is also used in a local, offline retrieval tool that cites the
catalog. We are not affiliated with IEC and do not use IEC logos.

Could you please confirm whether this use is acceptable, what attribution you
prefer, and whether you have any requirements for price snapshots or short
quotations from public web pages? If a permission or license is required, we
would appreciate guidance on the process.

Thank you.
```

## Contact

- IEC Webstore contact: https://webstore.iec.ch/en/contact/
- IEC terms: https://webstore.iec.ch/en/terms-conditions/

## Internal notes

- Until clarification is received, the repository includes only metadata,
  original summaries, links, and short attributed quotations.
- If IEC requests changes, the maintainers will update or remove the affected
  content. The data policy is in [`data-policy.md`](data-policy.md).
- This document is not legal advice.
