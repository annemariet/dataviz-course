# Session 6: Dashboards, AI-assisted BI, Ethics

Workshop code for the Open Food Facts analytical dashboard. Slides live in
[`slides/session6_dashboarding.md`](../slides/session6_dashboarding.md).

## Quick start (Streamlit)

From the **repository root**:

```bash
uv sync --extra s6
uv run streamlit run session6/streamlit_app.py
```

Opens at http://localhost:8501. You need `data/openfoodfacts.parquet`, the same
file as Sessions 3–5 (see the [root README](../README.md#open-food-facts-parquet-1-gb)).

## Workshop content

| Part | What you do |
|------|-------------|
| **Streamlit** | Extend the starter dashboard (default track) |
| **Tableau** (optional) | No-code comparison. Follow instructions in [`tableau.md`](tableau.md) |
| **Nao** (optional) | Agentic BI library. Follow instructions in [`nao.md`](nao.md) |

## Files

```
session6/
├── README.md                 # this guide
├── streamlit_app.py          # layout + charts (UI only)
├── off_dashboard_queries.py  # DuckDB queries + @st.cache_data
├── export_tableau_csv.py     # aggregate Parquet → CSV (Tableau track)
├── build_off_db.py           # Parquet → DuckDB (Nao track)
├── tableau.md                # Tableau Public steps
├── nao.md                    # optional agentic BI appendix
└── nao-workspace/            # nao_config.yaml + RULES.md
```

Generated data (gitignored): `session6/data/off.duckdb`, `data/off_grade_by_category.csv`.

## Main workshop: extend the Streamlit dashboard

Two files, one convention: **queries in** `off_dashboard_queries.py`, **charts in**
`streamlit_app.py`.

### Build order

1. **1.1–1.4** (starter): KPI query, two KPI tiles, Nutri-Score bar chart
2. **2.1–2.3**: `@st.cache_data` on queries; optional sidebar timing to show cache hits
3. **3.1–3.2**: Extra KPIs (`unknown`, `not-applicable`, NOVA-4 %) in queries → metrics in app
4. **4.1–4.2**: `query_nova_distribution` → horizontal bar chart (copy Nutri-Score panel)
5. **5.1–5.2**: `query_top_categories` → top-10 horizontal bar
6. **6.1–6.2**: `query_category_nutri_score` (with `share` column) → heatmap (`mark_rect`)

Query stubs for steps 4–6 are already in `off_dashboard_queries.py`; the app has
placeholder panels. Wire them up by copying the Nutri-Score chart pattern in section 1.4.

### Extension ideas

- Add one KPI from your own dashboard brainstorm
- Compare filtered vs unfiltered row counts in the sidebar
- Export a chart spec and note what a careless reader might misread

## Optional tracks

- **Tableau Public**: [`tableau.md`](tableau.md): `export_tableau_csv.py` → upload CSV → drag-and-drop dashboard
- **Nao (agentic BI)**: [`nao.md`](nao.md): `build_off_db.py` → `nao sync` → `nao chat`. Check the generated SQL.

