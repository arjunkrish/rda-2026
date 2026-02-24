# =============================================================================
# Rethinking Data Analysis
# In-class discussion: Three ways to estimate the standard error of the mean
# =============================================================================

set.seed(42)

# =============================================================================
# PART 1: Formula-based standard error of the mean
# =============================================================================

pop1       <- rnorm(1000, mean = 50, sd = 10)
sample1    <- sample(pop1, size = 10)

samp_mean  <- mean(sample1)
samp_sd    <- sd(sample1)
samp_sem   <- samp_sd / sqrt(length(sample1))

cat("=== Part 1: Formula-based SEM ===\n")
cat(sprintf("  Sample mean : %.4f\n", samp_mean))
cat(sprintf("  Sample SD   : %.4f\n", samp_sd))
cat(sprintf("  SEM (SD/√n) : %.4f\n\n", samp_sem))


# =============================================================================
# PART 2: Empirical standard error via repeated sampling
# =============================================================================

pop2        <- rnorm(1000, mean = 50, sd = 10)
n_reps      <- 100
sample_size <- 10

sample_means <- replicate(n_reps, mean(sample(pop2, size = sample_size)))

empirical_sem <- sd(sample_means)

cat("=== Part 2: Empirical SEM (repeated sampling) ===\n")
cat(sprintf("  Number of repeated samples : %d\n", n_reps))
cat(sprintf("  Sample size per draw       : %d\n", sample_size))
cat(sprintf("  Mean of sample means       : %.4f\n", mean(sample_means)))
cat(sprintf("  SD of sample means (empirical SEM) : %.4f\n\n", empirical_sem))


# =============================================================================
# PART 3: Bootstrap standard error of the mean
# =============================================================================

observed_sample <- sample(pop2, size = 10)
n_boot          <- 1000

boot_means <- replicate(n_boot, mean(sample(observed_sample,
                                            size    = length(observed_sample),
                                            replace = TRUE)))

bootstrap_sem <- sd(boot_means)

cat("=== Part 3: Bootstrap SEM ===\n")
cat(sprintf("  Observed sample: %s\n",
            paste(round(observed_sample, 2), collapse = ", ")))
cat(sprintf("  Number of bootstrap samples : %d\n", n_boot))
cat(sprintf("  Mean of bootstrap means     : %.4f\n", mean(boot_means)))
cat(sprintf("  SD of bootstrap means (bootstrap SEM) : %.4f\n\n", bootstrap_sem))


# =============================================================================
# COMPARISON SUMMARY
# =============================================================================

cat("=== Comparison of SEM estimates ===\n")
cat(sprintf("  Formula-based SEM (Part 1) : %.4f\n", samp_sem))
cat(sprintf("  Empirical SEM  (Part 2)    : %.4f\n", empirical_sem))
cat(sprintf("  Bootstrap SEM  (Part 3)    : %.4f\n", bootstrap_sem))
cat(sprintf("  True SEM (SD_pop / √n)     : %.4f\n", sd(pop2) / sqrt(10)))


# =============================================================================
# PLOT: Distribution of sample means for each part
# =============================================================================

xlim_all <- range(c(samp_mean, sample_means, boot_means)) + c(-5, 5)

png("standard_error_plot.png", width = 1200, height = 450, res = 120)

par(mfrow = c(1, 3),
    mar   = c(5, 4, 5, 2),
    cex.main = 1.05)

plot(NA,
     xlim = xlim_all, ylim = c(0, 1),
     xlab = "Sample Mean", ylab = "",
     yaxt = "n",
     main = "Part 1: Formula-based SEM\n(one sample, n = 10)")

abline(v = 50, col = "grey60", lty = 2, lwd = 1.5)
points(samp_mean, 0.5, pch = 19, col = "steelblue", cex = 2)
arrows(samp_mean - samp_sem, 0.5,
       samp_mean + samp_sem, 0.5,
       angle = 90, code = 3, length = 0.08,
       col = "steelblue", lwd = 2)
legend("topright",
       legend = c(sprintf("mean = %.2f", samp_mean),
                  sprintf("± SEM = %.2f", samp_sem)),
       bty = "n", cex = 0.85)

hist(sample_means,
     breaks = 15,
     col    = "steelblue", border = "white",
     xlim   = xlim_all,
     main   = "Part 2: Empirical SEM\n(100 samples, n = 10 each)",
     xlab   = "Sample Mean", ylab   = "Count")

abline(v = 50,                  col = "grey60",  lty = 2, lwd = 1.5)
abline(v = mean(sample_means),  col = "red",     lwd = 2)
legend("topright",
       legend = c(sprintf("mean = %.2f",          mean(sample_means)),
                  sprintf("Empirical SEM = %.2f", empirical_sem)),
       bty = "n", cex = 0.85)

hist(boot_means,
     breaks = 30,
     col    = "steelblue", border = "white",
     xlim   = xlim_all,
     main   = "Part 3: Bootstrap SEM\n(1000 resamples, n = 10)",
     xlab   = "Bootstrap Mean", ylab = "Count")

abline(v = 50,               col = "grey60", lty = 2, lwd = 1.5)
abline(v = mean(boot_means), col = "red",    lwd = 2)
legend("topright",
       legend = c(sprintf("mean = %.2f",           mean(boot_means)),
                  sprintf("Bootstrap SEM = %.2f",  bootstrap_sem)),
       bty = "n", cex = 0.85)

dev.off()
cat("\nPlot saved to standard_error_plot.png\n")
