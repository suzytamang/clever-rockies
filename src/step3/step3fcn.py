import glob

# this function loads the different sequences that the annotation tools tag

def loadSeqs(seqFiles, noteDict, termDict):
    sid = 0
    ants = {}
    for name in glob.glob(seqFiles):
        print("LOADING FILE: ", name)
        with open(name, "r") as fin:
            for line in fin:
                tmp = line.strip().split("\t")
                if len(tmp) < 4:
                    continue

                nid = tmp[0].strip()
                if nid not in noteDict:
                    print("Note not found:", nid)
                    continue

                sid += 1
                mdata = noteDict[nid]

                tmpt = tmp[1].split(":")
                tclass = tmpt[0]
                ttid = tmpt[1]
                tmpterm = termDict[ttid]
                tterm = tmpterm[0]
                sclass = tmpterm[2] if len(tmpterm) > 2 else ""

                tpos = tmp[2]
                head = "UK"
                hpos = "NULL"

                if len(tmp) > 4:
                    htmp = tmp[3].split(":")
                    if htmp[0].islower() and htmp[0] != "":
                        head = htmp[0]
                        hpos = htmp[1]
                        tmptags = tmp[4:-1] if len(tmp) > 5 else []
                    else:
                        tmptags = tmp[4:-1]
                else:
                    tmptags = []

                snippet = tmp[-1].strip()

                tmp_key = f"S{sid}-{tclass}"

                if not tmptags:
                    tmpstr = "NONE"
                    tagseqs = ["NONE", "NONE"]
                else:
                    tagterm = gettagterm(tmptags[0], termDict)
                    tmpstr = tagterm
                    for i in range(1, len(tmptags)):
                        tmp_item = tmptags[i]
                        tagterm = gettagterm(tmp_item, termDict)
                        tmpstr = f"{tmpstr}^{tagterm}"
                    tagseqs = getTagseq(tmpstr, "125", tclass)

                fullseq = tagseqs[0]
                sinfo = f"{tmp_key}|{fullseq}|{tterm}|{mdata['Location']}|{nid}|{mdata['NoteTitle']}|{mdata['VisitID']}|{mdata['DateTime']}|{mdata['PatientID']}|{tclass}|{sclass}|{ttid}|{tpos}|{head}|{hpos}|{tmpstr}|{mdata['Age']}|{mdata['Gender']}|{mdata['Code']}|SNIPPET: {snippet}"
                ants[tmp_key] = sinfo

    print(len(ants), "total annotations for target terms")
    return ants

def gettagterm(tag, dictionary):
    tmp = tag.split(":")
    tterm = dictionary[tmp[1]]
    tmpt = tterm[0].strip()
    if tmpt == ":": tterm[0] = "colon"
    if tmpt == ".": tterm[0] = "period"
    if tmpt == "/": tterm[0] = "slash"
    if tmpt == ",": tterm[0] = "comma"
    taginfo = f"{tterm[0]}:{tag}"
    return taginfo


def getTagseq(taginfo, window, tclass):
    wmax = int(window)
    fullseq = ""
    tmptags = taginfo.split("^")
    sem = 0
    for tag in tmptags:
        tmp = tag.split(":")
        tmpclass = tmp[1]
        tmppos = int(tmp[4])
        if tmppos < 0:
            fullseq = f"{fullseq}_{tmpclass}" if fullseq else tmpclass
        elif tmppos > 0 and sem == 1:
            fullseq = f"{fullseq}_{tmpclass}"
        elif tmppos > 0 and sem == 0:
            fullseq = f"{fullseq}_#{tclass}#_{tmpclass}" if fullseq else f"#{tclass}#_{tmpclass}"
            sem = 1
    if tmppos < 0:
        fullseq = f"{fullseq}_#{tclass}#"
    return [fullseq]


def getTerminology(dictname):
    termDict = {}
    with open(dictname) as f:
        for line in f:
            tmp = line.strip().split("|")
            if len(tmp) > 2:  # Ensure we have at least 3 fields
                tid = tmp[0].strip()
                term = tmp[1].strip()
                tclass = tmp[2].strip()
                sclass = tmp[3].strip() if len(tmp) > 3 else ""
                termDict[tid] = [term, tclass, sclass]
    return termDict

#loads all note metadata for patient subset
def loadSelectNoteMetadata(ptList):
# patient_id|note_id|doc_description|age_at_note_DATE_in_days|note_year        
    fname = "/data3/stride6/tp_annotator_notes.txt"
    noteDict = {}
    fout_notemeta = open("/data3/mbc/notemetadata.txt","w")
    with open(fname) as f_in:
        for line in nonblank_lines(f_in):
            tmp = line.split("|")
            pid = tmp[0].strip()
            nid = tmp[1].strip()
            if pid in ptList:
                #print(line.strip(), file=fout_notemeta)
#                with open("/data3/S6/corpus/notes/"+nid) as onconote:
#                    fout = open("/data3/oncoshare/oncocorpus/"+nid,"w")
#                print >> fout, onconote
                #fout.close()
                #noteDict[tmp[1]]=[tmp[0],tmp[2],tmp[3],tmp[4]]
                noteDict[tmp[1]]=[tmp[0],tmp[2],tmp[3],tmp[4],tmp[5]] # add tmp[5]:provider
    print("Total notes: ",len(noteDict))
    return noteDict

def loadVANoteMdata(fname):
    noteDict = {}
    with open(fname) as f_in:
        for line in nonblank_lines(f_in):
            tmp = line.strip().split("|")
            if len(tmp) >= 9:  # Ensure we have at least 9 fields
                noteDict[tmp[1]] = {
                    'PatientID': tmp[0],
                    'Location': tmp[2],
                    'DateTime': tmp[3],
                    'NoteTitle': tmp[4],
                    'VisitID': tmp[5],
                    'Age': tmp[6],
                    'Gender': tmp[7],
                    'Code': tmp[8]
                }
    print("Total notes: ", len(noteDict))
    return noteDict

def nonblank_lines(f):
    for l in f:
        line = l.rstrip()
        if line:
            yield line

def hasNumbers(inputString):
    return any(char.isdigit() for char in inputString)

# pt list is a selected group of patients
# set ptList =0 to return all patients
def getPids(ptList, ptkey):
    mimicMap = {}
    with open(ptkey) as f_in:
        next(f_in)  # Skip header
        for line in nonblank_lines(f_in):
            tmp = line.strip().split("|")
            if hasNumbers(tmp[0]):
                id_onco = tmp[0].strip()
                id_S6 = tmp[1].strip()
                mimicMap[id_onco] = id_S6

    if ptList == 0:
        print("Total pts:", len(mimicMap))
        return mimicMap

    sample = {}
    with open(ptList) as f_in:
        for line in nonblank_lines(f_in):
            id_onco = line.strip()
            if id_onco in mimicMap:
                sample[id_onco] = mimicMap[id_onco]

    print("Total Sampled pts:", len(sample))
    return sample

