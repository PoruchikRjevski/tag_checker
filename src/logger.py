import datetime

import common
from common import whoami

# TODO logs to
# linux: /tmp/tag_checker_log/
# windows: $CUR_DIR/log/

def outLog(who, msg):
    outMsg(who, msg, common.LOG_T)

def outErr(who, msg):
    outMsg(who, msg, common.ERR_T)

def outMsg(who, msg, type):
    out = "[%s] : [%s:%-20s] : [%s] : [%s]" % (type, who, whoami()+"()", datetime.datetime.now().__str__(), msg)

    return print (out)

def main():
    print ("do nothing from there")
    
if __name__ == "__main__":
    main()