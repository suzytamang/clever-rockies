#!/usr/bin/env python3

import os
import csv

# Define file paths
input_file = 'test_notes_with_metadata_one_line.txt'
output_metadata_file = os.path.join('metadata', 'test_metadata_one_line.txt')
output_notes_file = os.path.join('tsv', 'test_notes_one_line.txt')

# Ensure output directories exist
os.makedirs(os.path.dirname(output_metadata_file), exist_ok=True)
os.makedirs(os.path.dirname(output_notes_file), exist_ok=True)

# Define metadata headers
metadata_headers = ['PATIENTID', 'NOTEID', 'STATION', 'TIMESTAMP', 'NOTETYPE', 'VISIDSID', 'AGE', 'GENDER', 'OPCODE']


def remove_zwnbsp(text):
    return text.replace('\ufeff', '')


def split_line(line):
    parts = remove_zwnbsp(line).strip().split('|')
    # Swap the first two elements to match the desired order
    metadata = [parts[1], parts[0]] + parts[2:9]
    note_id = parts[0]  # NOTEID is the first element in the original order
    note = '\t'.join([note_id, '|'.join(parts[9:])])
    return metadata, note


# Process the input file and write to output files
with open(input_file, 'r', encoding='utf-8-sig') as infile, \
        open(output_metadata_file, 'w', newline='', encoding='utf-8') as metadata_file, \
        open(output_notes_file, 'w', encoding='utf-8') as notes_file:
    # Write metadata header
    metadata_writer = csv.writer(metadata_file, delimiter='|')
    metadata_writer.writerow(metadata_headers)

    # Process each line
    for line in infile:
        metadata, note = split_line(line)

        # Write metadata
        metadata_writer.writerow(metadata)

        # Write note
        notes_file.write(note + '\n')

print(f"Metadata written to: {output_metadata_file}")
print(f"Notes written to: {output_notes_file}")