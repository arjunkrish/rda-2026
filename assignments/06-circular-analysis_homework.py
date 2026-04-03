# ─────────────────────────────────────────────────────────────────────────────
# Assignment 06 — Homework: Circular Analysis and Sampling Bias
#
# Work through this script on your own, add detailed comments at every step,
# and answer the questions at the end. Submit a PDF of your annotated script
# and answers via the course submission form.
# ─────────────────────────────────────────────────────────────────────────────

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from scipy import stats
from sklearn.cluster import KMeans
from sklearn.neighbors import KNeighborsClassifier

# np.random.default_rng() creates a reproducible random-number generator.
rng = np.random.default_rng(seed=42)


# ══════════════════════════════════════════════════════════════════════════════
# Exercise 1 — Circular Analysis: Cluster-then-Test on the Same Data
# ══════════════════════════════════════════════════════════════════════════════


# ── Parameters ────────────────────────────────────────────────────────────────

n_obs      = 100   # number of observations; all drawn from a single distribution
k_clusters = 3     # number of clusters for k-means


# ── Step 1: Simulate data from a single bivariate normal distribution ─────────

data_ex1 = rng.standard_normal((n_obs, 2))   # shape (n_obs, 2): columns are x, y

print("Exercise 1 — Data summary:")
print(f"  n = {n_obs} observations drawn from N(0,1) × N(0,1)")
print("  True clusters: NONE\n")


# ── Step 2: Apply k-means clustering ─────────────────────────────────────────

km_ex1 = KMeans(n_clusters=k_clusters, n_init=25, random_state=42)
km_ex1.fit(data_ex1)
labels_ex1 = km_ex1.labels_   # integer cluster IDs: 0, 1, …, k_clusters-1

print("Exercise 1 — Cluster sizes after k-means:")
unique, counts = np.unique(labels_ex1, return_counts=True)
for cid, cnt in zip(unique, counts):
    print(f"  Cluster {cid}: {cnt} observations")
print()


# ── Step 3: Helper — Cohen's d (pooled-SD effect size) ───────────────────────

def cohens_d(a, b):
    """Pooled-SD Cohen's d effect size between two 1-D arrays."""
    n_a, n_b = len(a), len(b)
    s_pooled = np.sqrt(
        ((n_a - 1) * np.var(a, ddof=1) + (n_b - 1) * np.var(b, ddof=1))
        / (n_a + n_b - 2)
    )
    return abs(np.mean(a) - np.mean(b)) / s_pooled


# ── Step 4: Test each cluster against all others ──────────────────────────────

def test_cluster_vs_rest(x_all, labels, cluster_id):
    """
    Two-sample t-test + Cohen's d comparing x values in cluster_id
    against x values in all other clusters combined.
    Returns a dict of summary statistics.
    """
    in_mask  = labels == cluster_id
    in_grp   = x_all[in_mask]
    out_grp  = x_all[~in_mask]
    res = stats.ttest_ind(in_grp, out_grp, equal_var=False)
    return {
        "cluster":     cluster_id,
        "n_in":        len(in_grp),
        "n_out":       len(out_grp),
        "mean_in":     np.mean(in_grp),
        "mean_out":    np.mean(out_grp),
        "cohens_d":    cohens_d(in_grp, out_grp),
        "t_statistic": res.statistic,
        "p_value":     res.pvalue,
    }

x_ex1        = data_ex1[:, 0]   # x-coordinates only (column 0)
results_ex1  = [test_cluster_vs_rest(x_ex1, labels_ex1, cid)
                for cid in range(k_clusters)]

print("Exercise 1 — T-test results (each cluster vs. all others, tested on x):")
header = f"  {'Cluster':>7}  {'n_in':>5}  {'mean_in':>8}  {'mean_out':>9}  "
header += f"{'Cohen d':>7}  {'t-stat':>7}  {'p-value':>10}"
print(header)
for r in results_ex1:
    print(f"  {r['cluster']:>7}  {r['n_in']:>5}  {r['mean_in']:>8.4f}  "
          f"{r['mean_out']:>9.4f}  {r['cohens_d']:>7.4f}  "
          f"{r['t_statistic']:>7.4f}  {r['p_value']:>10.2e}")
print()


# ── Step 5: Visualise ─────────────────────────────────────────────────────────

CLUSTER_COLORS = [cm.Set1(i / 8) for i in range(k_clusters)]

# ── Figure 1A: scatter ────────────────────────────────────────────────────────
fig1a, ax1a = plt.subplots(figsize=(6, 5))

