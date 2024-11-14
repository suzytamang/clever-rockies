import os, sys, glob, re
import json

def load_trigs_dict(trigs_path):
    with open(trigs_path, 'r') as f:
        return json.load(f)

def term_offsets(term, string):
    string_lower = string.lower()
    pattern = re.compile(re.escape(term))
    offsets = []
    for match in pattern.finditer(string_lower):
        offsets.append(match.start())
    return offsets


def assignLabel(cevent, neg_trigs, na_trigs):
    sem = 1
    tmp = cevent.split("|")
    #print(tmp)
    sinfo = tmp[0].split("-")
    cid = sinfo[0]
    tclass = sinfo[1].strip()
    cseq = formatSeq(tmp[1],tclass)
    #print("CSEQ:",cseq)
    if cseq == [None,None] : 
        return ["POSITIVE",tclass]
    sentsem= checkSentence(cseq[0],cseq[1])
    if sentsem == 1: 
        return ["POSITIVE",tclass]
    label = cleverRule(cseq,tclass, neg_trigs, na_trigs)
    return label 

def formatSeq(seq,tclass):
    lseq = None
    rseq = None
    if "_#"+tclass+"#_" in seq: 
        tmp = seq.split("_#"+tclass+"#_")
        lseq = tmp[0].split("_")
        rseq = tmp[1].split("_")
    elif "_#"+tclass+"#" in seq: 
        tmp = seq.split("_#"+tclass+"#")
        lseq = tmp[0].split("_")
    elif "#"+tclass+"#_" in seq: 
        tmp = seq.split("#"+tclass+"#_")
        rseq = tmp[1].split("_")
    return [lseq,rseq]

def cleverRule(cseq, tclass, neg_trigs, na_trigs):
    pos = "POSITIVE"
    neg = "NEGATIVE"
    na = "NOT_APP"

    #trigs = ["NEGEX","HX","HYP","SCREEN","RISK","FAM","PREV"]
    # if trigs_list:
    #     trigs = trigs_list
    #     na_trigs = ["FAM"]
    # else:

    #     trigs = ["NEGEX","HX","HYP","SCREEN","RISK","PREV"]
    #     na_trigs = ["FAM"]
    if cseq[0] == None:
        llseq = 0
        pre1 = "DOT"
    else:
        lseq = cseq[0]
        llseq = len(cseq[0])
    if cseq[1] == None:
        lrseq = 0
        post1 = "DOT"
    else:
        rseq = cseq[1]
        lrseq = len(rseq)

    for tag in neg_trigs:
        if llseq > 0:
            pre1 = lseq[llseq-1]
            if pre1 == tag:
                return [neg,tag]
        if lrseq > 0:
            post1 = rseq[0]
            if post1 == tag:
                return [neg,tag]
        if llseq > 2:
            pre2 = lseq[llseq-2]
            if pre2 == tag and pre1 != "DOT":
                return [neg,tag]
                if llseq > 3 and tag != "NEGEX":
                        pre3 = lseq[llseq-3]
                        if pre3 == tag and pre1 != "DOT":
                            return [neg,tag]

    # Determine the NA label
    for tag in na_trigs:
        if llseq > 0: 
            pre1 = lseq[llseq-1]
            if pre1 == tag: 
                return [na,tag] 
        if lrseq > 0:
            post1 = rseq[0]
            if post1 == tag: 
                return [na,tag]
        if llseq > 2:
            pre2 = lseq[llseq-2]
            if pre2 == "CAPACITY":
                print(pre2,lseq)
            if pre2 == tag and pre1 != "DOT": 
                #print(lseq,pre2, pre1)
                return [na,tag]
                if llseq > 3 and tag != "NEGEX":
                        pre3 = lseq[llseq-3]
                        if pre3 == tag and pre1 != "DOT": 
                            return [na,tag] 
        # determine the boundry that was detected and the modifier type

    #PROBABLY POSITIVE...
    # target class
    if tclass == "DM":
        #print "POS: ",tclass, cseq
        return [pos,tclass]
    return [pos,tclass]

def checkSentence(lseq,rseq):
    if lseq == None and rseq == None: 
        return 1
    elif lseq == None:
        if "DOT" == rseq[0]: 
            return 1
    elif rseq == None:
        if "DOT" == lseq[len(lseq)-1]: 
            return 1
    elif "DOT" == lseq[len(lseq)-1] and "DOT" == rseq[0]:
            return 1
    else: return 0
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

