import sqlite3
import os
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "finance.db")

def transform():
    logging.info("TRANSFORM: Running SQL transformations...")

    conn   = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Drop and recreate the clean transactions table
    cursor.execute("DROP TABLE IF EXISTS transactions")

    cursor.execute("""
        CREATE TABLE transactions AS
        SELECT
            TRIM(Date)                          AS DATE,
            TRIM(Month)                         AS MONTH,
            TRIM(Category)                      AS CATEGORY,
            TRIM(Type)                          AS TYPE,
            TRIM(Description)                   AS DESCRIPTION,
            CAST(
                REPLACE(
                    REPLACE(TRIM(Amount), ',', ''),
                    ' ', ''
                ) AS REAL
            )                                   AS AMOUNT,
            SOURCE_FILE,
            datetime('now')                     AS LOADED_AT
        FROM raw_transactions
        WHERE
            TRIM(Date)        != ''
            AND LOWER(TRIM(Type)) IN ('income', 'expense')
            AND CAST(
                    REPLACE(TRIM(Amount), ',', '') AS REAL
                ) > 0
    """)

    # Create a monthly summary view
    cursor.execute("DROP VIEW IF EXISTS monthly_summary")
    cursor.execute("""
        CREATE VIEW monthly_summary AS
        SELECT
            MONTH,
            TYPE,
            COUNT(*)        AS TRANSACTIONS,
            SUM(AMOUNT)     AS TOTAL_AMOUNT,
            AVG(AMOUNT)     AS AVG_AMOUNT,
            MAX(AMOUNT)     AS MAX_AMOUNT,
            MIN(AMOUNT)     AS MIN_AMOUNT
        FROM transactions
        GROUP BY MONTH, TYPE
    """)

    # Create a category summary view
    cursor.execute("DROP VIEW IF EXISTS category_summary")
    cursor.execute("""
        CREATE VIEW category_summary AS
        SELECT
            CATEGORY,
            TYPE,
            COUNT(*)        AS TRANSACTIONS,
            SUM(AMOUNT)     AS TOTAL_AMOUNT
        FROM transactions
        GROUP BY CATEGORY, TYPE
    """)

    conn.commit()

    row_count = cursor.execute("SELECT COUNT(*) FROM transactions").fetchone()[0]
    conn.close()

    logging.info(f"TRANSFORM: {row_count} clean rows in 'transactions'")
    logging.info("TRANSFORM: Views created → monthly_summary, category_summary")

if __name__ == "__main__":
    transform()