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
showSlideNumber: true
---

<div class="absolute inset-0 z-0">
  <img src="/images/eiffel-photo-sunny.jpeg" class="w-full h-full object-cover" />
  <div class="absolute inset-0" style="background: rgba(0,0,0,0.2)"></div>
</div>

<div class="relative z-10 flex flex-col items-center justify-center h-full text-white text-center" style="text-shadow: 0 1px 10px rgba(0,0,0,0.9), 0 0 3px rgba(0,0,0,1)">

# Data is Beautiful

## Please Don't Ruin It

Anne-Marie Tousch · PSL Master IASD · May 2026

</div>

---
layout: center
---

# Let's start with a quick poll

Join at **wooclap.com** · code **AZNPLT**

<!--
Switch to Wooclap tab → https://app.wooclap.com/events/AZNPLT/live-session
-->


---
layout: two-cols-footer
---

# Why learn about data visualization?

::left::

**You will spend a lot of time visualizing data.**

- Exploring datasets before modelling
- Debugging model behaviour
- Discussing results with colleagues
- Convincing stakeholders

::right::

<img src="/images/training-console-output.png" class="w-full" style="max-height:250px; object-fit:cover; object-position:left" />


---

# Bad charts are everywhere

<div class="grid grid-cols-2 gap-3 mt-3">
<div class="text-center">
<img src="/images/bad-chart-french-tv-pie.png" class="mx-auto w-full" style="max-height:160px; object-fit:contain" />
</div>
<div class="text-center">
<img src="/images/bad-chart-fox-news-economic.png" class="mx-auto w-full" style="max-height:160px; object-fit:contain" />
</div>
<div class="text-center">
<img src="/images/bad-charts-pie-rounding.png" class="mx-auto w-full" style="max-height:160px; object-fit:contain" />
</div>
<div class="text-center">
<img src="/images/bad-chart-french-tv-bars.png" class="mx-auto w-full" style="max-height:160px; object-fit:contain" />
</div>
</div>

---
layout: two-cols-footer
---

# What's wrong with this chart?

::left::

<img src="/images/bad-chart-fox-news-economic.png" class="w-full" style="max-height:260px; object-fit:contain" />

::right::

**Chartjunk** showing many distracting colors, lines, glowing effects.

**Wrong label** (1.4% or 2%??)

**Dishonest:** Compares two periods of unequal length (59 years vs. 8 years)


---
layout: two-cols-footer
---

# What's wrong with this chart?

::left::

<img src="/images/bad-chart-fox-news-tax-cuts.png" class="w-full" style="max-height:260px; object-fit:contain" />


::right::

**Aesthetic** full of chartjunk

**Lie Factor** = (effect size in graphic) / (effect size in data) ~ 29 > 1

A quick redesign tells a different story:
<img src="/images/bad-chart-fox-redesign.png" class="w-full mt-3" style="max-height:55px; object-fit:contain" />

---
layout: center
---

# What to expect from this course

- Learn principled ways of designing your graphics
- Build hands-on experience with data (interactive) visualization tools
- Debug models visually
- Communicate results more efficiently to your stakeholders

---
layout: two-cols-header
---

# What to expect from this course

::left::

**Tentative program**

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

- 30–45 min: presentation
- 2h+: hands-on notebook workshop
- 15 min: quiz (spaced repetition)

**Assessment:** mini-project on June 11:

- choose a dataset (can be related to your daily work)
- find a story to tell / a problem to solve
- choose your tools
- demonstrate acquired visualization skills!

*Rubric will be communicated soon*.

---
layout: image-right
image: /images/eiffel-from-below-structural.jpeg
class: flex flex-col justify-center
---

# Why visualize?

---
layout: center
---

# A picture tells a thousand words


<img src="/images/chart-nvidia-vs-banks-market-cap.webp" class="w-full" style="max-height: 320px; object-fit: contain;" />

