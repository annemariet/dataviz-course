import marimo

__generated_with = "0.23.2"
app = marimo.App(
    width="medium",
    app_title="Data Visualization — Part 1: Matplotlib & Seaborn",
)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Datavis in practice, part 1 — the fundamentals: Matplotlib & Seaborn

    **Session duration**: ~2 hours &nbsp;|&nbsp; **Datasets**: Gapminder, Palmer Penguins

    ## What you'll be able to do after this session

    - Use tidy / long-form data as the default structure for reusable plots
    - Build charts with Matplotlib's **object-oriented API**
    - Encode ordered and categorical variables with appropriate visual channels
    - Annotate, polish, and export publication-quality figures
    - Use Seaborn to build statistical visualizations with less code
    - Show uncertainty and spread honestly with distributions and interval plots

    ---
    """)
    return


@app.cell
def _():
    from io import StringIO

    import marimo as mo
    import matplotlib.pyplot as plt
    import seaborn as sns
    import numpy as np
    import pandas as pd
    import requests
    from vega_datasets import data as vega_data

    plt.rcParams.update({
        "figure.dpi": 110,
        "font.family": "sans-serif",
        "axes.spines.top": False,
        "axes.spines.right": False,
    })
    sns.set_theme(style="ticks", palette="deep", font_scale=1.0)
    return mo, np, pd, plt, sns, vega_data


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 1 · Why Visualize? — Anscombe's Quartet

    You saw this in the intro slides. Run the cells below to have it at your fingertips —
    *running the code yourself* is different from seeing a static image.
    """)
    return


@app.cell
def _(pd):
    anscombe = pd.DataFrame({
        "dataset": ["I"]*11 + ["II"]*11 + ["III"]*11 + ["IV"]*11,
        "x": [10, 8, 13, 9, 11, 14, 6, 4, 12, 7, 5] * 3
             + [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 19],
        "y": [
            8.04, 6.95, 7.58, 8.81, 8.33, 9.96, 7.24, 4.26, 10.84, 4.82, 5.68,
            9.14, 8.14, 8.74, 8.77, 9.26, 8.10, 6.13, 3.10, 9.13, 7.26, 4.74,
            7.46, 6.77, 12.74, 7.11, 7.81, 8.84, 6.08, 5.39, 8.15, 6.42, 5.73,
            6.58, 5.76, 7.71, 8.84, 8.47, 7.04, 5.25, 5.56, 7.91, 6.89, 12.50,
        ],
    })
    return (anscombe,)


@app.cell
def _(anscombe):
    _summary = anscombe.groupby("dataset").agg(
        x_mean=("x", "mean"), x_std=("x", "std"),
        y_mean=("y", "mean"), y_std=("y", "std"),
    ).round(2)
    _corr = (
        anscombe.groupby("dataset")[["x", "y"]]
        .apply(lambda g: g["x"].corr(g["y"]).round(3))
        .rename("x–y corr")
    )
    _summary.join(_corr)
    return


@app.cell
def _(anscombe, np, plt):
    _colors = ["#4C72B0", "#DD8452", "#55A868", "#C44E52"]
    _fig, _axes = plt.subplots(2, 2, figsize=(9, 7), sharex=True, sharey=True)

    for _ax, (_name, _grp), _color in zip(_axes.flatten(), anscombe.groupby("dataset"), _colors):
        _ax.scatter(_grp["x"], _grp["y"], color=_color, s=55, alpha=0.85, zorder=2)
        _m, _b = np.polyfit(_grp["x"], _grp["y"], 1)
        _xs = np.linspace(3, 15, 100)
        _ax.plot(_xs, _m * _xs + _b, color="#888", lw=1.5, ls="--", zorder=1)
        _ax.set_title(f"Dataset {_name}", fontweight="bold")

    _fig.supxlabel("x", fontsize=11)
    _fig.supylabel("y", fontsize=11, x=0.01)
    _fig.suptitle("Same statistics — completely different structures",
                  fontsize=12, fontweight="bold")
    plt.tight_layout()
    _fig
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > **Core lesson**: Summary statistics hide patterns.
    > Always plot your data before drawing conclusions from numbers alone.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### If you're curious: the datasaurus dozen

    Matejka & Fitzmaurice (2017) showed how to generate many datasets with
    near-identical summary statistics but radically different shapes. Their
    method starts from an existing dataset, perturbs one point at a time, keeps
    summary statistics within tolerance, and uses simulated annealing to move
    toward a target shape.

    The full algorithm is a good advanced exercise, though beside the point of this course.
    What's interesting is the fact that they proved: **summary statistics hide fundamental patterns in your data**.

    You can download the **Datasaurus Dozen**: 12 fancy datasets with the same statistics at [https://www.openintro.org/data/csv/datasaurus.csv](https://www.openintro.org/data/csv/datasaurus.csv).

    Use the cells below to
    - update the file location and load the dataset
    - compare the summaries, then plot the data
    - [stretch] explore whether more robust statistics can help.
    """)
    return


@app.cell
def _(pd):
    from pathlib import Path
    datasaurus = pd.read_csv(Path.home()/"Downloads/datasaurus.csv")
    datasaurus.head()
    return (datasaurus,)


@app.cell
def _(datasaurus):
    _summary = datasaurus.groupby("dataset").agg(
        x_mean=("x", "mean"),
        x_std=("x", "std"),
        y_mean=("y", "mean"),
        y_std=("y", "std"),
        corr=("x", lambda s: s.corr(datasaurus.loc[s.index, "y"])),
    ).round(2)
    _summary
    return


@app.cell
def _(datasaurus, plt):
    _names = datasaurus["dataset"].unique()
    _fig, _axes = plt.subplots(4, 3, figsize=(10, 10), sharex=True, sharey=True)
    _color = plt.rcParams["axes.prop_cycle"].by_key()["color"][0]

    for _ax, _name in zip(_axes.flatten(), _names):
        _grp = datasaurus[datasaurus["dataset"] == _name]
        _ax.scatter(_grp["x"], _grp["y"], s=18, alpha=0.8, color=_color)
        _ax.set_title(_name, fontsize=9, fontweight="bold")

    _fig.suptitle("Same summary statistics, different visual structures", fontsize=12)
    plt.tight_layout()
    _fig
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 2 · Tidy Data

    Seaborn, Altair, ggplot2, and most reusable visualization pipelines work best
    with **tidy data**
    — a concept formalised by Hadley Wickham in his 2014 paper
    [*Tidy Data*, Journal of Statistical Software 59(10)](https://doi.org/10.18637/jss.v059.i10).

    | Rule | What it means |
    |------|--------------|
    | One row = one observation | No aggregation hidden in the structure |
    | One column = one variable | Column headers are variable names — values like `"France"`, `"Japan"` belong in a `country` column, not as headers |
    | One table = one observational unit | Don't mix granularities (e.g. per-country and per-continent) in the same table |

    **Why bother?** Wickham's key insight: *"tidy datasets are all alike, but every messy dataset is messy in its own way."*
    A tidy frame lets you:

    - **filter / group / aggregate** without reshaping first
    - **map columns directly to aesthetics** (`x=`, `y=`, `color=`, `size=`) — this is exactly what Seaborn and Altair expect
    - **reuse the same pipeline** across datasets with the same structure

    Matplotlib can plot arrays directly, and Seaborn accepts some wide-form inputs,
    but tidy data keeps mappings explicit. The most common transformation:
    `DataFrame.melt()` converts **wide → long (tidy)**.
    """)
    return


