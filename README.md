# 💰 Personal Finance Data Engineering Pipeline

---

## 📌 Project Overview

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://personal-finance-2026.streamlit.app/)

A full end-to-end personal finance data engineering project — from raw CSV data through a local data pipeline to an interactive Streamlit dashboard.

🔗 **Live Demo:** [https://personal-finance-2026.streamlit.app/](https://personal-finance-2026.streamlit.app/)

This project tracks personal income and expenses across categories and months. It implements a real data engineering pipeline that ingests raw data, stores it in a local data lake, moves it to a data warehouse, transforms it for analysis, and visualises it in an interactive dashboard.

The goal was to apply data engineering concepts — data lake, data warehouse, ETL pipeline, and BI dashboard — on a real personal dataset.

---

## 📌 Problem Statement

Managing personal finances is often fragmented, manual, and lacks visibility. Individuals typically rely on scattered spreadsheets, mobile apps, or raw transaction logs that do not provide a structured, end-to-end view of their financial behavior.

This creates several challenges:

Lack of centralized data — financial records are stored in inconsistent formats across different tools
Limited analytical insights — difficulty in tracking spending patterns, income trends, and savings behavior over time
Manual data handling — repetitive cleaning and aggregation of data increases the risk of errors
No scalable data pipeline — most personal finance tracking solutions do not simulate real-world data engineering workflows

As a result, individuals are unable to make data-driven financial decisions or apply modern data engineering practices to personal datasets.

This project addresses these gaps by building a structured, end-to-end data pipeline that transforms raw financial data into clean, analyzable, and visual insights through a data lake, warehouse, and interactive dashboard.

---

## 🏗️ Architecture & Pipeline

```
income_expense.csv               ← Source (raw CSV)
        │
        ▼
┌──────────────────────────┐
│        DATA LAKE         │  data_lake/raw/transactions/2026/
│     (local folder)       │  Single timestamped CSV (EAT timezone)
│                          │  Old files deleted on each run
└──────────────────────────┘
        │
        ▼
┌──────────────────────────┐
│     DATA WAREHOUSE       │  finance.db (SQLite)
│                          │  ├── raw_transactions  (exact copy from lake)
│                          │  ├── transactions      (cleaned & transformed)
│                          │  ├── monthly_summary   (view)
│                          │  └── category_summary  (view)
└──────────────────────────┘
        │
        ▼
┌──────────────────────────┐
│       DASHBOARD          │  dashboard.py (Streamlit)
│                          │  Reads from transactions table
└──────────────────────────┘
```

### Pipeline Steps

| Step | Script | Description |
|---|---|---|
| 1 — Ingest | `pipeline/01_ingest.py` | Reads CSV → deletes old lake files → saves single timestamped file (EAT) |
| 2 — Load | `pipeline/02_lake_to_warehouse.py` | Picks latest lake file → drops and reloads `raw_transactions` table |
| 3 — Transform | `pipeline/03_transform.py` | Cleans & types data → creates `transactions` table + views |
| Run all | `pipeline/run_pipeline.py` | Runs all 3 steps in order with logging |

---

## 📁 Project Structure

```
personal-finance-dashboard/
│
├── .github/
│   └── workflows/
│       └── keep_alive.yml                ← GitHub Actions keep alive workflow
│
├── data_lake/
│   └── raw/
│       └── transactions/
│           └── 2026/
│               └── Input_20260326_171645.csv   ← single file, replaced each run
│
├── pipeline/
│   ├── 01_ingest.py            ← Local CSV → Data Lake (cleans old files)
│   ├── 02_lake_to_warehouse.py ← Data Lake → Data Warehouse
│   ├── 03_transform.py         ← Raw → Clean + Views
│   └── run_pipeline.py         ← Runs all 3 steps in order
│
├── dashboard.py                ← Streamlit app
├── income_expense.csv          ← Source data
├── finance.db                  ← SQLite data warehouse
├── requirements.txt
├── .gitignore
└── README.md
```

---

## 🛠️ Tech Stack

| Layer | Tool |
|---|---|
| Language | Python 3.11 |
| Data Lake | Local filesystem (single timestamped CSV per run) |
| Data Warehouse | SQLite (`finance.db`) |
| Pipeline | Python (`pandas`, `sqlite3`) |
| Timezone handling | `zoneinfo` (EAT — Africa/Nairobi) |
| Dashboard | Streamlit |
| Charts | Plotly |
| Data manipulation | Pandas |
| Excel export | OpenPyXL |
| Automation | GitHub Actions |
| Version control | Git & GitHub |
| Deployment | Streamlit Cloud |

---

## 🚀 How to Run Locally

### 1. Clone the repository
```bash
git clone https://github.com/anormanangel/personal-finance-dashboard.git
cd personal-finance-dashboard
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the pipeline
This ingests the CSV, cleans old lake files, loads into the data lake, moves to the warehouse and transforms:
```bash
python pipeline/run_pipeline.py
```

You should see:
```
PIPELINE START
STEP 1/3 — Ingest: Local CSV → Data Lake
INGEST: Deleted old file → Input_20260325_080000.csv
INGEST: Raw file saved to data lake → Input_20260326_080000.csv
STEP 2/3 — Load: Data Lake → Data Warehouse
LAKE → WAREHOUSE: 340 rows loaded into 'raw_transactions'
STEP 3/3 — Transform: Clean & enrich in Warehouse
TRANSFORM: 340 clean rows in 'transactions'
PIPELINE FINISHED SUCCESSFULLY
```

### 4. Run the dashboard
```bash
streamlit run dashboard.py
```

Open your browser at `http://localhost:8501`

---

## ☁️ How to Deploy to Streamlit Cloud

1. Push your code to GitHub (including `finance.db`):
```bash
git add .
git commit -m "deploy"
git push origin main
```

2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Click **New app**
4. Select your repository, branch (`main`), and main file (`dashboard.py`)
5. Click **Deploy**

🔗 **Live App:** [https://personal-finance-2026.streamlit.app/](https://personal-finance-2026.streamlit.app/)

Streamlit Cloud will automatically redeploy every time you push to `main`.

### Refreshing data after deployment
When your source data changes, re-run the pipeline locally and push the updated database:
```bash
python pipeline/run_pipeline.py
git add finance.db
git commit -m "chore: refresh finance.db"
git push origin main
```

---

## 📊 Dashboard Features

- **Income & Expenses page**
  - KPI tiles — Total Income, Total Expense, Net Balance, Transaction count (figures in millions)
  - Expenses by Category (bar chart)
  - Income by Category (pie chart)
  - Monthly Totals — grouped bar chart (Income vs Expense side by side)
  - Transactions Table with CSV and Excel export

- **Transactions Summary page**
  - KPI tiles
  - Drill down by Category, Type, or Month

- **Sidebar filters** — filter by Month, Type, and Category across all views

---

## ⚙️ Automation

### Keep Alive — GitHub Actions
The app is kept alive automatically using a GitHub Actions workflow that pings the Streamlit app every day at 8am UTC.

```yaml
name: Keep Alive
on:
  schedule:
    - cron: "0 8 * * *"  # every day at 8am UTC
  workflow_dispatch:
```

To view the workflow runs go to the **Actions** tab on GitHub.

---

## 👤 Author

**Norman Angel**

[![GitHub](https://img.shields.io/badge/GitHub-anormanangel-181717?style=flat&logo=github)](https://github.com/anormanangel)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Norman%20Angel-0077B5?style=flat&logo=linkedin)](https://www.linkedin.com/in/anormanangel)
[![Substack](https://img.shields.io/badge/Substack-Learning%20in%20Public-FF6719?style=flat&logo=substack)](https://substack.com/@anormanangel)

---

## 📄 License

This project is for educational use.
