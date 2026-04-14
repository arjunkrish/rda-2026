# ─────────────────────────────────────────────────────────────────────────────
# Assignment 08 — Homework: How Does Sample Size Shape the Null Distribution
#                           of Correlation Coefficients?
#
# Work through this script on your own, add detailed comments at every step,
# and answer the questions at the end. Submit a PDF of your annotated script
# and answers via the course submission form.
# ─────────────────────────────────────────────────────────────────────────────

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from scipy import stats

rng = np.random.default_rng(seed=42)


# ── Parameters ────────────────────────────────────────────────────────────────

sample_sizes = [5, 10, 20, 50, 100]   # sample sizes to explore
n_sim        = 10000                   # simulations per sample size


# ── Step 1: Simulate null distributions for every sample size ─────────────────

print("Simulating null distributions:")
null_data = {}

for n in sample_sizes:
    print(f"  n = {n} ...")
    null_data[n] = np.array([
        stats.pearsonr(rng.uniform(size=n),
                       rng.uniform(size=n)).statistic
        for _ in range(n_sim)
    ])

print()


# ── Step 2: Compute the one-tailed 95th-percentile threshold for each n ───────

r_crits = {n: float(np.quantile(null_data[n], 0.95)) for n in sample_sizes}
r_sds   = {n: float(np.std(null_data[n], ddof=1))    for n in sample_sizes}

r_crits_theory = {n: 1.645 / np.sqrt(n - 1) for n in sample_sizes}

print("One-tailed critical r at each sample size:")
print(f"  {'n':>5}  {'r_crit':>8}  {'r_crit (theory)':>16}  {'SD(null r)':>10}")
for n in sample_sizes:
    print(f"  {n:>5}  {r_crits[n]:>8.4f}  {r_crits_theory[n]:>16.4f}"
          f"  {r_sds[n]:>10.4f}")
print()


# ── Step 3: Visualise — stacked histograms with threshold lines ───────────────

colors = [cm.Blues(v) for v in np.linspace(0.4, 0.9, len(sample_sizes))]

fig_hist, axes = plt.subplots(
    nrows=len(sample_sizes), ncols=1,
    figsize=(7, 11), sharex=True
)

for ax, n, color in zip(axes, sample_sizes, colors):
    ax.hist(null_data[n], bins=50, color=color, edgecolor="white", alpha=0.85)
    ax.axvline(r_crits[n], color="black", linewidth=1.0)
    ax.set_title(f"n = {n}", fontsize=11)
    ax.set_ylabel("Count", fontsize=10)
    ax.grid(True, linestyle="--", alpha=0.3)

axes[-1].set_xlabel("Pearson r", fontsize=12)
fig_hist.suptitle(
    f"Null distribution of Pearson r  |  {n_sim} simulations per n\n"
    "Vertical line = one-tailed critical r at α = 0.05",
    y=1.01, fontsize=11
)
fig_hist.tight_layout()
fig_hist.savefig("08-hw-null-r-by-n.pdf", bbox_inches="tight")
plt.show()


# ── Step 4: Visualise — critical r as a function of sample size ───────────────

n_grid   = np.linspace(4, 110, 300)
r_theory = 1.645 / np.sqrt(n_grid - 1)

fig_thresh, ax_thresh = plt.subplots(figsize=(6, 4))

ax_thresh.plot(
    sample_sizes, [r_crits[n] for n in sample_sizes],
    color="steelblue", linewidth=1.5, marker="o", markersize=7,
    label="Simulated"
)
ax_thresh.plot(
    n_grid, r_theory,
    color="black", linewidth=1.0, linestyle="--",
    label=r"Theory: $1.645\,/\,\sqrt{n-1}$"
)
ax_thresh.set_xlabel("Sample size (n)", fontsize=12)
ax_thresh.set_ylabel("Critical r", fontsize=12)
ax_thresh.set_title(
    "Critical r (one-tailed α = 0.05) vs. sample size\n"
    "Even a small correlation is 'significant' at very large n",
    fontsize=11
)
ax_thresh.legend(fontsize=10)
ax_thresh.grid(True, linestyle="--", alpha=0.4)
fig_thresh.tight_layout()
fig_thresh.savefig("08-hw-rcrit-vs-n.pdf")
plt.show()


# Question 1:
# Describe how the shape of the null distribution changes as n increases.
# Comment on both the width (spread) and the symmetry across the five panels.
#
# [ Write your answer here. ]


# Question 2:
# Report r_crit at n = 5 and n = 100. What does the difference imply for
# interpreting r = 0.35 from a study with n = 20 versus r = 0.10 from a
# study with n = 500? Which finding is more likely to be "significant"?
# Which is more likely to matter practically?
#
# [ Write your answer here. ]


# Question 3:
# With very large n (e.g., n = 10,000), virtually any non-zero r would be
# "statistically significant." What should a researcher report alongside a
# p-value to convey whether a significant correlation is practically meaningful?
#
# [ Write your answer here. ]


# Question 4:
# The dashed theory curve (1.645/sqrt(n−1)) tracks the simulation well at
# large n but diverges slightly at n = 5. Why might the approximation be less
# accurate at very small sample sizes?
#
# [ Write your answer here. ]


# Question 5:
# Extend Step 2 to also compute the 2.5th percentile (the lower-tail critical
# value). Add both lines to the Step 3 plot. What is the two-tailed critical
# |r| at n = 10? How does it compare to the one-tailed value?
#
# [ Write your answer here. ]
