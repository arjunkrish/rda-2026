# ─────────────────────────────────────────────────────────────────────────────
# Assignment 04 — Homework: Generating Multiple Power Curves for Detecting
#                           Unfair Coins
#
# Work through this script on your own, add detailed comments at every step,
# and answer the questions at the end. Submit a PDF of your annotated script
# and answers via the course submission form.
# ─────────────────────────────────────────────────────────────────────────────


# ── Part 2: Generating Multiple Power Curves for Detecting Unfair Coins ───────
#
# In the in-class assignment you produced one power curve for a fixed sample
# size (num_flips = 20). Here you extend that analysis to multiple sample
# sizes. You will see how power changes as a function of BOTH effect size
# (coin bias) AND sample size (number of flips). This kind of analysis is
# exactly what researchers use when designing a study: they ask "given the
# effect size I expect, how many observations do I need to have adequate power?"


import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm


# ── Parameters ───────────────────────────────────────────────────────────────
#
# Same random seed and significance threshold as the in-class script.

rng   = np.random.default_rng(seed=42)  # reproducible random-number generator
alpha = 0.05                             # significance threshold

num_permutations = 10_000  # simulations per null distribution
num_experiments  = 1000    # experiments per (bias, sample_size) combination

# Explore four different sample sizes to see how n affects power
flips = [5, 10, 50, 100]

# [ Add your notes here. ]


# ── Step 1: Build a null distribution for each sample size ───────────────────
#
# Each sample size has its own null distribution: with more flips, the
# distribution of head-counts under H0 shifts (spreads wider in raw counts
# but becomes relatively narrower around num_flips/2 as a fraction). We must
# use the *correct* null distribution for each sample size when computing
# p-values later.
#
# We store null distributions in a dictionary keyed by sample size for
# clean, readable lookup.

null_distributions = {}   # dict: num_flips → array of 10,000 head-counts under H0

for n in flips:
    # Draw num_permutations fair-coin experiments for this sample size
    null_distributions[n] = rng.binomial(n=n, p=0.5, size=num_permutations)

# [ Add your notes here. ]


# ── Step 2: Visualise the null distributions ─────────────────────────────────
#
# Plotting all four null distributions side by side lets you see concretely
# how the spread of the distribution changes with sample size. Even though
# the distributions get wider in absolute terms, the *relative* variability
# (coefficient of variation) decreases — larger n → more precise estimates.

fig, axes = plt.subplots(1, len(flips), figsize=(16, 4))
for ax, n in zip(axes, flips):
    ax.hist(null_distributions[n], bins=range(n + 2),
            edgecolor='k', color='steelblue', alpha=0.7)
    ax.set_title(f'n = {n} flips')
    ax.set_xlabel('Heads count (fair coin)')
    ax.set_ylabel('Count')
    ax.set_xlim(0, n)
fig.suptitle('Null distributions for four sample sizes', y=1.02)
plt.tight_layout()
plt.show()

# Question 3:
# What are your observations on how the null distribution changes with sample
# size? Comment on both the centre and the spread.
#
# [ Write your answer here. ]


# ── Step 3: Compute power curves for each sample size ────────────────────────
#
# We now repeat the power-curve calculation from the in-class script, but for
# every sample size in `flips`. For each (sample_size, coin_bias) pair we:
#   1. Simulate num_experiments biased-coin experiments
#   2. Test each against the corresponding null distribution
#   3. Estimate power as the rejection rate
#
# NOTE: this triple-nested loop is intentionally slow to make the logic
# transparent. On a modern laptop it takes 1–3 minutes. Be patient.

biases = np.arange(0.0, 1.01, 0.01)   # 101 bias values

# Store results as a list of (sample_size, bias, power) tuples for easy
# conversion to a structured array / data frame for plotting
results = []   # list of (num_flips, coin_bias, estimated_power)

for n in flips:
    print(f'Computing power curves for n = {n} flips …')
    null_devs = np.abs(null_distributions[n] - n / 2)  # deviations under H0

    for b in biases:
        # Simulate all experiments for this (n, b) combination at once
        heads_all = rng.binomial(n=n, p=b, size=num_experiments)

        # Estimate power: fraction of experiments that correctly reject H0
        rejects = sum(
            1 for h in heads_all
            if np.mean(null_devs > abs(h - n / 2)) < alpha
        )
        results.append((n, b, rejects / num_experiments))

# [ Add your notes here. ]


# ── Step 4: Visualise multiple power curves ───────────────────────────────────
#
# Plot all power curves on one axes to compare them directly. Power curves
# for larger sample sizes rise more steeply away from 0.5 — you need smaller
# effects (less biased coins) before you can reliably detect them.

# Organise results by sample size for plotting
results_by_n = {n: [] for n in flips}
for (n, b, power) in results:
    results_by_n[n].append((b, power))

colors  = cm.Set1(np.linspace(0.1, 0.9, len(flips)))
markers = ['o', '^', 's', 'p']

fig, ax = plt.subplots(figsize=(9, 6))
for (n, color, marker) in zip(flips, colors, markers):
    biases_n = [r[0] for r in results_by_n[n]]
    powers_n = [r[1] for r in results_by_n[n]]
    ax.plot(biases_n, powers_n, color=color, marker=marker,
            markersize=3, linewidth=1, label=f'n = {n}')

ax.axhline(0.80, color='black', ls='--', lw=1, alpha=0.5,
           label='Power = 0.80')
ax.axvline(0.50, color='gray',  ls=':',  lw=1, alpha=0.5,
           label='Fair coin (bias = 0.5)')
ax.set_xlabel('Coin bias (true P(heads))')
ax.set_ylabel('Estimated power')
ax.set_title(f'Power curves for multiple sample sizes  |  alpha = {alpha}')
ax.legend(title='Sample size')
plt.tight_layout()
plt.show()

# [ Add your notes here. ]


# Question 4:
# What are your interpretations of these curves? Write your thoughts in terms
# of the dependence of power on both effect size (coin bias) and sample size
# (number of flips).
#
# [ Write your answer here. ]


# Question 5:
# A national sports organisation wants to design an experiment to detect
# biased coins used in pre-game tosses. How would you use the power curves
# above to help them design the experiment? What questions would you need to
# ask before you could give a specific sample-size recommendation?
#
# [ Write your answer here. ]


# Question 6:
# If you make a specific sample-size recommendation, write down what you
# will tell the organisation about error rates (false-positive rate and
# false-negative rate).
#
# [ Write your answer here. ]


# Question 7:
# Which parts of your reasoning and recommendations change if the organisation
# says it cannot tolerate more than 1 biased coin for every 100 coins it uses?
# (Hint: this corresponds to changing alpha from 0.05 to 0.01.)
#
# [ Write your answer here. ]
