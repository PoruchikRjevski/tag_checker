import subprocess
import threading

import common_defs as c_d
import global_vars as g_v
from logger import *
from time_checker import *

__all__ = ['run_cmd']


def run_cmd(cmd):
    command = ""

    if g_v.SUDOER:
        command = c_d.SUDO_CMD

    command += cmd

    if g_v.DEBUG: out_log(c_d.CMD_WRAP, "cmd: " + command)

    cmd_run_t = start()
    proc = subprocess.Popen([command + '\n'],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            shell=True)
    (out, err) = proc.communicate()
    stop(cmd_run_t)

    if g_v.DEBUG: out_log("cmd: {:s} | pid: {:s} | exec time: {:s}".format(command,
                                                                           str(threading.get_ident()),
                                                                           get_pass_time(cmd_run_t)))

    u_out = out.decode(c_d.DOC_CODE).strip()
    u_err = err.decode(c_d.DOC_CODE).strip()

    if g_v.DEBUG: out_log("out: {:s}".format(u_out))

    if u_err:
        out_err("err: {:s}".format(u_err))

    return u_out


def main():
    print ("do nothing from there")

if __name__ == "__main__":
    main()