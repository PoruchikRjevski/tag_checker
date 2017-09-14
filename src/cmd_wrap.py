import subprocess
import threading

import common_defs as c_d
import global_vars as g_v
from logger import *
from time_profiler.time_checker import *

__all__ = ['run_cmd']


def run_cmd(cmd):
    command = ""

    if g_v.SUDOER:
        command = c_d.SUDO_CMD

    command += cmd

    if g_v.DEBUG: out_log("cmd: " + command)

    cmd_run_t = start()
    proc = subprocess.Popen([command + '\n'],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            shell=True)
    (out, err) = proc.communicate()
    stop(cmd_run_t)

    if g_v.TIM_OUT: out_log("exec time: {:s} | pid: {:s} | cmd: \"{:s}\"".format(get_pass_time(cmd_run_t),
                                                                             str(threading.get_ident()),
                                                                             command))

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