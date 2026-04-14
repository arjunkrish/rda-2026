# Correlation coefficients | Week 08 Homework assignment

This assignment extends the in-class simulation to ask how sample size shapes
the null distribution of Pearson r and what that means for interpreting
reported correlations.

Download the [R script](./08-correlation_homework.R) or
[Python script](./08-correlation_homework.py), annotate the code,
run it, and answer the questions below. Write your answers directly in the
script as comments, export as a PDF, and submit using
[this form](https://forms.gle/977e4vrVshwTyTcK7).

---

1. Describe how the shape of the null distribution changes as n increases.
   Comment on both the width (spread) and the symmetry across the five panels.

2. Report the critical r at n = 5 and n = 100. What does the difference imply
   for interpreting r = 0.35 from a study with n = 20 versus r = 0.10 from a
   study with n = 500? Which finding is more likely to be "statistically
   significant"? Which is more likely to matter practically?

3. With very large n (e.g., n = 10,000), virtually any non-zero r would be
   "statistically significant." What should a researcher report alongside a
   p-value to convey whether a significant correlation is practically
   meaningful?

4. The dashed theory curve (1.645 / √(n − 1)) tracks the simulation well at
   large n but diverges slightly at n = 5. Why might the approximation be less
   accurate at very small sample sizes?

5. Extend the code in Step 2 to also compute the 2.5th percentile (the
   lower-tail critical value). Add both the upper and lower critical values as
   vertical lines in the Step 3 plot. What is the two-tailed critical |r| at
   n = 10, and how does it compare to the one-tailed value?