@app.cell
def _(pd):
    wide_df = pd.DataFrame({
        "year":   [1960, 1970, 1980, 1990, 2000],
        "France": [71.5, 72.4, 74.3, 77.0, 79.0],
        "Japan":  [67.8, 72.0, 76.1, 78.9, 81.5],
        "Brazil": [54.7, 59.5, 63.1, 66.5, 70.0],
    })
    return (wide_df,)


@app.cell
def _(wide_df):
    wide_df
    return


@app.cell
def _(wide_df):
    tidy_df = wide_df.melt(id_vars="year", var_name="country", value_name="life_expectancy")
    return (tidy_df,)


@app.cell
def _(tidy_df):
    tidy_df
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    With tidy data the mapping is direct:
    `x = year`, `y = life_expectancy`, `color = country` — no reshaping at plot time.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Question:** Is the datasaurus dataset tidy?
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ---
    ## 3 · Our Two Datasets

    We'll use the same two datasets in the next 2 sessions so you can focus on
    **the chart**, not on learning new data each time. Feel free to bring your own data later!

    ### Gapminder
    Originally compiled by Hans Rosling's Gapminder Foundation, this dataset tracks
    development indicators for 63 countries from 1955 to 2005 (5-year steps),
    for 693 country-year observations.

    | Column | Type | Description |
    |--------|------|-------------|
    | `country` | string | Country name |
    | `year` | int | 1955 – 2005, every 5 years |
    | `pop` | int | Population |
    | `life_expect` | float | Life expectancy at birth (years) |
    | `fertility` | float | Fertility rate (children per woman) |
    | `region` | string | World region (added below from `cluster` code) |

    It's a go-to teaching dataset because it has **continuous**, **categorical**, and
    **temporal** variables, a clear narrative arc (global health improving over time),
    and enough rows (693) to make patterns visible without overwhelming.

    ### Palmer Penguins
    Measurements of 333 penguins from three species in the Palmer Archipelago,
    Antarctica (Horst, Hill & Gorman 2020).

    | Column | Type | Description |
    |--------|------|-------------|
    | `species` | string | Adelie / Chinstrap / Gentoo |
    | `island` | string | Biscoe / Dream / Torgersen |
    | `bill_length_mm` | float | Bill length |
    | `bill_depth_mm` | float | Bill depth |
    | `flipper_length_mm` | float | Flipper length |
    | `body_mass_g` | float | Body mass |
    | `sex` | string | Male / Female |

    It's the modern replacement for the Iris dataset. It has a similar clean structure,
    three well-separated clusters, and several correlated continuous variables
    that reward visual exploration. We'll use it later in the Seaborn sections.
    """)
    return


@app.cell
def _(sns, vega_data):
    gapminder = vega_data.gapminder()
    _region_names = {
        0: "South Asia", 1: "Europe & Central Asia",
        2: "Sub-Saharan Africa", 3: "Americas",
        4: "East Asia & Pacific", 5: "Middle East & N. Africa",
    }
    gapminder["region"] = gapminder["cluster"].map(_region_names)
    penguins = sns.load_dataset("penguins").dropna()
    return gapminder, penguins


@app.cell
def _(gapminder):
    gm2000 = gapminder[gapminder["year"] == 2000]
    line_subset = (
        gapminder[gapminder["country"].isin(["France", "Japan", "India", "Nigeria", "Brazil"])]
        .sort_values("year")
    )
    return gm2000, line_subset


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Marimo automatically displays a rich view of the dataframe you want to see in a frame. Let's validate that the values look correct.
    """)
    return


