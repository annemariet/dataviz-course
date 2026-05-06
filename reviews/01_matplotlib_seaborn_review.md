# Review: workshop 01 - Matplotlib and Seaborn

Scope: `notebooks/01_matplotlib_seaborn.py`, rebased and checked against the
updated `polish-course` version of `slides/slides.md`.

Note: the shared knowledge-vault URL was not reachable from this environment
(GitHub returned 404 / repository not found). This review is grounded in the
repository material plus the cited research and library documentation.

## Overall assessment

The workshop is now well aligned with the revised slides:

- The slides introduce explore vs explain, channel effectiveness, color,
  chartjunk, and Matplotlib/Seaborn defaults.
- The notebook applies those ideas with Gapminder and Palmer Penguins.
- The first hands-on session now has a clearer bridge to ML practice through EDA
  examples.

The main remaining risk is cognitive load. The notebook still covers many chart
families in one session. This is manageable if the instructor treats pair plots,
heatmaps, and the Datasaurus extension as optional material.

## Changes implemented in this PR

### Organization and progression

- Added prompted "Your turn" cells instead of empty workspaces.
- Added a Seaborn-based ML practitioner checkpoint after Seaborn is introduced.
- Marked pair plots and heatmaps as optional ML EDA toolbox material.
- Kept the main Grammar of Graphics theory light; session 2 remains the place
  for full grammar formalization.

### Accuracy and clarity fixes

- Fixed Gapminder metadata: the Vega subset is 63 countries x 11 years, not
  about 140 countries.
- Reframed tidy / long-form data as the default for reusable Seaborn, Altair,
  and analysis pipelines, not a universal Matplotlib requirement.
- Corrected Seaborn `lineplot` wording: the default band is a 95% bootstrap CI
  for the estimated mean, not direct country-level spread.
- Added cautions for KDE/violin plots, regression lines, and correlation
  heatmaps.
- Fixed exercise export paths to use `figures/`, and added `figures/` to
  `.gitignore`.

### Channels and palettes

- Replaced the single mixed channel ranking with two tables:
  - ordered attributes: quantitative, ordinal, temporal;
  - categorical attributes: nominal groups.
- This is closer to Munzner's separation of attribute types and avoids implying
  that categorical and quantitative channels share one universal ranking.
- Removed the hand-coded categorical palette in the first multi-color Matplotlib
  example. It now uses Matplotlib's active color cycle.
- The accessibility section now demonstrates palette choice through Seaborn's
  palette API (`tab10` vs `colorblind`).

### Anscombe / Datasaurus extension

- Added an optional Datasaurus Dozen stretch section after Anscombe.
- Students can inspect how datasets with similar summary statistics produce
  different shapes.
- The full Matejka and Fitzmaurice simulated annealing algorithm is better as a
  stretch lab, not core session-1 material. It is conceptually rich but adds
  optimization, target shapes, random perturbations, and runtime concerns.

## Remaining teaching suggestions

- If time is short, skip the optional Datasaurus, pairplot, and heatmap cells.
- During exercises, ask students to explain what the plot shows:
  raw data, aggregate, uncertainty interval, data spread, or fitted model.
- Use the same critique loop repeatedly:
  - What is the task?
  - What is the primary attribute?
  - Which channel carries it?
  - What did the chart aggregate or hide?
- If the Datasaurus extension becomes a larger activity, make it a separate
  notebook or later optional lab. The official page describes the algorithm and
  code, but the robust teaching version should include a bounded implementation,
  fixed random seed, small iteration count, and clear stopping criteria.

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

- Matplotlib documentation, "Matplotlib Application Interfaces (APIs)".
  <https://matplotlib.org/stable/users/explain/figure/api_interfaces.html>
- Matplotlib documentation, `Axes.scatter`.
  <https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.scatter.html>
- Matplotlib documentation, "Choosing Colormaps in Matplotlib".
  <https://matplotlib.org/stable/users/explain/colors/colormaps.html>
- Seaborn 0.13.2 documentation, `seaborn.lineplot`.
  <https://seaborn.pydata.org/generated/seaborn.lineplot.html>
- Seaborn 0.13.2 tutorial, "Statistical estimation and error bars".
  <https://seaborn.pydata.org/tutorial/error_bars.html>
- pandas documentation, `DataFrame.melt`.
  <https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.melt.html>
