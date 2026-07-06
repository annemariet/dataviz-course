import marimo

__generated_with = "0.23.8"
app = marimo.App(
    width="medium",
    app_title="Score this chart — peer review results",
)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Score this chart — peer review analysis

    Reads Microsoft Forms export from `chart-scoring/Score this chart.xlsx` and
    groups peer ratings by **Title of the graph**.

    Five criteria (1–5 stars each): Focus, Clarity, Encoding, Honesty, Craft.

    **Profile correlation** (per chart): compare each rater to student consensus.
    Switch Pearson / Spearman below (default Pearson). Teacher analysed separately.
    """)
    return


@app.cell
def _():
    from pathlib import Path

    import marimo as mo
    import matplotlib.pyplot as plt
    import pandas as pd
    import seaborn as sns
    import numpy as np

    plt.rcParams.update({
        "figure.dpi": 110,
        "font.family": "sans-serif",
        "axes.spines.top": False,
        "axes.spines.right": False,
    })
    sns.set_theme(style="ticks", palette="deep", font_scale=1.0)
    return Path, mo, np, pd, plt, sns


@app.cell
def _():
    TEAMS = ["YOP", 
             "Case départ",
             "PlotMyBar",
             "VizAlchemy",
             "Viz Khalifa",
             "viz-ionnaires",
             "Open your eyes",
             "Viz101",
             "RafChar",
             "EstOuest"
            ]
    return


@app.cell
def _():
    from course_env import CHART_SCORES_FILE, TEACHER_EMAIL

    TITLE_COLUMN = "Title of the graph"
    CRITERIA = ["Focus", "Clarity", "Encoding", "Honesty", "Craft"]
    MIN_CRITERIA_FOR_CORR = 3
    return (
        CHART_SCORES_FILE,
        CRITERIA,
        MIN_CRITERIA_FOR_CORR,
        TEACHER_EMAIL,
        TITLE_COLUMN,
    )


@app.cell
def _(CRITERIA, TEACHER_EMAIL, TITLE_COLUMN, pd):
    def normalize_email(value) -> str | None:
        if pd.isna(value):
            return None
        email = str(value).strip().lower()
        return email or None

    def criterion_name(column: str) -> str | None:
        if not column.startswith("Score the chart."):
            return None
        return column.split(".")[1].split(":")[0].strip().replace("\xa0", " ")

    def stars_to_score(value) -> float | None:
        if pd.isna(value):
            return None
        count = str(value).count("★")
        return float(count) if count else None

    def load_chart_scores(path) -> pd.DataFrame:
        raw = pd.read_excel(path, sheet_name=0, engine="openpyxl")
        raw = raw.rename(columns=lambda c: str(c).strip())

        score_cols = [c for c in raw.columns if c.startswith("Score the chart.")]
        rows = []
        for _, row in raw.iterrows():
            email = normalize_email(row.get("Email"))
            if email is None:
                continue
            title = row.get(TITLE_COLUMN)
            if pd.isna(title) or not str(title).strip():
                continue
            record = {
                "email": email,
                "name": row.get("Name"),
                "title": str(title).strip(),
                "is_teacher": email == TEACHER_EMAIL,
                "start_time": row.get("Start time"),
                "completion_time": row.get("Completion time"),
            }
            for col in score_cols:
                name = criterion_name(col)
                if name is None:
                    continue
                record[name] = stars_to_score(row.get(col))
            rows.append(record)

        scores = pd.DataFrame(rows)
        import hashlib

        def _hash_email(value) -> str | None:
            if pd.isna(value):
                return None
            email = str(value).strip().lower()
            return hashlib.sha256(email.encode()).hexdigest()[:12] if email else None

        scores["student_hash"] = scores["email"].map(_hash_email)
        for criterion in CRITERIA:
            if criterion not in scores.columns:
                scores[criterion] = pd.NA
        scores["mean_score"] = scores[CRITERIA].mean(axis=1, skipna=True)
        return scores

    return criterion_name, load_chart_scores, stars_to_score


@app.cell
def _(CHART_SCORES_FILE, load_chart_scores):
    all_scores = load_chart_scores(CHART_SCORES_FILE)
    chart_scores = all_scores[~all_scores["is_teacher"]].copy()
    teacher_scores = all_scores[all_scores["is_teacher"]].copy()
    return chart_scores, teacher_scores


@app.cell
def _(CRITERIA, chart_scores, mo):
    mo.vstack([
        mo.md(
            f"**{len(chart_scores)}** responses · "
            f"**{chart_scores['student_hash'].nunique()}** students · "
            f"**{chart_scores['title'].nunique()}** charts"
        ),
        mo.ui.table(
            chart_scores[
                ["title", "student_hash", *CRITERIA, "mean_score"]
            ].sort_values(["title", "mean_score"], ascending=[True, False]),
            pagination=False,
        ),
    ])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Summary by chart title
    """)
    return


@app.cell
def _(CRITERIA, chart_scores, pd):
    def summary_by_title(scores: pd.DataFrame) -> pd.DataFrame:
        grouped = scores.groupby("title", sort=True)
        rows = []
        for title, subset in grouped:
            row = {
                "title": title,
                "responses": len(subset),
                "students": subset["student_hash"].nunique(),
            }
            for criterion in CRITERIA:
                row[f"{criterion}_mean"] = round(subset[criterion].mean(), 2)
            row["overall_mean"] = round(subset["mean_score"].mean(), 2)
            rows.append(row)
        return pd.DataFrame(rows).sort_values("overall_mean", ascending=False)

    title_summary = summary_by_title(chart_scores)
    return (title_summary,)


@app.cell
def _(mo, title_summary):
    mo.ui.table(title_summary, pagination=False)
    return