for cid in range(k_clusters):
    mask = labels_ex1 == cid
    ax1a.scatter(data_ex1[mask, 0], data_ex1[mask, 1],
                 color=CLUSTER_COLORS[cid], label=f"Cluster {cid}",
                 s=50, alpha=0.8, zorder=2)

for cid, centroid in enumerate(km_ex1.cluster_centers_):
    ax1a.scatter(*centroid, color=CLUSTER_COLORS[cid],
                 marker="x", s=150, linewidths=2.0, zorder=3)

ax1a.set_xlabel("x")
ax1a.set_ylabel("y")
ax1a.set_title(
    f"Exercise 1A — K-means clusters on pure noise\n"
    f"n = {n_obs}, k = {k_clusters}  |  True clusters: NONE"
)
ax1a.legend(title="Cluster")
ax1a.grid(True, linestyle="--", alpha=0.4)
fig1a.tight_layout()
fig1a.savefig("06-ex1a-cluster-scatter.pdf")
plt.show()

# ── Figure 1B: p-value bar chart ──────────────────────────────────────────────
fig1b, ax1b = plt.subplots(figsize=(5, 4))

cluster_ids  = [r["cluster"] for r in results_ex1]
neg_log10_ps = [-np.log10(r["p_value"]) for r in results_ex1]

ax1b.bar(cluster_ids, neg_log10_ps,
         color=CLUSTER_COLORS[:k_clusters], width=0.5, alpha=0.85)
ax1b.axhline(-np.log10(0.05), color="black", linestyle="--", linewidth=0.9)
ax1b.text(-0.45, -np.log10(0.05) + 0.5, "p = 0.05", fontsize=9)
ax1b.set_xlabel("Cluster")
ax1b.set_ylabel(r"$-\log_{10}$(p-value)")
ax1b.set_xticks(cluster_ids)
ax1b.set_title(
    "Exercise 1B — T-test p-values (cluster vs. rest)\n"
    "Inflated significance: k-means maximised what the t-test is measuring"
)
ax1b.grid(True, linestyle="--", alpha=0.4, axis="y")
fig1b.tight_layout()
fig1b.savefig("06-ex1b-cluster-pvalues.pdf")
plt.show()


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

train_frac = 0.60   # fraction of data used for training (clustering)
k_nn       = 5      # number of neighbours for k-NN label propagation


# ── Step 1: Split data into training and test sets ────────────────────────────

n_train   = int(n_obs * train_frac)
train_idx = rng.choice(n_obs, size=n_train, replace=False)
test_idx  = np.setdiff1d(np.arange(n_obs), train_idx)

X_train = data_ex1[train_idx]
X_test  = data_ex1[test_idx]

print("Exercise 2 — Data split:")
print(f"  Training set: {len(train_idx)} observations")
print(f"  Test set:     {len(test_idx)} observations\n")


# ── Step 2: Apply k-means to the training set only ───────────────────────────

km_train = KMeans(n_clusters=k_clusters, n_init=25, random_state=42)
km_train.fit(X_train)
labels_train = km_train.labels_


# ── Step 3: Propagate labels to the test set via k-NN ────────────────────────

knn_clf     = KNeighborsClassifier(n_neighbors=k_nn)
knn_clf.fit(X_train, labels_train)
labels_test = knn_clf.predict(X_test)

print("Exercise 2 — Test-set cluster sizes (after k-NN label propagation):")
unique_test, counts_test = np.unique(labels_test, return_counts=True)
for cid, cnt in zip(unique_test, counts_test):
    print(f"  Cluster {cid}: {cnt} observations")
print()


# ── Step 4: Test for mean differences in the test set ────────────────────────

x_test      = X_test[:, 0]   # x-coordinate of test points only
results_ex2 = [test_cluster_vs_rest(x_test, labels_test, cid)
               for cid in sorted(np.unique(labels_test))]

print("Exercise 2 — T-test results on the test set (cluster vs. all others, on x):")
print(header)   # reuse header string from Exercise 1
for r in results_ex2:
    print(f"  {r['cluster']:>7}  {r['n_in']:>5}  {r['mean_in']:>8.4f}  "
          f"{r['mean_out']:>9.4f}  {r['cohens_d']:>7.4f}  "
          f"{r['t_statistic']:>7.4f}  {r['p_value']:>10.2e}")
print()


# ── Step 5: Visualise ─────────────────────────────────────────────────────────

fig2, (ax2a, ax2b) = plt.subplots(1, 2, figsize=(9, 4.5), sharey=True)

