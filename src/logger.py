import os
import logging
import datetime

import common_defs as c_d
import global_vars as g_v


__all__ = ['init_logging']


logger = None
formatter = None
file_handler = None
stream_handler = None


def gen_path(name):
    path = ""
    if g_v.CUR_PLATFORM == c_d.LINUX_P:
        path = c_d.LIN_LOG_P_DEF
    elif g_v.CUR_PLATFORM == c_d.WINDOWS_P:
        path = os.path.join(os.getcwd(), c_d.WIN_LOG_P_DEF)

    path = os.path.join(path, "{:s}_{:s}".format(name, datetime.datetime.now().strftime(c_d.TYPICAL_TIMESTAMP)))

    if not os.path.exists(path):
        os.makedirs(path, 0o777, True)

    return os.path.join(path, name)


def init_logging():
    global logger

    name = c_d.SOLUTION

    file_handler = None
    stream_handler = None
    formatter = logging.Formatter("[{:s}] : [{:s}] : [{:s}] : [{:s}] : [{:s}] : [{:s}] : [{:s}]".format(c_d.LOG_TIME,
                                                                                                        c_d.LOG_LEVEL,
                                                                                                        c_d.LOG_THREAD,
                                                                                                        c_d.LOG_NAME,
                                                                                                        c_d.LOG_FUNC,
                                                                                                        c_d.LOG_LINE,
                                                                                                        c_d.LOG_MSG))
    log_level = logging.DEBUG

    logger = logging.getLogger(name)
    logger.propagate = False
    logger.setLevel(log_level)

    if g_v.VERBOSE:
        logger.propagate = True

        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(log_level)
        stream_handler.setFormatter(formatter)
        logger.addHandler(stream_handler)

    if g_v.LOGGING:
        path = gen_path(name)
        file_handler = logging.FileHandler(path)
        file_handler.setFormatter(formatter)
        file_handler.setLevel(log_level)
        logger.addHandler(file_handler)
