import datetime
import inspect
import os
import threading
from collections import OrderedDict
from queue import Queue

import common_defs as c_d
import global_vars as g_v

__all__ = ['init_log', 'out_log', 'out_err', 'start_thread_logging', 'finish_thread_logging', 'out_threads_logs']

threads_list = []
threads_list_f = []
threads_out = OrderedDict()


def init_log():
    os.chdir(os.path.dirname(os.path.realpath(__file__)))

    path = ""

    if g_v.CUR_PLATFORM == c_d.LINUX_P:
        path = c_d.LIN_LOG_P_DEF
    elif g_v.CUR_PLATFORM == c_d.WINDOWS_P:
        path = os.path.join(os.getcwd(), c_d.WIN_LOG_P_DEF)

    if not os.path.isdir(path):
        os.mkdir(path, 0o777)

    g_v.CUR_PATH = path

    open(g_v.CUR_PATH + c_d.LOG_T, 'w')
    # open(g_v.CUR_PATH + c_d.ERR_T, 'w')


def start_thread_logging():
    pid = str(threading.get_ident())
    threads_list.append(pid)
    threads_out[pid] = []


def finish_thread_logging():
    pid = str(threading.get_ident())
    # threads_list.remove(pid)
    threads_list_f.append(pid)


def out_threads_logs():
    for pid in threads_list:
        if pid in threads_list_f:
            for out in threads_out[pid]:
                out_msg(out, c_d.LOG_T)


def write_msg(msg, path):
    if g_v.LOGGING:
        with open(g_v.CUR_PATH + path, 'a') as f:
            f.write(msg + "\n")


def out_log(msg):
    pid = str(threading.get_ident())

    out = gen_log_msg(msg, c_d.LOG_T)

    if pid in threads_list:
        threads_out[pid].append(out)
    else:
        out_msg(out, c_d.LOG_T)


def out_msg(out, place):
    write_msg(out, place)
    show_msg(out)


def out_err(msg):
    pid = str(threading.get_ident())

    out = gen_log_msg(msg, c_d.ERR_T)

    if pid in threads_list:
        threads_out[pid].append(out)
    else:
        out_msg(out, c_d.LOG_T)


def gen_log_msg(msg, type):
    (c_name, c_line) = get_caller_info()

    c_name += "()" + " " * (c_d.LOG_SYMB_CALLER - len(c_name))
    c_line = " " * (c_d.LOG_SYMB_C_LINE - len(c_line)) + c_line

    return "[{:s}] : [{:s}] : [{:s}] : [L: {:s}] : [{:s}] ".format(datetime.datetime.now().__str__(),
                                                                   type,
                                                                   c_name,
                                                                   c_line,
                                                                   msg)


def show_msg(msg):
    if not g_v.QUIET:
        print(msg)


def get_caller_info():
    stack = inspect.stack()

    if len(stack) < 3:
        return ""

    parent_frame = stack[3][0]

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


def main():
    print("do nothing from there")
    
if __name__ == "__main__":
    main()
