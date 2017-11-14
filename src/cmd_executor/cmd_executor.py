import subprocess
import threading
import logging

import common_defs as c_d
import global_vars as g_v
from time_profiler.time_checker import *

__all__ = ['run_cmd']


logger = logging.getLogger("{:s}.CmdExecutor".format(c_d.SOLUTION))


def run_cmd(command):
    if not command:
        return ""

    logger.info("cmd: {:s}".format(command))

    cmd_run_t = start()
    proc = subprocess.Popen(['{:s}\n'.format(command)],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            shell=True)
    (out, err) = proc.communicate()
    stop(cmd_run_t)

    logger.info("exec time: {:s} | pid: {:s} | cmd: \"{:s}\"".format(get_pass_time(cmd_run_t),
                                                                     str(threading.get_ident()),
                                                                     command))

    u_out = out.decode(c_d.DOC_CODE).strip()
    u_err = err.decode(c_d.DOC_CODE).strip()

    logger.info("out: {:s}".format(u_out))

    if u_err:
        logger.error("err: {:s}".format(u_err))

    return u_out


def main():
    print("do nothing from there")

if __name__ == "__main__":
    main()