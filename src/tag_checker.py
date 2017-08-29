#!/usr/bin/sudo python3
import os
import sys
from optparse import OptionParser

import common
from cmd_wrap import run_cmd
from logger import out_log, out_err, init_log
from cfg_loader import CfgLoader
from tag_model import TagModel
from git_man import GitMan
from web_gen import WebGenerator
from time_checker import TimeChecker


def is_git_installed():
    out = run_cmd(common.GIT_VER)
    
    if str(out).__contains__("version"):
        return True
    
    return False


def is_conf_file_exist(fileName):
    return os.path.exists(fileName)


def set_options(parser):
    usage = "usage: %prog [options] [path_to_config]"

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
    parser.add_option("-d", "--develop",
                      action="store_true", dest="develop",
                      default=False,
                      help="checkout branch to develop before scan")

    parser.add_option("-s", "--sudoer",
                      action="store_true", dest="sudoer",
                      default=False,
                      help="exec shell cmd from sudo")


def check_options(opts):
    if opts.quiet:
        common.QUIET = True
    if opts.log:
        common.LOGGING = True
    if opts.sudoer:
        common.SUDOER = True


def main():
    # create time checker
    timeCh = TimeChecker()
    timeCh.start()

    # check options
    optParser = OptionParser()
    set_options(optParser)

    (opts, args) = optParser.parse_args()

    check_options(opts)

    # check platform
    common.CUR_PLATFORM = sys.platform

    # init logger
    init_log()

    out_log(common.TAG_CHECKER, "-q: " + str(common.QUIET))
    out_log(common.TAG_CHECKER, "-l: " + str(common.LOGGING))
    out_log(common.TAG_CHECKER, "-s: " + str(common.SUDOER))
    out_log(common.TAG_CHECKER, "-d: " + str(opts.develop))
    out_log(common.TAG_CHECKER, "-u: " + str(opts.update))

    if len(args) != 1:
        path = common.CONFIG_PATH
    else:
        path = args[0]

    out_log(common.TAG_CHECKER, "config path: " + path)

    # check is config file was existed
    if not is_conf_file_exist(path):
       out_err(common.TAG_CHECKER, common.E_CFNE_STR)
       sys.exit(common.EXIT_CFNE)
    
    # check environment
    if not is_git_installed():
       out_err(common.TAG_CHECKER, common.E_GNT_STR)
       sys.exit(common.EXIT_GNT)

    # work
    # create model
    tagModel = TagModel()

    # load config
    cfgLoader = CfgLoader()
    cfgLoader.load_config(path, tagModel)

    # get tags and fill model
    gitMan = GitMan()
    gitMan.set_update_flag(opts.update)
    gitMan.set_ch_develop_flag(opts.develop)
    gitMan.scanning(tagModel)

    # generate web
    webGen = WebGenerator()
    webGen.generate_web(tagModel)

    timeCh.stop()
    out_log(common.TAG_CHECKER, timeCh.passed_time_str())

if __name__ == "__main__":
    main()


