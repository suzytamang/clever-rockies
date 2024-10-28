#!/usr/bin/env bash

# Define constants
LEXICON="../../res/dicts/dict.txt"
METADATA="../../tests/resources/test_notes/metadata/test_metadata_one_line.txt"
OUTPUT="../../tests/outputs"
ANTS="linkedAnts.txt"

# Change to the script's directory
cd "$(dirname "$0")"

# Function to run organize.py with common arguments
run_organize() {
    local target=$1
    python3 organize.py "$OUTPUT/$target" "$LEXICON" "$METADATA" "$OUTPUT/$target/$ANTS"
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

# Run organize.py for each target
for target in "${targets[@]}"; do
    echo "Processing organize $target..."
    run_organize "$target"
done

echo "All targets processed.."