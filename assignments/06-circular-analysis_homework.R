# ─────────────────────────────────────────────────────────────────────────────
# Assignment 06 — Homework: Circular Analysis and Sampling Bias
#
# Work through this script on your own, add detailed comments at every step,
# and answer the questions at the end. Submit a PDF of your annotated script
# and answers via the course submission form.
# ─────────────────────────────────────────────────────────────────────────────

library(tidyverse)
library(class)      # knn() for k-nearest-neighbour classification

# set.seed() locks the random-number sequence so results are reproducible.
set.seed(42)


# ══════════════════════════════════════════════════════════════════════════════
# Exercise 1 — Circular Analysis: Cluster-then-Test on the Same Data
# ══════════════════════════════════════════════════════════════════════════════


# ── Parameters ────────────────────────────────────────────────────────────────

n_obs      <- 100   # number of observations; all drawn from a single distribution
k_clusters <- 3     # number of clusters for k-means


# ── Step 1: Simulate data from a single bivariate normal distribution ─────────

df_ex1 <- tibble(
  x = rnorm(n_obs, mean = 0, sd = 1),
  y = rnorm(n_obs, mean = 0, sd = 1)
)

cat("Exercise 1 — Data summary:\n")
cat(sprintf("  n = %d observations drawn from N(0,1) × N(0,1)\n", n_obs))
cat("  True clusters: NONE\n\n")


# ── Step 2: Apply k-means clustering ─────────────────────────────────────────

km_fit <- kmeans(df_ex1, centers = k_clusters, nstart = 25)

df_ex1 <- df_ex1 |>
  mutate(cluster = factor(km_fit$cluster))

cat("Exercise 1 — Cluster sizes after k-means:\n")
print(table(df_ex1$cluster))
cat("\n")


# ── Step 3: Helper — Cohen's d (pooled-SD effect size) ───────────────────────

cohens_d <- function(group_a, group_b) {
  n_a <- length(group_a)
  n_b <- length(group_b)
  s_pooled <- sqrt(
    ((n_a - 1) * var(group_a) + (n_b - 1) * var(group_b)) / (n_a + n_b - 2)
  )
  abs(mean(group_a) - mean(group_b)) / s_pooled
}


# ── Step 4: Test each cluster against all others ──────────────────────────────

test_cluster_vs_rest <- function(data, cluster_id) {
  in_grp  <- data |> filter(cluster == cluster_id) |> pull(x)
  out_grp <- data |> filter(cluster != cluster_id) |> pull(x)
  res     <- t.test(in_grp, out_grp)
  tibble(
    cluster     = cluster_id,
    n_in        = length(in_grp),
    n_out       = length(out_grp),
    mean_in     = mean(in_grp),
    mean_out    = mean(out_grp),
    cohens_d    = cohens_d(in_grp, out_grp),
    t_statistic = as.numeric(res$statistic),
    p_value     = res$p.value
  )
}

results_ex1 <- map_dfr(levels(df_ex1$cluster), \(cid) {
  test_cluster_vs_rest(df_ex1, cid)
})

cat("Exercise 1 — T-test results (each cluster vs. all others, tested on x):\n")
print(results_ex1 |> mutate(across(where(is.numeric), \(v) round(v, 4))))
cat("\n")


# ── Step 5: Visualise ─────────────────────────────────────────────────────────

centroids_df <- as_tibble(km_fit$centers) |>
  mutate(cluster = factor(seq_len(k_clusters)))

p_ex1_scatter <- ggplot(df_ex1, aes(x = x, y = y,
                                     colour = cluster, shape = cluster)) +
  geom_point(size = 2.5, alpha = 0.8) +
  geom_point(
    data = centroids_df,
    aes(x = x, y = y, colour = cluster),
    shape = 4, size = 5, stroke = 2, inherit.aes = FALSE
  ) +
  scale_colour_brewer(palette = "Set1") +
  labs(
    title    = "Exercise 1A — K-means clusters on pure noise",
    subtitle = sprintf("n = %d, k = %d  |  True clusters: NONE", n_obs, k_clusters),
    x = "x", y = "y", colour = "Cluster", shape = "Cluster"
  ) +
  theme_bw()

p_ex1_pvals <- results_ex1 |>
  mutate(
    neg_log10_p = -log10(p_value),
    cluster     = factor(cluster)
  ) |>
  ggplot(aes(x = cluster, y = neg_log10_p, fill = cluster)) +
  geom_col(width = 0.5, alpha = 0.85) +
  geom_hline(yintercept = -log10(0.05), linetype = "dashed",
             colour = "black", linewidth = 0.8) +
  annotate("text", x = 0.55, y = -log10(0.05) + 0.5,
           label = "p = 0.05", hjust = 0, size = 3.5) +
  scale_fill_brewer(palette = "Set1") +
  labs(
    title    = "Exercise 1B — T-test p-values (cluster vs. rest)",
    subtitle = "Inflated significance: k-means maximised what the t-test is measuring",
    x = "Cluster",
    y = expression(-log[10](p-value))
  ) +
  theme_bw() +
  theme(legend.position = "none")

