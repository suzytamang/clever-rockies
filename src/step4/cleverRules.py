#TODO: Remove output to screen.

import sys

from ruleFcns import *

ppath = sys.argv[1]
fins = ppath + "/linkedAnts.txt"
aclass = sys.argv[2]
neg_trigs_file_path = sys.argv[3]
na_trigs_file_path = sys.argv[4]
print("Processing:", fins)

neg_trigs_dict = load_trigs_dict(neg_trigs_file_path)
na_trigs_dict = load_trigs_dict(na_trigs_file_path)

fout_pos = open(ppath + "/allPos_unfiltered.txt", "w")
fout_neg = open(ppath + "/allNeg_unfiltered.txt", "w")
fout_na = open(ppath + "/allNA_unfiltered.txt", "w")
fout_all = open(ppath + "/labeledAnts.txt", "w")
trigs = ["NEGEX","HX","HYP","SCREEN","RISK","FAM","PREV"]

header = "label|snippetID|term|sta3n|TIUdocumentSID|TIUstandardTitle|visitSID|referenceDateTime|PatientSID|targetClass|targetSubClass|termID|NoteAndSnipOffset|snippet|OpCode"
print(header, file=fout_pos)
print(header, file=fout_neg)
print(header, file=fout_na)
print(header, file=fout_all)

with open(fins) as f:
    for line in f:
        tmpst = line.strip()
        #print("TEMP",tmp)
        if aclass not in tmpst:
            continue

        tmpe = tmpst.split("|")
        cid = tmpe[0]
        tseq = tmpe[1]
        longseq = tmpe[2]
        Location = tmpe[3]  # Location
        nid = tmpe[4]
        NoteTitle = tmpe[5]  # NoteTitle
        VisitID = tmpe[6]  # VisitID
        DateTime = tmpe[7]  # DateTime
        PatientID = tmpe[8]  # PatientID
        tclass = tmpe[9]
        tsclass = tmpe[10]
        termid = tmpe[11]
        tpos = tmpe[12]
        head = tmpe[13]
        hpos = tmpe[14]
        tmpstr = tmpe[15]
        age = tmpe[16]
        gender = tmpe[17]
        OpCode = tmpe[18]  # Code
        snippet = tmpe[len(tmpe)-1]  # Use the last element as snippet

        # SNIPPET POSTPROCESSING
        tokens = snippet.split(" ")
        if len(tokens) >= 3:
                tmp = snippet.rsplit(' ', 1)[0]
                tmp = ' '.join(tmp.split()[2:])
                snippet = "SNIPPET:"+tmp

        # print(f"tmp {tmp}")

        # add the snippet offset to the output field "noteAndSnippetOffset"
        x = term_offsets(longseq, snippet)
        tpos = tpos+":"+str(x)

        # label = assignLabel(tmpst, trigs)
        # print(f" neg_trigs_dict {neg_trigs_dict.get(tclass, [])}")
        # print(f" na_trigs_dict {na_trigs_dict.get(tclass, [])}")
        label = assignLabel(tmpst, neg_trigs_dict.get(tclass, []), na_trigs_dict.get(tclass, []))

        sum_out = f"{label[0]}|{cid}|{longseq}|{Location}|{nid}|{NoteTitle}|{VisitID}|{DateTime}|{PatientID}|{tclass}|{tsclass}|{termid}|{tpos}|{snippet}|{OpCode}"
        long_out = f"{label[0]}|{label[1]}|{tmp}"

        if label[0] == "POSITIVE":
            print(sum_out, file=fout_pos)
            print(long_out, file=fout_all)
        elif label[0] == "NEGATIVE":
            print(sum_out, file=fout_neg)
            print(long_out, file=fout_all)
        elif label[0] == "NOT_APP":
            print(sum_out, file=fout_na)
            print(long_out, file=fout_all)

    fout_pos.close()
    fout_neg.close()
    fout_na.close()
    fout_all.close()

    print("WROTE POS NEG NA FILES")