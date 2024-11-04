#!/usr/bin/env python3

import os
import shutil
import subprocess
import sys

# Define base paths
BASE_DIR = "../.."
RES_DIR = os.path.join(BASE_DIR, "res")
TESTS_DIR = os.path.join(BASE_DIR, "tests")
SRC_DIR = os.path.join(BASE_DIR, "src")

# Define constants
LEXICON = os.path.join(RES_DIR, "dicts", "dict.txt")
HEADERS = os.path.join(RES_DIR, "headers.txt")
ANTS = "linkedAnts.txt"
ASSESSMENTTERMS = os.path.join(RES_DIR, "assessment_terms.txt")
OTHERTERMS = os.path.join(RES_DIR, "other_terms_to_drop.txt")
NEG_TRIGS = os.path.join(RES_DIR, "neg_trigs.json")
NA_TRIGS = os.path.join(RES_DIR, "na_trigs.json")
CROSS_CLASS_FILE = os.path.join(RES_DIR, "ccf.json")

CORPUS = os.path.join(TESTS_DIR, "resources", "test_notes", "tsv", "test_notes_one_line.txt")
METADATA = os.path.join(TESTS_DIR, "resources", "test_notes", "metadata", "test_metadata_one_line.txt")
OUTPUT = os.path.join(TESTS_DIR, "outputs_min")

SNIPPETS = 250
LGCONTEXT = 3
RGCONTEXT = 2
WORKERS = 2

# Store the initial directory
INITIAL_DIR = os.getcwd()

print(f"About to remove directory: {OUTPUT}")
confirm = input("Are you sure you want to proceed? (y/n): ").lower().strip()
if confirm != 'y':
    print("Operation cancelled.")
    sys.exit(0)

shutil.rmtree(OUTPUT, ignore_errors=True)
os.makedirs(OUTPUT, exist_ok=True)
print(f"Removed and recreated directory: {OUTPUT}")

# Read targets from the unique_targets.txt file
TARGETS_FILE = os.path.join(RES_DIR, "unique_targets.txt")

if not os.path.isfile(TARGETS_FILE):
    print(f"Error: {TARGETS_FILE} not found!")
    print("Please run grabtargets.sh first to generate the unique targets list.")
    sys.exit(1)

with open(TARGETS_FILE, 'r') as f:
    targets = [line.strip() for line in f if line.strip()]

if not targets:
    print(f"Error: No targets found in {TARGETS_FILE}")
    sys.exit(1)

print(f"Loaded {len(targets)} targets from {TARGETS_FILE}")

# Function to run sequencer.py (Step 2)
def run_sequencer(target):
    print(f"Processing sequencer {target}...")
    os.chdir(os.path.join(INITIAL_DIR, SRC_DIR, "step2"))
    subprocess.run([
        "python", "sequencer.py",
        "--lexicon", LEXICON,
        "--section-headers", HEADERS,
        "--main-targets", target,
        "--snippet-length", str(SNIPPETS),
        "--snippets",
        "--notes", CORPUS,
        "--workers", str(WORKERS),
        "--output", os.path.join(OUTPUT, target),
        "--left-gram-context", str(LGCONTEXT),
        "--right-gram-context", str(RGCONTEXT)
    ])
    os.chdir(INITIAL_DIR)

# Function to run organize.py (Step 3)
def run_organize(target):
    print(f"Processing organize {target}...")
    os.chdir(os.path.join(INITIAL_DIR, SRC_DIR, "step3"))
    subprocess.run([
        "python3", "organize.py",
        os.path.join(OUTPUT, target),
        LEXICON,
        METADATA,
        os.path.join(OUTPUT, target, ANTS)
    ])
    os.chdir(INITIAL_DIR)

# Function to run cleverRules.py (Step 4)
def run_clever_rules(target):
    print(f"Processing run_clever_rules {target}...")
    os.chdir(os.path.join(INITIAL_DIR, SRC_DIR, "step4"))
    subprocess.run([
        "python", "cleverRules.py",
        os.path.join(OUTPUT, target),
        target,
        NEG_TRIGS,
        NA_TRIGS
    ])
    os.chdir(INITIAL_DIR)

# Function to run filterTemplated.py (Step 5)
def run_filter_templated(target):
    print(f"Filtering tagged templated text for {target}")
    os.chdir(os.path.join(INITIAL_DIR, SRC_DIR, "step5"))
    subprocess.run([
        "python3", "filterTemplated.py",
        "-p", OUTPUT + "/",  # Add a trailing slash here
        "-t", target,
        "-a", ASSESSMENTTERMS,
        "-o", OTHERTERMS,
        "-sp", "14",
        "-tp", "6"
    ])
    os.chdir(INITIAL_DIR)

def run_cross_class_filter(target):
    print(f"Running cross-class filter for {target}...")
    os.chdir(os.path.join(INITIAL_DIR, SRC_DIR, "step5"))
    subprocess.run([
        "python3", "cross_class_filter.py",
        "-t", os.path.join(OUTPUT, target),
        "-d", LEXICON,
        "-c", CROSS_CLASS_FILE
    ])
    os.chdir(INITIAL_DIR)

# Main execution loop
for target in targets:
    run_sequencer(target)
    run_organize(target)
    run_clever_rules(target)
    run_filter_templated(target)
    # run_cross_class_filter(target)

# Run make_one_out.py
print("Running make_one_out.py...")
subprocess.run(["python3", "make_one_out.py", OUTPUT])
os.chdir(INITIAL_DIR)

print("All targets processed.")