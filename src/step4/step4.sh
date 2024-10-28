#!/usr/bin/env bash

# Define constants
OUTPUT="../../tests/outputs"
NEG_TRIGS="../../res/neg_trigs.json"
NA_TRIGS="../../res/na_trigs.json"

# Change to the script's directory
cd "$(dirname "$0")"

# Function to run cleverRules.py with common arguments
run_clever_rules() {
    local target=$1
    python cleverRules.py "$OUTPUT/$target" "$target" "$NEG_TRIGS" "$NA_TRIGS"
}

# Read targets from the unique_targets.txt file
TARGETS_FILE="../../res/unique_targets.txt"

if [ ! -f "$TARGETS_FILE" ]; then
    echo "Error: $TARGETS_FILE not found!"
    echo "Please run grabtargets.sh first to generate the unique targets list."
    exit 1
fi

# Read targets into an array
readarray -t targets < "$TARGETS_FILE"

# Check if targets were successfully read
if [ ${#targets[@]} -eq 0 ]; then
    echo "Error: No targets found in $TARGETS_FILE"
    exit 1
fi

echo "Loaded ${#targets[@]} targets from $TARGETS_FILE"

# overwrite Array of targets with static one below for testing 2+- concept(s)
#targets=(
#    "LONELINESS" "XYLA"
#)

# Run cleverRules.py for each target
for target in "${targets[@]}"; do
    echo "Processing run_clever_rules $target..."
    run_clever_rules "$target"
done

echo "All targets processed."