@app.cell
def _(CRITERIA, chart_scores, plt, sns):
    long_scores = chart_scores.melt(
        id_vars=["title", "student_hash"],
        value_vars=CRITERIA,
        var_name="criterion",
        value_name="score",
    )
    fig, ax = plt.subplots(figsize=(9, 4))
    sns.barplot(
        data=long_scores,
        x="criterion",
        y="score",
        hue="title",
        ax=ax,
        errorbar="sd",
    )
    ax.set_ylim(0, 5.5)
    ax.set_ylabel("Mean score (stars)")
    ax.set_xlabel("")
    ax.set_title("Mean criterion scores by chart title")
    ax.legend(title="Chart", bbox_to_anchor=(1.02, 1), loc="upper left")
    plt.tight_layout()
    fig
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Detail per chart
    """)
    return


@app.cell
def _(CRITERIA, chart_scores, mo):
    chart_sections = []
    for title in sorted(chart_scores["title"].unique()):
        subset = chart_scores[chart_scores["title"] == title].sort_values(
            "mean_score", ascending=False
        )
        chart_sections.append(
            mo.vstack([
                mo.md(f"### {title}"),
                mo.md(
                    f"{len(subset)} responses · "
                    f"overall mean **{subset['mean_score'].mean():.2f}** / 5"
                ),
                mo.ui.table(
                    subset[["student_hash", *CRITERIA, "mean_score"]],
                    pagination=False,
                ),
            ])
        )
    mo.accordion(dict(zip(sorted(chart_scores["title"].unique()), chart_sections)))
    return


@app.cell(hide_code=True)
def _(mo):
    correlation_method = mo.ui.dropdown(
        options=["Pearson (score alignment)", "Spearman (rank alignment)"],
        value="Pearson (score alignment)",
        label="Correlation method",
    )
    mo.vstack([
        mo.md(r"""
        ---
        ## Profile correlation with student consensus

        **Student consensus** = mean stars per criterion (students only, NaN skipped per column).

        | Stage | Handling |
        |-------|----------|
        | Blank / unparsed stars | `NaN`; excluded from mean and pairwise comparison |
        | Correlation | Only criteria scored on **both** profiles; need **≥3** pairs |
        | Constant profile | All equal on used criteria → undefined → NaN + **note** |
        | Teacher | Same rules; never in consensus |

        **Pearson**: absolute score alignment. **Spearman**: rank-order alignment.
        """),
        correlation_method,
    ])
    return (correlation_method,)


@app.cell
def _(
    CRITERIA,
    MIN_CRITERIA_FOR_CORR,
    chart_scores,
    np,
    pd,
    pearsonr,
    spearmanr,
    teacher_scores,
):

    def _profile(row) -> np.ndarray:
        return row[CRITERIA].astype(float).to_numpy()

    def _aligned_pair(vec_a: np.ndarray, vec_b: np.ndarray) -> tuple[np.ndarray, np.ndarray, int]:
        mask = ~(np.isnan(vec_a) | np.isnan(vec_b))
        return vec_a[mask], vec_b[mask], int(mask.sum())

    def _profile_correlation(vec_a: np.ndarray, vec_b: np.ndarray, method: str) -> tuple[float | None, int, str | None]:
        a, b, n = _aligned_pair(vec_a, vec_b)
        if n < MIN_CRITERIA_FOR_CORR:
            return None, n, f"fewer than {MIN_CRITERIA_FOR_CORR} scored criteria ({n})"
        if len(set(a)) <= 1:
            return None, n, "left profile constant on used criteria"
        if len(set(b)) <= 1:
            return None, n, "right profile constant on used criteria"
        result = spearmanr(a, b) if method == "spearman" else pearsonr(a, b)
        stat = float(result.statistic)
        if np.isnan(stat):
            return None, n, "undefined (scipy)"
        return round(stat, 3), n, None

    def _missing_criteria_report(scores: pd.DataFrame) -> pd.DataFrame:
        rows = []
        for _, row in scores.iterrows():
            missing = [c for c in CRITERIA if pd.isna(row[c])]
            rows.append({
                "title": row["title"],
                "student_hash": row["student_hash"],
                "n_missing": len(missing),
                "missing_criteria": ", ".join(missing) if missing else "",
            })
        report = pd.DataFrame(rows)
        return report[report["n_missing"] > 0].sort_values(["title", "n_missing"], ascending=[True, False])

    def _consensus_vector(students: pd.DataFrame) -> np.ndarray:
        return students[CRITERIA].mean(skipna=True).to_numpy(dtype=float)

    def correlations_for_title(title: str, method: str) -> dict:
        students = chart_scores[chart_scores["title"] == title]
        teacher_rows = teacher_scores[teacher_scores["title"] == title]
        consensus = _consensus_vector(students)

        student_corr = []
        for _, row in students.iterrows():
            corr, n_used, note = _profile_correlation(_profile(row), consensus, method)
            student_corr.append({
                "student_hash": row["student_hash"],
                "correlation": corr,
                "n_criteria_used": n_used,
                "note": note or "",
            })
        student_corr_df = pd.DataFrame(student_corr).sort_values(
            "correlation", ascending=False, na_position="last"
        )

        teacher_vs_consensus = None
        teacher_consensus_note = None
        teacher_consensus_n = None
        teacher_vs_students = pd.DataFrame()
        if len(teacher_rows) == 1:
            teacher_vec = _profile(teacher_rows.iloc[0])
            teacher_vs_consensus, teacher_consensus_n, teacher_consensus_note = _profile_correlation(
                teacher_vec, consensus, method
            )
            pairs = []
            for _, row in students.iterrows():
                corr, n_used, note = _profile_correlation(teacher_vec, _profile(row), method)
                pairs.append({
                    "student_hash": row["student_hash"],
                    "correlation": corr,
                    "n_criteria_used": n_used,
                    "note": note or "",
                })
            teacher_vs_students = pd.DataFrame(pairs).sort_values(
                "correlation", ascending=False, na_position="last"
            )

        return {
            "consensus": students[CRITERIA].mean(skipna=True).round(2),
            "student_corr": student_corr_df,
            "undefined_count": int(student_corr_df["correlation"].isna().sum()),
            "teacher_vs_consensus": teacher_vs_consensus,
            "teacher_consensus_n": teacher_consensus_n,
            "teacher_consensus_note": teacher_consensus_note,
            "teacher_vs_students": teacher_vs_students,
        }

    def build_correlations(method: str) -> dict:
        return {
            title: correlations_for_title(title, method)
            for title in sorted(chart_scores["title"].unique())
        }

    missing_scores = _missing_criteria_report(
        pd.concat([chart_scores, teacher_scores], ignore_index=True)
    )
    return build_correlations, missing_scores


@app.cell
def _(build_correlations, correlation_method):
    _method = "pearson" if str(correlation_method.value).startswith("Pearson") else "spearman"
    corr_by_title = build_correlations(_method)
    corr_by_title
    return (corr_by_title,)


@app.cell
def _(
    corr_by_title,
    correlation_method,
    missing_scores,
    mo,
    pd,
):
    _method = "pearson" if str(correlation_method.value).startswith("Pearson") else "spearman"
    method_label = "Pearson r" if _method == "pearson" else "Spearman ρ"
    corr_sections = []
    for _title in sorted(corr_by_title):
        block = corr_by_title[_title]
        consensus_parts = []
        for k, v in block["consensus"].items():
            consensus_parts.append(f"**{k}** {v:.2f}" if pd.notna(v) else f"**{k}** —")
        corr_sections.append(
            mo.vstack([
                mo.md(f"### {_title}"),
                mo.md("Student consensus (mean stars): " + ", ".join(consensus_parts)),
                mo.md(
                    f"**Students vs consensus** ({method_label}) · "
                    f"{block['undefined_count']} undefined"
                ),
                mo.ui.table(block["student_corr"], pagination=False),
                mo.md(
                    f"**Teacher vs consensus:** "
                    f"{method_label} = {block['teacher_vs_consensus']} "
                    f"(n={block['teacher_consensus_n']}"
                    + (f", {block['teacher_consensus_note']}" if block['teacher_consensus_note'] else "")
                    + ")"
                ),
                mo.md(f"**Teacher vs each student** ({method_label})"),
                mo.ui.table(block["teacher_vs_students"], pagination=False),
            ])
        )
    _preview = mo.vstack([
        mo.md(f"**Method:** {method_label}"),
        mo.ui.table(missing_scores, pagination=False)
        if len(missing_scores)
        else mo.md("_No missing criterion scores in the file._"),
        mo.accordion(dict(zip(sorted(corr_by_title), corr_sections))),
    ])
    _preview
    return


@app.cell
def _(mo):
    mo.md(r"""
    ---
    ## Calibration score

    Each student rates each of the **10 charts** on **5 criteria** (1–5 stars): Focus, Clarity, Encoding, Honesty, Craft.

    Build a **charts × criteria** 10x5 matrix for the student (`student_matrix`), and the same shape for:

    - **Crowd reference**: mean rating per cell across all students (`crowd_matrix`)
    - **Teacher reference**: teacher's ratings (`teacher_matrix`)

    Flatten student and reference matrices to vectors **s**, **r** (`_flatten`) of dimension `d=50`. Keep only index pairs where both values exist; require **≥ 3 pairs**.

    Compute **score_crowd** and **score_teacher** separately, then combine with weight α (`combined_score`):

    \[
    \text{score\_final} = \frac{\text{score\_crowd} + \alpha \cdot \text{score\_teacher}}{1 + \alpha}
    \]

    (scale `/20`: `PART3_SCALE = 20` in the helpers cell.)

    ### Alignment methods (dropdown)

    | Method | Formula | Implementation |
    |--------|---------|----------------|
    | **Pearson** | \(r = \mathrm{corr}(\mathbf{s}, \mathbf{r})\); score \(= \max(0,\, r) \times 20\) | `_pearson_alignment` |
    | **Mean absolute gap** | \(\mathrm{MAD} = \mathrm{mean}_i \,\|s_i - r_i\|\); score \(= \max(0,\, 1 - \mathrm{MAD}/4) \times 20\) | `_mad_alignment` (`MAX_STAR_GAP = 4`) |
    | **Rank agreement** | For each criterion, Spearman ρ between chart rank vectors; score \(= \max(0,\, \bar\rho) \times 20\) with \(\bar\rho\) = mean over criteria | `_spearman6b_alignment` |

    Undefined alignment (constant profile, too few pairs) → **0**, not NaN.

        Dispatcher: `calibration_scores(...)`.
    """)
    return


@app.cell(hide_code=True)
def _(CRITERIA, np, pd):
    from scipy.stats import pearsonr, spearmanr

    MAX_STAR_GAP = 4.0
    PART3_SCALE = 20.0
    SIM_N_STUDENTS = 26
    SIM_N_CHARTS = 10

    def student_matrix(rows: pd.DataFrame, charts: list[str]) -> np.ndarray:
        mat = np.full((len(charts), len(CRITERIA)), np.nan)
        by_title = rows.set_index("title")
        for i, title in enumerate(charts):
            if title not in by_title.index:
                continue
            rec = by_title.loc[title]
            if isinstance(rec, pd.DataFrame):
                rec = rec.iloc[0]
            for j, crit in enumerate(CRITERIA):
                val = rec.get(crit)
                mat[i, j] = float(val) if pd.notna(val) else np.nan
        return mat

    def crowd_matrix(students: pd.DataFrame, charts: list[str]) -> np.ndarray:
        mats = []
        for title in charts:
            sub = students[students["title"] == title]
            if sub.empty:
                mats.append(np.full(len(CRITERIA), np.nan))
            else:
                mats.append(sub[CRITERIA].mean(skipna=True).to_numpy(dtype=float))
        return np.vstack(mats)

    def teacher_matrix(teacher: pd.DataFrame, charts: list[str]) -> np.ndarray:
        return crowd_matrix(teacher, charts)

    def _flatten(mat: np.ndarray) -> np.ndarray:
        return mat.reshape(-1)

    def _score_from_unit(unit: float | None, *, is_mad: bool = False) -> float:
        if unit is None or np.isnan(unit):
            return 0.0
        if is_mad:
            return max(0.0, (1.0 - unit / MAX_STAR_GAP) * PART3_SCALE)
        return max(0.0, float(unit) * PART3_SCALE)

    def _coalesce_score(value: float | None) -> float:
        if value is None or (isinstance(value, float) and np.isnan(value)):
            return 0.0
        return float(value)

    def combined_score(
        score_crowd: float | None,
        score_teacher: float | None,
        alpha: float,
    ) -> float:
        sc = _coalesce_score(score_crowd)
        st = _coalesce_score(score_teacher)
        if alpha <= 0:
            return sc
        return (sc + alpha * st) / (1.0 + alpha)

    def _pearson_alignment(vec_s: np.ndarray, vec_ref: np.ndarray, min_pairs: int = 3):
        mask = ~(np.isnan(vec_s) | np.isnan(vec_ref))
        n = int(mask.sum())
        if n < min_pairs:
            return 0.0, n
        r = float(pearsonr(vec_s[mask], vec_ref[mask]).statistic)
        if np.isnan(r):
            return 0.0, n
        return _score_from_unit(r), n

    def _mad_alignment(vec_s: np.ndarray, vec_ref: np.ndarray, min_pairs: int = 3):
        mask = ~(np.isnan(vec_s) | np.isnan(vec_ref))
        n = int(mask.sum())
        if n < min_pairs:
            return 0.0, n
        mad = float(np.mean(np.abs(vec_s[mask] - vec_ref[mask])))
        return _score_from_unit(mad, is_mad=True), n

    def _rank_desc(values: np.ndarray) -> np.ndarray:
        order = (-values).argsort().argsort().astype(float)
        order[np.isnan(values)] = np.nan
        return order

    def _spearman6b_alignment(st_mat: np.ndarray, ref_mat: np.ndarray, min_charts: int = 3):
        rhos = []
        n_charts = st_mat.shape[0]
        for j in range(len(CRITERIA)):
            if n_charts < min_charts:
                continue
            s = st_mat[:, j]
            r = ref_mat[:, j]
            pair_mask = ~(np.isnan(s) | np.isnan(r))
            if pair_mask.sum() < min_charts:
                continue
            s_p = s[pair_mask]
            r_p = r[pair_mask]
            if len(set(s_p)) <= 1 or len(set(r_p)) <= 1:
                continue
            rho = float(spearmanr(_rank_desc(s_p), _rank_desc(r_p)).statistic)
            if not np.isnan(rho):
                rhos.append(rho)
        if not rhos:
            return 0.0, 0
        return _score_from_unit(float(np.mean(rhos))), len(rhos)

    def calibration_scores(
        st_mat: np.ndarray,
        crowd_mat: np.ndarray,
        teacher_mat: np.ndarray,
        method: str,
        alpha: float = 1.0,
    ) -> dict:
        flat_s = _flatten(st_mat)
        flat_c = _flatten(crowd_mat)
        flat_t = _flatten(teacher_mat)
        if method.startswith("Pearson"):
            sc, nc = _pearson_alignment(flat_s, flat_c)
            st, nt = _pearson_alignment(flat_s, flat_t)
            detail = f"{nc} pairs"
        elif method.startswith("MAD"):
            sc, nc = _mad_alignment(flat_s, flat_c)
            st, nt = _mad_alignment(flat_s, flat_t)
            detail = f"MAD on {nc} pairs"
        else:
            sc, nc = _spearman6b_alignment(st_mat, crowd_mat)
            st, nt = _spearman6b_alignment(st_mat, teacher_mat)
            detail = f"avg of {nc} criterion rank-ρ vs crowd"
        sf = combined_score(sc, st, alpha)
        return {
            "score_crowd": sc,
            "score_teacher": st,
            "score_final": sf,
            "n_crowd": nc,
            "n_teacher": nt,
            "detail": detail,
        }

    def normalize_cohort_sizes(well: int, ok: int, poor: int) -> dict[str, int]:
        sizes = {"well": int(well), "ok": int(ok), "poor": int(poor)}
        total = sum(sizes.values())
        if total == SIM_N_STUDENTS:
            return sizes
        if total <= 0:
            return {"well": 8, "ok": 10, "poor": 8}
        keys = list(sizes.keys())
        raw = [max(0, int(round(sizes[k] * SIM_N_STUDENTS / total))) for k in keys]
        while sum(raw) < SIM_N_STUDENTS:
            raw[raw.index(min(raw))] += 1
        while sum(raw) > SIM_N_STUDENTS:
            raw[raw.index(max(raw))] -= 1
        return dict(zip(keys, raw, strict=True))

    def _chart_quality_vector(
        rng: np.random.Generator,
        n_good: int,
        good_lo: float = 4.0,
        good_hi: float = 5.0,
        bad_lo: float = 1.5,
        bad_hi: float = 2.5,
    ) -> np.ndarray:
        n_good = int(np.clip(n_good, 0, SIM_N_CHARTS))
        n_bad = SIM_N_CHARTS - n_good
        good = rng.uniform(good_lo, good_hi, n_good) if n_good else np.array([])
        bad = rng.uniform(bad_lo, bad_hi, n_bad) if n_bad else np.array([])
        q = np.concatenate([good, bad])
        rng.shuffle(q)
        return q

    def _simulate_once(
        method: str,
        scenario: str,
        teacher_mode: str,
        rng: np.random.Generator,
        *,
        cohort_sizes: dict[str, int],
        n_good_charts: int = 5,
        alpha: float = 1.0,
    ):
        chart_quality = _chart_quality_vector(rng, n_good_charts)
        teacher_noise = 0.15 if teacher_mode.startswith("Good") else 0.0
        teacher_mat = np.clip(
            np.round(chart_quality[:, None] + rng.normal(0, teacher_noise, (SIM_N_CHARTS, len(CRITERIA)))),
            1,
            5,
        )

        cohorts = {
            "well": {"n": cohort_sizes["well"], "noise": 0.45, "invert": False},
            "ok": {"n": cohort_sizes["ok"], "noise": 1.1, "invert": False},
            "poor": {"n": cohort_sizes["poor"], "noise": 2.0, "invert": True},
        }
        rows = []
        crowd_accum = np.zeros((SIM_N_CHARTS, len(CRITERIA)))
        crowd_count = np.zeros((SIM_N_CHARTS, len(CRITERIA)))

        if scenario.startswith("Fully random"):
            mats = []
            labels = []
            for cohort, cfg in cohorts.items():
                for _ in range(cfg["n"]):
                    mats.append(rng.integers(1, 6, (SIM_N_CHARTS, len(CRITERIA))).astype(float))
                    labels.append(cohort)
            crowd_mat = np.mean(np.stack(mats, axis=0), axis=0)
            out = []
            for sm, cohort in zip(mats, labels, strict=True):
                sc = calibration_scores(sm, crowd_mat, teacher_mat, method, alpha=alpha)
                out.append({
                    "cohort": cohort,
                    "score_crowd": sc["score_crowd"],
                    "score_teacher": sc["score_teacher"],
                    "score_final": sc["score_final"],
                })
            return pd.DataFrame(out)

        for cohort, cfg in cohorts.items():
            for _ in range(cfg["n"]):
                sm = chart_quality[:, None] + rng.normal(0, cfg["noise"], (SIM_N_CHARTS, len(CRITERIA)))
                if cfg["invert"]:
                    sm = 6 - sm
                sm = np.clip(np.round(sm), 1, 5)
                crowd_accum += sm
                crowd_count += 1
                rows.append({"cohort": cohort, "_mat": sm})

        crowd_mat = crowd_accum / np.maximum(crowd_count, 1)
        out = []
        for row in rows:
            sc = calibration_scores(row["_mat"], crowd_mat, teacher_mat, method, alpha=alpha)
            out.append({
                "cohort": row["cohort"],
                "score_crowd": sc["score_crowd"],
                "score_teacher": sc["score_teacher"],
                "score_final": sc["score_final"],
            })
        return pd.DataFrame(out)

    def run_simulation(
        method: str,
        scenario: str,
        teacher_mode: str,
        n_runs: int = 100,
        seed: int = 0,
        *,
        cohort_sizes: dict[str, int],
        n_good_charts: int = 5,
        alpha: float = 1.0,
    ):
        rng = np.random.default_rng(seed)
        frames = [
            _simulate_once(
                method,
                scenario,
                teacher_mode,
                rng,
                cohort_sizes=cohort_sizes,
                n_good_charts=n_good_charts,
                alpha=alpha,
            )
            for _ in range(n_runs)
        ]
        sim = pd.concat(frames, ignore_index=True)
        summary = (
            sim.groupby("cohort")[["score_crowd", "score_teacher", "score_final"]]
            .agg(["mean", "std", "count"])
            .round(2)
        )
        return sim, summary

    return (
        PART3_SCALE,
        SIM_N_CHARTS,
        SIM_N_STUDENTS,
        calibration_scores,
        combined_score,
        crowd_matrix,
        normalize_cohort_sizes,
        pearsonr,
        run_simulation,
        spearmanr,
        student_matrix,
        teacher_matrix,
    )


@app.cell(hide_code=True)
def _(CRITERIA, SIM_N_CHARTS, mo):
    calibration_method = mo.ui.dropdown(
        options=[
            "Pearson — corr(flattened student, reference)",
            "MAD — mean |Δstars| on flattened vector",
            "Spearman — mean ρ of chart ranks per criterion",
        ],
        value="Pearson — corr(flattened student, reference)",
        label="Alignment method (see table above)",
    )
    teacher_weight = mo.ui.slider(
        0.0, 5.0, value=1.0, step=0.25,
        label="Teacher weight α  (score_final = (crowd + α·teacher) / (1+α))",
    )
    sim_scenario = mo.ui.dropdown(
        options=[
            "Fully random scoring",
            "Good/bad charts — mixed cohort (well / ok / poor)",
        ],
        value="Good/bad charts — mixed cohort (well / ok / poor)",
        label="Simulation scenario",
    )
    sim_teacher = mo.ui.dropdown(
        options=["Perfect (knows true chart quality)", "Good (small noise)"],
        value="Perfect (knows true chart quality)",
        label="Simulated teacher",
    )
    cohort_well = mo.ui.slider(0, 20, value=8, step=1, label="Students · well-calibrated")
    cohort_ok = mo.ui.slider(0, 20, value=10, step=1, label="Students · ok")
    cohort_poor = mo.ui.slider(0, 20, value=8, step=1, label="Students · poor")
    n_good_charts = mo.ui.slider(
        0, SIM_N_CHARTS, value=5, step=1,
        label=f"Good charts (of {SIM_N_CHARTS}; rest are bad)",
    )
    sim_runs = mo.ui.slider(20, 500, value=120, step=20, label="Simulation runs")

    mo.vstack([
        mo.md(
            f"Controls below. Simulation uses **{SIM_N_CHARTS} charts × {len(CRITERIA)} criteria**."
        ),
        calibration_method,
        teacher_weight,
        mo.md("---\n **Fairness simulation**"),
        sim_scenario,
        sim_teacher,
        mo.md("**Cohort sizes** (must sum to 26 — re-normalized if not)"),
        cohort_well,
        cohort_ok,
        cohort_poor,
        mo.md(f"**Chart quality split** (0–{SIM_N_CHARTS} good charts; rest are bad)"),
        n_good_charts,
        sim_runs,
    ])
    return (
        calibration_method,
        cohort_ok,
        cohort_poor,
        cohort_well,
        n_good_charts,
        sim_runs,
        sim_scenario,
        sim_teacher,
        teacher_weight,
    )


@app.cell(hide_code=True)
def _(
    SIM_N_CHARTS,
    calibration_method,
    calibration_scores,
    chart_scores,
    crowd_matrix,
    mo,
    pd,
    student_matrix,
    teacher_matrix,
    teacher_scores,
    teacher_weight,
):
    _charts = sorted(chart_scores["title"].unique())
    _crowd_mat = crowd_matrix(chart_scores, _charts)
    _teacher_mat = teacher_matrix(teacher_scores, _charts)
    _method = calibration_method.value
    _alpha = float(teacher_weight.value)

    _cal_rows = []
    for student_hash in sorted(chart_scores["student_hash"].unique()):
        sub = chart_scores[chart_scores["student_hash"] == student_hash]
        sm = student_matrix(sub, _charts)
        sc = calibration_scores(sm, _crowd_mat, _teacher_mat, _method, alpha=_alpha)
        _cal_rows.append({"student_hash": student_hash, "method": _method, "alpha": _alpha, **sc})

    calibration_table = pd.DataFrame(_cal_rows)
    if len(_charts) < SIM_N_CHARTS:
        _warn = mo.md(
            f"*Pilot: only **{len(_charts)}** charts in file — use **simulation** "
            f"({SIM_N_CHARTS} charts) to evaluate fairness.*"
        )
    else:
        _warn = mo.md("")

    _real_view = mo.vstack([
        _warn,
        mo.md(
            f"**Pilot · {len(_charts)} charts ·** { _method.split(' — ')[0] } · "
            f"α={_alpha:g}"
        ),
        mo.ui.table(
            calibration_table[
                [
                    "student_hash",
                    "score_crowd",
                    "score_teacher",
                    "score_final",
                    "n_crowd",
                    "n_teacher",
                    "detail",
                ]
            ].sort_values("score_final", ascending=False, na_position="last"),
            pagination=False,
        ),
    ])
    _real_view
    return


@app.cell(hide_code=True)
def _(
    PART3_SCALE,
    SIM_N_CHARTS,
    SIM_N_STUDENTS,
    calibration_method,
    cohort_ok,
    cohort_poor,
    cohort_well,
    mo,
    n_good_charts,
    normalize_cohort_sizes,
    pd,
    plt,
    run_simulation,
    sim_runs,
    sim_scenario,
    sim_teacher,
    sns,
    teacher_weight,
):
    _sim_sizes = normalize_cohort_sizes(
        int(cohort_well.value),
        int(cohort_ok.value),
        int(cohort_poor.value),
    )
    _raw_total = int(cohort_well.value) + int(cohort_ok.value) + int(cohort_poor.value)
    _n_good = int(n_good_charts.value)
    _sim_df, _sim_summary = run_simulation(
        calibration_method.value,
        sim_scenario.value,
        sim_teacher.value,
        n_runs=int(sim_runs.value),
        seed=42,
        cohort_sizes=_sim_sizes,
        n_good_charts=_n_good,
        alpha=float(teacher_weight.value),
    )
    _cohort_order = ["well", "ok", "poor"]
    _plot_df = _sim_df.copy()
    _plot_df["cohort"] = pd.Categorical(_plot_df["cohort"], categories=_cohort_order, ordered=True)

    fig_sim, axes = plt.subplots(1, 3, figsize=(13, 4), sharey=True)
    for _ax, _col, _title in zip(
        axes,
        ["score_crowd", "score_teacher", "score_final"],
        ["vs crowd", "vs teacher", "final (weighted)"],
        strict=True,
    ):
        sns.boxplot(data=_plot_df, x="cohort", y=_col, order=_cohort_order, ax=_ax)
        _ax.set_ylim(0, PART3_SCALE)
        _ax.set_xlabel("")
        _ax.set_ylabel("Calibration score /20")
        _ax.set_title(_title)
    fig_sim.suptitle(
        f"Simulation · {calibration_method.value} · α={float(teacher_weight.value):g}\n"
        f"{sim_scenario.value} · {sim_teacher.value} · "
        f"cohorts {_sim_sizes} · {_n_good} good charts",
        y=1.08,
    )
    plt.tight_layout()

    _means = _sim_df.groupby("cohort")[["score_crowd", "score_teacher", "score_final"]].mean()

    def _strictly_decreasing(series):
        if not set(_cohort_order).issubset(series.index):
            return None
        a, b, c = (series.loc[k] for k in _cohort_order)
        return a > b > c

    _sep = {col: _strictly_decreasing(_means[col]) for col in _means.columns}
    _verdict_lines = [
        f"- **{col.replace('score_', '')}**: "
        + ("well > ok > poor ✓" if ok else "no strict well > ok > poor")
        for col, ok in _sep.items()
    ]
    _cohort_msg = (
        f"*Cohort sliders sum to {_raw_total} (target {SIM_N_STUDENTS}) — using normalized {_sim_sizes}.*"
        if _raw_total != SIM_N_STUDENTS
        else f"Cohort mix: well={_sim_sizes['well']}, ok={_sim_sizes['ok']}, poor={_sim_sizes['poor']}."
    )

    _sim_view = mo.vstack([
        mo.md(_cohort_msg),
        mo.md(
            f"**Summary over {int(sim_runs.value)} runs** · "
            f"**{_n_good}** good / **{SIM_N_CHARTS - _n_good}** bad charts"
        ),
        mo.ui.table(_sim_summary.reset_index(), pagination=False),
        mo.md("**Fairness check (mean by cohort):**\n" + "\n".join(_verdict_lines)),
        fig_sim,
    ])
    _sim_view
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Mini-project session evaluation (production data)

    Loads Microsoft Forms exports from `project_eval/`:

    - **Teams** roster (`Enregistrement…Teams.csv`) — one row per team, up to 3 students
    - **Full evaluation** (`Evaluation Sheet…csv`) — Part 1 chart scores + Part 2 presentation scores

    | Part | Points | Rule |
    |------|--------|------|
    | **1 · Chart** | /40 | Peer mean (excluding self-evaluations) + teacher → weighted blend with α |
    | **2 · Presentation** | /40 | Same as Part 1 (peer mean excludes self-evaluations) |
    | **3 · Judgment** | /20 | Calibration vs crowd + teacher (self-eval optional; same α) |
    | **Total** | **/100** | Sum · final table shows **Note /20** (ceil to 0.5) |
    """)
    return


