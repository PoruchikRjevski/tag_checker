#!/usr/bin/sudo python3
import sys
from optparse import OptionParser

import common_defs as c_d
import global_vars as g_v
import version as v
from git_manager import GitMan
from logger import *
from tag_model import TagModel
from time_profiler.time_checker import *
from config_manager import CfgLoader
from web_generator.web_gen import WebGenerator

def set_options(parser):
    usage = "usage: %prog [options] [args]"

    parser.set_usage(usage)

    parser.add_option("-u", "--update",
                      action="store_true",
                      dest="update",
                      default=False,
                      help="update all")

    parser.add_option("-s", "--show",
                      action="store_true",
                      dest="show",
                      default=False,
                      help="show config, uses with '--dep [dep_name]' or alone")

    parser.add_option("--pref",
                      action="store_true", dest="prefix",
                      default=False,
                      help="set or change department repo's prefix command, uses with arg: [dep_name] [prefix]")

    parser.add_option("-a", "--add",
                      action="store_true", dest="add",
                      default=False,
                      help="add something, uses with --repo, --tr or --dep")
    parser.add_option("-r", "--rem",
                      action="store_true", dest="remove",
                      default=False,
                      help="remove something, uses with --repo, --tr or --dep")

    parser.add_option("--repo",
                      action="store_true", dest="repo",
                      default=False,
                      help="repo command, uses with --add or --rem and args: [dep] [repo_name]")
    parser.add_option("--dep",
                      action="store_true", dest="dep",
                      default=False,
                      help="dep command, uses with --add or --rem and args: dep_name")
    parser.add_option("--tr",
                      action="store_true", dest="translate",
                      default=False,
                      help="translate command, uses with --add or --rem and args: \"orig\" \"trans\"")

    parser.add_option("-l", "--log",
                      action="store_true", dest="log",
                      default=False,
                      help="don't write status messages to log-files")
    parser.add_option("-q", "--quiet",
                      action="store_true", dest="quiet",
                      default=False,
                      help="don't print status messages to stdout")
    parser.add_option("-m", "--mth",
                      action="store_true", dest="multithreading",
                      default=False,
                      help="exec script with using multithreading(may increase speed of esecution on really large "
                           "numbers of cpu cores")
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
        g_v.TIMEOUTS = True
    if opts.timings_out:
        g_v.TIMEOUTS = True


def check_main_opts(opts):
    return ((opts.update or opts.show or opts.prefix)
            or ((opts.add or opts.remove) and (opts.translate or opts.repo or opts.dep)))


def is_add_repo(opts):
    return opts.add and opts.repo


def is_add_translate(opts):
    return opts.add and opts.translate


def is_add_department(opts):
    return opts.add and opts.dep


def is_remove_repo(opts):
    return opts.remove and opts.repo


def is_remove_translate(opts):
    return opts.remove and opts.translate


def is_remove_department(opts):
    return opts.remove and opts.dep


def is_show(opts):
    return opts.show


def is_update(opts):
    return opts.update


def is_change_prefix(opts):
    return opts.prefix


def update(cfg_loader, git_man, tag_model):
    # load config
    cfg_loader.load_config(tag_model)

    # get tags and fill model
    scan_t = start(True)
    git_man.scanning(tag_model)
    stop(scan_t, True)
    g_v.SCAN_TIME = "{:s}".format(get_pass_time(scan_t))
    out_log("Scan time: {:s}".format(g_v.SCAN_TIME))

    # generate web
    web_gen_t = start()
    web_gen = WebGenerator()
    web_gen.generate_web(tag_model)
    stop(web_gen_t)
    if g_v.TIMEOUTS: out_log("web gen time: {:s}".format(get_pass_time(web_gen_t)))


def main():
    ver = "Версия: {:s}.{:s}.{:s}({:s}) {:s}:{:s}".format(v.V_MAJ,
                                                          v.V_MIN,
                                                          str(int(v.V_BUILD) - int(v.LAST)),
                                                          v.V_BUILD,
                                                          v.V_STAT,
                                                          v.HASH)
    # check options
    optParser = OptionParser(version=ver)
    set_options(optParser)

    (opts, args) = optParser.parse_args()

    if check_main_opts(opts):
        setup_options(opts)
    else:
        optParser.print_help()
        sys.exit(c_d.EXIT_WO)

    main_t = start()

    # check platform
    g_v.CUR_PLATFORM = sys.platform

    # init logger
    if g_v.LOGGING:
        init_log()

    # main func
    if g_v.DEBUG: out_log("start work")

    git_man = GitMan()

    # get build version
    git_man.try_get_build_ver()

    # create model
    tag_model = TagModel()

    # load config
    cfg_loader = CfgLoader()

    res = cfg_loader.open_cfg()
    if res is not None:
        sys.exit(res)

    if g_v.DEBUG:
        out_log("-q: " + str(g_v.QUIET))
        out_log("-l: " + str(g_v.LOGGING))
        out_log("-s: " + str(g_v.SUDOER))
        out_log("-m: " + str(g_v.MULTITH))
        out_log("-d: " + str(g_v.DEBUG))
        out_log("-t: " + str(g_v.TIMEOUTS))

    # branch by options
    bad_args = False

    if is_update(opts):
        update(cfg_loader, git_man, tag_model)
    elif is_show(opts):
        if args:
            cfg_loader.show(args[0])
        else:
            cfg_loader.show()
    elif is_add_repo(opts):
        if args and len(args) > 1:
            cfg_loader.add_repo(args[0], args[1:])
        else:
            bad_args = True
    elif is_remove_repo(opts):
        if args and len(args) > 1:
            cfg_loader.rem_repo(args[0], args[1:])
        else:
            bad_args = True
    elif is_add_translate(opts):
        if args and len(args) == 2:
            cfg_loader.add_translate(args[0], args[1])
        else:
            bad_args = True
    elif is_remove_translate(opts):
        if args and len(args) > 0:
            cfg_loader.rem_translate(args)
        else:
            bad_args = True
    elif is_add_department(opts):
        if args and len(args) > 0:
            cfg_loader.add_department(args)
        else:
            bad_args = True
    elif is_remove_department(opts):
        if args and len(args) > 0:
            cfg_loader.rem_department(args)
        else:
            bad_args = True
    elif is_change_prefix(opts):
        if args and len(args) == 2:
            cfg_loader.change_prefix(args[0], args[1])
        else:
            bad_args = True

    if bad_args:
        print(c_d.E_BAD_ARGS)
        out_err(c_d.E_BAD_ARGS)
        sys.exit(c_d.EXIT_WO)

    stop(main_t)
    if g_v.TIMEOUTS: out_log("finish work: {:s}".format(get_pass_time(main_t)))

    if g_v.MULTITH:
        out_deffered_logs()

if __name__ == "__main__":
    main()


