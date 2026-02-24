# =============================================================================
# Rethinking Data Analysis
# In-class discussion: Three ways to estimate the standard error of the mean
# =============================================================================

import numpy as np
import matplotlib.pyplot as plt

np.random.seed(42)

# =============================================================================
# PART 1: Formula-based standard error of the mean
# =============================================================================

pop1      = np.random.normal(50, 10, 1000)
sample1   = np.random.choice(pop1, size=10, replace=False)

samp_mean = np.mean(sample1)
samp_sd   = np.std(sample1, ddof=1)
samp_sem  = samp_sd / np.sqrt(len(sample1))

print("=== Part 1: Formula-based SEM ===")
print(f"  Sample mean : {samp_mean:.4f}")
print(f"  Sample SD   : {samp_sd:.4f}")
print(f"  SEM (SD/√n) : {samp_sem:.4f}\n")


# =============================================================================
# PART 2: Empirical standard error via repeated sampling
# =============================================================================

pop2        = np.random.normal(50, 10, 1000)
n_reps      = 100
sample_size = 10

sample_means = np.array([np.mean(np.random.choice(pop2, size=sample_size, replace=False))
                         for _ in range(n_reps)])

empirical_sem = np.std(sample_means, ddof=1)

print("=== Part 2: Empirical SEM (repeated sampling) ===")
print(f"  Number of repeated samples : {n_reps}")
print(f"  Sample size per draw       : {sample_size}")
print(f"  Mean of sample means       : {np.mean(sample_means):.4f}")
print(f"  SD of sample means (empirical SEM) : {empirical_sem:.4f}\n")


# =============================================================================
# PART 3: Bootstrap standard error of the mean
# =============================================================================

observed_sample = np.random.choice(pop2, size=10, replace=False)
n_boot          = 1000

boot_means = np.array([np.mean(np.random.choice(observed_sample,
                                                 size=len(observed_sample),
                                                 replace=True))
                        for _ in range(n_boot)])

bootstrap_sem = np.std(boot_means, ddof=1)

print("=== Part 3: Bootstrap SEM ===")
print(f"  Observed sample: {', '.join(str(round(x, 2)) for x in observed_sample)}")
print(f"  Number of bootstrap samples : {n_boot}")
print(f"  Mean of bootstrap means     : {np.mean(boot_means):.4f}")
print(f"  SD of bootstrap means (bootstrap SEM) : {bootstrap_sem:.4f}\n")


# =============================================================================
# COMPARISON SUMMARY
# =============================================================================

print("=== Comparison of SEM estimates ===")
print(f"  Formula-based SEM (Part 1) : {samp_sem:.4f}")
print(f"  Empirical SEM  (Part 2)    : {empirical_sem:.4f}")
print(f"  Bootstrap SEM  (Part 3)    : {bootstrap_sem:.4f}")
print(f"  True SEM (SD_pop / √n)     : {np.std(pop2, ddof=1) / np.sqrt(10):.4f}")


# =============================================================================
# PLOT: Distribution of sample means for each part
# =============================================================================

xlim_all = (min(samp_mean, sample_means.min(), boot_means.min()) - 5,
            max(samp_mean, sample_means.max(), boot_means.max()) + 5)

fig, axes = plt.subplots(1, 3, figsize=(12, 4.5))
fig.subplots_adjust(wspace=0.35)

ax = axes[0]
ax.set_xlim(xlim_all)
ax.set_ylim(0, 1)
ax.set_yticks([])
ax.set_xlabel("Sample Mean")
ax.set_title("Part 1: Formula-based SEM\n(one sample, n = 10)")
ax.axvline(50, color="grey", linestyle="--", linewidth=1.5)
ax.errorbar(samp_mean, 0.5, xerr=samp_sem,
            fmt="o", color="steelblue", markersize=8,
            capsize=5, capthick=2, elinewidth=2)
ax.legend([f"mean = {samp_mean:.2f}\n± SEM = {samp_sem:.2f}"],
          loc="upper right", frameon=False, fontsize=8.5)

ax = axes[1]
ax.hist(sample_means, bins=15, color="steelblue", edgecolor="white")
ax.set_xlim(xlim_all)
ax.set_xlabel("Sample Mean")
ax.set_ylabel("Count")
ax.set_title("Part 2: Empirical SEM\n(100 samples, n = 10 each)")
ax.axvline(50, color="grey", linestyle="--", linewidth=1.5)
ax.axvline(np.mean(sample_means), color="red", linewidth=2)
ax.legend([f"mean = {np.mean(sample_means):.2f}\nEmpirical SEM = {empirical_sem:.2f}"],
          loc="upper right", frameon=False, fontsize=8.5)

ax = axes[2]
ax.hist(boot_means, bins=30, color="steelblue", edgecolor="white")
ax.set_xlim(xlim_all)
ax.set_xlabel("Bootstrap Mean")
ax.set_ylabel("Count")
ax.set_title("Part 3: Bootstrap SEM\n(1000 resamples, n = 10)")
ax.axvline(50, color="grey", linestyle="--", linewidth=1.5)
ax.axvline(np.mean(boot_means), color="red", linewidth=2)
ax.legend([f"mean = {np.mean(boot_means):.2f}\nBootstrap SEM = {bootstrap_sem:.2f}"],
          loc="upper right", frameon=False, fontsize=8.5)

plt.savefig("standard_error_plot.png", dpi=120, bbox_inches="tight")
print("\nPlot saved to standard_error_plot.png")
