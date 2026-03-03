# P-values | Week 03 Homework assignment

This assignment builds on the permutation test from the in-class activity and
asks you to explore two additional ideas: how the properties of your data
determine the p-value you get, and how p-hacking works in practice.

Download the [R notebook](./03-pvalues_homework_student.Rmd) or
[Python notebook](./03-pvalues_homework_student.ipynb), annotate the code,
run it, and answer the questions embedded in the notebook as well as the
questions below. Submit your completed notebook as a PDF using
[this form](https://forms.gle/977e4vrVshwTyTcK7).

---

### Reflecting on the in-class permutation test

1. In your own words, write a general definition of a p-value — one that
   is not tied to any specific test or dataset.

2. The permutation test and the Welch t-test gave similar p-values. Now
   suppose the data contained one very large outlier in group 2. Which method
   would you trust more, and why?

---

### Part 2 — Effect of effect size, variance, and sample size

3. Look at the three-panel figure you produced. Describe the "boundary"
   between significant (red) and non-significant (blue) points. How does
   that boundary shift as you move from the left panel (SD = 0.5) to the
   right panel (SD = 2)?

4. A researcher runs a study and gets p = 0.06. They argue that with a
   larger sample size the result would surely become significant, and
   therefore the effect is real. Is this reasoning valid? Use what you
   observed in Part 2 to support your answer.

---

### Part 3 — P-hacking

5. The simulation in Part 3 always finds p < 0.05 eventually, even though
   the data come from a single population with no real group difference.
   How many attempts did it take in your run? What does this tell you about
   the 0.05 threshold when testing is repeated?

6. Describe one real-world practice in data analysis or experimental design
   that is structurally equivalent to what the while-loop in Part 3 is doing.
   Explain the analogy clearly.
