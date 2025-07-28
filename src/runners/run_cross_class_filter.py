import os
import subprocess

from common.consts import CROSS_CLASS_FILE, LEXICON, OUTPUT, SRC_DIR
from loguru import logger


def run_cross_class_filter(target):
    logger.debug(f"Running cross-class filter for {target}...")
    result = subprocess.run(
        [
            "python3",
            os.path.join(SRC_DIR, "step5", "cross_class_filter.py"),
            "-t",
            os.path.join(OUTPUT, target),
            "-d",
            LEXICON,
            "-c",
            CROSS_CLASS_FILE,
        ],
        capture_output=True,
        text=True,
    )
    logger.debug(f"STDOUT for {target} cross_class_filter: {result.stdout}")
    if result.stderr:
        logger.warning(f"STDERR for {target} cross_class_filter: {result.stderr}")
