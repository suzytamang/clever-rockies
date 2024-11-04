import os
import pandas as pd
from pathlib import Path
import sys

# Check if base directory is provided as an argument
if len(sys.argv) < 2:
    print("Usage: python make_one_out.py <base_directory>")
    sys.exit(1)

# Get the base directory from command line argument
base_dir = Path(sys.argv[1])

# Initialize an empty list to store all dataframes
all_dfs = []
sep='|'

# Loop through all subdirectories in the base directory
for category in base_dir.iterdir():
    if category.is_dir():
        # Define file paths
        allNA_path = category / 'allNA.txt'
        allNeg_path = category / 'allNeg.txt'
        allPos_path = category / 'allPos.txt'

        # Read each file into a dataframe, adding a 'Type' column
        if allNA_path.exists():
            df_NA = pd.read_csv(allNA_path, sep=sep)
            df_NA['Type'] = 'NA'
            all_dfs.append(df_NA)

        if allNeg_path.exists():
            df_Neg = pd.read_csv(allNeg_path, sep=sep)
            df_Neg['Type'] = 'Neg'
            all_dfs.append(df_Neg)

        if allPos_path.exists():
            df_Pos = pd.read_csv(allPos_path, sep=sep)
            df_Pos['Type'] = 'Pos'
            all_dfs.append(df_Pos)

        # Add the category information
        for df in all_dfs[-3:]:  # Last three dataframes added
            df['Category'] = category.name

# Concatenate all dataframes
final_df = pd.concat(all_dfs, ignore_index=True)

# Set pandas display options to show all columns and rows without truncation
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)

# Display the first few rows and basic info about the dataframe
print(final_df.head())
print(final_df.info())

# Save the dataframe to a CSV file
output_file = base_dir / 'All_outputs_filtered.txt'
final_df.to_csv(output_file, sep='|', index=False)

print(f"Combined output saved to: {output_file}")
print(f"Combined output length: {len(final_df)}")