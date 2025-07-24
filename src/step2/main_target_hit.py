from step2 import END_TOKEN


class MainTargetHit:
    def __init__(self, note, offset, size_context, term, context_terms, **kwargs):
        self.note = note
        self.offset = offset
        self.size_context = size_context
        self.term = term
        self.lsnip, self.rsnip = self.extract_target_snips()
        self.context_terms = context_terms
        self.context_hits = []
        self.top_offset = self.offset + len(self.term.label)
        self.header = None
        self._include_shorter = kwargs.get("include_shorter", None)
        assert self._include_shorter is not None

    def dump(self, i, out_extraction, out_discover, snippets):
        header_str = ""
        if self.header:
            header_str = "%s:%s" % (self.header[1], self.header[0])
        line = [
            self.note._id,
            "%s:%s" % (self.term._class, self.term._id),
            str(self.offset),
            header_str,
        ]
        context_sorted = sorted(self.context_hits, key=lambda x: x[2])
        for offset, term, distance in context_sorted:
            line.append("%s:%s:%d:%s" % (term._class, term._id, offset, distance))
        if snippets:
            line.append(self.note.text[self.linit : self.rend])
        out_extraction.write("\t".join(line) + "\n")
        left_context = self.note.text[self.linit : self.offset + len(self.term.label)]
        rigth_context = self.note.text[self.offset : self.rend]
        out_discover.write("[[ID=%s:%s:L]]\n" % (self.note._id, str(i)))
        out_discover.write(left_context + "\n")
        out_discover.write("[[ID=%s:%s:R]]\n" % (self.note._id, str(i)))
        out_discover.write(rigth_context + "\n")
        # return context without the labels
        left = self.note.text[self.linit : self.offset]
        right = self.note.text[self.offset + len(self.term.label) : self.rend]
        return left, right

    def is_contained_in(self, other):
        return other.offset <= self.offset and other.top_offset >= self.top_offset

    def extract_target_snips(self):
        ltext = len(self.note.text)
        linit = self.offset - self.size_context
        rend = self.offset + len(self.term.label) + self.size_context
        if linit < 0:
            linit = 0
        if rend >= ltext:
            rend = ltext
        self.linit = linit
        self.rend = rend
        l = self.note.text[linit : self.offset]  # noqa: E741
        r = self.note.text[self.offset + len(self.term.label) : rend]
        return l, r

    def add_context(self, term, hit, side):
        if side == 0:  # left
            note_offset = self.offset - (len(self.lsnip) - hit)
        else:  # right
            note_offset = self.offset + hit + len(self.term.label)
        distance = note_offset - self.offset
        self.context_hits.append((note_offset, term, distance))

    def only_longest_context(self):
        longest = []
        for context_a in self.context_hits:
            (note_offset, term, distance) = context_a
            top_offset = note_offset + len(term.label)
            is_longest = True
            for context_b in self.context_hits:
                if context_a == context_b:
                    continue
                if context_b[0] <= note_offset:
                    (note_offset_b, term_b, distance_b) = context_b
                    top_offset_b = note_offset_b + len(term_b.label)
                    if top_offset_b >= top_offset:
                        is_longest = False
                        break
            if is_longest:
                longest.append(context_a)
        self.context_hits = sorted(longest, key=lambda x: x[0])

    def extract_context_terms(self):
        for i, snip in enumerate([self.lsnip, self.rsnip]):
            snip_lower = snip.lower()
            for term in self.context_terms:
                offset = 0
                lt = len(term.label)
                ls = len(snip)

                while True:
                    hit = snip_lower.find(term.label, offset)
                    if hit == -1:
                        break
                    if hit + lt + 1 <= ls:
                        # if hit is PUNCT then do nothing (add it to context), else check both sides of term
                        if term._class != "DOT" and term._class != "PUNCT":
                            if (snip[hit + lt] not in END_TOKEN) or (
                                snip[hit - 1] not in END_TOKEN
                            ):
                                offset = hit + len(term.label)
                                continue
                        if term._class == "DOT":
                            if snip[hit + lt].isdigit() and snip[hit - 1].isdigit():
                                offset = hit + 1
                                continue
                    self.add_context(term, hit, i)
                    offset = hit + len(term.label)
        if not self._include_shorter:
            self.only_longest_context()
