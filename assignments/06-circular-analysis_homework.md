# Circular Analysis and Sampling Bias | Week 06 Homework assignment

This assignment extends the in-class introduction to circular analysis (double-dipping)
and sampling bias. You will work through four coding exercises that each isolate a
distinct mechanism by which an analysis pipeline can produce misleading results even
when no real effect exists: clustering and testing on the same data, inheriting
inflated group structure through label propagation, labeling by proximity to
arbitrary reference points, and comparing extreme values across populations of
unequal size.

Download the [R script](./06-circular-analysis_homework.R) or
[Python script](./06-circular-analysis_homework.py), annotate the code,
run it, and answer the questions embedded in the script as well as the
questions below. Submit your completed script as a PDF using
[this form](https://forms.gle/977e4vrVshwTyTcK7).

---

### Exercise 1 — Circular analysis: cluster-then-test on the same data

1. Look at the p-values and effect sizes your script produced. Are they what
   you would expect if the null hypothesis (no group differences) were true?
   What do these results tell you — and what do they *not* tell you — about
   the data?

2. K-means minimises within-cluster sum of squares. Explain in your own words
   why that objective makes the subsequent t-test circular. What would a valid
   test of group differences require that this pipeline does not provide?

---

### Exercise 2 — Circular analysis: a partial fix via data splitting

3. Compare the p-values from Exercise 2 (data splitting) with those from
   Exercise 1 (no split). Are they qualitatively different? Does data
   splitting appear to eliminate significance inflation? What does this suggest
   about treating data splitting as a universal safeguard against circular
   analysis?

4. The k-NN classifier assigns test-set labels by spatial proximity to
   training points. In what sense is this still a form of double-dipping, even
   though the exact same rows are not reused? What property of a labeling rule
   makes a subsequent hypothesis test circular, regardless of whether the data
   are split?

---

### Exercise 3 — Circular analysis: the Voronoi / proximity-labeling variant

5. The Voronoi boundary in Exercise 3 is the y-axis (the perpendicular
   bisector of segment AB). How does the orientation of AB relative to the
   tested variable *x* affect the magnitude of the resulting p-value? Predict
   what would happen — and why — if you rotated AB to lie along the y-axis
   instead (e.g., `ref_A = (0, −1)`, `ref_B = (0, 1)`). Test your prediction
   by modifying the script.

6. In Exercise 2, labels were propagated by k-NN proximity. In Exercise 3,
   labels are assigned by proximity to two fixed reference points. Identify the
   shared flaw in these two procedures. State in general terms: what property
   of a labeling rule makes a subsequent hypothesis test circular?

---

### Exercise 4 — Sampling bias: outliers and population size

7. The log-normal curve starts lower than both the normal and exponential
   curves at small population sizes. Explain why, in terms of the tail
   behaviour of each distribution. Your answer should reference the
   approximate growth formulas discussed in the script comments
   (√(2 ln *n*) for the normal, ln *n* for the exponential,
   exp(σ √(2 ln *n*)) for the log-normal).

8. World athletics records are maintained separately for each age group
   (under-20, open, masters). Suppose a journalist reports that a 35-year-old
   holds a better marathon record than any under-20 athlete ever has. Using
   the intuition from Exercise 4, what question would you ask before accepting
   that conclusion, and what additional analysis would you propose?

9. Rare genetic variants are far more likely to be discovered in large
   biobanks (*n* ~ 500,000) than in small cohort studies (*n* ~ 500). How
   does the sampling-bias argument from Exercise 4 apply to interpreting
   effect-size estimates for variants initially discovered in large vs. small
   studies? (*Hint:* think about which variants a small study can detect and
   how that selection shapes the distribution of reported effect sizes.)
