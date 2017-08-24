import datetime
import inspect
import os

import common

def initLog():
    os.chdir(os.path.dirname(os.path.realpath(__file__)))

    path = os.getcwd() + "/" + common.WIN_PATH

    if common.CUR_PLATFORM == common.LINUX_P:
        path = common.LIN_PATH

    if not os.path.isdir(path):
        os.mkdir(path, 0o777)

    outLog("logger", "path: " + path)

    common.CUR_PATH = path

    outLog("logger",  "cur path: " + common.CUR_PATH)

    LOG_F = open(common.CUR_PATH + common.LOG_T, 'w')
    ERR_F = open(common.CUR_PATH + common.ERR_T, 'w')

def writeMsg(msg, path):
    if common.LOGGING:
        f = open(common.CUR_PATH + path, 'a')
        if f:
            f.write(msg + "\n")
            f.close()

def outLog(who, msg):
    writeMsg(outMsg(who, msg, common.LOG_T), common.LOG_T)

def outErr(who, msg):
    writeMsg(outMsg(who, msg, common.ERR_T), common.ERR_T)

def outMsg(who, msg, type):
    out = "[%s] : [%s:%-20s] : [%s] : [%s]" % (type, who, whoami()+"()", datetime.datetime.now().__str__(), msg)

    if not common.QUIET:
        print (out)

    return out

def whoami():
    return inspect.stack()[3][3]

def main():
    print ("do nothing from there")
    
if __name__ == "__main__":
    main()