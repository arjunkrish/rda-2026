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

library(tidyverse)

# [ Add your notes here. ]


# Nested simulation: for each combination of effect_size, std_deviation,
# and sample_size, simulate two groups and record the t-test p-value.

effect_sizes <- seq(0.1, 1, by = 0.05)
std_devs     <- c(0.5, 1, 2)
sample_sizes <- c(5, 10, 20, 50, 100, 200, 500, 1000)

n_combos     <- length(effect_sizes) * length(std_devs) * length(sample_sizes)
results_list <- vector("list", n_combos)
idx          <- 1L

for (effect_size in effect_sizes) {
  for (stddev in std_devs) {
    for (sample_size in sample_sizes) {

      group1 <- rnorm(sample_size, mean = 0,           sd = stddev)
      group2 <- rnorm(sample_size, mean = effect_size, sd = stddev)

      ttest_result <- t.test(group1, group2)

      results_list[[idx]] <- c(
        effect_size   = effect_size,
        std_deviation = stddev,
        sample_size   = sample_size,
        pvalue        = ttest_result$p.value
      )

      idx <- idx + 1L
    }
  }
}

es_sd_ss_pvalue <- as_tibble(do.call(rbind, results_list))
print(es_sd_ss_pvalue)

# [ Add your notes here. ]


# Add a column flagging whether p < 0.05

es_sd_ss_pvalue <- es_sd_ss_pvalue |>
  mutate(pvalue_below_thresh = pvalue < 0.05)

# [ Add your notes here. ]


# Three-panel plot: one panel per std_deviation value.
# x-axis: sample_size (log scale); y-axis: effect_size;
# color/shape: whether p < 0.05 (red circle) or not (blue cross).

plot_es_sd_ss_pvalue <- es_sd_ss_pvalue |>
  ggplot(aes(
    x     = sample_size,
    y     = effect_size,
    color = pvalue_below_thresh,
    shape = pvalue_below_thresh
  )) +
  geom_point(size = 2.5, alpha = 0.8) +
  scale_shape_manual(
    values = c(`FALSE` = 4, `TRUE` = 16),
    labels = c("p >= 0.05", "p < 0.05")
  ) +
  scale_color_manual(
    values = c(`FALSE` = "dodgerblue", `TRUE` = "firebrick"),
    labels = c("p >= 0.05", "p < 0.05")
  ) +
  scale_x_log10(breaks = c(5, 10, 20, 50, 100, 200, 500, 1000)) +
  facet_wrap(
    ~ std_deviation,
    nrow     = 1,
    labeller = labeller(std_deviation = \(x) paste("SD =", x))
  ) +
  labs(
    title = "Which combinations of effect size, SD, and sample size yield p < 0.05?",
    x     = "Sample size (log scale)",
    y     = "Effect size",
    color = "Significance",
    shape = "Significance"
  ) +
  theme_bw(base_size = 12) +
  theme(legend.position = "bottom")

print(plot_es_sd_ss_pvalue)

ggsave(
  filename = "effectsize_variance_samplesize_pvalue.pdf",
  plot     = plot_es_sd_ss_pvalue,
  width    = 12,
  height   = 5
)


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

set.seed(42)
data <- rnorm(200)

hist(data,
     breaks = 20,
     col    = "lightsteelblue",
     border = "white",
     xlab   = "Value",
     main   = "200 observations from a single Normal(0, 1) distribution")

# [ Add your notes here. ]


# Initialise counters
attempts <- 0
pvalue   <- 1


# Keep splitting the data randomly into two groups until p < 0.05

all_indices <- seq_along(data)

while (pvalue > 0.05) {
  attempts <- attempts + 1

  case_indices    <- sample(all_indices, size = 100, replace = FALSE)
  control_indices <- setdiff(all_indices, case_indices)

  cases    <- data[case_indices]
  controls <- data[control_indices]

  pvalue <- t.test(cases, controls)$p.value
}

cat(sprintf(
  "\"Significant\" result found! p = %.4f after %d attempt(s).\n",
  pvalue, attempts
))

# [ Add your notes here. ]


# Question (Part 3):
# What does this coding exercise have to do with p-hacking?
#
# [ Write your answer here. ]
