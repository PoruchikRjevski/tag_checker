import os
import logging
import datetime
import inspect

import common_defs as c_d
import global_vars as g_v


__all__ = ['init_logging', 'debug', 'info', 'warning', 'error', 'critical']


logger = None
FORMAT = '[%(asctime)s] : [%(levelname)-8s] : [%(funcName)-30s]'


def is_inited(func):
    def wrapped(msg, *args, **kwargs):
        global logger
        if not logger is None:
            return func(msg, *args, **kwargs)
    return wrapped


def init_logging(name, debug):
    global logger, FORMAT

    path = ""

    if g_v.CUR_PLATFORM == c_d.LINUX_P:
        path = c_d.LIN_LOG_P_DEF
    elif g_v.CUR_PLATFORM == c_d.WINDOWS_P:
        path = os.path.join(os.getcwd(), c_d.WIN_LOG_P_DEF)

    path = os.path.join(path, "{:s}_{:s}".format(name, datetime.datetime.now().strftime(c_d.TYPICAL_TIMESTAMP)))

    if not os.path.isdir(path):
        os.mkdir(path, 0o777)

    path = os.path.join(path, name)

    logging.basicConfig(format=FORMAT,
                        filename=path,
                        level=(logging.DEBUG if debug else logging.WARNING))


@is_inited
def debug(msg):
    global logger
    logger.debug(msg)


@is_inited
def info(msg):
    global logger
    logger.info(msg)


@is_inited
def warning(msg):
    global logger
    logger.warning(msg)


@is_inited
def error(msg):
    global logger
    logger.error(msg)


@is_inited
def critical(msg):
    global logger
    logger.critical(msg)


def get_caller_info(level):
    stack = inspect.stack()

    if len(stack) < level:
        return ""

    parent_frame = stack[level][0]

    # get line number
    line_num = str(inspect.getframeinfo(parent_frame).lineno)

    full_name = "{:s}:{:s}"
    module_name = ""

    # get class or module name
    if 'self' in parent_frame.f_locals:
        module_name = parent_frame.f_locals['self'].__class__.__name__
    else:
        module = inspect.getmodule(parent_frame)
        if module:
            module_name = module.__name__

    full_name = full_name.format(module_name,
                                 parent_frame.f_code.co_name)

    return full_name, line_num
