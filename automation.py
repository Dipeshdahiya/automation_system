import os
import json
import logging
from datetime import datetime

# Paths
INPUT_DIR = "input"
OUTPUT_DIR = "output"
REQUIRED_FILES = ["data.txt", "config.json"]

# Setup logging
os.makedirs(OUTPUT_DIR, exist_ok=True)
log_path = os.path.join(OUTPUT_DIR, "run.log")

logging.basicConfig(
    filename=log_path,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def safe_exit(message):
    print(f"ERROR: {message}")
    logging.error(message)
    return

def validate_inputs():
    if not os.path.exists(INPUT_DIR):
        return False, "Input folder does not exist"

    for file in REQUIRED_FILES:
        file_path = os.path.join(INPUT_DIR, file)
        if not os.path.exists(file_path):
            return False, f"Missing required file: {file}"
        if os.path.getsize(file_path) == 0:
            return False, f"File is empty: {file}"

    # Validate JSON
    try:
        with open(os.path.join(INPUT_DIR, "config.json"), "r") as f:
            json.load(f)
    except json.JSONDecodeError:
        return False, "Invalid JSON in config.json"

    return True, "All inputs valid"

def generate_summary():
    data_file = os.path.join(INPUT_DIR, "data.txt")

    with open(data_file, "r") as f:
        lines = f.readlines()

    summary = {
        "total_lines": len(lines),
        "file_size_bytes": os.path.getsize(data_file),
        "processed_at": datetime.now().isoformat()
    }

    summary_path = os.path.join(OUTPUT_DIR, "summary.txt")
    with open(summary_path, "w") as f:
        for key, value in summary.items():
            f.write(f"{key}: {value}\n")

    logging.info("Summary generated successfully")

def main():
    logging.info("Automation started")

    valid, message = validate_inputs()
    if not valid:
        safe_exit(message)
        return

    print("Inputs validated successfully")
    logging.info("Inputs validated")

    generate_summary()

    print("Automation completed successfully")
    logging.info("Automation finished")

if __name__ == "__main__":
    main()
