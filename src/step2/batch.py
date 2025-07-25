import codecs
from multiprocessing import current_process
from batch import ExitProcess
from note import Note
import queue as qmod

import os


def process_note(
    line, offset_size, snippets, headers, main_terms, context_terms, **kwargs
):
    parts = line.split("\t")
    if len(parts) == 1:
        return
    _id = parts[0]
    text = " ".join(parts[1:])
    note = Note(_id, text, **kwargs)
    note_extraction = note.extract(main_terms, context_terms, offset_size, headers)
    return note_extraction


class Batch:
    def __init__(
        self,
        queue,
        snippet_length,
        snippets,
        headers,
        main_terms,
        context_terms,
        output_folder,
        ngram_contexts,
    ):
        self._queue = queue
        self.snippet_length = snippet_length
        self.snippets = snippets
        self.headers = headers
        self.main_terms = main_terms
        self.context_terms = context_terms
        self.output_folder = output_folder
        self.ngram_contexts = ngram_contexts

        if isinstance(self._queue, str):
            self.notes_file = open(self._queue, "r")

    def next_batch(self):
        if not isinstance(self._queue, str):
            try:
                batch = self._queue.get(True)
                if isinstance(batch, ExitProcess):
                    return None
                return batch
            except qmod.Empty:
                print("qmod empty")
                return []
        else:
            if self.notes_file is None:
                return None
            batch = []
            for line in self.notes_file:
                batch.append(line.strip())
            self.notes_file = None
            return batch

    def process(self):
        if isinstance(self._queue, str):
            pid = 0
        else:
            # TODO This looks like debug code, should it be removed?
            name = current_process().name  # noqa
            pid = os.getpid()
        output_file = codecs.open(
            os.path.join(self.output_folder, "extraction-%d.tsv" % pid),
            "w",
            encoding="utf8",
        )
        discover_file = codecs.open(
            os.path.join(self.output_folder, "discover-%d.tsv" % pid),
            "w",
            encoding="utf8",
        )
        fcontext_left = codecs.open(
            os.path.join(self.output_folder, "context-left-%d.tsv" % pid),
            "w",
            encoding="utf8",
        )
        fcontext_right = codecs.open(
            os.path.join(self.output_folder, "context-right-%d.tsv" % pid),
            "w",
            encoding="utf8",
        )

        while True:
            try:
                batch = self.next_batch()
                if batch is None:
                    assert isinstance(self._queue, qmod.Queue)
                    self._queue.task_done()
                    return
                for line in batch:
                    ext = process_note(
                        line,
                        self.snippet_length,
                        self.snippets,
                        self.headers,  # another case, variable referenced outside class scope (was just "headers")
                        self.main_terms,
                        self.context_terms,
                    )
                    if ext:
                        lefts, rights = ext.dump(
                            output_file,
                            discover_file,
                            self.snippets,
                            self.ngram_contexts,
                        )
                        if self.ngram_contexts:
                            self.ngram_contexts.dump_contexts(  # another case, variable referenced outside class scope (was just "ngram_contexts")
                                lefts, rights, fcontext_left, fcontext_right
                            )
            except Exception as e:
                print(e)
                continue
