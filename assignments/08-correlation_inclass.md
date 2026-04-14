# Correlation coefficients | Week 08 In-class assignment

This assignment is designed to help you understand what makes a correlation
coefficient "statistically significant," and how much a Pearson r can vary
purely by chance when no true relationship exists.

This prewritten script illustrates one core approach:

* **Part 1** — Simulate the null distribution of Pearson r at a fixed sample
  size of n = 10: draw 10,000 pairs of completely independent variables,
  compute r for each, and identify the 95th-percentile critical value. Then
  examine how wide this distribution is, and what it means for interpreting
  a "significant" correlation in a small study.

Here's what to do:

1. Download the [R script](./08-correlation_inclass.R) or
   [Python script](./08-correlation_inclass.py)
2. Load it into your favorite IDE
3. Work with a partner to go through the code step by step, discuss the
   logic in detail, and add detailed comments along the way
4. Run the code and discuss the output and the questions embedded at the end
