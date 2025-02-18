import re

def process_snippet(snippet):
    tokens = snippet.split(" ")
    if len(tokens) >= 3:
        tmp = snippet.rsplit(' ', 1)[0]
        tmp = ' '.join(tmp.split()[2:])
        return "SNIPPET:" + tmp
    return snippet

def transform_snippet_id(old_id):
    # Assuming old_id format is "S<number>-<concept>"
    match = re.match(r'S(\d+)-(\w+)', old_id)
    if match:
        number, concept = match.groups()
        return f"{concept}-{number}"
    return old_id  # Return original if it doesn't match expected format

def templated(path, target, stoplist):

    #NOTE: Removes templated text, mostly assessment related, sometimes medication list.

    #TODO: Have match with terms in stoplist account for end tokens (group but not groups).
    #TODO: Filter # points but not 'stuck points'.
    #TODO: Filter "several days" but not "for several days".
  
    labels = ['/allPos', '/allNeg', '/allNA']

    # Drop snippets that meet criteria.

    fd_dropped = open(path+target + "/filtered_out.txt", "w")
  
    for label in labels:
  
        fin = path + target + label + "_unfiltered.txt"
        fd_filtered = open(path + target + label + ".txt", "w")
  
        try:
            with open(fin) as f:
      
                for line in f:
      
                    omit = 0
                    tmp = line.strip().split("|")
                    # Snippet starts with the pre-fix 'SNIPPET: '.
                    # snippet = tmp[snippet_column][9:]
                    # testsnip = snippet.lower()
                    snippet = tmp[snippet_column]  # Use the full snippet for filtering
                    testsnip = snippet.lower()
                    # look for strings associated with assessments/semi-structured data
                    for term in stoplist:
                        if term.lower() in testsnip:
                            print("OMIT 0:", snippet, file=fd_dropped, flush=True)
                            omit = 1
                            break
      
                    if omit == 0:
                        # check for group notes by looking at Standard Note Title
                        if "GROUP" in tmp[title_column]:
                            print("OMIT 1:", tmp[title_column], file=fd_dropped, flush=True)
                            omit = 1           
                        # Conditions based on frequency.
                        elif testsnip.count("(") > 4:
                            print("OMIT 2:", snippet, file=fd_dropped, flush=True)
                            omit = 1
                        elif testsnip.count(" x ") > 3:
                            print("OMIT 3:", snippet, file=fd_dropped, flush=True)
                            omit = 1
                        elif testsnip.count("[") > 2:
                            print("OMIT 4:", snippet, file=fd_dropped, flush=True)
                            omit = 1
                        elif testsnip.count("?") > 1:
                            print("OMIT 5:", snippet, file=fd_dropped, flush=True)
                            omit = 1
                        elif (testsnip.count("yes") + \
                            testsnip.count("denied") + \
                            testsnip.count("no")) > 3:
                            print("OMIT 6:", snippet, file=fd_dropped, flush=True)
                            omit = 1
                        elif testsnip.count("_x_") > 0:
                            print("OMIT 7:", snippet, file=fd_dropped, flush=True)
                            omit = 1
                        elif testsnip.count("'y'") > 0:
                            print("OMIT 8:", snippet, file=fd_dropped, flush=True)
                            omit = 1
                        elif testsnip.count(" n ") > 0:
                            print("OMIT 9:", snippet, file=fd_dropped, flush=True)
                            omit = 1
                        # : catches few and wrong at that.
                        #elif testsnip.count(":") > 6:
                        #    print("OMIT 10:", snippet, file=fd_dropped, flush=True)
                        #    omit = 1
                        # Combined 11 and 12 in 13.
                        #elif testsnip.count("most of the time") > 1:
                        #    print("OMIT 11:", snippet, file=fd_dropped, flush=True)
                        #    omit = 1
                        #elif testsnip.count("nearly every day") > 1:
                        #    print("OMIT 12:", snippet, file=fd_dropped, flush=True)
                        #    omit = 1
                        elif testsnip.count("during the past month") + \
                            testsnip.count("most of the day") + \
                            testsnip.count("nearly every day") > 1:
                            print("OMIT 13:", snippet, file=fd_dropped, flush=True)
                            omit = 1
      
                    if omit == 0:
                        # Only process the snippet if it passes the filter
                        # Moved dropping first and last token back to step 4 as it should only happen if those
                        # tokens are not part of a tagged term.
                        tmp[snippet_column] = snippet
                        # Transform the snippet ID before writing
                        tmp[1] = transform_snippet_id(tmp[1])  # Assuming snippetID is the second column
                        fd_filtered.write("|".join(tmp) + "\n")
  
        except IOError:
            print("No or empty file by the name ", fin)
  
        fd_filtered.close()
  
    fd_dropped.close()
  
    return


if __name__ == "__main__":

    import argparse
    import sys
  
    # Takes output path and target concept as input.
    # Assumes labelled snippets are available.
  
    parser = argparse.ArgumentParser()
    parser.add_argument('-p','--path', type =str, required = True, 
                        help = 'path of directory where output lives')
    parser.add_argument('-t','--target', type = str, required = True, 
                        help = 'Label used for the target concept in the output directory')
    parser.add_argument('-a','--assessment_terms', type = str, required = True, 
                        help = 'File with list of terms that indicate assessment')
    parser.add_argument('-o','--other_terms', type = str, required = False, default='file.txt', 
                        help = 'Optional other file with terms that should trigger dropping the snippet')
    parser.add_argument('-sp','--snippet_position', type = int, required = True, 
                        help = 'Position of text in snippet (one-based column number)')
    parser.add_argument('-tp','--title_position', type = int, required = True, 
                        help = 'Position of standard title in snippet (one-based column number)')
  
    args = parser.parse_args()
  
    path   = args.path
    target = args.target
    assess = args.assessment_terms
    other  = args.other_terms
    snippet_column = args.snippet_position - 1
    title_column = args.title_position - 1
  
    # Combine assessment terms and (optional) other terms.
  
    try:
        with open(assess) as fa:
            assessment_terms = fa.read()
  
    except IOError:
        sys.exit("No file by the name " + assess + ". Filter aborted.")
  
    if other == 'file.txt':
        other_terms = ''
    else:
        try:
            with open(other) as fo:
                other_terms = fo.read()
        except IOError:
            sys.exit("No file by the name " + other + ". Filter aborted.")
  
    stoplist = assessment_terms.split("\n") + other_terms.split("\n")
    stoplist = [term for term in stoplist if term]
  
    templated(path, target, stoplist)