ggsave("06-ex1a-cluster-scatter.pdf",  p_ex1_scatter, width = 6, height = 5)
ggsave("06-ex1b-cluster-pvalues.pdf",  p_ex1_pvals,   width = 5, height = 4)

print(p_ex1_scatter)
print(p_ex1_pvals)


# Question 1:
# Look at the p-values and effect sizes from Exercise 1. Are they what you
# would expect if the null hypothesis (no group differences) were true?
# What do they tell you — and NOT tell you — about the data?
#
# [ Write your answer here. ]


# Question 2:
# K-means minimises within-cluster sum of squares. Explain in your own words
# why that objective makes the subsequent t-test circular. What would a valid
# test of group differences require that this pipeline does not provide?
#
# [ Write your answer here. ]


# ══════════════════════════════════════════════════════════════════════════════
# Exercise 2 — Circular Analysis: A Partial Fix via Data Splitting
# ══════════════════════════════════════════════════════════════════════════════


# ── Parameters ────────────────────────────────────────────────────────────────

train_frac <- 0.60   # fraction of data used for training (clustering)
k_nn       <- 5      # number of neighbours for k-NN label propagation


# ── Step 1: Split data into training and test sets ────────────────────────────

n_train   <- floor(n_obs * train_frac)
train_idx <- sample(seq_len(n_obs), size = n_train, replace = FALSE)

df_train <- df_ex1[train_idx,  ] |> select(x, y)
df_test  <- df_ex1[-train_idx, ] |> select(x, y)

cat("Exercise 2 — Data split:\n")
cat(sprintf("  Training set: %d observations\n", nrow(df_train)))
cat(sprintf("  Test set:     %d observations\n\n", nrow(df_test)))


# ── Step 2: Apply k-means to the training set only ───────────────────────────

km_train <- kmeans(df_train, centers = k_clusters, nstart = 25)

df_train <- df_train |>
  mutate(cluster = factor(km_train$cluster), split = "train")


# ── Step 3: Propagate labels to the test set via k-NN ────────────────────────

test_labels <- knn(
  train = df_train |> select(x, y),
  test  = df_test,
  cl    = km_train$cluster,
  k     = k_nn
)

df_test <- df_test |>
  mutate(cluster = factor(test_labels), split = "test")

cat("Exercise 2 — Test-set cluster sizes (after k-NN label propagation):\n")
print(table(df_test$cluster))
cat("\n")


# ── Step 4: Test for mean differences in the test set ────────────────────────

results_ex2 <- map_dfr(levels(df_test$cluster), \(cid) {
  test_cluster_vs_rest(df_test, cid)
})

cat("Exercise 2 — T-test results on the test set (cluster vs. all others, on x):\n")
print(results_ex2 |> mutate(across(where(is.numeric), \(v) round(v, 4))))
cat("\n")


# ── Step 5: Visualise ─────────────────────────────────────────────────────────

df_both <- bind_rows(df_train, df_test) |>
  mutate(split = factor(split, levels = c("train", "test")))

p_ex2 <- ggplot(df_both, aes(x = x, y = y, colour = cluster, shape = cluster)) +
  geom_point(size = 2.5, alpha = 0.8) +
  facet_wrap(
    ~ split,
    labeller = labeller(split = c(
      train = "Training set  (k-means labels)",
      test  = "Test set  (k-NN propagated labels)"
    ))
  ) +
  scale_colour_brewer(palette = "Set1") +
  labs(
    title    = "Exercise 2 — Data splitting: training vs. test cluster labels",
    subtitle = sprintf(
      "Train = %.0f%%  |  Test = %.0f%%  |  k-NN k = %d",
      100 * train_frac, 100 * (1 - train_frac), k_nn
    ),
    x = "x", y = "y", colour = "Cluster", shape = "Cluster"
  ) +
  theme_bw()

ggsave("06-ex2-data-splitting.pdf", p_ex2, width = 9, height = 4.5)
print(p_ex2)


# Question 3:
# Compare the p-values from Exercise 2 (data splitting) with those from
# Exercise 1 (no split). Are they qualitatively different? Does data splitting
# appear to eliminate significance inflation? What does this suggest about
# treating data splitting as a universal safeguard against circular analysis?
#
# [ Write your answer here. ]


# Question 4:
# k-NN assigns test-set labels by spatial proximity to training points. In what
# sense is this still a form of double-dipping, even though the exact same rows
# are not reused? What property of a labeling rule makes a subsequent
# hypothesis test circular, regardless of whether the data are split?
#
# [ Write your answer here. ]


