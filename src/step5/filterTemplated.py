import os
import sys
import argparse


def remove_templated_data(snippet, stoplist, title):
    omit = 0
    testsnip = snippet.lower()

    # Look for strings associated with assessments/semi-structured data
    for term in stoplist:
        if term.lower() in testsnip:
            omit = 1
            break

    if omit == 0:
        # Check for group notes by looking at Standard Note Title
        if "GROUP" in title:
            omit = 1
            # Conditions based on frequency
        elif testsnip.count("(") > 4:
            omit = 1
        elif testsnip.count(" x ") > 3:
            omit = 1
        elif testsnip.count("[") > 2:
            omit = 1
        elif testsnip.count("?") > 1:
            omit = 1
        elif (testsnip.count("yes") + testsnip.count("denied") + testsnip.count("no")) > 3:
            omit = 1
        elif testsnip.count("_x_") > 0:
            omit = 1
        elif testsnip.count("'y'") > 0:
            omit = 1
        elif testsnip.count(" n ") > 0:
            omit = 1
        elif testsnip.count("during the past month") + \
                testsnip.count("most of the day") + \
                testsnip.count("nearly every day") > 1:
            omit = 1

    return omit


import os
import shutil

def templated(path, target, stoplist):
    labels = ['/allPos', '/allNeg']

    for label in labels:
        fin = path + target + label + "_unfiltered.txt"
        fout_filtered_path = path + target + label + "_filtered.txt"
        fout_unfiltered_path = path + target + label + "_unfiltered.txt"
        fd_dropped_path = path + target + "/filtered_out" + label + ".txt"

        # Create directories if they don't exist
        os.makedirs(os.path.dirname(fout_filtered_path), exist_ok=True)
        os.makedirs(os.path.dirname(fd_dropped_path), exist_ok=True)

        # Check if unfiltered file exists
        if not os.path.exists(fin):
            print(f"Input file not found: {fin}")
            continue

        # Open filtered and dropped files for writing
        with open(fout_filtered_path, "w") as fout_filtered, open(fd_dropped_path, "w") as fd_dropped:
            try:
                with open(fin, "r") as f:
                    for line in f:
                        tmp = line.strip().split("|")
                        snippet = tmp[snippet_column][9:]  # Remove "SNIPPET: " prefix
                        testsnip = snippet.lower()
                        title = tmp[title_column]

                        omit = remove_templated_data(snippet, stoplist, title)

                        if omit == 0:
                            fout_filtered.write(line)
                        else:
                            fd_dropped.write(line)

            except IOError:
                print(f"Error reading file: {fin}")

    print("Filtering complete.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--path', type=str, required=True,
                        help='path of directory where output lives')
    parser.add_argument('-t', '--target', type=str, required=True,
                        help='Label used for the target concept in the output directory')
    parser.add_argument('-a', '--assessment_terms', type=str, required=True,
                        help='File with list of terms that indicate assessment')
    parser.add_argument('-o', '--other_terms', type=str, required=False, default='file.txt',
                        help='Optional other file with terms that should trigger dropping the snippet')
    parser.add_argument('-sp', '--snippet_position', type=int, required=True,
                        help='Position of text in snippet (one-based column number)')
    parser.add_argument('-tp', '--title_position', type=int, required=True,
                        help='Position of standard title in snippet (one-based column number)')

    args = parser.parse_args()

    path = args.path
    target = args.target
    assess = args.assessment_terms
    other = args.other_terms
    snippet_column = args.snippet_position - 1
    title_column = args.title_position - 1

    # Combine assessment terms and (optional) other terms
    stoplist = []
    try:
        with open(assess) as fa:
            stoplist.extend([line.strip() for line in fa if line.strip()])
    except IOError:
        sys.exit("No file by the name " + assess + ". Filter aborted.")

    if other != 'file.txt':
        try:
            with open(other) as fo:
                stoplist.extend([line.strip() for line in fo if line.strip()])
        except IOError:
            sys.exit("No file by the name " + other + ". Filter aborted.")

    templated(path, target, stoplist)