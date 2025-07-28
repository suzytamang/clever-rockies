#!/usr/bin/env python3

import os
from pathlib import Path
import subprocess
import sys

from dotenv import load_dotenv
from loguru import logger
from common.ascii_text_color import color_text
from common.folder_mgmt import clean_output_min_folder
from common.setup.grabtargets import run_grab_targets
from parse_args import parse_args
from common.consts import OUTPUT, RUN_DIR, SRC_DIR, TARGETS_FILE
from runners.run_clever_rules import run_clever_rules
from runners.run_filter_templated import run_filter_templated
from runners.run_organize import run_organize
from runners.run_sequencer import run_sequencer
from setup_logging import setup_logging


load_dotenv()


def check_run_dir(folder_type: str, folder_path: str | Path):

    if os.path.exists(folder_path) is False:
        print()
        while (
            choice := input(
                color_text(
                    f'The {folder_type} folder ("{str(folder_path)}") does not exist; create (y/n): ',
                    color_flag="yellow",
                )
            )
            .strip()
            .lower()
        ):
            if choice in ("y", "n"):
                break

        if choice == "y":
            os.makedirs(folder_path, exist_ok=True)
        else:
            logger.warning(
                "{} does not exist, and user selected not to create.  Exiting clever.",
                folder_path,
            )
            sys.exit(-1)


def get_targets():

    logger.info(f"Loaded targets from {TARGETS_FILE} ...")
    logger.complete()
    if not os.path.isfile(TARGETS_FILE):
        input_text = color_text(
            f'The targets file, "{TARGETS_FILE}", was not found; create (y/n): ',
            "yellow",
        )
        while create_targets_file := input(input_text).strip().lower():
            if create_targets_file in ("y", "n"):
                break

        if create_targets_file == "y":
            run_grab_targets()
        else:
            logger.error(
                "Please run src\\common\\setup\\grabtargets.py first to generate the unique targets list."
            )
            sys.exit(1)

    with open(TARGETS_FILE, "r") as fh:
        targets = [target for line in fh if (target := line.strip())]

    if not targets:
        logger.error(f"Error: No targets found in {TARGETS_FILE}")
        sys.exit(1)

    logger.info(f"Loaded {len(targets)} targets from {TARGETS_FILE}")
    return targets


def run_all_steps():
    args = parse_args()

    # Set up logging
    setup_logging(args, check_run_dir)

    check_run_dir("runs", RUN_DIR)

    clean_output_min_folder(OUTPUT, args.clean_outputs_min)

    # Read targets from the unique_targets.txt file
    targets = get_targets()

    # Main execution loop
    for target in targets:
        if run_sequencer(target, args.dry_run) is False:
            raise Exception("An error occured running sequencert")
        run_organize(target)
        run_clever_rules(target)
        run_filter_templated(target)
        # run_cross_class_filter(target)

    # Run make_one_out.py
    logger.info("Running make_one_out.py...")
    result = subprocess.run(
        ["python3", os.path.join(SRC_DIR, "make_one_out.py"), OUTPUT],
        capture_output=True,
        text=True,
    )
    logger.info(f"STDOUT: {result.stdout}")
    if result.stderr:
        logger.warning(f"STDERR: {result.stderr}")

    logger.info("All targets processed.")
    logger.info("All targets processed.")


if __name__ == "__main__":

    # Set up logging
    # Parse command-line arguments
    run_all_steps()
