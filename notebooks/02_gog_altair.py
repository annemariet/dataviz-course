import marimo

__generated_with = "0.23.2"
app = marimo.App(
    width="medium",
    app_title="Data Visualization — Part 2: Grammar of Graphics & Altair",
)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Part 2 — Grammar of Graphics & Altair

    **Session duration**: ~3 hours &nbsp;|&nbsp; **Datasets**: Gapminder, INSEE prénoms

    ## What you'll be able to do after this session

    - Explain the Grammar of Graphics and decompose any chart into its layers
    - Understand the Vega ecosystem — from D3 to Altair — and why we use Altair
    - Read and write Altair's declarative API fluently
    - Build layered, faceted, and interactive charts with linked views
    - Build a name explorer from real French open data (INSEE baby names)

    ---
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 1 · The Grammar of Graphics

    In 1999, Leland Wilkinson published
    [*The Grammar of Graphics*](https://link.springer.com/book/10.1007/0-387-28695-0)
    (Springer; 2nd ed. 2005) — **GoG** for short — arguing that every statistical
    chart is assembled from the same underlying components — a *grammar* — rather
    than being one item in a fixed menu of named chart types.

    **Why it matters:**
    - You stop asking *"which chart type should I use?"* and start asking
      *"which variables should map to which visual properties?"*
    - You can compose charts that don't have a pre-set name, and know exactly
      how to build them from first principles.
    - Libraries that implement the grammar (ggplot2, Vega-Lite, Altair) become
      predictable: learn it once, apply it everywhere.

    Wickham's [*A Layered Grammar of Graphics*](https://doi.org/10.1198/jcgs.2009.07098)
    (*Journal of Computational and Graphical Statistics*, 2010) is a shorter, more
    accessible reformulation — recommended as a next read after this session (find a pdf version [here](https://ucsb-bren.github.io/ESM296-3W-2016/refs/lit/Wickham%20-%202010%20-%20A%20Layered%20Grammar%20of%20Graphics.pdf)). It is
    also the theoretical foundation of **ggplot2** and, through the Vega-Lite lineage,
    of **Altair**.

    For a hands-on reference beyond this notebook, see the
    [Altair user guide](https://altair-viz.github.io/user_guide/encoding.html) and
    the [Vega-Lite paper](https://doi.org/10.1109/TVCG.2016.2599030)
    (Satyanarayan et al., *IEEE TVCG*, 2017).

    The grammar defines **seven layers** that together fully specify any chart.
    Most layers have sensible defaults — you only override what you need to change:

    | Layer | Question it answers | Example |
    |-------|---------------------|---------|
    | **Data** | What dataset, in what format? | Gapminder, tidy (one row per country-year) |
    | **Aesthetics** | Which variable maps to which visual channel? | `x = fertility`, `color = region` |
    | **Geometry (Mark)** | What shape is drawn for each row? | Point, line, bar, area |
    | **Statistics** | Any aggregation applied before drawing? | Mean per year, KDE, bin counts |
    | **Scales** | How are data values rendered visually? | Log axis, colour gradient, date format |
    | **Facets** | Small multiples along which variable? | One panel per region |
    | **Coordinates** | What coordinate system? | Cartesian (default), polar, geographic |
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.mermaid("""
    flowchart LR
        D["Data\n───\ntidy DataFrame"]
        A["Aesthetics\n───\nx, y, color\nsize, shape"]
        G["Geometry\n───\npoint, line\nbar, area"]
        S["Statistics\n───\nmean, bin\nKDE, count"]
        Sc["Scales\n───\nlog, sqrt\ncolor map"]
        F["Facets\n───\none panel\nper group"]
        C["Coordinates\n───\ncartesian\npolar / geo"]
        D --> A --> G --> S --> Sc --> F --> C
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### GoG lens on charts you already know

    Type codes: `Q` = Quantitative, `T` = Temporal, `N` = Nominal, `O` = Ordinal
    — covered in detail in section 5.

    | "Chart type" | GoG description |
    |-------------|----------------|
    | Scatter plot | Point mark + `x=Q`, `y=Q` |
    | Line chart | Line mark + `x=T`, `y=Q` |
    | Bar chart | Bar mark + `x=N`, `y=aggregate(count)` |
    | Histogram | Bar mark + `x=bin(Q)`, `y=count` |
    | Violin plot | Area mark + KDE statistic + `x=N` |
    | Faceted scatter | Any of the above + `facet=N` |

    Once you have the grammar, you can compose charts that don't have
    a pre-set name — and you'll know exactly how to build them.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 1.5 · Marks, Channels, and Visual Effectiveness

    GoG tells you *what the grammar consists of*. Munzner's framework tells you
    *how to choose encodings that work*.

    **Tamara Munzner**, *Visualization Analysis and Design* (2014), introduces
    two vocabulary terms that apply to any vis system, independent of any library:

    **Marks** — the geometric primitives drawn for each data item:

    | Mark | Typical use |
    |------|------------|
    | Point | Individual items: scatter plots, dot plots |
    | Line | Connected sequences: time series, trends |
    | Area | Filled regions: area charts, maps |
    | Bar | Length-encoded magnitude: bar charts, histograms |

    **Channels** — the visual properties that vary to carry data.
    Not all channels are equally readable. Cleveland & McGill (1984) measured
    empirically how accurately viewers can extract quantitative values from each:

    | Channel | Best data type | Accuracy |
    |---------|---------------|---------|
    | Position on a common scale (x, y) | Quantitative | ★★★★★ most accurate |
    | Position on non-aligned scales | Quantitative | ★★★★☆ |
    | Length | Quantitative | ★★★☆☆ |
    | Angle / slope | Avoid for quantities | ★★☆☆☆ (pie chart problem) |
    | Area | Rough magnitude only | ★★☆☆☆ |
    | Color saturation / density | Ordinal, sequential | ★★☆☆☆ |
    | Color hue | Nominal categories only | ★★☆☆☆ |
    | Shape | Nominal categories only | ★★☆☆☆ |

    **Two design principles** from Mackinlay (1986), synthesised by Munzner:

    - **Expressiveness**: the encoding conveys exactly the information in the data —
      no more, no less. Don't use an ordered channel (position, length) for a nominal
      variable, because it implies an ordering that isn't there.
    - **Effectiveness**: use the most accurate channel for the most important variable.
      Your key quantitative comparison should use position; secondary distinctions use color or shape.

    The classic failure: a pie chart encodes quantities as angles and areas —
    two of the least accurate channels — when a bar chart (position + length from a common baseline)
    would be immediately readable.

    **How this vocabulary maps across frameworks:**

    | Munzner | GoG layer | Altair API |
    |---------|-----------|-----------|
    | Mark | Geometry | `.mark_point()`, `.mark_line()`, `.mark_bar()`, … |
    | Channel (position) | Aesthetics `x`, `y` | `.encode(x="col:Q", y="col:Q")` |
    | Channel (color hue) | Aesthetics `color` | `.encode(color="cat:N")` |
    | Channel (size / area) | Aesthetics `size` | `.encode(size="pop:Q")` |
    | Attribute type | Variable type | `:Q`, `:N`, `:O`, `:T` |

    > When you write `.mark_point().encode(x="gdp:Q", color="region:N")`, you are making
    > explicit design decisions: the quantitative variable gets the most effective channel
    > (position); the nominal variable gets an appropriate channel (hue). That is principled
    > design, not just syntax.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 2 · The Ecosystem: From Theory to Python

    GoG is a theory. Every plotting library is (implicitly or explicitly) an attempt to implement it.

    | Year | Tool | Language | What it is | Source |
    |------|------|----------|-----------|--------|
    | 1999 | **Grammar of Graphics** (Wilkinson) | — | The theory | — |
    | 2005 | **ggplot2** (Wickham) | R | First widely-adopted GoG implementation; the gold standard in R | [GitHub](https://github.com/tidyverse/ggplot2) |
    | 2011 | **D3.js** (Bostock) | JavaScript | Low-level, data-driven SVG — the rendering engine underneath everything | [GitHub](https://github.com/d3/d3) |
    | 2013 | **Vega** (UW IDL) | JSON + JS | Declarative grammar on top of D3 | [GitHub](https://github.com/vega/vega) |
    | 2016 | **Vega-Lite** (UW IDL) | JSON + JS | Compact GoG grammar; compiles to Vega | [GitHub](https://github.com/vega/vega-lite) |
    | 2016 | **Altair** (VanderPlas et al.) | Python | Python API for Vega-Lite — **what we use** | [GitHub](https://github.com/vega/altair) |
    | 2017 | **plotnine** (Kibirige) | Python | ggplot2 API ported to Python; static only (matplotlib backend) | [GitHub](https://github.com/has2k1/plotnine) |
    | 2021 | **Observable Plot** (Bostock) | JavaScript | GoG-inspired high-level JS library, built on D3 | [GitHub](https://github.com/observablehq/plot) |

    **Altair vs plotnine** — both are GoG implementations in Python, different trade-offs:

    | | Altair | plotnine |
    |---|---|---|
    | Output | Web-native, interactive | Static image (matplotlib) |
    | Interactivity | First-class (brushing, linked views) | None built-in |
    | R crossover | New API to learn | Immediate if you know ggplot2 |
    | Statistical transforms | Limited — pre-compute or use Altair transforms | Rich — `geom_smooth`, `stat_density`, etc. |

    We use Altair because interactivity is a first-class goal of this session.
    If you know R and ggplot2, you might want to give plotnine a shot as well.

    **A note on Observable Plot vs Observable:**
    These are two separate products by the same company (Observable, Inc.):
    - **Observable Plot** — an open-source JS library (MIT licence, free forever).
      Think of it as D3's high-level layer, in the same way Altair sits above Vega-Lite.
      D3 is *not* going away — Plot is built on top of it and still needs it for anything
      custom (force graphs, geographic projections, bespoke layouts).
    - **Observable** — a cloud notebook platform for JavaScript (like Jupyter, but reactive
      and browser-native). Free tier available; paid plans for private notebooks and teams.
      Observable notebooks can use Plot, D3, or any JS library.

    **Also common in Python** (but not GoG-native):
    - **Plotly / Plotly Express** — chart-type focused, good for dashboards (Dash)
    - **Bokeh** — interactive, different architecture
    - **Matplotlib / Seaborn** — what you learned in session 1: explicit control, not declarative

    > We will learn to use Altair because it is the most faithful GoG implementation in Python:
    > declarative, composable, interactive by default.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 3 · Altair = Grammar of Graphics in Python

    Every Altair chart maps directly to the GoG layers from §1:

    ```
    alt.Chart(data)          ← DATA
        .mark_point()        ← GEOMETRY (the mark type)
        .encode(             ← AESTHETICS (data → visual channels)
            x="fertility:Q",
            y="life_expect:Q",
            color="region:N",
        )
    ```

    Under the hood, Altair writes a **Vega-Lite JSON spec**, which is then compiled
    into a lower-level **Vega spec** that the browser renders. There are therefore
    two levels of JSON in the pipeline:

    | Level | What it is | How to get it | Editor dropdown |
    |-------|-----------|---------------|-----------------|
    | **Vega-Lite** | Compact, human-readable — what Altair writes | `with alt.data_transformers.enable("default"): print(chart.to_json(indent=2))` | *Vega-Lite* |
    | **Vega** | Compiled, verbose — what the browser renders | `chart.to_json(format="vega")` | *Vega* |

    The Vega-Lite level is what to read: its keys (`mark`, `encoding`, `transform`)
    map one-to-one to the GoG layers. Here is a self-contained Vega-Lite spec you
    can paste straight into the [Vega editor](https://vega.github.io/editor/#/edited)
    — select *Vega-Lite* in the dropdown:

    ```json
    {
      "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
      "data": {
        "url": "https://cdn.jsdelivr.net/npm/vega-datasets@v1.31.1/data/gapminder.json"
      },
      "transform": [{"filter": "datum.year == 2000"}],
      "mark": {"type": "point"},
      "encoding": {
        "x": {"field": "fertility", "type": "quantitative"},
        "y": {"field": "life_expect", "type": "quantitative"},
        "color": {"field": "cluster", "type": "nominal"}
      }
    }
    ```

    **Why the Vega editor is useful:**
    - **Debugging** — when a chart looks wrong, inspecting the spec immediately
      shows whether the issue is in encoding types, missing fields, or transforms.
    - **Experimentation** — tweak a field name or type and re-render instantly,
      without re-running Python.

    We'll see an example chart with its Vega-Lite spec displayed alongside it below.

    We use the same Gapminder dataset as session 1 (63 countries, 1955–2005).
    The cell below loads it — run it whether or not you have session 1 open.
    """)
    return


@app.cell
def _():
    import marimo as mo
    import altair as alt
    import pandas as pd
    import requests
    import io
    import zipfile
    import os
    from vega_datasets import data as vega_data

    # The INSEE prénoms dataset (~300k rows) exceeds Altair's default 5 000-row limit.
    # vegafusion offloads data processing server-side, lifting that limit.
    # Gapminder and Penguins are small enough to work without it.
    alt.data_transformers.enable("vegafusion")
    return alt, io, mo, os, pd, requests, vega_data, zipfile


@app.cell
def _(vega_data):
    gapminder = vega_data.gapminder()
    _region_names = {
        0: "South Asia", 1: "Europe & Central Asia",
        2: "Sub-Saharan Africa", 3: "Americas",
        4: "East Asia & Pacific", 5: "Middle East & N. Africa",
    }
    gapminder["region"] = gapminder["cluster"].map(_region_names)
    return (gapminder,)


@app.cell
def _(alt, gapminder, mo):
    _gm2000 = gapminder[gapminder["year"] == 2000]
    _chart = alt.Chart(_gm2000).mark_point(filled=True, tooltip=True).encode(
        x="fertility:Q",
        y="life_expect:Q",
        color="region:N",
    )
    with alt.data_transformers.enable("default"):
        _spec = _chart.to_json(indent=2)
    mo.hstack([_chart, mo.md(f"```json\n{_spec}\n```")])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    Hover over the points — `tooltip=True` on the mark enables tooltips
    for all encoded fields. Use `tooltip=[...]` in `.encode()` to customise which fields appear.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 4 · Marks

    The mark defines the **geometry** — what shape is drawn for each data row.

    | Mark | Method | Best for |
    |------|--------|---------|
    | Point | `mark_point()` | Scatter plots — hollow by default; use `filled=True` for solid |
    | Line | `mark_line()` | Time series, trends |
    | Bar | `mark_bar()` | Counts, aggregates |
    | Area | `mark_area()` | Filled time series |
    | Tick | `mark_tick()` | Strip plots, rug plots |
    | Rule | `mark_rule()` | Reference lines |
    | Text | `mark_text()` | Labels on chart |
    | Rect | `mark_rect()` | Heatmaps |

    Configure with properties: `mark_point(size=60, opacity=0.7, filled=True)`.

    `mark_circle()` is a shorthand alias for `mark_point(shape="circle", filled=True)` — same result.
    """)
    return


@app.cell
def _(alt, gapminder):
    _gm2000 = gapminder[gapminder["year"] == 2000]
    _base = alt.Chart(_gm2000).encode(x="fertility:Q", y="life_expect:Q")
    alt.hconcat(
        _base.mark_point(opacity=0.7).properties(title="mark_point (hollow)"),
        _base.mark_point(filled=True, opacity=0.7).properties(title="mark_point(filled=True)"),
        _base.mark_tick(thickness=1).properties(title="mark_tick"),
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 5 · Encodings and Data Types

    Altair needs to know the *type* of each variable to choose scales, axes, and legends.

    | Type | Code | Examples |
    |------|------|---------|
    | Quantitative | `:Q` | Temperature, population, price |
    | Ordinal | `:O` | Low/medium/high, survey scores |
    | Nominal | `:N` | Country, species, category |
    | Temporal | `:T` | Dates, timestamps |

    **Shorthand**: `"column:Q"` &nbsp;|&nbsp; **Longhand**: `alt.X("column", type="quantitative", title="…")`
    """)
    return


@app.cell
def _(alt, gapminder):
    _gm2000 = gapminder[gapminder["year"] == 2000]
    alt.Chart(_gm2000).mark_point(filled=True, opacity=0.75).encode(
        x=alt.X("fertility:Q", title="Fertility rate (children per woman)"),
        y=alt.Y("life_expect:Q", title="Life expectancy (years)"),
        color=alt.Color("region:N", title="Region",
                        scale=alt.Scale(scheme="tableau10")),
        size=alt.Size("pop:Q", title="Population",
                      scale=alt.Scale(range=[20, 600])),
        tooltip=["country:N", "fertility:Q", "life_expect:Q", "region:N"],
    ).properties(title="Gapminder 2000 — hover for details", width=550, height=380)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 6 · Marimo Reactivity + Altair

    Marimo's reactive execution means a widget in one cell
    automatically updates every cell that depends on it.
    """)
    return


@app.cell
def _(mo):
    year_slider = mo.ui.slider(1955, 2005, step=5, value=2000, label="Year")
    year_slider
    return (year_slider,)


@app.cell
def _(alt, gapminder, year_slider):
    _gm = gapminder[gapminder["year"] == year_slider.value]
    alt.Chart(_gm).mark_point(filled=True, opacity=0.75).encode(
        x=alt.X("fertility:Q", scale=alt.Scale(domain=[0, 9]), title="Fertility rate"),
        y=alt.Y("life_expect:Q", scale=alt.Scale(domain=[20, 90]),
                title="Life expectancy (years)"),
        color=alt.Color("region:N", scale=alt.Scale(scheme="tableau10")),
        size=alt.Size("pop:Q", scale=alt.Scale(range=[20, 600])),
        tooltip=["country:N", "year:O", "fertility:Q", "life_expect:Q"],
    ).properties(title=f"Gapminder {year_slider.value}", width=550, height=380)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    Move the slider — the chart updates reactively. This is Marimo's execution model.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 7 · Transforms — Data Before Drawing

    Altair can transform data *inside the specification* — no pandas groupby needed.

    | Transform | What it does |
    |-----------|-------------|
    | Filter | Keep rows matching a condition |
    | Aggregate | Compute statistics per group (`mean(col):Q`) |
    | Calculate | Add a computed column |
    | Bin | Group a continuous variable into bins |
    | Fold | Wide → long (like `melt`) |

    Shorthand aggregation: `"mean(life_expect):Q"`.
    """)
    return


@app.cell
def _(alt, gapminder):
    _gm2000 = gapminder[gapminder["year"] == 2000]
    alt.Chart(_gm2000).mark_bar().encode(
        x=alt.X("mean(life_expect):Q", title="Mean life expectancy (years)"),
        y=alt.Y("region:N", sort="-x", title=""),
        color=alt.Color("region:N", legend=None, scale=alt.Scale(scheme="tableau10")),
        tooltip=[
            alt.Tooltip("region:N"),
            alt.Tooltip("mean(life_expect):Q", format=".1f", title="Mean"),
            alt.Tooltip("count():Q", title="n countries"),
        ],
    ).properties(title="Mean life expectancy by region — 2000", width=480, height=260)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 8 · Layering Charts

    Add layers with `+`. Each layer can use different marks or data.

    ```python
    points = alt.Chart(df).mark_point()...
    regression = alt.Chart(df).mark_line()...
    points + regression   # ← layered
    ```
    """)
    return


@app.cell
def _(alt, gapminder):
    _gm2000 = gapminder[gapminder["year"] == 2000]
    _base = alt.Chart(_gm2000).encode(
        x=alt.X("fertility:Q", title="Fertility rate"),
        y=alt.Y("life_expect:Q", title="Life expectancy (years)"),
    )
    _points = _base.mark_point(filled=True, opacity=0.6, size=50).encode(
        color=alt.Color("region:N", scale=alt.Scale(scheme="tableau10")),
        tooltip=["country:N", "fertility:Q", "life_expect:Q"],
    )
    _reg = (_base.mark_line(color="#C44E52", strokeWidth=2, opacity=0.8)
                 .transform_regression("fertility", "life_expect"))
    (_points + _reg).properties(
        title="Scatter + regression line — layered with +", width=540, height=360,
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 9 · Concatenation and Facets

    | Operator | Creates |
    |----------|---------|
    | `a \| b` | Side by side |
    | `a & b` | Stacked vertically |
    | `.facet("col:N", columns=3)` | Small multiples |
    """)
    return


@app.cell
def _(alt, gapminder):
    _gm2000 = gapminder[gapminder["year"] == 2000]
    alt.Chart(_gm2000).mark_point(filled=True, opacity=0.65, size=30).encode(
        x=alt.X("fertility:Q", title="Fertility rate"),
        y=alt.Y("life_expect:Q", title="Life expectancy"),
        color=alt.Color("region:N", legend=None, scale=alt.Scale(scheme="tableau10")),
        tooltip=["country:N", "fertility:Q", "life_expect:Q"],
    ).facet("region:N", columns=3).properties(
        title="Faceted scatter: one panel per region (Gapminder 2000)",
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 10 · Interactivity — Selections

    Altair's interactivity is built on **selections** (params).
    A selection is a filter — points inside are highlighted, others dimmed.

    | Selection | Triggered by | Use case |
    |-----------|-------------|---------|
    | `selection_point()` | Click | Highlight individual points or legend entries |
    | `selection_interval()` | Click-drag | Brush a rectangular region |

    Wire into encodings with `condition()`:
    ```python
    sel = alt.selection_point()
    color = alt.condition(sel, alt.Color("region:N"), alt.value("lightgray"))
    chart.add_params(sel).encode(color=color)
    ```
    """)
    return


@app.cell
def _(alt, gapminder):
    _gm2000 = gapminder[gapminder["year"] == 2000]
    _sel = alt.selection_point(fields=["region"], bind="legend")
    alt.Chart(_gm2000).mark_point(filled=True, size=60).encode(
        x=alt.X("fertility:Q", title="Fertility rate"),
        y=alt.Y("life_expect:Q", title="Life expectancy (years)"),
        color=alt.condition(
            _sel,
            alt.Color("region:N", scale=alt.Scale(scheme="tableau10")),
            alt.value("lightgray"),
        ),
        opacity=alt.condition(_sel, alt.value(0.85), alt.value(0.15)),
        size=alt.Size("pop:Q", scale=alt.Scale(range=[20, 500])),
        tooltip=["country:N", "region:N", "fertility:Q", "life_expect:Q"],
    ).add_params(_sel).properties(
        title="Click a region in the legend to highlight it",
        width=560, height=380,
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Linked views — the most powerful interaction pattern

    Two charts sharing a selection: brushing one filters the other.
    This is where interactive charts genuinely help exploratory analysis.
    """)
    return


@app.cell
def _(alt, gapminder):
    _gm2000 = gapminder[gapminder["year"] == 2000]
    _brush = alt.selection_interval()

    _scatter = (
        alt.Chart(_gm2000).mark_point(filled=True, opacity=0.7, size=50).encode(
            x=alt.X("fertility:Q", title="Fertility rate"),
            y=alt.Y("life_expect:Q", title="Life expectancy"),
            color=alt.condition(
                _brush,
                alt.Color("region:N", scale=alt.Scale(scheme="tableau10"), legend=None),
                alt.value("lightgray"),
            ),
            tooltip=["country:N", "region:N"],
        )
        .add_params(_brush)
        .properties(width=330, height=280, title="Drag to select countries")
    )

    _bar = (
        alt.Chart(_gm2000).mark_bar().encode(
            x=alt.X("count():Q", title="Countries"),
            y=alt.Y("region:N", sort="-x", title=""),
            color=alt.Color("region:N", scale=alt.Scale(scheme="tableau10"), legend=None),
        )
        .transform_filter(_brush)
        .properties(width=330, height=280, title="Region breakdown of selection")
    )

    _scatter | _bar
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Drag a selection box on the scatter — the bar chart updates instantly.

    This **brush-one, filter-another** pattern is one of the most effective tools
    for exploratory analysis.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 11 · French Open Data: Baby Names (INSEE)

    The **national baby names database** from INSEE covers all births
    in France from 1900 to 2023 (~4 MB, cached after first run).

    Source: [INSEE — Fichier des prénoms](https://www.insee.fr/fr/statistiques/7633685)

    Columns: `sex` (Male/Female), `name`, `year`, `count`
    """)
    return


@app.cell
def _(io, os, pd, requests, zipfile):
    def _clean(df):
        df.columns = ["sex", "name", "year", "count"]
        df = df[df["year"] != "XXXX"].copy()
        df["year"] = df["year"].astype(int)
        df["count"] = df["count"].astype(int)
        df["sex"] = df["sex"].map({"1": "Male", "2": "Female"})
        df["name"] = df["name"].str.title()
        return df[df["year"] >= 1950]

    def _load(cache="data/prenoms.parquet"):
        os.makedirs("data", exist_ok=True)
        if os.path.exists(cache):
            return pd.read_parquet(cache)

        _urls = [
            "https://www.insee.fr/fr/statistiques/fichier/7633685/nat2023_csv.zip",
            "https://www.insee.fr/fr/statistiques/fichier/2540004/nat2021_csv.zip",
        ]
        for _url in _urls:
            try:
                _r = requests.get(_url, timeout=30)
                _r.raise_for_status()
                with zipfile.ZipFile(io.BytesIO(_r.content)) as _z:
                    _fname = next(n for n in _z.namelist() if n.endswith(".csv"))
                    with _z.open(_fname) as _f:
                        _df = pd.read_csv(_f, sep=";", encoding="utf-8", dtype=str)
                _df = _clean(_df)
                _df.to_parquet(cache, index=False)
                return _df
            except Exception:
                continue

        print("⚠️  Could not download INSEE data — using a small built-in sample.")
        _sample = pd.DataFrame({
            "sex":   ["Female"]*6 + ["Male"]*6,
            "name":  ["Marie","Marie","Marie","Emma","Emma","Emma",
                      "Jean","Jean","Jean","Lucas","Lucas","Lucas"],
            "year":  [1960, 1980, 2000]*4,
            "count": [35000,20000,8000, 500,4000,15000,
                      50000,30000,10000, 200,3000,18000],
        })
        return _sample

    prenoms = _load()
    return (prenoms,)


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### Most popular names in France since 1950
    """)
    return


@app.cell
def _(alt, prenoms):
    _top = (
        prenoms.groupby(["name", "sex"], as_index=False)["count"]
        .sum().sort_values("count", ascending=False).head(30)
    )
    alt.Chart(_top).mark_bar().encode(
        x=alt.X("count:Q", title="Total births since 1950"),
        y=alt.Y("name:N", sort="-x", title=""),
        color=alt.Color("sex:N",
                        scale=alt.Scale(domain=["Male", "Female"],
                                        range=["#4C72B0", "#DD8452"])),
        tooltip=["name:N", "sex:N", alt.Tooltip("count:Q", format=",")],
    ).properties(title="30 most common names in France since 1950", width=460, height=520)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Name trends over time

    The chart normalises by total births per year — showing *popularity share*
    rather than raw counts (birth rates changed considerably over 70 years).
    """)
    return


@app.cell
def _(mo):
    name_input = mo.ui.text(
        value="Marie, Jean, Emma, Lucas",
        label="Names to compare (comma-separated)",
    )
    name_input
    return (name_input,)


@app.cell
def _(alt, name_input, prenoms):
    _names = [n.strip().title() for n in name_input.value.split(",") if n.strip()]
    _totals = (
        prenoms.groupby(["year", "sex"])["count"].sum()
        .reset_index().rename(columns={"count": "total"})
    )
    _trend = (
        prenoms[prenoms["name"].isin(_names)]
        .merge(_totals, on=["year", "sex"])
        .assign(share=lambda d: d["count"] / d["total"] * 10_000)
    )
    if _trend.empty:
        _chart = alt.Chart({"values": [{}]}).mark_text().encode(
            text=alt.value("No names found — try: Marie, Jean, Emma, Lucas")
        )
    else:
        _chart = alt.Chart(_trend).mark_line(strokeWidth=2.2).encode(
            x=alt.X("year:Q", title="Year", axis=alt.Axis(format="d")),
            y=alt.Y("share:Q", title="Babies per 10 000 births"),
            color=alt.Color("name:N", title="Name"),
            strokeDash=alt.StrokeDash(
                "sex:N",
                scale=alt.Scale(domain=["Male", "Female"], range=[[1, 0], [4, 2]]),
                legend=alt.Legend(title="Sex"),
            ),
            tooltip=["name:N", "sex:N", "year:Q",
                     alt.Tooltip("share:Q", format=".1f", title="per 10 000")],
        ).properties(
            title="Name trends in France — popularity per 10 000 births",
            width=580, height=360,
        ).interactive()
    _chart
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    Try: `Marie, Camille, Théo, Léa` to see how naming fashions cycle.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### The name diversity explosion — distinct names used per year
    """)
    return


@app.cell
def _(alt, prenoms):
    _div = (
        prenoms.groupby(["year", "sex"])["name"].nunique()
        .reset_index().rename(columns={"name": "distinct_names"})
    )
    alt.Chart(_div).mark_area(opacity=0.7).encode(
        x=alt.X("year:Q", title="Year", axis=alt.Axis(format="d")),
        y=alt.Y("distinct_names:Q", title="Distinct names used"),
        color=alt.Color("sex:N",
                        scale=alt.Scale(domain=["Male", "Female"],
                                        range=["#4C72B0", "#DD8452"])),
        tooltip=["year:Q", "sex:N",
                 alt.Tooltip("distinct_names:Q", format=",", title="Distinct names")],
    ).properties(
        title="Name diversity in France: distinct names per year",
        width=580, height=300,
    ).interactive()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Exercise 1 — GoG Decomposition

    Pick any chart you've created in Session 1 or 2 and decompose it
    using the Grammar of Graphics framework:

    | Layer | Your answer |
    |-------|------------|
    | Data | |
    | Aesthetics | |
    | Geometry | |
    | Statistics | |
    | Scales | |
    | Facets | |
    | Coordinates | |

    Then ask: are there unused layers? Could adding one make the chart more informative?
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Exercise 2 — GoG Spec from Scratch

    Using the French prénoms data, build an Altair chart showing the
    **top 15 names given in 2020** using only Altair transforms (no pandas):

    1. `transform_filter` to keep only 2020
    2. `transform_aggregate` to sum counts per name and sex
    3. `transform_window` + `transform_filter` to keep the top 15
    4. Color by sex, sort by count descending, tooltip with name/sex/count
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({
        "Hint — transform chain": mo.md(
            r"""
            ```python
            alt.Chart(prenoms).mark_bar().encode(
                x=alt.X("total:Q", title="Births"),
                y=alt.Y("name:N", sort="-x"),
                color=alt.Color("sex:N", ...),
                tooltip=[...],
            ).transform_filter(
                alt.datum.year == 2020
            ).transform_aggregate(
                total="sum(count)",
                groupby=["name", "sex"],
            ).transform_window(
                rank="rank(total)",
                sort=[alt.SortField("total", order="descending")],
            ).transform_filter(alt.datum.rank <= 15)
            ```
            """
        )
    })
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Exercise 3 — Your Own Interactive Chart

    Build one interactive chart using either Gapminder or INSEE prénoms.

    Requirements:
    - At least **one selection** (brush or click) that changes the visual
    - A **tooltip** with at least 3 informative fields
    - A title that states an insight

    Directions:
    - Gapminder: linked view — scatter + timeline of selected countries
    - Prénoms: brush on a time series → reveal which names were popular in that period
    - Prénoms: interactive bump chart of name rankings per decade
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Summary

    | Concept | Key takeaway |
    |---------|-------------|
    | Grammar of Graphics | Data → Aesthetics → Geometry → Statistics → Scales → Facets |
    | GoG payoff | Compose any chart from first principles — not just named types |
    | Vega-Lite | Declarative JSON grammar; Altair generates it; Vega renders it via D3 |
    | Altair = GoG | `Chart(data).mark_X().encode(...)` = data → geometry → aesthetics |
    | Encoding types | `:Q` quantitative, `:N` nominal, `:O` ordinal, `:T` temporal |
    | Transforms | Filter, aggregate, calculate — keep transformation in the spec |
    | Layering | `chart1 + chart2` — different marks or data, same axes |
    | Faceting | `.facet("col:N")` — small multiples in one line |
    | Selections | `selection_point()` / `selection_interval()` → `condition()` |
    | Linked views | Share a selection across panels for exploratory analysis |

    ---

    ## Where to go next

    - **Altair gallery**: [altair-viz.github.io/gallery](https://altair-viz.github.io/gallery/)
    - **Vega-Lite docs**: the authoritative reference — Altair compiles to this
    - **Observable**: browser-based notebooks, great for sharing interactive charts publicly
    - **Streamlit / Marimo app mode**: wrap an Altair chart in a deployable web app
    - **Further reading**: Munzner (2014) *Visualization Analysis and Design*;
      Franconeri et al. (2021) *The Science of Visual Data Communication*
    """)
    return


if __name__ == "__main__":
    app.run()
