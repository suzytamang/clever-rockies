import json
import re


def load_trigs_dict(trigs_path):
    with open(trigs_path, 'r') as f:
        return json.load(f)

def term_offsets(term, string):
    string_lower = string.lower()
    pattern = re.compile(re.escape(term.lower()))
    offsets = [match.start() for match in pattern.finditer(string_lower)]
    return offsets

def assignLabel(cevent, neg_trigs, na_trigs):
    tmp = cevent.split("|")
    sinfo = tmp[0].split("-")
    tclass = sinfo[1].strip()
    cseq = formatSeq(tmp[1], tclass)

    if cseq == [None, None]:
        return ["POSITIVE", tclass]

    sentsem = checkSentence(cseq[0], cseq[1])
    if sentsem == 1:
        return ["POSITIVE", tclass]

    label = cleverRule(cseq, tclass, neg_trigs, na_trigs)
    return label

def formatSeq(seq, tclass):
    lseq = None
    rseq = None
    if f"_#{tclass}#_" in seq:
        tmp = seq.split(f"_#{tclass}#_")
        lseq = tmp[0].split("_")
        rseq = tmp[1].split("_")
    elif f"_#{tclass}#" in seq:
        tmp = seq.split(f"_#{tclass}#")
        lseq = tmp[0].split("_")
    elif f"#{tclass}#_" in seq:
        tmp = seq.split(f"#{tclass}#_")
        rseq = tmp[1].split("_")
    return [lseq, rseq]

def cleverRule(cseq, tclass, neg_trigs, na_trigs):
    pos = "POSITIVE"
    neg = "NEGATIVE"
    na = "NOT_APP"

    if tclass == "DM":
        #print "POS: ",tclass, cseq
        return [pos,tclass]

    if cseq[0] is None:
        llseq = 0
        pre1 = "DOT"
    else:
        lseq = cseq[0]
        llseq = len(cseq[0])
    if cseq[1] is None:
        lrseq = 0
        post1 = "DOT"
    else:
        rseq = cseq[1]
        lrseq = len(rseq)

    # Determine the NA label
    for tag in na_trigs:
        if llseq > 0 and lseq[llseq-1] == tag:
            return [na, tag]
        if lrseq > 0 and rseq[0] == tag:
            return [na, tag]
        if llseq > 2 and lseq[llseq-2] == tag and lseq[llseq-1] != "DOT":
            return [na, tag]

    # Determine the negative label
    for tag in neg_trigs:
        if llseq > 0 and lseq[llseq-1] == tag:
            return [neg, tag]
        if lrseq > 0 and rseq[0] == tag:
            return [neg, tag]
        if llseq > 2 and lseq[llseq-2] == tag and lseq[llseq-1] != "DOT":
            return [neg, tag]

    return [pos, tclass]

def checkSentence(lseq, rseq):
    if lseq is None and rseq is None:
        return 1
    elif lseq is None:
        return 1 if "DOT" == rseq[0] else 0
    elif rseq is None:
        return 1 if "DOT" == lseq[-1] else 0
    elif "DOT" == lseq[-1] and "DOT" == rseq[0]:
        return 1
    else:
        return 0

def getTerminology(dictname):
    termDict = {}
    print(dictname)
    with open(dictname) as f:
        for line in f:
            tmp = line.split("|")
            tid = tmp[0].strip()
            term = tmp[1].strip()
            tclass = tmp[2].strip()
            termDict[tid]=[term,tclass]
    return termDict

