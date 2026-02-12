# Software setup guide for statistics course

*Choose either **R** or **Python**. Both are fully supported.*

---

## Option 1: R Setup

### 1. Install R

* Download and install R from: [https://cran.r-project.org](https://cran.r-project.org)
* Choose your operating system and follow installation instructions.

### 2. Install RStudio (Recommended)

* Download RStudio Desktop (free version): [https://posit.co/download/rstudio-desktop/](https://posit.co/download/rstudio-desktop/)
* Install after R is installed.

RStudio provides a user-friendly interface for coding, plotting, and managing files.

---

### 3. Install Required Packages

Open RStudio and run:

```r
install.packages(c("tidyverse", "data.table"))
```

**Packages used in this course:**

* **tidyverse** → data wrangling (dplyr), plotting (ggplot2), reading data (readr)
* **data.table** → fast data manipulation (optional but useful)

Base R already includes:

* mean(), sd(), quantile(), cor()
* rnorm(), runif(), sample()
* for / while loops
* hist(), plot(), boxplot()

---

### 4. Verify Installation

Run:

```r
library(tidyverse)

x <- rnorm(100)
mean(x)
hist(x)
```

If this runs without error and produces a histogram, you're ready.

---

## Option 2: Python Setup

### 1. Install Anaconda (Recommended)

Download **Anaconda (Individual Edition)** from:
[https://www.anaconda.com/products/distribution](https://www.anaconda.com/products/distribution)

This installs:

* Python
* Jupyter Notebook
* Core scientific libraries

Follow installation instructions for your OS.

---

### 2. Create a Course Environment (Recommended)

Open **Anaconda Prompt** (or terminal) and run:

```bash
conda create -n stats_course python=3.11
conda activate stats_course
conda install numpy pandas matplotlib seaborn scipy jupyter
```

---

### 3. Required Libraries

We will use:

* **numpy** → arrays, random numbers, simulations
* **pandas** → data wrangling
* **matplotlib** → plotting
* **seaborn** → statistical visualization
* **scipy** → statistical tests

Python built-ins already support:

* for / while loops
* basic math
* random via numpy.random

---

### 4. Verify Installation

Start Jupyter:

```bash
jupyter notebook
```

In a new notebook, run:

```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

x = np.random.normal(size=100)
np.mean(x)

plt.hist(x)
plt.show()
```

If this runs and shows a histogram, you're ready.

---

# What You Should Be Able to Do

After setup, you should be able to:

* Read datasets (CSV files)
* Generate mock data
* Clean and reshape data
* Compute summary statistics (mean, sd, quantiles, correlation)
* Perform simulations
* Use loops
* Generate scatterplots, histograms, and boxplots

---

If you encounter installation issues, bring your laptop to class or post the exact error message.
