# ─────────────────────────────────────────────────────────────────────────────
# Assignment 08 — Homework: How Does Sample Size Shape the Null Distribution
#                           of Correlation Coefficients?
#
# Work through this script on your own, add detailed comments at every step,
# and answer the questions at the end. Submit a PDF of your annotated script
# and answers via the course submission form.
# ─────────────────────────────────────────────────────────────────────────────

library(tidyverse)

set.seed(42)


# ── Parameters ────────────────────────────────────────────────────────────────

sample_sizes <- c(5, 10, 20, 50, 100)   # sample sizes to explore
n_sim        <- 10000                    # simulations per sample size


# ── Step 1: Simulate null distributions for every sample size ─────────────────

cat("Simulating null distributions:\n")

null_df <- map_dfr(sample_sizes, \(n) {
  cat(sprintf("  n = %d ...\n", n))
  tibble(
    n_obs = n,
    r     = map_dbl(seq_len(n_sim), \(i) cor(runif(n), runif(n)))
  )
})

cat("\n")


# ── Step 2: Compute the one-tailed 95th-percentile threshold for each n ───────

thresh_df <- null_df |>
  group_by(n_obs) |>
  summarise(
    r_crit = quantile(r, 0.95),
    r_sd   = sd(r),
    .groups = "drop"
  )

thresh_df <- thresh_df |>
  mutate(r_crit_theory = 1.645 / sqrt(n_obs - 1))

cat("One-tailed critical r at each sample size:\n")
print(thresh_df |> mutate(across(where(is.numeric), \(v) round(v, 4))))
cat("\n")


# ── Step 3: Visualise — stacked histograms with threshold lines ───────────────

null_df_plot <- null_df |>
  mutate(n_obs_label = factor(sprintf("n = %d", n_obs),
                              levels = sprintf("n = %d", sample_sizes)))

thresh_plot <- thresh_df |>
  mutate(n_obs_label = factor(sprintf("n = %d", n_obs),
                              levels = sprintf("n = %d", sample_sizes)))

p_hist <- null_df_plot |>
  ggplot(aes(x = r, fill = n_obs_label)) +
  geom_histogram(bins = 50, colour = "white", alpha = 0.85) +
  geom_vline(data  = thresh_plot,
             aes(xintercept = r_crit),
             colour = "black", linewidth = 0.9) +
  facet_wrap(~ n_obs_label, ncol = 1, scales = "free_y") +
  scale_fill_brewer(palette = "Blues", direction = 1) +
  labs(
    title    = sprintf("Null distribution of Pearson r  |  %d simulations per n",
                       n_sim),
    subtitle = "Vertical line = one-tailed critical r at α = 0.05",
    x        = "Pearson r",
    y        = "Count"
  ) +
  theme_bw() +
  theme(legend.position = "none")

ggsave("08-hw-null-r-by-n.pdf", p_hist, width = 7, height = 11)
print(p_hist)


# ── Step 4: Visualise — critical r as a function of sample size ───────────────

n_grid <- seq(4, 110, by = 1)

p_thresh <- thresh_df |>
  ggplot(aes(x = n_obs)) +
  geom_line(aes(y = r_crit), colour = "steelblue", linewidth = 1.0) +
  geom_point(aes(y = r_crit), colour = "steelblue", size = 3.0) +
  geom_line(
    data = tibble(n = n_grid, r_theory = 1.645 / sqrt(n_grid - 1)),
    aes(x = n, y = r_theory),
    colour = "black", linewidth = 0.7, linetype = "dashed",
    inherit.aes = FALSE
  ) +
  annotate("text", x = 75, y = 0.52, label = "Simulated",
           colour = "steelblue", size = 3.5, hjust = 0) +
  annotate("text", x = 75, y = 0.46,
           label = "Theory: 1.645 / \u221a(n\u22121)",
           colour = "black", size = 3.5, hjust = 0) +
  labs(
    title    = "Critical r (one-tailed α = 0.05) vs. sample size",
    subtitle = "Even a small correlation is 'significant' at very large n",
    x        = "Sample size (n)",
    y        = "Critical r"
  ) +
  theme_bw()

ggsave("08-hw-rcrit-vs-n.pdf", p_thresh, width = 6, height = 4)
print(p_thresh)


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