@app.cell
def _(gapminder):
    gapminder.head()
    return


@app.cell
def _(penguins):
    penguins.head()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 4 · Matplotlib: two APIs

    Every Matplotlib chart is built from two objects:

    - **`Figure`** — the canvas. Holds one or many `Axes`.
    - **`Axes`** — a single plot: x/y axes, title, tick marks, artists.

    There are **two APIs**:

    | | `pyplot` (stateful) | Object-Oriented |
    |---|---|---|
    | Style | `plt.plot(...)` | `ax.plot(...)` |
    | Best for | Quick, one-off exploration | Reusable, composable code |
    | Subplots | Verbose | Natural |

    **Recommendation**: use `pyplot` to get something on screen fast,
    then switch to the object-oriented API as soon as you have more than one panel.

    **Tip**: type `help(plt.scatter)` or another function to display the corresponding doc.
    """)
    return


@app.cell
def _(gm2000, plt):
    _fig, (_ax_left, _ax_right) = plt.subplots(1, 2, figsize=(11, 4))

    plt.sca(_ax_left)
    plt.scatter(gm2000["fertility"], gm2000["life_expect"], alpha=0.5, s=35)
    plt.xlabel("Fertility")
    plt.ylabel("Life expectancy")
    plt.title("pyplot API  (plt.scatter, plt.xlabel…)")

    _ax_right.scatter(gm2000["fertility"], gm2000["life_expect"],
                      alpha=0.5, s=35, color="#DD8452")
    _ax_right.set_xlabel("Fertility")
    _ax_right.set_ylabel("Life expectancy")
    _ax_right.set_title("Object-oriented API  (ax.scatter, ax.set_xlabel…)")

    plt.tight_layout()
    _fig
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Try it! Make it break!**

    Mixing the 2 APIs is generally a bad idea, in particular because the pyplot API doesn't work intuitively with subplots.

    In the plot above, try using the pyplot API after the object-oriented one
    (e.g. add `plt.xlabel("new label")`). What happens?
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 5 · Encoding Variables as Visual Channels

    **Reminder:**

    Every variable you show must be mapped to a visual *channel* — a property of a mark
    that the eye can decode. Not all channels are equal.
    Cleveland & McGill (1984) established the empirical **accuracy ranking** through
    perception experiments. Mackinlay (1986) then formalised two design principles:

    - **Effectiveness**: use the most accurate channel for the most important variable.
    - **Expressiveness**: encode all the data — and only the data (no decoration that implies information you don't have).

    Munzner's *Visualization Analysis and Design* (2014) builds on their work in her formal textbook which strives to define the most useful data abstractions for datavis.

    <img src="public/expressiveness-types-and-effectiveness-ranks.png" width="700" />
    *(Figure 5.1 from Munzner)*

    Munzner separates channels by the kind of attribute you encode.
    A ranking for quantitative values is not the same as a ranking for categories.

    **Ordered attributes** — quantitative, temporal, ordinal:

    | Channel | Matplotlib | Use it for |
    |---------|-----------|------------|
    | Position on a common scale | `x=`, `y=` | Primary quantitative comparisons |
    | Length | bars, intervals | Magnitudes with a common baseline |
    | Area / size | `s=` | Rough magnitude, not precise ratios |
    | Luminance / saturation | sequential `cmap=` | Ordered values when position is already used |

    **Categorical attributes** — nominal groups:

    | Channel | Matplotlib | Use it for |
    |---------|-----------|------------|
    | Spatial grouping | ordering, offsets, enclosure, facets | Keep related items together; facets are one option |
    | Hue | `color=`, `c=` | A few categories, usually <= 6-8 |
    | Shape | `marker=` | A few categories, often redundant with hue |
    | Line style | `linestyle=` | Groups in line charts |
    | Transparency | `alpha=` | Overplotting or uncertainty, not nominal labels |

    **Rules of thumb**:
    - First identify the attribute type, then choose the channel.
    - Encode the most important ordered variable with position when possible.
    - Humans compare lengths better than areas; bubble size is approximate.
    - Redundant encoding (same variable → color *and* shape) can improve accessibility.
    - Avoid using hue for both categories and quantities in the same chart.

    Here, **spatial grouping** means using the plane to keep categories visually
    distinct: adjacent positions, separated bands, enclosed regions, or separate
    facets. Faceting is a strong case, but not the only one.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Let's say we want to explore how the fertility rate correlates with life expectancy, and see if there are regional patterns.

    - the most important variables are fertility and life expectancy, which we can encode with positions x and y.
    - to group regions together, we can do one plot per region. But it might be clearer to superimpose them, so the next choice is color
    - population size is interesting but not fundamental, we can encode it with a less efficient channel, circle area
    - we add transparency to avoid overlapping points to become invisible.
    """)
    return


