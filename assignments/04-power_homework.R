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
# sizes to see how power changes as a function of BOTH effect size (coin bias)
# AND sample size (number of flips). This is exactly the analysis researchers
# use when designing a study: "given the effect I expect, how many observations
# do I need for adequate power?"

library(tidyverse)


# ── Parameters ───────────────────────────────────────────────────────────────
#
# set.seed() fixes the random-number sequence for reproducibility.

set.seed(42)

alpha            <- 0.05   # significance threshold
num_permutations <- 10000  # simulations per null distribution
num_experiments  <- 1000   # experiments per (bias, sample_size) combination

# Explore four different sample sizes
flips <- c(5, 10, 50, 100)

# [ Add your notes here. ]


# ── Step 1: Build a null distribution for each sample size ───────────────────
#
# Each sample size has its own null distribution: with more flips, the
# distribution of head-counts under H0 spreads wider in raw counts but
# becomes relatively more concentrated around num_flips/2 as a fraction.
# We must pair each p-value calculation with the correct null distribution.
#
# We store the data in a tidy tibble (one row per simulation per sample size)
# so that downstream ggplot code is straightforward.

null_df <- map_dfr(flips, \(n) {
  tibble(
    sample_size    = n,
    fair_num_heads = rbinom(n = num_permutations, size = n, prob = 0.5)
  )
})

# [ Add your notes here. ]


# ── Step 2: Visualise the null distributions ─────────────────────────────────
#
# Plotting all four null distributions side by side reveals how the spread
# changes with sample size.

null_df |>
  ggplot(aes(x = fair_num_heads)) +
  geom_histogram(binwidth = 1, fill = "steelblue",
                 colour = "black", alpha = 0.7) +
  facet_wrap(~ sample_size, nrow = 1, scales = "free",
             labeller = label_both) +
  labs(
    x     = "Heads count (fair coin)",
    y     = "Count",
    title = "Null distributions for four sample sizes"
  ) +
  theme_bw() +
  theme(legend.position = "none")

# Question 3:
# What are your observations on how the null distribution changes with sample
# size? Comment on both the centre and the spread.
#
# [ Write your answer here. ]


# ── Step 3: Compute power curves for each sample size ────────────────────────
#
# For each (sample_size, coin_bias) combination we:
#   1. Retrieve the pre-computed null distribution for that sample size
#   2. Simulate num_experiments biased-coin experiments
#   3. Compute the p-value for each experiment against the null
#   4. Estimate power as the fraction of experiments where p < alpha
#
# NOTE: This computation is intentionally written with explicit loops to make
# each step readable. It will take 1–3 minutes on a modern laptop.

biases <- seq(0, 1, by = 0.01)   # 101 bias values

power_results <- map_dfr(flips, \(n) {
  cat(n, "flips\n")

  # Retrieve the null distribution and compute its deviations from centre
  null_heads <- null_df |>
    filter(sample_size == n) |>
    pull(fair_num_heads)
  null_devs <- abs(null_heads - n / 2)   # how far each null sim deviated from n/2

  map_dfr(biases, \(b) {
    # Simulate all experiments for this (n, b) combination at once
    heads_all <- rbinom(n = num_experiments, size = n, prob = b)

    # Compute p-value for each experiment and check significance
    p_vals <- sapply(heads_all, \(h) mean(null_devs > abs(h - n / 2)))

    tibble(
      sample_size     = n,
      effect_size     = b,
      estimated_power = mean(p_vals < alpha)
    )
  })
})

# [ Add your notes here. ]


# ── Step 4: Visualise multiple power curves ───────────────────────────────────
#
# All power curves on one axes for direct comparison. Larger n → curves rise
# more steeply, meaning you can detect smaller biases.

power_results |>
  mutate(sample_size = factor(sample_size)) |>
  ggplot(aes(x     = effect_size,
             y     = estimated_power,
             colour = sample_size,
             shape  = sample_size)) +
  geom_line()  +
  geom_point(size = 1.5) +
  geom_hline(yintercept = 0.80, colour = "black",
             linetype = "dashed", linewidth = 0.6, alpha = 0.6) +
  geom_vline(xintercept = 0.50, colour = "grey50",
             linetype = "dotted", linewidth = 0.6, alpha = 0.6) +
  scale_colour_brewer(palette = "Dark2", name = "Sample size (n)") +
  scale_shape_discrete(name = "Sample size (n)") +
  labs(
    x     = "Coin bias (true P(heads))",
    y     = "Estimated power",
    title = sprintf("Power curves for multiple sample sizes  |  alpha = %.2f", alpha)
  ) +
  theme_bw()

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
