# Provenance and Licensing Status

Data was taken from public pages on 2026-11-19/20. No automated Webstore scraper
was used. Whether systematic manual collection of public catalog pages counts as
“data mining” under the IEC terms is one of the questions submitted to IEC;
see `docs/iec-engagement.md`. Third-party aggregators appear only as identifier
references in `standards/classics.md`. The current catalog size is reported by
`python3 tools/config.py --show`.

## Sources

- IEC Webstore: product pages, catalog navigation, terms, FAQ.
- IEC website: process FAQ, publication types, work programme, lifecycle, OSD,
  affiliate rules.
- IEC Open PDFs: Directives and stage codes (linked, not copied).
- ISO Directives, Electropedia, public third-party catalogues (identifiers only).

Every standard note records its source URL in frontmatter; the full source list is
in that frontmatter and in `index/index.json`.

## Licensing status

| Material | Status |
| --- | --- |
| Code | MIT — `LICENSES/MIT.txt` |
| Original content and metadata compilation | CC BY 4.0 — `LICENSES/CC-BY-4.0.txt` |
| IEC/ISO names, titles, metadata | Owned by the respective organizations; identification only |
| Short third-party quotations | Original terms; attributed and linked |

No IEC/ISO document bodies, PDFs, or long verbatim excerpts are included. This is
not official IEC/ISO material and may contain errors; see [`NOTICE.md`](../NOTICE.md).

The IEC Webstore Terms (version 2025-08-04) govern IEC Products sold through the
Webstore: copyright, no unauthorised copying or scraping, and no AI/ML use of
those publications without specific permission. This project uses only public
bibliographic metadata and links, not IEC Products, and does not ingest purchased
IEC content into any model. Exact reuse terms for IEC-derived metadata are being
clarified with IEC; see `docs/iec-engagement.md`. IEC-requested changes will be
applied to the catalog and documentation.

## Related

`docs/data-policy.md`, `docs/iec-engagement.md`, `NOTICE.md`, `LICENSE`,
`processes/webstore-terms.md`.
