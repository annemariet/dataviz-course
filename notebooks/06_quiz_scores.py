import marimo

__generated_with = "0.23.8"
app = marimo.App(
    width="medium",
    app_title="Wooclap quiz scores — assiduity & grading",
)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Wooclap quiz score analysis

    **Course:** Data Visualization (PSL Master IASD, 2026)

    Five session slots (S1, S2, S3, S4–5, S6). Each slot contributes **4/20**:
    `score = (earned / max) × 4` from the Wooclap `Total` column.

    For **each slot**, independently:

    | Step | Autonomous only | In-class fallback | Final (with mega) |
    |------|-----------------|-------------------|-------------------|
    | 1 | autonomous score | autonomous score | autonomous score |
    | 2 | else **0** | else in-class × `(1 − penalty)` | else `max(in-class × (1 − penalty), mega credit)` |
    | Mega credit | — | — | `(earned/67) × weight` on missing autonomous; weights **4, 3, 2, 1, 0** for the 1st…5th gap |

    **In-class fallback** never uses the mega-quiz. **Final** uses mega only when it
    beats the penalised in-class score for that slot (or when in-class is missing).

    The leaderboard shows all three totals side by side. Only **final** is rounded
    for the reported mark.
    """)
    return


@app.cell
def _():
    from pathlib import Path

    import marimo as mo
    import matplotlib.pyplot as plt
    import pandas as pd
    import seaborn as sns

    plt.rcParams.update({
        "figure.dpi": 110,
        "font.family": "sans-serif",
        "axes.spines.top": False,
        "axes.spines.right": False,
    })
    sns.set_theme(style="ticks", palette="deep", font_scale=1.0)
    return Path, mo, pd, plt, sns


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 1. Quiz inventory & loading
    """)
    return


@app.cell
def _():
    from course_env import EXCLUDED_EMAILS, NOTES_DIR

    SLOT_ORDER = [1, 2, 3, 4, 6]
    SLOT_LABELS = {1: "S1", 2: "S2", 3: "S3", 4: "S4-5", 6: "S6"}
    POINTS_PER_QUIZ = 4
    MAX_TOTAL = 20
    N_SLOTS = 5

    MEGA_QUIZ_FILE = "IXRPAHC_The_optional_final_mega-quizz-results.xlsx"
    MEGA_MAX_POINTS = 67
    MEGA_SLOT_WEIGHTS = [4, 3, 2, 1, 0]

    SESSION_QUIZ_FILES = {
        1: {
            "in_class": "PUNIKL_Data_visualization_-_01_-_introduction_-_quiz-results.xlsx",
            "autonomous": "PUNIKL_Session_1_final_quiz-results (1).xlsx",
        },
        2: {
            "in_class": "DCSGQB_Data_visualization_-_02_-_Grammar_of_Graphics_-_quiz-results.xlsx",
            "autonomous": "DCSGQB_Session_2_-_Evaluation_quiz-results.xlsx",
        },
        3: {
            "in_class": "ABYNTKL_Data_visualization_-_03_-_Data_exploration_-_quiz-results.xlsx",
            "autonomous": "ABYNTKL_Session_3_-_Evaluation_Quiz-results.xlsx",
        },
        4: {
            "autonomous": "QMPBASA_Data_visualization_-_45_-_Viz__x_ML_-_quiz-results.xlsx",
            "in_class": "QMPBASA_Data_visualization_-_45__-_quiz-results.xlsx",
        },
        6: {
            "in_class": "IBYBCCT_Data_visualization_-_06_-_dashboarding_-_quiz-results.xlsx",
            "autonomous": "IBYBCCT_Session_6_-_dashboarding_-_evaluation_-_quiz-results.xlsx",
        },
    }
    return (
        EXCLUDED_EMAILS,
        MAX_TOTAL,
        MEGA_MAX_POINTS,
        MEGA_QUIZ_FILE,
        MEGA_SLOT_WEIGHTS,
        NOTES_DIR,
        N_SLOTS,
        POINTS_PER_QUIZ,
        SESSION_QUIZ_FILES,
        SLOT_LABELS,
        SLOT_ORDER,
    )