for cid in range(k_clusters):
    mask_tr = labels_train == cid
    ax2a.scatter(X_train[mask_tr, 0], X_train[mask_tr, 1],
                 color=CLUSTER_COLORS[cid], label=f"Cluster {cid}",
                 s=50, alpha=0.8)
    mask_te = labels_test == cid
    ax2b.scatter(X_test[mask_te, 0], X_test[mask_te, 1],
                 color=CLUSTER_COLORS[cid], label=f"Cluster {cid}",
                 s=50, alpha=0.8)

for ax, title in zip(
    [ax2a, ax2b],
    ["Training set  (k-means labels)", "Test set  (k-NN propagated labels)"]
):
    ax.set_xlabel("x")
    ax.set_title(title)
    ax.legend(title="Cluster", fontsize=8)
    ax.grid(True, linestyle="--", alpha=0.4)

ax2a.set_ylabel("y")
fig2.suptitle(
    f"Exercise 2 — Data splitting: training vs. test cluster labels\n"
    f"Train = {100*train_frac:.0f}%  |  Test = {100*(1-train_frac):.0f}%  "
    f"|  k-NN k = {k_nn}",
    y=1.02
)
fig2.tight_layout()
fig2.savefig("06-ex2-data-splitting.pdf", bbox_inches="tight")
plt.show()


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

n_obs_ex3 = 100                         # number of observations
ref_A     = np.array([-1.0, 0.0])      # reference point A
ref_B     = np.array([ 1.0, 0.0])      # reference point B


# ── Step 1: Generate data and compute distances to A and B ───────────────────

data_ex3 = rng.standard_normal((n_obs_ex3, 2))

dist_A = np.linalg.norm(data_ex3 - ref_A, axis=1)   # shape (n_obs_ex3,)
dist_B = np.linalg.norm(data_ex3 - ref_B, axis=1)


# ── Step 2: Assign Voronoi labels ─────────────────────────────────────────────

labels_ex3 = np.where(dist_A < dist_B, "green", "orange")

print("Exercise 3 — Group sizes from Voronoi labeling:")
for lbl in ["green", "orange"]:
    print(f"  {lbl}: {np.sum(labels_ex3 == lbl)} observations")
print()


# ── Step 3: T-test on x between the two groups ────────────────────────────────

green_x  = data_ex3[labels_ex3 == "green",  0]
orange_x = data_ex3[labels_ex3 == "orange", 0]

res_ex3 = stats.ttest_ind(green_x, orange_x, equal_var=False)
d_ex3   = cohens_d(green_x, orange_x)

print("Exercise 3 — T-test result (green vs. orange, on x):")
print(f"  Mean x (green)  = {np.mean(green_x):+.3f}")
print(f"  Mean x (orange) = {np.mean(orange_x):+.3f}")
print(f"  Cohen's d       =  {d_ex3:.3f}")
print(f"  t-statistic     = {res_ex3.statistic:+.3f}")
print(f"  p-value         =  {res_ex3.pvalue:.2e}\n")


# ── Step 4: Visualise ─────────────────────────────────────────────────────────

midpoint = (ref_A + ref_B) / 2
ab_vec   = ref_B - ref_A
perp_vec = np.array([-ab_vec[1], ab_vec[0]])   # rotate AB by 90 degrees

t_ext = 3.5   # how far to extend the bisector in each direction
bisect_pts = np.array([
    midpoint - t_ext * perp_vec,
    midpoint + t_ext * perp_vec
])

fig3, ax3 = plt.subplots(figsize=(6, 5))

for lbl, color in [("green", "forestgreen"), ("orange", "darkorange")]:
    mask = labels_ex3 == lbl
    ax3.scatter(data_ex3[mask, 0], data_ex3[mask, 1],
                color=color, label=lbl.capitalize(), s=50, alpha=0.8, zorder=2)

ax3.plot(bisect_pts[:, 0], bisect_pts[:, 1],
         "k--", linewidth=1.0, zorder=1, label="_bisector")

for pt, name in [(ref_A, "A"), (ref_B, "B")]:
    ax3.scatter(*pt, color="black", marker="x", s=150, linewidths=2.0, zorder=3)
    ax3.text(pt[0], pt[1] + 0.22, name, ha="center", fontsize=12,
             fontweight="bold")

