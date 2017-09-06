import subprocess

import common_defs as c_d
import global_vars as g_v
from logger import *

__all__ = ['run_cmd']


def run_cmd(cmd):
    command = ""

    if g_v.SUDOER:
        command = c_d.SUDO_CMD

    command += cmd

    out_log(c_d.CMD_WRAP, "cmd: " + command)

    proc = subprocess.Popen([command + '\n'],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            shell=True)
    (out, err) = proc.communicate()

    u_out = out.decode(c_d.DOC_CODE).strip()
    u_err = err.decode(c_d.DOC_CODE).strip()

    if u_err:
        out_err(c_d.CMD_WRAP, "cmd: " + cmd)
        out_err(c_d.CMD_WRAP, "err: " + u_err)

    return u_out


def main():
    print ("do nothing from there")

if __name__ == "__main__":
    main()