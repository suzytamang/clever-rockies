#!/usr/bin/env bash

# Define constants
OUTPUT="../../tests/outputs"
ASSESSMENTTERMS="../../res/assessment_terms.txt"
OTHERTERMS="../../res/other_terms_to_drop.txt"

# Change to the script's directory
cd "$(dirname "$0")"

# Function to run filterTemplated.py with common arguments
run_filter_templated() {
    local target=$1
    echo "Filtering tagged templated text for $target"
    python3 filterTemplated.py -p "$OUTPUT/" -t "$target" -a "$ASSESSMENTTERMS" -o "$OTHERTERMS" -sp 14 -tp 6
    # echo "Removing cross target subset tags for $TARGET$POLARITY"
    # python3 cross_tagging_removal.py -d $LEXICON -t $OUTPUT/$TARGET -c $CROSSCLASS
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

# Run filterTemplated.py for each target
for target in "${targets[@]}"; do
    echo "Processing run_filter_templated $target..."
    run_filter_templated "$target"
done

echo "All targets processed."