#!/usr/bin/env bash

# Define constants
LEXICON="../../res/dicts/dict.txt"
HEADERS="../../res/headers.txt"
CORPUS="../../tests/resources/test_notes/tsv/test_notes_one_line.txt"
OUTPUT="../../tests/outputs"
SNIPPETS=250
LGCONTEXT=3
RGCONTEXT=2
WORKERS=8

# Change to the script's directory
cd "$(dirname "$0")"

# Function to run sequencer.py with common arguments
run_sequencer() {
    local target=$1
    python sequencer.py \
        --lexicon "$LEXICON" \
        --section-headers "$HEADERS" \
        --main-targets "$target" \
        --snippet-length "$SNIPPETS" \
        --snippets \
        --notes "$CORPUS" \
        --workers "$WORKERS" \
        --output "$OUTPUT/$target" \
        --left-gram-context "$LGCONTEXT" \
        --right-gram-context "$RGCONTEXT"
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

# Run sequencer for each target
for target in "${targets[@]}"; do
    echo "Processing sequencer $target..."
    run_sequencer "$target"
done

echo "All targets processed.."