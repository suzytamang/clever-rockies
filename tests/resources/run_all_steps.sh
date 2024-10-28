#!/usr/bin/env bash

# Define base paths
BASE_DIR="../.."
RES_DIR="$BASE_DIR/res"
TESTS_DIR="$BASE_DIR/tests"
SRC_DIR="$BASE_DIR/src"

# Define constants
LEXICON="$RES_DIR/dicts/dict.txt"
HEADERS="$RES_DIR/headers.txt"
ANTS="linkedAnts.txt"
ASSESSMENTTERMS="$RES_DIR/assessment_terms.txt"
OTHERTERMS="$RES_DIR/other_terms_to_drop.txt"
NEG_TRIGS="$RES_DIR/neg_trigs.json"
NA_TRIGS="$RES_DIR/na_trigs.json"
CROSS_CLASS_FILE="$RES_DIR/ccf.json"

CORPUS="$TESTS_DIR/resources/test_notes/tsv/test_notes_one_line.txt"
METADATA="$TESTS_DIR/resources/test_notes/metadata/test_metadata_one_line.txt"
OUTPUT="$TESTS_DIR/outputs_min"

SNIPPETS=250
LGCONTEXT=3
RGCONTEXT=2
WORKERS=8

# Store the initial directory
INITIAL_DIR=$(pwd)

# Remove existing outputs and create a new directory
rm -rf "$OUTPUT" && mkdir -p "$OUTPUT"

# Read targets from the unique_targets.txt file
TARGETS_FILE="$RES_DIR/unique_targets.txt"

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

# overwrite Array of targets with static one below for testing one concept
#targets=(
#    "LONELINESS" "XYLA"
#)

# Function to run sequencer.py (Step 2)
run_sequencer() {
    local target=$1
    echo "Processing sequencer $target..."
    cd "$INITIAL_DIR/$SRC_DIR/step2"
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
    cd "$INITIAL_DIR"
}

# Function to run organize.py (Step 3)
run_organize() {
    local target=$1
    echo "Processing organize $target..."
    cd "$INITIAL_DIR/$SRC_DIR/step3"
    python3 organize.py "$OUTPUT/$target" "$LEXICON" "$METADATA" "$OUTPUT/$target/$ANTS"
    cd "$INITIAL_DIR"
}

# Function to run cleverRules.py (Step 4)
run_clever_rules() {
    local target=$1
    echo "Processing run_clever_rules $target..."
    cd "$INITIAL_DIR/$SRC_DIR/step4"
    python cleverRules.py "$OUTPUT/$target" "$target" "$NEG_TRIGS" "$NA_TRIGS"
    cd "$INITIAL_DIR"
}

# Function to run filterTemplated.py (Step 5)
run_filter_templated() {
    local target=$1
    echo "Filtering tagged templated text for $target"
    cd "$INITIAL_DIR/$SRC_DIR/step5"
    python3 filterTemplated.py -p "$OUTPUT/" -t "$target" -a "$ASSESSMENTTERMS" -o "$OTHERTERMS" -sp 14 -tp 6
    cd "$INITIAL_DIR"
}

run_cross_class_filter() {
    local target=$1
    echo "Running cross-class filter for $target..."
    cd "$INITIAL_DIR/$SRC_DIR/step5"
    python3 cross_class_filter.py -t "$OUTPUT/$target" -d "$LEXICON" -c "$CROSS_CLASS_FILE"
    cd "$INITIAL_DIR"
}

# Main execution loop
for target in "${targets[@]}"; do
    run_sequencer "$target"
    run_organize "$target"
    run_clever_rules "$target"
    run_filter_templated "$target"
    #run_cross_class_filter "$target"
done

echo "All targets processed.."
