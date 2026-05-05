# AGENTS.md — dataviz-course

Guidance for AI agents working in this repository.

---

## What this repo is

A public teaching repository for a data visualization course (PSL Master IASD, 2026).
Students clone it to follow along with the slides and run the workshop notebooks.

**Not in this repo** (kept private in the amai-lab monorepo):
- `TEACHER_NOTES.md` — design rationale
- `course_plan.md` — full session plan with private notes

---

## Structure

```
slides/           Slidev presentation (slides.md + seriph theme)
  public/images/  Slide images — committed directly, see below
notebooks/        Marimo workshop notebooks
  01_matplotlib_seaborn.py
  02_gog_altair.py
pyproject.toml    Python deps (uv)
uv.lock
```

---

## Running things

**Slides** — must run from `slides/`, not the repo root:
```bash
cd slides
npm install
npm run dev      # localhost:3030
```

**Notebooks** — run from the repo root:
```bash
uv sync --no-install-project
uv run marimo edit notebooks/01_matplotlib_seaborn.py
uv run marimo edit notebooks/02_gog_altair.py
```

To skip `uv run` each time, activate the venv first:
```bash
source .venv/bin/activate
marimo edit notebooks/01_matplotlib_seaborn.py
```

---

## Images

Images are committed directly to `slides/public/images/` — **do not use symlinks**.

This repo originated from a monorepo where images were a vault symlink. That approach
doesn't work for students cloning the repo, so images are now real committed files.

**To add a new image:**
1. Drop it into `slides/public/images/`
2. Reference it in slides.md as `<img src="/images/filename.ext" />`
3. Commit it

**Pitfall:** `slides/.gitignore` used to have a blanket `public/` rule (Slidev default).
It was replaced with specific entries (`public/fonts/`, `public/icons/`) so that
`slides/public/images/` is tracked. Don't re-add `public/` there.

---

## Slides — key patterns

The deck uses **Slidev** with the `seriph` theme and `mdc: true`.

**Vertical centering** — to center body content below a title, wrap it in:
```html
<div class="flex flex-col justify-center h-full">

markdown content here...

</div>
```
For `two-cols-header` layout, apply the wrapper inside each `::left::` / `::right::` slot.

**Images in slides:**
```html
<img src="/images/filename.png" class="w-full" style="max-height:350px; object-fit:contain" />
```
Use `object-fit:cover` for photos, `object-fit:contain` for diagrams/charts.

**Grid layout for 4 images:**
```html
<div class="grid grid-cols-4 gap-3 items-end">
  <div class="text-center">
    <img ... />
    <p class="text-xs text-gray-400 mt-1">Caption</p>
  </div>
  ...
</div>
```

---

## Notebooks — key patterns

- **Session 1** (`01_matplotlib_seaborn.py`): Matplotlib + Seaborn, Gapminder + Palmer Penguins datasets
- **Session 2** (`02_gog_altair.py`): Grammar of Graphics + Altair, Gapminder + INSEE prénoms

Both use **pandas** (not polars) — Seaborn's classic API requires it.

The prénoms dataset (~300k rows) exceeds Altair's 5000-row default limit.
VegaFusion is enabled at the top of `02_gog_altair.py` to lift that limit:
```python
alt.data_transformers.enable("vegafusion")
```

Data is downloaded on first run and cached to `data/prenoms.parquet` (gitignored).
The notebook has a fallback sample if the INSEE URL is unreachable.

---

## Course content overview

7 sessions across May–June 2026:

| # | Date | Topic |
|---|------|-------|
| 1 | 07/05 | Principles + Matplotlib/Seaborn |
| 2 | 27/05 | Grammar of Graphics + Altair |
| 3 | 28/05 | Communication & Storytelling |
| 4 | 03/06 | Visualization × ML |
| 5 | 04/06 | Big Data Scale |
| 6 | 08/06 | AI-Assisted Viz + Ethics |
| 7+8 | 11/06 | Mini-project hackathon |

Key theoretical framework: Munzner's marks/channels vocabulary → Grammar of Graphics (Wilkinson/Wickham) → Altair implementation. Cleveland & McGill accuracy ranking underpins channel choice guidance.

---

## What not to do

- Don't run `npm install` from the repo root — `package.json` is in `slides/`
- Don't add `public/` back to `slides/.gitignore`
- Don't commit `data/`, `.venv/`, or `slides/node_modules/` (all gitignored)
- Don't add a vault symlink at `slides/public/images` — commit images directly
