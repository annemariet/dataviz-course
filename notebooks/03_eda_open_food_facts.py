import marimo

__generated_with = "0.23.8"
app = marimo.App(
    width="medium",
    app_title="Session 3 — EDA, scale, and story (Open Food Facts)",
)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Session 3: EDA, scale, and story

    **Dataset:** [Open Food Facts](https://world.openfoodfacts.org/) (worldwide product database)

    **Guiding question:** How do you use data visualization to explore a wide, messy, million-row dataset and when do you switch from exploring to explaining?

    ---
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 1. Setup and data load

    We read a **Parquet** file with [DuckDB](https://duckdb.org/docs/data/parquet/overview) and keep only a sample of rows in memory.

    **Data:** pre-built Parquet on [course SharePoint](https://universitedauphine.sharepoint.com/:u:/r/sites/upd_25_a5aias150_espacepromo/Documents%20partages/Visualisation%20de%20donn%C3%A9es/data/openfoodfacts.parquet?csf=1&web=1&e=XeGvP6) (Dauphine login).

    - **Easiest:** download in the browser → save as `data/openfoodfacts.parquet`
    - **Optional:** `export PARQUET_URL="..."` for a direct-download URL (automated fetch may still fail on SharePoint)
    """)
    return


@app.cell
def _():
    import marimo as mo
    import pandas as pd
    import altair as alt
    import seaborn as sns
    import matplotlib.pyplot as plt
    import duckdb
    from skrub import TableReport

    sns.set_theme(style="whitegrid", palette="muted")
    alt.data_transformers.disable_max_rows()

    from course_data import (
        PARQUET_PATH,
        parquet_bind_path,
        resolve_parquet_url,
        validate_country,
        validate_nutrient,
        validate_sample_n,
    )

    # DuckDB: bind values with ? placeholders; allowlist for column names.
    PARQUET_URL = resolve_parquet_url()
    SAMPLE_N = 100_000
    COUNTRY = None
    GRADES = ["A", "B", "C", "D", "E"]
    GRADE_COLORS = {
        "A": "#1a9641",
        "B": "#a6d96a",
        "C": "#d4c000",
        "D": "#fdae61",
        "E": "#d7191c",
    }
    NOVA_COLORS = {1: "#2ca02c", 2: "#98df8a", 3: "#ffbb78", 4: "#d62728"}
    return (
        COUNTRY,
        GRADES,
        GRADE_COLORS,
        NOVA_COLORS,
        PARQUET_PATH,
        PARQUET_URL,
        SAMPLE_N,
        TableReport,
        alt,
        duckdb,
        mo,
        parquet_bind_path,
        plt,
        sns,
        validate_country,
        validate_nutrient,
        validate_sample_n,
    )


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Exercise 1.1: Change the sample size

    Edit `SAMPLE_N` in the cell above (try `50_000` or `200_000`), then check the load cell re-runs below.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Exercise 1.2: Set a country filter

    Set `COUNTRY = "en:france"` in the setup cell, then check the load cell re-runs. Compare row counts printed below.
    """)
    return


@app.cell
def _(PARQUET_PATH, PARQUET_URL):
    from course_data import ensure_openfoodfacts_parquet

    ensure_openfoodfacts_parquet(PARQUET_PATH, PARQUET_URL)
    print(f"Using Parquet: {PARQUET_PATH}")
    return


@app.cell
def _(
    COUNTRY,
    PARQUET_PATH,
    SAMPLE_N,
    duckdb,
    parquet_bind_path,
    validate_country,
    validate_sample_n,
):
    _path = parquet_bind_path(PARQUET_PATH)
    _sample_n = validate_sample_n(SAMPLE_N)
    _country = validate_country(COUNTRY)
    _sample_clause = f"USING SAMPLE {_sample_n} ROWS (reservoir, 42)"

    if _country:
        df_raw = duckdb.sql(
            """
            SELECT *
            FROM read_parquet($path)
            WHERE countries_tags LIKE $country_pattern
            """
            + _sample_clause,
            params={"path": _path, "country_pattern": f"%{_country}%"},
        ).df()
    else:
        df_raw = duckdb.sql(
            """
            SELECT *
            FROM read_parquet($path)
            """
            + _sample_clause,
            params={"path": _path},
        ).df()
    print(f"Loaded {len(df_raw):,} rows, {len(df_raw.columns)} columns")
    return (df_raw,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 2. Explore vs explain

    **Explore:** you do not know the story yet. You count, filter, and plot to find out what's in the data. Possible questions:
    - what kind of patterns are there in the data?
    - are there surprising patterns that would make an interesting story?
    - are there issues which could be solved using statistics or machine learning?
    - do I have my own questions I could answer with this data?

    **Explain:** you know the message. Every chart supports one conclusion. The title states that conclusion, not the axes.

    **Bin → aggregate → render:** for large data, compute statistics in SQL (eg through DuckDB), so you can pass a small table to [Altair](https://altair-viz.github.io/).

    **First plot idea:** Missing values! Even before you plot distributions, this allows filtering broken fields.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 3. First look

    Stat cards, an interactive table, and missingness patterns.
    """)
    return


@app.cell
def _(df_raw, mo):
    _n = len(df_raw)
    _cols = len(df_raw.columns)
    _graded = df_raw["nutriscore_grade"].notna().sum()
    mo.hstack(
      [
          mo.stat(label="Rows in sample", value=f"{_n:,}"),
          mo.stat(label="Columns", value=str(_cols)),
          mo.stat(label="With Nutri-Score", value=f"{_graded:,}"),
      ],
      justify="start",
      gap=2,
      )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Let's see what columns we have
    """)
    return


@app.cell
def _(df_raw):
    df_raw.head().T
    return


@app.cell
def _(TableReport, df_raw):
    CORE_COLS = [
        "product_name",
        "brands",
        "categories",
        "nutriscore_grade",
        "nova_group",
        "energy-kcal_100g",
        "sugars_100g",
        "fat_100g",
    ]
    TableReport(df_raw[CORE_COLS].head(500))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Exercise 3.1: Explore more columns distributions
    """)
    return


@app.cell
def _(TableReport, df_raw):
    # Find columns for nutrients, vitamins or addititives in product
    # comp_cols = [c for c in df_raw.columns if "100g" in c]
    # comp_cols

    # note the nutrients columns (fat, saturated-fat, proteins, etc.)
    NUTRIENT_COLS = [
        "fat_100g",
        "salt_100g",
        "fiber_100g",
    ]
    TableReport(df_raw[NUTRIENT_COLS].head(500))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Exercise 3.2: Toggle worldwide vs France scope

    Compare `COUNTRY = None` vs `COUNTRY = "en:france"` using Exercise 1.2. Note how grade mix changes.
    """)
    return


@app.cell
def _(df_raw, plt, sns):
    top_miss = df_raw.isna().mean().sort_values(ascending=False).head(25)
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.barplot(x=top_miss.values, y=top_miss.index, ax=ax, color="steelblue")
    ax.set_xlabel("Fraction missing")
    ax.set_title("Top 25 columns by missingness")
    plt.tight_layout()
    fig
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 4. Scale patterns

    **Projection:** read only the columns you need.

    **Sampling:** `USING SAMPLE` in DuckDB draws rows while scanning the file.

    **[Predicate pushdown](https://www.dremio.com/wiki/predicate-pushdown/)** means applying filters (WHERE clauses) in the database engine before rows reach Python, so less data is transferred. Filter to valid rows *before* sampling so the sample is useful for modeling (Section 4 exercise).
    """)
    return


@app.cell
def _(PARQUET_PATH, SAMPLE_N, duckdb, parquet_bind_path, validate_sample_n):
    _path = parquet_bind_path(PARQUET_PATH)
    _sample_n = validate_sample_n(SAMPLE_N)
    _sample_clause = f"USING SAMPLE {_sample_n} ROWS (reservoir, 1)"
    _filtered_sample_clause = f"USING SAMPLE {_sample_n} ROWS (reservoir, 2)"

    _blind = duckdb.sql(
        """
        SELECT count(*) AS n
        FROM read_parquet($path)
        """
        + _sample_clause,
        params={"path": _path},
    ).df()["n"][0]
    _filtered = duckdb.sql(
        """
        SELECT count(*) AS n FROM (
            SELECT 1
            FROM read_parquet($path)
            WHERE sugars_100g IS NOT NULL
              AND lower(nutriscore_grade) IN ('a','b','c','d','e')
        ) """
        + _filtered_sample_clause,
        params={"path": _path},
    ).df()["n"][0]
    print(f"Blind sample rows: {_blind:,}")
    print(f"After nutrient + grade filter, then sample: {_filtered:,}")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Exercise 4.1: Edit the WHERE clause

    In the cell above, add `AND nova_group IS NOT NULL` to the filtered query. Re-run and compare counts.

    ### Exercise 4.2: Compare printed row counts

    What could be the consequence downstream of sampling at the wrong level?
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 5. Nutrient landscape

    Histograms are binned in DuckDB so Altair receives hundreds of rows, not millions.
    """)
    return


@app.cell
def _(PARQUET_PATH, alt, duckdb, parquet_bind_path, validate_nutrient):
    _nutrient = validate_nutrient("sugars_100g")
    _path = parquet_bind_path(PARQUET_PATH)
    _hist = duckdb.sql(
        f"""
        SELECT floor("{_nutrient}" / 2) * 2 AS bin, count(*) AS n
        FROM read_parquet($path)
        WHERE "{_nutrient}" BETWEEN $lo AND $hi
        GROUP BY 1 ORDER BY 1
        """,
        params={"path": _path, "lo": 0, "hi": 80},
    ).df()
    alt.Chart(_hist, title=f"Binned distribution of {_nutrient}").mark_bar().encode(
        x="bin:Q",
        y="n:Q",
    ).properties(width=500, height=280)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Exercise 5.1: Swap the nutrient in the ridge-style plot

    In the cell below, create a `RIDGE_NUTRIENT` to `fat_100g` or `salt_100g`, then re-run.
    Then use a dropdown with the nutrients list created earlier.
    """)
    return


@app.cell
def _(GRADES, GRADE_COLORS, df_raw, plt, sns):
    RIDGE_NUTRIENT = "sugars_100g"  # Exercise 5.1: change nutrient here
    _df = df_raw[["nutriscore_grade", RIDGE_NUTRIENT]].dropna().copy()
    _df["grade"] = _df["nutriscore_grade"].str.upper()
    _df = _df[_df["grade"].isin(GRADES)]
    _df = _df[_df[RIDGE_NUTRIENT].between(0, 60)]
    def violin_plot_nutrients(df):
        fig, ax = plt.subplots(figsize=(9, 4))
        sns.violinplot(
            data=_df,
            x="grade",
            y=RIDGE_NUTRIENT,
            hue="grade",
            order=GRADES,
            palette=GRADE_COLORS,
            ax=ax,
        )
        ax.set_title(f"{RIDGE_NUTRIENT} by Nutri-Score grade")
        plt.tight_layout()
        return fig

    violin_plot_nutrients(_df)
    return


@app.cell
def _(df_raw, plt, sns):
    _nums = [
        c
        for c in [
            "energy-kcal_100g",
            "fat_100g",
            "saturated-fat_100g",
            "sugars_100g",
            "salt_100g",
            "proteins_100g",
        ]
        if c in df_raw.columns
    ]
    _corr = df_raw[_nums].corr()

    def plot_correlations(df):
        fig, ax = plt.subplots(figsize=(6, 5))
        sns.heatmap(df, annot=True, fmt=".2f", cmap="RdBu_r", center=0, ax=ax)
        ax.set_title("Nutrient correlations")
        plt.tight_layout()
        return fig

    plot_correlations(_corr)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Exercise 5.2: Pick two nutrients in the heatmap

    Check for nutrients correlations. Which could you drop for a simple model?

    ### Exercise 5.3: Change the brush variable

    In the linked scatter below, map `color` to `nova_group` instead of `grade`.
    """)
    return


@app.cell
def _(GRADES, GRADE_COLORS, NOVA_COLORS, PARQUET_PATH, alt, duckdb, parquet_bind_path):
    _path = parquet_bind_path(PARQUET_PATH)
    _lk = duckdb.sql(
        """
        SELECT sugars_100g, fat_100g, upper(nutriscore_grade) AS grade,
               nova_group, product_name
        FROM read_parquet($path)
        WHERE sugars_100g BETWEEN $sugars_lo AND $sugars_hi
          AND fat_100g BETWEEN $fat_lo AND $fat_hi
          AND lower(nutriscore_grade) IN ('a','b','c','d','e')
          AND nova_group IS NOT NULL
        USING SAMPLE 6000 ROWS (reservoir, 42)
        """,
        params={
            "path": _path,
            "sugars_lo": 0,
            "sugars_hi": 70,
            "fat_lo": 0,
            "fat_hi": 60,
        },
    ).df()
    BRUSH_COLOR_FIELD = "grade"  # Exercise 5.3: try "nova_group"
    brush = alt.selection_interval(name="brush", empty=True)
    _grade_scale = alt.Scale(
        domain=GRADES,
        range=[GRADE_COLORS[g] for g in GRADES],
    )
    _nova_scale = alt.Scale(
        domain=[1, 2, 3, 4],
        range=[NOVA_COLORS[g] for g in [1, 2, 3, 4]],
    )
    _scatter_color = (
        alt.Color("nova_group:N", scale=_nova_scale, legend=None)
        if BRUSH_COLOR_FIELD == "nova_group"
        else alt.Color("grade:N", sort=GRADES, scale=_grade_scale, legend=None)
    )
    _scatter = (
        alt.Chart(_lk)
        .mark_point(size=14)
        .encode(
            x=alt.X("sugars_100g:Q", title="Sugars (g/100g)"),
            y=alt.Y("fat_100g:Q", title="Fat (g/100g)"),
            color=_scatter_color,
            opacity=alt.condition(brush, alt.value(0.75), alt.value(0.12)),
            tooltip=["product_name", "grade", "nova_group"],
        )
        .properties(width=320, height=300, title="Brush a region")
        .add_params(brush)
    )
    _grade_bar = (
        alt.Chart(_lk)
        .mark_bar()
        .encode(
            x=alt.X("grade:N", sort=GRADES),
            y=alt.Y("count():Q", title="in selection"),
            color=alt.Color("grade:N", sort=GRADES, scale=_grade_scale, legend=None),
        )
        .transform_filter(brush)
        .properties(width=180, height=300, title="Grades")
    )
    _nova_bar = (
        alt.Chart(_lk)
        .mark_bar()
        .encode(
            x=alt.X("nova_group:O", title="NOVA"),
            y=alt.Y("count():Q", title=None),
            color=alt.Color("nova_group:N", scale=_nova_scale, legend=None),
        )
        .transform_filter(brush)
        .properties(width=180, height=300, title="NOVA groups")
    )
    (_scatter | _grade_bar | _nova_bar).resolve_scale(color="independent")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 6. More exploration!

    Linked views use [Altair selections](https://altair-viz.github.io/user_guide/interactions.html): `selection_point`, `.add_params()`, `.transform_filter()`.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Exercise 6.1: NOVA bar linked to grade mix

    Click each NOVA group on the left. Compare grade distributions on the right.
    """)
    return


@app.cell
def _(GRADES, GRADE_COLORS, NOVA_COLORS, PARQUET_PATH, alt, duckdb, parquet_bind_path):
    _path = parquet_bind_path(PARQUET_PATH)
    _nova_dist = duckdb.sql(
        """
        SELECT cast(nova_group AS integer) AS nova_group, count(*) AS n
        FROM read_parquet($path)
        WHERE nova_group IS NOT NULL
        GROUP BY 1 ORDER BY 1
        """,
        params={"path": _path},
    ).df()
    _grade_by_nova = duckdb.sql(
        """
        SELECT cast(nova_group AS integer) AS nova_group,
               upper(nutriscore_grade) AS grade, count(*) AS n
        FROM read_parquet($path)
        WHERE nova_group IS NOT NULL
          AND lower(nutriscore_grade) IN ('a','b','c','d','e')
        GROUP BY 1, 2
        """,
        params={"path": _path},
    ).df()
    nova_click = alt.selection_point(fields=["nova_group"], empty=False)
    _nova_scale = alt.Scale(
        domain=[1, 2, 3, 4],
        range=[NOVA_COLORS[g] for g in [1, 2, 3, 4]],
    )
    _grade_scale = alt.Scale(
        domain=GRADES,
        range=[GRADE_COLORS[g] for g in GRADES],
    )
    _nova_bars = (
        alt.Chart(_nova_dist, title="Click a NOVA group")
        .mark_bar()
        .encode(
            x=alt.X("nova_group:O", title="NOVA group"),
            y=alt.Y("n:Q", title="Products"),
            color=alt.condition(
                nova_click,
                alt.Color("nova_group:O", scale=_nova_scale, legend=None),
                alt.value("#d0d0d0"),
            ),
            opacity=alt.condition(nova_click, alt.value(1.0), alt.value(0.45)),
        )
        .add_params(nova_click)
        .properties(width=280, height=300)
    )
    _grade_bars = (
        alt.Chart(_grade_by_nova, title="Nutri-Score mix for selected NOVA group")
        .mark_bar()
        .encode(
            x=alt.X("grade:N", sort=GRADES),
            y=alt.Y("n:Q"),
            color=alt.Color("grade:N", sort=GRADES, scale=_grade_scale, legend=None),
        )
        .transform_filter(nova_click)
        .properties(width=320, height=300)
    )
    (_nova_bars | _grade_bars).resolve_scale(color="independent")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Exercise 6.2: Ridge plot by grade

    Done in Section 5 (`RIDGE_NUTRIENT`). Try another nutrient.

    ### Exercise 6.3: Category linked to grade mix (stretch)

    Repeat the three-line pattern from 6.1 with `main_category` (top 12 categories).

    ### Exercise 6.4: Country bar chart

    Build a bar chart of `countries_tags` top 10 for your sample, or compare two countries.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 7. Workshop

    Build one chart that answers a question you care about (category, brand, country, nutrients).

    ### Exercise 7.1: Build 1-5 charts that are different (as time permits)

    Use DuckDB, pandas or polars to aggregate if necessary, then Altair or Seaborn to plot.

    ### Exercise 7.2: Share to team chat

    Post a screenshot, a one-sentence headline (the insight), and the cell you changed.
    Have it graded by the class!

    ### Exercise 7.3: Find a story to tell (if time permits)

    Did you find something interesting in the data?
    Headline + chart + three sentences (context, evidence, caveat).
    And have your chart graded by the class.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Chart scoring sheet

    [Link to form](https://forms.office.com/Pages/ResponsePage.aspx?id=3sTngckmMUWwdrcOLXWWbileOTvFZR5JrLztwF0qkr1UOUZLVFhGV1ZQQ1o3MVpOM1JNMzRaMEVKVC4u)

    **Focus:**
    *Does the chart serve one clear purpose, with no irrelevant elements?*

    | Stars | Description |
    |-------|-------------|
    | ★ | Multiple unrelated messages; heavy visual noise; hard to know what to look at |
    | ★★ | A message exists but is buried; several distracting elements |
    | ★★★ | One message, but some elements could be removed without loss |
    | ★★★★ | Clear purpose; minor unnecessary decoration |
    | ★★★★★ | Every element earns its place; nothing to add, nothing to remove |



    **Clarity:**
    *Does the key insight emerge within 5 seconds, without reading a caption or explanation?*

    | Stars | Description |
    |-------|-------------|
    | ★ | Requires extensive explanation before understanding is possible |
    | ★★ | Message emerges only after careful study |
    | ★★★ | Readable but requires moderate effort; title helps a lot |
    | ★★★★ | Insight is quick but one small barrier remains (legend, scale, etc.) |
    | ★★★★★ | Insight is immediate to someone unfamiliar with the data |



    **Encoding:**
    *Are the right visual channels used for the data types involved?*

    Reference: position > length > angle > area > colour saturation > colour hue.

    | Stars | Description |
    |-------|-------------|
    | ★ | Wrong channel for the data type (e.g. pie for comparison, 3D with no 3D data, dual-axis misused) |
    | ★★ | Suboptimal encoding; a clearly better option was available |
    | ★★★ | Acceptable; could be improved (e.g. colour where position would be clearer) |
    | ★★★★ | Good fit; minor improvement possible |
    | ★★★★★ | Best-fit encoding: quantities on position/length, categories on hue, size used purposefully if at all |

    ---

    **Honesty:**
    *Is the chart truthful? Are scale, context, and data limitations shown fairly?*

    | Stars | Description |
    |-------|-------------|
    | ★ | Actively misleading: truncated axis, cherry-picked range, distorted scale, correlation presented as causal |
    | ★★ | Not intentionally deceptive but omits important caveats (no n shown, outliers hidden) |
    | ★★★ | Honest but incomplete; a key limitation is absent |
    | ★★★★ | Honest and mostly complete; one minor labelling gap |
    | ★★★★★ | Axes start at zero (or deviation is justified); n shown; uncertainty conveyed; no selective framing |



    **Craft:**
    *Is the chart clean, fully labelled, and accessible to a broad audience?*

    | Stars | Description                                                                                                      |
    | ----- | ---------------------------------------------------------------------------------------------------------------- |
    | ★     | Missing title and/or axis labels; illegible text; inaccessible colours                                           |
    | ★★    | Title present but vague ("Figure 1"); units missing; default rainbow palette                                     |
    | ★★★   | Functional; rough around edges (some labels missing, source not cited)                                           |
    | ★★★★  | Well-labelled; readable; minor gap (source missing or font too small at print size)                              |
    | ★★★★★ | Title states the insight; axes carry units; text legible at any size; colourblind-friendly palette; source cited |
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 8. Quiz

    Complete the **Session 3 quiz** on Wooclap (EDA and storytelling).
    """)
    return


if __name__ == "__main__":
    app.run()
