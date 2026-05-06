# Review: workshop 01 - Matplotlib and Seaborn

Scope: `notebooks/01_matplotlib_seaborn.py`, checked against `slides/slides.md`
and the Python visualization libraries used in `pyproject.toml`.

Note: the shared knowledge-vault URL was not reachable from this environment
(GitHub returned 404 / repository not found). This review is therefore grounded
in the repository material plus the cited research and library documentation.

## Overall assessment

The workshop has a strong foundation:

- It starts with a real motivation for visualization before modeling.
- It uses stable teaching datasets and keeps the code runnable.
- It introduces Matplotlib's explicit `Figure` / `Axes` API early.
- It links practice to perception research: Anscombe, Cleveland and McGill,
  Mackinlay, Munzner, Tufte, and Wickham.

The main risk is overload. The notebook currently tries to teach data
reshaping, Matplotlib APIs, visual encoding, annotation, small multiples,
export, Seaborn distributions, regression, faceting, pair plots, heatmaps,
uncertainty, and accessibility in one 3-hour first workshop. For Master IASD
students, especially in a work-study program, the session would be stronger if
it emphasized fewer concepts, more critique, and more ML-oriented decision
points.

## Proposed organization

Recommended flow:

| Block | Content | Teaching goal |
| --- | --- | --- |
| 1. Why plot before modeling | Anscombe / Datasaurus, data types, tidy data | Connect visualization to EDA and ML failure modes |
| 2. Matplotlib essentials | Figure / Axes / Artists, scatter, line, annotation, export | Give students a reusable mental model |
| 3. Encoding and design critique | Position, color, size, labels, small multiples, accessibility | Make design choices explicit |
| 4. Seaborn statistical views | Distributions, relationships, faceting, error bars | Teach what Seaborn computes automatically |
| 5. Practice | Two scaffolded exercises plus one optional ML checkpoint | Consolidate, do not just read examples |

Suggested cuts or moves:

- Merge "Grid Plots" with "Small Multiples". `FacetGrid` is the Seaborn version
  of the same design idea.
- Move color accessibility before the first multi-color examples, or explicitly
  say that early palettes are temporary teaching examples.
- Keep `pairplot` and `heatmap` as optional "if time" material. They are useful,
  but less central than distribution plots and error bars.
- Add empty student workspace cells after each exercise. Accordions with hints
  are useful, but the active work should be visible in the notebook.
- Add a short "ML practitioner checkpoint": e.g. plot class imbalance,
  residuals, calibration error, or feature distributions by target. This aligns
  the first session with the Master AI / ML / Big Data audience without waiting
  for session 4.

## Specific changes requested

### 1. Fix the Gapminder description

`notebooks/01_matplotlib_seaborn.py` describes Gapminder as "~140 countries"
in section 3. The slides describe the actual Vega dataset as "63 countries x
11 time points (1955-2005)".

Change the notebook text to:

> The Vega Gapminder subset contains 63 countries observed every five years
> from 1955 to 2005, for 693 country-year rows.

Reason: students will notice row counts in the notebook. Consistency matters in
teaching data literacy.

### 2. Correct the Seaborn confidence-interval explanation

The notebook says:

> Here it reflects spread across countries within a region, not model uncertainty.

This is not precise. In Seaborn 0.13, `lineplot` defaults to
`estimator="mean"` and `errorbar=("ci", 95)`. The band is a bootstrap
confidence interval for the estimated mean at each x value, not a direct display
of within-region spread. Seaborn's own error-bar tutorial distinguishes
uncertainty of an estimate (`ci`, `se`) from spread of the underlying data
(`sd`, `pi`).

Recommended replacement:

> By default, `sns.lineplot` aggregates repeated x values with the mean and
> shows a 95% bootstrap CI for that mean. This is uncertainty about the
> estimated regional mean, not the full spread of country trajectories.
> To show spread, use `errorbar="sd"` or `errorbar=("pi", 95)`, or plot
> individual countries with `units="country", estimator=None`.

Reason: this is the most important accuracy issue in the notebook. It also
teaches a core statistical graphics distinction that ML students need.

### 3. Align color-channel wording with the slides

The notebook's channel table says color is "High" accuracy and is good for
"Categories (<= 8) or a quantitative gradient". The slides correctly warn that
color hue should not be used for quantities.

Recommended wording:

| Channel | Best use | Caution |
| --- | --- | --- |
| Position | Primary quantitative comparisons | Most accurate |
| Length | Bars and intervals | Common baseline helps |
| Color hue | Nominal categories | Limit to about 6-8 hues |
| Luminance / saturation | Ordered or continuous values | Lower precision than position |
| Area / size | Rough magnitude, emphasis | Hard to compare precisely |
| Shape | Nominal categories | Low capacity |
| Transparency | Overplotting / density | Not a category channel |

Reason: this matches Cleveland and McGill's perceptual ranking, Mackinlay's
effectiveness principle, Munzner's channel vocabulary, and Matplotlib's colormap
guidance on sequential, diverging, cyclic, and qualitative maps.

### 4. Clarify Matplotlib marker size

In Matplotlib, `Axes.scatter(..., s=...)` expects marker area in points squared,
not radius or diameter.

Add a note near the bubble chart:

> In Matplotlib, `s` controls marker area (`points**2`). Because people compare
> areas poorly, use bubble size only for approximate magnitude and add labels or
> legends when exact values matter.

Reason: the slide deck already warns that size is perceptually weak. The code
should make the library behavior explicit.

### 5. Reframe "tidy data" as a default, not a universal requirement

