import shutil
from datetime import datetime
from glob import glob
from pathlib import Path
import sys

from loguru import logger


from common.consts import (
    CORPUS,
    METADATA,
    OUTPUT,
    PROJECT_ROOT,
    RES_DIR,
    RUN_DIR,
    SRC_DIR,
    TESTS_DIR,
    get_environment_var,
)

# Global flag to track if logging has already been configured
_logging_configured = False

LOG_PATH: Path = get_environment_var("LOG_PATH", Path)
LOGGING_PREFIX = get_environment_var("LOGGING_PREFIX", str)


_logging_configured = False  # Ensure this is defined somewhere globally


def setup_logging(args, check_run_dir):
    global _logging_configured
    if _logging_configured:
        return logger

    move_old_logs(check_run_dir)

    log_file: Path = LOG_PATH / make_log_file_name(args.dry_run)

    check_run_dir("logging", LOG_PATH)

    # Remove default Loguru handler
    logger.remove()

    # Add file handler (always DEBUG)
    logger.add(
        log_file, level="DEBUG", format="{time} - {level} - {message}", enqueue=True
    )

    # Add console handler (user-defined level)
    logger.add(
        sys.stderr,
        level=args.log_level,
        format="<level>{level}</level>: {message}",
        enqueue=True,
        colorize=True,
    )

    logger.info(f"Console logging level set to: {args.log_level}")
    logger.debug("File logging level set to: DEBUG")

    _logging_configured = True

    # Print paths for debugging
    logger.debug(f"PROJECT_ROOT: {PROJECT_ROOT}")
    logger.debug(f"RES_DIR: {RES_DIR}")
    logger.debug(f"TESTS_DIR: {TESTS_DIR}")
    logger.debug(f"SRC_DIR: {SRC_DIR}")
    logger.debug(f"CORPUS: {CORPUS}")
    logger.debug(f"METADATA: {METADATA}")
    logger.debug(f"OUTPUT: {OUTPUT}")
    logger.debug(f"RUN_DIR: {RUN_DIR}")

    return logger


def make_log_file_name(dry_run: bool):
    dry_run_label = "__dry_run__" if dry_run else ""
    return (
        f"{LOGGING_PREFIX}{dry_run_label}{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    )


def move_old_logs(check_run_dir):
    log_archive: Path = get_environment_var("LOG_ARCHIVE", Path)
    check_run_dir("log archive", log_archive)

    existing_logs = glob(str(Path(RUN_DIR) / Path(f"{LOGGING_PREFIX}*")))
    if len(existing_logs) > 0:
        for existing_log in existing_logs:
            if not (Path(log_archive) / Path(existing_log)).exists():
                shutil.move(existing_log, log_archive)
