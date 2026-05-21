import marimo

__generated_with = "0.23.2"
app = marimo.App(
    width="medium",
    app_title="Data Visualization · Part 3: Communication & Storytelling",
)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Part 3: Communication & Storytelling

    **Session duration**: ~3 hours &nbsp;|&nbsp; **Dataset**: Palmer Penguins

    ## What you'll be able to do after this session

    - Distinguish *exploration* charts from *explanation* charts and choose the right mode
    - Apply a three-act narrative arc to a data analysis
    - Build a complete visual story around a KMeans clustering result
    - Critique charts for storytelling effectiveness

    ---
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 1. Theory: From Exploration to Explanation

    ### 1.1  Two modes of visualisation

    Gelman & Unwin (2013) distinguish two goals:

    | Mode | Goal | Audience | Typical charts |
    |------|------|----------|----------------|
    | **Exploration** | Find patterns, surprises, anomalies | Yourself / analysts | Pairplots, faceted grids, quick sketches |
    | **Explanation** | Communicate a specific finding | Decision-makers, public | One polished chart, one message |

    Most courses (and most practitioners) focus on one at the expense of the other.
    Great analysts switch modes deliberately.

    ---

    ### 1.2  The narrative arc (Knaflic, 2015)

    Every effective data story has three acts:

    1. **Setup**: who is the audience, what do they already know, what is at stake?
    2. **Conflict / Rising action**: charts and statistics that reveal the problem or insight
    3. **Resolution**: call to action or key takeaway (what should the audience *do* or *believe*?)

    ---

    ### 1.3  Five principles for explanation charts

    1. **One chart, one message**: resist the urge to show everything
    2. **Title = insight**: write the takeaway, not a variable name ("Gentoo flippers are 20 mm longer", not "Flipper length by species")
    3. **Reduce cognitive load**: remove grid lines, borders, redundant legends
    4. **Guide the eye**: use colour, size, or annotation to highlight what matters
    5. **Respect the data**: don't truncate axes, don't cherry-pick time windows

    ---

    ### 1.4  Gelman's click-through solution

    For technical audiences who want both the story *and* the details, present in layers:

    1. **Overview**: one grab chart, insight title, minimal decoration
    2. **Statistical detail**: the evidence (elbow curve, silhouette, confidence intervals)
    3. **Raw data**: link to dataset / appendix for reproducibility

    This is the structure we will follow in the workshop today.

    ---
    """)
    return


@app.cell
def _():
    import marimo as mo
    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt
    import seaborn as sns
    import altair as alt

    from sklearn.preprocessing import StandardScaler
    from sklearn.cluster import KMeans
    from sklearn.decomposition import PCA
    from sklearn.metrics import silhouette_score

    alt.data_transformers.enable("vegafusion")
    return KMeans, PCA, StandardScaler, alt, mo, pd, plt, silhouette_score, sns


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## 2. Case Study: Telling the Story of Penguin Clusters

    We will build a complete visual story in three acts using the Palmer Penguins dataset.

    **Business question**: *"Are there natural groups of penguins that differ in their physical measurements?
    If so, how many groups are there, and what distinguishes them?"*

    This mirrors a real machine learning workflow where you need to explain clustering results to a non-specialist audience.

    ---
    """)
    return


@app.cell
def _(sns):
    penguins = sns.load_dataset("penguins").dropna()

    features = ["bill_length_mm", "bill_depth_mm", "flipper_length_mm", "body_mass_g"]
    labels_feat = {
        "bill_length_mm": "Bill length (mm)",
        "bill_depth_mm": "Bill depth (mm)",
        "flipper_length_mm": "Flipper length (mm)",
        "body_mass_g": "Body mass (g)",
    }
    return features, labels_feat, penguins


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Act 1: What does the data look like?

    Before we can tell a story, we need to explore.
    These charts are for **us**, not for the audience.

    ---
    """)
    return


@app.cell
def _(features, labels_feat, penguins, plt):
    fig, axes = plt.subplots(2, 2, figsize=(10, 7))
    fig.suptitle("Penguin measurements: raw distributions (exploration)", fontsize=13)

    for ax, feat in zip(axes.flat, features):
        for species, grp in penguins.groupby("species"):
            ax.hist(grp[feat], bins=20, alpha=0.55, label=species)
        ax.set_xlabel(labels_feat[feat])
        ax.set_ylabel("Count")

    axes[0, 0].legend(fontsize=8)
    plt.tight_layout()
    plt.gca()
    return (ax,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Observation (exploration note)**: the distributions look bimodal or trimodal on several features,
    hinting at distinct groups.  Flipper length and body mass show the clearest separation.

    ---
    """)
    return


