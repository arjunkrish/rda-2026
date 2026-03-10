# ─────────────────────────────────────────────────────────────────────────────
# Assignment 04 — In-Class: Calculating Power and Generating a Power Curve
#
# In-class activity: work through this script with a partner, add detailed
# comments at every step, run it block by block, and discuss the outputs.
# Add your notes in the spaces marked [ Add your notes here ].
# ─────────────────────────────────────────────────────────────────────────────


# ── Part 1: Calculating Power and Generating a Power Curve for Detecting Unfair Coins ──

import numpy as np
import matplotlib.pyplot as plt


# ── Parameters ───────────────────────────────────────────────────────────────

rng = np.random.default_rng(seed=42)   # reproducible random-number generator

num_flips = 20    # sample size: number of coin flips per experiment
alpha     = 0.05  # significance threshold: reject H0 when p-value < alpha

# [ Add your notes here. ]


# ── Step 1: Build the null distribution ──────────────────────────────────────

num_permutations = 10_000   # number of simulations for the null distribution

# Each element of fair_num_heads is the head-count from one fair-coin simulation
fair_num_heads = rng.binomial(n=num_flips, p=0.5, size=num_permutations)

# Visualise the null distribution so we can see its shape before using it
fig, ax = plt.subplots(figsize=(7, 4))
ax.hist(fair_num_heads, bins=range(num_flips + 2),
        edgecolor='k', color='steelblue', alpha=0.7)
ax.set_xlabel('Number of heads (fair coin)')
ax.set_ylabel(f'Count (out of {num_permutations:,} simulations)')
ax.set_title(f'Null distribution: fair coin flipped {num_flips} times')
ax.set_xlim(0, num_flips)
plt.tight_layout()
plt.show()

# [ Add your notes here. ]


# ── Step 2: Run one experiment with a biased coin ────────────────────────────

coin_bias = 0.8   # effect size: true P(heads) of the coin being tested

# Simulate one experiment: flip the biased coin num_flips times
num_heads = int(rng.binomial(n=num_flips, p=coin_bias, size=1))
print(f'{num_heads} heads in {num_flips} flips')

# Compute the two-tailed p-value from the null distribution.
# deviations_null[i] = how far the i-th null simulation fell from num_flips/2
# obs_deviation      = how far OUR observed count fell from num_flips/2
# p-value = fraction of null simulations that deviated AT LEAST as much as us
deviations_null = np.abs(fair_num_heads - num_flips / 2)  # array of null deviations
obs_deviation   = abs(num_heads - num_flips / 2)          # scalar observed deviation
p_value = np.mean(deviations_null > obs_deviation)         # fraction more extreme than observed

# Visualise where the observed result falls in the null distribution
fig, ax = plt.subplots(figsize=(7, 4))
ax.hist(fair_num_heads, bins=range(num_flips + 2),
        edgecolor='k', color='steelblue', alpha=0.7,
        label='Null distribution (fair coin)')
ax.axvline(num_heads, color='red', lw=2,
           label=f'Observed: {num_heads} heads (p = {p_value:.3f})')
ax.set_xlabel('Number of heads')
ax.set_ylabel('Count')
ax.set_title('One experiment: observed result vs. null distribution')
ax.set_xlim(0, num_flips)
ax.legend()
plt.tight_layout()
plt.show()

if p_value < alpha:
    print(f'p-value = {p_value:.4f} < {alpha}  →  Reject H0. The coin appears biased!')
else:
    print(f'p-value = {p_value:.4f} ≥ {alpha}  →  Fail to reject H0. Coin appears fair.')

# [ Add your notes here. ]


# ── Step 3: Estimate power by repeating the experiment many times ─────────────

num_experiments = 1000   # number of independent experiments for power estimation

# Draw all num_experiments head-counts at once (one row per experiment)
heads_per_experiment = rng.binomial(n=num_flips, p=coin_bias,
                                    size=num_experiments)  # shape: (1000,)

# Count how many experiments yield a significant p-value (i.e., reject H0)
num_null_rejects = 0
for h in heads_per_experiment:
    obs_dev = abs(h - num_flips / 2)
    p_val   = np.mean(deviations_null > obs_dev)
    if p_val < alpha:
        num_null_rejects += 1

estimated_power = num_null_rejects / num_experiments
print(f'\nEstimated power: {estimated_power:.3f}')
print(f'(num_flips={num_flips}, alpha={alpha}, coin_bias={coin_bias})')

# [ Add your notes here. ]


# Question 1:
# Define the power you just obtained in terms of this specific experiment.
# (e.g., "Power = X means that if we flip a coin with P(heads) = 0.8 exactly
# num_flips times and apply our test, we expect to correctly identify it as
# biased X% of the time.")
#
# [ Write your answer here. ]


# ── Step 4: Generate a power curve ───────────────────────────────────────────

biases = np.arange(0.0, 1.01, 0.01)        # 101 bias values: 0.00, 0.01, …, 1.00
estimated_powers = np.empty(len(biases))    # pre-allocate output array

for j, b in enumerate(biases):
    # Simulate all experiments for this bias level at once
    heads_all = rng.binomial(n=num_flips, p=b, size=num_experiments)

    # Count rejections: how many experiments correctly detect the bias?
    rejects = sum(
        1 for h in heads_all
        if np.mean(deviations_null > abs(h - num_flips / 2)) < alpha
    )
    estimated_powers[j] = rejects / num_experiments

# [ Add your notes here. ]

# Plot the power curve
fig, ax = plt.subplots(figsize=(8, 5))
ax.plot(biases, estimated_powers, 'ko-', markersize=3, linewidth=1)
ax.axhline(0.80, color='firebrick', ls='--', lw=1.2,
           label='Power = 0.80 (conventional minimum)')
ax.axvline(0.50, color='gray',      ls=':',  lw=1.2,
           label='Fair coin (bias = 0.5)')
ax.set_xlabel('Coin bias (true P(heads))')
ax.set_ylabel('Estimated power')
ax.set_title(f'Power curve  |  {num_flips} flips, alpha = {alpha}')
ax.legend()
plt.tight_layout()
plt.show()


# Question 2:
# What does this power curve tell you? Describe the shape, and explain what
# happens to power as the coin becomes more biased away from 0.5.
#
# [ Write your answer here. ]
