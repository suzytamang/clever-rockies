import os
import shutil
import sys


def clean_output_min_folder(OUTPUT, clean_outputs_min, logger):
    if clean_outputs_min is False:
        confirm = (
            input(
                f"About to remove directory: {OUTPUT} \nAre you sure you want to proceed? (y/n): "
            )
            .lower()
            .strip()
        )
    else:
        confirm = "y"
    if confirm != "y":
        logger.info("Operation cancelled.")
        sys.exit(0)

    shutil.rmtree(OUTPUT, ignore_errors=True)
    os.makedirs(OUTPUT, exist_ok=True)
    logger.info(f"Removed and recreated directory: {OUTPUT}")
