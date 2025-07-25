from note_extraction import NoteExtraction
from main_target_hit import MainTargetHit
from step2 import END_TOKEN


class Note:
    def __init__(self, _id, text, **kwargs):
        self._id = _id
        self.text = text
        self.text_lower = text.lower()
        self._include_shorter = kwargs.get("include_shorter", None)
        assert self._include_shorter is not None

    def extract(self, main_terms, context_terms, size_context, headers):
        nt = NoteExtraction(self)
        for term in main_terms:
            offset = 0
            while True:
                hit = self.text_lower.find(term.label, offset)

                continue_loop = False

                if hit == -1:
                    continue_loop = False
                elif term.label == self.text_lower:
                    continue_loop = True
                elif (
                    hit + len(term.label) == len(self.text_lower)
                    and (hit != 0)
                    and (self.text_lower[hit - 1] not in END_TOKEN)
                ):
                    continue_loop = False
                elif (
                    hit + len(term.label) == len(self.text_lower)
                    and (hit != 0)
                    and (self.text_lower[hit - 1] in END_TOKEN)
                ):
                    continue_loop = True
                elif (self.text_lower[hit + len(term.label)] not in END_TOKEN) or (
                    self.text_lower[hit - 1] not in END_TOKEN and hit != 0
                ):
                    continue_loop = False
                else:
                    continue_loop = True

                if not continue_loop:
                    break

                target = MainTargetHit(self, hit, size_context, term, context_terms)
                target.extract_context_terms()
                nt.add_target(target)
                offset = hit + len(term.label)
        if nt.any_targets():
            nt.match_headers(headers)
            if not self._include_shorter:
                nt.only_longest_targets()
            return nt
        return None
