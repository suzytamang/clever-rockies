import argparse
import json
import os

import pandas as pd


def load_dictionary(dict_path):
    dict_file = pd.read_csv(dict_path, sep="|", header=0)
    dict_file.columns = ['dict_ID', 'TERM', 'CLASS', 'SUBCLASS']
    return dict_file


def load_cross_class_items(cross_class_path):
    with open(cross_class_path, 'r') as file:
        return json.load(file)


def cross_tag_search(data_path, output_path, removed_path, cross_class, dict_file):
    if os.path.exists(data_path) and os.path.getsize(data_path) > 0:
        all_data = pd.read_csv(data_path, sep="|", header=None, on_bad_lines='warn', keep_default_na=False)
        print(f"Processing {data_path}...")

        to_be_dropped = {}
        for _, row in all_data.iterrows():
            snippet_id, dict_id, snippet = row[1], row[11], row[13]
            if str(dict_id) in cross_class:
                matching_parents = []
                for parent in cross_class[str(dict_id)]:
                    parent_term = dict_file['TERM'][dict_file['dict_ID'] == parent].iloc[0]
                    if parent_term in snippet:
                        matching_parents.append(parent)
                if matching_parents:
                    to_be_dropped[snippet_id] = matching_parents

        after_cross_tags_removed = all_data[~all_data[1].isin(to_be_dropped.keys())]
        removed_cross_tags = all_data[all_data[1].isin(to_be_dropped.keys())]

        if not after_cross_tags_removed.empty:
            after_cross_tags_removed.to_csv(output_path, sep='|', index=False, header=False)
        else:
            open(output_path, 'w').close()

        if not removed_cross_tags.empty:
            # Add information about matching parents
            removed_cross_tags['matching_parents'] = removed_cross_tags[1].map(to_be_dropped)
            removed_cross_tags.to_csv(removed_path, sep='|', index=False, header=False)
        else:
            open(removed_path, 'w').close()
    else:
        print(f"File {data_path} does not exist or is empty.")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--target', type=str, required=True, help='Path for TARGET class')
    parser.add_argument('-d', '--dictionary', type=str, required=True, help='Path and filename for the dictionary')
    parser.add_argument('-c', '--crossclass', type=str, required=True, help='File name of the cross_class_items list')
    args = parser.parse_args()

    dict_file = load_dictionary(args.dictionary)
    cross_class_items = load_cross_class_items(os.path.join(os.path.dirname(args.dictionary), args.crossclass))

    for label in ['Pos', 'Neg']:
        input_file = os.path.join(args.target, f"all{label}.txt")
        output_file = os.path.join(args.target, f"all{label}_cross_tag.txt")
        removed_file = os.path.join(args.target, f"all{label}_cross_tag_removed.txt")

        cross_tag_search(input_file, output_file, removed_file, cross_class_items, dict_file)


if __name__ == "__main__":
    main()