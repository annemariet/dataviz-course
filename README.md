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
