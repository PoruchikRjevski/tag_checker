import datetime
import inspect
import os

import common


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
    write_msg(out_msg(who, msg, common.LOG_T), common.LOG_T)


def out_err(who, msg):
    write_msg(out_msg(who, msg, common.ERR_T), common.ERR_T)


def out_msg(who, msg, type):
    caller = caller_func()

    symbols = common.LOG_SYMB_CALLER - len(caller) - len(who)

    caller += " " * symbols

    out = "{:s} : [{:s}:{:s}] : {:s} : {:s} ".format(type, who,
                                                     caller + "()", datetime.datetime.now().__str__(),
                                                     msg)
    # out = "[%s] : [%s:%-20s] : [%s] : [%s]" % (type, who, whoiam() + "()", datetime.datetime.now().__str__(), msg)

    if not common.QUIET:
        print(out)

    return out


def caller_func():
    return inspect.stack()[3][3]


def main():
    print("do nothing from there")
    
if __name__ == "__main__":
    main()