The notebook says tidy data is "the prerequisite for almost every plotting
library". This is directionally useful, but too broad.

Recommended wording:

> Tidy / long-form data is the most reusable format for Seaborn, Altair, and
> data-analysis pipelines. Matplotlib can plot arrays directly, and Seaborn can
> handle some wide-form inputs, but tidy data keeps mappings explicit.

Reason: this keeps Wickham's tidy-data principle while staying accurate about
Matplotlib and Seaborn APIs.

### 6. Add warnings around KDE, regression, and correlation

Add short notes where these appear:

- KDE: bandwidth is a modeling choice; it can oversmooth, undersmooth, or imply
  impossible values outside natural bounds.
- `regplot`: the line is descriptive unless the modeling assumptions and causal
  story are justified. Across countries, it is an ecological association.
- Heatmap: correlation is pairwise and linear; it can hide nonlinear
  relationships and subgroup effects.

Reason: Master ML students should learn to ask what a statistical graphic has
computed, not just how to call the function.

### 7. Make the exercises more progressive

Current exercises are good, but they come after many examples and are not fully
scaffolded.

Suggested exercise sequence:

1. Recreate a chart from scratch using the explicit Matplotlib API.
2. Improve it using one design principle: direct labels, sorted categories,
   reduced clutter, or accessible color.
3. Use Seaborn to compare a distribution across groups.
4. Explain what the plot computes: raw observations, aggregate, CI, SD, PI, or
   model fit.

Reason: this progression moves from syntax to design judgement to statistical
interpretation.

### 8. Fix export path robustness

Exercise 1 asks students to save to `../figures/exercise_1.pdf`. When the
notebook is launched from the repository root, this path points outside the
repository.

Recommended code:

```python
from pathlib import Path

Path("figures").mkdir(exist_ok=True)
fig.savefig("figures/exercise_1.pdf", bbox_inches="tight")
```

Also consider adding `figures/` to `.gitignore` if outputs should not be
committed.

Reason: the repo instructions launch Marimo from the repository root.

### 9. Align slides and notebook dataset story

The slides introduce session 1 as using Gapminder only. The notebook uses both
Gapminder and Palmer Penguins.

Either:

- update the slides to mention Palmer Penguins as the Seaborn/statistical
  graphics dataset, or
- postpone Penguins until the first Seaborn section.

Reason: a stable dataset story reduces cognitive load.

## General notes for the author

- The first workshop should not try to be a complete tour of Matplotlib and
  Seaborn. It should teach a decision process: what am I comparing, what data
  type is it, which channel is effective, and what statistic is being shown?
- Use the slides for principles and the notebook for applying those principles.
  Avoid repeating the full theory twice.
- For work-study students, every major chart should answer a workplace question:
  "Would this help me debug a dataset, a model, or a stakeholder decision?"
- Prefer fewer, deeper examples over many chart types. Students remember a
  workflow better than a gallery.
- Keep the statistical semantics visible. A Seaborn one-liner is only safe if
  students know whether it drew raw data, an aggregate, an uncertainty interval,
  or a model.

## Source grounding

Research and textbooks:

- Anscombe, F. J. (1973). Graphs in statistical analysis. *The American
  Statistician*, 27(1), 17-21.
- Cleveland, W. S., and McGill, R. (1984). Graphical perception: Theory,
  experimentation, and application to the development of graphical methods.
  *Journal of the American Statistical Association*, 79(387), 531-554.
- Mackinlay, J. (1986). Automating the design of graphical presentations of
  relational information. *ACM Transactions on Graphics*, 5(2), 110-141.
- Tufte, E. R. (2001). *The Visual Display of Quantitative Information*.
  Graphics Press.
- Munzner, T. (2014). *Visualization Analysis and Design*. CRC Press.
- Wickham, H. (2014). Tidy data. *Journal of Statistical Software*, 59(10).
  <https://doi.org/10.18637/jss.v059.i10>
- Matejka, J., and Fitzmaurice, G. (2017). Same stats, different graphs:
  Generating datasets with varied appearance and identical statistics through
  simulated annealing. *CHI 2017*. <https://doi.org/10.1145/3025453.3025912>
- Gelman, A., and Unwin, A. (2013). Infovis and statistical graphics: Different
  goals, different looks. *Journal of Computational and Graphical Statistics*,
  22(1), 2-28.
- Horst, A. M., Hill, A. P., and Gorman, K. B. (2020). *palmerpenguins*.
  <https://doi.org/10.5281/zenodo.3960218>

Library documentation checked:

- Matplotlib documentation, "Matplotlib Application Interfaces (APIs)": explicit
  Axes interface vs implicit pyplot interface.
  <https://matplotlib.org/stable/users/explain/figure/api_interfaces.html>
- Matplotlib documentation, `Axes.scatter`: marker size `s` is in `points**2`.
  <https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.scatter.html>
- Matplotlib documentation, "Choosing Colormaps in Matplotlib": sequential,
  diverging, cyclic, and qualitative colormap classes; perceptual uniformity.
  <https://matplotlib.org/stable/users/explain/colors/colormaps.html>
- Seaborn 0.13.2 documentation, `seaborn.lineplot`: default estimator and
  error-bar behavior. <https://seaborn.pydata.org/generated/seaborn.lineplot.html>
- Seaborn 0.13.2 tutorial, "Statistical estimation and error bars": distinction
  between uncertainty intervals and spread intervals.
  <https://seaborn.pydata.org/tutorial/error_bars.html>
- pandas documentation, `DataFrame.melt`: unpivoting wide data to long form.
  <https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.melt.html>
