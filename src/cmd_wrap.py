import subprocess

import common
import logger

def runCmd(cmd):
    proc = subprocess.Popen([cmd],
                            stdout=subprocess.PIPE,
                            shell=True)
    (out, err) = proc.communicate()
    
    if err:
        logger.outMsg(common.CMD_WRAP, err)
        # to log
    
    return out


def main():
    print ("do nothing from there")
    
if __name__ == "__main__":
    main()