@app.cell
def _(gm2000, plt):
    _regions = sorted(gm2000["region"].dropna().unique())
    _color_cycle = plt.rcParams["axes.prop_cycle"].by_key()["color"]
    _palette = dict(zip(_regions, _color_cycle))
    _marker_map = {"Sub-Saharan Africa": "^", "East Asia & Pacific": "s"}

    _fig, _ax = plt.subplots(figsize=(9, 6))
    for _region, _grp in gm2000.groupby("region"):
        _ax.scatter(
            _grp["fertility"], _grp["life_expect"],
            color=_palette[_region],
            marker=_marker_map.get(_region, "o"),
            s=_grp["pop"] / gm2000["pop"].max() * 700 + 15,
            alpha=0.72, edgecolors="white", linewidths=0.4,
            label=_region,
        )

    _ax.set_xlabel("Fertility rate (children per woman)", fontsize=11)
    _ax.set_ylabel("Life expectancy (years)", fontsize=11)
    _ax.set_title("Gapminder 2000 — four variables encoded in one chart",
                  fontsize=12, fontweight="bold")
    _ax.legend(fontsize=8, loc="lower left", framealpha=0.9, title="Region")
    _fig.tight_layout()
    _fig
    return


@app.cell(hide_code=True)
def _(mo):
    mo.vstack([
        mo.md(r"""
    **Try another encoding.**

    - Remove `s=...`: what becomes easier or harder to see?
    - Replace region color with a single neutral color: what story disappears?
    - Try `marker=` for two selected regions. When does shape help? When does it clutter?

    Note: in Matplotlib, `s` is marker **area** in points squared (`points**2`).
    Area is useful for rough magnitude, not for reading exact values.
    """),
        mo.accordion({
            "Hint — adding markers per group": mo.md(r"""
    Unlike `c=` and `s=`, `marker=` only accepts a **single value** per `scatter()` call — you cannot pass an array.
    Since the chart already loops over groups, assign one marker per group:

    ```python
    _marker_map = {"Sub-Saharan Africa": "^", "East Asia & Pacific": "s"}

    for _region, _grp in gm2000.groupby("region"):
        _ax.scatter(
            _grp["fertility"], _grp["life_expect"],
            color=_palette[_region],
            marker=_marker_map.get(_region, "o"),  # "o" for all other regions
        )
    ```

    Common marker strings: `"o"` circle · `"s"` square · `"^"` triangle · `"D"` diamond · `"P"` plus · `"X"` cross
    """)
        })
    ])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 6 · Annotations

    Good annotations draw attention to what matters most.
    Use them sparingly — one or two per chart is usually right.

    Key tools: `ax.annotate()`, `ax.text()`, `ax.axhline()`, `ax.axvspan()`.
    """)
    return


@app.cell
def _(gm2000, plt):
    _fig, _ax = plt.subplots(figsize=(9, 6))
    _ax.scatter(gm2000["fertility"], gm2000["life_expect"],
                alpha=0.45, s=40, color="#4C72B0", edgecolors="white", linewidths=0.3)

    _ax.axvspan(1.0, 2.3, ymin=0.68, alpha=0.06, color="#55A868")

    for _country in ["France", "China", "India"]:
        _row = gm2000[gm2000["country"] == _country]
        if _row.empty:
            continue
        _row = _row.iloc[0]
        _ox = 0.15 if _row["fertility"] < 5 else -0.15
        _ax.annotate(
            _country,
            xy=(_row["fertility"], _row["life_expect"]),
            xytext=(_row["fertility"] + _ox, _row["life_expect"] + 1.2),
            fontsize=8.5, color="#222",
            arrowprops=dict(arrowstyle="-", color="#999", lw=0.8),
        )

    _ax.axhline(70, color="#C44E52", lw=1.2, ls="--", alpha=0.6)
    _ax.text(7.3, 70.8, "70-year mark", color="#C44E52", fontsize=8.5)
    _ax.set_xlabel("Fertility rate", fontsize=11)
    _ax.set_ylabel("Life expectancy (years)", fontsize=11)
    _ax.set_title("Annotations guide the reader to what matters", fontsize=12)
    plt.tight_layout()
    _fig
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Exercise:**

    - Remove country labels. Add more. What is the effect?
    - Try a lower `alpha`: when does transparency reveal density, and when does it
      just make the chart harder to read?
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 7 · Time Series and Line Charts

    Line charts connect ordered observations — most commonly over time.
    """)
    return


