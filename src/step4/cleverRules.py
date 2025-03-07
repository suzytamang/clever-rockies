#TODO:

import os, sys, re
from ruleFcns import *

ppath = sys.argv[1]
fins = ppath + "/linkedAnts.txt"
aclass = sys.argv[2]
neg_trigs_file_path = sys.argv[3]
na_trigs_file_path = sys.argv[4]
print("Processing:", fins)

neg_trigs_dict = load_trigs_dict(neg_trigs_file_path)
na_trigs_dict = load_trigs_dict(na_trigs_file_path)

ptPEvents = {}
ptNEvents = {}
ptEvents = {}
fout_pos = open(ppath+"/allPos_unfiltered.txt","w")
fout_neg = open(ppath+"/allNeg_unfiltered.txt","w")
fout_na = open(ppath+"/allNA_unfiltered.txt","w")
fout_all = open(ppath+"/labeledAnts.txt","w")

print("label|snippetID|term|sta3n|TIUdocumentSID|TIUstandardTitle|visitSID|referenceDateTime|PatientSID|targetClass|targetSubClass|termID|NoteAndSnipOffset|snippet|OpCode",file=fout_pos)
print("label|snippetID|term|sta3n|TIUdocumentSID|TIUstandardTitle|visitSID|referenceDateTime|PatientSID|targetClass|targetSubClass|termID|NoteAndSnipOffset|snippet|OpCode",file=fout_neg)
print("label|snippetID|term|sta3n|TIUdocumentSID|TIUstandardTitle|visitSID|referenceDateTime|PatientSID|targetClass|targetSubClass|termID|NoteAndSnipOffset|snippet|OpCode",file=fout_na)
print("label|snippetID|term|sta3n|TIUdocumentSID|TIUstandardTitle|visitSID|referenceDateTime|PatientSID|targetClass|targetSubClass|termID|NoteAndSnipOffset|snippet|OpCode",file=fout_all)

with open(fins) as f:
    for line in f:
        tmp = line.strip()
        if aclass not in tmp:
            continue

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
        termid = tmpe[11]
        noffset = tmpe[12]
        tags = tmpe[15]
        age = tmpe[16]
        gender = tmpe[17]
        upcode = tmpe[18]
        snippet = tmpe[len(tmpe)-1]

        label = assignLabel(tmp, neg_trigs_dict.get(tclass, []), na_trigs_dict.get(tclass, []))

        # SNIPPET POSTPROCESSING
        # remove the first and last token in the snippet to help readability, only if not the tagged term.
        # NOTE: Cannot use endswith() because last token may include end tokens.

        tokens = snippet.split(' ')
        term_tokens = longseq.split(' ')
        if ((len(tokens) >= 3) &
            (not ((tmpe[-1].lower().startswith(f'snippet: {longseq}')) |
                  (' '.join(tokens[-len(term_tokens):]).lower().startswith(longseq))))):
            tmp = snippet.rsplit(' ', 1)[0]
            tmp = ' '.join(tmp.split()[2:])
            snippet_fc = "SNIPPET: "+tmp
        else:
            snippet_fc = snippet

        # Determine offsets of target terms and main target term that triggered the snippet.
        # Add the snippet offsets to the output field "noteAndSnippetOffset"

        snippet_offsets = term_offsets(longseq, tags, snippet_fc)
        offsets = f'{noffset}:{str(snippet_offsets)}'

        sum_out = label[0]+"|"+cid+"|"+longseq+"|"+tterm+"|"+pid+"|"+nid+"|"+ntype+"|"+time+"|"+year+"|"+tclass+"|"+tsclass+"|"+termid+"|"+offsets+"|"+snippet_fc+"|"+upcode

        long_out = label[0]+"|"+label[1]+"|"+tmp

        tmpE = ""
        if label[0] == "POSITIVE":
            print(sum_out, file=fout_pos)
            print(long_out, file=fout_all)
        if label[0] == "NEGATIVE":
            print(sum_out, file=fout_neg)
            print(long_out, file=fout_all)
        if label[0] == "NOT_APP":
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
