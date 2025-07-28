#!/usr/bin/env python3

import os
import subprocess
import sys
from pathlib import Path

from dotenv import load_dotenv

from common.folder_mgmt import clean_output_min_folder
from common.parameters.sequencer_parameter import SequencerParameters
from parse_args import parse_args
from run_all_consts import (
    ANTS,
    ASSESSMENTTERMS,
    CORPUS,
    CROSS_CLASS_FILE,
    HEADERS,
    LEXICON,
    METADATA,
    NA_TRIGS,
    NEG_TRIGS,
    OTHERTERMS,
    OUTPUT,
    RUN_DIR,
    SRC_DIR,
    get_environment_var,
)
from setup_logging import setup_logging
from step2.sequencer import sequencer_main

load_dotenv()

# Set up logging
# Parse command-line arguments
args = parse_args()

# Set up logging
logger = setup_logging(args)


clean_output_min_folder(OUTPUT, args.clean_outputs_min)

# Read targets from the unique_targets.txt file
TARGETS_FILE = os.path.join(RUN_DIR, "unique_targets.txt")

if not os.path.isfile(TARGETS_FILE):
    logger.error(f"Error: {TARGETS_FILE} not found!")
    logger.error("Please run grabtargets.sh first to generate the unique targets list.")
    sys.exit(1)

with open(TARGETS_FILE, "r") as fh:
    targets = [target for line in fh if (target := line.strip())]

if not targets:
    logger.error(f"Error: No targets found in {TARGETS_FILE}")
    sys.exit(1)

logger.info(f"Loaded {len(targets)} targets from {TARGETS_FILE}")


# Function to run sequencer.py (Step 2)
def run_sequencer(target: str, dry_run) -> bool:

    sequencer_parameters = SequencerParameters(
        workers=get_environment_var("WORKERS", int),
        right_gram=get_environment_var("RGCONTEXT", int),
        left_gram=get_environment_var("LGCONTEXT", int),
        snippet_length=get_environment_var("SNIPPETS", int),
        snippets=snippets,
        main_targets=target,
        lexicon=LEXICON,
        section_headers=HEADERS,
        output_folder=Path(OUTPUT) / target,
        notes_file=CORPUS,
    )

    from common.step_runner import DirectStepRunner

    runner = DirectStepRunner(
        "sequencer", sequencer_parameters, sequencer_main, dry_run=dry_run
    )

    return runner.run()

    # logging.debug(f"Processing sequencer {target}...")
    # result = subprocess.run(
    #     [
    #         "python",
    #         os.path.join(SRC_DIR, "step2", "sequencer.py"),
    #         "--lexicon",
    #         LEXICON,
    #         "--section-headers",
    #         HEADERS,
    #         "--main-targets",
    #         target,
    #         "--snippet-length",
    #         str(SNIPPETS),
    #         "--snippets",
    #         "--notes",
    #         CORPUS,
    #         "--workers",
    #         str(WORKERS),
    #         "--output",
    #         os.path.join(OUTPUT, target),
    #         "--left-gram-context",
    #         str(LGCONTEXT),
    #         "--right-gram-context",
    #         str(RGCONTEXT),
    #     ],
    #     capture_output=True,
    #     text=True,
    # )
    # logging.debug(f"STDOUT for {target} sequencer: {result.stdout}")
    # if result.stderr:
    #     logging.warning(f"STDERR for {target} sequencer: {result.stderr}")


# Function to run organize.py (Step 3)
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


# Function to run cleverRules.py (Step 4)
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


# Function to run filterTemplated.py (Step 5)
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
