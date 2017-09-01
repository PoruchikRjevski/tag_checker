import datetime
import inspect
import os
from queue import Queue

import common

__all__ = ['init_log', 'out_log', 'out_err', 'out_log_def', 'out_err_def', 'release_log', 'release_err']

def init_log():
    os.chdir(os.path.dirname(os.path.realpath(__file__)))

    path = os.getcwd() + "/" + common.WIN_PATH

    if common.CUR_PLATFORM == common.LINUX_P:
        path = common.LIN_PATH

    if not os.path.isdir(path):
        os.mkdir(path, 0o777)

    common.CUR_PATH = path

    open(common.CUR_PATH + common.LOG_T, 'w')
    open(common.CUR_PATH + common.ERR_T, 'w')


def write_msg(msg, path):
    if common.LOGGING:
        f = open(common.CUR_PATH + path, 'a')
        if f:
            f.write(msg + "\n")
            f.close()


def out_log(who, msg):
    out = gen_log_msg(who, msg, common.LOG_T)
    write_msg(out, common.LOG_T)

    show_msg(out)


def out_log_def(who, msg):
    return gen_log_msg(who, msg, common.LOG_T)


def release_log(msgs):
    if not isinstance(msgs, str):
        for msg in msgs:
            write_msg(msg, common.LOG_T)
            show_msg(msg)
    else:
        write_msg(msgs, common.LOG_T)
        show_msg(msgs)


def out_err(who, msg):
    out = gen_log_msg(who, msg, common.ERR_T)
    write_msg(out, common.ERR_T)

    show_msg(out)


def out_err_def(who, msg):
    return gen_log_msg(who, msg, common.ERR_T)


def release_err(msgs):
    if not isinstance(msgs, str):
        for msg in msgs:
            write_msg(msg, common.ERR_T)
            show_msg(msg)
    else:
        write_msg(msgs, common.ERR_T)
        show_msg(msgs)


def gen_log_msg(who, msg, type):
    caller = caller_func()
    c_line = caller_line()

    caller += "()"

    symbols = common.LOG_SYMB_CALLER - len(caller) - len(who)

    caller += " " * symbols

    symbols = common.LOG_SYMB_C_LINE - len(c_line)

    c_line = " " * symbols + c_line

    out = "[{:s}] : [{:s}] : [{:s}:{:s}] : [L: {:s}] : [{:s}] ".format(datetime.datetime.now().__str__(), type,
                                                                       who, caller,
                                                                       c_line, msg)

    return out


def show_msg(msg):
    if not common.QUIET:
        print(msg)


def caller_func():
    return str(inspect.stack()[3][3])

def caller_line():
    frame = inspect.stack()[3][0]
    info = inspect.getframeinfo(frame)
    return str(info.lineno)

def main():
    print("do nothing from there")
    
if __name__ == "__main__":
    main()