ax3.set_xlabel("x")
ax3.set_ylabel("y")
ax3.set_title(
    f"Exercise 3 — Voronoi labeling on pure noise\n"
    f"p = {res_ex3.pvalue:.2e}  |  Cohen's d = {d_ex3:.2f}  |  "
    f"True population difference: NONE"
)
ax3.legend()
ax3.grid(True, linestyle="--", alpha=0.4)
fig3.tight_layout()
fig3.savefig("06-ex3-voronoi-labeling.pdf")
plt.show()


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

pop_sizes = [10**k for k in range(1, 7)]   # 10, 100, …, 1 000 000
n_reps    = 200                            # repetitions per (distribution, n) cell


# ── Step 1: Define distribution samplers ──────────────────────────────────────

dist_samplers = {
    "normal":      lambda n: rng.normal(loc=1.0, scale=1.0, size=n),
    "exponential": lambda n: rng.exponential(scale=1.0, size=n),
    "log_normal":  lambda n: rng.lognormal(mean=0.0, sigma=1.0, size=n),
}


# ── Step 2: Simulate and record the maximum for each (distribution, n) ────────

print("Exercise 4 — Simulating maxima across population sizes:")

maxima_results = {dist_name: {} for dist_name in dist_samplers}

for dist_name, sampler in dist_samplers.items():
    print(f"  Distribution: {dist_name} ...")
    for n in pop_sizes:
        maxima = np.array([np.max(sampler(n)) for _ in range(n_reps)])
        maxima_results[dist_name][n] = {
            "median_max": float(np.median(maxima)),
            "q25_max":    float(np.percentile(maxima, 25)),
            "q75_max":    float(np.percentile(maxima, 75)),
        }

print()


# ── Step 3: Scale maxima relative to the n = 10^6 reference ──────────────────

max_n = max(pop_sizes)   # = 10^6

scaled = {}
for dist_name in dist_samplers:
    ref_val = maxima_results[dist_name][max_n]["median_max"]
    scaled[dist_name] = {
        "log10_n":   [np.log10(n) for n in pop_sizes],
        "median":    [maxima_results[dist_name][n]["median_max"] / ref_val
                      for n in pop_sizes],
        "q25":       [maxima_results[dist_name][n]["q25_max"]    / ref_val
                      for n in pop_sizes],
        "q75":       [maxima_results[dist_name][n]["q75_max"]    / ref_val
                      for n in pop_sizes],
    }

print("Exercise 4 — Scaled median maximum at each population size:")
col_width = 13
header_row  = f"  {'pop_size':>10}" + "".join(
    f"  {d:>{col_width}}" for d in dist_samplers
)
print(header_row)
for i, n in enumerate(pop_sizes):
    row = f"  {n:>10}"
    for dist_name in dist_samplers:
        val = scaled[dist_name]["median"][i]
        row += f"  {val:>{col_width}.3f}"
    print(row)
print()


# ── Step 4: Visualise ─────────────────────────────────────────────────────────

DIST_COLORS = {
    "normal":      "#1B9E77",
    "exponential": "#D95F02",
    "log_normal":  "#7570B3",
}
DIST_LABELS = {
    "normal":      "Normal",
    "exponential": "Exponential",
    "log_normal":  "Log-normal",
}
MARKERS = {"normal": "o", "exponential": "s", "log_normal": "^"}

fig4, ax4 = plt.subplots(figsize=(7, 5))

for dist_name in dist_samplers:
    log10_n = scaled[dist_name]["log10_n"]
    med     = scaled[dist_name]["median"]
    q25     = scaled[dist_name]["q25"]
    q75     = scaled[dist_name]["q75"]
    color   = DIST_COLORS[dist_name]

    ax4.fill_between(log10_n, q25, q75, alpha=0.15, color=color)
    ax4.plot(log10_n, med,
             color=color, linewidth=1.0,
             marker=MARKERS[dist_name], markersize=6,
             label=DIST_LABELS[dist_name])

ax4.set_xticks([np.log10(n) for n in pop_sizes])
ax4.set_xticklabels([fr"$10^{{{k}}}$" for k in range(1, 7)])
ax4.set_xlabel("Population size (log scale)")
ax4.set_ylabel(r"Scaled median maximum" "\n" r"(relative to $n = 10^6$)")
ax4.set_title(
    "Exercise 4 — How the expected maximum grows with population size\n"
    f"Median ± IQR over {n_reps} repetitions per cell  |  "
    r"Scaled to $n = 10^6$ maximum"
)
ax4.legend(title="Distribution", loc="lower right")
ax4.grid(True, linestyle="--", alpha=0.4)
fig4.tight_layout()
fig4.savefig("06-ex4-sampling-bias-maxima.pdf")
plt.show()


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
