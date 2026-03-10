# Statistical power | Week 04 In-class assignment

This assignment is designed to help you build an intuitive, simulation-based
understanding of statistical power — the probability that your test correctly
detects a real effect when one exists.

The prewritten script implements a coin-flip experiment to detect biased coins,
building up to a power curve that shows how detectable an effect is across a
range of bias strengths:

* **Step 1** — Build the null distribution by simulating 10,000 fair-coin experiments
* **Step 2** — Run one experiment with a biased coin and compute a p-value
* **Step 3** — Estimate power by repeating the experiment 1,000 times
* **Step 4** — Sweep across all coin biases to generate a power curve

Here's what to do:

1. Download the [R script](./04-power_inclass_student.R) or [Python script](./04-power_inclass_student.py)
2. Load it into your favorite IDE
3. Work with a partner to go through the code, discuss the logic in detail, and add detailed comments along the way
4. Run the code step-by-step and discuss the results at each stage
5. Answer the two questions at the end of the script
