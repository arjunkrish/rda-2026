# ─────────────────────────────────────────────────────────────────────────────
# Assignment 08 — In-class: Simulating the Null Distribution of Pearson r
#                           at a Fixed Sample Size
#
# Work through this script with a partner: discuss each step, add your own
# comments, run the code, and answer the questions at the end.
# ─────────────────────────────────────────────────────────────────────────────

import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

# np.random.default_rng() creates a reproducible random-number generator.
# The seed fixes the sequence so every machine gets identical draws.
rng = np.random.default_rng(seed=42)


# ── Parameters ────────────────────────────────────────────────────────────────

n_obs = 10      # sample size: how many (x, y) observations per pair
n_sim = 10000   # number of random pairs to simulate


# ── Step 1: Simulate the null distribution of Pearson r ──────────────────────

null_r = np.array([
    stats.pearsonr(rng.uniform(size=n_obs),
                   rng.uniform(size=n_obs)).statistic
    for _ in range(n_sim)
])

print(f"Null r  (n = {n_obs}, {n_sim} simulations):")
print(f"  Mean : {np.mean(null_r):+.4f}   (should be ≈ 0 — no true correlation)")
print(f"  SD   :  {np.std(null_r, ddof=1):.4f}")
print(f"  Range: [{np.min(null_r):.3f}, {np.max(null_r):.3f}]\n")

# [ Add your notes here. ]


# ── Step 2: Identify the significance threshold ───────────────────────────────

r_crit = float(np.quantile(null_r, 0.95))

print(f"One-tailed critical r at n = {n_obs} (α = 0.05): r_crit = {r_crit:.3f}")
print(f"Fraction of null r values that exceed r_crit: {np.mean(null_r > r_crit):.3f}\n")

# [ Add your notes here. ]


# ── Step 3: Visualise the null distribution ───────────────────────────────────

fig, ax = plt.subplots(figsize=(7, 4))

ax.hist(null_r, bins=50, color="steelblue", edgecolor="white", alpha=0.8)
ax.axvline(r_crit, color="black", linewidth=1.5)
ax.text(r_crit + 0.03, ax.get_ylim()[1] * 0.97,
        f"r = {r_crit:.3f}\n(95th percentile)",
        va="top", ha="left", fontsize=9)
ax.set_xlabel("Pearson r", fontsize=12)
ax.set_ylabel("Count", fontsize=12)
ax.set_title(
    f"Null distribution of Pearson r  |  n = {n_obs}  |  {n_sim} simulations\n"
    "x and y are independent Uniform(0,1) — no true correlation exists",
    fontsize=11
)
ax.grid(True, linestyle="--", alpha=0.4)
fig.tight_layout()
fig.savefig("08-inclass-null-r-n10.pdf")
plt.show()

# [ Add your notes here. ]


# ── Discussion questions ──────────────────────────────────────────────────────

# Question 1:
# What is the critical r you found at n = 10? Is it larger or smaller than you
# expected before running the simulation? What does the width of the histogram
# tell you about the reliability of a single correlation from a small study?
#
# [ Write your answer here. ]


# Question 2:
# The simulation used rng.uniform() draws for both x and y. Replace uniform()
# with normal() or exponential() and re-run. Does r_crit change? Explain why
# or why not.
#
# [ Write your answer here. ]


# Question 3:
# A colleague reports r = 0.45, n = 10 and claims a "statistically significant
# positive correlation." Based on your null distribution, is this claim
# justified? What exactly would you tell them?
#
# [ Write your answer here. ]
