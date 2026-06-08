# Dataviz Workshop

PSL Master IASD · 2026 · Anne-Marie Tousch

## Structure

```
slides/      Slidev decks (session1_principles.md, session6_dashboarding.md, ...)
notebooks/   Marimo workshop notebooks
```

## Running the slides

Run all commands from `slides/` (not the repo root):

```bash
cd slides
npm install
```

**Session 1** (`session1_principles.md`):

```bash
npm run dev        # or npm run dev:s1 — live preview at localhost:3030
npm run build      # or npm run build:s1 — export to dist/
```

**Session 6** (`session6_dashboarding.md`):

```bash
npm run dev:s6
npm run build:s6
```

### Slide images

Deck markdown references images as `/images/filename.ext`. Slidev resolves these from `slides/public/images/` — files are committed directly (not symlinked). Session 6 adds ~30 assets on top of the Session 1 set; if a build fails with missing `/images/...` imports, check that the file exists under `slides/public/images/` before running `npm run build:s6`.

## Running the notebooks

Run all commands from the **repository root** (the folder that contains `notebooks/` and `course_data.py`):

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

From the repository root:

```bash
uv sync
uv run marimo edit notebooks/03_eda_open_food_facts.py
```

`course_data.py` at the repository root supplies the Parquet path and download helper. Paths such as `data/openfoodfacts.parquet` and `mlruns.db` are relative to this directory. Marimo adds the repository root to `PYTHONPATH` via `.marimo.toml`.

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

### Session 4 — ML visualization (Open Food Facts)

From the repository root (same Parquet as Session 3):

```bash
uv sync --no-install-project
uv run marimo edit notebooks/04_ml_viz_open_food_facts.py
```

MLflow logs to `mlruns.db` (SQLite) at the repo root by default in this notebook. Optional UI:

```bash
uv run mlflow ui --backend-store-uri sqlite:///mlruns.db --host 127.0.0.1 --port 5000
```

### Session 5 — Embeddings (OFF nutrients + optional Wikipedia embeddings)

```bash
uv sync --no-install-project
uv run marimo edit notebooks/05_embeddings.py
```

Optional real text embeddings (large download):

```bash
uv run marimo edit notebooks/05_embeddings.py -- --real-embeddings
```

