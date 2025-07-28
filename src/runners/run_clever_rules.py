# Function to run cleverRules.py (Step 4)
import os
import subprocess

from common.consts import NA_TRIGS, NEG_TRIGS, OUTPUT, SRC_DIR
from loguru import logger


def run_clever_rules(target):
    logger.debug(f"Processing run_clever_rules {target}...")
    result = subprocess.run(
        [
            "python",
            os.path.join(SRC_DIR, "step4", "cleverRules.py"),
            os.path.join(OUTPUT, target),
            target,
            NEG_TRIGS,
            NA_TRIGS,
        ],
        capture_output=True,
        text=True,
    )
    logger.debug(f"STDOUT for {target} run_clever_rules: {result.stdout}")
    if result.stderr:
        logger.warning(f"STDERR for {target} run_clever_rules: {result.stderr}")