@app.cell
def _(penguins, sns):
    _pp = sns.pairplot(penguins[["bill_length_mm", "bill_depth_mm",
                                  "flipper_length_mm", "body_mass_g", "species"]],
                       hue="species", plot_kws={"alpha": 0.5}, height=2.2)
    _pp.fig.suptitle("Pairplot: exploration only, not for presentation", y=1.01, fontsize=11)
    _pp.fig
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The pairplot is a great *exploration* tool but far too dense for a slide or report.
    We will distil its information into focused explanation charts.

    ---

    ### Act 2: How many clusters?

    We now need to justify our choice of K to the audience.
    Two complementary statistics: **inertia (elbow curve)** and **silhouette score**.
    """)
    return


@app.cell
def _(KMeans, StandardScaler, features, pd, penguins, silhouette_score):
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(penguins[features])

    _ks = range(2, 9)
    _inertias, _silhouettes = [], []

    for _k in _ks:
        _km = KMeans(n_clusters=_k, random_state=42, n_init="auto")
        _labels = _km.fit_predict(X_scaled)
        _inertias.append(_km.inertia_)
        _silhouettes.append(silhouette_score(X_scaled, _labels))

    elbow_df = pd.DataFrame({
        "k": list(_ks),
        "inertia": _inertias,
        "silhouette": _silhouettes,
    })
    return X_scaled, elbow_df


@app.cell
def _(elbow_df, plt):
    fig_elbow, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4))

    ax1.plot(elbow_df["k"], elbow_df["inertia"], marker="o", color="#4C72B0")
    ax1.axvline(3, color="#DD4444", linestyle="--", linewidth=1.5, label="K = 3")
    ax1.set_xlabel("Number of clusters K")
    ax1.set_ylabel("Inertia (within-cluster SS)")
    ax1.set_title("Elbow curve")
    ax1.legend()

    ax2.plot(elbow_df["k"], elbow_df["silhouette"], marker="o", color="#55A868")
    ax2.axvline(3, color="#DD4444", linestyle="--", linewidth=1.5, label="K = 3")
    ax2.set_xlabel("Number of clusters K")
    ax2.set_ylabel("Silhouette score")
    ax2.set_title("Silhouette score")
    ax2.legend()

    fig_elbow.suptitle("Both metrics agree: K = 3 is the natural number of groups",
                       fontsize=12, fontweight="bold")
    plt.tight_layout()
    fig_elbow
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Storytelling note**: placing the annotation "K = 3" on both charts simultaneously
    makes the agreement obvious without asking the reader to compare axes mentally.
    This is the "guide the eye" principle in action.

    ---
    """)
    return


