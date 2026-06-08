"""Session 6: Open Food Facts dashboard starter (Streamlit).

Run from the repository root after ``uv sync --extra s6``:

    uv run streamlit run session6/streamlit_app.py

**Two files:** ``off_dashboard_queries.py`` = DuckDB + caching;
``streamlit_app.py`` = layout + charts (this file).

Build order:
  1.1–1.4  KPI query, KPI tiles, Nutri-Score query, one bar chart (live)
  2.1–2.3  ``@st.cache_data`` on 1.1 / 1.3; optional sidebar timing
  3+       New queries in ``off_dashboard_queries.py``, charts here (copy 1.4 pattern)
"""

from __future__ import annotations

import altair as alt
import streamlit as st

from off_dashboard_queries import (
    NUTRI_SCORES,
    NUTRI_SCORE_COLORS,
    compute_kpis,
    list_countries,
    query_nutri_score_distribution,
    resolve_parquet,
)

st.set_page_config(
    page_title="Open Food Facts: analytical dashboard",
    page_icon="🥫",
    layout="wide",
)


# --- Sidebar ------------------------------------------------------------------

parquet = resolve_parquet()

st.sidebar.title("Filters")
country_options = ["(all)"] + list_countries(parquet)
country_choice = st.sidebar.selectbox("Country", country_options, index=0)
country = None if country_choice == "(all)" else country_choice

st.sidebar.caption("Pass ``country`` into every query in ``off_dashboard_queries.py``.")

# 2.3 — optional: time ``compute_kpis`` before/after 2.1 to show cache hits


# --- 1.2 — KPI tiles ----------------------------------------------------------

st.title("Open Food Facts: analytical dashboard")
st.caption("Type: **analytical**. Queries in ``off_dashboard_queries.py``; charts below.")

kpis = compute_kpis(parquet, country)
col_a, col_b = st.columns(2)
col_a.metric("Products", f"{kpis['n_products']:,}")
col_b.metric("Nutri-Score A–E", f"{kpis['pct_with_nutri_score']:.0%}")

# 3.2 — add metrics after 3.1 (``unknown``, ``not-applicable``, NOVA-4 %)


# --- 1.4 — Nutri-Score chart (template for 4.2 / 5.2 / 6.2) -----------------

chart_left, chart_right = st.columns(2)

with chart_left:
    st.subheader("Nutri-Score distribution")
    nutri_score_df = query_nutri_score_distribution(parquet, country)
    nutri_score_color = alt.Scale(
        domain=NUTRI_SCORES,
        range=[NUTRI_SCORE_COLORS[s] for s in NUTRI_SCORES],
    )
    nutri_score_chart = (
        alt.Chart(nutri_score_df)
        .mark_bar()
        .encode(
            x=alt.X(
                "nutri_score:N",
                title="Nutri-Score",
                scale=alt.Scale(domain=NUTRI_SCORES),
            ),
            y=alt.Y("n:Q", title="Products", scale=alt.Scale(zero=True)),
            color=alt.Color("nutri_score:N", scale=nutri_score_color, legend=None),
            tooltip=["nutri_score", alt.Tooltip("n:Q", format=",")],
        )
        .properties(width="container", height=280)
    )
    st.altair_chart(nutri_score_chart, width="stretch")

with chart_right:
    st.subheader("NOVA processing groups")
    # 4.2 — horizontal bar: x = n, y = nova label; see 4.1 in queries file
    st.info("**4.1** query → **4.2** chart (copy the Nutri-Score panel).")

st.divider()

row2_left, row2_right = st.columns([1, 2])

with row2_left:
    st.subheader("Top food categories")
    # 5.2 — horizontal bar on pnns_groups_1; top 10
    st.info("**5.1** query → **5.2** chart.")

with row2_right:
    st.subheader("Nutri-Score mix by category")
    # 6.2 — mark_rect; color = share within category (not raw n)
    st.info("**6.1** query + ``share`` column → **6.2** heatmap.")

st.divider()
with st.expander("Ethics check", expanded=False):
    st.markdown(
        """
        For each chart on this dashboard, write:

        > *A careless reader of this chart would conclude __, but the data actually says __.*
        """
    )