@app.cell
def _(mo):
    project_teacher_weight = mo.ui.slider(
        0.0, 5.0, value=1.0, step=0.25,
        label="Teacher weight α (Parts 1–3)",
    )
    project_teacher_weight
    return (project_teacher_weight,)


@app.cell
def _(
    CRITERIA,
    PART1_MAX_RAW,
    PART1_SCALE,
    combined_score,
    mo,
    pd,
    project_eval_students,
    project_eval_teacher,
    project_teacher_weight,
):
    PRES_COLS = [
        "question_dataset",
        "approach_literacy",
        "narrative_variety",
        "tool_execution",
        "reproducibility",
    ]


    def part1_raw(subset: pd.DataFrame) -> float | None:
        if subset.empty:
            return None
        return float(subset[CRITERIA].sum(axis=1, min_count=1).mean())


    def part2_raw(subset: pd.DataFrame, pres_cols: list[str]) -> float | None:
        if subset.empty:
            return None
        return float(subset[pres_cols].sum(axis=1, min_count=1).mean())


    def part1_team_scores(
        students: pd.DataFrame,
        teacher: pd.DataFrame,
        alpha: float,
    ) -> pd.DataFrame:
        peer = students[~students["is_self_eval"]]
        teams = sorted(students["team_evaluated"].dropna().unique())
        rows = []
        for team in teams:
            student_raw = part1_raw(peer[peer["team_evaluated"] == team])
            teacher_raw = part1_raw(teacher[teacher["team_evaluated"] == team])
            score_student = (
                (student_raw / PART1_MAX_RAW) * PART1_SCALE if student_raw is not None else None
            )
            score_teacher = (
                (teacher_raw / PART1_MAX_RAW) * PART1_SCALE if teacher_raw is not None else None
            )
            combined = combined_score(score_student, score_teacher, alpha)
            rows.append({
                "team": team,
                "part1_raw_student": round(student_raw, 2) if student_raw is not None else pd.NA,
                "part1_raw_teacher": round(teacher_raw, 2) if teacher_raw is not None else pd.NA,
                "part1_score_student": round(score_student, 2) if score_student is not None else pd.NA,
                "part1_score_teacher": round(score_teacher, 2) if score_teacher is not None else pd.NA,
                "part1_score": round(combined, 2) if combined is not None else pd.NA,
                "n_student_ratings": len(peer[peer["team_evaluated"] == team]),
            })
        return pd.DataFrame(rows).sort_values("part1_score", ascending=False, na_position="last")


    def part2_team_scores(
        students: pd.DataFrame,
        teacher: pd.DataFrame,
        pres_cols: list[str],
        alpha: float,
    ) -> pd.DataFrame:
        peer = students[~students["is_self_eval"]]
        teams = sorted(students["team_evaluated"].dropna().unique())
        rows = []
        for team in teams:
            student_raw = part2_raw(peer[peer["team_evaluated"] == team], pres_cols)
            teacher_raw = part2_raw(teacher[teacher["team_evaluated"] == team], pres_cols)
            combined = combined_score(student_raw, teacher_raw, alpha)
            rows.append({
                "team": team,
                "part2_raw_student": round(student_raw, 2) if student_raw is not None else pd.NA,
                "part2_raw_teacher": round(teacher_raw, 2) if teacher_raw is not None else pd.NA,
                "part2_score_student": round(student_raw, 2) if student_raw is not None else pd.NA,
                "part2_score_teacher": round(teacher_raw, 2) if teacher_raw is not None else pd.NA,
                "part2_score": round(combined, 2) if combined is not None else pd.NA,
                "n_student_ratings": len(peer[peer["team_evaluated"] == team]),
            })
        return pd.DataFrame(rows).sort_values("part2_score", ascending=False, na_position="last")


    _alpha = float(project_teacher_weight.value)
    part1_by_team = part1_team_scores(project_eval_students, project_eval_teacher, _alpha)
    part2_by_team = part2_team_scores(
        project_eval_students,
        project_eval_teacher,
        PRES_COLS,
        _alpha,
    )
    mo.vstack([
        mo.md(
            f"**{len(project_eval_students)}** student ratings · "
            f"**{project_eval_students['student_hash'].nunique()}** raters · "
            f"**{part1_by_team['team'].nunique()}** teams · α={_alpha:g} · "
            f"peer means exclude self-evaluations"
        ),
        mo.md("### Part 1 — chart scores (/40)"),
        mo.ui.table(part1_by_team, pagination=False),
        mo.md("### Part 2 — presentation scores (/40)"),
        mo.ui.table(part2_by_team, pagination=False),
    ])
    return part1_by_team, part2_by_team


