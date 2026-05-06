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

# Many ways to represent the world


<div class="grid grid-cols-4 gap-2">
<div class="flex items-center justify-center" style="height:155px">
<img src="/images/eiffel-engineering-blueprints-1887.jpeg" style="max-height:155px; max-width:100%; object-fit:contain" />
</div>
<div class="flex items-center justify-center" style="height:155px">
<img src="/images/eiffel-under-construction-1888.jpeg" style="max-height:155px; max-width:100%; object-fit:contain" />
</div>
<div class="flex items-center justify-center" style="height:155px">
<img src="/images/eiffel-from-below-structural.jpeg" style="max-height:155px; max-width:100%; object-fit:contain" />
</div>
<div class="flex items-center justify-center" style="height:155px">
<img src="/images/eiffel-cail-inscription-detail.jpeg" style="max-height:155px; max-width:100%; object-fit:contain" />
</div>
<div class="flex items-center justify-center" style="height:155px">
<img src="/images/eiffel-hand-forced-perspective.jpeg" style="max-height:155px; max-width:100%; object-fit:contain" />
</div>
<div class="flex items-center justify-center" style="height:155px">
<img src="/images/eiffel-photo-sunny.jpeg" style="max-height:155px; max-width:100%; object-fit:contain" />
</div>
<div class="flex items-center justify-center" style="height:155px">
<img src="/images/eiffel-lego-model.jpeg" style="max-height:155px; max-width:100%; object-fit:contain" />
</div>
<div class="flex items-center justify-center" style="height:155px">
<img src="/images/eiffel-delaunay-painting-1926.jpeg" style="max-height:155px; max-width:100%; object-fit:contain" />
</div>
</div>


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

A **large fraction** of the cerebral cortex is involved in vision.

**Gestalt principles** (1920s–) describe how we group:

| Principle | What it means |
|---|---|
| Proximity | Close → grouped |
| Similarity | Alike → grouped |
| Continuity | We follow smooth lines |
| Closure | We complete incomplete shapes |

> Good dataviz exploits these principles intentionally.


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


---

# What is the context?

**Success starts with an understanding of the context.**

- **WHAT**: What is the question you want to anwer?
    - Explore: Define before starting the exploration.
    - Explain: You know the answer.

- **HOW**: How can you use data to make your point?

- **WHO**: Consider your audience

---
layout: center
class: text-center
---

# Two different types of goals

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


---
layout: two-cols-footer
---

# Discovery or Communication?

<div class="flex items-center gap-3 mb-2">
<img src="/images/portrait-andrew-gelman.gif" class="rounded-full" style="height:48px; width:48px; object-fit:cover" />
<img src="/images/portrait-antony-unwin.jpeg" class="rounded-full" style="height:48px; width:48px; object-fit:cover" />
</div>

::left::

**Discovery**

- Observe **deviation** from expectations
- Overview / check **assumptions**, look for patterns
- Give a sense of the **complexity** of the data
- Flexible displays / interaction

::right::

**Communication**

- Display a **convincing** pattern
- Share information readily **understandable**
- **Storytelling**
- Attract attention, **stimulate** interest

::footer::

