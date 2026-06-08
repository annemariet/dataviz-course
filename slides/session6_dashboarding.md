---
theme: seriph
title: "Session 6: Dashboards, AI-assisted BI, Ethics"
info: |
  Session 6: PSL Master IASD · June 2026
  Anne-Marie Tousch
highlighter: shiki
lineNumbers: false
drawings:
  persist: false
transition: slide-left
mdc: true
colorSchema: light
showSlideNumber: true
---

<!--
SLIDE-AUTHORING NOTES (delete before class):
- One point per slide. Short title + short body + one image.
- New images live in slides/public/images/. Reuse existing assets where possible
  (datasaurus-dozen, books-desk-stack, portrait-andrew-gelman, gestalt-*).
- TODO comments mark images Anne-Marie still needs to source.
- File name matches the eventual destination in the public repo:
  dataviz-course/slides/session6_dashboarding.md. See ../README.md
  "Slides" section for the local preview workflow (short version:
  copy in, add per-deck npm script, npm run dev:s6).
- DO NOT push this file (or anything else in session6/) to the
  dataviz-course public repo until the session has been reviewed and
  validated. That includes the slides: they ship together with the
  rest of the material once signed off.
-->

<!-- TODO image: a dashboard/control-room photo, ideally a real BI dashboard
     screenshot or a Bloomberg-style trading floor. /images/hero-dashboard.jpeg -->
<div class="absolute inset-0 z-0">
  <img src="/images/hero-dashboard.jpeg" class="w-full h-full object-cover" />
  <div class="absolute inset-0" style="background: rgba(0,0,0,0.35)"></div>
</div>

<div class="relative z-10 flex flex-col items-center justify-center h-full text-white text-center" style="text-shadow: 0 1px 10px rgba(0,0,0,0.9), 0 0 3px rgba(0,0,0,1)">

# Dashboards, AI-assisted BI, Ethics

## Session 6: assembling the tools you've built

Anne-Marie Tousch · PSL Master IASD · 8 June 2026

</div>


---
layout: image-right
image: /images/eiffel-from-below-structural.jpeg
class: flex flex-col justify-center
---

# Where we are

You've learned to **build** charts (S1–S2),
to **explore** large datasets (S3), to **debug** ML (S4),
and to **see** high-dimensional data (S5).

Today: 
- How to **assemble** them into a tool for someone else,
- More tips to make sure your charts don't lie.


---
layout: image-right
image: /images/eiffel-engineering-blueprints-1887.jpeg
class: flex flex-col justify-center
---

<p class="text-gray-400 text-sm font-mono mb-2">Section 1 / 5</p>

# What is a dashboard?


---
layout: quote
---

A visual display of the most important information needed to achieve one or more objectives,
consolidated and arranged on a single screen so the information can be monitored at a glance.

