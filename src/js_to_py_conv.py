import os

# !/usr/bin/env python3
import os
import sys
from optparse import OptionParser

def setOptions(parser):
    usage = "usage: %prog 'path to *.js' "

    parser.set_usage(usage)

def doPy(file):
    f = open(file, 'r')
    outF = open(file.split('.')[:-1][0] + ".py", 'w')

    if not f or not outF:
        closeFiles(f, outF)

        return 1

    beforeLines = f.readlines()

    outF.write("SCRIPTS = ")
    for line in beforeLines:
        outF.write(" \\")
        outF.write("\n")
        outF.write("\"")
        nline = line.replace("\"", "\\\"")
        nline = nline.replace("}", "}}")
        nline = nline.replace("{", "{{")
        nline = nline.replace("\n", "")
        if "pridurok" in nline:
            nline = nline.replace("pridurok", " %s")
        outF.write(nline)
        outF.write("\\n\\r")
        outF.write("\"")
        outF.flush()

    closeFiles(f, outF)

def closeFiles(inF, outF):
    if inF:
        inF.flush()
        inF.close()
    if outF:
        outF.flush()
        outF.close()

def main():
    # check options
    optParser = OptionParser()
    setOptions(optParser)

    (_, args) = optParser.parse_args()

    if len(args) != 1:
        sys.exit(1)

    path = args[0]

    if os.path.exists(path):
        if doPy(path):
            sys.exit(0)
        else:
            sys.exit(1)

if __name__ == "__main__":
    main()


