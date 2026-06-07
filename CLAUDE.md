# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

A public teaching repository for a data visualization course (PSL Master IASD, 2026). Students clone it to run slides and workshop notebooks. Private files (`TEACHER_NOTES.md`, `course_plan.md`) live in the amai-lab monorepo and are not here.

## Commands

**Slides** — must run from `slides/`, not the repo root:
```bash
cd slides && npm install
npm run dev        # session 1 (session1_principles.md)
npm run build      # or build:s1
npm run dev:s6     # session 6 (session6_dashboarding.md)
npm run build:s6
```

**Notebooks** — run from repo root:
```bash
uv sync --no-install-project
uv run marimo edit notebooks/01_matplotlib_seaborn.py
uv run marimo edit notebooks/02_gog_altair.py
```

Or activate the venv once to skip `uv run`:
```bash
source .venv/bin/activate
marimo edit notebooks/01_matplotlib_seaborn.py
```

## Architecture

Two independent sub-projects with no shared build system:

- **`slides/`** — Slidev decks (`session1_principles.md`, `session6_dashboarding.md`, …) with the `seriph` theme, `mdc: true`. Custom layouts in `slides/layouts/`. Images committed to `slides/public/images/` and referenced as `/images/filename.ext`. The `slides/.gitignore` excludes `public/fonts/` and `public/icons/` but intentionally does NOT exclude `public/` — don't add that rule back.

- **`notebooks/`** — Two Marimo notebooks (`.py` format). Session 1: matplotlib + seaborn on Gapminder / Palmer Penguins. Session 2: Grammar of Graphics + Altair on Gapminder / INSEE prénoms (~300k rows).

## Key patterns

**Slides — vertical centering below a title:**
```html
<div class="flex flex-col justify-center h-full">

markdown content here...

</div>
```
Apply inside `::left::` / `::right::` slots for `two-cols-header` layout.

**Slides — images:**
```html
<img src="/images/filename.png" class="w-full" style="max-height:350px; object-fit:contain" />
```
Use `object-fit:cover` for photos, `object-fit:contain` for diagrams/charts.

**Notebooks — large datasets:** The prénoms dataset exceeds Altair's 5000-row default. VegaFusion is enabled at the top of `02_gog_altair.py` to lift that limit:
```python
alt.data_transformers.enable("vegafusion")
```

**Notebooks — use pandas, not polars.** Seaborn's classic API requires pandas DataFrames.

**Notebooks — prénoms data** is downloaded on first run and cached to `data/prenoms.parquet` (gitignored). The notebook has a fallback sample if the INSEE URL is unreachable.

## Dependency versioning

**Python** (`pyproject.toml`): pin exact versions (`==x.y.z`), never `>=` or `~=`. Never pin a PyPI release from the last 7 days. After edits, run `uv sync` and commit `uv.lock`.

**npm / Node** (`slides/package.json`): pin exact versions in `dependencies` / `devDependencies` (no `^`, `~`, `*`, or ranges). Check release date with `npm view <package>@<version> time --json`; if the latest stable is <7 days old, pin the previous stable. After edits, run `npm install` in `slides/` and commit `package-lock.json`.

## What not to do

- Don't run `npm install` from the repo root — `package.json` is in `slides/`
- Don't add `public/` to `slides/.gitignore` (images must be tracked)
- Don't commit `data/`, `.venv/`, or `slides/node_modules/` (all gitignored)
