# OFF dataset rules for the agent

These rules ground nao's SQL generation against the Open Food Facts
sample (`products` table in `off-local`).

## Columns

- `product_name` — free text, often non-English; do not pattern-match
- `brands` — semi-colon-separated free text; split before grouping
- `countries_en` — single English country name; one value per row
- `pnns_groups_1`, `pnns_groups_2` — categorical, contain literal value `'unknown'`
  that must be filtered out when summarising
- `nutriscore_grade` — letter A–E, **ordered categorical**. Treat as
  ordinal; never compute a numeric mean or sum over it
- `nova_group` — integer 1–4; higher = more processed
- `energy_kcal_100g`, `fat_100g`, `sugars_100g`, `salt_100g`, `proteins_100g`,
  `fiber_100g` — numeric per 100 g
- `created_t`, `last_modified_t` — Unix epoch seconds. Wrap in
  `to_timestamp(...)` before any date function

## Defaults

- When a question is ambiguous, prefer COUNT + GROUP BY rather than a
  single scalar
- When a categorical column has `'unknown'`, filter it out unless the
  user explicitly asks for it
- For "average" / "median" requests on `nutriscore_grade`, return a
  grade-by-grade count and surface the limitation, rather than silently
  mapping to integers
- Sort grade categories in the canonical order A, B, C, D, E (not by count)

## Charting

- Time series → line chart
- Distribution over a small categorical → bar chart, sorted by natural order
- Two categoricals → heatmap with share-within-group, not raw counts
