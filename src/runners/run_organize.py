# Function to run organize.py (Step 3)
import os
import subprocess

from common.consts import ANTS, LEXICON, METADATA, OUTPUT, SRC_DIR
from loguru import logger


def run_organize(target):
    logger.debug(f"Processing organize {target}...")
    result = subprocess.run(
        [
            "python3",
            os.path.join(SRC_DIR, "step3", "organize.py"),
            os.path.join(OUTPUT, target),
            LEXICON,
            METADATA,
            os.path.join(OUTPUT, target, ANTS),
        ],
        capture_output=True,
        text=True,
    )
    logger.debug(f"STDOUT for {target} organize: {result.stdout}")
    if result.stderr:
        logger.warning(f"STDERR for {target} organize: {result.stderr}")
