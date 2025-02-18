import glob

# this function loads the different sequences that the annotation tools tag
def loadSeqs(seqFiles,noteDict,termDict):
    #TODO: window argument passed to getTagseq is hardcoded, should probably be parameter.
    sid = 0
    ants = {}

    for name in glob.glob(seqFiles):
        print("LOADING FILE: ",name)
        fin = open(name,"r")
        for line in fin:
            tags = []
            tmp_tags = []
            tag_offests = []
            sem = 0
            line = line.strip()
            tmp = line.split("\t")
            cols = len(tmp)
            nid = tmp[0].strip()
            if nid not in noteDict: 
                print("Note not found:",nid)
                continue
            sid += 1
            mdata = noteDict[nid]
            pid = mdata[1]
            doc_dec = mdata[3]
            tage = mdata[2] #can add to mdatafile
            provider_class = mdata[4] # provider class: added later
            age = str(tage)
            nyear = mdata[0]
            ptage = mdata[5]
            gender = mdata[6]
            opcode = mdata[7]         
            snippet = tmp[cols-1].strip()
            tmpt = tmp[1].split(":")
            tclass = tmpt[0]
            ttid = tmpt[1]
            tmpterm = termDict[ttid]
            tterm = tmpterm[0]
            #try:
            sclass = tmpterm[2]
            #except:
            #    sclass = ""
            tpos = tmp[2]
            if cols < 4: continue
            if sem != 1:
                tmpTestHead = tmp[3].split(":")
                if tmpTestHead[0].islower() and tmpTestHead != "": 
                    htmp = tmp[3].split(":")
                    head = htmp[0]
                    hpos = htmp[1]
                    if cols>5: tmptags = tmp[4:cols-1]
                    else: tmptags = []
                else:
                    head = "UK"
                    hpos = "NULL"
                    tmptags = tmp[4:cols-1]
            tmp_key = "S"+str(sid)+"-"+tclass
            if tmptags == []:
                tmpstr="NONE"
                tagseqs = ["NONE","NONE"]
            else:
                tagterm = gettagterm(tmptags[0],termDict)
                tmpstr = tagterm
                if len(tmptags) > 1:
                    for i in range(1,len(tmptags)):
                        tmp_item = tmptags[i]
                        tagterm = gettagterm(tmp_item,termDict)
                        tmpstr = tmpstr+"^"+tagterm
                tagseqs = getTagseq(tmpstr,"125",tclass)
            #truncseq = "NA"
            fullseq = tagseqs[0]
            sinfo = tmp_key+"|"+fullseq+"|"+tterm+"|"+pid+"|"+nid+"|"+doc_dec+"|"+provider_class+"|"+age+"|"+nyear+"|"+tclass+"|"+sclass + "|"+ttid+"|"+tpos+"|"+head+"|"+hpos+"|"+tmpstr+"|"+ptage+"|"+gender+"|"+opcode+"|"+"SNIPPET: "+snippet
            #print tmp_key+"|"+tterm+"|"+pid+"|"+nid+"|"+doc_dec+"|"+age+"|"+nyear+"|"+tclass+"|"+ttid+"|"+tpos+"|"+head+"|"+hpos+"|"+tmpstr+"|"+snippet
            ants[tmp_key] = sinfo
    print(len(ants),"total annotation for target terms")
    return ants

def gettagterm(tag,dictionary):
    tmp = tag.split(":")
    tterm = dictionary[tmp[1]]
    tmpt = tterm[0].strip()
    if tmpt==":": tterm[0] = "colon"
    if tmpt==".": tterm[0] = "period"
    if tmpt=="/": tterm[0] = "slash"
    if tmpt==",": tterm[0] = "comma"
    taginfo = tterm[0]+":"+tag
    #print ("CLEANED TAG TERM:", tag)
    #print ("TAGINFO:",taginfo)
    return taginfo


def getTagseq(taginfo,window,tclass):
    wmax = int(window)
    wmin = -wmax
    fullseq = ""
    truncseq = ""
    #print (taginfo)
    tmptags = taginfo.split("^")
    #print ("TAGINFO:",taginfo)
    sem = 0
    for tag in tmptags:
        tmp = tag.split(":")
        tmpclass = tmp[1]
        tmppos = int(tmp[4])
        if tmppos < 0:
            if fullseq == "": 
                fullseq = tmpclass
            else: 
                fullseq = fullseq+"_"+tmpclass
#            if abs(tmppos) <= wmax:
#                #print "good",truncseq
#                if truncseq == "":
#                    truncseq = tmpclass
#                else: 
#                    truncseq = truncseq+"_"+tmpclass
        if tmppos > 0 and sem == 1:
            fullseq = fullseq+"_"+tmpclass
#            if tmppos <= wmax:
#                truncseq = truncseq+"_"+tmpclass
        if tmppos > 0 and sem == 0:
            if fullseq == "":
                fullseq = "#"+tclass+"#"+"_"+tmpclass
            else:
                fullseq = fullseq+"_"+"#"+tclass+"#"+"_"+tmpclass
#            if truncseq == "":
#                truncseq = "#"+tclass+"#"+"_"+tmpclass
#            else:
#                truncseq = truncseq+"_"+"#"+tclass+"#"+"_"+tmpclass
            sem = 1
    # if snippet ends with target class and there is no context term after that:
    if tmppos < 0:
        fullseq = fullseq + "_"+"#"+tclass+"#"
    #print ("SNIPPET SEQ:", fullseq)
    #print (tag, taginfo)                                                                                                                   
    return [fullseq]


def getTerminology(dictname):
    termDict = {}
    with open(dictname) as f:
        for line in f:
            tmp = line.split("|")
            tid = tmp[0].strip()
            term = tmp[1].strip()
            tclass = tmp[2].strip()
            try:
               sclass = tmp[3].strip()
            except:
               sclass = ""
            termDict[tid]=[term,tclass,sclass]
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
#PATIENTID|NOTEID|STATION|TIMESTAMP|NOTETYPE|VISIDSID|AGE|GENDER|OPCODE
    noteDict = {}
    with open(fname) as f_in:
        for line in nonblank_lines(f_in):
            tmp = line.split("|")
            #print(tmp)
            #noteDict[tmp[1]]=[tmp[0],tmp[2],tmp[3],tmp[4]]
            noteDict[tmp[1]]=[tmp[0],tmp[2],tmp[3],tmp[4],tmp[5],tmp[6],tmp[7],tmp[8]] # add tmp[5]: provider
    print("Total notes: ",len(noteDict))
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
def getPids(ptList,ptkey):
    lc = 0
    mimicMap = {}
    with open(ptkey) as f_in:
        for line in nonblank_lines(f_in):
            if lc == 0: 
                lc += 1
                continue
            line = line.strip()
            tmp = line.split("|")
#            print tmp
            if hasNumbers(tmp) == False: continue
            id_onco = tmp[0].strip()
            id_S6 = tmp[1].strip()
            mimicMap[id_onco]=id_S6
    f_in.close()
    sample = {}
    if ptList == 0:
        print("Total pts:", len(mimicMap))
        return mimicMap
    with open(ptList) as f_in:
        for line in nonblank_lines(f_in):
            tmp = line.strip()
            id_onco = tmp
            x = mimicMap[id_onco]
            sample[tmp]=x
    print("Total Sampled pts:", len(sample))
    return sample