@app.cell
def _():
    from course_env import EVAL_CSV, NOTES_DIR, TEAMS_CSV

    PART1_MAX_RAW = 25.0
    PART1_SCALE = 40.0
    PRESENTATION_CRITERIA = [
        "question_dataset",
        "approach_literacy",
        "narrative_variety",
        "tool_execution",
        "reproducibility",
    ]
    return (
        EVAL_CSV,
        NOTES_DIR,
        PART1_MAX_RAW,
        PART1_SCALE,
        PRESENTATION_CRITERIA,
        TEAMS_CSV,
    )


@app.cell
def _(
    CRITERIA,
    PRESENTATION_CRITERIA,
    TEACHER_EMAIL,
    criterion_name,
    pd,
    stars_to_score,
):
    import hashlib
    import re

    def _hash_value(value: str) -> str:
        return hashlib.sha256(value.encode()).hexdigest()[:12]

    def hash_email(value) -> str | None:
        if pd.isna(value):
            return None
        email = str(value).strip().lower()
        return _hash_value(email) if email else None

    def normalize_person_name(value) -> str | None:
        if pd.isna(value):
            return None
        text = str(value).strip()
        if not text:
            return None
        if "," in text:
            last, first = [part.strip() for part in text.split(",", 1)]
            return f"{first} {last}".lower()
        return text.lower()


    def family_name(value) -> str | None:
        if pd.isna(value):
            return None
        text = str(value).strip()
        if not text:
            return None
        if "," in text:
            return text.split(",", 1)[0].strip()
        tokens = text.split()
        upper_tokens = [t for t in tokens if t.isupper() and len(t) > 1]
        if upper_tokens:
            return " ".join(upper_tokens)
        particles = {"de", "du", "des", "le", "la", "van", "von", "ait", "el", "ben", "ibn"}
        if len(tokens) >= 4 and tokens[-3].lower().strip("-'") in particles:
            return " ".join(tokens[-3:])
        if len(tokens) >= 2 and tokens[-2].lower().strip("-'") in particles:
            return " ".join(tokens[-2:])
        # Prénom(s) then two-token surname (no ALL-CAPS block, no comma)
        if len(tokens) == 4 and not upper_tokens:
            return " ".join(tokens[-2:])
        if len(tokens) == 3 and not upper_tokens:
            return " ".join(tokens[-2:])
        return tokens[-1]

    def name_key(value) -> str | None:
        normalized = normalize_person_name(value)
        if not normalized:
            return None
        tokens = re.findall(r"[a-zàâäéèêëïîôùûüç'-]+", normalized)
        return " ".join(sorted(tokens)) if tokens else None

    def resolve_team_from_name_key(nk: str | None, key_to_team: dict[str, str]) -> str | None:
        if not nk:
            return None
        if nk in key_to_team:
            return key_to_team[nk]
        nk_tokens = set(nk.split())
        best_team = None
        best_len = -1
        for roster_key, team in key_to_team.items():
            roster_tokens = set(roster_key.split())
            if roster_tokens.issubset(nk_tokens) or nk_tokens.issubset(roster_tokens):
                if len(roster_tokens) > best_len:
                    best_team = team
                    best_len = len(roster_tokens)
        return best_team

    def team_key_from_label(value) -> str | None:
        if pd.isna(value):
            return None
        match = re.match(r"^([^(]+)", str(value).strip())
        return match.group(1).strip() if match else str(value).strip()

    def load_teams_roster(path) -> tuple[pd.DataFrame, dict[str, str]]:
        raw = pd.read_csv(path, sep=";", encoding="utf-8-sig")
        student_cols = [c for c in raw.columns if "lève" in c]
        roster_rows = []
        submitter_rows = []
        for _, row in raw.iterrows():
            team = str(row.iloc[5]).strip()
            submitter_email = str(row.get("Email", "")).strip().lower()
            if submitter_email:
                submitter_rows.append({"team": team, "email": submitter_email})
            for col in student_cols:
                if pd.notna(row[col]) and str(row[col]).strip():
                    nk = name_key(row[col])
                    if nk:
                        roster_rows.append({"team": team, "name_key": nk})
        roster = pd.DataFrame(roster_rows)
        team_sizes = roster.groupby("team", sort=True).size().rename("team_size")
        key_to_team = dict(roster.drop_duplicates("name_key")[["name_key", "team"]].values)
        submitter_map = {row["email"]: row["team"] for row in submitter_rows}
        return team_sizes.reset_index(), key_to_team, submitter_map

    def build_email_team_map(notes_dir, key_to_team, submitter_map, eval_name_keys) -> dict[str, str]:
        email_to_team = dict(submitter_map)
        for f in notes_dir.glob("*results*.xlsx"):
            try:
                raw = pd.read_excel(f, sheet_name="Résultats principaux", engine="openpyxl")
            except Exception:
                continue
            for _, row in raw.iterrows():
                email = str(row.get("Email", "")).strip().lower()
                if not email or email == "nan":
                    continue
                name = row.get("Name")
                if pd.isna(name):
                    name = f"{row.get('Prénom', '')} {row.get('Nom de famille', '')}".strip()
                team = resolve_team_from_name_key(name_key(name), key_to_team)
                if team:
                    email_to_team[email] = team
        for email, nk in eval_name_keys.items():
            if email in email_to_team:
                continue
            team = resolve_team_from_name_key(nk, key_to_team)
            if team:
                email_to_team[email] = team
        return email_to_team

    def load_project_eval(path, email_to_team: dict[str, str]) -> pd.DataFrame:
        raw = pd.read_csv(path, sep=";", encoding="utf-8-sig")
        raw = raw.rename(columns=lambda c: str(c).strip())
        team_col = "Name of the team being evaluated"
        chart_cols = [c for c in raw.columns if c.startswith("Score the chart.")]
        pres_cols = [
            c
            for c in raw.columns
            if c not in raw.columns[:6]
            and not c.startswith("Score the chart.")
            and c not in {"Final comments", "If you think your choice may not be so obvious: why did you choose this score?"}
        ]
        rows = []
        for _, row in raw.iterrows():
            email_raw = str(row.get("Email", "")).strip().lower()
            if not email_raw or email_raw == "nan":
                continue
            team_eval = team_key_from_label(row.get(team_col))
            student_team = email_to_team.get(email_raw)
            student_name = str(row.get("Name", "")).strip()
            record = {
                "student_hash": hash_email(email_raw),
                "student_name": student_name or pd.NA,
                "team_evaluated": team_eval,
                "student_team": student_team,
                "is_teacher": email_raw == TEACHER_EMAIL,
                "is_self_eval": student_team == team_eval if student_team else False,
            }
            for col in chart_cols:
                name = criterion_name(col)
                if name in CRITERIA:
                    record[name] = stars_to_score(row.get(col))
            for idx, col in enumerate(pres_cols):
                record[PRESENTATION_CRITERIA[idx]] = pd.to_numeric(row.get(col), errors="coerce")
            rows.append(record)
        return pd.DataFrame(rows), pres_cols

    return (
        build_email_team_map,
        family_name,
        load_project_eval,
        load_teams_roster,
        name_key,
    )