@app.cell
def _(line_subset, plt):
    _fig, _ax = plt.subplots(figsize=(10, 5))
    for _country, _grp in line_subset.groupby("country"):
        _line, = _ax.plot(_grp["year"], _grp["life_expect"], lw=2.2, label=_country)
        _last = _grp.iloc[-1]

    _ax.set_xlim(right=2011)
    _ax.set_xlabel("Year", fontsize=11)
    _ax.set_ylabel("Life expectancy (years)", fontsize=11)
    _ax.set_title("Evolution of Life expectancy in 5 countries", fontsize=12)
    _ax.legend(bbox_to_anchor=(1.02, 1), loc="upper left", borderaxespad=0) 
    _fig.tight_layout()
    _fig
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Exercise:**

    - How many more countries can you add before it becomes unreadable?
    - Can you think of strategies to improve readability beyond that number?
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 8 · Small Multiples

    **Small multiples** = the same chart, repeated across subgroups.
    The eye compares *position* across panels effortlessly — one of Tufte's
    most recommended techniques.
    """)
    return


@app.cell
def _(gapminder, plt):
    _regions = sorted(gapminder["region"].unique())
    _fig, _axes = plt.subplots(2, 3, figsize=(13, 8), sharex=True, sharey=True,
                               constrained_layout=True)

    _years_all = sorted(gapminder["year"].unique())
    _cmap = plt.cm.plasma
    _norm = plt.Normalize(vmin=min(_years_all), vmax=max(_years_all))

    for _ax, _region in zip(_axes.flatten(), _regions):
        for _year, _grp in gapminder[gapminder["region"] == _region].groupby("year"):
            _ax.scatter(_grp["fertility"], _grp["life_expect"],
                        c=[_cmap(_norm(_year))], s=12, alpha=0.65, linewidths=0)
        _ax.set_title(_region, fontsize=9, fontweight="bold")

    _fig.supxlabel("Fertility rate", fontsize=11, y=0.01)
    _fig.supylabel("Life expectancy (years)", fontsize=11, x=0.01)
    _sm = plt.cm.ScalarMappable(cmap=_cmap, norm=_norm)
    _cbar = _fig.colorbar(_sm, ax=_axes.flatten(), shrink=0.55, aspect=25, pad=0.03)
    _cbar.set_label("Year", fontsize=10)
    _fig.suptitle("Small multiples: fertility vs. life expectancy, by region, coloured by year",
                  fontsize=12, fontweight="bold")
    _fig
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 9 · From Draft to Polished

    The gap between exploration and communication:
    - **Title** = a message, not a description
    - **Axis labels** = plain language with units, not column names
    - **Direct labels** instead of a legend box
    - **Spine cleanup** (no top, no right border)
    - **Intentional color** (consistent palette)

    ### Exercise:

    Improve the plot on the right in the figure below applying these principles where relevant to build a publication-ready line chart.

    1. Pick **5 countries** from at least 3 different region (`line_subset` was defined towards the beginning of the notebook).
    2. One line per country, labelled at the endpoint — no legend box.
    3. Title that states an **insight**, not just a description.
    4. No top or right spines.
    5. Save as `figures/exercise_1.pdf` (see section 10 for syntax).
    """)
    return


@app.cell
def _(line_subset, plt):
    _fig, (_ax_raw, _ax_pol) = plt.subplots(1, 2, figsize=(13, 5))

    for _country, _grp in line_subset.groupby("country"):
        _ax_raw.plot(_grp["year"], _grp["life_expect"])
    _ax_raw.set_title("Evolution of Life expectancy in 5 countries")
    _ax_raw.set_xlabel("year")
    _ax_raw.set_ylabel("life_expect")
    _ax_raw.spines["top"].set_visible(True)
    _ax_raw.spines["right"].set_visible(True)

    for _country, _grp in line_subset.groupby("country"):
        _line, = _ax_pol.plot(_grp["year"], _grp["life_expect"])
        _last = _grp.iloc[-1]
        _ax_pol.text(_last["year"] + 0.4, _last["life_expect"],
                     _country, color=_line.get_color(), va="center", fontsize=9, fontweight="bold")


    _ax_pol.set_xlim(right=2011)
    _ax_pol.set_xlabel("year")
    _ax_pol.set_ylabel("life_expect")
    _ax_pol.set_title("Evolution of Life expectancy in 5 countries",
                      fontsize=11)
    plt.tight_layout()
    _fig
    return


@app.cell
def _(mo):
    mo.accordion({
            "Hint — Direct labels at line endpoints": mo.md(r"""

        ```python
            ...
            _line, = _ax.plot(_grp["year"], _grp["life_expect"], lw=2.2)
            _last = _grp.iloc[-1]
            _ax.text(_last["year"] + 0.4, _last["life_expect"],
                     _country, color=_line.get_color(),
                     va="center", fontsize=9, fontweight="bold")
            ...
        ```
    """)
    })
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({
        "Hint — code skeleton": mo.md(
            r"""
            ```python
            from pathlib import Path

            _countries = ["...", "...", "...", "...", "..."]
            _subset = gapminder[gapminder["country"].isin(_countries)].sort_values("year")

            _fig, _ax = plt.subplots(figsize=(10, 5))
            for _country, _grp in _subset.groupby("country"):
                _line, = _ax.plot(_grp["year"], _grp["life_expect"], lw=2)
                _last = _grp.iloc[-1]
                _ax.text(_last["year"] + 0.4, _last["life_expect"],
                         _country, color=_line.get_color(), va="center", fontsize=9)

            _ax.set_xlim(right=2011)
            _ax.set_xlabel("Year")
            _ax.set_ylabel("Life expectancy (years)")
            _ax.set_title("Your insight here")
            for spine in ["top", "right"]:
                _ax.spines[spine].set_visible(False)
            Path("figures").mkdir(exist_ok=True)
            _fig.savefig("figures/exercise_1.pdf", bbox_inches="tight")
            ```
            """
        )
    })
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 10 · Exporting Figures

    | Format | Use case |
    |--------|---------|
    | `.png` | Slides, web, reports |
    | `.pdf` | Papers and print — vector, scales to any size |
    | `.svg` | Web, further editing in Inkscape / Illustrator |

    ```python
    fig.savefig("figures/my_figure.pdf", bbox_inches="tight")
    fig.savefig("figures/my_figure.png", bbox_inches="tight", dpi=150)
    ```

    **`bbox_inches="tight"`** trims excess whitespace automatically.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 11 · Seaborn: Philosophy

    Seaborn is built on Matplotlib. It adds two things:

    1. **Statistical defaults** — confidence intervals, kernel density estimates,
       regression lines — without you computing them manually.
    2. **Opinionated aesthetics** — sensible colors, grids, font sizes out of the box.

    The trade-off: less flexibility than raw Matplotlib, but much less code
    for the things data scientists do every day.

    Seaborn charts return an `Axes` or `FacetGrid` — you can always fine-tune
    with Matplotlib afterwards.
    """)
    return


@app.cell
def _(gm2000, plt, sns):
    _fig = plt.figure(figsize=(13, 4))
    for _i, _theme in enumerate(["white", "whitegrid", "darkgrid"]):
        with sns.axes_style(_theme):
            _ax = _fig.add_subplot(1, 3, _i + 1)
            sns.scatterplot(data=gm2000, x="fertility", y="life_expect",
                            hue="region", s=40, alpha=0.75, legend=False, ax=_ax)
            _ax.set_title(f"style='{_theme}'", fontsize=10)

    _fig.suptitle("Same data — three Seaborn style contexts", fontsize=11)
    _fig.tight_layout()
    _fig
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### ML practitioner checkpoint

    Before fitting a classifier, it's advised to inspect the target and feature distributions.
    With Penguins, this means checking class balance and whether a feature
    separates species cleanly enough to be useful.
    """)
    return


