# IEC Engagement — Questions for Clarification

Status: **questionnaire to be sent in parallel with the public release**. The
repository is already public under the disclaimers in `README.md` and `NOTICE.md`;
if IEC requests changes, they will be applied. This document is a preparation
aid, not legal advice.

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

What attribution wording and placement would IEC prefer? A possible wording is:
IEC references and metadata are used for identification only, with IEC Webstore
as the source; this is an unofficial aggregate of public information, not
official IEC documentation, may contain errors, and is not affiliated with IEC.

### 4. Names and marks

May we use “IEC”, standard references, and committee names in a nominative
way (to identify the standards), together with a clear “not affiliated”
disclaimer? We do not use IEC logos.

### 5. Price display

Are there restrictions on displaying price snapshots from public product pages?
We mark them “as of [date]” and link the official page, but we can remove prices
entirely if preferred.

### 6. No direct quotations

We currently paraphrase all public pages and link the sources; we do not
reproduce IEC wording. Is this the preferred approach, or is attribution alone
sufficient if short quotations were used in future?

### 7. Electropedia / IEV

Is linking to Electropedia without reproducing term definitions acceptable? We
do not bulk-import or copy definitions.

### 8. Public process documents

We summarize and link public IEC Open PDFs (e.g., ISO/IEC Directives, stage
codes) without copying text. Is that acceptable?

### 9. Takedown / review

If any content is not acceptable, what is the preferred contact and process for
review or removal?

### 10. Database and compilation rights

Does IEC consider a small, attributed, non-exhaustive catalog of public
bibliographic metadata (references, titles, ICS codes, dates, price snapshots,
source links) to be acceptable, or does it require a licence even for such a
subset? At what size or scope would IEC consider it a database re-publication?

## Suggested message

```text
Hello IEC Webstore team,

We maintain an independent, non-commercial open-source knowledge base that
catalogs public metadata about IEC standards (references, titles, editions,
committees, ICS codes, dates, prices with source links) and provides original
short summaries. It contains no IEC document bodies, PDFs, or long excerpts.
The metadata is also used in a local, offline retrieval tool that cites the
catalog. We are not affiliated with IEC and do not use IEC logos. We state
prominently that this is not official IEC communication or documentation of any
kind, that it is an unofficial aggregate of public information, and that it may
contain errors.

Could you please confirm whether this use is acceptable, what attribution you
prefer, and whether you have any requirements for price snapshots? We currently
paraphrase all public pages and do not reproduce IEC wording. Do you consider this small, attributed,
non-exhaustive metadata catalog acceptable, or is a licence needed even for a
subset? If a permission or license is required, we would appreciate guidance on
the process.

Thank you.
```

## Contact

- IEC Webstore contact: https://webstore.iec.ch/en/contact/
- IEC terms: https://webstore.iec.ch/en/terms-conditions/

## Internal notes

- The project name and GitHub URL slug are now **Unofficial IEC Metadata Vault**
  / `unofficial-iec-metadata-vault` (renamed 2026-11-20). GitHub redirects the old
  URL. The local folder name is unchanged for path stability.
- Until clarification is received, the repository includes only metadata,
  original summaries, links, and paraphrases only.
- If IEC requests changes, the maintainers will update or remove the affected
  content. The data policy is in [`data-policy.md`](data-policy.md).
- This document is not legal advice.
