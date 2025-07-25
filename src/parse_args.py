import argparse
import logging


def parse_args():
    parser = argparse.ArgumentParser(
        description="Run all steps of the processing pipeline."
    )
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "--debug",
        action="store_const",
        dest="log_level",
        const=logging.DEBUG,
        help="Set console logging level to DEBUG",
    )
    group.add_argument(
        "--info",
        action="store_const",
        dest="log_level",
        const=logging.INFO,
        help="Set console logging level to INFO",
    )
    group.add_argument(
        "--quiet",
        action="store_const",
        dest="log_level",
        const=logging.WARNING,
        help="Set console logging level to WARNING (default)",
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
        log_level=logging.WARNING
    )  # This makes quiet (WARNING) the default
    return parser.parse_args()