@app.cell
def _(penguins, plt, sns):
    _fig, (_ax_count, _ax_mass) = plt.subplots(1, 2, figsize=(11, 4))

    sns.countplot(data=penguins, x="species", hue="species", legend=False, ax=_ax_count)
    _ax_count.set_title("Target balance: species counts")
    _ax_count.set_xlabel("")
    _ax_count.set_ylabel("Count")

    sns.boxplot(
        data=penguins,
        x="species",
        y="body_mass_g",
        hue="species",
        legend=False,
        ax=_ax_mass,
    )
    _ax_mass.set_title("Feature distribution: body mass by species")
    _ax_mass.set_xlabel("")
    _ax_mass.set_ylabel("Body mass (g)")

    plt.tight_layout()
    _fig
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Try it!**

    - Replace `body_mass_g` with `bill_length_mm` or `flipper_length_mm`.
    - Which single feature would you feed to a classifier first, and why?
    - Where do you see overlap that a model might confuse?
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 12 · Visualizing Distributions

    Before looking at relationships, understand each variable on its own.

    | Plot | Best for |
    |------|---------|
    | `histplot` | Raw counts, bin sizes visible |
    | `kdeplot` | Smooth shape, easy to overlay multiple groups |
    | `ecdfplot` | Cumulative view — "what fraction is below X?" |
    | `boxplot` | Compact summary: median, IQR, outliers |
    | `violinplot` | Full distribution shape + quartiles |
    | `swarmplot` | Individual observations for small/medium groups |

    **Caution:** KDE and violin plots estimate a smooth density. Bandwidth is a
    modelling choice; a smooth curve can hide small clusters or imply structure
    that is not really in the data. `swarmplot` avoids overlap by moving points,
    but it does not scale well to large numbers of observations; use `stripplot`
    or sampling when there are too many points.
    """)
    return


@app.cell
def _(gm2000, plt, sns):
    _fig, _axes = plt.subplots(1, 3, figsize=(13, 4))

    sns.histplot(data=gm2000, x="life_expect", bins=20, ax=_axes[0])
    _axes[0].set_title("histplot — raw counts")

    sns.kdeplot(data=gm2000, x="life_expect", ax=_axes[1])
    _axes[1].set_title("kdeplot — smoothed density")

    sns.ecdfplot(data=gm2000, x="life_expect", ax=_axes[2])
    _axes[2].set_title("ecdfplot — cumulative")
    _axes[2].axhline(0.5, color="gray", lw=1, ls="--")
    _axes[2].text(40, 0.52, "median", color="gray", fontsize=8)

    for _ax in _axes:
        _ax.set_xlabel("Life expectancy (years)", fontsize=9)
    plt.tight_layout()
    _fig
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Comparing distributions across groups

    Use `hue=` to overlay multiple groups — one of Seaborn's most useful defaults.
    """)
    return


@app.cell
def _(gm2000, plt, sns):
    _order = (gm2000.groupby("region")["life_expect"]
               .median().sort_values().index.tolist())
    _fig, (_ax1, _ax2) = plt.subplots(1, 2, figsize=(12, 4))

    sns.kdeplot(data=gm2000, x="life_expect", hue="region",
                fill=True, alpha=0.25, linewidth=1., ax=_ax1)
    _ax1.set_title("Life expectancy distribution by region (2000)")
    _ax1.set_xlabel("Life expectancy (years)")

    sns.boxplot(data=gm2000, y="region", x="life_expect",
                order=_order, ax=_ax2, width=0.5)
    _ax2.set_title("Sorted boxplot — easier to rank regions")
    _ax2.set_xlabel("Life expectancy (years)")
    _ax2.set_ylabel("")
    plt.tight_layout()
    _fig
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Box vs. Violin

    A **violin plot** shows the full distribution shape (via KDE), not just quantiles.
    Prefer it when the shape matters — e.g., to spot bimodality.
    """)
    return


@app.cell
def _(gm2000, plt, sns):
    _order = (gm2000.groupby("region")["life_expect"]
               .median().sort_values().index.tolist())
    _fig, (_ax1, _ax2) = plt.subplots(1, 2, figsize=(13, 5), sharey=True)

    sns.boxplot(data=gm2000, y="region", x="life_expect",
                order=_order, ax=_ax1, width=0.5)
    _ax1.set_title("boxplot — quantile summary")
    _ax1.set_xlabel("Life expectancy (years)")
    _ax1.set_ylabel("")

    sns.violinplot(data=gm2000, y="region", x="life_expect",
                   order=_order, ax=_ax2, density_norm="width", inner="quart")
    _ax2.set_title("violinplot — full distribution shape")
    _ax2.set_xlabel("Life expectancy (years)")
    _ax2.set_ylabel("")
    plt.tight_layout()
    _fig
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 13 · Visualizing Relationships

    | Plot | Purpose |
    |------|---------|
    | `scatterplot` | Two quantitative variables, optionally grouped by color/size |
    | `lineplot` | Ordered x-axis; can aggregate repeated x-values and show uncertainty |
    | `regplot` | Scatter + fitted regression line + CI band |

    The regression line is descriptive here, not causal. Country-level fertility
    and life expectancy are ecological aggregates, confounded by many variables.
    """)
    return


