"""DuckDB helpers for the Session 6 dashboard.

**Layout convention:** analytics live here; ``streamlit_app.py`` is UI only.
Add numbered query functions below as the workshop progresses (3.1, 4.1, …).

Workshop checklist (implement here, call from the app):
  1.1 ``compute_kpis`` — live
  1.3 ``query_nutri_score_distribution`` — live
  2.1–2.2 ``@st.cache_data`` on 1.1 / 1.3 (enabled below; comment out to demo spinners)
  3.1 extra coverage metrics (``unknown``, ``not-applicable``, NOVA-4 %)
  4.1 ``query_nova_distribution``; map labels with ``NOVA_LABELS``
  5.1 ``query_top_categories`` on ``pnns_groups_1``; exclude ``unknown``
  6.1 ``query_category_nutri_score``; ``share`` within category in pandas
"""

from __future__ import annotations

from pathlib import Path

import duckdb
import pandas as pd
import streamlit as st

from course_data import (
    PARQUET_PATH,
    ensure_openfoodfacts_parquet,
    parquet_bind_path,
)

NUTRI_SCORES = ["A", "B", "C", "D", "E"]
NUTRI_SCORES_SQL = ", ".join(f"'{s.lower()}'" for s in NUTRI_SCORES)
NUTRI_SCORE_COLORS = {
    "A": "#1a9641",
    "B": "#a6d96a",
    "C": "#d4c000",
    "D": "#fdae61",
    "E": "#d7191c",
}
NOVA_LABELS = {
    1: "1: unprocessed",
    2: "2: culinary",
    3: "3: processed",
    4: "4: ultra-processed",
}


def country_clause(country: str | None) -> tuple[str, list]:
    """SQL fragment + params for the sidebar country filter."""
    if country:
        return " AND countries_tags = ?", [country]
    return "", []


@st.cache_data(show_spinner="Locating Open Food Facts Parquet…")
def resolve_parquet() -> str:
    path: Path = ensure_openfoodfacts_parquet(PARQUET_PATH)
    return parquet_bind_path(path)


@st.cache_data(show_spinner="Loading country list…")
def list_countries(parquet: str, top_n: int = 30) -> list[str]:
    df = duckdb.sql(
        """
        SELECT countries_tags AS country, COUNT(*) AS n
        FROM read_parquet(?)
        WHERE countries_tags IS NOT NULL
          AND countries_tags NOT LIKE '%,%'
        GROUP BY 1
        ORDER BY n DESC
        LIMIT ?
        """,
        params=[parquet, top_n],
    ).df()
    return df["country"].tolist()


@st.cache_data(show_spinner="Computing KPIs…")
def compute_kpis(parquet: str, country: str | None) -> dict[str, float]:
    cc, cp = country_clause(country)
    row = duckdb.sql(
        f"""
        SELECT
            COUNT(*) AS n_products,
            COUNT_IF(LOWER(nutriscore_grade) IN ({NUTRI_SCORES_SQL}))
                * 1.0 / NULLIF(COUNT(*), 0) AS pct_with_nutri_score,
            COUNT_IF(LOWER(nutriscore_grade) = 'unknown')
                * 1.0 / NULLIF(COUNT(*), 0) AS pct_unknown,
            COUNT_IF(LOWER(nutriscore_grade) = 'not-applicable')
                * 1.0 / NULLIF(COUNT(*), 0) AS pct_not_applicable,
            COUNT_IF(nova_group = 4) * 1.0 / NULLIF(COUNT(nova_group), 0) AS pct_nova_4
        FROM read_parquet(?)
        WHERE TRUE{cc}
        """,
        params=[parquet, *cp],
    ).df().iloc[0]
    return {
        "n_products": int(row["n_products"]),
        "pct_with_nutri_score": float(row["pct_with_nutri_score"] or 0.0),
        "pct_unknown": float(row["pct_unknown"] or 0.0),
        "pct_not_applicable": float(row["pct_not_applicable"] or 0.0),
        "pct_nova_4": float(row["pct_nova_4"] or 0.0),
    }


@st.cache_data(show_spinner="Querying Nutri-Score distribution…")
def query_nutri_score_distribution(parquet: str, country: str | None) -> pd.DataFrame:
    cc, cp = country_clause(country)
    return duckdb.sql(
        f"""
        SELECT UPPER(nutriscore_grade) AS nutri_score, COUNT(*) AS n
        FROM read_parquet(?)
        WHERE LOWER(nutriscore_grade) IN ({NUTRI_SCORES_SQL}){cc}
        GROUP BY 1
        ORDER BY 1
        """,
        params=[parquet, *cp],
    ).df()


@st.cache_data(show_spinner="Querying NOVA distribution…")
def query_nova_distribution(parquet: str, country: str | None) -> pd.DataFrame:
    cc, cp = country_clause(country)
    df = duckdb.sql(
        f"""
        SELECT nova_group, COUNT(*) AS n
        FROM read_parquet(?)
        WHERE nova_group IS NOT NULL{cc}
        GROUP BY 1
        ORDER BY 1
        """,
        params=[parquet, *cp],
    ).df()
    df["nova"] = df["nova_group"].map(NOVA_LABELS)
    return df


@st.cache_data(show_spinner="Querying top categories…")
def query_top_categories(parquet: str, country: str | None, top_n: int = 10) -> pd.DataFrame:
    cc, cp = country_clause(country)
    return duckdb.sql(
        f"""
        SELECT pnns_groups_1 AS category, COUNT(*) AS n
        FROM read_parquet(?)
        WHERE pnns_groups_1 IS NOT NULL
          AND pnns_groups_1 <> 'unknown'{cc}
        GROUP BY 1
        ORDER BY n DESC
        LIMIT ?
        """,
        params=[parquet, *cp, top_n],
    ).df()


@st.cache_data(show_spinner="Querying category × Nutri-Score…")
def query_category_nutri_score(parquet: str, country: str | None) -> pd.DataFrame:
    cc, cp = country_clause(country)
    df = duckdb.sql(
        f"""
        SELECT pnns_groups_1 AS category,
               UPPER(nutriscore_grade) AS nutri_score,
               COUNT(*) AS n
        FROM read_parquet(?)
        WHERE pnns_groups_1 IS NOT NULL
          AND pnns_groups_1 <> 'unknown'
          AND LOWER(nutriscore_grade) IN ({NUTRI_SCORES_SQL}){cc}
        GROUP BY 1, 2
        """,
        params=[parquet, *cp],
    ).df()
    df["share"] = df["n"] / df.groupby("category")["n"].transform("sum")
    return df
