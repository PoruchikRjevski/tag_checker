#!/usr/bin/env python3

#import getopt
import os
import sys
from optparse import OptionParser

import common
from cmd_wrap import runCmd
from logger import outMsg
from cfg_loader import CfgLoader

def isGitInstalled():
    out = runCmd("git --version")
    
    if str(out).__contains__("version"):
        return True
    
    return False
    
def isConfFileExist(fileName):
    return os.path.exists(fileName)

def setOptions(parser):
    usage = "usage: %prog [options] path_to_config"

    parser.set_usage(usage)

    parser.add_option("-u", "--update",
                      action="store_true", dest="update",
                      default=False,
                      help="update repo's before checking tags")
    parser.add_option("-q", "--quiet",
                      action="store_true", dest="quiet",
                      default=False,
                      help="don't print status messages to stdout")

def checkOptions(parser):
    if parser.quiet:
        # TODO do it quiet
        print ("quiet")
    if parser.update:
        # TODO do update
        print ("update")
    
def main():
    # check options
    optParser = OptionParser()
    setOptions(optParser)

    (opts, args) = optParser.parse_args()

    if opts.quiet:
        # TODO do it quiet
        print ("quiet")

    if len(args) != 1:
        outMsg(common.CHECKER, common.E_WA_STR)
        outMsg(common.CHECKER, common.FOR_HELP)
        sys.exit(common.EXIT_WA)

    path = args[0]

    # check is config file was existed
    if not isConfFileExist(path):
       outMsg(common.CHECKER, common.E_CFNE_STR)
       sys.exit(common.EXIT_CFNE)
    
    # check environment
    if not isGitInstalled():
       outMsg(common.CHECKER, common.E_GNT_STR)
       sys.exit(common.EXIT_GNT)

    # start work    
    cfgLoader = CfgLoader()
    cfgLoader.loadCfg(path)
    #webCreator = web_creator.WebCreator()

if __name__ == "__main__":
    main()

# check arguments
# check config file exist
# tests 
# 

#config = configparser.ConfigParser()
#config.read('src/config.ini')

#departments = config.sections()

#deps = list()

#for i in departments:
    #repos = config.get(i, 'repos').split(", ") 
    #for j in repos:
        #print (j)
    #deps.append((i, repos))

#for i in deps:
    #for j in i[1]
    #print (i)



#print ('suka')

#print config.get('140', 'repo_lnk', 0)