@app.cell
def _(EXCLUDED_EMAILS, POINTS_PER_QUIZ, SLOT_LABELS, SLOT_ORDER, pd):
    def normalize_email(value) -> str | None:
        if pd.isna(value):
            return None
        email = str(value).strip().lower()
        return email or None

    def parse_total(value) -> tuple[float, bool]:
        """Return (normalized score out of 4, participated)."""
        if pd.isna(value):
            return 0.0, False
        text = str(value).strip()
        if text in ("/", "") or " / " not in text:
            return 0.0, False
        earned_s, max_s = text.split(" / ", 1)
        try:
            earned = float(earned_s.strip())
            max_pts = float(max_s.strip())
        except ValueError:
            return 0.0, False
        if max_pts <= 0:
            return 0.0, False
        return (earned / max_pts) * POINTS_PER_QUIZ, True

    def load_quiz_file(path, slot, mode: str) -> pd.DataFrame:
        raw = pd.read_excel(path, sheet_name="Résultats principaux", engine="openpyxl")
        if "Total" not in raw.columns:
            raise ValueError(f"Missing Total column in {path.name}")
        total_idx = raw.columns.get_loc("Total")
        raw = raw.iloc[:, : total_idx + 1].copy()
        raw = raw.rename(columns=lambda c: str(c).strip())

        rows = []
        for _, row in raw.iterrows():
            email = normalize_email(row.get("Email"))
            if email is None or email in EXCLUDED_EMAILS:
                continue
            score, participated = parse_total(row.get("Total"))
            raw_family = row.get("Nom de famille")
            family_name = (
                None
                if pd.isna(raw_family)
                else str(raw_family).strip().upper() or None
            )
            rows.append({
                "email": email,
                "family_name": family_name,
                "slot": slot,
                "slot_label": SLOT_LABELS[slot],
                "quiz_mode": mode,
                "raw_score": row.get("Total"),
                "score": score,
                "participated": participated,
                "source_file": path.name,
            })
        return pd.DataFrame(rows)

    def load_all_quizzes(notes_dir, session_map) -> pd.DataFrame:
        frames = []
        inventory = []
        for slot in SLOT_ORDER:
            for mode, filename in session_map[slot].items():
                path = notes_dir / filename
                if not path.exists():
                    raise FileNotFoundError(f"Missing quiz file: {path}")
                inventory.append({
                    "slot": SLOT_LABELS[slot],
                    "quiz_mode": mode,
                    "file": filename,
                    "rows": len(pd.read_excel(path, sheet_name="Résultats principaux", engine="openpyxl")),
                })
                frames.append(load_quiz_file(path, slot, mode))
        return pd.concat(frames), pd.DataFrame(inventory)

    def load_mega_quiz(path, max_points: int) -> pd.DataFrame:
        raw = pd.read_excel(path, sheet_name="Résultats principaux", engine="openpyxl")
        if "Total" not in raw.columns:
            raise ValueError(f"Missing Total column in {path.name}")
        rows = []
        for _, row in raw.iterrows():
            email = normalize_email(row.get("Email"))
            if email is None or email in EXCLUDED_EMAILS:
                continue
            text = str(row.get("Total", "")).strip()
            if text in ("", "/") or " / " not in text:
                rows.append({
                    "email": email,
                    "participated": False,
                    "mega_ratio": 0.0,
                    "raw_score": text or None,
                })
                continue
            earned_s, max_s = text.split(" / ", 1)
            try:
                earned = float(earned_s.strip())
                max_pts = float(max_s.strip())
            except ValueError:
                rows.append({
                    "email": email,
                    "participated": False,
                    "mega_ratio": 0.0,
                    "raw_score": text,
                })
                continue
            if max_pts <= 0:
                rows.append({
                    "email": email,
                    "participated": False,
                    "mega_ratio": 0.0,
                    "raw_score": text,
                })
                continue
            ratio = earned / max_pts
            rows.append({
                "email": email,
                "participated": True,
                "mega_ratio": ratio,
                "raw_score": text,
                "mega_max_points": max_pts if max_pts != max_points else max_points,
            })
        return pd.DataFrame(rows)


    return load_all_quizzes, load_mega_quiz