# ══════════════════════════════════════════════════════════════════════════════
# Exercise 3 — Circular Analysis: The Voronoi / Proximity-Labeling Variant
# ══════════════════════════════════════════════════════════════════════════════


# ── Parameters ────────────────────────────────────────────────────────────────

n_obs_ex3   <- 100           # number of observations
ref_A       <- c(x = -1, y = 0)   # reference point A
ref_B       <- c(x =  1, y = 0)   # reference point B


# ── Step 1: Generate data and compute distances to A and B ───────────────────

df_ex3 <- tibble(
  x = rnorm(n_obs_ex3),
  y = rnorm(n_obs_ex3)
) |>
  mutate(
    dist_A = sqrt((x - ref_A["x"])^2 + (y - ref_A["y"])^2),
    dist_B = sqrt((x - ref_B["x"])^2 + (y - ref_B["y"])^2)
  )


# ── Step 2: Assign Voronoi labels ─────────────────────────────────────────────

df_ex3 <- df_ex3 |>
  mutate(label = if_else(dist_A < dist_B, "green", "orange"))

cat("Exercise 3 — Group sizes from Voronoi labeling:\n")
print(table(df_ex3$label))
cat("\n")


# ── Step 3: T-test on x between the two groups ────────────────────────────────

green_x  <- df_ex3 |> filter(label == "green")  |> pull(x)
orange_x <- df_ex3 |> filter(label == "orange") |> pull(x)

res_ex3 <- t.test(green_x, orange_x)
d_ex3   <- cohens_d(green_x, orange_x)

cat("Exercise 3 — T-test result (green vs. orange, on x):\n")
cat(sprintf("  Mean x (green)  = %+.3f\n", mean(green_x)))
cat(sprintf("  Mean x (orange) = %+.3f\n", mean(orange_x)))
cat(sprintf("  Cohen's d       =  %.3f\n", d_ex3))
cat(sprintf("  t-statistic     = %+.3f\n", res_ex3$statistic))
cat(sprintf("  p-value         =  %.2e\n\n", res_ex3$p.value))


# ── Step 4: Visualise ─────────────────────────────────────────────────────────

midpoint <- (ref_A + ref_B) / 2
ab_vec   <- ref_B - ref_A          # direction of AB
perp_vec <- c(x = -ab_vec["y"], y = ab_vec["x"])   # perpendicular direction

t_ext <- 3.5   # how far to extend the bisector line in each direction
bisector_df <- tibble(
  x = midpoint["x"] + c(-t_ext, t_ext) * perp_vec["x"],
  y = midpoint["y"] + c(-t_ext, t_ext) * perp_vec["y"]
)

ref_pts_df <- tibble(
  x = c(ref_A["x"], ref_B["x"]),
  y = c(ref_A["y"], ref_B["y"]),
  pt_label = c("A", "B")
)

p_ex3 <- ggplot(df_ex3, aes(x = x, y = y, colour = label)) +
  geom_point(size = 2.5, alpha = 0.8) +
  geom_line(
    data = bisector_df, aes(x = x, y = y),
    colour = "black", linetype = "dashed", linewidth = 0.9,
    inherit.aes = FALSE
  ) +
  geom_point(
    data = ref_pts_df, aes(x = x, y = y),
    colour = "black", shape = 4, size = 5, stroke = 1.8,
    inherit.aes = FALSE
  ) +
  geom_text(
    data = ref_pts_df, aes(x = x, y = y, label = pt_label),
    colour = "black", nudge_y = 0.22, size = 5, fontface = "bold",
    inherit.aes = FALSE
  ) +
  scale_colour_manual(values = c(green = "forestgreen", orange = "darkorange")) +
  labs(
    title    = "Exercise 3 — Voronoi labeling on pure noise",
    subtitle = sprintf(
      "p = %.2e  |  Cohen's d = %.2f  |  True population difference: NONE",
      res_ex3$p.value, d_ex3
    ),
    x = "x", y = "y", colour = "Label"
  ) +
  theme_bw()

ggsave("06-ex3-voronoi-labeling.pdf", p_ex3, width = 6, height = 5)
print(p_ex3)


# Question 5:
# The Voronoi boundary here is the y-axis. How does the orientation of segment
# AB (relative to the tested variable x) affect the magnitude of the resulting
# p-value? Predict what would happen — and why — if you rotated AB to lie along
# the y-axis instead. You can test your prediction by changing ref_A and ref_B.
#
# [ Write your answer here. ]


# Question 6:
# In Exercise 2, labels were propagated by k-NN proximity. In Exercise 3,
# labels are assigned by proximity to two fixed reference points. Identify the
# shared flaw in these two procedures. State in general terms: what property of
# a labeling rule makes a subsequent hypothesis test circular?
#
# [ Write your answer here. ]


