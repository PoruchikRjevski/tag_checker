import datetime
import inspect
import os
import threading
from collections import OrderedDict
from queue import Queue

import common_defs as c_d
import global_vars as g_v

__all__ = ['init_log', 'out_log', 'out_err', 'start_thread_logging', 'finish_thread_logging', 'out_deffered_logs']

threads_list = []
threads_list_f = []
threads_logs = OrderedDict()
threads_errs = OrderedDict()


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
    open(g_v.CUR_PATH + c_d.ERR_T, 'w')


def start_thread_logging():
    pid = str(threading.get_ident())
    threads_list.append(pid)
    threads_logs[pid] = []
    threads_errs[pid] = []


def finish_thread_logging():
    pid = str(threading.get_ident())
    # threads_list.remove(pid)
    threads_list_f.append(pid)


def out_deffered_logs():
    for pid in threads_list:
        if pid in threads_logs.keys():
            out_msg(gen_log_msg("", c_d.LOG_T, 2), c_d.LOG_T)
            out_msg(gen_log_msg("PID: {:s}".format(pid), c_d.LOG_T, 2), c_d.LOG_T)
            for out in threads_logs[pid]:
                out_msg(out, c_d.LOG_T)

        if pid in threads_errs.keys():
            out_msg(gen_log_msg("", c_d.ERR_T, 2), c_d.ERR_T)
            out_msg(gen_log_msg("PID: {:s}".format(pid), c_d.ERR_T, 2), c_d.ERR_T)
            for out in threads_errs[pid]:
                out_msg(out, c_d.ERR_T)


def write_msg(msg, path):
    if g_v.LOGGING:
        with open(g_v.CUR_PATH + path, 'a') as f:
            f.write(msg + "\n")


def out_log(msg):
    pid = str(threading.get_ident())

    out = gen_log_msg(msg, c_d.LOG_T, 3)

    if g_v.MULTITH:
        check_pid(pid)

        threads_logs[pid].append(out)
    else:
        out_msg(out, c_d.LOG_T)
    # if pid in threads_list and g_v.MULTITH:
    #     threads_logs[pid].append(out)
    # else:



def out_msg(out, place):
    write_msg(out, place)
    show_msg(out)


def check_pid(pid):
    if pid not in threads_list:
        threads_list.append(pid)
        threads_logs[pid] = []
        threads_errs[pid] = []


def out_err(msg):
    pid = str(threading.get_ident())

    out = gen_log_msg(msg, c_d.ERR_T, 3)

    if g_v.MULTITH:
        check_pid(pid)

        threads_errs[pid].append(out)
    else:
        out_msg(out, c_d.ERR_T)

    # if pid in threads_list and g_v.MULTITH:
    #     threads_errs[pid].append(out)
    # else:
    #     out_msg(out, c_d.ERR_T)


def gen_log_msg(msg, type, level):
    (c_name, c_line) = get_caller_info(level)

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


def main():
    print("do nothing from there")
    
if __name__ == "__main__":
    main()
