#!/usr/bin python3
import os
import sys
from optparse import OptionParser

import common
from cfg_loader import CfgLoader
from tag_model import TagModel
from git_man import GitMan
from web_gen import WebGenerator

from logger import *
from time_checker import *


def is_conf_file_exist(file_name):
    return os.path.exists(file_name)


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
    time_ch = TimeChecker()
    time_ch.start

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

    # main func
    git_man = GitMan()
    # check environment
    if not git_man.check_git_installed():
        out_err(common.TAG_CHECKER, common.E_GNT_STR)
        sys.exit(common.EXIT_GNT)

    # create model
    tag_model = TagModel()

    # load config
    cfg_loader = CfgLoader()
    cfg_loader.load_config(path, tag_model)

    # get tags and fill model
    git_man.update = opts.update
    git_man.swDevelop = opts.develop
    git_man.scanning(tag_model)

    # generate web
    web_gen = WebGenerator()
    web_gen.generate_web(tag_model)

    time_ch.stop
    out_log(common.TAG_CHECKER, time_ch.passed_time_str)

if __name__ == "__main__":
    main()


