#!/usr/bin/env python3

import argparse
import logging
import os
import subprocess
import sys
from datetime import datetime

from common.folder_mgmt import clean_output_min_folder


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


# Define base paths
# Get the directory of the current script
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
# Go up one level to the parent directory
BASE_DIR = os.path.dirname(SCRIPT_DIR)
RES_DIR = os.path.join(BASE_DIR, "res")
TESTS_DIR = os.path.join(BASE_DIR, "tests")
SRC_DIR = os.path.join(BASE_DIR, "src")
RUN_DIR = os.path.join(BASE_DIR, "run")

# Define constants
LEXICON = os.path.join(RES_DIR, "dicts", "dict.txt")
HEADERS = os.path.join(RES_DIR, "headers.txt")
ANTS = "linkedAnts.txt"
ASSESSMENTTERMS = os.path.join(RES_DIR, "assessment_terms.txt")
OTHERTERMS = os.path.join(RES_DIR, "other_terms_to_drop.txt")
NEG_TRIGS = os.path.join(RES_DIR, "neg_trigs.json")
NA_TRIGS = os.path.join(RES_DIR, "na_trigs.json")
CROSS_CLASS_FILE = os.path.join(RES_DIR, "ccf.json")

CORPUS = os.path.join(TESTS_DIR, "test_notes", "tsv", "test_notes_one_line.txt")
METADATA = os.path.join(
    TESTS_DIR, "test_notes", "metadata", "test_metadata_one_line.txt"
)
OUTPUT = os.path.join(RUN_DIR, "outputs_min")


SNIPPETS = 250
LGCONTEXT = 3
RGCONTEXT = 2
WORKERS = 2


# Set up logging
def setup_logging(args):
    log_file: str = os.path.join(
        RUN_DIR, f"run_all_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    )

    console_level = args.log_level  # This will be WARNING by default

    # Set up file handler (always DEBUG level)
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.DEBUG)
    file_formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    file_handler.setFormatter(file_formatter)

    # Set up console handler (level based on user input)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(console_level)
    console_formatter = logging.Formatter("%(levelname)s: %(message)s")
    console_handler.setFormatter(console_formatter)

    # Set up root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)  # This ensures all messages are processed
    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)

    logging.info(f"Console logging level set to: {logging.getLevelName(console_level)}")
    logging.debug("File logging level set to: DEBUG")


# Parse command-line arguments
args = parse_args()

# Set up logging
setup_logging(args)

# Print paths for debugging
logging.debug(f"BASE_DIR: {BASE_DIR}")
logging.debug(f"RES_DIR: {RES_DIR}")
logging.debug(f"TESTS_DIR: {TESTS_DIR}")
logging.debug(f"SRC_DIR: {SRC_DIR}")
logging.debug(f"CORPUS: {CORPUS}")
logging.debug(f"METADATA: {METADATA}")
logging.debug(f"OUTPUT: {OUTPUT}")
logging.debug(f"RUN_DIR: {RUN_DIR}")


clean_output_min_folder(OUTPUT, args.clean_outputs_min, logging)

# Read targets from the unique_targets.txt file
TARGETS_FILE = os.path.join(RUN_DIR, "unique_targets.txt")

if not os.path.isfile(TARGETS_FILE):
    logging.error(f"Error: {TARGETS_FILE} not found!")
    logging.error(
        "Please run grabtargets.sh first to generate the unique targets list."
    )
    sys.exit(1)

with open(TARGETS_FILE, "r") as f:
    targets = [line.strip() for line in f if line.strip()]

if not targets:
    logging.error(f"Error: No targets found in {TARGETS_FILE}")
    sys.exit(1)

logging.info(f"Loaded {len(targets)} targets from {TARGETS_FILE}")


# Function to run sequencer.py (Step 2)
def run_sequencer(target, dry_run) -> bool:
    from common.step_runner import SubprocessStepRunner

    runner = SubprocessStepRunner(
        os.path.join(SRC_DIR, "step2", "sequencer.py"),
        "sequencer",
        logging,
        {
            "lexicon": LEXICON,
            "section-headers": HEADERS,
            "main-targets": target,
            "snippet-length": str(SNIPPETS),
            "snippets": None,
            "notes": CORPUS,
            "workers": str(WORKERS),
            "output": os.path.join(OUTPUT, target),
            "left-gram-context": str(LGCONTEXT),
            "right-gram-context": str(RGCONTEXT),
        },
        dry_run=dry_run,
    )

    return runner.run(target)

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
    logging.debug(f"Processing organize {target}...")
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
    logging.debug(f"STDOUT for {target} organize: {result.stdout}")
    if result.stderr:
        logging.warning(f"STDERR for {target} organize: {result.stderr}")


# Function to run cleverRules.py (Step 4)
def run_clever_rules(target):
    logging.debug(f"Processing run_clever_rules {target}...")
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
    logging.debug(f"STDOUT for {target} run_clever_rules: {result.stdout}")
    if result.stderr:
        logging.warning(f"STDERR for {target} run_clever_rules: {result.stderr}")


# Function to run filterTemplated.py (Step 5)
def run_filter_templated(target):
    logging.debug(f"Filtering tagged templated text for {target}")
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
    logging.debug(f"STDOUT for {target} filterTemplated: {result.stdout}")
    if result.stderr:
        logging.warning(f"STDERR for {target} filterTemplated: {result.stderr}")


def run_cross_class_filter(target):
    logging.debug(f"Running cross-class filter for {target}...")
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
    logging.debug(f"STDOUT for {target} cross_class_filter: {result.stdout}")
    if result.stderr:
        logging.warning(f"STDERR for {target} cross_class_filter: {result.stderr}")


# Main execution loop
for target in targets:
    if run_sequencer(target, args.dry_run) is False:
        raise Exception("An error occured running sequencert")
    run_organize(target)
    run_clever_rules(target)
    run_filter_templated(target)
    # run_cross_class_filter(target)

# Run make_one_out.py
logging.info("Running make_one_out.py...")
result = subprocess.run(
    ["python3", os.path.join(SRC_DIR, "make_one_out.py"), OUTPUT],
    capture_output=True,
    text=True,
)
logging.info(f"STDOUT: {result.stdout}")
if result.stderr:
    logging.warning(f"STDERR: {result.stderr}")

logging.info("All targets processed.")