@app.cell
def _(NOTES_DIR, SESSION_QUIZ_FILES, load_all_quizzes):
    quiz_long, file_inventory = load_all_quizzes(NOTES_DIR, SESSION_QUIZ_FILES)
    student_names = (
        quiz_long.dropna(subset=["family_name"])
        .drop_duplicates("email", keep="first")[["email", "family_name"]]
    )
    return file_inventory, quiz_long, student_names


@app.cell
def _(file_inventory, mo, quiz_long):
    mo.vstack([
            mo.md(
            f"Loaded **{len(file_inventory)}** quiz files "
            f"({quiz_long['email'].nunique()} unique student emails)."
        ),
    mo.ui.table(file_inventory)])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 2. Assiduity

    How many of the **5** slots each student completed (autonomous vs in-class).
    """)
    return


@app.cell
def _(N_SLOTS, pd, quiz_long):
    def _assiduity_table(long_df: pd.DataFrame) -> pd.DataFrame:
        records = []
        for email in sorted(long_df["email"].unique()):
            subset = long_df[long_df["email"] == email]
            auto_count = (
                subset[(subset["quiz_mode"] == "autonomous") & subset["participated"]]
                .groupby("slot")
                .ngroups
            )
            in_class_count = (
                subset[(subset["quiz_mode"] == "in_class") & subset["participated"]]
                .groupby("slot")
                .ngroups
            )
            records.append({
                "email": email,
                "autonomous_assiduity": f"{auto_count}/{N_SLOTS}",
                "in_class_assiduity": f"{in_class_count}/{N_SLOTS}",
                "autonomous_slots": auto_count,
                "in_class_slots": in_class_count,
            })
        return pd.DataFrame(records)

    assiduity = _assiduity_table(quiz_long)
    return (assiduity,)


@app.cell
def _(assiduity, mo):
    mo.md(
        f"**Mean assiduity:** autonomous "
        f"{assiduity['autonomous_slots'].mean():.1f}/5 · in-class "
        f"{assiduity['in_class_slots'].mean():.1f}/5"
    )
    mo.ui.table(
        assiduity.sort_values("autonomous_slots", ascending=False),
        pagination=False,
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 3. Parameters

    **In-class penalty:** when autonomous is missing, in-class score is multiplied
    by `(1 − penalty)` before comparing with mega-quiz credit.
    """)
    return


@app.cell
def _(mo):
    penalty_slider = mo.ui.slider(
        0.0,
        1.0,
        value=0.0,
        step=0.05,
        label="In-class penalty (when autonomous is missing)",
    )
    rounding_unit = mo.ui.dropdown(
        options=["0.25", "0.5", "1.0"],
        value="0.5",
        label="Rounding unit for final mark (round up)",
    )
    mo.vstack([
        mo.hstack([penalty_slider, mo.md("0 = full in-class credit · 1 = in-class ignored")]),
        rounding_unit,
    ])
    return penalty_slider, rounding_unit


@app.cell
def _(
    MEGA_MAX_POINTS,
    MEGA_QUIZ_FILE,
    MEGA_SLOT_WEIGHTS,
    NOTES_DIR,
    load_mega_quiz,
    mo,
):
    mega_quiz = load_mega_quiz(NOTES_DIR / MEGA_QUIZ_FILE, MEGA_MAX_POINTS)
    _mega_part = int(mega_quiz["participated"].sum())
    mo.md(
        f"Optional mega-quiz: **{_mega_part}** participants · "
        f"**{MEGA_MAX_POINTS}** pts max · diminishing weights **{MEGA_SLOT_WEIGHTS}** "
        f"× `(earned/max)` per autonomous gap"
    )
    return (mega_quiz,)


