---
theme: seriph
title: "Data is Beautiful — Please Don't Ruin It"
info: |
  Introduction to Data Visualization
  PSL Master IASD · 2026
highlighter: shiki
lineNumbers: false
drawings:
  persist: false
transition: slide-left
mdc: true
colorSchema: light
---

# Data is Beautiful

## Please Don't Ruin It

Anne-Marie Tousch · PSL Master IASD · May 2026

---
layout: center
---

# Let's start with a quick poll

Join at **wooclap.com** · code **AZNPLT**

<!--
Switch to Wooclap tab → https://app.wooclap.com/events/AZNPLT/live-session
-->

---

# The same structure, rendered four ways

<p class="text-gray-500 text-sm mb-3">Same structure — different representations, different purposes. Data is no different.</p>

<div class="grid grid-cols-4 gap-3">
<div class="text-center">
<img src="/images/eiffel-photo-sunny.jpeg" class="mx-auto w-full" style="max-height:310px; object-fit:cover" />
<p class="text-xs text-gray-400 mt-1">Photography</p>
</div>
<div class="text-center">
<img src="/images/eiffel-lego-model.jpeg" class="mx-auto w-full" style="max-height:310px; object-fit:cover" />
<p class="text-xs text-gray-400 mt-1">Model (LEGO)</p>
</div>
<div class="text-center">
<img src="/images/eiffel-delaunay-painting-1926.jpeg" class="mx-auto w-full" style="max-height:310px; object-fit:cover" />
<p class="text-xs text-gray-400 mt-1">Painting (Delaunay, 1926)</p>
</div>
<div class="text-center">
<img src="/images/eiffel-engineering-blueprints-1887.jpeg" class="mx-auto w-full" style="max-height:310px; object-fit:cover" />
<p class="text-xs text-gray-400 mt-1">Engineering blueprints (1887)</p>
</div>
</div>

---
layout: two-cols-header
---

# Why does this course exist?

::left::

**You will spend a lot of time visualizing data.**

- Exploring datasets before modelling
- Debugging model behaviour
- Communicating results to colleagues
- Convincing stakeholders

::right::

**Most of what you see is bad.**

- Plain tables where a chart would fit on one slide
- Rainbow color maps hiding structure
- Pie charts that nobody can read
- Charts that mislead rather than inform

<br/>

> The ability to make a good chart is rarer than it should be — and more impactful than most people think.

---
layout: center
class: text-center
---

# Two reasons to visualize

<div class="grid grid-cols-2 gap-16 mt-12">
<div class="border border-blue-400 rounded-xl p-8">

### Explore

Understand your data before you model it.

*What is the distribution? Are there outliers? Is there a pattern?*

</div>
<div class="border border-orange-400 rounded-xl p-8">

### Explain

Communicate what you found to someone else.

*What is the story? What should they remember?*

</div>
</div>

<p class="mt-12 text-gray-400">The tools and the mindset are different. Know which mode you're in.</p>

---
layout: two-cols-header
---

# What to expect from this course

::left::

**6 sessions + 1 mini-project day**

| # | Date | Topic |
|---|------|-------|
| 1 | 07/05 | Principles + Matplotlib/Seaborn |
| 2 | 27/05 | Grammar of Graphics + Altair |
| 3 | 28/05 | Communication & Storytelling |
| 4 | 03/06 | Visualization × ML |
| 5 | 04/06 | Big Data Scale |
| 6 | 08/06 | AI-Assisted Viz + Ethics |
| 7+8 | 11/06 | Mini-project hackathon |

::right::

**How each session works**

- 30–45 min: concepts & examples
- 2h+: hands-on notebook workshop
- 15 min: quiz (spaced repetition)

**What you'll be able to do**

- Choose the right chart for any comparison
- Write publication-quality Python plots
- Debug models visually
- Communicate results that convince

**Assessment:** the mini-project on June 11 — one dataset, one story, your tools.

---

# I keep seeing plain tables

<div class="grid grid-cols-2 gap-8 mt-4">
<div>

