#TODO: Remove output to screen.

import os, sys, re
from ruleFcns import *

ppath = sys.argv[1]
fins = ppath + "/linkedAnts.txt"
aclass = sys.argv[2]
print("Processing:", fins)

ptPEvents = {}
ptNEvents = {}
ptEvents = {}
fout_pos = open(ppath+"/allPos.txt","w")
fout_neg = open(ppath+"/allNeg.txt","w")
fout_na = open(ppath+"/allNA.txt","w")
fout_all = open(ppath+"/labeledAnts.txt","w")
trigs = ["NEGEX","HX","HYP","SCREEN","RISK","FAM","PREV"]


print("label|snippetID|term|sta3n|TIUdocumentSID|TIUstandardTitle|visitSID|referenceDateTime|PatientSID|targetClass|targetSubClass|termID|NoteAndSnipOffset|snippet|OpCode",file=fout_pos)
print("label|snippetID|term|sta3n|TIUdocumentSID|TIUstandardTitle|visitSID|referenceDateTime|PatientSID|targetClass|targetSubClass|termID|NoteAndSnipOffset|snippet|OpCode",file=fout_neg)
print("label|snippetID|term|sta3n|TIUdocumentSID|TIUstandardTitle|visitSID|referenceDateTime|PatientSID|targetClass|targetSubClass|termID|NoteAndSnipOffset|snippet|OpCode",file=fout_na)
print("label|snippetID|term|sta3n|TIUdocumentSID|TIUstandardTitle|visitSID|referenceDateTime|PatientSID|targetClass|targetSubClass|termID|NoteAndSnipOffset|snippet|OpCode",file=fout_all)

with open(fins) as f:
    for line in f:
        tmp = line.strip()
        #print("TEMP",tmp)
        if aclass not in tmp:
            continue
        label = assignLabel(tmp, trigs)
        tmpe = tmp.split("|")
        cid = tmpe[0]
        tseq = tmpe[1]
        longseq = tmpe[2]
        tterm = tmpe[3]
        pid = tmpe[4]
        nid = tmpe[5]
        ntype = tmpe[6]
        time = tmpe[7]
        year = tmpe[8]
        tclass = tmpe[9]
        tsclass = tmpe[10]
        noffset = tmpe[11]
        termid = tmpe[12]
        tags = tmpe[15]
        age = tmpe[16]
        gender = tmpe[17]
        upcode = tmpe[18]
        snippet = tmpe[len(tmpe)-1]
        # SNIPPET POSTPROCESSING
        # remove the first and last token in the snippet to help readability"
        tokens = snippet.split(" ")
        if len(tokens) >= 3:
                tmp = snippet.rsplit(' ', 1)[0]
                tmp = ' '.join(tmp.split()[2:])
                snippet = "SNIPPET:"+tmp
        # add the snippet offset to the output field "noteAndSnippetOffset"
        x = term_offsets(longseq, snippet)
        termid = termid+":"+str(x)
        #print(termid, longseq, snippet)
        #print(termid,longseq,snippet)
                
        sum_out = label[0]+"|"+cid+"|"+longseq+"|"+tterm+"|"+pid+"|"+nid+"|"+ntype+"|"+time+"|"+year+"|"+tclass+"|"+tsclass+"|"+noffset+"|"+termid+"|"+snippet+"|"+upcode

        long_out =  label[0]+"|"+label[1]+"|"+tmp

        tmpE = ""
        if label[0] == "POSITIVE":
                print(sum_out, file=fout_pos)
                print(long_out, file=fout_all)
        if label[0] == "NEGATIVE":
                print(sum_out, file=fout_neg)
                print(long_out, file=fout_all)
        if label[0] == "NO_APPLICABLE":
                print(sum_out, file=fout_na)
                print(long_out, file=fout_all)
fout_pos.close()
fout_neg.close()
print("WROTE POS NEG NA FILES")

#print len(ptPEvents)
#print len(ptNEvents)
#print len(ptEvents)
#for pid in ptPEvents:
#        fpos = open(opath+"pt"+pid+"_pos.txt","w")
#        te = ptPEvents[pid]
#        for i in range(len(te)):
#                tevent = te[i]
#                print >> fpos,tevent
#                print pid,tevent
#        fpos.close()

#for pid in ptNEvents:
#        fneg = open(opath+"pt"+pid+"_neg.txt","w")
#        te = ptNEvents[pid]
#        for i in range(len(te)):
#                tevent = te[i] 
#                print >> fneg,tevent
#                print pid,tevent
#        fneg.close()

#for pid in ptEvents:
#        fcron = open(opath+"pt"+pid+"_cronology.txt","w")
#        te = ptEvents[pid]
#        for i in range(len(te)):
#                tevent = te[i] 
#                print >> fcron,tevent
#                print pid,tevent
#        fcron.close()

#s =assignMBCLabel(snippet)
#print s

#s = assignMBCLabel(s2)
