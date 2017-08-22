#!/usr/bin/env python3

import os

import common
from tag_model import TagModel
from tag_model import Tag
from tag_model import Repo
from cmd_wrap import runCmd
from logger import outLog
from logger import outErr

class GitMan:
    def __init__(self):
        self.update = False
        self.lastBr = " "
        self.needReturnBranch = False

    def setUpdate(self, update):
        self.update = update

    def updateRepo(self):
        (_, err) = runCmd(common.UPD_REPO)

        outLog(self.__class__.__name__, "update repo")

        if err:
            outErr(self.__class__.__name__, err)

    def checkBranch(self):
        branch = self.curBranch()
        outLog(self.__class__.__name__, "cur branch: " + branch)

        if branch != common.BR_DEV:
            self.lastBr = branch
            self.needReturnBranch = True
            self.switchBranch(common.BR_DEV)
            outLog(self.__class__.__name__, "cur branch: " + self.curBranch())

    def curBranch(self):
        (branch, _) = runCmd(common.CUR_BRANCH)
        return branch

    def switchBranch(self, branch):
        outLog(self.__class__.__name__, "switch to branch: " + branch)
        runCmd(common.SW_BRANCH + branch)

    def returnBranch(self):
        outLog(self.__class__.__name__, "return branch")
        outLog(self.__class__.__name__, "cur branch: " + self.curBranch())
        self.switchBranch(self.lastBr)
        self.needReturnBranch = False
        outLog(self.__class__.__name__, "cur branch: " + self.curBranch())

    # use module os for multiplatform
    def goToDir(self, link):
        outLog(self.__class__.__name__, "go to dir: " + link)
        os.chdir(link)

    def checkDir(self, link):
        curDir = os.getcwd()

        if curDir[-1:] == "\/":
            curDir = curDir[:-1]

        outLog(self.__class__.__name__, "cur dir: " + curDir)

        if curDir != link:
            outErr(self.__class__.__name__, "can't go to " + link)
            return False
        return True

    def doDirtyJob(self, model):
        deps = model.getDepsKeys()

        for dep, repos in deps.items():
            outLog(self.__class__.__name__, dep)
            for repo in repos:
                link = repo.getLink()
                # try go to dir link
                self.goToDir(link)
                if self.checkDir(link):
                    # check branch
                    self.checkBranch()

                    # update if need
                    if self.update:
                        self.updateRepo()

                    # do dirty work

                    # return last branch if need
                    if self.needReturnBranch:
                        self.returnBranch()

        # for even dep
        # for even repo
        # update or not
        # get all tags
        # fill tags