*Gelman & Unwin, "Infovis and Statistical Graphics: Different Goals, Different Looks" (2013) — [vis14.pdf](http://www.stat.columbia.edu/~gelman/research/published/vis14.pdf)*


---
layout: two-cols-footer
---

# Table or graph?


::left::

**Use a table when:**

- Reader needs to **look up individual values**
- Precise numbers matter
- Multiple units of measure in one display
- Values at different levels of aggregation (summary + detail)


::right::

**Use a graph when:**

- The message lives in **patterns, trends, exceptions**
- Whole series need to be compared at a glance
- Distributions, correlations, similarities...
- Network topology, spatial shapes...



---
layout: image-right
image: /images/eiffel-hand-forced-perspective.jpeg
class: flex flex-col justify-center
---

<p class="text-gray-400 text-sm font-mono mb-2">Step 2 / 4</p>

# Choose an effective visual


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


---

# Preattentive attributes

Processed in < 200ms, *before* conscious attention.


<img src="/images/preattentive-attributes-full-channels.png" class="w-full mt-2" />


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

<!--
| Channel | n | Implication |
|---|---|---|
| Line length | ≈ 1.0 | Accurate |
| Area | ≈ 0.7 | We underestimate |
| Brightness | ≈ 0.5 | We underestimate even more |

This is why **bar charts** (length, n≈1) outperform **bubble charts** (area, n≈0.7) for precise comparisons.

> Use channels where n≈1 for your most important variable.
-->

---
layout: center
---

# Visual encoding channels — ranked by accuracy

*Cleveland & McGill (1984) — empirical ranking from perception experiments*

<img src="/images/channel-ranking-infographic.png" class="mx-auto mt-4" style="max-height:400px; object-fit:contain" />

<!--
**Most powerful** (use for key comparisons)
- Spatial position
- Color hue / intensity
- Size / line length

**Weaker** (avoid for primary encoding)
- Angle → pie charts fail here
- Volume / 3D perspective
- Curvature
-->

---
layout: image-right
image: /images/eiffel-cail-inscription-detail.jpeg
class: flex flex-col justify-center
---

<p class="text-gray-400 text-sm font-mono mb-2">Step 3 / 4</p>

# Find the right focus


---

# Clutter is your worst enemy

<!-- 
Clutter is any visual element that takes up space but does not increase understanding.
The example shows a cluttered line chart before and after decluttering.
-->

<div class="grid grid-cols-2 gap-6 mt-4">
<div>

<img src="/images/line-chart-bad-before-redesign.png" class="w-full" style="max-height:200px; object-fit:contain" />

</div>
<div>

<img src="/images/line-chart-good-after-redesign.png" class="w-full" style="max-height:200px; object-fit:contain" />

</div>
</div>

---
layout: center
---

# Leverage white space

> Don't fear white space.

---

# Gestalt theory: similarity

<img src="/images/gestalt-similarity.png" class="w-full mt-2" style="max-height:360px; object-fit:contain" />
---

# Gestalt theory: proximity

<img src="/images/gestalt-proximity.png" class="w-full mt-2" style="max-height:360px; object-fit:contain" />
---
layout: one-col-footer
---

# There are many preattentive attributes

<img src="/images/preattentive-attributes-examples.png" class="w-full mt-2" style="max-height:360px; object-fit:contain" />

::footer::
Source: http://www.storytellingwithdata.com/book/downloads 

---

# But two are special
<br />

<span class="text-2xl font-bold">Size</span>  matters.

- If items are equally important, size them similarly.
- If one item is critical, make it *BIG*.

<span class="font-bold text-blue-600">Color</span> is the most powerful tool you have.

- Use it sparingly.
- Resist using color just to be colorful.
- Use color selectively to highlight what matters.

---
layout: two-cols-footer
---

# Colors

::left::
Think about:

- Color blindness
- Black & white reproduction
- Choosing the right palette

Use:

- Categories -> hue
- Magnitudes -> saturation / value

::right::

<img src="/images/colorblind-ishihara-test.jpeg" class="w-full mt-3" style="max-height:360px; object-fit:contain"/>

::footer::
Tip: [colorbrewer2.org](https://colorbrewer2.org)

---
layout: quote
---

Maximise data-ink ratio, within reason.

::author::
Edward Tufte, *The Visual Display of Quantitative Information*

---

# The moiré effect

<img src="/images/moire-hatched-bars-chartjunk.png" class="w-full mt-3" style="max-height:360px; object-fit:contain" />

---
layout: quote
---

Forgo chartjunk, including moire vibration, the grid, and the duck.

::author::
Edward Tufte, *The Visual Display of Quantitative Information*

---

# Rules of thumb

No unjustified 3D


<div class="grid grid-cols-2 gap-6 mt-4">
<div>

<img src="/images/pie-chart-3d-ugly.png" class="mx-auto mt-4" style="max-height:240px; object-fit:contain" />
</div>
<div>
<img src="/images/bad-chart-example.jpg" class="mx-auto mt-4" style="max-height:240px; object-fit:contain" />
</div>
</div>

---
layout: center
class: text-center
---

# Remember

<div class="font-mono text-2xl tracking-widest leading-loose mt-8">

756<span class="text-red-400 font-bold">3</span>9506847<span class="text-red-400 font-bold">3</span>

65866<span class="text-red-400 font-bold">3</span>0<span class="text-red-400 font-bold">3</span>7576

860<span class="text-red-400 font-bold">3</span>72658602

8465891078<span class="text-red-400 font-bold">3</span>0

</div>

---
layout: quote
---

Don't let your design choices be happenstance. They should be the result of explicit decisions.

---
layout: image-right
image: /images/eiffel-photo-sunny.jpeg
class: flex flex-col justify-center
---

<p class="text-gray-400 text-sm font-mono mb-2">Step 4 / 4</p>

# Close the loop


---
layout: two-cols-header
---

# Show rigor

::left::

<div class="flex flex-col justify-center h-full">

- Check the data
- Label axes
- Include units

</div>

::right::

<img src="/images/label-axes.jpg" class="w-full" style="max-height:340px; object-fit:cover" />


# Be honest

::left::

<div class="flex flex-col justify-center h-full">

- Check the lie factor, keep your geometry in check
- Include your sources
- Include a baseline

</div>

::right::

<img src="/images/label-axes.jpg" class="w-full" style="max-height:340px; object-fit:cover" />


---
layout: two-cols-footer
---

# Overview first, Zoom and Filter, Details on demand

::left::
<img src="/images/zoom-filter.png" class="w-full mt-2" style="max-height:360px; object-fit:contain" />

::right::
"The click-through solution"

- Start with a visually grabby graphic (Infovis) or a simple graph (stats)
- Click and get a suite of statistical graphs showing more details
- Click again to get a spreadsheet with all the numbers and a list of sources.

::footer::
From http://andrewgelman.com/2015/08/26/vizzy-vizzy-vizzy-viz/

---

# Function first, form next.


<img src="/images/duck-building-venturi-form-function.jpg" class="w-full mt-2" style="max-height:360px; object-fit:contain" />

<!--
The duck: when the architect went too far and forgot the windows.
-->

---


# A wealth of resources: links

- [awesome-dataviz](https://github.com/hal9ai/awesome-dataviz)
- [flowingdata.com](https://flowingdata.com)
- [colorbrewer2.org](https://colorbrewer2.org)
- [viz.wtf](https://viz.wtf)
- [nytimes.com/section/upshot](https://www.nytimes.com/section/upshot)
- [informationisbeautiful.net](https://informationisbeautiful.net/)

---
layout: two-cols-header
---

# A wealth of resources: books

::left::

<img src="/images/books-desk-stack-dataviz.jpeg" class="w-full" style="max-height:340px; object-fit:cover" />

::right::


- *How to Lie with Statistics*, Huff, 1954
- *The Visual Display of Quantitative Information*, Tufte, 2001
- *Show Me the Numbers*, Few, 2012
- *The Wall Street Journal Guide to Information Graphics: The Dos and Don'ts of Presenting Data, Facts, and Figures*, Dona M. Wong. W. W. Norton & Company, 2013.
- *Visualization Analysis and Design*, Munzner, 2014
- *Storytelling with Data: A Data Visualization Guide for Business Professionals*, Knaflic, 2015  

---

# A wealth of resources: papers


- Cleveland, William S., and Robert McGill. "Graphical perception: Theory, experimentation, and application to the development of graphical methods." Journal of the American statistical association 79.387 (1984): 531-554.  
- Gelman, Andrew, and Antony Unwin. "Infovis and statistical graphics: different goals, different looks." Journal of Computational and Graphical Statistics 22.1 (2013): 2-28
- [Datasaurus] Matejka, J., & Fitzmaurice, G. (2017, May). Same stats, different graphs: generating datasets with varied appearance and identical statistics through simulated annealing. In Proceedings of the 2017 CHI conference on human factors in computing systems (pp. 1290-1294)

---

<div class="absolute inset-0 z-0">
  <img src="/images/practice-time.png" class="w-full h-full object-cover" />
  <div class="absolute inset-0" style="background: rgba(0,0,0,0.4)"></div>
</div>

<div class="relative z-10 flex flex-col items-center justify-center h-full text-black text-center" style="text-shadow: 0 1px 10px rgba(255, 255, 255, 0.9), 0 0 3px rgba(255, 255, 255, 1)">

# Time to practice!

</div>


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
