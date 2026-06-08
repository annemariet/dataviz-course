"""Build a DuckDB file over Open Food Facts for the optional Nao track.

Run from the repository root:

    uv run python session6/build_off_db.py

Writes ``session6/data/off.duckdb`` — one ``products`` table with ~15
demo-relevant columns over the full ~3M-row Parquet.

Quick smoke test (smaller row count):

    uv run python session6/build_off_db.py --sample 50000

See ``nao.md`` for setup and prompts.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import duckdb

from course_data import (
    PARQUET_PATH,
    ensure_openfoodfacts_parquet,
    parquet_bind_path,
)

DEMO_COLUMNS_SQL = """
SELECT product_name, brands, countries_tags AS countries_en,
       pnns_groups_1, pnns_groups_2,
       nutriscore_grade, nova_group,
       "energy-kcal_100g" AS energy_kcal_100g,
       fat_100g, sugars_100g, salt_100g, proteins_100g, fiber_100g,
       created_t, last_modified_t
FROM read_parquet('{parquet}')
"""


def build(sample: int | None) -> Path:
    parquet = parquet_bind_path(ensure_openfoodfacts_parquet(PARQUET_PATH))
    out = Path("session6/data/off.duckdb")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.unlink(missing_ok=True)

    select = DEMO_COLUMNS_SQL.format(parquet=parquet)
    if sample:
        select += f"\nUSING SAMPLE {int(sample)} ROWS (RESERVOIR, 42)"

    con = duckdb.connect(out)
    con.sql(f"CREATE TABLE products AS {select}")
    n = con.sql("SELECT COUNT(*) FROM products").fetchone()[0]
    con.close()
    print(f"wrote {out} ({n:,} rows, {out.stat().st_size:,} bytes)")
    return out


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument(
        "--sample",
        type=int,
        default=None,
        help="Optional reservoir sample size; default loads the full dataset.",
    )
    build(ap.parse_args().sample)


if __name__ == "__main__":
    main()
