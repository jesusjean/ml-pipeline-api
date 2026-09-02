#Orchestrates the ML pipelone steps, such as preprocessing and training 

import subprocess
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("logs/pipeline.log"),
        logging.StreamHandler()
    ]
)

def run_step(name, command):
    logging.info(f"Running step: {name}")

    result = subprocess.run(command, shell=True)

    if result.returncode != 0:
        raise RuntimeError(f"Step failed: {name}")

def main():
    run_step(
        "Preprocessing data",
        "python scripts/preprocess.py"
    )

    run_step(
        "Training model",
        "python train.py"
    )

    logging.info("Pipeline finished successfully")

if __name__ == "__main__":
    main()
