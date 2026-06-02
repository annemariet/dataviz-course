# Dataviz Workshop

PSL Master IASD · 2026 · Anne-Marie Tousch

## Structure

```
slides/      Slidev presentation (slides.md)
notebooks/   Marimo workshop notebooks
```

## Running the slides

```bash
cd slides
npm install
npm run dev      # live preview at localhost:3030
npm run build    # export to dist/
```

## Running the notebooks

```bash
uv sync --no-install-project
uv run marimo edit notebooks/01_matplotlib_seaborn.py
uv run marimo edit notebooks/02_gog_altair.py
```

If you haven't used Marimo before, run the built-in intro tutorial first:

```bash
uv run marimo tutorial intro
```

### Session 3 — EDA (Open Food Facts)

```bash
uv sync
uv run marimo edit notebooks/03_eda_open_food_facts.py
```

`course_data.py` at the repo root supplies the Parquet path and download helper. Marimo adds the project root to `PYTHONPATH` via `.marimo.toml`.

#### Open Food Facts Parquet (~1 GB)

**Course file (SharePoint, Dauphine login):**

https://universitedauphine.sharepoint.com/:u:/r/sites/upd_25_a5aias150_espacepromo/Documents%20partages/Visualisation%20de%20donn%C3%A9es/data/openfoodfacts.parquet?csf=1&web=1&e=XeGvP6

1. Open the link in a browser and sign in with your university account.
2. Download `openfoodfacts.parquet`.
3. Save it as `data/openfoodfacts.parquet` in this repository (create `data/` if needed).

Notebooks call `course_data.ensure_openfoodfacts_parquet()` on first run. If the file is missing, you may see an error pointing to these manual steps.

Optional mirror:

```bash
export PARQUET_URL="https://example.com/openfoodfacts.parquet"
```