::author::
Stephen Few, *Dashboard Confusion Revisited* (2007)
[PDF](http://perceptualedge.com/articles/visual_business_intelligence/dboard_confusion_revisited.pdf)


---
layout: center
class: text-left max-w-3xl mx-auto
---

# Three kinds of dashboards

Stephen Few (2006) groups dashboards by **who** monitors them and **how often**.

Each type uses a different time budget, chart vocabulary, and failure mode.

<p class="text-gray-500 text-sm mt-8">Few, <em>Information Dashboard Design</em> (2nd ed., 2013), Chapter 2: "Variations in Dashboard Uses and Data"</p>


---
layout: two-cols-footer
---

# Strategic dashboards

::left::

<img src="/images/dashboard-strategic.png" class="w-full" style="max-height:340px; object-fit:contain" />

::right::

**Audience:** executives  
**Cadence:** weekly to monthly

High-level KPIs vs targets and prior periods.



---
layout: two-cols-footer
---

# Analytical dashboards

::left::

<img src="/images/dashboard-analytical.png" class="w-full" style="max-height:340px; object-fit:contain" />

::right::

**User seat:** analyst / power user  
**Cadence:** on demand

You still **build for someone else**. Their job is to filter, drill down, and compare segments.

At Open Food Facts: a volunteer contributor checking coverage and data quality, not you in a notebook.



---
layout: two-cols-footer
---

# Operational dashboards

::left::

<img src="/images/dashboard-operational.png" class="w-full" style="max-height:340px; object-fit:contain" />

::right::

**Audience:** ops / on-call  
**Cadence:** real-time

What's broken right now? Alerts and status, not exploration.


---
layout: two-cols-footer
---

# Modern references on dashboards

::left::

<img src="/images/bach-design-patterns-site.png" class="w-full" style="max-height:340px; object-fit:contain" />

::right::

**Bach et al. (2023). "Dashboard Design Patterns." IEEE TVCG.**

- Survey of 144 real-world dashboards
- 8 design-pattern groups
- [Process & guidelines](https://dashboarddesignpatterns.github.io/processguidelines.html) (audience, tasks, staged workflow)

::footer::

[dashboarddesignpatterns.github.io](https://dashboarddesignpatterns.github.io/) · [open arXiv](https://arxiv.org/abs/2205.00757)


---
layout: two-cols-footer
---

# Modern practitioner standard

::left::

<img src="/images/bigbook-dashboards-cover.png" class="mx-auto" style="max-height:340px; object-fit:contain" />

::right::

**Wexler, Shaffer & Cotgreave (2017).
*The Big Book of Dashboards.*** Wiley.

~30 real-world case studies. Tableau dashboards from the book freely available.

::footer::

[bigbookofdashboards.com](https://www.bigbookofdashboards.com/) · [SWD review](https://www.storytellingwithdata.com/blog/2017/8/9/recommended-reading-the-big-book-of-dashboards)


---
layout: image-right
image: /images/eiffel-hand-forced-perspective.jpeg
class: flex flex-col justify-center
---

<p class="text-gray-400 text-sm font-mono mb-2">Section 2 / 5</p>

# Think first: what would an Open Food Facts team monitor?


---
layout: center
---

Let's think of (around?) 5 metrics for your dashboard

<br/>

Wooclap · code **LJIETBD**


---
layout: image-right
image: /images/eiffel-cail-inscription-detail.jpeg
class: flex flex-col justify-center
---

<p class="text-gray-400 text-sm font-mono mb-2">Section 3 / 5</p>

# Course-correct with design rules


---
layout: two-cols-footer
---

# Few lists 13 common pitfalls

::left::

<!-- TODO cover of Information Dashboard Design 2nd ed,
     /images/few-idd-cover.jpg -->
<img src="/images/few-idd-cover.jpg" class="mx-auto" style="max-height:240px; object-fit:contain" />

::right::

*Information Dashboard Design* (2nd ed., 2013) Chapter 3.

We will only cover 5 in this presentation.

::footer::

Free abridgement: ["Common Pitfalls in Dashboard Design" (PDF)](https://www.perceptualedge.com/articles/Whitepapers/Common_Pitfalls.pdf)


---
layout: two-cols-footer
---

# #1: Exceeding the boundaries of a single screen

::left::

<!-- Datadog high-density dashboard scroll demo -->
<video
  src="https://web-assets.dd-static.net/42588/1776293806-datadog-dashboards-high-density-mode-compressed.mp4"
  class="w-full rounded"
  style="max-height:340px; object-fit:contain"
  controls
  loop
  muted
  playsinline
/>

::right::

Few: a dashboard that scrolls is a report.

Wexler et al. (2017): on **desktop**, still aim for one screen. On **phone**, a layout **designed to scroll** (tall, single column) can work, not a desktop view squeezed onto a small screen.


---
layout: two-cols-footer
---

# #2: Inadequate context for the data

::left::

<!-- Generated mock: one KPI, no comparison baseline -->
<img src="/images/kpi-tile-no-context.png" class="w-full" style="max-height:340px; object-fit:contain" />

::right::

> *A number without a comparison is uninterpretable.*

Always show: vs. target, vs. prior period, vs. peer baseline.


---
layout: two-cols-footer
---

# #3: Excessive detail or precision

::left::

<!-- Generated mock: same metric, too many decimals -->
<img src="/images/excessive-precision-tile.png" class="w-full" style="max-height:340px; object-fit:contain" />

::right::

5-second glance medium. Six decimal places is noise.

Show "12%" + the comparison interval.


---
layout: two-cols-footer
---

# #9: Arranging the data poorly

::left::

<!-- Generated mock: logo in prime real estate, related metrics split apart -->
<img src="/images/dashboard-poor-arrangement.png" class="w-full" style="max-height:340px; object-fit:contain" />

::right::

Few: placement should follow **importance** and **use**, not whatever fits.

Top-left is prime real estate: don't waste it on logo or nav.

Metrics you compare should sit **together**; otherwise the layout fights the task.

::footer::

Few, pitfall #9 · [Common Pitfalls (PDF)](https://www.perceptualedge.com/articles/Whitepapers/Common_Pitfalls.pdf)


---
layout: two-cols-footer
---

# #11: Cluttering the screen with useless decoration

::left::

<!-- Gauge / speedometer-style widget (Few pitfall #11) -->
<img src="/images/dashboard-gauges-bad.png" class="w-full" style="max-height:340px; object-fit:contain" />

::right::

Faux control panels, LED-style meters, 3D bevels: decoration the viewer must process before the data.

A plain number + delta carries more information per pixel.

::footer::

Few, pitfall #11 · [Common Pitfalls (PDF)](https://www.perceptualedge.com/articles/Whitepapers/Common_Pitfalls.pdf)


---
layout: two-cols-footer
---

# Positive complement: design patterns to reach for

::left::

<!-- Bach et al. pattern groups + process guidelines screenshot -->
<img src="/images/dashboard-design-patterns-compact.png" class="w-full" style="max-height:340px; object-fit:contain" />

::right::

144-dashboard survey · 8 pattern groups · **staged design process** + 20 guidelines.

Use Bach et al. *with* Few: pitfalls to avoid; [process & guidelines](https://dashboarddesignpatterns.github.io/processguidelines.html) for what to reach for.

::footer::

[Pattern catalogue](https://dashboarddesignpatterns.github.io/) · [Process & guidelines](https://dashboarddesignpatterns.github.io/processguidelines.html)


---
layout: image-right
image: /images/eiffel-under-construction-1888.jpeg
class: flex flex-col justify-center
---

<p class="text-gray-400 text-sm font-mono mb-2">Section 4 / 5</p>

# Ethics: six examples


---
layout: two-cols-footer
---

# 1: Graphical integrity

::left::

<img src="/images/truncated-baseline.png" class="w-full" style="max-height:340px; object-fit:contain" />

::right::

> The numbers on the chart should be proportional to the quantities they represent.

The classical baseline.

::footer::

Tufte, *The Visual Display of Quantitative Information* (1983) Ch. 2 · [edwardtufte.com](https://www.edwardtufte.com/book/the-visual-display-of-quantitative-information/)
See also: [6.2 Misleading Axes from Calling BS](https://www.youtube.com/watch?v=9pNWVMxaFuM)


---
layout: two-cols-footer
---

# 2: Selective disclosure

::left::

<img src="/images/aggregate-hides-disparity.png" class="w-full" style="max-height:340px; object-fit:contain" />

::right::

Each chart can be technically honest.
The *selection* tells a different story.

Headline aggregate (55): disaggregate and Group A is 40, Group B is 70.

A dashboard's **first screen is its message**.

<div class="flex items-center gap-3 mb-3">
<img src="/images/portrait-alberto-cairo.jpg" class="rounded-full" style="height:48px; width:48px; object-fit:cover" />
<span class="text-sm text-gray-500">Alberto Cairo</span>
</div>

::footer::

Cairo, *How Charts Lie* (2019) · [Norton](https://wwnorton.com/books/9781324001560) · [Datawrapper book club](https://www.datawrapper.de/blog/datavis-bookclub-alberto-cairo-how-charts-lie)


---
layout: two-cols-footer
---

# 3: Misleading arrangement

*Design obscurity*

::left::

<img src="/images/georgia-covid-reordered-axis.png" class="w-full" style="max-height:340px; object-fit:contain" />

::right::

The values can be real.
**Axis and category order** invent the story anyway.

Georgia DPH, May 2020: dates on the x-axis out of chronological order, so bars always trend "down."

Cairo's **design obscurity**: misleading *arrangement*, not selective disclosure.

::footer::

Georgia DPH COVID dashboard, May 2020 (dates out of chronological order) · chart via [Route Fifty](https://www.route-fifty.com/management/2020/05/officials-apologize-retool-coronavirus-graph-after-backlash/165478/) · also [AJC](https://www.ajc.com/news/state--regional-govt--politics/just-cuckoo-state-latest-data-mishap-causes-critics-cry-foul/182PpUvUX9XEF8vO11NVGO/) · [Atlanta Magazine](https://www.atlantamagazine.com/great-reads/behind-georgias-covid-19-dashboard-disaster/)

<div class="flex items-center gap-3 mb-3">
<img src="/images/portrait-alberto-cairo.jpg" class="rounded-full" style="height:48px; width:48px; object-fit:cover" />
<span class="text-sm text-gray-500">Alberto Cairo</span>
</div>

Cairo, *How Charts Lie* (2019) · [Norton](https://wwnorton.com/books/9781324001560) · [Datawrapper book club](https://www.datawrapper.de/blog/datavis-bookclub-alberto-cairo-how-charts-lie)


---
layout: two-cols-footer
---

# 4: Empirically measured deception

::left::

<img src="/images/pandey-deception-effects.png" class="w-full" style="max-height:340px; object-fit:contain" />

<p class="text-xs text-gray-400 mt-1">Pandey et al., CHI 2015, Figure 8</p>

::right::

"Is axis truncation really that bad?" → has an experimental answer.

Controlled studies of 4 common distortion techniques.

::footer::

Pandey et al. (2015), "How Deceptive Are Deceptive Visualizations?" *CHI* · [PDF (RPI mirror)](http://www.cs.rpi.edu/~cutler/classes/visualization/S24/papers/2015_Pandey_Deceptive_Visualization.pdf) · [ACM DOI](https://doi.org/10.1145/2702123.2702608)


---
layout: two-cols-footer
---

# 5: Who gets counted

::left::

<!-- Calling Bullshit case study: genre vs age at death (right-censoring confound) -->
<img src="/images/musician_mortality.jpg" class="w-full" style="max-height:340px; object-fit:contain" />

::right::

<!-- <div class="flex items-center gap-3 mb-3">
TODO portraits of Catherine D'Ignazio and Lauren Klein, head-shots circa
     the Data Feminism launch. /images/portrait-dignazio.jpg,
     /images/portrait-klein.jpg -->
<!-- <img src="/images/portrait-dignazio.jpg" class="rounded-full" style="height:48px; width:48px; object-fit:cover" />
<img src="/images/portrait-klein.jpg" class="rounded-full" style="height:48px; width:48px; object-fit:cover" />
<span class="text-sm text-gray-500">D'Ignazio & Klein</span>
</div> -->

The chart inherits the biases of the data, the schema, and the contribution pipeline.

Who contributes to Open Food Facts? Volunteers, OECD, smartphones, supermarkets.

::footer::

Bergstrom & West, *Calling Bullshit* · [Case study: Musicians and mortality](https://callingbullshit.org/case_studies/case_study_musician_mortality.html)


---
layout: two-cols-footer
---

# 6: Algorithmic accountability

::left::

<!-- Calling Bullshit: Wu & Zhang criminality-from-faces (biased training data) -->
<img src="/images/criminals.png" class="w-full" style="max-height:340px; object-fit:contain" />

::right::

The models reproduce biases.

A "Criminals detector" actually is a smile detector.

::footer::

Example from Bergstrom & West: [Criminal machine learning](https://callingbullshit.org/case_studies/case_study_criminal_machine_learning.html). See also: [ProPublica *Machine Bias* (COMPAS)](https://www.propublica.org/article/machine-bias-risk-assessments-in-criminal-sentencing)


---
layout: quote
---

A careless reader of this chart would conclude ___, but the data actually says ___.

::author::
How do you read charts? Try this next time!


---
layout: image-right
image: /images/eiffel-delaunay-painting-1926.jpeg
class: flex flex-col justify-center
---

<p class="text-gray-400 text-sm font-mono mb-2">Section 5 / 5</p>

# Communicating statistics with clarity


---
layout: two-cols-footer
---

# The summary-statistic trap

::left::

<img src="/images/datasaurus-dozen-identical-stats.png" class="w-full" />

::right::

A KPI tile is a summary statistic.

Any single number hides a distribution.

Datasaurus & Anscombe: same lesson, applied to the dashboard.

::footer::

Spiegelhalter, *The Art of Statistics* (Pelican 2019) · [Wilke Ch. 6](https://clauswilke.com/dataviz/histograms-density-plots.html)


---
layout: two-cols-footer
---

# Showing uncertainty

::left::

<!-- Wilke Ch. 16: confidence interval visualizations -->
<img src="/images/confidence-visualizations-1.png" class="w-full" style="max-height:340px; object-fit:contain" />

::right::

Most dashboards hide uncertainty.

**Wilke:** how to show it (intervals, bands, dotplots).

**Hullman:** authors still skip it, more because of the effort and fear of diluting the message than because readers can't learn to read it.

::footer::

Wilke (2019), [Ch. 16 *Visualizing uncertainty*](https://clauswilke.com/dataviz/visualizing-uncertainty.html) · Hullman (2019), ["Why Authors Don't Visualize Uncertainty"](https://users.eecs.northwestern.edu/~jhullman/Value_of_Uncertainty_Vis_CR.pdf)


---
layout: two-cols-footer
---

# Tools for uncertainty

::left::

<div class="grid grid-cols-2 gap-3">
  <div class="text-center">
    <img src="/images/uncertainty-error-bars-wiki.png" class="w-full" style="max-height:150px; object-fit:contain" />
    <p class="text-xs text-gray-400 mt-1">Error bars / CI</p>
  </div>
  <div class="text-center">
    <img src="/images/uncertainty-gradient-wiki.png" class="w-full" style="max-height:150px; object-fit:contain" />
    <p class="text-xs text-gray-400 mt-1">Gradient / envelope</p>
  </div>
  <div class="text-center">
    <img src="/images/uncertainty-quantile-dotplot-vega.png" class="w-full" style="max-height:150px; object-fit:contain" />
    <p class="text-xs text-gray-400 mt-1">Quantile dotplot</p>
  </div>
  <div class="text-center">
    <img src="/images/uncertainty-hops-plos.png" class="w-full" style="max-height:150px; object-fit:contain" />
    <p class="text-xs text-gray-400 mt-1">HOPs (frames)</p>
  </div>
</div>

::right::

- Error bars
- Gradient plots
- HOPs (Hypothetical Outcome Plots)
- Quantile dotplots · Kay's [`ggdist`](https://mjskay.github.io/ggdist/)

::footer::

Error bars: [Leonhard Bamberg](https://commons.wikimedia.org/wiki/File:95%25_confidence_interval.svg) (CC BY-SA 4.0) · Gradient ribbons: [Undermedia](https://commons.wikimedia.org/wiki/File:Opinion_polling_during_the_pre-campaign_period_of_2018_Quebec_general_election.svg) (CC BY-SA 4.0) · Quantile dotplot: [Vega example](https://vega.github.io/vega/examples/quantile-dot-plot/) (Kay et al. 2016) · HOPs: [Hullman et al. 2015, Fig. 2](https://doi.org/10.1371/journal.pone.0142444) (CC BY)


---
layout: two-cols-footer
---

# Discovering bias: survivorship

::left::

<!-- TODO: Wald WW2 bomber red-dot illustration,
     /images/wald-bomber-survivorship.png -->
<img src="/images/wald-bomber-survivorship.png" class="w-full" style="max-height:340px; object-fit:contain" />

::right::

The bombers that came back were hit *here*.

Where should we improve the armor?

::footer::

Abraham Wald, WW2. Retold in Ellenberg, *How Not to Be Wrong* (2014).


---
layout: two-cols-footer
---

# Spurious correlations

::left::

<!-- TODO: tylervigen.com classic example chart,
     /images/tylervigen-spurious-correlation.png -->
<img src="/images/tylervigen-spurious-correlation.png" class="w-full" style="max-height:340px; object-fit:contain" />

::right::

Two lines going up together is not evidence of causation.

::footer::

[tylervigen.com/spurious-correlations](https://www.tylervigen.com/spurious-correlations) · [Calling Bullshit case studies](https://www.callingbullshit.org/case_studies.html)


---
layout: two-cols-footer
---

# Simpson's paradox

::left::

<!-- UCBAdmissions data (Bickel et al. 1975); generated from R table -->
<img src="/images/simpsons-paradox-berkeley.png" class="w-full" style="max-height:340px; object-fit:contain" />

::right::

Aggregated: men admitted at a *higher* rate (45% vs 30%).

By department: rates are similar; women *higher* in A, B, D, F.

Lurking variable: women applied more to competitive departments (C–F).

::footer::

Bickel, Hammel & O'Connell (1975), [*Science*](https://doi.org/10.1126/science.187.4175.398) · [UCBAdmissions (R)](https://stat.ethz.ch/R-manual/R-devel/library/datasets/html/UCBAdmissions.html) · [Wikipedia table](https://en.wikipedia.org/wiki/Simpson%27s_paradox#UC_Berkeley_gender_bias)


---
layout: two-cols-footer
---

# Right censoring

::left::

<!-- TODO: Kaplan-Meier survival curve, /images/kaplan-meier-curve.png -->
<img src="/images/kaplan-meier-curve.png" class="w-full" style="max-height:340px; object-fit:contain" />

::right::

"Average time to event" usually means
*time to event among events that already happened*.

Ongoing cases are silently dropped.

Use a [Kaplan-Meier curve](https://en.wikipedia.org/wiki/Kaplan%E2%80%93Meier_estimator) · or at minimum a "% complete" denominator.


---
layout: two-cols-footer
---

# Risk communication

::left::

<!-- TODO: Gigerenzer's natural-frequency icon array: 1000 stick figures,
     8 highlighted (the breast-cancer / mammography example). Or a
     two-panel chart: left "0.8%" bar, right 10x100 icon array with 8 filled.
     Source: the Harding Center for Risk Literacy fact-box graphics. CC.
     /images/gigerenzer-natural-frequencies.png -->
<img src="/images/gigerenzer-natural-frequencies.webp" class="w-full" style="max-height:340px; object-fit:contain" />

::right::

**"0.8% prevalence"** is hard to read.

**"8 of 1000 people have it"** is easy.

Same data. Different comprehension.

::footer::

*Calculated Risks* (Simon & Schuster 2002) · [Max Planck Risk Literacy group](https://www.mpib-berlin.mpg.de/research/research-centers/adaptive-rationality) · [Harding Center fact-boxes](https://www.hardingcenter.de/en/transfer-and-impact/fact-boxes)


---
layout: two-cols-footer
---

# Absolute vs relative risk

::left::

<!-- TODO illustration: 1-in-a-million bar vs 2-in-a-million bar
     labelled "DOUBLES YOUR RISK", /images/absolute-vs-relative-risk.png -->
<img src="/images/absolute-vs-relative-risk.png" class="w-full" style="max-height:340px; object-fit:contain" />

::right::

"Doubles your risk" can mean
1-in-a-million → 2-in-a-million.

For lay audiences:
show **absolute numbers** + the **comparison**.


---
layout: two-cols-footer
---

# Multiple comparisons

::left::

<!-- TODO: the XKCD #882 "Significant" jelly-beans strip: the canonical
     popular illustration of multiple comparisons. xkcd CC-BY-NC 2.5,
     attribute. https://xkcd.com/882/. /images/xkcd-significant-jelly-beans.png -->
<img src="/images/xkcd-significant-jelly-beans.png" class="w-full" style="max-height:340px; object-fit:contain" />

::right::

<div class="flex items-center gap-3 mb-3">
<img src="/images/portrait-andrew-gelman.gif" class="rounded-full" style="height:48px; width:48px; object-fit:cover" />
<span class="text-sm text-gray-500">Andrew Gelman</span>
</div>

Every filter combination on an analytical dashboard is a silent hypothesis test.

3 filters × 10 levels = 1000 "comparisons": ~50 will look "significant" by chance at p < 0.05.

::footer::

Gelman & Loken (2013), ["The Garden of Forking Paths"](http://www.stat.columbia.edu/~gelman/research/unpublished/p_hacking.pdf) · open preprint · [xkcd #882](https://xkcd.com/882/)


---
layout: two-cols-footer
---

# Choropleths inherit *and amplify* all of this

::left::

<!-- Datawrapper Academy: discrete vs sensible bin breaks (US Southeast) -->
<img src="/images/choropleth-datawrapper-bin-choice.png" class="w-full" style="max-height:340px; object-fit:contain" />

::right::

- Map **rates**, not raw counts (population normalisation)
- **Bin choice** rewrites the story (left vs right above)
- Projection and area distort what readers see

::footer::

[What to consider when creating choropleth maps](https://www.datawrapper.de/academy/what-to-consider-when-creating-choropleth-maps) · [Choropleth maps (Academy index)](https://www.datawrapper.de/academy/category/choropleth-maps)


---
layout: two-cols-footer
---

# Time series: who chose the window?

::left::

<!-- Illustrative cherry-picking: same 52-week series, two cropped windows -->
<img src="/images/timeseries-window-choice.png" class="w-full" style="max-height:340px; object-fit:contain" />

::right::

**Cherry-picked windows**: same series, opposite headlines (above).

**Arbitrary baselines**: “since the pandemic” or YTD from a trough can make “recovery” look inevitable.

**Smoothing choices**: YoY and rolling averages can hide seasonality and recent turns.

::footer::

[Kelleher & Wagener (2011)](https://jcom.sissa.it/article/pubid/JCOM_2107_2022_A07/) · [ISVD: arbitrary time ranges](https://isvd.or.jp/en/columns/graph-literacy-five-checkpoints) · [Wilke, time series](https://clauswilke.com/dataviz/time-series.html) · [7-day rolling averages (COVID)](https://eclecticlight.co/2020/06/18/good-online-charts-can-confuse-not-clarify-covid-19-examples/)
---

# Open Food Facts ethics: 60-second mention

- **Contribution bias**: crowdsourced, volunteer, smartphone-mediated. Branded supermarket goods are over-represented.
- **Nutri-Score itself is political**: adopted by some EU governments, contested by parts of the food industry. A chart "by Nutri-Score" sits *inside that political frame*.
- **Provenance**: Open Food Facts is non-profit and licence-compatible. Your company data probably isn't. Always ask: what's the source, what's the licence, who's affected.

---
layout: image-right
image: /images/books-desk-stack-dataviz.jpeg
class: flex flex-col justify-center
---

# Going deeper


---

# Dashboards: modern references

- [Bach et al. (2023), "Dashboard Design Patterns"](https://arxiv.org/abs/2205.00757) · [patterns](https://dashboarddesignpatterns.github.io/) · [process & guidelines](https://dashboarddesignpatterns.github.io/processguidelines.html)
- [Sarikaya et al. (2019), "What Do We Talk About When We Talk About Dashboards?"](https://alper.datav.is/publications/dashboards/)
- Wexler, Shaffer & Cotgreave (2017), [*The Big Book of Dashboards*](https://www.bigbookofdashboards.com/)
- Kirk (2019), [*Data Visualisation*](https://www.visualisingdata.com/book/)
- Few · open whitepapers at [Perceptual Edge](http://www.perceptualedge.com/article-index.php)


---

# Ethics: read first

- *(free)* Bergstrom & West, **[Calling Bullshit](https://www.callingbullshit.org/)** · Week 6 = the data-viz module
- Cairo, *How Charts Lie* · [Datawrapper book club](https://www.datawrapper.de/blog/datavis-bookclub-alberto-cairo-how-charts-lie)
- *(free full text)* D'Ignazio & Klein, **[Data Feminism](https://data-feminism.mitpress.mit.edu/)** · Ch. 4 *What Gets Counted Counts*
- O'Neil · [11-min TED talk](https://www.ted.com/talks/cathy_o_neil_the_era_of_blind_faith_in_big_data_must_end) + [mathbabe.org](https://mathbabe.org/)
- Huff (1954), *How to Lie with Statistics* · train-ride classic


---

# Communicating statistics: read first

- Spiegelhalter (2019), [*The Art of Statistics*](https://www.penguin.co.uk/books/294857/the-art-of-statistics-by-spiegelhalter-david/9780241398630)
- *(free full text)* Wilke (2019), **[Fundamentals of Data Visualization](https://clauswilke.com/dataviz/)** · Ch. 16 on uncertainty
- Gigerenzer (2002), [*Calculated Risks*](https://www.simonandschuster.com/books/Calculated-Risks/Gerd-Gigerenzer/9780743254236) · risk communication
- Rosling (2018), [*Factfulness*](https://www.gapminder.org/factfulness-book/) · cognitive biases lay audiences bring
- Ellenberg (2014), [*How Not to Be Wrong*](https://www.penguinrandomhouse.com/books/312349/how-not-to-be-wrong-by-jordan-ellenberg/)


---

# Blogs, videos, storytelling...

- [callingbullshit.org](https://www.callingbullshit.org/) · I recommend the whole free course, not just the part on data visualization
- [dashboarddesignpatterns.github.io](https://dashboarddesignpatterns.github.io/)
- [tylervigen.com/spurious-correlations](https://www.tylervigen.com/spurious-correlations)
- [Junk Charts (Kaiser Fung)](https://junkcharts.typepad.com/) · daily chart critiques
- [Storytelling with Data](https://www.storytellingwithdata.com/) blog + [YouTube](https://www.youtube.com/c/storytellingwithdata)
- [The Pudding](https://pudding.cool/) · what the craft of storytelling looks like



---
layout: center
---

# Use data visualization to *think critically* about data

Developing your critical thinking is key:
- to call out misleading claims
- to avoid blindspots in your practice
- to present your own data truthfully

---
layout: image-right
image: /images/eiffel-lego-model.jpeg
class: flex flex-col justify-center
---

# Time to build


---
layout: one-col-footer
---

# Streamlit

```bash
uv sync --extra s6
uv run streamlit run \
    session6/streamlit_app.py
```

Scaffold: DuckDB + country filter + 2 KPI tiles + 1 chart.

Extend: heatmap + one KPI from Beat 1.

::footer::

[docs.streamlit.io](https://docs.streamlit.io/)


---
layout: one-col-footer
---

# After class (optional)

**Tableau Public** — no-code, self-paced: [`TABLEAU_SETUP.md`](TABLEAU_SETUP.md)

**Nao** — agentic BI walkthrough: [`NAO_DEMO.md`](NAO_DEMO.md)

Not covered live; same aggregate-first lesson as Streamlit.

::footer::

[public.tableau.com](https://public.tableau.com/)

