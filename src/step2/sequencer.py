"""
extractor.py uses CLEVER's terminology and note header file to generate generate concept
    sequences and other annotated textual information for expressing CLEVER rules for
    automatically labeling events documented in clinical text.

input: file paths to the tagging lexicon with word class mappings, the list of clinical
    note headers, target classes for event extraction, maximum snippet length,
    directory path to the clinical corpus, number of workers, output folder and size
    of n-gram context for n-gram feature generation

output: for target mentions detected using a maximum string length, right truncated partial
    string matching, CLEVER's output files include right and left n-gram features
    (context_left.txt, context_right.txt), candidate event snippets that can be used for
    additional processing steps such as SNOMED-CT concept extraction (discover.txt), and
    CLEVER's extraction files (extraction.txt).

*** it is important to note that only the extraction.txt file is required to develop a
    rule based extractor.  Additional textual features are provided in the extraction.txt
    file, and other extractor.py output; however, they are inteded to be used in the
    development of statistical extractors trained on a small portion of development
    data that is labeled by CLEVER during rule execution
"""

import pdb  # noqa: F401
import sys
import codecs
import os
import time  # noqa: F401
import warnings  # noqa: F401
from argparse import ArgumentParser
from multiprocessing import Pool, JoinableQueue
import importlib  # noqa: F401
from batch import Batch
from term import Term
from ngram_context import NGramContext

# from resource import getrusage, RUSAGE_SELF


def read_headers(f):
    header_list = set()
    with codecs.open(f, "r", "utf-8") as f:
        for line in f:
            header = line.strip().lower()
            if header:
                header_list.add(header)
        return header_list


def read_dict(f):
    terms = []
    with codecs.open(f, "r", "utf-8") as f:
        for line in f:
            # print(line)
            _id, label, _class, _subclass = line.strip().split("|")
            # if ("_" in _class) or ("_" in _subclass):
            # raise Exception("Underline in "+_class+":underline is not allowed in target class.")
            term = Term(_id, label, _class, _subclass)
            terms.append(term)
        return terms


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument(
        "-o",
        "--output",
        dest="output_folder",
        default=None,
        help="output folder",
        metavar="FILE",
    )
    parser.add_argument(
        "-n",
        "--notes",
        dest="notes_file",
        default=None,
        help="Notes file",
        metavar="FILE",
    )
    parser.add_argument(
        "-l",
        "--lexicon",
        dest="lexicon",
        default="mbc-dic.txt",
        help="read word classes from FILE",
        metavar="FILE",
    )
    parser.add_argument("-w", "--workers", dest="workers", default=2, metavar="N")
    parser.add_argument(
        "-s",
        "--section-headers",
        dest="section_headers",
        default="headers.txt",
        help="read headers from FILE",
        metavar="FILE",
    )
    parser.add_argument(
        "-t",
        "--main-targets",
        dest="main_targets",
        action="append",
        default=[],
        help=(
            "the word classes to use as a main target " "(can be used multiple times)"
        ),
        metavar="TARGET",
    )
    parser.add_argument(
        "-ln", "--snippet-length", dest="snippet_length", type=int, default=150
    )
    parser.add_argument("--snippets", dest="snippets", action="store_true")
    parser.add_argument(
        "--shorter-too", dest="include_shorter", action="store_true", default=False
    )
    parser.add_argument("--no-snippets", dest="snippets", action="store_false")
    parser.add_argument("--left-gram-context", dest="left_gram", default=3)
    parser.add_argument("--right-gram-context", dest="right_gram", default=2)
    args = parser.parse_args()
    args.workers = int(args.workers)

    if not args.output_folder:
        print("Output folder must be provided with -o/--output")
        sys.exit(-1)
    if os.path.exists(args.output_folder):
        print(("Output folder '%s' already exists" % (args.output_folder)))
        print("This tool will create an empty folder to save clean data")
        sys.exit(-1)

    os.mkdir(args.output_folder)
    main_targets_index = set(["MBC", "METS", "BCTRIG"])
    if len(args.main_targets) > 0:
        main_targets_index = set([x.strip() for x in args.main_targets[0].split(",")])

    terms = read_dict(args.lexicon)
    headers = read_headers(args.section_headers)

    main_terms = [x for x in terms if x._class in main_targets_index]

    # For target terms in the context to be tagged as well, context terms need to include all terms.
    context_terms = terms

    if len(main_terms) == 0:
        sys.stderr.write("Main targets not found - exiting")
        sys.exit(-1)

    if not args.snippets and (args.right_gram > 0 or args.left_gram > 0):
        sys.stderr.write(
            ("If snippets are disabled context " "ngrams cannot be extracted")
        )
        sys.exit(-1)
    ngram_contexts = None
    if args.left_gram:
        args.left_gram = int(args.left_gram)
    if args.right_gram:
        args.right_gram = int(args.right_gram)

    if args.snippets and (args.right_gram > 0 or args.left_gram > 0):
        ngram_contexts = NGramContext(args.left_gram, args.right_gram)

    if args.workers > 0:
        queue = JoinableQueue(args.workers)
        batch = Batch(
            queue,
            args.snippet_length,
            args.snippets,
            headers,
            main_terms,
            context_terms,
            args.output_folder,
            ngram_contexts,
        )
        pool = Pool(args.workers, batch.process)
        batch = []
        with open(args.notes_file, "r") as file_notes:
            for line in file_notes:
                if len(batch) == 5000:
                    queue.put(batch, True, None)
                    batch = []
                batch.append(line.strip())
            if batch:
                queue.put(batch, True, None)
        for x in range(args.workers):
            # queue.put(ExitProcess())
            queue.put(None)
        # queue.close()
        pool.close()
        pool.join()
    else:
        batch = Batch(
            args.notes_file,
            args.snippet_length,
            args.snippets,
            headers,
            main_terms,
            context_terms,
            args.output_folder,
            ngram_contexts,
        )
        batch.process()

    if ngram_contexts:
        ngram_contexts.aggregate(args.output_folder)
