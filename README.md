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
3. Is the treatment effect **statistically significant**?
4. Are some **user segments** affected differently?
5. Should the product team **launch the new module globally**?

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

| Group | Label | Description |
|---|---|---|
| `gate_30` | Control | Original version — progression gate at round 30 |
| `gate_40` | Treatment | New module — gate moved to round 40 |

---

## 4. Experiment Design

- **Unit of analysis:** Individual user
- **Randomisation:** Users randomly assigned at install time
- **Sample size:** 90,189 users (Control: 44,700 / Treatment: 45,489)
- **Primary metric:** 7-day retention (`retention_7`)
- **Secondary metrics:** 1-day retention (`retention_1`), total game rounds
- **Test type:** Two-proportion z-test (two-tailed), 95% confidence intervals

> **Why D7 retention as primary metric?**
> D1 retention reflects short-term return behaviour. D7 retention is more relevant to sustained engagement and product stickiness — a better signal of long-term value.

---

## 5. Methodology

1. **Data Cleaning** — Checked missing values, duplicate user IDs, invalid experiment labels, and engagement outliers
2. **SQL Database** — Loaded cleaned data into SQLite for SQL-based querying
3. **SQL Funnel Analysis** — Built engagement funnel using game-round thresholds (user-level data, not event-level)
4. **Sample Balance Diagnostics** — Compared treatment and control sample sizes and engagement distributions
5. **A/B Test Analysis** — Estimated D1 and D7 retention uplift, ran two-proportion z-tests, computed 95% confidence intervals
6. **Segment Analysis** — Estimated heterogeneous treatment effects across engagement-level segments (non_player / low / medium / high)
7. **Dashboard** — Streamlit dashboard communicating results and product recommendation

---

## 6. Key Results

### Overall Retention

| Metric | Control (gate_30) | Treatment (gate_40) | Uplift | p-value | Significant |
|---|---|---|---|---|---|
| D1 Retention | 44.82% | 44.23% | -0.59pp | 0.074 | No |
| **D7 Retention** | **19.02%** | **18.20%** | **-0.82pp** | **0.002** | **Yes** |

The treatment group's D7 retention was 0.82 percentage points lower than control. The 95% confidence interval [-1.33pp, -0.31pp] is entirely below zero, confirming this is not random variation.

### Segment-level D7 Retention

| Segment | Control | Treatment | Uplift | p-value | Significant |
|---|---|---|---|---|---|
| Non-player (0 rounds) | 0.8% | 0.6% | -0.19pp | 0.470 | No |
| Low (1-4 rounds) | 1.2% | 1.4% | +0.19pp | 0.256 | No |
| **Medium (5-29 rounds)** | **6.2%** | **5.6%** | **-0.56pp** | **0.027** | **Yes** |
| High (30+ rounds) | 43.9% | 43.0% | -0.87pp | 0.108 | No |

Only the medium-engagement segment showed a statistically confirmed negative effect. High-engagement users showed the largest observed drop but did not reach significance, likely due to sample size constraints within this segment.

---

## 7. Final Recommendation

**Do not launch gate_40 globally.**

The new module caused a statistically significant decrease in 7-day retention (p=0.002). No segment showed a confirmed positive effect. The most conclusively harmed group was medium-engagement users — the largest and most commercially valuable segment.

**Next steps:**
1. Keep the current version (gate_30)
2. Redesign the progression gate timing based on user research
3. Run a follow-up experiment with event-level tracking
4. Collect pre-experiment user features for more rigorous segment analysis

Full analysis and reasoning: [`reports/executive_summary.md`](reports/executive_summary.md)

---

## 8. Limitations

- Dataset is user-level, not event-level — the engagement funnel is constructed from game-round thresholds rather than actual user journey events
- No pre-experiment covariates available; sample balance is diagnostic only
- Engagement segments are post-treatment constructs and may partially reflect the treatment effect itself

---

## 9. Repository Structure

```
app-recommendation-ab-test-analytics/
├── README.md
├── requirements.txt
├── .gitignore
├── data/
│   ├── raw/cookie_cats.csv          # Original dataset (90,189 users)
│   ├── processed/cookie_cats_cleaned.csv
│   └── app_ab_test.db               # SQLite database
├── notebooks/
│   ├── 01_data_cleaning.ipynb
│   ├── 02_sql_funnel_analysis.ipynb
│   ├── 03_ab_test_retention_analysis.ipynb
│   └── 04_segment_analysis.ipynb
├── sql/
│   ├── create_tables.sql
│   ├── funnel_analysis.sql
│   ├── retention_analysis.sql           # D1/D7 retention rates and uplift by group
│   └── segment_analysis.sql             # HTE analysis — D7 retention by user segment
├── src/
│   ├── database.py                      # Loads cleaned CSV into SQLite
│   └── ab_testing.py                    # Reusable z-test, CI, and A/B test pipeline
├── app/
│   └── streamlit_app.py
├── reports/
│   └── executive_summary.md
└── outputs/
    ├── figures/
    └── tables/
```

---

## 10. How to Run

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Build the database
python src/database.py

# 3. Run notebooks in order
jupyter lab

# 4. Launch dashboard
streamlit run app/streamlit_app.py
```

---

## Tech Stack

`Python` · `pandas` · `numpy` · `scipy` · `statsmodels` · `SQLite` · `SQL` · `Streamlit` · `Matplotlib` · `Seaborn` · `Jupyter`
