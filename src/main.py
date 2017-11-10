#!/usr/bin/sudo python3
import os
import sys
from optparse import OptionParser
import logging
import datetime


import common_defs as c_d
import global_vars as g_v
import version as v
from git_manager import GitMan
from tag_model import TagModel
from time_profiler.time_checker import *
from config_manager import CfgLoader
from web_generator.web_gen import WebGenerator
from cmd_executor.cmd_executor import *

def set_options(parser):
    usage = "usage: %prog [options] [args]"

    parser.set_usage(usage)

    parser.add_option("-u", "--update",
                      action="store_true",
                      dest="update",
                      default=False,
                      help="update by /etc/tag_checker/update.ini")

    parser.add_option("-f", "--fully",
                      action="store_true",
                      dest="fully",
                      default=False,
                      help="uses only with --update, means that script will be update info about all repos in /etc/tag_checker/config.ini")

    parser.add_option("--related",
                      action="store_true",
                      dest="related",
                      default=False,
                      help="uses only with --update and --repo, add repo(if it exist in config) to /etc/tag_checker/update.ini")

    parser.add_option("--setuphooks",
                      action="store_true",
                      dest="setuphooks",
                      default=False,
                      help="uses alone for setup git hooks to all repos in /etc/tag_checker/config.ini")

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
    parser.add_option("-v", "--verbose",
                      action="store_true", dest="verbose",
                      default=False,
                      help="print status messages to stdout")
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
    if opts.verbose:
        g_v.VERBOSE = True
    if opts.log:
        g_v.LOGGING = True
    if opts.multithreading:
        g_v.MULTITH = True
    if opts.debug_out:
        g_v.DEBUG = True
        g_v.TIMEOUTS = True
    if opts.timings_out:
        g_v.TIMEOUTS = True


def check_main_opts(opts):
    return ((opts.update or opts.show or opts.prefix)
            or (opts.update and opts.fully)
            or (opts.update and opts.related and opts.repo)
            or opts.setuphooks
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


def is_full_update(opts):
    return opts.fully and opts.update


def is_related_update(opts):
    return opts.update and opts.related and opts.repo


def is_change_prefix(opts):
    return opts.prefix


def is_setup_hooks(opts):
    return opts.setuphooks


def update(cfg_loader, git_man, tag_model):
    # load config
    if cfg_loader.load_config(tag_model):
        # get tags and fill model
        scan_t = start(True)
        # git_man.scanning(tag_model)
        stop(scan_t, True)
        g_v.SCAN_TIME = "{:s}".format(get_pass_time(scan_t))
        logging.warning("Scan time: {:s}".format(g_v.SCAN_TIME))

        # generate web
        # web_gen_t = start()
        # web_gen = WebGenerator()
        # web_gen.generate_web(tag_model, cfg_loader.partly_update)
        # stop(web_gen_t)
        # if g_v.TIMEOUTS: l.warning("web gen time: {:s}".format(get_pass_time(web_gen_t)))


def setup_hooks(cfg_loader, tag_model):
    cfg_loader.load_config(tag_model)

    cfg_loader.setup_hooks(tag_model)


def init_logging(name, debug):
    path = ""

    if g_v.CUR_PLATFORM == c_d.LINUX_P:
        path = c_d.LIN_LOG_P_DEF
    elif g_v.CUR_PLATFORM == c_d.WINDOWS_P:
        path = os.path.join(os.getcwd(), c_d.WIN_LOG_P_DEF)

    path = os.path.join(path, "{:s}_{:s}".format(name, datetime.datetime.now().strftime(c_d.TYPICAL_TIMESTAMP)))

    if not os.path.isdir(path):
        os.mkdir(path, 0o777)

    path = os.path.join(path, name)

    logging.basicConfig(format=c_d.LOG_FORMAT,
                        filename=path,
                        level=(logging.DEBUG if debug else logging.WARNING))


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
        init_logging(c_d.SOLUTION, g_v.DEBUG)

    # main func
    logging.info("start work: {:s}".format(" ".join(sys.argv)))

    git_man = GitMan()
    git_man.try_get_build_ver()

    tag_model = TagModel()
    cfg_loader = CfgLoader()

    res = cfg_loader.open_cfg()
    if res is not None:
        logging.critical("can't open config")
        sys.exit(res)

    if g_v.DEBUG:
        logging.info("-q {:s}".format(str(g_v.VERBOSE)))
        logging.info("-l {:s}".format(str(g_v.LOGGING)))
        logging.info("-m {:s}".format(str(g_v.MULTITH)))
        logging.info("-d {:s}".format(str(g_v.DEBUG)))
        logging.info("-t {:s}".format(str(g_v.TIMEOUTS)))

    # branch by options
    bad_args = False

    if is_setup_hooks(opts):
        setup_hooks(cfg_loader, tag_model)
    elif is_related_update(opts):
        if args and len(args) == 1:
            cfg_loader.add_repo_to_updates(args[0])
        else:
            bad_args = True
    elif is_full_update(opts):
        update(cfg_loader, git_man, tag_model)
    elif is_update(opts):
        cfg_loader.partly_update = True
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
        logging.critical(c_d.E_BAD_ARGS)
        sys.exit(c_d.EXIT_WO)

    stop(main_t)
    if g_v.TIMEOUTS: logging.warning("finish work: {:s}".format(get_pass_time(main_t)))

if __name__ == "__main__":
    main()


