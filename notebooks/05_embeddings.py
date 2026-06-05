import marimo

__generated_with = "0.23.8"
app = marimo.App(width="medium", app_title="Session 5: Embeddings")


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Session 5: Visualizing high-dimensional data

    **Guiding question:** How do you visualize high-dimensional data without fooling yourself, and what do hyperparameters actually change?

    Act 1: Open Food Facts nutrients (tabular features). Act 2: precomputed French Wikipedia text embeddings.

    Session 5 is **embeddings / dimensionality reduction** (not the scale-at-millions session; that comes later). Course plan: [knowledge-vault PR #15](https://github.com/annemariet/knowledge-vault/pull/15).

    ---
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 1. Embedding concepts

    Three dimensionality-reduction algorithms:

    - **PCA** (Principal Component Analysis): linear projection along directions of maximum variance. Axes are interpretable (% variance explained).
    - **t-SNE** (t-distributed Stochastic Neighbour Embedding): non-linear; keeps nearby points close in 2D. **Distances between clusters are not trustworthy.** See [How to Use t-SNE Effectively](https://distill.pub/2016/misread-tsne/) (Wattenberg et al., 2016).
    - **UMAP** (Uniform Manifold Approximation and Projection): non-linear; similar goal to t-SNE but faster. Tune `n_neighbors` (local vs global) and `min_dist` (cluster tightness).

    | Method | Preserves | Good for |
    |--------|-----------|----------|
    | PCA | Global variance | Quick 2D overview, axis labels = % variance |
    | t-SNE | Local neighborhoods | Clusters; **distances not trustworthy** |
    | UMAP | Local + some global | Larger datasets; tune [n_neighbors](https://umap-learn.readthedocs.io/en/latest/parameters.html) |

    **Standardize** = subtract each feature mean and divide by its standard deviation (z-score), so kcal does not dominate grams purely because of scale. Apply before UMAP/t-SNE on tabular nutrients.

    **Rule:** tight blobs in 2D do not prove groups are meaningful. Check original variables. **Always try multiple perplexity / n_neighbors / min_dist values**; if the picture changes radically, the structure was not robust.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 2. Open Food Facts nutrient space

    Same Parquet as Sessions 3-4 (`data/openfoodfacts.parquet`). Download from course SharePoint if missing (see README).

    `.fit_transform(X)` computes mean/std on `X` then scales (workshop sample only). On held-out data, call **only** `.transform()` after fitting on the training set.
    """)
    return


@app.cell
def _():
    import marimo as mo
    import pandas as pd
    import altair as alt
    import numpy as np
    import duckdb
    import matplotlib.pyplot as plt
    from sklearn.preprocessing import StandardScaler
    from sklearn.decomposition import PCA
    from sklearn.manifold import TSNE
    import umap

    from course_data import PARQUET_PATH, resolve_parquet_url

    alt.data_transformers.disable_max_rows()
    PARQUET_URL = resolve_parquet_url()
    FEATURE_COLS = [
        "energy-kcal_100g",
        "fat_100g",
        "saturated-fat_100g",
        "sugars_100g",
        "salt_100g",
        "proteins_100g",
        "fiber_100g",
    ]
    RANDOM_STATE = 42
    COLOR_BY = "grade"  # Exercise 2.2: "grade" or "category"
    return (
        COLOR_BY,
        FEATURE_COLS,
        PARQUET_PATH,
        PARQUET_URL,
        PCA,
        RANDOM_STATE,
        StandardScaler,
        TSNE,
        alt,
        duckdb,
        mo,
        np,
        pd,
        plt,
        umap,
    )


@app.cell
def _(mo):
    umap_neighbors_sel = mo.ui.slider(value=15, start=5,stop=100,step=5, label="Nb neighbors")
    umap_min_dist_sel = mo.ui.number(value=0.1, start=0.0, stop=1.0, step=0.05, label="Min distance")
    mo.vstack([umap_neighbors_sel, umap_min_dist_sel])
    return umap_min_dist_sel, umap_neighbors_sel


@app.cell
def _(umap_min_dist_sel, umap_neighbors_sel):
    UMAP_NEIGHBORS = umap_neighbors_sel.value  # Exercise 2.1: try 5 or 50
    UMAP_MIN_DIST = umap_min_dist_sel.value
    return UMAP_MIN_DIST, UMAP_NEIGHBORS


@app.cell
def _(PARQUET_PATH, PARQUET_URL):
    from course_data import ensure_openfoodfacts_parquet

    ensure_openfoodfacts_parquet(PARQUET_PATH, PARQUET_URL)
    print(f"Using Parquet: {PARQUET_PATH}")
    return


@app.cell
def _(FEATURE_COLS, PARQUET_PATH, duckdb):
    _cols = ", ".join(f'"{c}"' for c in FEATURE_COLS)
    _nulls = " AND ".join(f'"{c}" IS NOT NULL' for c in FEATURE_COLS)
    df_nut = duckdb.sql(f"""
        SELECT {_cols},
               upper(nutriscore_grade) AS grade,
               split_part(categories, ',', 1) AS category
        FROM read_parquet('{PARQUET_PATH.as_posix()}')
        WHERE {_nulls}
          AND lower(nutriscore_grade) IN ('a','b','c','d','e')
        USING SAMPLE 10000 ROWS (reservoir, 42)
    """).df()
    print(f"Embedding sample: {len(df_nut):,} products")
    return (df_nut,)


@app.cell
def _(
    FEATURE_COLS,
    PCA,
    RANDOM_STATE,
    StandardScaler,
    UMAP_MIN_DIST,
    UMAP_NEIGHBORS,
    df_nut,
    umap,
):
    X = df_nut[FEATURE_COLS]
    X_scaled = StandardScaler().fit_transform(X)
    pca = PCA(n_components=2, random_state=RANDOM_STATE)
    xy_pca = pca.fit_transform(X_scaled)
    df_nut["pc1"] = xy_pca[:, 0]
    df_nut["pc2"] = xy_pca[:, 1]
    pc1_var = f"{pca.explained_variance_ratio_[0]:.0%}"
    pc2_var = f"{pca.explained_variance_ratio_[1]:.0%}"

    reducer = umap.UMAP(
        n_neighbors=UMAP_NEIGHBORS,
        min_dist=UMAP_MIN_DIST,
        random_state=RANDOM_STATE,
    )
    xy_umap = reducer.fit_transform(X_scaled)
    df_nut["umap_x"] = xy_umap[:, 0]
    df_nut["umap_y"] = xy_umap[:, 1]
    return X_scaled, pc1_var, pc2_var


@app.cell
def _(COLOR_BY, alt, df_nut, pc1_var, pc2_var):
    _color_field = "grade:N" if COLOR_BY == "grade" else "category:N"
    alt.Chart(df_nut, title=f"PCA of nutrient space (PC1 {pc1_var}, PC2 {pc2_var})").mark_circle(
        size=12, opacity=0.5
    ).encode(
        x=alt.X("pc1:Q", title=f"PC1 ({pc1_var} variance)"),
        y=alt.Y("pc2:Q", title=f"PC2 ({pc2_var} variance)"),
        color=_color_field,
        tooltip=["grade", "category", "sugars_100g", "fat_100g"],
    ).properties(width=520, height=380).interactive()
    return


@app.cell
def _(COLOR_BY, UMAP_NEIGHBORS, alt, df_nut):
    _color_field = "grade:N" if COLOR_BY == "grade" else "category:N"
    alt.Chart(df_nut, title=f"UMAP of nutrient space n={UMAP_NEIGHBORS}").mark_circle(size=12, opacity=0.5).encode(
        x="umap_x:Q",
        y="umap_y:Q",
        color=_color_field,
        tooltip=["grade", "category", "sugars_100g", "fat_100g"],
    ).properties(width=520, height=380).interactive()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### t-SNE: same data, different perplexity

    The gap between grade blobs is **not a real distance**. Re-run with another perplexity and the gap moves. That is what "distances not trustworthy" means in practice ([Distill.pub](https://distill.pub/2016/misread-tsne/)).
    """)
    return


@app.cell
def _(RANDOM_STATE, TSNE, X_scaled, df_nut, pd, plt):
    _perplexities = [5, 30, 100]
    _grades = df_nut["grade"].values
    _codes = pd.Categorical(_grades).codes
    fig_tsne, _axes_tsne = plt.subplots(1, len(_perplexities), figsize=(14, 4))
    for _ax, perp in zip(_axes_tsne, _perplexities):
        _xy = TSNE(
            n_components=2,
            perplexity=perp,
            random_state=RANDOM_STATE,
            init="pca",
            learning_rate="auto",
        ).fit_transform(X_scaled)
        _ax.scatter(_xy[:, 0], _xy[:, 1], c=_codes, alpha=0.35, s=6, cmap="tab10")
        _ax.set_title(f"t-SNE perplexity={perp}")
        _ax.axis("off")
    plt.suptitle("Same 8k products: layout changes with perplexity")
    plt.tight_layout()
    fig_tsne
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Exercise 2.1: Move `UMAP_NEIGHBORS`

    Try 5 vs 50 in setup, re-run UMAP cell.

    ### Exercise 2.2: Switch `COLOR_BY` to `category`

    ### Exercise 2.3: Compare PCA vs UMAP axis meaning

    Which plot has axes you can interpret? Which would you show a non-technical audience?
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 3. Wikipedia FR embeddings

    Teacher-prepared `data/wiki_fr_embeddings_sample.parquet` caches **embedding vectors only** (not built live in class). Regenerate with `teacher_scripts/build_wiki_fr_embeddings_sample.py` (see README).

    - **Default (workshop):** synthetic 32-dim embeddings with five hand-labelled `topic` clusters.
    - **With `--real-embeddings`:** French Wikipedia titles embedded with [`sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2`](https://huggingface.co/sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2) (384-dim). The `topic` column comes from Wikipedia categories (truncated).

    **You compute UMAP here** (same `UMAP_NEIGHBORS` / `UMAP_MIN_DIST` as Section 2) after standardizing the embedding matrix. Proximity in the plot means **similarity in embedding space**, not geographic or causal closeness.
    """)
    return


@app.cell
def _(pd):
    from pathlib import Path

    _wiki_path = Path("data/wiki_fr_embeddings_sample.parquet")
    if not _wiki_path.exists():
        raise FileNotFoundError(
            "Missing data/wiki_fr_embeddings_sample.parquet. Ask instructor or run teacher_scripts/build_wiki_fr_embeddings_sample.py"
        )
    df_wiki = pd.read_parquet(_wiki_path)
    if "embedding" not in df_wiki.columns:
        raise ValueError(
            "wiki_fr_embeddings_sample.parquet must have an 'embedding' column. "
            "Re-run teacher_scripts/build_wiki_fr_embeddings_sample.py"
        )
    return (df_wiki,)


@app.cell
def _(
    RANDOM_STATE,
    StandardScaler,
    UMAP_MIN_DIST,
    UMAP_NEIGHBORS,
    df_wiki,
    np,
    umap,
):
    X_wiki = np.vstack(df_wiki["embedding"].to_numpy())
    X_wiki_scaled = StandardScaler().fit_transform(X_wiki)
    xy_wiki = umap.UMAP(
        n_neighbors=UMAP_NEIGHBORS,
        min_dist=UMAP_MIN_DIST,
        random_state=RANDOM_STATE,
    ).fit_transform(X_wiki_scaled)
    df_wiki["umap_x"] = xy_wiki[:, 0]
    df_wiki["umap_y"] = xy_wiki[:, 1]
    return


@app.cell
def _(UMAP_NEIGHBORS, alt, df_wiki):

    alt.Chart(df_wiki, title=f"Wikipedia FR: UMAP of text embeddings n={UMAP_NEIGHBORS}").mark_circle(size=20, opacity=0.7).encode(
        x="umap_x:Q",
        y="umap_y:Q",
        color="topic:N",
        tooltip=["title", "topic"],
    ).properties(width=560, height=400).interactive()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Exercise 3.1: Filter by topic

    Add `transform_filter` or subset `df_wiki` to one topic.

    ### Exercise 3.2: Find two nearby titles

    Hover neighbors. Do they share a topic or is it a parameter artifact?
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 4. Parameter sensitivity

    Re-run UMAP on a 5k subsample with different `n_neighbors` and `min_dist`. **The danger:** with one setting you can construct whatever story you want. Always compare at least two values before drawing conclusions.
    """)
    return


@app.cell
def _(FEATURE_COLS, RANDOM_STATE, StandardScaler, UMAP_MIN_DIST, df_nut, umap):
    sub = df_nut[FEATURE_COLS].dropna().head(5000)
    _Xs = StandardScaler().fit_transform(sub.to_numpy())
    layouts = {}
    for _k in [5, 50]:
        layouts[_k] = umap.UMAP(
            n_neighbors=_k, min_dist=UMAP_MIN_DIST, random_state=RANDOM_STATE
        ).fit_transform(_Xs)
    min_dist_layouts = {}
    for _md in [0.0, 0.5, 0.99]:
        min_dist_layouts[_md] = umap.UMAP(
            n_neighbors=15, min_dist=_md, random_state=RANDOM_STATE
        ).fit_transform(_Xs)
    return layouts, min_dist_layouts, sub


@app.cell
def _(df_nut, layouts, pd, plt, sub):
    _grades = df_nut.loc[sub.index, "grade"].values
    _codes = pd.Categorical(_grades).codes
    fig_nn, _axes_nn = plt.subplots(1, 2, figsize=(12, 4))
    for _ax, k in zip(_axes_nn, [5, 50]):
        _ax.scatter(
            layouts[k][:, 0],
            layouts[k][:, 1],
            c=_codes,
            alpha=0.3,
            s=6,
            cmap="tab10",
        )
        _ax.set_title(f"UMAP n_neighbors={k}")
        _ax.axis("off")
    plt.suptitle("Same 5k products: local vs global structure")
    plt.tight_layout()
    fig_nn
    return


@app.cell
def _(df_nut, min_dist_layouts, pd, plt, sub):
    _grades = df_nut.loc[sub.index, "grade"].values
    _codes = pd.Categorical(_grades).codes
    fig_md, _axes_md = plt.subplots(1, 3, figsize=(14, 4))
    for _ax, md in zip(_axes_md, [0.0, 0.5, 0.99]):
        _ax.scatter(
            min_dist_layouts[md][:, 0],
            min_dist_layouts[md][:, 1],
            c=_codes,
            alpha=0.3,
            s=6,
            cmap="tab10",
        )
        _ax.set_title(f"UMAP min_dist={md}")
        _ax.axis("off")
    plt.suptitle("Cluster crispness is a parameter choice, not a data property")
    plt.tight_layout()
    fig_md
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    At `n_neighbors=5` you see many small fragments; at `50`, smoother global blobs. Neither is "wrong". At low `min_dist`, clusters look artificially tight; at high `min_dist`, they blur together.

    ### Exercise 4.1: Set `n_neighbors` to 5 vs 50

    ### Exercise 4.2: Write one sentence on what changed in the layout
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 5. Workshop

    ### Exercise 5.1: Explain one surprising neighbor pair on the Wiki plot

    ### Exercise 5.2: Share plot + UMAP parameters to team chat

    ### Exercise 5.3: BYOD (stretch)

    Run UMAP on your own project features.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 6. Quiz

    Complete the **Session 5 quiz** on Wooclap (embeddings).
    """)
    return


if __name__ == "__main__":
    app.run()
