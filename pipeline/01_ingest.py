# Import Libraries
import pandas as pd
import os
import logging
from datetime import datetime
from zoneinfo import ZoneInfo

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

# CONFIG
SOURCE_FILE = os.path.join(os.path.dirname(__file__), "..", "income_expense.csv")
LAKE_PATH   = os.path.join(os.path.dirname(__file__), "..", "data_lake", "raw", "transactions", "2026")

def ingest():
    logging.info("INGEST: Reading local CSV file...")

    # Check file exists
    if not os.path.exists(SOURCE_FILE):
        raise FileNotFoundError(f"Source file not found: {SOURCE_FILE}")

    df = pd.read_csv(SOURCE_FILE)
    logging.info(f"INGEST: {len(df)} rows read from '{SOURCE_FILE}'")

    # Create data lake folder if it doesn't exist
    os.makedirs(LAKE_PATH, exist_ok=True)

    # Delete old files in data lake — keep only latest
    for old_file in os.listdir(LAKE_PATH):
        if old_file.endswith(".csv"):
            os.remove(os.path.join(LAKE_PATH, old_file))
            logging.info(f"INGEST: Deleted old file → {old_file}")

    # Save new file with EAT timestamp
    eat_time  = datetime.now(ZoneInfo("Africa/Nairobi"))
    timestamp = eat_time.strftime("%Y%m%d_%H%M%S")
    filename  = f"Input_{timestamp}.csv"
    filepath  = os.path.join(LAKE_PATH, filename)

    df.to_csv(filepath, index=False)
    logging.info(f"INGEST: Raw file saved to data lake → {filepath}")

    return filepath

if __name__ == "__main__":
    ingest()