<img src="/images/ml-paper-results-table.jpg" class="w-full" style="max-height:300px; object-fit:cover" />

<p class="text-xs text-gray-400 mt-1">Real ML paper results table. Which method wins? Hard to say.</p>

</div>
<div class="text-gray-700">

Questions this raises:

- Do they want me to read *all* of this?
- Did they copy-paste from their paper?
- Do they care about their audience?
- **Are they hiding something?**
- Do they realize a chart would be clearer?

Most charitable interpretation: **they didn't think about it.**

</div>
</div>

---
layout: two-cols-header
---

# A picture tells a thousand words

::left::

<img src="/images/chart-nvidia-vs-banks-market-cap.webp" class="w-full" style="max-height: 320px; object-fit: contain;" />

*[Nvidia's market cap vs. major banks. Source: Visual Capitalist, 2024.](https://www.visualcapitalist.com/chart-nvidias-market-cap-compared-to-banks/)*

::right::

<br/><br/>

A chart that makes the comparison **obvious** communicates far more than a table.

Direct labeling beats a legend. Annotations tell the story.

**Rule:** if your audience has to squint at a legend, you've already lost them.

---
layout: center
class: text-center
---

<img src="/images/meme-plot-all-the-data.jpg" class="mx-auto" style="max-height:400px" />

---
layout: two-cols-header
---

# Never trust summary statistics alone

::left::

<img src="/images/datasaurus-dozen-identical-stats.png" class="w-full" />

::right::

<br/>

All 13 datasets have **identical** means, standard deviations, and correlation.

They look completely different when plotted.

**Datasaurus** (Matejka & Fitzmaurice, 2017) — the modern heir to Anscombe's Quartet.

> Always visualize your data before modelling it.

---
layout: two-cols-header
---

# The human visual system

::left::

<img src="/images/brain-visual-cortex-areas.jpg" class="w-full" />

::right::

Our visual cortex processes images through a hierarchy of specialized areas — V1 through V8+.

**~50%** of the cerebral cortex is involved in vision.

**Gestalt principles** (1920s–) describe how we group:

| Principle | What it means |
|---|---|
| Proximity | Close → grouped |
| Similarity | Alike → grouped |
| Continuity | We follow smooth lines |
| Closure | We complete incomplete shapes |

> Good dataviz exploits these principles intentionally.

---
layout: center
class: text-center
---

# Count the 3s

<div class="font-mono text-2xl tracking-widest leading-loose mt-8">

756395068473

658663037576

860372658602

846589107830

</div>

<p class="text-gray-400 mt-8">Source: Storytelling with Data (Cole Nussbaumer Knaflic)</p>

---
layout: center
class: text-center
---

# Count the 3s

<div class="font-mono text-2xl tracking-widest leading-loose mt-8">

756<span class="text-red-400 font-bold">3</span>9506847<span class="text-red-400 font-bold">3</span>

65866<span class="text-red-400 font-bold">3</span>0<span class="text-red-400 font-bold">3</span>7576

860<span class="text-red-400 font-bold">3</span>72658602

8465891078<span class="text-red-400 font-bold">3</span>0

</div>

<p class="text-gray-400 mt-8">Color highlights the target before conscious processing. This is a <strong>preattentive attribute</strong>.</p>

---
layout: two-cols-header
---

# Preattentive attributes

Processed in < 200ms — *before* conscious attention.

::left::

<img src="/images/preattentive-attributes-examples.png" class="w-full mt-2" />

::right::

**Most powerful** (use for key comparisons)
- Spatial position
- Color hue / intensity
- Size / line length

**Weaker** (avoid for primary encoding)
- Angle → pie charts fail here
- Volume / 3D perspective
- Curvature

> Encode your most important dimension with the most powerful channel.

---
layout: two-cols-header
---

# Which channels carry quantity most accurately?

*Cleveland & McGill (1984) — empirical ranking from perception experiments*

::left::

<img src="/images/cleveland-mcgill-channel-ranking.png" class="w-full" style="max-height:420px; object-fit:contain" />

::right::

<br/>

Viewers extract quantities **most accurately** from:

1. **Position on a common scale** — scatter, dot plot
2. **Length** — bar chart
3. **Direction / angle** — line slope
4. Area — bubble chart
5. Volume / 3D — avoid
6. Color saturation — heatmap
7. Color hue — never for quantities

**Why pie charts fail:** they encode quantities as angles and areas — ranks 3–5. A bar chart uses position and length — ranks 1–2.

> "Encode your most important variable with the most effective channel."

---

# Use color sparingly

Limit to 6–8 distinct hues. Beyond that, viewers can't track them. Use color to *highlight*, not to decorate.

<div class="grid grid-cols-2 gap-8 mt-6">
<div>

**Choose the right type for your data:**

| Data type | Palette |
|---|---|
| Sequential (low→high) | `viridis`, `plasma`, `cividis` |
| Diverging (midpoint matters) | `RdBu`, `PiYG`, `coolwarm` |
| Categorical (no order) | `tab10`, `Set2`, `Paired` |
| **Never** | `jet`, `rainbow`, `hsv` |

</div>
<div>

```python
# Bad: rainbow colormap
ax.scatter(x, y, c=values, cmap="jet")

# Good: perceptually uniform
ax.scatter(x, y, c=values, cmap="viridis")

# Best for categories: qualitative palette
palette = sns.color_palette("tab10", n_colors=5)
```

</div>
</div>

---

# Design for color accessibility

~8% of men have color vision deficiency. Design for them by default.

<div class="grid grid-cols-2 gap-8 mt-6">
<div>

**Rules:**
- Avoid red/green as the only distinguishing factor
- Use ColorBrewer palettes ([colorbrewer2.org](https://colorbrewer2.org))
- Add shape or texture as a second channel
- Test with a colorblind simulator before publishing

**Resist decorative color.**  
If color carries no information, remove it.

</div>
<div>

```python
# seaborn's colorblind palette — safe by default
sns.set_palette("colorblind")

# matplotlib: explicit Okabe-Ito palette
OKABE_ITO = [
    "#E69F00", "#56B4E9", "#009E73",
    "#F0E442", "#0072B2", "#D55E00",
    "#CC79A7", "#000000",
]
ax.set_prop_cycle(color=OKABE_ITO)
```

</div>
</div>

---

# Size matters

Encode magnitude differences you want to compare.

<div class="grid grid-cols-2 gap-8 mt-4">
<div>

**When to use size:**
- Bubble charts: 3rd quantitative dimension
- Bar width (usually keep uniform)
- Point size in scatter plots for emphasis

**Rules:**
- Area encodes value → radius should be `sqrt(value)`
- Don't map 1D quantities to 2D area without warning

</div>
<div>

```python
# Bubble chart with Gapminder
ax.scatter(
    gdp_per_cap, life_expect,
    s=population / 1e5,   # area ∝ pop
    alpha=0.6,
    c=region_colors,
)
```

**If something is equally important, size it equally.**  
If one thing is more important — make it **BIG**.

</div>
</div>

---

# Follow the process

<div class="grid grid-cols-2 gap-8 mt-4">
<div>

**1. Define your goal**
- Explore vs explain?
- Who is the audience?
- What is the one thing they should remember?

**2. Choose an effective visual**
- Match chart type to the comparison you want
- Simple is almost always better

**3. Find the right focus**
- Remove everything that isn't load-bearing
- Highlight the key element

**4. Close the loop**
- Does it answer your question?
- Is there a story?

</div>
<div>

```
Explore / Explain
        ↓
Simple > Complex
        ↓
Function first, form next
        ↓
Use color and size with intent
        ↓
Remove clutter
        ↓
Does it answer your question?
```

</div>
</div>

---

# Best practices

<div class="grid grid-cols-2 gap-6">
<div>

✅ **Do**
- Choose the simplest chart that shows the pattern
- Start axes at zero for bar charts
- Label directly (annotations > legends when possible)
- Sort categories meaningfully
- Use a consistent color scheme
- Think about colorblind readers

</div>
<div>

❌ **Don't**
- Use 3D effects (skews perception)
- Truncate axes to exaggerate differences (without marking it clearly)
- Use pie charts for > 2 categories
- Use dual y-axes (almost always confusing)
- Add decorative grid lines, borders, tick marks
- Map the same variable to multiple channels redundantly

</div>
</div>

> "Don't let your design choices be happenstance. They should be the result of explicit decisions." — Tufte

---

# Pie charts are evil

Humans judge *angles* and *areas* poorly. Bar charts use *position* — our strongest channel.

<div class="grid grid-cols-3 gap-4 mt-4">
<div class="text-center">

<img src="/images/pie-chart-3d-ugly.png" class="mx-auto" style="max-height:185px" />

*3D tilt makes comparison impossible.*

</div>
<div class="text-center">

<img src="/images/pie-charts-three-variants.jpeg" class="mx-auto" style="max-height:185px" />

*Flat pies. Which slice is biggest in A vs C?*

</div>
<div class="text-center">

<img src="/images/bar-charts-three-variants.jpeg" class="mx-auto" style="max-height:185px" />

*Same data as bars. Ranking is obvious.*

</div>
</div>

<p class="text-gray-400 mt-4 text-sm">Your stakeholders will still ask for pie charts. Now you know how to push back.</p>

---

# Maximize data-ink ratio

**Edward Tufte**, *The Visual Display of Quantitative Information* (1983):

> "Data-ink is the non-erasable core of a graphic. The rest is ink that can be wiped away without losing data-information."

<div class="grid grid-cols-2 gap-8 mt-4">
<div>

**Chartjunk to remove:**
- Background colors
- Decorative borders
- Gradient fills
- Unnecessary tick marks
- Redundant labels
- 3D effects
- The grid (unless needed for reading values)

</div>
<div>

```python
# Matplotlib: start clean
plt.rcParams.update({
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.grid": False,
    "figure.facecolor": "white",
})

# Or use seaborn's default style
sns.set_theme(style="ticks")
sns.despine()
```

</div>
</div>

---

# The moiré effect & other traps

<div class="grid grid-cols-2 gap-8">
<div>

<img src="/images/moire-hatched-bars-chartjunk.png" class="w-full" />

*Hatched bars with a dense legend — visually noisy, no extra information gained.*

</div>
<div>

**Moiré patterns** arise from hatching. Distracting, carry no data.

**3D bar charts** distort heights — back bars look shorter even when equal.

**Rainbow colormaps** create false discontinuities. Prefer:

```python
# Sequential: viridis, plasma, cividis
# Diverging:  RdBu, PiYG, coolwarm
# Categorical: tab10, Set2, Paired
# Never: jet, rainbow, hsv
```

</div>
</div>

---
layout: two-cols-header
---

# Good defaults: matplotlib

::left::

<img src="/images/matplotlib-defaults-histogram.png" class="w-full" />
<p class="text-xs text-gray-400 text-center mt-1">matplotlib out of the box</p>

::right::

<br/>

Not terrible — but vivid blue, heavy spines, and no visual hierarchy.

A few `rcParams` changes buy you a lot:

```python
plt.rcParams.update({
    "figure.dpi": 110,
    "font.family": "sans-serif",
    "axes.spines.top": False,
    "axes.spines.right": False,
})
```

---
layout: two-cols-header
---

# Good defaults: seaborn

::left::

<img src="/images/seaborn-colorblind-clean-histogram.png" class="w-full" />
<p class="text-xs text-gray-400 text-center mt-1">seaborn white + colorblind + despine</p>

::right::

<br/>

Same data, two lines of change:

```python
sns.set_theme(
    style="white",
    palette="colorblind",
    font_scale=1.2,
)
sns.despine()
```

Set this **once** at the top of every notebook. Every plot inherits it.

---
layout: two-cols-header
---

# What can be visualized?

*Tamara Munzner, Visualization Analysis and Design (2014)*

::left::

<img src="/images/munzner-what-data-types.png" class="w-full" style="max-height:390px; object-fit:contain" />

::right::

<br/>

**4 dataset types** shape what charts are even possible:

- **Tables** — rows are items, columns are attributes
- **Networks** — nodes and links (trees are a subtype)
- **Fields** — continuous data (images, simulation grids)
- **Geometry** — spatial data with explicit positions

**5 attribute types** shape how you encode:

- *Categorical* — no order (countries, species)
- *Ordinal* — ordered but not numeric (small/medium/large)
- *Quantitative* — numeric with magnitude
- *Sequential / Diverging / Cyclic* — ordering direction

> "Many aspects of vis design are driven by the kind of data that you have at your disposal."

---

# Know your data

Before reaching for a chart type, ask:

| Question | Answer shapes the chart |
|---|---|
| How many variables? | 1 → distribution; 2 → relationship; 3+ → need encoding strategy |
| What *type* of variable? | Quantitative, Ordinal, Nominal, Temporal |
| What *comparison* do I want? | Ranking? Part-of-whole? Trend over time? Distribution? Correlation? |
| What is the *audience*? | Explorer needs detail; presenter needs story |

<br/>

> Choosing the wrong chart type for a comparison is one of the most common mistakes. A bar chart is terrible at showing a trend over time. A line chart is terrible at comparing magnitudes between unrelated categories.

---

# Table or graph?

*Stephen Few, Show Me the Numbers (2012)*

<div class="grid grid-cols-2 gap-8 mt-4">
<div class="border border-blue-300 rounded-xl p-6">

**Use a table when:**

- Reader needs to **look up individual values**
- Precise numbers matter
- Multiple units of measure in one display
- Values at different levels of aggregation (summary + detail)

*Example: quarterly sales by region with % of plan*

</div>
<div class="border border-orange-300 rounded-xl p-6">

**Use a graph when:**

- The message lives in **patterns, trends, exceptions**
- Whole series need to be compared at a glance

*Example: six months of revenue vs. last year vs. target*

</div>
</div>

<br/>

**The 8 relationships graphs can show:** nominal comparison · time series · ranking · part-of-whole · deviation · distribution · correlation · geospatial

> "Colorful 3D bar charts look impressive but tell the executive almost nothing. A plain table with context tells the whole story."

---
layout: two-cols-header
---

# Books worth reading

::left::

<img src="/images/books-desk-stack-dataviz.jpeg" class="w-full" style="max-height:340px; object-fit:cover" />

::right::

**Classics**

*The Visual Display of Quantitative Information* — Tufte · 2001  
*Visualization Analysis and Design* — Munzner · 2014

**For practitioners**

*Show Me the Numbers* — Few · 2012  
*Storytelling with Data* — Knaflic · 2015  
*How to Lie with Statistics* — Huff · 1954 (still sharp)

**Research**

Cleveland & McGill (1984) — Graphical perception  
Gelman & Unwin (2013) — Infovis vs statistical graphics  
Matejka & Fitzmaurice (2017) — Datasaurus

**Online:** [flowingdata.com](https://flowingdata.com) · [colorbrewer2.org](https://colorbrewer2.org) · [viz.wtf](https://viz.wtf) · [nytimes.com/section/upshot](https://www.nytimes.com/section/upshot)

---

# What we'll cover today

**Session 1 — Matplotlib & Seaborn**

- Figure anatomy: Figure, Axes, Artists
- pyplot vs object-oriented API
- Visual channels in practice: position, color, size, shape
- Distributions: histograms, KDE, box plots
- Relationships: scatter plots, pair plots, heatmaps
- Multi-panel figures and layout

<br/>

**Dataset:** Gapminder — 63 countries × 11 time points (1955–2005). Familiar, tells real stories, rewards every chart type we'll try.

---
layout: center
class: text-center
---

# Let's build some charts

```bash
cd projects/dataviz-workshop
uv sync --no-install-project
uv run marimo edit notebooks/01_matplotlib_seaborn.py
```

<p class="text-gray-400 mt-8">Open the notebook in edit mode to follow along and run each cell.</p>
