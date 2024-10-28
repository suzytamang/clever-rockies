#!/bin/bash

# Path to the dict.txt file
DICT_FILE="../res/dicts/dict.txt"

# Output files
FULL_CONCEPTS_FILE="../res/unique_concepts_full.txt"
UNIQUE_TARGETS_FILE="../res/unique_targets.txt"

# Check if the input file exists
if [ ! -f "$DICT_FILE" ]; then
    echo "Error: $DICT_FILE not found!"
    exit 1
fi

# Extract all unique concepts and save to the full concepts file
echo "Extracting all unique concepts from $DICT_FILE..."
awk -F'|' '{print $3}' "$DICT_FILE" | sort -u | sed '/^$/d' > "$FULL_CONCEPTS_FILE"

# Check if the full concepts file was created successfully
if [ $? -eq 0 ] && [ -f "$FULL_CONCEPTS_FILE" ]; then
    echo "All unique concepts have been saved to $FULL_CONCEPTS_FILE"
    echo "Number of all unique concepts: $(wc -l < "$FULL_CONCEPTS_FILE")"
else
    echo "Error: Failed to create $FULL_CONCEPTS_FILE"
    exit 1
fi

# Filter out specified terms and save to the unique targets file
echo "Filtering unique targets..."
grep -vE '^(DOT|PUNCT|HX|NEGEX|PREV|RISK|SCREEN|FAM)$' "$FULL_CONCEPTS_FILE" > "$UNIQUE_TARGETS_FILE"

# Check if the unique targets file was created successfully
if [ $? -eq 0 ] && [ -f "$UNIQUE_TARGETS_FILE" ]; then
    echo "Unique targets have been saved to $UNIQUE_TARGETS_FILE"
    echo "Number of unique targets: $(wc -l < "$UNIQUE_TARGETS_FILE")"
else
    echo "Error:  Failed to create $UNIQUE_TARGETS_FILE"
    exit 1
fi