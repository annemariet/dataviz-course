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

## Images

`slides/public/images` is a **symlink** into the local knowledge vault:

```
slides/public/images -> ~/MEGA/NotesApp/LucyKnowledgeBase/docs/library/raw/own/Teaching/Dataviz/old_materials/images/ppt/media
```

Images are **not tracked by git** — they live in the vault and are only available on the machine where the vault is synced. To add a new image, drop the file directly into that vault directory; it will be immediately available to the dev server via the symlink.

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
