# ─────────────────────────────────────────────────────────────────────────────
# Assignment 03 — In-Class: Calculating P-values Using a Permutation Test
#
# In-class activity. Work through this script with a partner, add detailed
# comments at every step, run it block by block, and discuss the outputs.
# Add your notes in the spaces marked [ Add your notes here ].
# ─────────────────────────────────────────────────────────────────────────────


# ── Part 1: Calculating a P-value Using a Permutation Test ───────────────────
#
# Scenario: A small clinical trial enrolled 40 patients. Twenty received a
# placebo (group 1, control) and twenty received a new drug (group 2,
# treatment). Each value represents that patient's change in symptom score.
# Higher scores mean worse symptoms.


import numpy as np
import matplotlib.pyplot as plt
from scipy import stats


# ── Step 0: How the data were generated (reference only) ─────────────────────
# Do not run the code below — it shows how data like these could be simulated.

# rng         = np.random.default_rng()
# effect_size = 0.25
# stddev      = 0.5
# sample_size = 20
#
# group1 = np.round(rng.normal(loc=0,           scale=stddev, size=sample_size) * 10)
# group2 = np.round(rng.normal(loc=effect_size, scale=stddev, size=sample_size) * 10)
#
# print('Group 1:', group1)
# print('Group 2:', group2)


# ── Step 1: Enter and inspect the data ───────────────────────────────────────

# Define the two groups
group1 = np.array([ 0,  5,  2, -2,  8,
                   -6,  0,  0, -6, -3,
                   -7,  4, -2, -2,  0,
                   -4, -1, -8,  0,  6])

group2 = np.array([-2,  2, -2, -5,  7,
                   11,  6,  2,  1,  1,
                    6, -2, -1,  7,  7,
                   -2,  4,  3, -1, 17])

sample_size = len(group1)

print(f'Group 1 (control)   mean: {np.mean(group1):.2f}  sd: {np.std(group1, ddof=1):.2f}')
print(f'Group 2 (treatment) mean: {np.mean(group2):.2f}  sd: {np.std(group2, ddof=1):.2f}')

# [ Add your notes here. ]


# ── Step 2: Visualize the two distributions ──────────────────────────────────

# Overlapping histograms of the two groups
fig, ax = plt.subplots(figsize=(8, 4))

ax.hist(group1, color='steelblue', alpha=0.4, edgecolor='k',
        label='Group 1 (control)')
ax.hist(group2, color='firebrick', alpha=0.4, edgecolor='k',
        label='Group 2 (treatment)')

ax.axvline(np.mean(group1), color='steelblue', lw=2, ls='--',
           label=f'Mean group1 = {np.mean(group1):.1f}')
ax.axvline(np.mean(group2), color='firebrick',  lw=2, ls='--',
           label=f'Mean group2 = {np.mean(group2):.1f}')

ax.set_xlabel('Change in symptom score')
ax.set_ylabel('Count')
ax.set_title('Symptom score distributions: control vs. treatment')
ax.legend()

plt.tight_layout()
plt.show()

# [ Add your notes here. ]


# ── Step 3: Compute the observed test statistic ───────────────────────────────

# Compute signal / noise (the test statistic)
signal = np.mean(group2) - np.mean(group1)
noise  = np.sqrt((np.var(group2, ddof=1) / sample_size) +
                  (np.var(group1, ddof=1) / sample_size))

test_statistic = signal / noise

print(f'Signal (difference in means):  {signal:.4f}')
print(f'Noise  (SE of the difference): {noise:.4f}')
print(f'Observed test statistic:       {test_statistic:.4f}')

# [ Add your notes here. ]


# ── Step 4: Set up the permutation test ──────────────────────────────────────

# Set up containers for the permutation test
rng = np.random.default_rng()

num_permutations         = 10000
permuted_test_statistics = np.empty(num_permutations)


# ── Step 5: Run the permutation loop ─────────────────────────────────────────

# Permutation loop: shuffle the combined pool, re-split, compute the test statistic
pool = np.concatenate([group1, group2])

for i in range(num_permutations):

    shuffled = rng.permutation(pool)

    rand_group1 = shuffled[:sample_size]
    rand_group2 = shuffled[sample_size:]

    perm_signal = np.mean(rand_group2) - np.mean(rand_group1)
    perm_noise  = np.sqrt((np.var(rand_group2, ddof=1) / sample_size) +
                           (np.var(rand_group1, ddof=1) / sample_size))

    permuted_test_statistics[i] = perm_signal / perm_noise

# [ Add your notes here. ]


# ── Step 6: Visualize the null distribution ──────────────────────────────────

# Histogram of the null distribution; red dashed line = observed test statistic
fig, ax = plt.subplots(figsize=(8, 4))

ax.hist(permuted_test_statistics, bins=60, color='lightsteelblue',
        edgecolor='white', label='Null distribution')
ax.axvline(test_statistic, color='red', lw=2, ls='--',
           label=f'Observed statistic = {test_statistic:.2f}')

ax.set_xlabel('Test statistic under H0 (null distribution)')
ax.set_ylabel('Count')
ax.set_title('Null distribution from 10,000 permutations')
ax.legend()

plt.tight_layout()
plt.show()

# [ Add your notes here. ]


# ── Step 7: Compute the permutation p-value ───────────────────────────────────

# Compute the p-value as the fraction of permuted statistics >= observed
pvalue = np.mean(permuted_test_statistics >= test_statistic)
print(f'Permutation p-value: {pvalue:.4f}')

# [ Add your notes here. ]


# ── Step 8: Compare to the parametric t-test ─────────────────────────────────

# Welch two-sample t-test for comparison
result = stats.ttest_ind(group2, group1, equal_var=False, alternative='greater')
print(f'Parametric Welch t-test p-value:   {result.pvalue:.4f}')
print(f'Permutation p-value (from above):  {pvalue:.4f}')


# ── Questions ────────────────────────────────────────────────────────────────

# Question 1:
# Using the language of this specific experiment (placebo vs. drug, symptom
# scores), write a precise one-sentence definition of the permutation p-value
# you calculated.
#
# [ Write your answer here. ]


# Question 2:
# Is the permutation p-value close to the t-test p-value? What does agreement
# (or disagreement) between the two methods tell you?
#
# [ Write your answer here. ]