*[Nvidia's market cap vs. major banks. Source: Visual Capitalist, 2024.](https://www.visualcapitalist.com/chart-nvidias-market-cap-compared-to-banks/)*

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

# Visualization: a different view on data

<p class="text-gray-500 text-sm mb-3">There are many ways to represent the world. Don't get stuck in one projection.</p>

<div class="grid grid-cols-4 gap-3">
<div class="text-center">
<img src="/images/eiffel-engineering-blueprints-1887.jpeg" class="mx-auto w-full" style="max-height:200px; object-fit:cover; object-position:bottom" />
<p class="text-xs text-gray-400 mt-1">Engineering blueprints (1887)</p>
</div>
<div class="text-center">
<img src="/images/eiffel-under-construction-1888.jpeg" class="mx-auto w-full" style="max-height:200px; object-fit:cover" />
<p class="text-xs text-gray-400 mt-1">Under construction (1888)</p>
</div>
<div class="text-center">
<img src="/images/eiffel-from-below-structural.jpeg" class="mx-auto w-full" style="max-height:200px; object-fit:cover" />
<p class="text-xs text-gray-400 mt-1">Structural view from below</p>
</div>
<div class="text-center">
<img src="/images/eiffel-cail-inscription-detail.jpeg" class="mx-auto w-full" style="max-height:200px; object-fit:cover" />
<p class="text-xs text-gray-400 mt-1">Detail: Cail inscription</p>
</div>
<div class="text-center">
<img src="/images/eiffel-hand-forced-perspective.jpeg" class="mx-auto w-full" style="max-height:200px; object-fit:cover" />
<p class="text-xs text-gray-400 mt-1">Forced perspective</p>
</div>
<div class="text-center">
<img src="/images/eiffel-photo-sunny.jpeg" class="mx-auto w-full" style="max-height:200px; object-fit:cover" />
<p class="text-xs text-gray-400 mt-1">Photography</p>
</div>
<div class="text-center">
<img src="/images/eiffel-lego-model.jpeg" class="mx-auto w-full" style="max-height:200px; object-fit:cover" />
<p class="text-xs text-gray-400 mt-1">Model (LEGO)</p>
</div>
<div class="text-center">
<img src="/images/eiffel-delaunay-painting-1926.jpeg" class="mx-auto w-full" style="max-height:200px; object-fit:cover" />
<p class="text-xs text-gray-400 mt-1">Painting (Delaunay, 1926)</p>
</div>
</div>

---
layout: center
class: text-center
---

# Two reasons to visualize

<div class="grid grid-cols-2 gap-16 mt-8">
<div class="border border-blue-400 rounded-xl p-6">

### Explore

<img src="/images/oysters-explore.jpg" class="w-full mx-auto my-3" style="max-height:160px; object-fit:cover" />

Understand your data before you model it.

*What is the distribution? Are there outliers? Is there a pattern?*

</div>
<div class="border border-orange-400 rounded-xl p-6">

### Explain

<img src="/images/pearl-explain.jpg" class="w-full mx-auto my-3" style="max-height:160px; object-fit:cover" />

Communicate what you found to someone else.

*What is the story? What should they remember?*

</div>
</div>

<p class="mt-6 text-gray-400">The tools and the mindset are different. Know which mode you're in.</p>


---
layout: image-right
image: /images/eiffel-under-construction-1888.jpeg
class: flex flex-col justify-center
---

# How?

A four-step process for charts that actually work.

<div class="mt-6 text-gray-500">

1. Define your goal
2. Choose an effective visual
3. Find the right focus
4. Close the loop

</div>


---
layout: image-right
image: /images/eiffel-engineering-blueprints-1887.jpeg
class: flex flex-col justify-center
---

<p class="text-gray-400 text-sm font-mono mb-2">Step 1 / 4</p>

# Define your goal

Before picking a chart type, know what question you're answering — and who you're answering it for.


---
layout: two-cols-footer
---

# Discovery or Communication?

*Andrew Gelman & Antony Unwin — Infovis and Statistical Graphics (2013)*

::left::

**Discovery**
*For yourself*

- Fast, rough, iterative
- Many plots, few eyes
- Unexpected findings welcome
- "What's going on here?"

::right::

**Communication**
*For your audience*

- Polished, purposeful, annotated
- One plot, many readers
- Story decided in advance
- "Here is what I found"

::tagline::

> These modes have different aesthetics and conventions — and different failure modes. Know which one you're in.


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

> Choosing a table is a valid decision — don't reach for a chart by default.


---
layout: image-right
image: /images/eiffel-hand-forced-perspective.jpeg
class: flex flex-col justify-center
---

<p class="text-gray-400 text-sm font-mono mb-2">Step 2 / 4</p>

# Choose an effective visual

Match the visual encoding to the comparison you want to make. Not all channels carry the same weight.


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

<img src="/images/preattentive-attributes-full-channels.png" class="w-full mt-2" />

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

# Stevens' Psychophysical Power Law

*S. S. Stevens (1957) — the science behind perception accuracy*

::left::

<img src="/images/stevens-psychophysical-power-law.png" class="w-full" style="max-height:340px; object-fit:contain" />

::right::

<br/>

**S = I^n** — perceived magnitude *S* scales as a power of actual intensity *I*.

The exponent *n* varies by channel:

| Channel | n | Implication |
|---|---|---|
| Line length | ≈ 1.0 | Accurate |
| Area | ≈ 0.7 | We underestimate |
| Brightness | ≈ 0.33 | Heavily compressed |

This is why **bar charts** (length, n≈1) outperform **bubble charts** (area, n≈0.7) for precise comparisons.

> Use channels where n≈1 for your most important variable.

---
layout: center
---

# Visual encoding channels — ranked by accuracy

*Cleveland & McGill (1984) — empirical ranking from perception experiments*

<img src="/images/channel-ranking-infographic.png" class="mx-auto mt-4" style="max-height:400px; object-fit:contain" />


---
layout: image-right
image: /images/eiffel-cail-inscription-detail.jpeg
class: flex flex-col justify-center
---

<p class="text-gray-400 text-sm font-mono mb-2">Step 3 / 4</p>

# Find the right focus

Remove everything that isn't load-bearing. Highlight what matters. One chart = one message.


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
layout: image-right
image: /images/eiffel-delaunay-painting-1926.jpeg
class: flex flex-col justify-center
---

<p class="text-gray-400 text-sm font-mono mb-2">Step 4 / 4</p>

# Close the loop

Does it answer your question? Is there a story? Would a stranger understand it in 5 seconds?


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

<br/>

*Coming sessions will go deeper: Grammar of Graphics, interactive viz, storytelling, visualization × ML, and AI-assisted tools.*

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


---
layout: center
class: text-center
---

<img src="/images/meme-plot-all-the-data.jpg" class="mx-auto" style="max-height:400px" />
