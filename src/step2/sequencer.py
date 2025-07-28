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

from pathlib import Path
import sys
import codecs
import os
from typing import List
from argparse import ArgumentParser, Namespace
from multiprocessing import Pool, JoinableQueue
from common.parameters.sequencer_parameter import SequencerParameters
from step2.batch import Batch
from step2.term import Term
from step2.ngram_context import NGramContext

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


def sequencer_main(sequencer_parameters: SequencerParameters):

    workers = sequencer_parameters["workers"]
    output_folder = sequencer_parameters["output_folder"]
    main_targets = target
    lexicon = sequencer_parameters["lexicon"]
    section_headers = sequencer_parameters["section_headers"]
    right_gram = sequencer_parameters["right_gram"]
    left_gram = sequencer_parameters["left_gram"]
    snippets = sequencer_parameters["snippets"]
    snippet_length = sequencer_parameters["snippet_length"]
    notes_file = sequencer_parameters["notes_file"]
    assert workers is not None
    assert output_folder is not None
    assert main_targets is not None
    assert lexicon is not None
    assert section_headers is not None
    assert right_gram is not None
    assert left_gram is not None
    assert snippet_length is not None
    assert notes_file is not None

    if not output_folder:
        print("Output folder must be provided with -o/--output")
        sys.exit(-1)
    if os.path.exists(output_folder):
        print(("Output folder '%s' already exists" % (output_folder)))
        print("This tool will create an empty folder to save clean data")
        sys.exit(-1)

    os.mkdir(output_folder)
    main_targets_index = set(["MBC", "METS", "BCTRIG"])
    if isinstance(main_targets, List):
        main_targets_index = set([x.strip() for x in main_targets[0].split(",")])

    terms = read_dict(lexicon)
    headers = read_headers(section_headers)

    main_terms = [x for x in terms if x._class in main_targets_index]

    # For target terms in the context to be tagged as well, context terms need to include all terms.
    context_terms = terms

    if len(main_terms) == 0:
        sys.stderr.write("Main targets not found - exiting")
        sys.exit(-1)

    if not snippets and (right_gram > 0 or left_gram > 0):
        sys.stderr.write(
            ("If snippets are disabled context " "ngrams cannot be extracted")
        )
        sys.exit(-1)
    ngram_contexts = None
    if left_gram:
        left_gram = int(left_gram)
    if right_gram:
        right_gram = int(right_gram)

    if snippets and (right_gram > 0 or left_gram > 0):
        ngram_contexts = NGramContext(left_gram, right_gram)

    if workers > 0:
        queue = JoinableQueue(workers)
        batch = Batch(
            queue,
            snippet_length,
            snippets,
            headers,
            main_terms,
            context_terms,
            output_folder,
            ngram_contexts,
        )
        pool = Pool(workers, batch.process)
        batch = []
        with open(notes_file, "r") as file_notes:
            for line in file_notes:
                if len(batch) == 5000:
                    queue.put(batch, True, None)
                    batch = []
                batch.append(line.strip())
            if batch:
                queue.put(batch, True, None)
        for x in range(workers):
            # queue.put(ExitProcess())
            queue.put(None)
        # queue.close()
        pool.close()
        pool.join()
    else:
        batch = Batch(
            notes_file,
            snippet_length,
            snippets,
            headers,
            main_terms,
            context_terms,
            output_folder,
            ngram_contexts,
        )
        batch.process()

    if ngram_contexts:
        ngram_contexts.aggregate(output_folder)


def get_sequencer_parameters() -> Namespace:
    """Get sequencer parameters from args

    Returns:
        _type_: _description_
    """
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
    return args


if __name__ == "__main__":
    args = get_sequencer_parameters()

    target = "ADLB"

    sequencer_parameters = SequencerParameters(
        workers=int(args.workers),
        right_gram=int(args.right_gram),
        left_gram=int(args.left_gram),
        snippet_length=int(args.snippet_length),
        snippets=str(args.snippets) if args.snippets is not None else None,
        main_targets=target,
        lexicon=Path(args.lexicon),
        section_headers=Path(args.section_headers),
        output_folder=Path(args.output_folder),
        notes_file=Path(args.notes_file),
    )

    sequencer_main(sequencer_parameters)
