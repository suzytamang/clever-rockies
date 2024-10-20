import sys

from step3fcn import *

ppath = sys.argv[1]  # project path where the output of step2 lives
dictfile = sys.argv[2]  # terminology file
noteMdata = sys.argv[3]  # note metadata
ptAntfile = sys.argv[4]  # annotation file

termDict = getTerminology(dictfile)  # get terminology

noteMDict = loadVANoteMdata(noteMdata)
print("NOTES:", len(noteMDict))

seqDict = {}

seqFile = ppath + "/extraction*.tsv"
tmpDict = loadSeqs(seqFile, noteMDict, termDict)
seqDict.update(tmpDict)
print("Length of Sequence Dictionary:", len(seqDict))
print("CANDIDATE EVENTS:", str(len(seqDict)))

with open(ptAntfile, "w") as fout:
    for sid in seqDict:
        tmp = seqDict[sid]
        print(tmp, file=fout)