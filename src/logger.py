import datetime
import inspect
import os

import common

# TODO logs to
# linux: /tmp/tag_checker_log/
# windows: $CUR_DIR/log/

def initLog():
    path = common.WIN_PATH

    if common.CUR_PLATFORM == common.LINUX_P:
        path = common.LIN_PATH

    if not os.path.isdir(path):
        os.mkdir(path, 0o777)

    outLog("logger", "path: " + path)

    common.CUR_PATH = path

    outLog("logger",  "cur path: " + common.CUR_PATH)

    LOG_F = open(common.CUR_PATH + common.LOG_T, 'w')
    ERR_F = open(common.CUR_PATH + common.ERR_T, 'w')

def writeLog(msg):
    LOG_F = open(common.CUR_PATH + common.LOG_T, 'a')
    if LOG_F:
        LOG_F.write(msg + "\n")
        LOG_F.close()

def writeErr(msg):
    ERR_F = open(common.CUR_PATH + common.ERR_T, 'a')
    if ERR_F:
        ERR_F.write(msg + "\n")
        ERR_F.close()

def outLog(who, msg):
    writeLog(outMsg(who, msg, common.LOG_T))

def outErr(who, msg):
    writeErr(outMsg(who, msg, common.ERR_T))

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