# ══════════════════════════════════════════════════════════════════════════════
# Exercise 4 — Sampling Bias: Outliers and Population Size
# ══════════════════════════════════════════════════════════════════════════════


# ── Parameters ────────────────────────────────────────────────────────────────

pop_sizes <- 10^(1:6)   # 10, 100, 1 000, 10 000, 100 000, 1 000 000
n_reps    <- 200        # repetitions per (distribution, n) cell


# ── Step 1: Define distribution samplers ──────────────────────────────────────

dist_samplers <- list(
  normal      = function(n) rnorm(n,  mean = 1,    sd = 1),
  exponential = function(n) rexp(n,   rate = 1),
  log_normal  = function(n) rlnorm(n, meanlog = 0, sdlog = 1)
)


# ── Step 2: Simulate and record the maximum for each (distribution, n) ────────

cat("Exercise 4 — Simulating maxima across population sizes:\n")

maxima_df <- map_dfr(names(dist_samplers), \(dist_name) {
  cat(sprintf("  Distribution: %-12s ...\n", dist_name))
  sampler <- dist_samplers[[dist_name]]

  map_dfr(pop_sizes, \(n) {
    maxima <- vapply(seq_len(n_reps), \(i) max(sampler(n)), numeric(1))
    tibble(
      distribution = dist_name,
      pop_size     = n,
      median_max   = median(maxima),
      q25_max      = quantile(maxima, 0.25),
      q75_max      = quantile(maxima, 0.75)
    )
  })
})

cat("\n")


# ── Step 3: Scale maxima relative to the n = 10^6 reference ──────────────────

maxima_df <- maxima_df |>
  group_by(distribution) |>
  mutate(
    ref_val    = median_max[pop_size == max(pop_sizes)],   # value at n = 10^6
    scaled_max = median_max / ref_val,
    scaled_q25 = q25_max   / ref_val,
    scaled_q75 = q75_max   / ref_val
  ) |>
  ungroup()

cat("Exercise 4 — Scaled median maximum at each population size:\n")
maxima_df |>
  select(distribution, pop_size, scaled_max) |>
  mutate(scaled_max = round(scaled_max, 3)) |>
  pivot_wider(names_from = distribution, values_from = scaled_max) |>
  print()
cat("\n")


# ── Step 4: Visualise ─────────────────────────────────────────────────────────

p_ex4 <- maxima_df |>
  mutate(
    distribution = factor(
      distribution,
      levels = c("normal", "exponential", "log_normal"),
      labels = c("Normal", "Exponential", "Log-normal")
    )
  ) |>
  ggplot(aes(
    x      = log10(pop_size),
    colour = distribution,
    fill   = distribution
  )) +
  geom_ribbon(
    aes(ymin = scaled_q25, ymax = scaled_q75),
    alpha = 0.15, colour = NA
  ) +
  geom_line(aes(y = scaled_max), linewidth = 1.0) +
  geom_point(aes(y = scaled_max), size = 2.5) +
  scale_x_continuous(
    breaks = log10(pop_sizes),
    labels = \(x) parse(text = sprintf("10^%g", x))
  ) +
  scale_colour_brewer(palette = "Dark2", name = "Distribution") +
  scale_fill_brewer(  palette = "Dark2", name = "Distribution") +
  labs(
    title    = "Exercise 4 — How the expected maximum grows with population size",
    subtitle = sprintf(
      "Median ± IQR over %d repetitions per cell  |  Scaled to n = 10\u2076 maximum",
      n_reps
    ),
    x = "Population size (log scale)",
    y = "Scaled median maximum\n(relative to n = 10\u2076)"
  ) +
  theme_bw() +
  theme(legend.position = "bottom")

ggsave("06-ex4-sampling-bias-maxima.pdf", p_ex4, width = 7, height = 5)
print(p_ex4)


# Question 7:
# The log-normal curve starts the lowest of the three distributions at n = 10.
# Explain why, in terms of the tail behaviour of each distribution. Your answer
# should reference the approximate formulas given in the comments above.
#
# [ Write your answer here. ]


# Question 8:
# World athletics records are maintained separately for each age group (under-
# 20, open, masters). Suppose a journalist reports that a 35-year-old holds a
# better marathon record than any under-20 athlete ever has. Using the
# intuition from Exercise 4, what question would you ask before accepting
# that conclusion, and what additional analysis would you propose?
#
# [ Write your answer here. ]


# Question 9:
# Rare genetic variants are far more likely to be discovered in large biobanks
# (n ~ 500 000) than in small cohort studies (n ~ 500). How does the sampling-
# bias argument from this exercise apply to interpreting effect-size estimates
# for variants initially discovered in large vs. small studies?
#
# [ Write your answer here. ]