@app.cell
def _(gm2000, plt, sns):
    _fig, _axes = plt.subplots(1, 2, figsize=(12, 5))

    sns.scatterplot(data=gm2000, x="fertility", y="life_expect",
                    hue="region", size="pop", sizes=(20, 400), alpha=0.7, ax=_axes[0])
    _axes[0].set_title("scatterplot — hue + size encode extra variables")
    _axes[0].legend(fontsize=7, loc="lower left")

    sns.regplot(data=gm2000, x="fertility", y="life_expect",
                scatter_kws={"alpha": 0.4, "s": 30},
                line_kws={"color": "#C44E52", "lw": 2},
                ax=_axes[1])
    _axes[1].set_title("regplot — regression line + 95% CI band")

    for _ax in _axes:
        _ax.set_xlabel("Fertility rate", fontsize=10)
        _ax.set_ylabel("Life expectancy (years)", fontsize=10)
    plt.tight_layout()
    _fig
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### `lineplot` with built-in uncertainty

    `lineplot` aggregates repeated x-values with `estimator="mean"` and shows a
    **95% bootstrap CI for that mean** by default.

    > **Important**: always caption what your CI band represents.
    > Here it is uncertainty about the estimated regional mean under a sampling
    > interpretation. It is **not** the full spread of countries in the region.
    > To show heterogeneity, plot individual countries or use a spread interval
    > such as `errorbar="sd"` for standard deviation or `errorbar=("pi", 95)` for percentiles.
    """)
    return


@app.cell
def _(gapminder, plt, sns):
    _fig, _ax = plt.subplots(figsize=(10, 5))
    sns.lineplot(data=gapminder, x="year", y="life_expect",
                 hue="region", errorbar=("ci", 95), lw=2, ax=_ax)
    _ax.set_title("Life expectancy over time — mean ± 95% CI per region",
                  fontsize=12, fontweight="bold")
    _ax.set_xlabel("Year")
    _ax.set_ylabel("Life expectancy (years)")
    _ax.legend(fontsize=8, loc="lower right", title="Region")
    plt.tight_layout()
    _fig
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 14 · Grid Plots

    This is the Seaborn version of **small multiples**: repeat the same plot
    across groups so comparisons stay local and aligned.

    | Function | What it does |
    |----------|-------------|
    | `FacetGrid` | Repeat any chart across rows/columns of a categorical variable |
    | `pairplot` | Optional ML EDA shortcut: all pairwise scatter plots + diagonal distributions |
    | `heatmap` | Optional ML EDA shortcut: correlation matrices, pivot tables |
    """)
    return


@app.cell
def _(gm2000, sns):
    _g = sns.FacetGrid(data=gm2000, col="region", col_wrap=3,
                       height=3.2, aspect=1.2, sharex=True, sharey=True)
    _g.map_dataframe(sns.scatterplot, x="fertility", y="life_expect",
                     alpha=0.65, s=25, color="#4C72B0")
    _g.set_axis_labels("Fertility rate", "Life expectancy")
    _g.set_titles(col_template="{col_name}", size=9, fontweight="bold")
    _g.fig.suptitle("FacetGrid: one panel per region (2000)", y=1.02, fontsize=11)
    _g.fig
    return


@app.cell
def _(penguins, sns):
    _pair = sns.pairplot(penguins, hue="species",
                         plot_kws={"alpha": 0.5, "s": 20}, diag_kind="kde")
    _pair.fig.suptitle(
        "pairplot — all pairwise relationships + diagonal KDEs\n"
        "(Palmer Penguins: bill/flipper measurements by species)",
        y=1.01, fontsize=11,
    )
    _pair.fig
    return


