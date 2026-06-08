# Tableau Public — optional track

Compare drag-and-drop dashboarding with the Streamlit workshop on the **same**
Open Food Facts aggregates.

Tableau Public is free; everything you publish is **world-readable**. Do not
upload company or personal data.

## Why a pre-aggregated CSV?

Tableau Public caps uploads at ~15M rows. The lesson matches Streamlit:
**aggregate to the grain the chart needs, then plot**. We export category ×
Nutri-Score × country counts in DuckDB; Tableau draws them.

In Tableau Desktop you might use an Extract with “Aggregate data for visible
dimensions”. Public web authoring has no database connector — a small CSV is
the pragmatic path.

## 1. Export the CSV

From the repository root (`uv sync` done; Parquet at `data/openfoodfacts.parquet`):

```bash
uv run python session6/export_tableau_csv.py
# → data/off_grade_by_category.csv (few hundred rows)
```

The SQL lives in [`export_tableau_csv.py`](export_tableau_csv.py) — do not duplicate it elsewhere.

## 2. Build a dashboard (~30 min)

1. Sign in at https://public.tableau.com/ (free account)
2. **Create → Web Authoring** — no install required
3. Upload `data/off_grade_by_category.csv`
4. Suggested view (mirrors the Streamlit heatmap story at aggregate level):
   - Rows = `category`, Columns = `SUM(n)`, Color = `grade` (stacked bars)
   - Filter on `country` (single-select, like the Streamlit sidebar)
   - Title = **insight**, not variable names (Session 3 Big Idea rule)
5. **File → Save to Tableau Public As…** → copy the public URL

## 3. Ethics drill

Same sentence as the Streamlit workshop:

> *A careless reader of this chart would conclude __, but the data actually says __.*

Works on any medium — the question is about the chart, not the tool.

## What this track is good for

- Feeling drag-and-drop vs code-driven dashboarding on the same aggregates
- A second pass after finishing Streamlit
- Interview context (“I've used Tableau Public / Power BI-style tools”)

## Limitations

- **Privacy** — Public is world-readable
- **Reproducibility** — workbooks live on Tableau's servers; no git history
- **Refresh** — no API on the free tier; manual re-upload only

## Links

- [Tableau Public](https://public.tableau.com/)
- [Web Authoring help](https://help.tableau.com/current/pro/desktop/en-us/web_author_home.htm)
- [Gallery](https://public.tableau.com/app/discover) — design references
