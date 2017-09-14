#!/usr/bin/sudo python3
import sys
from optparse import OptionParser

import common_defs as c_d
import global_vars as g_v
from cfg_loader import CfgLoader
from git_manager import GitMan
from logger import *
from tag_model import TagModel
from time_profiler.time_checker import *
from web_generator.web_gen import WebGenerator


def set_options(parser):
    usage = "usage: %prog [options] [path_to_config]"

    parser.set_usage(usage)

    parser.add_option("-l", "--log",
                      action="store_true", dest="log",
                      default=False,
                      help="don't write status messages to log-files")
    parser.add_option("-q", "--quiet",
                      action="store_true", dest="quiet",
                      default=False,
                      help="don't print status messages to stdout")
    parser.add_option("-s", "--sudoer",
                      action="store_true", dest="sudoer",
                      default=False,
                      help="exec shell cmd from sudo")
    parser.add_option("-m", "--multith",
                      action="store_true", dest="multithreading",
                      default=False,
                      help="exec script with multithreading")
    parser.add_option("-d", "--debug",
                      action="store_true", dest="debug_out",
                      default=False,
                      help="run debug out")
    parser.add_option("-t", "--timings",
                      action="store_true", dest="timings_out",
                      default=False,
                      help="run timings out if -d - True by default")


def setup_options(opts):
    if opts.quiet:
        g_v.QUIET = True
    if opts.log:
        g_v.LOGGING = True
    if opts.sudoer:
        g_v.SUDOER = True
    if opts.multithreading:
        g_v.MULTITH = True
    if opts.debug_out:
        g_v.DEBUG = True
        g_v.TIM_OUT = True
    if opts.timings_out:
        g_v.TIM_OUT = True


def main():
    # init_cmd_wrapper()

    # check options
    optParser = OptionParser()
    set_options(optParser)

    (opts, args) = optParser.parse_args()

    setup_options(opts)

    main_t = start()

    # check platform
    g_v.CUR_PLATFORM = sys.platform

    # init logger
    init_log()

    if g_v.DEBUG:
        out_log("-q: " + str(g_v.QUIET))
        out_log("-l: " + str(g_v.LOGGING))
        out_log("-s: " + str(g_v.SUDOER))
        out_log("-m: " + str(g_v.MULTITH))
        out_log("-d: " + str(g_v.DEBUG))
        out_log("-t: " + str(g_v.TIM_OUT))

    if len(args) != 1:
        path = ""
    else:
        path = args[0]

    if g_v.DEBUG: out_log("config path: " + path)

    # main func
    if g_v.DEBUG: out_log("start work")

    git_man = GitMan()
    # check environment
    if not git_man.check_git_installed:
        out_err(c_d.E_GNT_STR)
        sys.exit(c_d.EXIT_GNT)

    # check script ver
    git_man.try_get_build_ver()

    # create model
    tag_model = TagModel()

    # load config
    cfg_loader = CfgLoader()
    load_t = start()
    res = cfg_loader.load_config(path, tag_model)
    stop(load_t)
    if g_v.TIM_OUT: out_log("load config time: {:s}".format(get_pass_time(load_t)))

    if res is not None:
        sys.exit(res)

    # get tags and fill model
    scan_t = start()
    git_man.scanning(tag_model)
    stop(scan_t)
    if g_v.TIM_OUT: out_log("scan time: {:s}".format(get_pass_time(scan_t)))

    # generate web
    web_gen_t = start()
    web_gen = WebGenerator()
    web_gen.generate_web(tag_model)
    stop(web_gen_t)
    if g_v.TIM_OUT: out_log("web gen time: {:s}".format(get_pass_time(web_gen_t)))

    stop(main_t)
    if g_v.TIM_OUT: out_log("finish work: {:s}".format(get_pass_time(main_t)))

    if g_v.MULTITH:
        out_deffered_logs()

if __name__ == "__main__":
    main()

