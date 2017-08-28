#!/usr/bin/env python3
import os
import sys
from optparse import OptionParser

import common
from cmd_wrap import runCmd
from logger import out_log
from logger import out_err
from logger import init_log
from cfg_loader import CfgLoader
from tag_model import TagModel
from git_man import GitMan
from web_gen import WebGenerator
from time_checker import TimeChecker

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
    parser.add_option("-l", "--log",
                      action="store_true", dest="log",
                      default=False,
                      help="don't write status messages to log-files")
    parser.add_option("-q", "--quiet",
                      action="store_true", dest="quiet",
                      default=False,
                      help="don't print status messages to stdout")

def main():
    # create time checker
    timeCh = TimeChecker()

    timeCh.start()

    # check options
    optParser = OptionParser()
    setOptions(optParser)

    (opts, args) = optParser.parse_args()

    if opts.quiet:
        common.QUIET = True

    if opts.log:
        common.LOGGING = True

    # check platform
    common.CUR_PLATFORM = sys.platform

    # init logger
    init_log()

    print(common.CUR_PATH)

    if len(args) != 1:
        out_err(common.TAG_CHECKER, common.E_WA_STR)
        out_err(common.TAG_CHECKER, common.FOR_HELP)
        sys.exit(common.EXIT_WA)

    path = args[0]

    # check is config file was existed
    if not isConfFileExist(path):
       out_err(common.TAG_CHECKER, common.E_CFNE_STR)
       sys.exit(common.EXIT_CFNE)
    
    # check environment
    if not isGitInstalled():
       out_err(common.TAG_CHECKER, common.E_GNT_STR)
       sys.exit(common.EXIT_GNT)

    # work
    # create model
    tagModel = TagModel()

    # load config
    cfgLoader = CfgLoader()
    cfgLoader.loadCfg(path, tagModel)

    # get tags and fill model
    repoMan = GitMan()
    repoMan.setUpdate(opts.update)
    repoMan.doDirtyJob(tagModel)

    # generate web
    webGen = WebGenerator()
    webGen.generateWeb(tagModel)

    timeCh.stop()
    out_log(common.TAG_CHECKER, timeCh.howMuchStr())

if __name__ == "__main__":
    main()


