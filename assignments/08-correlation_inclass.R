# ─────────────────────────────────────────────────────────────────────────────
# Assignment 08 — In-class: Simulating the Null Distribution of Pearson r
#                           at a Fixed Sample Size
#
# Work through this script with a partner: discuss each step, add your own
# comments, run the code, and answer the questions at the end.
# ─────────────────────────────────────────────────────────────────────────────

library(tidyverse)

# set.seed() fixes the random-number sequence so every machine in the room
# gets identical draws and results are directly comparable.
set.seed(42)


# ── Parameters ────────────────────────────────────────────────────────────────

n_obs <- 10      # sample size: how many (x, y) observations per pair
n_sim <- 10000   # number of random pairs to simulate


# ── Step 1: Simulate the null distribution of Pearson r ──────────────────────

null_r <- map_dbl(seq_len(n_sim), \(i) {
  x <- runif(n_obs)
  y <- runif(n_obs)
  cor(x, y)
})

cat(sprintf("Null r  (n = %d, %d simulations):\n", n_obs, n_sim))
cat(sprintf("  Mean : %+.4f   (should be ≈ 0 — no true correlation)\n", mean(null_r)))
cat(sprintf("  SD   :  %.4f\n", sd(null_r)))
cat(sprintf("  Range: [%.3f, %.3f]\n\n", min(null_r), max(null_r)))

# [ Add your notes here. ]


# ── Step 2: Identify the significance threshold ───────────────────────────────

r_crit <- quantile(null_r, 0.95)

cat(sprintf("One-tailed critical r at n = %d (α = 0.05): r_crit = %.3f\n",
            n_obs, r_crit))
cat(sprintf("Fraction of null r values that exceed r_crit: %.3f\n\n",
            mean(null_r > r_crit)))

# [ Add your notes here. ]


# ── Step 3: Visualise the null distribution ───────────────────────────────────

p_inclass <- tibble(r = null_r) |>
  ggplot(aes(x = r)) +
  geom_histogram(bins = 50, fill = "steelblue", colour = "white", alpha = 0.8) +
  geom_vline(xintercept = r_crit, colour = "black", linewidth = 1.0) +
  annotate("text",
           x = r_crit + 0.03, y = Inf,
           label = sprintf("r = %.3f\n(95th percentile)", r_crit),
           hjust = 0, vjust = 1.4, size = 3.5) +
  labs(
    title    = sprintf("Null distribution of Pearson r  |  n = %d  |  %d simulations",
                       n_obs, n_sim),
    subtitle = "x and y are independent Uniform(0,1) — no true correlation exists",
    x        = "Pearson r",
    y        = "Count"
  ) +
  theme_bw()

ggsave("08-inclass-null-r-n10.pdf", p_inclass, width = 7, height = 4)
print(p_inclass)

# [ Add your notes here. ]


# ── Discussion questions ──────────────────────────────────────────────────────

# Question 1:
# What is the critical r you found at n = 10? Is it larger or smaller than you
# expected before running the simulation? What does the width of the histogram
# tell you about the reliability of a single correlation from a small study?
#
# [ Write your answer here. ]


# Question 2:
# The simulation used Uniform(0,1) draws for both x and y. Replace runif() to
# rnorm() (Normal) or rexp() (Exponential) and re-run. Does r_crit change?
# Explain why or why not.
#
# [ Write your answer here. ]


# Question 3:
# A colleague reports r = 0.45, n = 10 and claims a "statistically significant
# positive correlation." Based on your null distribution, is this claim
# justified? What exactly would you tell them?
#
# [ Write your answer here. ]
