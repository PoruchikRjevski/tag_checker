#!/usr/bin/sudo python3
import sys
from optparse import OptionParser
import logging

import os

import common_defs as c_d
import global_vars as g_v
import version as v
from config_manager import CfgLoader, dir_man
from git_manager import GitMan
from tag_model import TagModel
from time_profiler.time_checker import *
from web_generator.web_gen import WebGenerator
from logger import init_logging, log_func_name


logger = logging.getLogger("{:s}.main".format(c_d.SOLUTION))


def init_logger(func):
    def wrapped(*args, **kwargs):
        init_logging()

        return func(*args, **kwargs)

    return wrapped


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

    parser.add_option("-c", "--cfg-dir",
                      dest="config_dir",
                      help="overrides config file directory path (rel or abs)")
    parser.add_option("--root-dir",
                      dest="root_dir",
                      help="overrides root directory path")
    parser.add_option("--short-dirs",
                      action="store_true", dest="short_dirs",
                      default=False,
                      help="do use short relative dirs")


def setup_options(opts):
    if opts.verbose:
        g_v.VERBOSE = True
    if opts.log:
        g_v.LOGGING = True
    if opts.multithreading:
        g_v.MULTITH = True
    if opts.root_dir:
        if not os.path.isabs(opts.root_dir):
            dir_man.g_dir_man.def_root_dir = os.path.join(os.getcwd(), opts.root_dir)
        else:
            dir_man.g_dir_man.def_root_dir = opts.root_dir
        dir_man.g_dir_man.reconfigure()
    if opts.short_dirs:
        dir_man.g_dir_man.default_configure_short_rel_paths()
    if opts.config_dir:
        if not os.path.isabs(opts.config_dir):
            dir_man.g_dir_man.def_config_dir = os.path.join(os.getcwd(), opts.config_dir)
        else:
            dir_man.g_dir_man.def_config_dir = opts.config_dir
        dir_man.g_dir_man.reconfigure()


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


def is_partial_update(opts):
    return (not opts.fully) and opts.update


def is_full_update(opts):
    return opts.fully and opts.update


def is_related_update(opts):
    return opts.update and opts.related and opts.repo


def is_change_prefix(opts):
    return opts.prefix


def is_setup_hooks(opts):
    return opts.setuphooks


def update(cfg_loader, git_man, tag_model):
    main_t = start()
    logger.info("Start work")
    # load config
    if cfg_loader.load_config(tag_model):
        # get tags and fill model
        scan_t = start()
        git_man.scanning(tag_model)
        stop(scan_t)
        g_v.SCAN_TIME = "{:s}".format(get_pass_time(scan_t))
        logger.info("Scan time: {:s}".format(g_v.SCAN_TIME))

        # generate web
        web_gen_t = start()
        web_gen = WebGenerator()
        web_gen.generate_web(tag_model, cfg_loader.partly_update)
        stop(web_gen_t)
        logger.info("web gen time: {:s}".format(get_pass_time(web_gen_t)))

    stop(main_t)
    logger.info("finish work: {:s}".format(get_pass_time(main_t)))


@init_logger
@log_func_name(logger)
def setup_hooks():
    tag_model = TagModel()
    cfg_loader = CfgLoader()

    cfg_loader.load_config(tag_model)

    cfg_loader.setup_hooks(tag_model)


@init_logger
@log_func_name(logger)
def full_update(updates_list = None):
    if updates_list is None:
        updates_list = []

    tag_model = TagModel()
    git_man = GitMan()
    cfg_loader = CfgLoader(updates_list)

    if updates_list:
        cfg_loader.partly_update = False # todo return True and fix the problem

    update(cfg_loader, git_man, tag_model)


def partial_update():
    updates_list = CfgLoader.get_list_of_updates()

    if updates_list:
        full_update(updates_list)


@init_logger
@log_func_name(logger)
def add_related_update(args):
    if args and len(args) == 1:
        CfgLoader.add_repo_to_updates(args[0])
        return False

    return True


@init_logger
@log_func_name(logger)
def show_config(args):
    cfg_loader = CfgLoader()

    if args and len(args) > 1:
        cfg_loader.show(args[0])
    else:
        cfg_loader.show()


@init_logger
@log_func_name(logger)
def add_repo(args):
    cfg_loader = CfgLoader()

    if args and len(args) > 1:
        cfg_loader.add_repo(args[0], args[1:])
        return False

    return True


@init_logger
@log_func_name(logger)
def rem_repo(args):
    cfg_loader = CfgLoader()

    if args and len(args) > 1:
        cfg_loader.rem_repo(args[0], args[1:])
        return False

    return True


@init_logger
@log_func_name(logger)
def add_tr(args):
    cfg_loader = CfgLoader()

    if args and len(args) == 2:
        cfg_loader.add_translate(args[0], args[1])
        return False

    return True


@init_logger
@log_func_name(logger)
def rem_tr(args):
    cfg_loader = CfgLoader()

    if args and len(args) > 0:
        cfg_loader.rem_translate(args)
        return False

    return True


@init_logger
@log_func_name(logger)
def add_dep(args):
    cfg_loader = CfgLoader()

    if args and len(args) > 0:
        cfg_loader.add_department(args)
        return False

    return True


@init_logger
@log_func_name(logger)
def rem_dep(args):
    cfg_loader = CfgLoader()

    if args and len(args) > 0:
        cfg_loader.rem_department(args)
        return False

    return True


@init_logger
@log_func_name(logger)
def change_prefix(args):
    cfg_loader = CfgLoader()

    if args and len(args) == 2:
        cfg_loader.change_prefix(args[0], args[1])
        return False

    return True


def get_version_str():
    commits_diff = int(v.LAST)

    try:
        cur = int(v.CURRENT)
        v.V_BUILD = str(cur)

        commits_diff = cur - commits_diff
    except ValueError:
        commits_diff = 0

    v.FULL_VERSION = "Версия: {:s}.{:s}.{:s}({:s}) {:s}:{:s}".format(v.V_MAJ,
                                                                     v.V_MIN,
                                                                     str(commits_diff),
                                                                     v.V_BUILD,
                                                                     v.V_STAT,
                                                                     v.HASH)


def main():
    get_version_str()

    # check options
    opt_parser = OptionParser(version=v.FULL_VERSION)
    set_options(opt_parser)

    (opts, args) = opt_parser.parse_args()

    if check_main_opts(opts):
        setup_options(opts)
    else:
        opt_parser.print_help()
        sys.exit(c_d.EXIT_WO)

    # options branch
    bad_args = False

    # set version

    if is_related_update(opts):
        bad_args = add_related_update(args)
    elif is_full_update(opts):
        full_update()
    elif is_partial_update(opts):
        partial_update()
    elif is_setup_hooks(opts):
        setup_hooks()
    elif is_show(opts):
        show_config(args)
    elif is_add_repo(opts):
        bad_args = add_repo(args)
    elif is_remove_repo(opts):
        bad_args = rem_repo(args)
    elif is_add_translate(opts):
        bad_args = add_tr(args)
    elif is_remove_translate(opts):
        bad_args = rem_tr(args)
    elif is_add_department(opts):
        bad_args = add_dep(args)
    elif is_remove_department(opts):
        bad_args = rem_dep(args)
    elif is_change_prefix(opts):
        bad_args = change_prefix(args)

    if bad_args:
        logger.critical(c_d.E_BAD_ARGS)
        sys.exit(c_d.EXIT_WO)

if __name__ == "__main__":
    main()


