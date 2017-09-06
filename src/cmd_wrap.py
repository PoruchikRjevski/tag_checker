import subprocess

import common_defs as c_d
import global_vars as g_v
from logger import *

__all__ = ['run_cmd']


def run_cmd(cmd):
    prefix = ""

    if g_v.SUDOER:
        prefix = c_d.SUDO_CMD

    proc = subprocess.Popen([prefix + cmd + '\n'],
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