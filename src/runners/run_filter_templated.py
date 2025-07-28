# Function to run filterTemplated.py (Step 5)
import os
import subprocess

from common.consts import ASSESSMENTTERMS, OTHERTERMS, OUTPUT, SRC_DIR
from loguru import logger


def run_filter_templated(target):
    logger.debug(f"Filtering tagged templated text for {target}")
    result = subprocess.run(
        [
            "python3",
            os.path.join(SRC_DIR, "step5", "filterTemplated.py"),
            "-p",
            OUTPUT + "/",  # Add a trailing slash here
            "-t",
            target,
            "-a",
            ASSESSMENTTERMS,
            "-o",
            OTHERTERMS,
            "-sp",
            "14",
            "-tp",
            "6",
        ],
        capture_output=True,
        text=True,
    )
    logger.debug(f"STDOUT for {target} filterTemplated: {result.stdout}")
    if result.stderr:
        logger.warning(f"STDERR for {target} filterTemplated: {result.stderr}")
