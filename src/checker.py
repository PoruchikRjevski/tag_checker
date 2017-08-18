#!/usr/bin/env python3

import os
import sys
import getopt
import string
import subprocess

import common
import logger

import configparser

def isGitInstalled():
    proc = subprocess.Popen(["git --version"],
                            stdout=subprocess.PIPE,
                            shell=True)
    (out, err) = proc.communicate()
    
    if not str(out).__contains__("version"):
        return True
    
    return False
    
def isConfFileExist(fileName):
    if open(fileName, 'r'):
        return True
    
    return False
    
def main():
    # check arguments
    try:
        opts, args = getopt.getopt(sys.argv[1:], "h", ["help"])
    except getopt.GetoptError as err:
        logger.outMsg(common.CHECKER, common.E_WA_STR)
        logger.outMsg(common.CHECKER, common.FOR_HELP)
           
        sys.exit(common.EXIT_WA)
    
    for o in opts:
        if o in ("-h", "--help"):
            print (__doc__)
            sys.exit(common.EXIT_NORMAL)
    
    if not isConfFileExist(args[0]):
        logger.outMsg(common.CHECKER, common.E_GNT_STR)
        sys.exit(common.EXIT_CFNE)
    
    # check environment
    if not isGitInstalled():
        logger.outMsg(common.CHECKER, common.E_GNT_STR)
        sys.exit(common.EXIT_GNT)    

    # start work    

if __name__ == "__main__":
    main()

# check arguments
# check config file exist
# tests 
# 

config = configparser.ConfigParser()
config.read('src/config.ini')

departments = config.sections()

deps = list()

for i in departments:
    repos = config.get(i, 'repos').split(", ") 
    for j in repos:
        print (j)
    deps.append((i, repos))

for i in deps:
    #for j in i[1]
    print (i)



#print ('suka')

#print config.get('140', 'repo_lnk', 0)