@app.cell
def _(gapminder, plt, sns):
    _corr = gapminder[["fertility", "life_expect", "pop", "year"]].corr().round(2)
    _fig, _ax = plt.subplots(figsize=(5, 4))
    sns.heatmap(_corr, annot=True, fmt=".2f", cmap="RdBu_r",
                center=0, square=True, linewidths=0.5, ax=_ax)
    _ax.set_title("Gapminder correlation matrix", fontsize=11)
    plt.tight_layout()
    _fig
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Caution:** a correlation heatmap shows pairwise linear association.
    It can hide nonlinear patterns, subgroup structure, outliers, and changes
    over time. Treat it as a quick EDA index, not as evidence of causality.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 15 · Color and Accessibility

    ~8% of men and ~0.5% of women have some form of color vision deficiency.
    The most common: red-green confusion (deuteranopia / protanopia).

    **Rules of thumb**:
    - **Sequential data**: `viridis`, `plasma`, `cividis` — perceptually uniform
    - **Diverging data** (e.g., correlation): `RdBu`, `coolwarm`
    - **Categorical**: Matplotlib's `tab10` or Seaborn's `"colorblind"` palette
    - **Consistency**: keep the same category → color mapping across plots
    - **Avoid**: red + green together; jet/rainbow for continuous data

    Okabe-Ito is a well-known accessible palette, but it is not available as a
    named palette in the stable Matplotlib/Seaborn versions used here. If you
    need it, define it once and reuse it; otherwise prefer built-in palette APIs.

    Print your chart in greyscale — if information is lost, fix the palette.
    """)
    return


@app.cell
def _(gm2000, plt, sns):
    _order = (gm2000.groupby("region")["life_expect"]
               .median().sort_values().index.tolist())
    _palette_tab10 = sns.color_palette("tab10", n_colors=len(_order))
    _palette_colorblind = sns.color_palette("colorblind", n_colors=len(_order))
    _fig, (_ax1, _ax2) = plt.subplots(1, 2, figsize=(13, 5), sharey=True)

    sns.boxplot(data=gm2000, y="region", x="life_expect",
                hue="region", legend=False,
                order=_order, ax=_ax1, width=0.5, palette=_palette_tab10)
    _ax1.set_title("Matplotlib tab10", fontsize=10)
    _ax1.set_ylabel("")

    sns.boxplot(data=gm2000, y="region", x="life_expect",
                hue="region", legend=False,
                order=_order, ax=_ax2, width=0.5, palette=_palette_colorblind)
    _ax2.set_title("Seaborn colorblind", fontsize=10)
    _ax2.set_ylabel("")

    for _ax in [_ax1, _ax2]:
        _ax.set_xlabel("Life expectancy (years)")
    plt.suptitle("Same chart — different palettes", fontsize=11)
    plt.tight_layout()
    _fig
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Try different palettes.**

    - Replace `"colorblind"` with `"Set2"`, `"Dark2"`, or `"Paired"`.
    - Try Matplotlib's style context: `with plt.style.context("tableau-colorblind10"): ...`
    - For repeated plots, build a mapping once and reuse it:

    ```python
    _levels = sorted(gm2000["region"].dropna().unique())
    _palette = dict(zip(_levels, sns.color_palette("colorblind", n_colors=len(_levels))))

    sns.scatterplot(..., hue="region", hue_order=_levels, palette=_palette)
    sns.boxplot(..., hue="region", hue_order=_levels, palette=_palette)
    ```

    The goal is not to find the prettiest palette. It is to keep categories
    distinguishable, accessible, and consistent across the whole analysis.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Exercise 2 — Uncertainty, Honestly

    The regional `lineplot` above showed the mean life expectancy per region.
    That hides a lot of variation *within* regions.

    1. Pick **one region** and plot life expectancy trajectories for
       **all individual countries** in it (thin grey lines).
    2. Overlay the **regional mean** as a thick coloured line.
    3. Write a title that captures what this reveals beyond the average alone.

    *To go further:*
    - compare one region with low variation and one with high variation
    - try different alpha values: when does overplotting become noise?
    - decide whether the mean line helps or hides the individual trajectories
    - write a caption that says exactly what the grey lines and mean line represent
    """)
    return


@app.cell
def _():
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({
        "Hint": mo.md(
            r"""
            ```python
            _region = "Sub-Saharan Africa"
            _subset = gapminder[gapminder["region"] == _region].sort_values("year")
            _mean = _subset.groupby("year")["life_expect"].mean().reset_index()

            _fig, _ax = plt.subplots(figsize=(9, 5))
            for _country, _grp in _subset.groupby("country"):
                _ax.plot(_grp["year"], _grp["life_expect"],
                         color="#aaa", lw=0.8, alpha=0.6)
            _ax.plot(_mean["year"], _mean["life_expect"],
                     color="#C44E52", lw=2.5, label="Regional mean")
            _ax.legend()
            _ax.set_title("...")
            ```
            """
        )
    })
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Summary

    | Concept | Key takeaway |
    |---------|-------------|
    | Why visualize | Anscombe's Quartet: identical stats, completely different shapes |
    | Tidy data | Prefer long-form data for explicit, reusable mappings |
    | Figure anatomy | `Figure` → `Axes` → artists (lines, patches, text) |
    | Two APIs | `pyplot` for exploration, object-oriented (`fig, ax`) for everything shareable |
    | Visual channels | Ordered and categorical attributes need different channel rankings |
    | Small multiples | Repeat the same chart per group for effortless comparison |
    | Polishing | Title = insight, direct labels, no top/right spines |
    | Seaborn | High-level API on Matplotlib; statistical defaults built in |
    | Distributions | `histplot` → `kdeplot` → `violinplot`; `swarmplot` for small groups |
    | Uncertainty | Distinguish estimate uncertainty from data spread |
    | Color | Use library palette tools; keep category colors consistent; test accessibility |

    **Next session**: Grammar of Graphics + Altair — a principled framework for
    thinking about visualization, and a Python library that implements it directly.
    """)
    return


if __name__ == "__main__":
    app.run()
