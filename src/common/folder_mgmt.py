import os
import shutil
import sys
from loguru import logger  # initialized in run_all_steps.py currently


def clean_output_min_folder(OUTPUT, clean_outputs_min):
    print()

    confirm = "y"
    if clean_outputs_min is False:
        while confirm := (
            input(
                f"About to remove output_min directory: {OUTPUT} \nAre you sure you want to proceed? (y/n): "
            )
            .lower()
            .strip()
        ):
            if confirm in ("y", "n"):
                break

    if confirm != "y":
        logger.info(
            "User chose to note remove output_min directory; operation cancelled."
        )
        sys.exit(0)

    shutil.rmtree(OUTPUT, ignore_errors=True)
    os.makedirs(OUTPUT, exist_ok=True)
    logger.info(f"Removed and recreated directory: {OUTPUT}")
