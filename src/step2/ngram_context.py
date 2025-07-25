import os
from collections import defaultdict


def extract_context(words, start, end):
    words = [x for x in words if len(x) > 0]
    step = 1
    if start > end:
        # TODO Is this needed, or can it be removed?
        step = -1  # noqa
    context = []
    for i in range(start, end, +1):
        if i > -1 and i < len(words):
            context.append(words[i])
        else:
            break
    context = " ".join(context).lower()
    return context


class NGramContext:
    def __init__(self, left_size, right_size):
        self.left_size = left_size
        self.right_size = right_size

    def dump_contexts(self, lefts, rights, fleft, fright):
        # left and right do not include the target label
        if self.left_size:
            for left in lefts:
                words = left.strip().split(" ")
                words = [x for x in words if len(x) > 0]
                start = len(words)
                lcontext = extract_context(words, start - self.left_size, start)
                fleft.write(lcontext + "\n")
        if self.right_size:
            for right in rights:
                words = right.strip().split(" ")
                words = [x for x in words if len(x) > 0]
                rcontext = extract_context(words, 0, self.right_size)
                fright.write(rcontext + "\n")

    def aggregate(self, output_folder):

        onlyfiles = [
            os.path.join(output_folder, f)
            for f in os.listdir(output_folder)
            if os.path.isfile(os.path.join(output_folder, f))
        ]
        count_left = defaultdict(lambda: 0)
        count_right = defaultdict(lambda: 0)
        for f in onlyfiles:
            d = None
            if "context-left" in f:
                d = count_left
            elif "context-right" in f:
                d = count_right
            else:
                continue
            with open(f) as fin:
                for line in fin:
                    d[line.strip()] += 1
        self.dump_stats(
            os.path.join(output_folder, "context-left-stats.tsv"), count_left
        )
        self.dump_stats(
            os.path.join(output_folder, "context-right-stats.tsv"), count_right
        )

    def dump_stats(self, fname, counts):
        total = float(sum(counts.values()))
        accumulative = [
            (f, c, (float(c) / total) * 100) for (f, c) in list(counts.items())
        ]
        sorted_acc = sorted(accumulative, key=lambda x: x[1], reverse=True)
        with open(fname, "w") as fout:
            fout.write(
                "\n".join(["%s\t%d\t%.4f" % (x[0], x[1], x[2]) for x in sorted_acc])
            )
