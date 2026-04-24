# High-dimensional data & ML | Week 09 Homework assignment

This assignment extends the in-class discussion to give you some more time to
think through the ideas presented in the lecture.

Write your answers in a separate text document, export as a PDF, and submit
using [this form](https://forms.gle/977e4vrVshwTyTcK7).

---

1.  **Accuracy vs. balanced accuracy calculation:** 
    Consider a clinical dataset with a 10:1 imbalance where 90% of samples are
    healthy and 10% have a disease. If a "random" predictor simply guesses that
    every patient is healthy, what is its **accuracy**?. Research the definition
    of **balanced accuracy**, calculate it for this same scenario, and explain
    why this metric is a more honest reflection of the model’s utility.
2.  **Defining and comparing evaluation curves:** 
    Define the terms **precision** and **recall** (noting that recall is
    equivalent to statistical power). Based on these definitions,
    explain why the **Precision-Recall (PR) curve** is a more effective
    evaluation tool than the **ROC curve** when you are working with a highly
    imbalanced dataset. Recall that 'recall' is an one of the axes in both
    curves!
3.  **Detecting preprocessing data leakage:** 
    Describe the specific risk of performing **Principal Component Analysis
    (PCA)** or **feature selection** on a full dataset before it has been split
    into training and testing sets. Explain why this constitutes "subliminal
    data leakage" and how it leads to an **overestimation of model
    performance**.
4.  **Prerequisites for a robust workflow:**
    Your lecture outlines essential **prerequisites for a sound computational
    analysis** across the input, model, and output stages. Choose one of these
    stages and synthesize the "ideals" described in the lecture that should
    occur at that stage to prevent **confounding variables** or **spurious
    associations** from ruining the model's reliability.
5.  **Applying the evaluation checklist:**
    Select three specific questions from the lecture’s **Benchmarking and
    Evaluation checklist** (such as questions about out-of-distribution data,
    independent validation, or practical vs. statistical significance).
    Briefly explain why each of these three questions is critical for vetting a
    new "black box" machine learning method before it is deployed in a
    real-world setting.

