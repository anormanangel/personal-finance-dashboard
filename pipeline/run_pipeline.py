import logging
import subprocess
import sys
import os

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

PIPELINE_DIR = os.path.dirname(__file__)

def run_step(script_name):
    script_path = os.path.join(PIPELINE_DIR, script_name)
    logging.info(f"Running {script_name}...")
    result = subprocess.run([sys.executable, script_path], check=True)
    return result

if __name__ == "__main__":
    logging.info("=" * 60)
    logging.info("PIPELINE START")
    logging.info("=" * 60)

    try:
        logging.info("STEP 1/3 — Ingest: Local CSV → Data Lake")
        run_step("01_ingest.py")

        logging.info("STEP 2/3 — Load: Data Lake → Data Warehouse")
        run_step("02_lake_to_warehouse.py")

        logging.info("STEP 3/3 — Transform: Clean & enrich in Warehouse")
        run_step("03_transform.py")

        logging.info("=" * 60)
        logging.info("PIPELINE FINISHED SUCCESSFULLY")
        logging.info("=" * 60)

    except subprocess.CalledProcessError as e:
        logging.error(f"PIPELINE FAILED: {e}")
        raise