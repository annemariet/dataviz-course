import marimo

__generated_with = "0.23.8"
app = marimo.App(
    width="medium",
    app_title="Session 4: ML visualization (Open Food Facts)",
)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Session 4: Visualization × machine learning

    **Guiding question:** How can you use data visualization to improve your understanding of the learning process?

    Same nutrient features, two targets (classification vs regression use different diagnostic charts): **grade** (A-E, classification) and **nutriscore_score** (numeric, regression).

    Track experiments with [MLflow](https://mlflow.org/docs/latest/mlflow/tracking/quickstart/) from Section 3 onward (UI: Section 2).

    ---
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 1. ML visualization concepts

    | Stage | Question | Typical chart |
    |-------|----------|---------------|
    | Training | Is the model learning? Train vs validation | Learning curve ([HF LLM ch3/5](https://huggingface.co/learn/llm-course/en/chapter3/5): eval loss vs steps; Section 4: tabular accuracy/RMSE vs size or round) |
    | Classification | Which NUTRISCORES get confused? | Confusion matrix |
    | Classification | Are predicted frequencies realistic? | Calibration |
    | Regression | How far off are predictions? | Predicted vs actual, residuals |
    | Interpretation | Which features push predictions? | SHAP beeswarm |

    **MLflow** logs parameters, metrics, and figure [artifacts](https://mlflow.org/docs/latest/mlflow/tracking.html#logging-artifacts) per training run so you can compare later.

    ### Tools in this notebook

    | Tool | Role |
    |------|------|
    | **MLflow** | Run tracking: params, metrics over time, figure artifacts, compare runs in `mlflow ui` (Sections 2-8) |
    | **Skore** | Model-centric CV reports and estimator comparison (`CrossValidationReport`, `compare`); local `.skore-workspace/` (Section 5b) |
    | **skrub** | Not used here. Elsewhere: tabular preprocessing and sklearn-style pipelines on messy columns. |
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 2. MLflow quick start

    **MLflow** logs each training run: hyperparameters (e.g. `max_depth`), metrics (accuracy, RMSE), and figure files from `mlflow.log_figure`. Compare runs in the UI instead of scrolling old cell output.

    - **This notebook uses:** `sqlite:///mlruns.db` (Section 3 setup) → `mlruns.db` at the **repository root** when you run marimo from the repo root.
    - **Alternative (MLflow default):** omit `set_tracking_uri` → logs under `./mlruns/`; `uv run mlflow ui` or `--backend-store-uri file:./mlruns`.
    - **Reset workshop:** delete `mlruns.db` (this notebook) or `./mlruns/` (if using the default).
    - **MLflow UI for this notebook** (after at least one training run in Section 5+):

    ```bash
    uv run mlflow ui --backend-store-uri sqlite:///mlruns.db --host 127.0.0.1 --port 5000
    ```

    Open http://127.0.0.1:5000 (`--port 5001` if 5000 is busy). Stop with `Ctrl+C` in that terminal only; do not restart the marimo kernel. Do **not** run `mlflow ui` inside a marimo cell.

    **Terminal 1 (notebook):** from the repository root:

    ```bash
    uv sync
    uv run marimo edit notebooks/04_ml_viz_open_food_facts.py
    ```

    ### Best practices

    - **One experiment per dataset:** `off-nutriscore` for all runs; separate tasks with `run_name` and tags.
    - **Three log types:** params (fixed choices), metrics (numbers or curves via `step=`), artifacts (PNG from `log_figure`).

    Docs: [Tracking](https://mlflow.org/docs/latest/ml/tracking/), [Tracking UI](https://mlflow.org/docs/latest/ml/tracking/mlflow-tracking-ui.html).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 3. Setup

    Same Parquet as Session 3 (`data/openfoodfacts.parquet`, SharePoint manual download or `PARQUET_URL`).

    Predicate-pushdown sample: only rows with complete nutrients and valid grade/score.

    **Target `nutriscore_score`:** OFF numeric Nutri-Score is roughly **−15 to 55** (not 0–100); higher = worse nutrition. It correlates strongly with letter grade; regression can fit quickly (high capacity), so learning curves use mild regularization in Section 4b.

    MLflow tracking is configured in the code cell below (see Section 2 for the UI).
    """)
    return


@app.cell
def _():
    import marimo as mo
    import pandas as pd
    import numpy as np
    import altair as alt
    import matplotlib.pyplot as plt
    import seaborn as sns
    import duckdb
    import mlflow
    from sklearn.model_selection import train_test_split
    from sklearn.preprocessing import LabelEncoder
    from xgboost import XGBClassifier, XGBRegressor
    sns.set_theme(style="whitegrid")
    alt.data_transformers.disable_max_rows()
    from course_data import PARQUET_PATH, resolve_parquet_url
    PARQUET_URL = resolve_parquet_url()
    SAMPLE_N = 200_000
    MAX_DEPTH = 4  # Exercises 3.1 / 5.1: try 2 or 8
    USE_SKORE_HUB = True  # Teachers: True, then re-run §5b login + Skore cells
    SKORE_HUB_WORKSPACE = "amarie"  # Hub slug: workspace/name
    FEATURE_COLS = [
        "energy-kcal_100g",
        "fat_100g",
        "saturated-fat_100g",
        "sugars_100g",
        "salt_100g",
        "proteins_100g",
    ]
    NUTRISCORES = ["A", "B", "C", "D", "E"]
    NUM_CLASSES = len(NUTRISCORES)
    grade_encoder = LabelEncoder()
    grade_encoder.fit(NUTRISCORES)
    XGB_CLF_KWARGS = {
        "objective": "multi:softprob",
        "num_class": NUM_CLASSES,
        "eval_metric": "mlogloss",
        "tree_method": "hist",
    }
    mlflow.set_tracking_uri("sqlite:///mlruns.db")
    mlflow.set_experiment("off-nutriscore")
    mlflow.xgboost.autolog(log_models=False)
    return (
        FEATURE_COLS,
        MAX_DEPTH,
        NUTRISCORES,
        PARQUET_PATH,
        PARQUET_URL,
        SAMPLE_N,
        SKORE_HUB_WORKSPACE,
        USE_SKORE_HUB,
        XGBClassifier,
        XGBRegressor,
        XGB_CLF_KWARGS,
        alt,
        duckdb,
        grade_encoder,
        mlflow,
        mo,
        np,
        pd,
        plt,
        sns,
        train_test_split,
    )


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Exercise 3.1: Change `SAMPLE_N`

    Re-run the data load after editing the setup cell.

    ### Exercise 3.2: Drop one nutrient column

    Remove one entry from `FEATURE_COLS`, re-run load and Section 5. Compare accuracy.
    """)
    return


@app.cell
def _(PARQUET_PATH, PARQUET_URL):
    from course_data import ensure_openfoodfacts_parquet
    ensure_openfoodfacts_parquet(PARQUET_PATH, PARQUET_URL)
    print(f"Using Parquet: {PARQUET_PATH}")
    return


@app.cell
def _(FEATURE_COLS, PARQUET_PATH, SAMPLE_N, duckdb):
    _cols = ", ".join(f'"{c}"' for c in FEATURE_COLS)
    _nulls = " AND ".join(f'"{c}" IS NOT NULL' for c in FEATURE_COLS)
    df_model = duckdb.sql(f"""
        SELECT {_cols},
               upper(nutriscore_grade) AS nutriscore_grade,
               nutriscore_score
        FROM read_parquet('{PARQUET_PATH.as_posix()}')
        WHERE {_nulls}
          AND lower(nutriscore_grade) IN ('a','b','c','d','e')
          AND nutriscore_score IS NOT NULL
        USING SAMPLE {SAMPLE_N} ROWS (reservoir, 42)
    """).df()
    print(f"Modeling sample: {len(df_model):,} rows")
    return (df_model,)


@app.cell
def _(FEATURE_COLS, df_model, grade_encoder, train_test_split):
    train_df, test_df = train_test_split(
        df_model,
        test_size=0.2,
        random_state=0,
        stratify=df_model["nutriscore_grade"],
    )
    X_train = train_df[FEATURE_COLS]
    X_test = test_df[FEATURE_COLS]
    y_train_g = train_df["nutriscore_grade"].to_numpy(dtype=object)
    y_test_g = test_df["nutriscore_grade"].to_numpy(dtype=object)
    y_train_clf = grade_encoder.transform(y_train_g)
    y_test_clf = grade_encoder.transform(y_test_g)
    y_train_s = train_df["nutriscore_score"].to_numpy(dtype=float)
    y_test_s = test_df["nutriscore_score"].to_numpy(dtype=float)
    return (
        X_test,
        X_train,
        y_test_clf,
        y_test_g,
        y_test_s,
        y_train_clf,
        y_train_s,
    )


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 4. Learning curves

    **Parallel reading:** [Hugging Face LLM course, ch3 §5 — Understanding learning curves](https://huggingface.co/learn/llm-course/en/chapter3/5) plots **train and eval loss** over fine-tuning steps (often in Weights & Biases). Here we use **sklearn and XGBoost** on Nutri-Score tabular data: same ideas (train vs validation, overfitting gap, underfitting when both stay high), different x-axes (training set size or boosting round).

    **Two questions:** Would more labeled data help? Does the model keep improving as you add trees?

    **Three ways to log them in MLflow** (run the cells below):

    | Approach | X-axis | MLflow pattern |
    |----------|--------|----------------|
    | sklearn `LearningCurveDisplay` | Training set size | One parent run + figure artifact; **disable autolog** inside CV (many fits) |
    | XGBoost `eval_set` / `evals_result` | Boosting round | One run per task; `log_metric(..., step=round)` per iteration |
    | Manual size loop | Training rows | `log_metric` history only (lightweight third option) |

    Autolog is enabled globally for Sections 5-7, but **turned off** inside learning-curve loops (`mlflow.autolog(disable=True)` and `mlflow.xgboost.autolog(disable=True)`) so subset fits do not spawn extra runs or duplicate eval_set metric names (Section 2, 4b).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 4a. Score vs training set size
    """)
    return


@app.cell
def _(mo):
    max_depth_sel = mo.ui.number(start=1, step=1,stop=8, value=4, label="Maximum depth")
    nb_estimators_sel = mo.ui.number(start=10, step=10, stop=100, value=50, label="Nb estimators")
    mo.vstack([max_depth_sel, nb_estimators_sel])
    return max_depth_sel, nb_estimators_sel


@app.cell
def _(max_depth_sel, nb_estimators_sel):
    max_depth = max_depth_sel.value
    nb_estimators = nb_estimators_sel.value
    return max_depth, nb_estimators


@app.cell(hide_code=True)
def _(
    FEATURE_COLS,
    XGBClassifier,
    XGBRegressor,
    XGB_CLF_KWARGS,
    df_model,
    grade_encoder,
    max_depth,
    mlflow,
    nb_estimators,
    np,
    plt,
):
    from sklearn.model_selection import LearningCurveDisplay
    _X = df_model[FEATURE_COLS].to_numpy()
    _yg = grade_encoder.transform(df_model["nutriscore_grade"].to_numpy(dtype=object))
    _ys = df_model["nutriscore_score"].to_numpy(dtype=float)
    _clf_est = XGBClassifier(
        max_depth=max_depth, n_estimators=nb_estimators, random_state=0, **XGB_CLF_KWARGS
    )
    _reg_est = XGBRegressor(max_depth=max_depth, n_estimators=nb_estimators, random_state=0)
    mlflow.autolog(disable=True)
    mlflow.xgboost.autolog(disable=True)
    try:
        # One parent run for both panels; name shows up in the runs table
        with mlflow.start_run(run_name="learning-curve-size"):
            # Tag filters in UI Compare view; approach distinguishes 4a vs 4c
            mlflow.set_tag("approach", "sklearn-learning-curve-display")
            fig_lc_size, _lc_axes = plt.subplots(1, 2, figsize=(11, 4))
            LearningCurveDisplay.from_estimator(
                _clf_est,
                _X,
                _yg,
                ax=_lc_axes[0],
                train_sizes=np.linspace(0.1, 1.0, 5),
            )
            _lc_axes[0].set_title("Classification: accuracy vs training size")
            LearningCurveDisplay.from_estimator(
                _reg_est,
                _X,
                _ys,
                scoring="neg_root_mean_squared_error",
                ax=_lc_axes[1],
                train_sizes=np.linspace(0.1, 1.0, 5),
            )
            _lc_axes[1].set_title("Regression: RMSE vs training size")
            plt.tight_layout()
            # Artifact path in Artifacts tab; PNG survives kernel restarts unlike cell output
            mlflow.log_figure(fig_lc_size, "learning_curve_vs_size.png")
    finally:
        # Re-enable autolog for Sections 5-7 (one baseline fit per run)
        mlflow.xgboost.autolog(log_models=False)
    fig_lc_size
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 4b. Metric vs boosting round (train vs validation)

    One fixed train/validation split; each round adds another tree. Gap between curves = overfitting signal (HF ch3/5: training loss still falls while **eval loss** rises).

    **Healthy vs pathological:** on round 1, train and validation should be close (same scale, similar RMSE or mlogloss). A small gap that **widens** after ~10-20 rounds means the model is memorizing the training set. If validation is **worse than train from round 1** by a large margin, check data (aligned `X`/`y`?) or metric mapping (`validation_0` = first `eval_set` entry = train here). **Underfitting:** both curves stay high and flat early; try more capacity or features before adding rounds.

    **Early stopping:** `early_stopping_rounds` mirrors HF `EarlyStoppingCallback` on eval loss: stop when validation stops improving.

    **MLflow:** the code cell logs `train_*` and `validation_*` metrics with `step=` = boosting round. Autolog is off during `fit` so XGBoost does not also write `validation_0-*` names on the same run (see inline comments).
    """)
    return


@app.cell
def _(
    XGBClassifier,
    XGBRegressor,
    XGB_CLF_KWARGS,
    X_test,
    X_train,
    alt,
    max_depth,
    mlflow,
    nb_estimators,
    pd,
    y_test_clf,
    y_test_s,
    y_train_clf,
    y_train_s,
):
    _n_rounds = nb_estimators
    _early_stop = 12
    mlflow.autolog(disable=True)
    mlflow.xgboost.autolog(disable=True)
    def _eval_long(hist: dict, task: str, metric: str) -> pd.DataFrame:
        rows = []
        for split_name, key in (("train", "validation_0"), ("validation", "validation_1")):
            for rnd, value in enumerate(hist[key][metric], start=1):
                rows.append(
                    {
                        "round": rnd,
                        "split": split_name,
                        "metric_value": value,
                        "task": task,
                        "metric": metric,
                    }
                )
        return pd.DataFrame(rows)
    chart_lc_iter = None
    try:
        with mlflow.start_run(run_name="learning-curve-iterations-clf"):
            # task tag lets you filter classification vs regression in UI
            mlflow.set_tag("task", "classification")
            mlflow.set_tag("approach", "xgboost-eval-set")
            _clf_iter = XGBClassifier(
                max_depth=max_depth,
                n_estimators=_n_rounds,
                early_stopping_rounds=_early_stop,
                random_state=0,
                **XGB_CLF_KWARGS,
            )
            _clf_iter.fit(
                X_train,
                y_train_clf,
                eval_set=[(X_train, y_train_clf), (X_test, y_test_clf)],
                verbose=False,
            )
            _clf_hist = _clf_iter.evals_result()
            for rnd, value in enumerate(_clf_hist["validation_0"]["mlogloss"], start=1):
                # step= builds a metric curve in the UI (x-axis = boosting round)
                mlflow.log_metric("train_mlogloss", value, step=rnd)
            for rnd, value in enumerate(_clf_hist["validation_1"]["mlogloss"], start=1):
                mlflow.log_metric("validation_mlogloss", value, step=rnd)

        with mlflow.start_run(run_name="learning-curve-iterations-reg"):
            # Separate run from clf: different task tag and metric names
            mlflow.set_tag("task", "regression")
            mlflow.set_tag("approach", "xgboost-eval-set")
            _reg_iter = XGBRegressor(
                max_depth=max_depth,
                n_estimators=_n_rounds,
                early_stopping_rounds=_early_stop,
                subsample=0.8,
                reg_lambda=1.0,
                random_state=0,
                eval_metric="rmse",
            )
            _reg_iter.fit(
                X_train,
                y_train_s,
                eval_set=[(X_train, y_train_s), (X_test, y_test_s)],
                verbose=False,
            )
            _reg_hist = _reg_iter.evals_result()
            for rnd, value in enumerate(_reg_hist["validation_0"]["rmse"], start=1):
                mlflow.log_metric("train_rmse", value, step=rnd)
            for rnd, value in enumerate(_reg_hist["validation_1"]["rmse"], start=1):
                mlflow.log_metric("validation_rmse", value, step=rnd)

        _lc_iter = pd.concat(
            [
                _eval_long(_clf_hist, "classification", "mlogloss"),
                _eval_long(_reg_hist, "regression", "rmse"),
            ],
            ignore_index=True,
        )

        chart_lc_iter = (
            alt.Chart(_lc_iter,width=260, height=140)
            .mark_line()
            .encode(
                x=alt.X("round:Q", title="Boosting round"),
                y=alt.Y("metric_value:Q", title="Metric"),
                color=alt.Color("split:N", title="Split"),
                strokeDash=alt.StrokeDash("split:N"),
            )
            .facet(column=alt.Column("task:N", title=None))
            .properties( title="Learning curve vs boosting round")
            .resolve_scale(y="independent")
        )
    finally:
        mlflow.xgboost.autolog(log_models=False)
    chart_lc_iter
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 4c. Manual loop (MLflow metric history)

    Same question as 4a (more data?), but you choose sample sizes and log one validation metric per step. No sklearn display, no XGBoost `evals_result` chart.
    """)
    return


@app.cell
def _(
    FEATURE_COLS,
    MAX_DEPTH,
    XGBClassifier,
    XGB_CLF_KWARGS,
    alt,
    df_model,
    grade_encoder,
    mlflow,
    mo,
    np,
    pd,
    train_test_split,
):
    _X = df_model[FEATURE_COLS].to_numpy()
    _y = grade_encoder.transform(df_model["nutriscore_grade"].to_numpy(dtype=object))
    _Xt, _Xv, _yt, _yv = train_test_split(
        _X, _y, test_size=0.2, random_state=0, stratify=_y
    )
    _manual_rows = []
    mlflow.autolog(disable=True)
    mlflow.xgboost.autolog(disable=True)
    try:
        with mlflow.start_run(run_name="learning-curve-size-manual"):
            mlflow.set_tag("task", "classification")
            mlflow.set_tag("approach", "manual-size-loop")
            for frac in np.linspace(0.1, 1.0, 5):
                _n = max(int(frac * len(_Xt)), 50)
                _clf = XGBClassifier(
                    max_depth=MAX_DEPTH,
                    n_estimators=50,
                    random_state=0,
                    **XGB_CLF_KWARGS,
                )
                _clf.fit(_Xt[:_n], _yt[:_n])
                _train_acc = float(_clf.score(_Xt[:_n], _yt[:_n]))
                _val_acc = float(_clf.score(_Xv, _yv))
                # step= training rows (not fraction) so UI x-axis matches sample size
                mlflow.log_metric("train_accuracy", _train_acc, step=_n)
                mlflow.log_metric("validation_accuracy", _val_acc, step=_n)
                _manual_rows.append(
                    {
                        "train_rows": _n,
                        "train_accuracy": _train_acc,
                        "validation_accuracy": _val_acc,
                    }
                )
    finally:
        mlflow.xgboost.autolog(log_models=False)
    _manual_lc_long = pd.DataFrame(_manual_rows).melt(
        id_vars=["train_rows"],
        value_vars=["train_accuracy", "validation_accuracy"],
        var_name="split",
        value_name="accuracy",
    )
    _manual_lc_long["split"] = _manual_lc_long["split"].str.replace("_accuracy", "")
    chart_manual_lc = (
        alt.Chart(_manual_lc_long)
        .mark_line(point=True)
        .encode(
            x=alt.X("train_rows:Q", title="Training rows"),
            y=alt.Y("accuracy:Q", title="Accuracy"),
            color=alt.Color("split:N", title="Split"),
            strokeDash=alt.StrokeDash("split:N"),
        )
        .properties(
            width=420,
            height=260,
            title="Manual learning curve: train vs validation",
        )
    )
    chart_manual_lc
    _manual_lc_table = mo.ui.table(_manual_rows)
    _manual_lc_table
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 4d. Interactive learning curves

    Inspired by the [sklearn learning curve example](https://scikit-learn.org/stable/auto_examples/model_selection/plot_learning_curve.html). Vocabulary matches [HF ch3/5](https://huggingface.co/learn/llm-course/en/chapter3/5) (loss/accuracy vs steps there; accuracy vs training size here).

    Use the sliders to explore three teaching stories on **Nutri-Score grade**:

    | Story | Slider starting point | What to look for | HF ch3/5 label |
    |-------|----------------------|------------------|----------------|
    | **Overfitting** | `max_depth=8`, 6 features | Train accuracy high, cross-val gap wide; more data helps validation | Train improves, eval lags or worsens |
    | **Underfitting** | `max_depth=2`, 2 features | **Both** curves modest and flat; more data barely helps | Train and eval both stay high |
    | **Contrast** | Compare low depth + few columns vs high depth + more rows | Feature capacity vs labeled data | Capacity vs data (tabular knobs) |

    No MLflow logging in this cell: `learning_curve` runs many inner fits; each slider move would spam the runs table (see Section 4 intro).
    """)
    return


@app.cell
def _(FEATURE_COLS, mo):
    lc_depth = mo.ui.slider(2, 8, value=8, step=2, label="max_depth")
    lc_n_feats = mo.ui.slider(2, len(FEATURE_COLS), value=6, step=1, label="Feature columns")
    lc_train_max = mo.ui.slider(0.4, 1.0, value=1.0, step=0.1, label="Max train fraction")
    mo.vstack([
        mo.hstack([lc_depth, lc_n_feats, lc_train_max]),
        mo.md(
            "Try **depth=8 + 6 features** (overfit: train high, cross-val gap), "
            "**depth=2 + 2 features** (underfit: both curves flat/modest), "
            "then contrast adding columns at low depth vs adding data at high depth."
        ),
    ])
    return lc_depth, lc_n_feats, lc_train_max


@app.cell
def _(
    FEATURE_COLS,
    XGBClassifier,
    XGB_CLF_KWARGS,
    df_model,
    grade_encoder,
    lc_depth,
    lc_n_feats,
    lc_train_max,
    mlflow,
    mo,
    np,
    plt,
):
    from sklearn.model_selection import learning_curve
    _depth = lc_depth.value
    _n_feats = int(lc_n_feats.value)
    _train_max = float(lc_train_max.value)
    _feat_subset = FEATURE_COLS[:_n_feats]
    _X_lc = df_model[_feat_subset].to_numpy()
    _y_lc = grade_encoder.transform(df_model["nutriscore_grade"].to_numpy(dtype=object))
    mlflow.autolog(disable=True)
    mlflow.xgboost.autolog(disable=True)
    try:
        _clf_lc = XGBClassifier(
            max_depth=_depth,
            n_estimators=50,
            random_state=0,
            **XGB_CLF_KWARGS,
        )
        _train_sizes_abs, _train_scores, _val_scores = learning_curve(
            _clf_lc,
            _X_lc,
            _y_lc,
            train_sizes=np.linspace(0.1, _train_max, 5),
            cv=3,
            scoring="accuracy",
            n_jobs=-1,
        )
        _train_mean = _train_scores.mean(axis=1)
        _val_mean = _val_scores.mean(axis=1)

        fig_lc_inter, _ax_lc = plt.subplots(figsize=(7, 4.5))
        _ax_lc.plot(_train_sizes_abs, _train_mean, marker="o", label="Train")
        _ax_lc.plot(_train_sizes_abs, _val_mean, marker="o", label="Cross-val")
        _ax_lc.set_xlabel("Training set size")
        _ax_lc.set_ylabel("Accuracy")
        _ax_lc.set_title(
            f"Nutri-Score grade (depth={_depth}, {len(_feat_subset)} features, max frac={_train_max:.0%})"
        )
        _ax_lc.legend(loc="lower right")
        _ax_lc.set_ylim(0, 1.05)
        plt.tight_layout()
    finally:
        mlflow.xgboost.autolog(log_models=False)
    if _depth >= 6 and _n_feats >= 5:
        _story = "**Overfitting (HF: diverging curves):** train stays high while cross-val lags. More labeled data should lift the cross-val curve."
    elif _depth <= 3 and _n_feats <= 3:
        _story = "**Underfitting (HF: both curves high/flat):** train and cross-val stay modest. More data alone will not fix low capacity or missing nutrients."
    else:
        _story = "**Contrast:** try depth=2 with 2 features (underfit) vs depth=8 with 6 features (overfit, data helps)."
    mo.vstack([mo.md(_story), fig_lc_inter])
    return


@app.cell
def _(
    FEATURE_COLS,
    MAX_DEPTH,
    XGBClassifier,
    XGB_CLF_KWARGS,
    df_model,
    grade_encoder,
    mlflow,
    train_test_split,
):
    _extra = "fiber_100g"
    if _extra in df_model.columns:
        # Optional run: compare to grade-baseline via accuracy in UI
        with mlflow.start_run(run_name="grade-with-fiber"):
            mlflow.set_tag("task", "classification")
            _feats = FEATURE_COLS + [_extra]
            _mask = df_model[_feats].notna().all(axis=1)
            _Xm = df_model.loc[_mask, _feats].to_numpy()
            _ym = grade_encoder.transform(
                df_model.loc[_mask, "nutriscore_grade"].to_numpy(dtype=object)
            )
            _Xt, _Xv, _yt, _yv = train_test_split(
                _Xm, _ym, test_size=0.2, random_state=0, stratify=_ym
            )
            _c = XGBClassifier(
                max_depth=MAX_DEPTH, n_estimators=80, random_state=0, **XGB_CLF_KWARGS
            )
            _c.fit(_Xt, _yt)
            # Metric = measured outcome; param = fixed experimental choice (filter in UI)
            mlflow.log_metric("accuracy", _c.score(_Xv, _yv))
            mlflow.log_param("with_fiber", True)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Exercise 4.1: Which task gains more from more training data?

    Compare the Section 4a panels (score vs training size).

    ### Exercise 4.2: Where would you stop boosting?

    On Section 4b, at which round does validation stop improving for classification? For regression?

    ### Exercise 4.3: Fiber feature

    If `grade-with-fiber` was logged, open MLflow UI (Section 2) and compare accuracy to the baseline run.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 5. Classification: grade

    Section 4 and [HF ch3/5](https://huggingface.co/learn/llm-course/en/chapter3/5) diagnose **fit** (train vs validation curves). This section diagnoses **probability honesty** once the model predicts.

    [Calibration](https://scikit-learn.org/stable/modules/calibration.html): high accuracy does not mean predicted probabilities match reality.

    A **reliability diagram** plots the fraction of positives against mean predicted probability in bins. A well-calibrated model lies on the diagonal. With five grades we use **one-vs-rest** (OvR): grade **E** is the positive class, all others negative, following the [sklearn calibration curve example](https://scikit-learn.org/stable/auto_examples/calibration/plot_calibration_curve.html).

    See also this nice [introduction to reliability diagrams](https://medium.com/data-science/introduction-to-reliability-diagrams-for-probability-calibration-ed785b3f5d44) taking weather forecast as an example.

    The code cell fits **XGBoost**, **logistic regression**, and **random forest** on the same train/test split and overlays their grade-E calibration curves.
    """)
    return


@app.cell
def _(
    MAX_DEPTH,
    NUTRISCORES,
    XGBClassifier,
    XGB_CLF_KWARGS,
    X_test,
    X_train,
    grade_encoder,
    mlflow,
    mo,
    pd,
    plt,
    sns,
    y_test_clf,
    y_test_g,
    y_train_clf,
):
    from sklearn.calibration import calibration_curve
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.linear_model import LogisticRegression
    from sklearn.metrics import confusion_matrix
    from sklearn.pipeline import Pipeline
    from sklearn.preprocessing import StandardScaler
    _grade_e = int(grade_encoder.transform(["E"])[0])
    with mlflow.start_run(run_name="grade-baseline"):
        mlflow.set_tag("task", "classification")
        clf = XGBClassifier(
            max_depth=MAX_DEPTH,
            n_estimators=100,
            random_state=0,
            **XGB_CLF_KWARGS,
        )
        clf.fit(X_train, y_train_clf)
        acc = clf.score(X_test, y_test_clf)
        mlflow.log_metric("accuracy", acc)
        print(f"Test accuracy (XGBoost): {acc:.2%}")

        y_pred = grade_encoder.inverse_transform(clf.predict(X_test).astype(int))
        cm_arr = confusion_matrix(y_test_g, y_pred, labels=NUTRISCORES)
        # Log raw counts so any run's confusion matrix can be rebuilt from MLflow
        mlflow.log_dict(
            {"labels": NUTRISCORES, "matrix": cm_arr.tolist()},
            "confusion_matrix.json",
        )
        fig_cm, _ax_cm = plt.subplots(figsize=(6, 5))
        sns.heatmap(
            cm_arr,
            annot=True,
            fmt="d",
            xticklabels=NUTRISCORES,
            yticklabels=NUTRISCORES,
            ax=_ax_cm,
        )
        _ax_cm.set_xlabel("Predicted")
        _ax_cm.set_ylabel("Actual")
        _ax_cm.set_title("Confusion matrix: grade classification (XGBoost)")
        plt.tight_layout()
        mlflow.log_figure(fig_cm, "confusion_matrix.png")

        _pred_counts = pd.Series(y_pred).value_counts().reindex(NUTRISCORES, fill_value=0)
        _true_counts = pd.Series(y_test_g).value_counts().reindex(NUTRISCORES, fill_value=0)
        fig_cal, _axs_cal = plt.subplots(1, 2, figsize=(10, 4))
        _axs_cal[0].bar(NUTRISCORES, _true_counts.values, color="steelblue")
        _axs_cal[0].set_title("Actual grade counts (test)")
        _axs_cal[1].bar(NUTRISCORES, _pred_counts.values, color="coral")
        _axs_cal[1].set_title("Predicted grade counts (test)")
        plt.suptitle("Calibration check: do predicted frequencies look like reality?")
        plt.tight_layout()
        mlflow.log_figure(fig_cal, "grade_distribution_compare.png")

        _cal_models = [
            ("XGBoost", clf),
            (
                "LogisticRegression",
                Pipeline(
                    [
                        ("scale", StandardScaler()),
                        ("clf", LogisticRegression(max_iter=2000, random_state=0)),
                    ]
                ),
            ),
            ("RandomForest", RandomForestClassifier(n_estimators=100, random_state=0)),
        ]
        fig_rel, _ax_rel = plt.subplots(figsize=(6, 5))
        _ax_rel.plot([0, 1], [0, 1], linestyle="--", color="gray", label="Perfect calibration")
        _rel_data = {}
        for _name, _est in _cal_models:
            if _name != "XGBoost":
                _est.fit(X_train, y_train_clf)
            _proba_e = _est.predict_proba(X_test)[:, _grade_e]
            _y_bin_e = (y_test_clf == _grade_e).astype(int)
            _frac_pos, _mean_pred = calibration_curve(_y_bin_e, _proba_e, n_bins=10)
            _ax_rel.plot(_mean_pred, _frac_pos, marker="o", label=_name)
            _rel_data[_name] = {"mean_pred": _mean_pred.tolist(), "frac_pos": _frac_pos.tolist()}
        _ax_rel.set_xlabel("Mean predicted probability (grade E)")
        _ax_rel.set_ylabel("Fraction of positives (grade E)")
        _ax_rel.set_title("Reliability diagram: grade E (one-vs-rest)")
        _ax_rel.legend(loc="lower right")
        plt.tight_layout()
        # Log curve data so reliability diagrams can be compared across runs
        mlflow.log_dict(_rel_data, "calibration_curve_grade_E.json")
        mlflow.log_figure(fig_rel, "calibration_grade_E_multi_model.png")

    mo.vstack([fig_cm, fig_cal, fig_rel])
    return (clf,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 5c. ROC-AUC vs PR-AUC (grade E, one-vs-rest)

    **ROC-AUC** summarizes ranking quality across all decision thresholds on the same holdout set.

    **PR-AUC** (average precision) matters when positives are rare: ROC can look optimistic while the model still misses most true grade-E products.

    Keep the **same** train/test split; compare **XGBoost** vs **logistic regression** on grade **E** (OvR), alongside the calibration curves above.
    """)
    return


@app.cell
def _(
    X_test,
    X_train,
    clf,
    grade_encoder,
    mlflow,
    plt,
    y_test_clf,
    y_train_clf,
):
    from sklearn.linear_model import LogisticRegression as _LogisticRegression
    from sklearn.metrics import (
        PrecisionRecallDisplay,
        RocCurveDisplay,
        average_precision_score,
        roc_auc_score,
    )
    from sklearn.pipeline import Pipeline as _Pipeline
    from sklearn.preprocessing import StandardScaler as _StandardScaler

    _grade_e = int(grade_encoder.transform(["E"])[0])
    _y_bin = (y_test_clf == _grade_e).astype(int)
    _log_reg = _Pipeline(
        [
            ("scale", _StandardScaler()),
            ("clf", _LogisticRegression(max_iter=2000, random_state=0)),
        ]
    )
    _log_reg.fit(X_train, y_train_clf)
    _models = [("XGBoost", clf), ("LogisticRegression", _log_reg)]
    fig_roc_pr, _axes = plt.subplots(1, 2, figsize=(10, 4))
    _ax_roc, _ax_pr = _axes
    with mlflow.start_run(run_name="grade-roc-pr"):
        mlflow.set_tag("task", "classification")
        mlflow.set_tag("positive_class", "grade_E_ovr")
        for _name, _est in _models:
            _scores_e = _est.predict_proba(X_test)[:, _grade_e]
            RocCurveDisplay.from_predictions(_y_bin, _scores_e, ax=_ax_roc, name=_name)
            PrecisionRecallDisplay.from_predictions(
                _y_bin, _scores_e, ax=_ax_pr, name=_name
            )
            _roc = roc_auc_score(_y_bin, _scores_e)
            _pr = average_precision_score(_y_bin, _scores_e)
            print(f"{_name}: ROC-AUC={_roc:.3f}, PR-AUC={_pr:.3f}")
            _key = {"XGBoost": "xgboost", "LogisticRegression": "logistic"}[_name]
            mlflow.log_metric(f"roc_auc_{_key}", _roc)
            mlflow.log_metric(f"pr_auc_{_key}", _pr)
        _ax_roc.set_title("ROC — grade E (OvR)")
        _ax_pr.set_title("Precision–recall — grade E (OvR)")
        plt.tight_layout()
        mlflow.log_figure(fig_roc_pr, "roc_pr_grade_E.png")
    fig_roc_pr
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 5b. Skore (cross-validation reports)

    **MLflow** (above) logs each training run: metrics, artifacts, compare in `mlflow ui`.

    **Skore** (this section) is complementary: stratified CV summaries and side-by-side estimator comparison for the grade classifier. Use `compare()` to contrast `max_depth` values without opening MLflow.

    ### Two storage paths

    | Path | When | Setup |
    |------|------|-------|
    | **Workshop default (local)** | Students in class | `Project(..., mode="local", workspace=".skore-workspace")` — JSON under `.skore-workspace/` (gitignored) |
    | **Hub (teacher / optional)** | Share reports in [Skore Hub](https://skore.probabl.ai/) | Install `skore[hub]`, run the **Optional: Skore Hub** cell below (`skore.login()` opens a browser or reuses cached credentials), then switch the main cell to `mode="hub"` |

    Requires `skore[hub]` (already in this repo's `pyproject.toml`). No local `skore ui` CLI in pinned `skore==0.18.0`.
    """)
    return


@app.cell
def _(USE_SKORE_HUB):
    # Optional Skore Hub login — run when USE_SKORE_HUB is True (teachers).
    # Opens your browser once; credentials are cached for later sessions.
    if USE_SKORE_HUB:
        import skore

        skore.login()
        print("Skore Hub login OK (cached credentials on this machine)")
    else:
        print("Skipping Hub login (USE_SKORE_HUB is False in setup).")
    return (skore,)


@app.cell
def _(
    MAX_DEPTH,
    SKORE_HUB_WORKSPACE,
    USE_SKORE_HUB,
    XGBClassifier,
    XGB_CLF_KWARGS,
    X_train,
    alt,
    pd,
    skore,
    y_train_clf,
):
    from pathlib import Path

    if USE_SKORE_HUB:
        _skore_project = skore.Project(
            f"{SKORE_HUB_WORKSPACE}/off-nutriscore-skore",
            mode="hub",
        )
        print(f"Skore Hub project: {SKORE_HUB_WORKSPACE}/off-nutriscore-skore")
    else:
        _skore_ws = Path(".skore-workspace").resolve()
        _skore_project = skore.Project(
            "off-nutriscore-skore",
            mode="local",
            workspace=_skore_ws,
        )
        print(f"Skore workspace: {_skore_ws}")

    # Single EstimatorReport (80/20 split) pushed to Hub for interactive exploration
    _est_single = XGBClassifier(
        max_depth=MAX_DEPTH, n_estimators=50, random_state=0, **XGB_CLF_KWARGS
    )
    _single_report = skore.evaluate(_est_single, X_train, y_train_clf, splitter=0.2)
    _skore_project.put("grade-estimator", _single_report)
    print("Pushed EstimatorReport to Hub as \'grade-estimator\'")

    # Cross-validation at several depths
    _depths = sorted({2, MAX_DEPTH, 8})
    _cv_by_depth = {}
    for _d in _depths:
        _est = XGBClassifier(
            max_depth=_d, n_estimators=50, random_state=0, **XGB_CLF_KWARGS
        )
        _cv_by_depth[_d] = skore.evaluate(
            _est, X_train, y_train_clf, splitter=3, n_jobs=-1
        )
        _skore_project.put(f"grade-cv-depth-{_d}", _cv_by_depth[_d])

    # Build parallel-coords data including max_depth as an axis
    _pc_rows = []
    for _d, _r in _cv_by_depth.items():
        _f = _r.metrics.summarize().frame()
        _mean_col = next(c for c in _f.columns if c[1] == "mean")
        _roc_idx = [idx for idx in _f.index if idx[0] == "ROC AUC"]
        _pc_rows.append({
            "max_depth": _d,
            "Accuracy": float(_f.loc[("Accuracy", ""), _mean_col]),
            "ROC AUC (macro)": float(_f.loc[_roc_idx, _mean_col].mean()),
            "Log loss": float(_f.loc[("Log loss", ""), _mean_col]),
            "Fit time (s)": float(_f.loc[("Fit time (s)", ""), _mean_col]),
        })

    _pc_df = pd.DataFrame(_pc_rows)
    _pc_df["depth_label"] = _pc_df["max_depth"].astype(str)
    _metric_order = ["max_depth", "Accuracy", "ROC AUC (macro)", "Log loss", "Fit time (s)"]
    _pc_melted = _pc_df[_metric_order + ["depth_label"]].melt(
        id_vars="depth_label", var_name="metric", value_name="raw_value"
    )
    _pc_melted["value"] = _pc_melted.groupby("metric")["raw_value"].transform(
        lambda s: (s - s.min()) / (s.max() - s.min() + 1e-9)
    )

    _chart_parallel = (
        alt.Chart(_pc_melted)
        .mark_line(point=True)
        .encode(
            x=alt.X("metric:N", sort=_metric_order, title=None, axis=alt.Axis(labelAngle=-15)),
            y=alt.Y("value:Q", title="Normalized (0 = min, 1 = max across depths)", axis=alt.Axis(labels=False)),
            color=alt.Color("depth_label:N", title="max_depth"),
            detail="depth_label:N",
            tooltip=["depth_label:N", "metric:N", alt.Tooltip("raw_value:Q", format=".4f")],
        )
        .properties(width=500, height=260, title="Depth comparison: CV metrics + hyperparameter (each axis normalized)")
    )
    print("Project keys:", ["grade-estimator"] + [f"grade-cv-depth-{d}" for d in _depths])
    _chart_parallel
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Exercise 5.1: Change `max_depth`

    Edit `MAX_DEPTH` in setup, re-run Section 5 (new MLflow run).

    ### Exercise 5.2: Read one misclassified pair

    From the confusion matrix, name one (actual, predicted) pair with a large off-diagonal count.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 6. Regression: score

    Numeric Nutri-Score: predicted vs actual and residuals.
    """)
    return


@app.cell
def _(
    MAX_DEPTH,
    XGBRegressor,
    X_test,
    X_train,
    mlflow,
    mo,
    np,
    plt,
    y_test_s,
    y_train_s,
):
    from sklearn.metrics import mean_absolute_error, r2_score

    with mlflow.start_run(run_name="score-baseline"):
        mlflow.set_tag("task", "regression")
        reg = XGBRegressor(max_depth=MAX_DEPTH, n_estimators=100, random_state=0)
        reg.fit(X_train, y_train_s)
        y_pred_s = reg.predict(X_test)
        rmse = float(np.sqrt(np.mean((y_test_s - y_pred_s) ** 2)))
        mae = float(mean_absolute_error(y_test_s, y_pred_s))
        r2 = float(r2_score(y_test_s, y_pred_s))
        mlflow.log_metric("rmse", rmse)
        mlflow.log_metric("mae", mae)
        mlflow.log_metric("r2", r2)
        print(f"Test RMSE: {rmse:.2f}  MAE: {mae:.2f}  R2: {r2:.3f}")

        fig_sc, _ax_sc = plt.subplots(figsize=(5, 5))
        _ax_sc.scatter(y_test_s, y_pred_s, alpha=0.2, s=8)
        lims = [min(y_test_s.min(), y_pred_s.min()), max(y_test_s.max(), y_pred_s.max())]
        _ax_sc.plot(lims, lims, "k--", lw=1)
        _ax_sc.set_xlabel("Actual nutriscore_score")
        _ax_sc.set_ylabel("Predicted")
        _ax_sc.set_title("Predicted vs actual")
        plt.tight_layout()
        mlflow.log_figure(fig_sc, "pred_vs_actual.png")

        resid = y_test_s - y_pred_s
        fig_r, _ax_r = plt.subplots(figsize=(5, 4))
        _ax_r.hist(resid, bins=40, color="steelblue", edgecolor="white")
        _ax_r.set_xlabel("Residual (actual - predicted)")
        _ax_r.set_title("Residual distribution")
        plt.tight_layout()
        mlflow.log_figure(fig_r, "residuals.png")

    mo.hstack([fig_sc, fig_r])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Exercise 6.1: Change `max_depth` for the regressor

    Re-run Section 6 after editing setup.

    ### Exercise 6.2: Find the largest residual

    Which product index has the largest absolute error? (Optional: inspect `df_model` row.)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 7. SHAP (classification)

    Multiclass XGBoost yields one SHAP tensor per grade. We slice **grade E** (one-vs-rest), matching Section 5.

    - [Beeswarm](https://shap.readthedocs.io/en/latest/example_notebooks/api_examples/plots/beeswarm.html): global feature impacts for grade E
    - [Waterfall](https://shap.readthedocs.io/en/latest/example_notebooks/api_examples/plots/waterfall.html): one predicted-E product in the test slice
    """)
    return


@app.cell
def _(FEATURE_COLS, X_test, X_train, clf, grade_encoder, mlflow, mo, plt):
    import shap

    _X_shap = X_test.iloc[:500]
    explainer = shap.Explainer(clf, X_train, feature_names=FEATURE_COLS)
    shap_values = explainer(_X_shap)

    _grade_e = int(grade_encoder.transform(["E"])[0])
    _vals = shap_values.values
    if _vals.ndim == 3:
        _base = shap_values.base_values
        _base_e = _base[:, _grade_e] if getattr(_base, "ndim", 0) == 2 else _base
        shap_e = shap.Explanation(
            values=_vals[:, :, _grade_e],
            base_values=_base_e,
            data=shap_values.data,
            feature_names=FEATURE_COLS,
        )
    else:
        shap_e = shap_values

    # Explicit new figures so beeswarm and waterfall don't share a canvas
    plt.figure(figsize=(8, 5))
    shap.plots.beeswarm(shap_e, max_display=8, show=False)
    fig_sh = plt.gcf()
    fig_sh.suptitle("SHAP beeswarm: grade E (multiclass slice)")
    plt.tight_layout()

    _e_mask = clf.predict(_X_shap) == _grade_e
    if _e_mask.any():
        _e_idx = int(_e_mask.nonzero()[0][0])
        plt.figure(figsize=(8, 5))
        shap.plots.waterfall(shap_e[_e_idx], max_display=8, show=False)
        fig_wf = plt.gcf()
        fig_wf.suptitle(f"SHAP waterfall: grade E (test sample {_e_idx})")
        plt.tight_layout()
    else:
        fig_wf = None
        print("No predicted-E rows in SHAP slice; waterfall skipped.")

    # Log SHAP mean |value| per feature so runs are comparable in MLflow
    _shap_importance = {
        f"shap_mean_abs_{feat}": float(abs(shap_e.values[:, i]).mean())
        for i, feat in enumerate(FEATURE_COLS)
    }
    with mlflow.start_run(run_name="grade-shap-figure"):
        mlflow.set_tag("task", "classification")
        for _k, _v in _shap_importance.items():
            mlflow.log_metric(_k, _v)
        mlflow.log_figure(fig_sh, "shap_beeswarm_grade_E.png")
        if fig_wf is not None:
            mlflow.log_figure(fig_wf, "shap_waterfall_grade_E.png")

    mo.vstack([fig_sh] + ([fig_wf] if fig_wf is not None else []))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Exercise 7.1: Change `max_display` in the SHAP cell

    ### Exercise 7.2: Name one feature that pushes samples toward grade E
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 8. Compare all runs

    Runs from Sections 4-7 are already in MLflow. Use `search_runs()` for a programmatic compare chart.

    **Required:** in a **separate terminal** (see Section 2), run MLflow UI, open a run, and find a logged PNG (Exercise 8.3).
    """)
    return


@app.cell
def _(mlflow):
    runs = mlflow.search_runs(experiment_names=["off-nutriscore"])
    _plot_df = runs[
        ["run_id", "tags.task", "metrics.accuracy", "metrics.rmse", "params.max_depth"]
    ].copy()
    _plot_df.head(10)
    return (runs,)


@app.cell
def _(alt, runs):
    _acc = runs.dropna(subset=["metrics.accuracy"])
    if len(_acc):
        alt.Chart(_acc).mark_circle(size=80).encode(
            x=alt.X("params.max_depth:O", title="max_depth"),
            y=alt.Y("metrics.accuracy:Q", title="accuracy"),
            color="tags.task:N",
            tooltip=["run_id", "metrics.accuracy"],
        ).properties(width=450, height=280, title="Classifier runs")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Exercise 8.1: Filter runs by tag `task=regression`

    ### Exercise 8.2: Build one Altair chart from the runs table

    ### Exercise 8.3: Open MLflow UI

    Run MLflow UI as in Section 2 (`uv run mlflow ui --backend-store-uri sqlite:///mlruns.db` from the repo root). If you use the default `./mlruns/` backend instead, use `uv run mlflow ui` or `--backend-store-uri file:./mlruns`. Find `confusion_matrix.png` on a classification run.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 9. Workshop

    ### Exercise 9.1: Build one chart from your runs table

    Hyperparameter story, or overlay two regressor configs.

    ### Exercise 9.2: Share to team chat

    Screenshot + one sentence + what you changed.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.status.toast(
        "Synced from git",
        description="Re-run setup + data cells if outputs look stale",
    )
    mo.md("**Pairing active:** Cursor agent is connected to this kernel.")
    return


if __name__ == "__main__":
    app.run()
