---
title: "Final Project Rubric — PSL IASD 2026 Dataviz"
date: 2026-06-02
tags: [teaching, dataviz, rubric, assessment, PSL, IASD]
status: draft
---

# Final Project Rubric for PSL IASD 2026 Dataviz

**Weight:** Main grade for the course (80%)
**Total:** 100 points

---

## Session format

- **Groups:** 1–3 students.
- **Group sign-up soft deadline:** Tuesday 2pm. Students submit: group name + member names.
- **Morning:** 
	- Students prepare their submission independently (no teaching in the morning).
	- All materials frozen and submitted at **2pm max**
- **Afternoon:** Presentations & self-evaluation:
	- ~5 min per group to present (no slides, present your notebook/dashboard)
	- ~5 min to evaluate, ask questions
	- Will adjust the slot length once the final group count is known.

### Submission

One of:
- Runnable notebook (Marimo or Jupyter)
- Streamlit app (deployed or runnable locally with clear setup instructions)
- Tableau Public dashboard (public link with file export or pure desktop file)

Submission files shared with the teacher before the afternoon starts.
**Charts must be reproducible with the provided files.**

### Presentation

1. What dataset did you choose, and why?
2. What question did you want to answer?
3. How did you approach it? (data processing, tool choice)
4. **Present your one focus chart.** This is the chart scored by Part 1.
5. Disclose what work you built upon (course notebooks, tutorials, existing code).

---

## Scoring structure

| Part                        | What it assesses                              | Evaluated by           | Points  |
| --------------------------- | --------------------------------------------- | ---------------------- | ------- |
| **1. Chart scoring**        | The one focus chart, on 5 criteria            | All students + teacher | 40      |
| **2. Presentation scoring** | Submission quality + the 5-min talk           | All students + Teacher | 40      |
| **3. Judgment**             | Calibration of critical eye across all charts | Computed post-session  | 20      |
| **Total**                   |                                               |                        | **100** |

---

## Part 1: Chart Scoring (40 pts)

### How it works

Immediately after each group's presentation, **all students and the teacher score the focus chart** silently using the MS Form (2–3 minutes). All students score all charts, including their own group's.

Scores are not revealed until the end of the afternoon. Self-ratings are included by default and can be filtered out in post-processing if needed.

The five questions are the same ones used in previous sessions.

### The five questions

---

**Q1. Focus** ★★★★★  
*Does the chart serve one clear purpose, with no irrelevant elements?*

| Stars | Description |
|-------|-------------|
| ★ | Multiple unrelated messages; heavy visual noise; hard to know what to look at |
| ★★ | A message exists but is buried; several distracting elements |
| ★★★ | One message, but some elements could be removed without loss |
| ★★★★ | Clear purpose; minor unnecessary decoration |
| ★★★★★ | Every element earns its place; nothing to add, nothing to remove |

---

**Q2. Clarity** ★★★★★  
*Does the key insight emerge within 5 seconds, without reading a caption or explanation?*

| Stars | Description |
|-------|-------------|
| ★ | Requires extensive explanation before understanding is possible |
| ★★ | Message emerges only after careful study |
| ★★★ | Readable but requires moderate effort; title helps a lot |
| ★★★★ | Insight is quick but one small barrier remains (legend, scale, etc.) |
| ★★★★★ | Insight is immediate to someone unfamiliar with the data |

---

**Q3. Encoding** ★★★★★  
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

**Q4. Honesty** ★★★★★  
*Is the chart truthful? Are scale, context, and data limitations shown fairly?*

| Stars | Description |
|-------|-------------|
| ★ | Actively misleading: truncated axis, cherry-picked range, distorted scale, correlation presented as causal |
| ★★ | Not intentionally deceptive but omits important caveats (no n shown, outliers hidden) |
| ★★★ | Honest but incomplete; a key limitation is absent |
| ★★★★ | Honest and mostly complete; one minor labelling gap |
| ★★★★★ | Axes start at zero (or deviation is justified); n shown; uncertainty conveyed; no selective framing |

---

**Q5. Craft** ★★★★★  
*Is the chart clean, fully labelled, and accessible to a broad audience?*

| Stars | Description                                                                                                      |
| ----- | ---------------------------------------------------------------------------------------------------------------- |
| ★     | Missing title and/or axis labels; illegible text; inaccessible colours                                           |
| ★★    | Title present but vague ("Figure 1"); units missing; default rainbow palette                                     |
| ★★★   | Functional; rough around edges (some labels missing, source not cited)                                           |
| ★★★★  | Well-labelled; readable; minor gap (source missing or font too small at print size)                              |
| ★★★★★ | Title states the insight; axes carry units; text legible at any size; colourblind-friendly palette; source cited |

