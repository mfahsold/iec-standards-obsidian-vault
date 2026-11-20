# Provenance, Sources and Licensing Status

## How data was collected

All data was collected manually from public pages on 2026-11-19 and
2026-11-20. No automated scraping of the IEC Webstore was used. References from
third-party aggregators are used only for standard identifiers in
`standards/classics.md`; prices and technical details are not taken from them.

## Official sources

| Source | Used for |
| --- | --- |
| <https://webstore.iec.ch/en/products/> | Catalog navigation |
| <https://webstore.iec.ch/en/publication/…> | Product metadata and price snapshots |
| <https://webstore.iec.ch/en/terms-conditions/> | Webstore terms summary |
| <https://iec.ch/faq> | Process FAQ |
| <https://iec.ch/standards-development/workflows> | Publication types |
| <https://iec.ch/publications/international-standards> | IS definition, consensus, voluntary adoption |
| <https://iec.ch/publications/specifications> | TS and PAS definitions |
| <https://iec.ch/publications/technical-reports> | TR definition |
| <https://iec.ch/standards-development/work-programme> | Work programme and target dates |
| <https://iec.ch/standards-development/drafting-publications-overview> | Publication lifecycle |
| <https://iec.ch/online-standards-development> | OSD platform |
| <https://www.prd.iec.ch/acp/standardization-affiliates> | Affiliate rules |
| <https://www.electropedia.org/iev/iev.nsf/Welcome> | IEV reference |
| IEC Open PDFs (Directives, stage codes) | Stage names and codes |
| <https://www.iso.org/sites/directives/current/part2/index.xhtml> | ISO definitions |

Third-party references: <https://www.normfile.com/iec.html> (classics only),
<https://standards.iteh.ai/> (ISO 14678 metadata).

## Verified catalog entries (23)

The catalog is recorded in `index/index.json`, `standards/index-standards.md`,
and `index/index.md`. It covers IS, ISO/IEC, TRF, PAS, TR, COR1, AMD2, and ISO
documents. Every entry has a `sources` URL; prices are snapshots with a
collection date.

## Price and date policy

Prices were read from public product pages on the collection date. They change; the
official catalog is the only current source. The vault marks them as snapshots
and links to the product page. The same applies to publication and stability
dates.

## Licensing status

| Material | License |
| --- | --- |
| Code (scripts, CI) | MIT — `LICENSES/MIT.txt` |
| Original content and metadata compilation | CC BY 4.0 — `LICENSES/CC-BY-4.0.txt` |
| IEC/ISO names, titles, metadata | Owned by the respective organizations; used for identification only |
| Third-party quotations | Original terms; short, attributed, linked |

The vault contains no IEC or ISO document bodies, PDFs, or long verbatim
excerpts. It is not affiliated with or endorsed by any standards body.

The exact reuse terms for IEC-derived metadata and its use in a local retrieval
tool are being clarified with the IEC. See `docs/iec-engagement.md`. Any changes
requested by the IEC will be applied to the catalog and documentation.

## Related

- `docs/data-policy.md` — rules for current contributions
- `docs/iec-engagement.md` — open questions for IEC
- `NOTICE.md` — third-party notices
- `LICENSE` — license overview