@app.cell
def _(
    EVAL_CSV,
    NOTES_DIR,
    TEAMS_CSV,
    build_email_team_map,
    load_project_eval,
    load_teams_roster,
    name_key,
    pd,
):
    team_sizes, key_to_team, submitter_map = load_teams_roster(TEAMS_CSV)
    _eval_raw = pd.read_csv(EVAL_CSV, sep=";", encoding="utf-8-sig", usecols=["Email", "Name"])
    eval_name_keys = {
        str(r["Email"]).strip().lower(): name_key(r["Name"])
        for _, r in _eval_raw.iterrows()
        if pd.notna(r["Email"])
    }
    del _eval_raw
    email_to_team = build_email_team_map(
        NOTES_DIR, key_to_team, submitter_map, eval_name_keys
    )
    project_eval, presentation_col_names = load_project_eval(EVAL_CSV, email_to_team)
    project_eval_students = project_eval[~project_eval["is_teacher"]].copy()
    project_eval_teacher = project_eval[project_eval["is_teacher"]].copy()
    return (
        email_to_team,
        project_eval_students,
        project_eval_teacher,
        team_sizes,
    )


@app.cell(hide_code=True)
def _(mo):
    project_self_eval = mo.ui.checkbox(
        value=True,
        label="Part 3 only: include self-evaluations when building crowd reference",
    )
    project_calibration_method = mo.ui.dropdown(
        options=[
            "Pearson — corr(flattened student, reference)",
            "MAD — mean |Δstars| on flattened vector",
            "Spearman — mean ρ of chart ranks per criterion",
        ],
        value="Spearman — mean ρ of chart ranks per criterion",
        label="Part 3 alignment method",
    )
    mo.vstack([
        mo.md("### Part 3 — judgment (/20)"),
        project_self_eval,
        project_calibration_method,
    ])
    return project_calibration_method, project_self_eval


