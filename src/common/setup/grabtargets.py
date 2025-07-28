#!/usr/bin/env python3

import os
import sys
from loguru import logger
from common.consts import LEXICON, RUN_DIR


def run_grab_targets():

    # Define paths

    # Output files
    FULL_CONCEPTS_FILE = os.path.join(RUN_DIR, "unique_concepts_full.txt")
    UNIQUE_TARGETS_FILE = os.path.join(RUN_DIR, "unique_targets.txt")

    # Create the 'run' directory if it doesn't exist
    os.makedirs(RUN_DIR, exist_ok=True)

    # Check if the input file exists
    if not os.path.isfile(LEXICON):
        print(f"Error: {LEXICON} not found!")
        sys.exit(1)

    # Extract all unique concepts and save to the full concepts file
    print(f"Extracting all unique concepts from {LEXICON}...")
    unique_concepts = set()

    try:
        logger.info("Loading lexicon (dict.txt) entries ...")
        with open(LEXICON, "r") as f:
            for line in f:
                parts = line.strip().split("|")
                if len(parts) >= 3:
                    concept = parts[2].strip()
                    if concept:
                        unique_concepts.add(concept)
        logger.info("Lexicon (dict.txt) entries loaded")
        logger.info("Writing concepts file ...")
        with open(FULL_CONCEPTS_FILE, "w") as f:
            for concept in sorted(unique_concepts):
                f.write(f"{concept}\n")
        logger.info("Concepts file written to {}", FULL_CONCEPTS_FILE)

        logger.info(f"All unique concepts have been saved to {FULL_CONCEPTS_FILE}")
        logger.info(f"Number of all unique concepts: {len(unique_concepts)}")
    except IOError as e:
        logger.error(f"Error: Failed to create {FULL_CONCEPTS_FILE}")
        logger.error(f"IOError: {e}")
        sys.exit(1)

    # Filter out specified terms and save to the unique targets file
    logger.info("Filtering unique targets...")
    excluded_terms = {"DOT", "PUNCT", "HX", "NEGEX", "PREV", "RISK", "SCREEN", "FAM"}
    unique_targets = [
        concept for concept in unique_concepts if concept not in excluded_terms
    ]

    try:
        with open(UNIQUE_TARGETS_FILE, "w") as f:
            for target in sorted(unique_targets):
                f.write(f"{target}\n")

        logger.info(f"Unique targets have been saved to {UNIQUE_TARGETS_FILE}")
        logger.info(f"Number of unique targets: {len(unique_targets)}")
    except IOError as e:
        logger.info(f"Error: Failed to create {UNIQUE_TARGETS_FILE}")
        logger.info(f"IOError: {e}")
        sys.exit(1)


if __name__ == "__main__":

    run_grab_targets()