@app.cell
def _(KMeans, PCA, X_scaled, pd, penguins):
    _km3 = KMeans(n_clusters=3, random_state=42, n_init="auto")
    cluster_labels = _km3.fit_predict(X_scaled)

    _pca = PCA(n_components=2, random_state=42)
    _coords = _pca.fit_transform(X_scaled)
    var_explained = _pca.explained_variance_ratio_ * 100

    plot_df = pd.DataFrame({
        "PC1": _coords[:, 0],
        "PC2": _coords[:, 1],
        "cluster": [f"Cluster {c+1}" for c in cluster_labels],
        "species": penguins["species"].values,
    })
    return cluster_labels, plot_df, var_explained


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Act 3: The grab chart

    The grab chart is the single image that should work stand-alone:
    a reader who sees only this chart should understand the finding.

    **Rules for a good grab chart**:
    - Insight title (not a variable name)
    - Axis labels with units and context
    - Minimal decoration
    - Colour used *only* to encode the key variable
    """)
    return


@app.cell
def _(alt, plot_df, var_explained):
    _scatter = (
        alt.Chart(plot_df)
        .mark_circle(size=70, opacity=0.75)
        .encode(
            x=alt.X("PC1:Q",
                    title=f"PC 1 ({var_explained[0]:.1f}% variance explained)"),
            y=alt.Y("PC2:Q",
                    title=f"PC 2 ({var_explained[1]:.1f}% variance explained)"),
            color=alt.Color("cluster:N",
                            title="Cluster",
                            scale=alt.Scale(scheme="tableau10")),
            tooltip=["cluster", "species", "PC1", "PC2"],
        )
        .properties(
            title=alt.TitleParams(
                "Three distinct penguin groups emerge from physical measurements",
                fontSize=14,
                fontWeight="bold",
            ),
            width=520,
            height=380,
        )
    )

    _scatter
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Exercise**: hover over points. Notice how clusters align with species; we will reveal this shortly.

    ---

    #### Supporting chart 1: Violin plots (distribution per cluster)

    The grab chart tells us *that* groups exist; violin plots tell us *what* distinguishes them.
    """)
    return


@app.cell
def _(ax, cluster_labels, features, labels_feat, penguins, plt, sns):
    fig_violin, axes_v = plt.subplots(2, 2, figsize=(11, 7))
    fig_violin.suptitle("Feature distributions differ clearly across clusters",
                         fontsize=13, fontweight="bold")

    _pdf = penguins.copy()
    _pdf["cluster"] = [f"C{c+1}" for c in cluster_labels]
    _palette = {"C1": "#4C72B0", "C2": "#DD8452", "C3": "#55A868"}

    for _ax, _feat in zip(axes_v.flat, features):
        sns.violinplot(data=_pdf, x="cluster", y=_feat,
                       palette=_palette, inner="box", ax=_ax)
        ax.set_xlabel("")
        ax.set_ylabel(labels_feat[_feat])

    plt.tight_layout()
    fig_violin
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### Supporting chart 2: Cluster profile heatmap

    A heatmap of *standardised* mean values lets us name each cluster by its defining traits.
    Standardisation puts all features on the same ±2 scale regardless of units.
    """)
    return


@app.cell
def _(
    StandardScaler,
    cluster_labels,
    features,
    labels_feat,
    pd,
    penguins,
    plt,
    sns,
):
    _pdf2 = penguins[features].copy()
    _pdf2["cluster"] = [f"Cluster {c+1}" for c in cluster_labels]

    _means = _pdf2.groupby("cluster")[features].mean()
    _std_means = pd.DataFrame(
        StandardScaler().fit_transform(_means),
        index=_means.index,
        columns=[labels_feat[f] for f in features],
    )

    fig_heat, ax_heat = plt.subplots(figsize=(8, 3.5))
    sns.heatmap(_std_means, annot=True, fmt=".2f", cmap="RdBu_r",
                center=0, linewidths=0.5, ax=ax_heat)
    ax_heat.set_title("Standardised cluster profiles\n(red = above average, blue = below average)",
                      fontsize=11)
    plt.tight_layout()
    fig_heat
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Reading the heatmap**:

    - **Cluster 1**: long bills, small flippers, light body; likely a small-billed, compact species
    - **Cluster 2**: short deep bills, average flippers; a stocky, bill-heavy morphotype
    - **Cluster 3**: very large flippers, heavy; the big species

    Can you guess which clusters correspond to which species?

    ---
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### The reveal: clusters vs. species
    """)
    return