@app.cell
def _(mega_quiz):
    mega_quiz
    return


@app.cell
def _(MEGA_SLOT_WEIGHTS, SLOT_ORDER, pd):
    def _slot_scores(long_df, email: str) -> dict:
        subset = long_df[long_df["email"] == email]
        out = {}
        for slot in SLOT_ORDER:
            auto_rows = subset[(subset["slot"] == slot) & (subset["quiz_mode"] == "autonomous")]
            in_rows = subset[(subset["slot"] == slot) & (subset["quiz_mode"] == "in_class")]
            auto_part = bool(auto_rows["participated"].any())
            in_part = bool(in_rows["participated"].any())
            auto_score = (
                float(auto_rows.loc[auto_rows["participated"], "score"].iloc[0])
                if auto_part
                else None
            )
            in_score = (
                float(in_rows.loc[in_rows["participated"], "score"].iloc[0])
                if in_part
                else None
            )
            out[slot] = {
                "autonomous": auto_score,
                "in_class": in_score,
                "auto_participated": auto_part,
                "in_class_participated": in_part,
            }
        return out

    def _mega_credit(mega_ratio: float, gap_index: int) -> float:
        if mega_ratio <= 0:
            return 0.0
        weight = MEGA_SLOT_WEIGHTS[gap_index] if gap_index < len(MEGA_SLOT_WEIGHTS) else 0.0
        return mega_ratio * weight

    def compute_scores(
        long_df: pd.DataFrame,
        penalty: float,
        mega_df: pd.DataFrame | None = None,
    ) -> pd.DataFrame:
        mega_lookup: dict[str, float] = {}
        if mega_df is not None and len(mega_df):
            for _, row in mega_df.iterrows():
                if bool(row["participated"]):
                    mega_lookup[row["email"]] = float(row["mega_ratio"])

        rows = []
        for email in sorted(long_df["email"].unique()):
            slots = _slot_scores(long_df, email)
            mega_ratio = mega_lookup.get(email, 0.0)

            autonomous_total = 0.0
            inclass_fallback_total = 0.0
            final_total = 0.0
            mega_slots_used = 0
            gap_index = 0

            for slot in SLOT_ORDER:
                s = slots[slot]
                if s["auto_participated"]:
                    auto = float(s["autonomous"])
                    autonomous_total += auto
                    inclass_fallback_total += auto
                    final_total += auto
                    continue

                inc = float(s["in_class"]) if s["in_class_participated"] else 0.0
                inc_credit = inc * (1.0 - penalty)
                mega_slot_credit = _mega_credit(mega_ratio, gap_index)

                inclass_fallback_total += inc_credit
                slot_final = max(inc_credit, mega_slot_credit)
                final_total += slot_final
                if mega_slot_credit > inc_credit:
                    mega_slots_used += 1
                gap_index += 1

            rows.append({
                "email": email,
                "autonomous_total": round(autonomous_total, 2),
                "inclass_fallback_total": round(inclass_fallback_total, 2),
                "final_total": round(final_total, 2),
                "mega_slots_used": mega_slots_used,
            })
        return pd.DataFrame(rows)


    return (compute_scores,)


@app.cell
def _(
    MAX_TOTAL,
    compute_scores,
    mega_quiz,
    mo,
    penalty_slider,
    quiz_long,
    rounding_unit,
):
    import math

    def round_up_to_unit(value: float, unit: float) -> float:
        if unit <= 0:
            return value
        rounded = math.ceil(value / unit - 1e-12) * unit
        return min(MAX_TOTAL, round(rounded, 2))

    _raw = compute_scores(quiz_long, penalty_slider.value, mega_df=mega_quiz)
    _unit = float(rounding_unit.value)
    student_scores = _raw.assign(
        final_rounded=_raw["final_total"].map(lambda v: round_up_to_unit(v, _unit)),
    )
    mo.vstack([
        mo.md(
            f"Penalty **{penalty_slider.value:g}** · rounding **{_unit}** · "
            f"preview (top 10 by final rounded)"
        ),
        mo.ui.table(
            student_scores[[
                "email",
                "autonomous_total",
                "inclass_fallback_total",
                "final_total",
                "final_rounded",
                "mega_slots_used",
            ]]
            .sort_values("final_rounded", ascending=False)
            .head(10),
            pagination=False,
        ),
    ])

    return (student_scores,)