---

### Part 1 scoring

For each chart: **sum of 5 question scores** (5–25 pts). Normalize the total across all charts to 40 pts.

Students may add a brief written comment on any rating to justify their choice. The teacher reviews these post-session and may adjust Part 3 for a student whose divergent rating is well-argued (see Part 3).

---

## Part 2: Presentation Scoring (40 pts)

### What is evaluated

Part 2 is graded by the students and the teacher from the 5-minute presentation and the submitted work, still using the Form.

### The five criteria (8 pts each)

---

**C1. Question and dataset choice** /8

| Score | Description |
|-------|-------------|
| 1–2 | No clear question; dataset used as-is with no stated purpose |
| 3–4 | A question is stated but trivial or obvious |
| 5–6 | Specific, non-trivial question; student explains why the dataset can answer it |
| 7–8 | Sharp question; compelling motivation; student acknowledges what the data cannot answer |

---

**C2. Approach and data literacy** /8

| Score | Description |
|-------|-------------|
| 1–2 | No explanation of processing; data used as-is |
| 3–4 | Processing described but choices not justified |
| 5–6 | Key choices explained (why outliers capped, why log transform, how missing data handled) |
| 7–8 | Every non-trivial step justified by the data's properties; student can answer follow-up questions |

---

**C3. Narrative and chart variety** /8

| Score | Description |
|-------|-------------|
| 1–2 | Charts are a list; no logical order; only one chart type used |
| 3–4 | Some order but transitions are not motivated; limited variety |
| 5–6 | Coherent arc; ≥3 chart types used appropriately; focus chart is the natural climax |
| 7–8 | Story is tight; complexity introduced progressively; chart types are each the best fit for their data |

---

**C4. Tool choice and execution** /8

| Score | Description                                                                                |
| ----- | ------------------------------------------------------------------------------------------ |
| 1–2   | Tool choice seems arbitrary or default; no interactivity where it would help               |
| 3–4   | Reasonable tool; one missed opportunity (e.g. static where interactive would add value)    |
| 5–6   | Tool fits the purpose; interactive or dashboard elements used where appropriate            |
| 7–8   | Tool choice is explicitly motivated; execution is clean; the medium reinforces the message |

---

**C5. Reproducibility and attribution** /8

| Score | Description |
|-------|-------------|
| 1–2 | Submission cannot be opened or run; no attribution |
| 3–4 | Runs with manual intervention; prior work not clearly disclosed |
| 5–6 | Runs end-to-end; data loading documented; sources of inspiration cited |
| 7–8 | Zero-friction reproduction; code or dashboard is clean and self-documenting; all built-upon work explicitly disclosed |

---

## Part 3: Judgment (20 pts)

### Rationale

Part 3 rewards students whose critical eye is well-calibrated against the teacher's and the cohort's collective judgment.

This is computed after the session from the Part 1 rating data.

### Formula

Let:
- $r_s$ = student's Part 1 ratings (all groups × 5 questions, in presentation order)
- $r_T$ = teacher's ratings for the same charts and questions
- $\bar{r}_P$ = mean ratings from the full cohort
- $r^* = \dfrac{\alpha \cdot r_T + \bar{r}_P}{\alpha + 1}$ : weighted consensus (teacher weight TBD)

**Calibration score:**
$$\text{score}_3 = \max(0,\ \rho_S(r_s,\ r^*)) \times 20$$

where $\rho_S$ is the **Spearman rank correlation** (appropriate for ordinal 1–5 scales). Floor at 0.

Tentative scoring, may be adjusted depending on actual correlation values:

| Spearman ρ | Part 3 score |
| ---------- | ------------ |
| ≥ 0.80     | 16–20        |
| 0.60–0.79  | 12–15        |
| 0.40–0.59  | 8–11         |
| 0.20–0.39  | 4–7          |
| < 0.20     | 0–3          |

### Handling divergent ratings

The correlation will penalize divergent ratings. There is a chance for students to justify their choice if they want to:
- Students may add a written comment on any Part 1 rating to explain their reasoning.
- After the session, the teacher reviews ratings that diverge significantly from the consensus and checks whether a written comment justifies the divergence.
- If the justification is compelling, the teacher may exclude that chart from the student's correlation calculation or apply a manual adjustment to Part 3.

This rewards original, well-argued critical thinking.
