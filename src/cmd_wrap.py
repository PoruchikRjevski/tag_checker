import subprocess

import common_defs
from logger import *

__all__ = ['run_cmd']


def run_cmd(cmd):
    prefix = ""

    if common_defs.SUDOER:
        prefix = common_defs.SUDO_CMD

    proc = subprocess.Popen([prefix +cmd + '\n'],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            shell=True)
    (out, err) = proc.communicate()

    u_out = out.decode("utf-8").strip()
    u_err = err.decode("utf-8").strip()

    if u_err:
        out_err(common_defs.CMD_WRAP, "cmd: " + cmd)
        out_err(common_defs.CMD_WRAP, "err: " + u_err)

    return u_out


def main():
    print ("do nothing from there")

if __name__ == "__main__":
    main()