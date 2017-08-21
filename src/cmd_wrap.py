import subprocess

import common
from logger import outMsg

def runCmd(cmd):
    proc = subprocess.Popen([cmd],
                            stdout=subprocess.PIPE,
                            shell=True)
    (out, err) = proc.communicate()
    
    if err:
        outMsg(common.CMD_WRAP, err)
        # to log
    
    return out

def main():
    print ("do nothing from there")

if __name__ == "__main__":
    main()