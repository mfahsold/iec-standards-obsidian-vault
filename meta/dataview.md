# Dataview — Query Examples for this Vault

Install the **Dataview** community plugin and use these queries in notes or via inline DQL. Data source: frontmatter of `standards/` notes.

## Tables

```dataview
TABLE
  type AS Type,
  edition AS Edition,
  technical_committee AS "TC/SC",
  published AS Published,
  ics AS ICS,
  price_chf AS Price,
  status AS Status
FROM "standards"
SORT ref
LIMIT 200
```

```dataview
TABLE
  type AS Type,
  technical_committee AS "TC/SC",
  price_chf AS Price,
  status AS Status
FROM "standards"
WHERE type = "PAS" OR type = "TRF" OR type = "TR"
SORT ref
```

```dataview
TABLE
  technical_committee AS "TC/SC",
  length(rows) AS "Count"
FROM "standards"
GROUP BY technical_committee
SORT length(rows) DESC
```

```dataview
TABLE ics, type, price_chf, status
FROM "standards"
WHERE ics != ""
SORT ics
```

```dataview
TABLE ref, price_chf
FROM "standards"
WHERE price_chf != null AND price_chf >= 200 AND price_chf <= 500
SORT price_chf ASC
```

## Lists

```dataview
LIST
FROM "standards" WHERE contains(tags, "security") AND status = "active"
SORT ref
```

```dataview
LIST
FROM #security
```

## Agent-Readability (no plugin needed)

- [index/index.json](../index/index.json) — raw JSON array of all vault standards (ref, type, edition, TC, ICS, status, price, sources) — parse directly for tools/agents.

## MASTER
