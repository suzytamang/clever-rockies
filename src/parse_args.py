import argparse

from logging import DEBUG as DEBUG_LOG_LEVEL
from logging import INFO as INFO_LOG_LEVEL
from logging import WARNING as WARNING_LOG_LEVEL


def parse_args():
    parser = argparse.ArgumentParser(
        description="Run all steps of the processing pipeline."
    )
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "--debug",
        action="store_const",
        dest="log_level",
        const=DEBUG_LOG_LEVEL,
        help="Set console logger level to DEBUG",
    )
    group.add_argument(
        "--info",
        action="store_const",
        dest="log_level",
        const=INFO_LOG_LEVEL,
        help="Set console logger level to INFO",
    )
    group.add_argument(
        "--quiet",
        action="store_const",
        dest="log_level",
        const=WARNING_LOG_LEVEL,
        help="Set console logger level to WARNING (default)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_const",
        dest="dry_run",
        const=True,
        help="Perform a dry run without running code to observe flow",
    )
    parser.add_argument(
        "--clean-outputs-min",
        action="store_const",
        dest="clean_outputs_min",
        const=True,
        help="Quietly clean output_min",
    )
    parser.set_defaults(
        log_level=WARNING_LOG_LEVEL
    )  # This makes quiet (WARNING) the default
    return parser.parse_args()
