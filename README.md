# E-Commerce A/B Testing Project: Button Color & Text Optimization

This repository contains a complete, end-to-end data science analysis of a two-variant A/B experiment for an e-commerce website. The goal is to determine if changing the checkout button from blue with the text "Buy Now" (Control) to green with the text "Purchase Now" (Treatment) increases the customer conversion rate.

## 📊 Business Problem & Experiment Setup

- **Scenario:** The company wants to test whether changing the color/text of the "Buy Now" button increases the proportion of users completing a checkout.
- **Control Group (A):** Original blue "Buy Now" button.
- **Treatment Group (B):** New green "Purchase Now" button.
- **Primary Metric:** Binary conversion (1 = purchased, 0 = not).
- **Allocation:** 50/50 randomized split (10,000 users per group; $N = 20,000$ total).
- **Hypotheses:**
  - $H_0: p_{\text{treatment}} - p_{\text{control}} \le 0$ (No difference or treatment is worse)
  - $H_1: p_{\text{treatment}} - p_{\text{control}} > 0$ (Treatment conversion rate is higher; one-sided test)
- **Parameters:** Significance Level ($\alpha$) = 0.05, Target Power = 80%, Minimum Detectable Effect (MDE) = 2.0% absolute lift (from 5% baseline to 7%).

---

## 📈 Key Findings & Statistical Results

### 1. Exploratory Data Analysis (EDA)
- **Control Group:** 10,000 users, 500 conversions (**5.00%** conversion rate).
- **Treatment Group:** 10,000 users, 752 conversions (**7.52%** conversion rate).
- **Observed Lift:** **+2.52 percentage points** (absolute) or **+50.40%** (relative).

### 2. Hypothesis Testing
- **Two-Proportion Z-Test:**
  - $Z$-statistic: **7.3516**
  - $p$-value (one-sided): **$9.6 \times 10^{-14}$** (extremely close to 0)
  - Since $p < 0.05$, we **reject the Null Hypothesis**. The green button conversion rate is significantly higher.
- **Chi-Square Test of Independence:**
  - $\chi^2$-statistic: **52.9238**
  - $p$-value: **$3.5 \times 10^{-13}$** (confirms the Z-test results).

### 3. Confidence Intervals
- **95% Confidence Interval for Absolute Lift:** **$[1.872\%, 3.168\%]$** (calculated using the Wald method).
- Since the entire interval is above $0\%$ and its lower bound is very close to the $2.0\%$ MDE, we have high confidence in a major business impact.

### 4. Bootstrapping (Non-parametric)
- Resampling the dataset 10,000 times yielded an empirical 95% Confidence Interval of **$[1.880\%, 3.160\%]$**, which aligns closely with the parametric Wald interval.
- **Probability that Treatment > Control:** **100%** of bootstrap replicates showed positive lift.

### 5. Power Analysis
- **Pre-test Sample Size:** For an MDE of 2.0% (5% to 7%) and 80% power, the required sample size was **2,367 users per group**. Our sample size of 10,000 per group was more than sufficient.
- **Post-hoc Power:** Given our observed lift of 2.52% and $N = 10,000$, the statistical power of this experiment was **99.99%** (effectively 100%).

### 6. Projected Business Impact
Assuming **1,000,000 monthly checkout page visits** and an Average Order Value (AOV) of **$50**:
- **Additional Monthly Conversions:** +25,200 orders.
- **Additional Monthly Revenue:** **+$1,260,000**!
- **Rollout Recommendation:** **Roll out the green "Purchase Now" button immediately.**

---

## 📁 Repository Structure

```
.
├── data/
│   └── ab_data.csv                    # Simulated user conversions log (20k rows)
├── notebooks/
│   └── ab_testing_analysis.ipynb      # Main Jupyter notebook with plots and markdown
├── src/
│   ├── __init__.py
│   ├── generate_data.py               # Data simulation script
│   └── stats_utils.py                 # Statistical helpers (confidence intervals, bootstrapping, power curves)
├── requirements.txt                   # Project package dependencies
└── README.md                          # Case study and execution guide
```

---

## 🚀 How to Run the Project Locally

### 1. Set Up the Virtual Environment
Create and activate a virtual environment to isolate project packages:
```bash
# Create the virtual environment
python -m venv .venv

# Activate it (Windows PowerShell)
.venv\Scripts\Activate.ps1

# Activate it (Windows Command Prompt)
.venv\Scripts\activate.bat

# Activate it (macOS/Linux)
source .venv/bin/activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Generate the Simulation Data
(Optional, as the dataset is already generated, but you can recreate or customize it):
```bash
python src/generate_data.py
```

### 4. Open the Jupyter Notebook
```bash
jupyter notebook notebooks/ab_testing_analysis.ipynb
```
Run all cells in the notebook to view the charts and statistical testing steps.

---

## 🛠️ Tech Stack & Skills Highlighted
- **Languages:** Python
- **Data Manipulation:** `pandas`, `numpy`
- **Statistical Analysis:** `scipy.stats`, `statsmodels`
- **Visualization:** `matplotlib`, `seaborn`
- **A/B Testing Methodologies:** Two-proportion Z-test, Chi-Square test, Power Analysis (Pre-hoc and Post-hoc), Bootstrapping (Non-parametric resampling), Wald Confidence Intervals.
