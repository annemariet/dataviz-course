"""Aggregate the OFF Parquet into a small CSV for the Tableau Public track.

Run from the repository root:

    uv run python session6/export_tableau_csv.py

Writes ``data/off_grade_by_category.csv`` — a few hundred rows of
(category, grade, country, n). See ``tableau.md`` for next steps.
"""

from __future__ import annotations

from pathlib import Path

import duckdb

from course_data import (
    PARQUET_PATH,
    ensure_openfoodfacts_parquet,
    parquet_bind_path,
)


def main() -> None:
    parquet = parquet_bind_path(ensure_openfoodfacts_parquet(PARQUET_PATH))
    out = Path("data/off_grade_by_category.csv")
    out.parent.mkdir(parents=True, exist_ok=True)

    duckdb.sql(
        """
        SELECT pnns_groups_1                AS category,
               UPPER(nutriscore_grade)      AS grade,
               countries_tags               AS country,
               COUNT(*)                     AS n
        FROM read_parquet(?)
        WHERE pnns_groups_1 IS NOT NULL
          AND pnns_groups_1 <> 'unknown'
          AND nutriscore_grade IS NOT NULL
          AND countries_tags IS NOT NULL
          AND countries_tags NOT LIKE '%,%'
        GROUP BY 1, 2, 3
        """,
        params=[parquet],
    ).df().to_csv(out, index=False)
    print(f"wrote {out} ({out.stat().st_size:,} bytes)")


if __name__ == "__main__":
    main()
