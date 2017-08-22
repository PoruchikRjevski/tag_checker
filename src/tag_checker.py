#!/usr/bin/env python3

#import getopt
import os
import sys
from optparse import OptionParser

import common
from cmd_wrap import runCmd
from logger import outLog
from logger import outErr
from cfg_loader import CfgLoader
from tag_model import TagModel
from git_man import GitMan

def isGitInstalled():
    out = runCmd(common.GIT_VER)
    
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

def main():
    # check options
    optParser = OptionParser()
    setOptions(optParser)

    (opts, args) = optParser.parse_args()

    if opts.quiet:
        common.QUIET = True

    if len(args) != 1:
        outErr(common.TAG_CHECKER, common.E_WA_STR)
        outErr(common.TAG_CHECKER, common.FOR_HELP)
        sys.exit(common.EXIT_WA)

    path = args[0]

    # check is config file was existed
    if not isConfFileExist(path):
       outErr(common.TAG_CHECKER, common.E_CFNE_STR)
       sys.exit(common.EXIT_CFNE)
    
    # check environment
    if not isGitInstalled():
       outErr(common.TAG_CHECKER, common.E_GNT_STR)
       sys.exit(common.EXIT_GNT)

    # work
    tagModel = TagModel()

    cfgLoader = CfgLoader()
    cfgLoader.loadCfg(path, tagModel)

    tagModel.show()

    repoMan = GitMan()
    repoMan.setUpdate(opts.update)
    repoMan.doDirtyJob(tagModel)

    tagModel.show()

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


