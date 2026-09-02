# Checks whether the raw data changed. If changes are detected, it triggers the ML pipeline.
# If nothing changed, it skips execution.

from pathlib import Path
import subprocess
import logging

RAW_DATA_DIR = Path("data/raw")
STATE_FILE = Path("data/raw/raw_state.txt")

LOG_DIR = Path("logs")  # Folder where logs will be stored
LOG_FILE = LOG_DIR / "raw_data_watcher.log"  # Watcher log file
LOG_DIR.mkdir(exist_ok=True)  # Create logs folder if it does not exist

# Configure log format: date/time - level - message
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


def list_raw_files():
    files = list(RAW_DATA_DIR.glob("*.csv"))

    print(f"Total CSV files found: {len(files)}")


    if len(files) == 0:
        print("No CSV files found. Nothing to process.")
        return []

    print("Files found in data/raw:")

    for file in files:
        print(f"- {file}")

    return files

def should_run_pipeline(previous_state, current_state):
    return previous_state != current_state


def get_current_state(files):
    state = []
    for file in files:
        modified_time = file.stat().st_mtime
        state.append(f"{file}|{modified_time}")
    return state


def save_state(state):
    STATE_FILE.write_text("\n".join(state))


def load_previous_state():
    if not STATE_FILE.exists():
        return []
    content = STATE_FILE.read_text()
    if content == "":
        return []
    return content.splitlines()


def run_pipeline():
    print("Running pipeline...")

    try:
        subprocess.run(
            ["python", "pipeline.py"],
            check=True
        )

        message = "Pipeline executed successfully."
        print(message)
        logging.info(message)
        return True

    except subprocess.CalledProcessError as error:
        message = "Error while running the pipeline."
        print(message)
        logging.error(message)
        logging.error(f"Error code: {error.returncode}")
        return False



if __name__ == "__main__":
    message = "Raw data watcher started"
    print(message)
    logging.info(message)

    files = list_raw_files()

    previous_state = load_previous_state()
    print(f"Previous saved state: {previous_state}")

    current_state = get_current_state(files)
    print(f"Current detected state: {current_state}")

    if should_run_pipeline(previous_state, current_state):
        message = "Change detected. Pipeline will run."
        print(message)
        logging.info(message)

        pipeline_success = run_pipeline()

        if pipeline_success:
            save_state(current_state)

            message = "Current state saved."
            print(message)
            logging.info(message)
        else:
            message = "Current state was not saved because the pipeline failed."
            print(message)
            logging.error(message)
    else:
        message = "No changes detected. Pipeline will not run."
        print(message)
        logging.info(message)
