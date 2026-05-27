# App Recommendation A/B Test Analytics

> An end-to-end product data science project evaluating whether a new in-app recommendation/progression module improves user retention using A/B testing, SQL funnel analysis, confidence intervals, heterogeneous treatment effect analysis, and a Streamlit dashboard.

---

## 1. Project Overview

This project simulates a real-world product data science workflow. A mobile app tested a redesigned **in-app recommendation/progression module** that changes when users are exposed to the next recommended content gate — moving it from round 30 to round 40.

The role taken in this project is **Product Data Scientist**: define metrics, run the statistical analysis, and deliver a clear launch/no-launch recommendation to the product team.

---

## 2. Business Problem

The product team wants to know:

1. Did the new module improve **1-day retention**?
2. Did the new module improve **7-day retention**?
3. Did it increase **user engagement** (total game rounds)?
4. Is the treatment effect **statistically significant**?
5. Are some **user segments** affected differently?
6. Should the product team **launch the new module globally**?

---

## 3. Dataset

**Source:** [Cookie Cats Mobile Games A/B Testing](https://www.kaggle.com/datasets/yufengsui/mobile-games-ab-testing) (Kaggle)

| Field | Description |
|---|---|
| `userid` | Unique user identifier |
| `version` | Experiment group: `gate_30` (control) or `gate_40` (treatment) |
| `sum_gamerounds` | Total game rounds played in the first 14 days after install |
| `retention_1` | Whether the user returned on Day 1 |
| `retention_7` | Whether the user returned on Day 7 |

**Experiment groups:**

| Group | Label | Description |
|---|---|---|
| `gate_30` | Control | Original version — progression gate at round 30 |
| `gate_40` | Treatment | New recommendation/progression module — gate moved to round 40 |

---

## 4. Experiment Design

- **Unit of analysis:** Individual user
- **Randomisation:** Users randomly assigned to control or treatment at install
- **Primary metric:** 7-day retention (`retention_7`)
- **Secondary metrics:** 1-day retention (`retention_1`), average game rounds (`sum_gamerounds`)
- **Test type:** Two-proportion z-test (two-tailed), supplemented by bootstrap confidence intervals

> **Why D7 retention as primary metric?**
> D1 retention reflects short-term return behaviour, while D7 retention is more relevant to sustained user engagement and product stickiness.

---

## 5. Methodology

1. **Data Cleaning** — Check for missing values, duplicate user IDs, invalid experiment labels, and engagement outliers
2. **SQL Funnel Analysis** — Build engagement funnel using game-round thresholds (user-level data, not event-level)
3. **Sample Balance Diagnostics** — Compare treatment/control sample sizes and engagement distributions
4. **A/B Test Analysis** — Estimate D1 and D7 retention uplift, run two-proportion z-tests, compute 95% confidence intervals
5. **Engagement Analysis** — Compare game-round distributions using Mann-Whitney U test and bootstrap CI
6. **Segment Analysis** — Estimate heterogeneous treatment effects across engagement-level segments
7. **Logistic Regression** — Robustness check with interaction terms to control for engagement differences
8. **Dashboard** — Streamlit dashboard communicating results and product recommendation

---

## 6. Key Results

> *(To be filled after analysis)*

---

## 7. Final Recommendation

> *(To be filled after analysis)*

---

## 8. Limitations

- The dataset is user-level, not event-level — the engagement funnel is constructed from game-round thresholds rather than actual user journey events
- No pre-experiment covariates are available; sample balance is diagnostic only, not proof of randomisation quality
- Engagement segments (`low`, `medium`, `high`) are post-treatment constructs and may partially reflect treatment effects

---

## 9. Repository Structure

```
app-recommendation-ab-test-analytics/
├── README.md
├── requirements.txt
├── .gitignore
├── data/
│   ├── raw/                    # Original dataset
│   │   └── cookie_cats.csv
│   ├── processed/              # Cleaned dataset
│   └── app_ab_test.db          # SQLite database
├── notebooks/
│   ├── 01_data_cleaning.ipynb
│   ├── 02_sql_funnel_analysis.ipynb
│   ├── 03_ab_test_retention_analysis.ipynb
│   ├── 04_segment_analysis.ipynb
│   └── 05_dashboard_preparation.ipynb
├── sql/
│   ├── create_tables.sql
│   ├── funnel_analysis.sql
│   ├── retention_analysis.sql
│   └── segment_analysis.sql
├── src/
│   ├── data_cleaning.py
│   ├── database.py
│   ├── metrics.py
│   ├── ab_testing.py
│   ├── segment_analysis.py
│   └── visualization.py
├── app/
│   └── streamlit_app.py
├── reports/
│   ├── experiment_report.md
│   └── executive_summary.md
├── outputs/
│   ├── figures/
│   └── tables/
└── tests/
    ├── test_metrics.py
    └── test_ab_testing.py
```

---

## 10. How to Run

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run notebooks in order (notebooks/)
jupyter lab

# 3. Launch dashboard
streamlit run app/streamlit_app.py
```

---

## Tech Stack

`Python` · `pandas` · `scipy` · `statsmodels` · `SQLite` · `SQL` · `Streamlit` · `Plotly` · `Jupyter`
