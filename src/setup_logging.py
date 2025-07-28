import os
import shutil
from datetime import datetime
from glob import glob
from pathlib import Path
import sys

from loguru import logger

from run_all_consts import (
    BASE_DIR,
    CORPUS,
    METADATA,
    OUTPUT,
    RES_DIR,
    RUN_DIR,
    SRC_DIR,
    TESTS_DIR,
)

# Global flag to track if logging has already been configured
_logging_configured = False


LOGGING_PREFIX = "run_all_"


_logging_configured = False  # Ensure this is defined somewhere globally


def setup_logging(args):
    global _logging_configured
    if _logging_configured:
        return

    move_old_logs()

    dry_run_label = "__dry_run__" if args.dry_run else ""
    log_file = os.path.join(
        RUN_DIR,
        f"{LOGGING_PREFIX}{dry_run_label}{datetime.now().strftime('%Y%m%d_%H%M%S')}.log",
    )

    # Remove default Loguru handler
    logger.remove()

    # Add file handler (always DEBUG)
    logger.add(log_file, level="DEBUG", format="{time} - {level} - {message}", enqueue=True)

    # Add console handler (user-defined level)
    logger.add(sys.stderr, level=args.log_level, format="<level>{level}</level>: {message}", enqueue=True, colorize=True)

    logger.info(f"Console logging level set to: {args.log_level}")
    logger.debug("File logging level set to: DEBUG")

    _logging_configured = True

    # Print paths for debugging
    logger.debug(f"BASE_DIR: {BASE_DIR}")
    logger.debug(f"RES_DIR: {RES_DIR}")
    logger.debug(f"TESTS_DIR: {TESTS_DIR}")
    logger.debug(f"SRC_DIR: {SRC_DIR}")
    logger.debug(f"CORPUS: {CORPUS}")
    logger.debug(f"METADATA: {METADATA}")
    logger.debug(f"OUTPUT: {OUTPUT}")
    logger.debug(f"RUN_DIR: {RUN_DIR}")


def move_old_logs():
    log_archive: Path = Path(RUN_DIR) / "log_archive"
    os.makedirs(log_archive, exist_ok=True)

    existing_logs = glob(str(Path(RUN_DIR) / Path(f"{LOGGING_PREFIX}*")))
    if len(existing_logs) > 0:
        for existing_log in existing_logs:
            shutil.move(existing_log, log_archive)
