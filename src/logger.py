#!/usr/bin/env python3

import datetime

def outMsg(who, msg):
    print ("[" + who + "] : [" +
           datetime.datetime.now().__str__() + "] : [" +
           msg + "]")

def main():
    print ("do nothing from there")
    
if __name__ == "__main__":
    main()