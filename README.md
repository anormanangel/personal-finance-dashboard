# 💰 Personal Finance Dashboard

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://income-expense-dashboard.streamlit.app/)

A full end-to-end personal finance data engineering project — from raw CSV data through a local data pipeline to an interactive Streamlit dashboard.

🔗 **Live Demo:** [income-expense-dashboard.streamlit.app](https://income-expense-dashboard.streamlit.app/)

---

## 📌 Project Overview

This project tracks personal income and expenses across categories and months. It implements a real data engineering pipeline that ingests raw data, stores it in a local data lake, moves it to a data warehouse, transforms it for analysis, and visualises it in an interactive dashboard.

The goal was to apply data engineering concepts — data lake, data warehouse, ETL pipeline, and BI dashboard — on a real personal dataset.

---

## 🏗️ Architecture & Pipeline

```
income_expense.csv          ← Source (raw CSV)
        │
        ▼
┌─────────────────────┐
│     DATA LAKE       │  data_lake/raw/transactions/2023/
│  (local folder)     │  Timestamped raw CSV files stored as-is
└─────────────────────┘
        │
        ▼
┌─────────────────────┐
│   DATA WAREHOUSE    │  finance.db (SQLite)
│                     │  ├── raw_transactions  (exact copy from lake)
│                     │  ├── transactions      (cleaned & transformed)
│                     │  ├── monthly_summary   (view)
│                     │  └── category_summary  (view)
└─────────────────────┘
        │
        ▼
┌─────────────────────┐
│     DASHBOARD       │  app.py (Streamlit)
│                     │  Reads from transactions table
└─────────────────────┘
```

### Pipeline Steps

| Step | Script | Description |
|---|---|---|
| 1 — Ingest | `pipeline/01_ingest.py` | Reads CSV → saves timestamped raw file to data lake |
| 2 — Load | `pipeline/02_lake_to_warehouse.py` | Picks latest lake file → loads into `raw_transactions` table |
| 3 — Transform | `pipeline/03_transform.py` | Cleans & types data → creates `transactions` table + views |
| Run all | `pipeline/run_pipeline.py` | Runs all 3 steps in order |

---

## 📁 Project Structure

```
personal-finance-dashboard/
│
├── data_lake/
│   └── raw/
│       └── transactions/
│           └── 2023/
│               └── Input_20260316_100914.csv   ← auto-created by pipeline
│
├── pipeline/
│   ├── 01_ingest.py            ← Local CSV → Data Lake
│   ├── 02_lake_to_warehouse.py ← Data Lake → Data Warehouse
│   ├── 03_transform.py         ← Raw → Clean + Views
│   └── run_pipeline.py         ← Runs all 3 steps
│
├── app.py                ← Streamlit app
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
| Data Lake | Local filesystem (timestamped CSV files) |
| Data Warehouse | SQLite (`finance.db`) |
| Pipeline | Python (`pandas`, `sqlite3`) |
| Dashboard | Streamlit |
| Charts | Plotly |
| Data manipulation | Pandas |
| Excel export | OpenPyXL |
| Version control | Git & GitHub |

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
This ingests the CSV, loads it into the data lake, moves it to the warehouse and transforms it:
```bash
python pipeline/run_pipeline.py
```

You should see:
```
PIPELINE START
STEP 1/3 — Ingest: Local CSV → Data Lake
STEP 2/3 — Load: Data Lake → Data Warehouse
STEP 3/3 — Transform: Clean & enrich in Warehouse
PIPELINE FINISHED SUCCESSFULLY
```

### 4. Run the dashboard
```bash
streamlit run app.py
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
4. Select your repository, branch (`main`), and main file (`app.py`)
5. Click **Deploy**

🔗 **Live App:** [income-expense-dashboard.streamlit.app](https://income-expense-dashboard.streamlit.app/)

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
  - KPI tiles — Total Income, Total Expense, Net Balance, Transaction count
  - Expenses by Category (bar chart)
  - Income by Category (pie chart)
  - Monthly Totals — grouped bar chart (Income vs Expense side by side)
  - Transactions Table with CSV and Excel export

- **Transactions Summary page**
  - KPI tiles
  - Drill down by Category, Type, or Month

- **Sidebar filters** — filter by Month, Type, and Category across all views

---

## 👤 Author

**Norman Angel**
[GitHub](https://github.com/anormanangel)

---

## 📄 License

This project is for personal and educational use.
