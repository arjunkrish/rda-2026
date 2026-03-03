# ─────────────────────────────────────────────────────────────────────────────
# Assignment 03 — Homework: Effect Size, Variance, Sample Size & P-hacking
#
# Homework. Annotate this script, run it, and answer the questions embedded
# below. Add your notes in the spaces marked [ Add your notes here ].
# ─────────────────────────────────────────────────────────────────────────────


# ── Part 2: Effect of Effect Size, Variance, and Sample Size on P-values ─────
#
# Apart from the null hypothesis, the p-value depends on:
#   1. Effect size, 2. Sample size, and 3. Variance within each group.
#
# The code below simulates two groups for every combination of these three
# factors and runs a t-test for each.


import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import pandas as pd


# Nested simulation: for each combination of effect_size, std_deviation,
# and sample_size, simulate two groups and record the t-test p-value.

rng = np.random.default_rng()

effect_sizes = np.arange(0.1, 1.05, 0.05)
std_devs     = [0.5, 1, 2]
sample_sizes = [5, 10, 20, 50, 100, 200, 500, 1000]

records = []

for effect_size in effect_sizes:
    for stddev in std_devs:
        for sample_size in sample_sizes:

            group1 = rng.normal(loc=0,           scale=stddev, size=sample_size)
            group2 = rng.normal(loc=effect_size, scale=stddev, size=sample_size)

            result = stats.ttest_ind(group1, group2)

            records.append({
                'effect_size':   effect_size,
                'std_deviation': stddev,
                'sample_size':   sample_size,
                'pvalue':        result.pvalue
            })

es_sd_ss_pvalue = pd.DataFrame(records)
print(es_sd_ss_pvalue)

# [ Add your notes here. ]


# Add a column flagging whether p < 0.05
es_sd_ss_pvalue['below_threshold'] = es_sd_ss_pvalue['pvalue'] < 0.05
print(es_sd_ss_pvalue)

# [ Add your notes here. ]


# Three-panel plot: one panel per std_deviation value.
# x-axis: sample_size (log scale); y-axis: effect_size;
# color/marker: whether p < 0.05 (red circle) or not (blue cross).

std_deviation_levels = [0.5, 1, 2]

fig, axes = plt.subplots(nrows=1, ncols=3, figsize=(14, 5), sharey=True)

for ax, sd_val in zip(axes, std_deviation_levels):

    subset  = es_sd_ss_pvalue[es_sd_ss_pvalue['std_deviation'] == sd_val]
    sig     = subset[subset['below_threshold'] == True]
    not_sig = subset[subset['below_threshold'] == False]

    ax.plot(sig['sample_size'],     sig['effect_size'],
            'ro', markersize=6, alpha=0.8, label='p < 0.05')
    ax.plot(not_sig['sample_size'], not_sig['effect_size'],
            'bx', markersize=6, alpha=0.8, label='p >= 0.05')

    ax.set_xscale('log')
    ax.set_title(f'SD = {sd_val}', fontsize=12)
    ax.set_xlabel('Sample size (log scale)', fontsize=11)

axes[0].set_ylabel('Effect size', fontsize=11)
axes[1].legend(loc='lower right', fontsize=10)

fig.suptitle('Which combinations of effect size, SD, and sample size yield p < 0.05?',
             fontsize=13, y=1.02)
plt.tight_layout()
plt.savefig('effectsize_variance_samplesize_pvalue.pdf', bbox_inches='tight')
plt.show()


# Question (Part 2):
# Examine the figure and write a short paragraph about your observations on how
# effect size, sample size, and within-group variance each influence the p-value.
#
# [ Write your answer here. ]


# ── Part 3: P-hacking ────────────────────────────────────────────────────────
#
# P-hacking is the practice of collecting or selecting data or statistical
# analyses until nonsignificant results become significant.


# Generate a null dataset: 200 observations from a single Normal(0, 1) distribution
rng  = np.random.default_rng(seed=42)
data = rng.normal(size=200)

fig, ax = plt.subplots(figsize=(7, 4))
ax.hist(data, bins=20, color='lightsteelblue', edgecolor='white')
ax.set_xlabel('Value')
ax.set_ylabel('Count')
ax.set_title('200 observations from a single Normal(0, 1) distribution')
plt.tight_layout()
plt.show()

# [ Add your notes here. ]


# Initialise counters
attempts = 0
pvalue   = 1.0


# Keep splitting the data randomly into two groups until p < 0.05

all_indices = np.arange(len(data))

while pvalue > 0.05:
    attempts += 1

    case_indices = rng.choice(all_indices, size=100, replace=False)

    control_mask = np.ones(len(data), dtype=bool)
    control_mask[case_indices] = False

    cases    = data[case_indices]
    controls = data[control_mask]

    result = stats.ttest_ind(cases, controls)
    pvalue = result.pvalue

print(f'"Significant" result found! p = {pvalue:.4f} after {attempts} attempt(s).')

# [ Add your notes here. ]


# Question (Part 3):
# What does this coding exercise have to do with p-hacking?
#
# [ Write your answer here. ]
