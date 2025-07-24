import re


class NoteExtraction:
    def __init__(self, note):
        self.note = note
        self.targets = []

    def only_longest_targets(self):
        longest = []
        for target_a in self.targets:
            is_longest = True
            for target_b in self.targets:
                if target_a == target_b:
                    continue
                if target_a.is_contained_in(target_b):
                    is_longest = False
                    break
            if is_longest:
                longest.append(target_a)
        self.targets = sorted(longest, key=lambda x: x.offset)

    def add_target(self, target):
        self.targets.append(target)

    def any_targets(self):
        return len(self.targets) > 0

    def match_headers(self, headers):
        max_target = max([x.offset for x in self.targets])
        header_text_space = self.note.text[:max_target]
        header_index = list()
        for header in headers:
            index = [m.start() for m in re.finditer(header + ":", header_text_space)]
            for i in index:
                header_index.append((i, header))
        header_index = sorted(header_index, key=lambda x: x[0])
        for target in self.targets:
            for i, header in header_index:
                if i > target.offset:
                    break
                else:
                    target.header = (i, header)

    def dump(self, out_extraction, out_discover, snippets, ngram_contexts):
        sorted_targets = sorted(self.targets, key=lambda x: x.offset)
        lefts, rights = [], []
        for i, target in enumerate(sorted_targets):
            left, right = target.dump(i, out_extraction, out_discover, snippets)
            lefts.append(left)
            rights.append(right)
        return lefts, rights