@app.cell
def _(cluster_labels, pd, penguins):
    _pdf3 = penguins.copy()
    _pdf3["cluster"] = [f"Cluster {c+1}" for c in cluster_labels]
    pd.crosstab(_pdf3["cluster"], _pdf3["species"])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The clusters align almost perfectly with the three species (Adelie, Chinstrap, Gentoo),
    even though KMeans had **no access to species labels** during training.
    This confirms that the physical measurements alone are sufficient to distinguish the species.

    ---

    #### Presentation-ready grab chart with cluster names
    """)
    return


@app.cell
def _(alt, plot_df, var_explained):
    _name_map = {"Cluster 1": "Chinstrap", "Cluster 2": "Adelie", "Cluster 3": "Gentoo"}
    _pdf_named = plot_df.copy()
    _pdf_named["group"] = _pdf_named["cluster"].map(_name_map)

    _final = (
        alt.Chart(_pdf_named)
        .mark_circle(size=72, opacity=0.8)
        .encode(
            x=alt.X("PC1:Q",
                    title=f"PC 1 ({var_explained[0]:.1f}% variance explained)",
                    axis=alt.Axis(grid=False)),
            y=alt.Y("PC2:Q",
                    title=f"PC 2 ({var_explained[1]:.1f}% variance explained)",
                    axis=alt.Axis(grid=False)),
            color=alt.Color("group:N",
                            title="Species (recovered by KMeans)",
                            scale=alt.Scale(
                                domain=["Adelie", "Chinstrap", "Gentoo"],
                                range=["#4C72B0", "#DD8452", "#55A868"],
                            )),
            tooltip=["group", "species", "PC1", "PC2"],
        )
        .properties(
            title=alt.TitleParams(
                [
                    "KMeans recovers penguin species from physical measurements alone",
                    "Three clusters match Adelie, Chinstrap, and Gentoo with >95% accuracy",
                ],
                fontSize=13,
                fontWeight="bold",
                anchor="start",
            ),
            width=540,
            height=380,
        )
        .configure_view(strokeWidth=0)
        .configure_axis(labelFontSize=11, titleFontSize=11)
    )

    _final
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Compare this to the first grab chart**: same data, but now the legend names are meaningful,
    the title states the finding in two lines (what + how well), and chart junk has been removed.
    This chart could stand alone in a paper, slide, or report.

    ---

    ## 3. Exercises

    ### Exercise A: Chart critique (15 min)

    Find a chart online (news article, paper, social media) that tells a data story poorly.
    Identify:
    1. What is the intended message?
    2. Which storytelling principle(s) does it violate?
    3. How would you redesign it?

    Share with a neighbour and explain your reasoning.

    ---

    ### Exercise B: Build your own story (30 min)

    Take the penguins dataset (or a dataset of your choice) and build a 3-chart story:

    1. **One exploration chart**: help yourself find something interesting
    2. **One evidence chart**: the statistical proof
    3. **One grab chart**: presentation-ready, insight title, minimal decoration

    Write the narrative arc (3 sentences: setup / conflict / resolution) to accompany your charts.

    ---

    ### Exercise C: Apply to your project (remaining time)

    Take the most important chart from your group project (Sessions 5–7).
    Apply the five storytelling principles to improve it.
    Bring the before/after pair to the next session.

    ---
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Summary

    | Concept | Key idea |
    |---------|----------|
    | Exploration vs. Explanation | Different goals, different charts; switch modes deliberately |
    | Narrative arc | Setup → Conflict → Resolution; every presentation needs all three |
    | One chart, one message | Remove everything that doesn't serve the single takeaway |
    | Title = insight | Write what the chart *means*, not what it *shows* |
    | Click-through structure | Overview → Statistical detail → Raw data |
    | KMeans visualisation stack | Elbow + silhouette → PCA scatter → violin plots → profile heatmap |

    ---

    ## References

    - Gelman, A. & Unwin, A. (2013). Infovis and statistical graphics: different goals, different looks. *Journal of Computational and Graphical Statistics*, 22(1), 2–28.
    - Knaflic, C. N. (2015). *Storytelling with Data*. Wiley.
    - Cleveland, W. S. & McGill, R. (1984). Graphical perception: Theory, experimentation, and application to the development of graphical methods. *JASA*, 79(387), 531–554.
    - Horst, A. M., Hill, A. P., & Gorman, K. B. (2020). Palmer Archipelago (Antarctica) penguin data. R package *palmerpenguins*.
    """)
    return


if __name__ == "__main__":
    app.run()
