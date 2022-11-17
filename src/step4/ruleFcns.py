import os, sys, glob

# S372-DM|COLON_COLON_COLON_HX_COLON_HX_#DM#_PUNCT_DM-NEURO_HX_HX_DOT|COLON_COLON_COLON_HX_COLON_HX_#DM#_PUNCT_DM-NEURO_HX_HX_DOT|diabetes|995|42562|"Nursing/Other"|3166-07-11 17:49:00 EST|XXXX|DM|1188|206|UK|NULL|colon:COLON:1:82:-124,colon:COLON:1:108:-98,colon:COLON:1:119:-87,history of:HX:746:127:-79,colon:COLON:1:153:-53,history of:HX:746:195:-11,comma:PUNCT:6:230:24,neuropathy:DM-NEURO:1204:250:44,ho:HX:745:262:56,history:HX:747:291:85,period:DOT:2:327:121|SNIPPET: h:   [**3113-9-8**]     Sex:  MService:  C MEDHISTORY OF PRESENT ILLNESS:  This is a 53-year-old white malewith a history of diabetes mellitus type 2, hypertension,with neuropathy who presented with a four day history ofchest pain and diaphoresis.  Of note,

def assignLabel(cevent,trigs_list):
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
    label = cleverRule(cseq,tclass, trigs_list)
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

def cleverRule(cseq,tclass, trigs_list):
    pos = "POSITIVE"
    neg = "NEGATIVE"
    na = "NO_APPLICABLE"
    #trigs = ["NEGEX","HX","HYP","SCREEN","RISK","FAM","PREV"]
    if trigs_list:
        trigs = trigs_list
        na_trigs = ["FAM"]
    else:
        
        trigs = ["NEGEX","HX","HYP","SCREEN","RISK","PREV"]
        na_trigs = ["FAM"]
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
    for tag in trigs:
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