@app.cell(hide_code=True)
def _(mo, project_teacher_weight):
    mo.md(f"""
    *Uses the same teacher weight α={float(project_teacher_weight.value):g} as Parts 1–2.*
    """)
    return


@app.cell
def _(
    CRITERIA,
    calibration_scores,
    crowd_matrix,
    family_name,
    mo,
    np,
    pd,
    pearsonr,
    project_calibration_method,
    project_eval_students,
    project_eval_teacher,
    project_self_eval,
    project_teacher_weight,
    student_matrix,
    teacher_matrix,
):
    _charts = sorted(project_eval_students["team_evaluated"].dropna().unique())
    _filtered = project_eval_students.copy()
    if not project_self_eval.value:
        _filtered = _filtered[~_filtered["is_self_eval"]]

    _chart_form = _filtered.assign(title=_filtered["team_evaluated"]).rename(
        columns={"student_hash": "email"}
    )
    _teacher_form = project_eval_teacher.assign(title=project_eval_teacher["team_evaluated"]).rename(
        columns={"student_hash": "email"}
    )
    _crowd_mat = crowd_matrix(_chart_form, _charts)
    _teacher_mat = teacher_matrix(_teacher_form, _charts)
    _method = project_calibration_method.value
    _alpha = float(project_teacher_weight.value)

    _names = (
        project_eval_students[["student_hash", "student_name", "student_team"]]
        .drop_duplicates("student_hash")
        .set_index("student_hash")
    )

    _part3_rows = []
    for _student_hash in sorted(_chart_form["email"].unique()):
        _sub = _chart_form[_chart_form["email"] == _student_hash]
        _sm = student_matrix(_sub, _charts)
        _sc = calibration_scores(_sm, _crowd_mat, _teacher_mat, _method, alpha=_alpha)
        _part3_rows.append({
            "student_hash": _student_hash,
            "part3_score": _sc["score_final"],
            "score_crowd": _sc["score_crowd"],
            "score_teacher": _sc["score_teacher"],
            "detail": _sc["detail"],
        })
    part3_by_student = pd.DataFrame(_part3_rows).sort_values(
        "part3_score", ascending=False, na_position="last"
    )

    _issue_rows = []
    for _, _row in part3_by_student.iterrows():
        if _row["part3_score"] > 0:
            continue
        _h = _row["student_hash"]
        _meta = _names.loc[_h] if _h in _names.index else None
        _family = (
            (family_name(_meta["student_name"]) or "").upper() or pd.NA
            if _meta is not None and pd.notna(_meta["student_name"])
            else _h
        )
        _team = _meta["student_team"] if _meta is not None else pd.NA
        _rated = project_eval_students[project_eval_students["student_hash"] == _h]
        _chart_ratings = _rated.groupby("team_evaluated")[CRITERIA].first()
        _flat = _chart_ratings.to_numpy(dtype=float).ravel()
        _valid = _flat[~np.isnan(_flat)]
        _reason = []
        if pd.isna(_team):
            _reason.append("team not mapped from roster/name")
        if len(_valid) == 0:
            _reason.append("no chart ratings found")
        elif len(set(_valid)) == 1:
            _reason.append(
                f"constant chart profile ({_valid[0]:g} on every scored criterion) — "
                f"scored 0 (no rank variation to reward)"
            )
        if _method.startswith("Pearson"):
            _sub = _rated.assign(title=_rated["team_evaluated"])
            _sm = student_matrix(_sub, _charts)
            _flat_s = _sm.reshape(-1)
            _flat_c = _crowd_mat.reshape(-1)
            _flat_t = _teacher_mat.reshape(-1)
            _mask_c = ~np.isnan(_flat_s) & ~np.isnan(_flat_c)
            _mask_t = ~np.isnan(_flat_s) & ~np.isnan(_flat_t)
            if _mask_c.sum() >= 3:
                _r_c = float(pearsonr(_flat_s[_mask_c], _flat_c[_mask_c]).statistic)
                if np.isnan(_r_c):
                    _reason.append("Pearson vs crowd undefined → 0")
                elif _r_c < 0:
                    _reason.append(
                        f"negative Pearson r={_r_c:.3f} vs crowd (generous/inverted vs cohort) → max(0,r)×20 = 0"
                    )
            if _mask_t.sum() >= 3:
                _r_t = float(pearsonr(_flat_s[_mask_t], _flat_t[_mask_t]).statistic)
                if not np.isnan(_r_t) and _r_t < 0:
                    _reason.append(f"negative Pearson r={_r_t:.3f} vs teacher → max(0,r)×20 = 0")
        elif not _reason:
            _reason.append(f"alignment scored 0 ({_row['detail']})")
        if not _reason:
            _reason.append("combined crowd/teacher alignment scored 0")
        _issue_rows.append({
            "family_name": _family,
            "student_team": _team,
            "part3_score": _row["part3_score"],
            "score_crowd": _row["score_crowd"],
            "score_teacher": _row["score_teacher"],
            "detail": _row["detail"],
            "likely_reason": "; ".join(_reason),
        })
    part3_issues = pd.DataFrame(_issue_rows)

    _part3_view = mo.vstack([
        mo.ui.table(
            part3_by_student.merge(
                _names.reset_index()[["student_hash", "student_name", "student_team"]],
                on="student_hash",
                how="left",
            )
            .assign(
                family_name=lambda df: df["student_name"].map(
                    lambda n: (family_name(n) or "").upper() or pd.NA
                ).astype("string"),
            )[
                [
                    "family_name",
                    "student_team",
                    "part3_score",
                    "score_crowd",
                    "score_teacher",
                    "detail",
                ]
            ],
            pagination=False,
        ),
        mo.md("#### Part 3 — missing or zero scores"),
        mo.ui.table(part3_issues, pagination=False)
        if len(part3_issues)
        else mo.md("_No missing or zero Part 3 scores._"),
    ])
    _part3_view
    return (part3_by_student,)