@app.cell
def _(mo, student_scores):
    def _stats(series):
        return {
            "mean": round(series.mean(), 2),
            "min": round(series.min(), 2),
            "max": round(series.max(), 2),
        }

    mo.md(
        f"""
        | Score | Mean | Min | Max |
        |-------|------|-----|-----|
        | Autonomous only | {_stats(student_scores['autonomous_total'])['mean']} | {_stats(student_scores['autonomous_total'])['min']} | {_stats(student_scores['autonomous_total'])['max']} |
        | In-class fallback | {_stats(student_scores['inclass_fallback_total'])['mean']} | {_stats(student_scores['inclass_fallback_total'])['min']} | {_stats(student_scores['inclass_fallback_total'])['max']} |
        | **Final (with mega)** | **{_stats(student_scores['final_total'])['mean']}** | **{_stats(student_scores['final_total'])['min']}** | **{_stats(student_scores['final_total'])['max']}** |
        """
    )

    return


@app.cell
def _(plt, sns, student_scores):
    _plot_df = student_scores.melt(
        id_vars=["email"],
        value_vars=["autonomous_total", "inclass_fallback_total", "final_total"],
        var_name="score_type",
        value_name="score",
    )
    _labels = {
        "autonomous_total": "Autonomous only",
        "inclass_fallback_total": "In-class fallback",
        "final_total": "Final (with mega)",
    }
    _plot_df["score_type"] = _plot_df["score_type"].map(_labels)

    fig_scores, axes = plt.subplots(1, 3, figsize=(11, 3.5), sharey=True)
    for ax, label in zip(axes, _labels.values(), strict=True):
        subset = _plot_df[_plot_df["score_type"] == label]["score"]
        sns.histplot(subset, kde=True, ax=ax, bins=12, color="#4c72b0")
        ax.set_title(label)
        ax.set_xlabel("Score /20")
        ax.set_xlim(0, 20)
    plt.tight_layout()
    fig_scores

    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 4. Leaderboard

    Ranked by **final** (rounded). All three scoring columns shown for comparison.
    """)
    return


@app.cell
def _(assiduity, mo, student_names, student_scores):
    leaderboard = (
        student_scores.merge(student_names, on="email", how="left")
        .merge(assiduity, on="email")
        .sort_values(["final_rounded", "email"], ascending=[False, True])
        .reset_index(drop=True)
    )
    leaderboard["rank"] = leaderboard.index + 1
    mo.ui.table(
        leaderboard[[
            "rank",
            "family_name",
            "email",
            "autonomous_total",
            "inclass_fallback_total",
            "final_total",
            "final_rounded",
            "mega_slots_used",
            "autonomous_assiduity",
            "in_class_assiduity",
        ]],
        pagination=True,
    )
    return (leaderboard,)


@app.cell
def _(leaderboard):
    leaderboard["final_rounded"].mean()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 5. Per-slot score matrix

    Raw normalized scores (out of 4) per slot — autonomous and in-class columns.
    """)
    return


@app.cell
def _(mo, quiz_long):
    slot_matrix = (
        quiz_long[quiz_long["participated"]]
        .pivot_table(
            index="email",
            columns=["slot_label", "quiz_mode"],
            values="score",
            aggfunc="first",
        )
        .round(2)
    )
    slot_matrix.columns = [f"{slot} ({quiz_mode})" for slot, quiz_mode in slot_matrix.columns]
    mo.ui.table(slot_matrix.reset_index(), pagination=True)
    return


if __name__ == "__main__":
    app.run()
