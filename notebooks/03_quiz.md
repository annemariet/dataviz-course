# Session 3 Quiz — Communication & Storytelling

**Duration**: 15 minutes &nbsp;|&nbsp; **Format**: Wooclap (or paper)  
**Tip**: discuss answers after each part — the explanations matter as much as the correct choice.

---

## Part A — Exploration vs. Explanation (Q1–Q4)

**Q1.** You are analysing a new dataset for the first time. Which chart approach is most appropriate?

- A. A single polished chart with a clear insight title
- B. A grid of small multiples showing many variables at once
- **C. A pairplot or faceted scatter matrix to search for patterns** ✓
- D. A pie chart of category proportions

> *Explanation*: During exploration you want to see everything quickly and let the data surprise you. Polished single charts are for communication, not discovery.

---

**Q2.** Gelman & Unwin (2013) describe two goals of data visualisation. Which pair best captures them?

- A. Static vs. interactive
- **B. Exploration (find patterns) vs. Explanation (communicate findings)** ✓
- C. Descriptive vs. predictive
- D. Simple vs. complex

---

**Q3.** You have found an interesting finding and want to present it to a non-technical audience. Which choice best follows the "explanation" mode?

- A. Show the full pairplot so they can explore themselves
- **B. One chart, one message, with a descriptive title stating the insight** ✓
- C. Export a raw CSV and let them query it
- D. Show the code that produced the result

---

**Q4.** Which of the following is a sign that a chart is still in "exploration" mode rather than "explanation" mode?

- A. It has a descriptive title like "Species A has larger flippers than Species B"
- B. It uses a single, consistent colour palette
- **C. It displays all variables simultaneously with no highlighted takeaway** ✓
- D. It has removed chart junk (grid lines, unnecessary borders)

---

## Part B — Choosing K & KMeans Visualisation (Q5–Q8)

**Q5.** The elbow curve plots inertia (within-cluster sum of squares) against the number of clusters K. What are you looking for?

- A. The K with the highest inertia
- B. The K where inertia reaches exactly zero
- **C. The K where the rate of decrease in inertia sharply slows down** ✓
- D. The K that maximises the number of data points per cluster

---

**Q6.** The silhouette score ranges from −1 to +1. Which statement is correct?

- A. A score near −1 means clusters are well-separated
- B. A score near 0 means every point is perfectly classified
- **C. A score near +1 means points are much closer to their own cluster than to neighbours** ✓
- D. Silhouette score cannot be used alongside the elbow method

---

**Q7.** You visualise KMeans clusters on a 2-D PCA scatter plot. The axis label should include:

- A. The cluster labels only
- **B. The percentage of variance explained by each principal component** ✓
- C. The raw feature names (bill_length_mm, flipper_length_mm, …)
- D. Nothing — axes are irrelevant for cluster plots

> *Explanation*: % variance explained tells the reader how much information is preserved in the 2-D projection. Without it, the viewer cannot judge how representative the plot is.

---

**Q8.** A cluster profile heatmap shows standardised mean feature values per cluster. Why standardise?

- A. To make all values positive
- B. To ensure all clusters have equal numbers of points
- **C. So that features measured on different scales (mm vs. g) can be compared fairly** ✓
- D. To speed up the KMeans algorithm

---

## Part C — Storytelling Principles (Q9–Q12)

**Q9.** Cole Nussbaumer Knaflic's narrative arc has three acts. In the context of a data presentation, what does Act 2 ("Conflict / Rising action") typically contain?

- A. The dataset description and data cleaning steps
- B. The final recommendation
- **C. The evidence and analytical steps that reveal the problem or insight** ✓
- D. The thank-you slide

---

**Q10.** Gelman's "click-through" solution recommends presenting data in what order?

- **A. Overview → Statistical detail → Raw data** ✓
- B. Raw data → Statistical detail → Overview
- C. Hypothesis → Raw data → Conclusion
- D. Introduction → Methods → Results → Discussion

---

**Q11.** Which of the following best illustrates the "one chart, one message" principle?

- A. A dashboard with 12 KPIs visible simultaneously
- B. A table showing all numerical columns of the dataset
- **C. A scatter plot titled "Gentoo penguins have markedly longer flippers than other species"** ✓
- D. An interactive chart where the user can choose any two variables

---

**Q12.** *(Spaced repetition — Sessions 1 & 2)*  
According to Cleveland & McGill's perceptual accuracy ranking, which visual channel allows the most accurate quantitative comparisons?

- **A. Position along a common scale** ✓
- B. Colour hue
- C. Area
- D. Angle / slope

> *Explanation*: Cleveland & McGill (1984) ranked perceptual tasks from most to least accurate: position on a common scale > position on non-aligned scales > length > angle > area > colour saturation > colour hue. This is why bar charts beat pie charts for comparing quantities.

---

*End of quiz. Total: 12 questions × ~75 seconds ≈ 15 minutes.*
