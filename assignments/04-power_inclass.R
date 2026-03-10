# ─────────────────────────────────────────────────────────────────────────────
# Assignment 04 — In-Class: Calculating Power and Generating a Power Curve
#
# In-class activity: work through this script with a partner, add detailed
# comments at every step, run it block by block, and discuss the outputs.
# Add your notes in the spaces marked [ Add your notes here ].
# ─────────────────────────────────────────────────────────────────────────────


# ── Part 1: Calculating Power and Generating a Power Curve for Detecting Unfair Coins ──

library(tidyverse)


# ── Parameters ───────────────────────────────────────────────────────────────

set.seed(42)      # reproducibility

num_flips <- 20   # sample size: number of coin flips per experiment
alpha     <- 0.05 # significance threshold: reject H0 when p-value < alpha

# [ Add your notes here. ]


# ── Step 1: Build the null distribution ──────────────────────────────────────

num_permutations <- 10000   # number of simulations for the null distribution

# Each element of fair_num_heads is the head-count from one fair-coin simulation
fair_num_heads <- rbinom(n    = num_permutations,
                         size = num_flips,
                         prob = 0.5)

# Visualise the null distribution
tibble(heads = fair_num_heads) |>
  ggplot(aes(x = heads)) +
  geom_histogram(binwidth = 1, fill = "steelblue", colour = "black", alpha = 0.7) +
  labs(
    x     = "Number of heads (fair coin)",
    y     = glue::glue("Count (out of {num_permutations} simulations)"),
    title = glue::glue("Null distribution: fair coin flipped {num_flips} times")
  ) +
  xlim(0, num_flips) +
  theme_bw()

# [ Add your notes here. ]


# ── Step 2: Run one experiment with a biased coin ────────────────────────────

coin_bias <- 0.8   # effect size: true P(heads) of the coin being tested

# Simulate one experiment: flip the biased coin num_flips times
num_heads <- rbinom(n = 1, size = num_flips, prob = coin_bias)
cat(num_heads, "heads in", num_flips, "flips\n")

# Compute the two-tailed p-value from the null distribution.
# deviations_null[i] = how far the i-th null simulation deviated from num_flips/2
# obs_deviation      = how far OUR observed count deviated from num_flips/2
# p-value = fraction of null simulations more extreme than what we observed
deviations_null <- abs(fair_num_heads - num_flips / 2)  # vector of null deviations
obs_deviation   <- abs(num_heads      - num_flips / 2)  # scalar observed deviation
p_value <- mean(deviations_null > obs_deviation)         # fraction more extreme than observed

# Visualise where the observed result falls in the null distribution
tibble(heads = fair_num_heads) |>
  ggplot(aes(x = heads)) +
  geom_histogram(binwidth = 1, fill = "steelblue", colour = "black", alpha = 0.7) +
  geom_vline(xintercept = num_heads, colour = "red", linewidth = 1.2) +
  annotate("text", x = num_heads + 0.5, y = Inf,
           label = sprintf("observed = %d\np = %.3f", num_heads, p_value),
           hjust = 0, vjust = 2, colour = "red") +
  labs(x     = "Number of heads",
       y     = "Count",
       title = "One experiment: observed result vs. null distribution") +
  xlim(0, num_flips) +
  theme_bw()

if (p_value < alpha) {
  cat(sprintf("p-value = %.4f < %.2f  →  Reject H0. The coin appears biased!\n",
              p_value, alpha))
} else {
  cat(sprintf("p-value = %.4f ≥ %.2f  →  Fail to reject H0. Coin appears fair.\n",
              p_value, alpha))
}

# [ Add your notes here. ]


# ── Step 3: Estimate power by repeating the experiment many times ─────────────

num_experiments <- 1000   # number of independent experiments

# Draw all head-counts at once (one per experiment)
heads_per_experiment <- rbinom(n    = num_experiments,
                               size = num_flips,
                               prob = coin_bias)

# For each experiment compute the p-value and check significance
p_values <- sapply(heads_per_experiment, \(h) {
  obs_dev <- abs(h - num_flips / 2)
  mean(deviations_null > obs_dev)
})

estimated_power <- mean(p_values < alpha)
cat(sprintf("\nEstimated power: %.3f\n", estimated_power))
cat(sprintf("(num_flips=%d, alpha=%.2f, coin_bias=%.1f)\n",
            num_flips, alpha, coin_bias))

# [ Add your notes here. ]


# Question 1:
# Define the power you just obtained in terms of this specific experiment.
#
# [ Write your answer here. ]


# ── Step 4: Generate a power curve ───────────────────────────────────────────

biases <- seq(0, 1, by = 0.01)   # 101 bias values: 0.00, 0.01, …, 1.00

# For each bias level, simulate num_experiments experiments and estimate power
power_curve <- tibble(
  effect_size     = biases,
  estimated_power = sapply(biases, \(b) {
    heads_all <- rbinom(n = num_experiments, size = num_flips, prob = b)
    p_vals    <- sapply(heads_all, \(h) mean(deviations_null > abs(h - num_flips / 2)))
    mean(p_vals < alpha)
  })
)

# [ Add your notes here. ]

# Plot the power curve
power_curve |>
  ggplot(aes(x = effect_size, y = estimated_power)) +
  geom_line() +
  geom_point(size = 1) +
  geom_hline(yintercept = 0.80, colour = "firebrick", linetype = "dashed",
             linewidth = 0.8) +
  geom_vline(xintercept = 0.50, colour = "grey50",    linetype = "dotted",
             linewidth = 0.8) +
  annotate("text", x = 0.02, y = 0.82, label = "Power = 0.80",
           colour = "firebrick", hjust = 0, size = 3.5) +
  labs(
    x     = "Coin bias (true P(heads))",
    y     = "Estimated power",
    title = sprintf("Power curve  |  %d flips, alpha = %.2f", num_flips, alpha)
  ) +
  theme_bw()


# Question 2:
# What does this power curve tell you? Describe the shape, and explain what
# happens to power as the coin becomes more biased away from 0.5.
#
# [ Write your answer here. ]