@app.cell
def _(mo):
    final_table_sort = mo.ui.dropdown(
        options=[
            "Score (rank)",
            "Family name A→Z",
            "Family name Z→A",
        ],
        value="Score (rank)",
        label="Sort final table by",
    )
    final_table_sort
    return (final_table_sort,)


@app.cell
def _(
    family_name,
    final_table_sort,
    mo,
    part1_by_team,
    part2_by_team,
    part3_by_student,
    pd,
    project_eval_students,
    team_sizes,
):
    import math

    def note_on_20(total_on_100: float) -> float:
        return math.ceil((total_on_100 / 100.0) * 20.0 * 2) / 2

    _student_teams = (
        project_eval_students[["student_hash", "student_name", "student_team"]]
        .dropna(subset=["student_team"])
        .drop_duplicates("student_hash")
        .assign(
            family_name=lambda df: df["student_name"].map(
                lambda n: (family_name(n) or "").upper() or pd.NA
            ).astype("string"),
        )
    )
    _grades = (
        _student_teams.merge(part1_by_team, left_on="student_team", right_on="team", how="left")
        .merge(
            part2_by_team[["team", "part2_score", "part2_raw_student", "n_student_ratings"]],
            left_on="student_team",
            right_on="team",
            how="left",
            suffixes=("", "_p2"),
        )
        .merge(part3_by_student, on="student_hash", how="left")
        .merge(team_sizes.rename(columns={"team": "student_team"}), on="student_team", how="left")
    )
    _grades["project_total"] = (
        _grades["part1_score"].fillna(0)
        + _grades["part2_score"].fillna(0)
        + _grades["part3_score"].fillna(0)
    ).round(2)
    _grades["note_20"] = _grades["project_total"].map(note_on_20)
    _grades = _grades.sort_values(
        ["project_total", "family_name", "student_hash"],
        ascending=[False, True, True],
    )
    _grades["rank"] = range(1, len(_grades) + 1)

    final_grades_base = _grades[[
        "rank",
        "family_name",
        "student_team",
        "part1_score",
        "part2_score",
        "part3_score",
        "project_total",
        "note_20",
        "team_size",
    ]].rename(columns={
        "part1_score": "part1_chart",
        "part2_score": "part2_pres",
        "part3_score": "part3_judgment",
    })

    _sort = final_table_sort.value
    if _sort == "Family name A→Z":
        final_grades_display = final_grades_base.sort_values(
            ["family_name"], ascending=[True], na_position="last"
        )
    elif _sort == "Family name Z→A":
        final_grades_display = final_grades_base.sort_values(
            ["family_name"], ascending=[False], na_position="last"
        )
    else:
        final_grades_display = final_grades_base

    _unmapped = (
        project_eval_students[["student_hash", "student_team"]]
        .drop_duplicates("student_hash")
        .loc[lambda df: df["student_team"].isna()]
    )
    mo.vstack([
        mo.md("### Final mini-project grades (/100)"),
        mo.ui.table(final_grades_display, pagination=False),
        mo.md(
            "**Rank** is always by score. Use the sort control above for alphabetical views. "
            "**Note /20** = ceil to nearest 0.5 of `(project_total / 100) × 20`."
        ),
        mo.md("#### Students without team mapping (excluded from final table)")
        if len(_unmapped)
        else mo.md(""),
        mo.ui.table(_unmapped, pagination=False) if len(_unmapped) else mo.md(""),
    ])
    return (final_grades_display,)


@app.cell
def _(final_grades_display, mo):
    mo.ui.table(final_grades_display, pagination=False)
    return


@app.cell
def _(final_grades_display, mo):
    mo.ui.table(final_grades_display[["family_name", "student_team", "note_20"]], pagination=False)
    return


@app.cell
def _(final_grades_display):
    final_grades_display["note_20"].describe()
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
