#!/usr/bin/env python3

import os
import sys

# Get the directory of the current script
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# Go up one level to the parent directory
PARENT_DIR = os.path.dirname(SCRIPT_DIR)

# Define paths
DICT_FILE = os.path.join(PARENT_DIR, "res", "dicts", "dict.txt")
RUN_DIR = os.path.join(PARENT_DIR, "run")

# Output files
FULL_CONCEPTS_FILE = os.path.join(RUN_DIR, "unique_concepts_full.txt")
UNIQUE_TARGETS_FILE = os.path.join(RUN_DIR, "unique_targets.txt")

# Create the 'run' directory if it doesn't exist
os.makedirs(RUN_DIR, exist_ok=True)

# Check if the input file exists
if not os.path.isfile(DICT_FILE):
    print(f"Error: {DICT_FILE} not found!")
    sys.exit(1)

# Extract all unique concepts and save to the full concepts file
print(f"Extracting all unique concepts from {DICT_FILE}...")
unique_concepts = set()

try:
    with open(DICT_FILE, 'r') as f:
        for line in f:
            parts = line.strip().split('|')
            if len(parts) >= 3:
                concept = parts[2].strip()
                if concept:
                    unique_concepts.add(concept)

    with open(FULL_CONCEPTS_FILE, 'w') as f:
        for concept in sorted(unique_concepts):
            f.write(f"{concept}\n")

    print(f"All unique concepts have been saved to {FULL_CONCEPTS_FILE}")
    print(f"Number of all unique concepts: {len(unique_concepts)}")
except IOError as e:
    print(f"Error: Failed to create {FULL_CONCEPTS_FILE}")
    print(f"IOError: {e}")
    sys.exit(1)

# Filter out specified terms and save to the unique targets file
print("Filtering unique targets...")
excluded_terms = {'DOT', 'PUNCT', 'HX', 'NEGEX', 'PREV', 'RISK', 'SCREEN', 'FAM'}
unique_targets = [concept for concept in unique_concepts if concept not in excluded_terms]

try:
    with open(UNIQUE_TARGETS_FILE, 'w') as f:
        for target in sorted(unique_targets):
            f.write(f"{target}\n")

    print(f"Unique targets have been saved to {UNIQUE_TARGETS_FILE}")
    print(f"Number of unique targets: {len(unique_targets)}")
except IOError as e:
    print(f"Error: Failed to create {UNIQUE_TARGETS_FILE}")
    print(f"IOError: {e}")
    sys.exit(1)