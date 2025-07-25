import logging
import os
from datetime import datetime

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


def setup_logging(args):
    global _logging_configured
    if _logging_configured:
        return  # Skip setup if already configured

    log_file = os.path.join(
        RUN_DIR, f"run_all_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    )

    console_level = args.log_level  # Default is WARNING

    # File handler (always DEBUG)
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(
        logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    )

    # Console handler (user-defined level)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(console_level)
    console_handler.setFormatter(logging.Formatter("%(levelname)s: %(message)s"))

    # Root logger setup
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)
    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)

    logging.info(f"Console logging level set to: {logging.getLevelName(console_level)}")
    logging.debug("File logging level set to: DEBUG")

    _logging_configured = True

    # Print paths for debugging
    logging.debug(f"BASE_DIR: {BASE_DIR}")
    logging.debug(f"RES_DIR: {RES_DIR}")
    logging.debug(f"TESTS_DIR: {TESTS_DIR}")
    logging.debug(f"SRC_DIR: {SRC_DIR}")
    logging.debug(f"CORPUS: {CORPUS}")
    logging.debug(f"METADATA: {METADATA}")
    logging.debug(f"OUTPUT: {OUTPUT}")
    logging.debug(f"RUN_DIR: {RUN_DIR}")
