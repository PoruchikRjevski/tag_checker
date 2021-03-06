#!/usr/bin/sudo python3

import os
import sys
from optparse import OptionParser

import common_defs as c_d
from cmd_executor.cmd_executor import *
from config_manager import dir_man


def is_tag_checker_runned():
    out = run_cmd("ps -eo pid,cmd | grep '[t]ag_checker/main.py'")

    if out:
        return True

    return False


def run_tag_checker():
    exec_path = os.path.join(dir_man.g_dir_man.bin_dir, "main.py")
    # os.spawnl(os.P_NOWAIT, exec_path, *sys.argv)
    os.system("{:s} {:s}".format(exec_path,
                                 " ".join(sys.argv[1:])))


def main():
    if is_tag_checker_runned():
        print(c_d.E_ALREADY_RUNS)
        sys.exit(c_d.EXIT_AR)
    else:
        run_tag_checker()

    sys.exit(c_d.EXIT_NORMAL)


if __name__ == "__main__":
    main()
