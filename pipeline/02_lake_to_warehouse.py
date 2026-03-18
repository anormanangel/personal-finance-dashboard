import pandas as pd
import sqlite3
import os
import glob
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

# CONFIG
LAKE_PATH  = os.path.join(os.path.dirname(__file__), "..", "data_lake", "raw", "transactions", "2026")
DB_PATH    = os.path.join(os.path.dirname(__file__), "..", "finance.db")
TABLE_NAME = "raw_transactions"

def lake_to_warehouse():
    logging.info("LAKE → WAREHOUSE: Finding latest file in data lake...")

    # Pick the most recently created file in the lake
    files = sorted(glob.glob(os.path.join(LAKE_PATH, "*.csv")))
    if not files:
        raise FileNotFoundError(f"No CSV files found in {LAKE_PATH}")

    latest_file = files[-1]
    logging.info(f"LAKE → WAREHOUSE: Loading file → {latest_file}")

    df = pd.read_csv(latest_file)
    df["SOURCE_FILE"] = os.path.basename(latest_file)

    logging.info(f"LAKE → WAREHOUSE: {len(df)} rows read from lake")

    # Load into warehouse raw table
    conn   = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            Date        TEXT,
            Month       TEXT,
            Category    TEXT,
            Type        TEXT,
            Description TEXT,
            Amount      TEXT,
            SOURCE_FILE TEXT
        )
    """)

    cursor.execute(f"DROP TABLE IF EXISTS {TABLE_NAME}")
    df.to_sql(TABLE_NAME, conn, if_exists="replace", index=False)
    conn.commit()

    row_count = cursor.execute(f"SELECT COUNT(*) FROM {TABLE_NAME}").fetchone()[0]
    conn.close()

    logging.info(f"LAKE → WAREHOUSE: {row_count} rows loaded into '{TABLE_NAME}'")

if __name__ == "__main__":
    lake_to_warehouse()