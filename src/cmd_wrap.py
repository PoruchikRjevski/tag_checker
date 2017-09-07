import subprocess
import threading

import common_defs as c_d
import global_vars as g_v
from logger import *
from time_checker import *

__all__ = ['run_cmd']


t_chckr = TimeChecker()

# def init_cmd_wrapper():
#     t_chckr = TimeChecker()


def run_cmd(cmd):
    command = ""

    if g_v.SUDOER:
        command = c_d.SUDO_CMD

    command += cmd

    # out_log(c_d.CMD_WRAP, "cmd: " + command)

    t_chckr.start
    proc = subprocess.Popen([command + '\n'],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            shell=True)
    (out, err) = proc.communicate()
    t_chckr.stop

    out_log("cmd: {:s} | pid: {:s} | exec time: {:s}".format(command,
                                                             str(threading.get_ident()),
                                                             t_chckr.passed_time_str,))

    u_out = out.decode(c_d.DOC_CODE).strip()
    u_err = err.decode(c_d.DOC_CODE).strip()

    # out_log("out: {:s}".format(u_out))

    if u_err:
        out_err("err: {:s}".format(u_err))

    return u_out


def main():
    print ("do nothing from there")

if __name__ == "__main__":
    main()