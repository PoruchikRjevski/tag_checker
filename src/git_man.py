import os

import common
from tag_model import TagModel
from tag_model import Repo
from tag_model import Note
from tag_model import Device
from cmd_wrap import runCmd
from logger import outLog
from logger import outErr
from time_checker import TimeChecker

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
        branch = self.getCurrentBranch()
        outLog(self.__class__.__name__, "cur branch: " + branch)

        if branch != common.BR_DEV:
            self.lastBr = branch
            self.needReturnBranch = True
            self.switchToBranch(common.BR_DEV)
            outLog(self.__class__.__name__, "cur branch: " + self.getCurrentBranch())

    def getCurrentBranch(self):
        (branch, _) = runCmd(common.CUR_BRANCH)
        return branch

    def switchToBranch(self, branch):
        outLog(self.__class__.__name__, "switch to branch: " + branch)
        runCmd(common.SW_BRANCH + branch)

    def returnBackBranch(self):
        outLog(self.__class__.__name__, "return branch")
        outLog(self.__class__.__name__, "cur branch: " + self.getCurrentBranch())
        self.switchToBranch(self.lastBr)
        self.needReturnBranch = False
        outLog(self.__class__.__name__, "cur branch: " + self.getCurrentBranch())

    # use module os for multiplatform
    def goToDir(self, link):
        outLog(self.__class__.__name__, "go to dir: " + link)
        os.chdir(link)

    def isDirExist(self, link):
        curDir = os.getcwd()

        if link[-1:] == "/" and not curDir[-1:] == "/":
            curDir = curDir + "/"
        elif not link[-1:] == "/" and curDir[-1:] == "/":
            curDir = curDir[:-1]

        outLog(self.__class__.__name__, "cur dir: " + curDir)

        if curDir != link:
            outErr(self.__class__.__name__, "can't go to " + link)
            return False
        return True

    def getTags(self):
        outLog(self.__class__.__name__, "get tags")

        (out, err) = runCmd(common.GET_TAGS)

        if err:
            outErr(self.__class__.__name__, err)

        return out

    def getSHash(self, tagStr):
        (out, err) = runCmd(common.GET_TAG_SSHA + tagStr)

        if err:
            outErr(self.__class__.__name__, err)

        return out

    def getCommDateBySHash(self, hash):
        (out, err) = runCmd(common.GET_COMM_DATE + hash)

        if err:
            outErr(self.__class__.__name__, err)

        return out

    def isTagValid(self, tag):
        for inc in common.PROD:
            if inc in tag:
                return True

        return False

    def genNoteByTag(self, tag):
        parts = tag.split("/")

        note = Note()

        if len(parts) < 3:
            return note

        note.name = parts[1]

        date = ""
        if len(parts) == 3:
            date = self.doRepairDate(parts[2])
        elif len(parts) == 4:
            note.type = parts[2].split("-")[:-1][0]
            note.num = int(parts[2].split("-")[-1:][0])
            date = self.doRepairDate(parts[3])

        if not date:
            outErr(self.__class__.__name__, "Bad tag: " + tag)
            return note
        elif date:
            note.date = date

        note.sHash = self.getSHash(tag)

        note.commDate = self.getCommDateBySHash(note.sHash)

        note.tag = tag

        note.author = self.getCommAuthorByHash(note.sHash)

        note.valid = True

        return note

    def getCommAuthorByHash(self, hash):
        (out, err) = runCmd(common.GET_COMM_INFO.format(common.GIT_AUTHOR_NEST, common.FORM_AUTHOR) + hash)

        if err:
            outErr(self.__class__.__name__, err)

        return out

    def doRepairDate(self, date):
        temp = date.split("-")

        res = ""

        try:
            res += temp[0] + "-" + temp[1] + "-" + temp[2] + " "
            res += temp[3][0] + temp[3][1] + ":" + temp[3][2] + temp[3][3]
        except Exception:
            outErr(self.__class__.__name__, "Bad date: " + date)

        return res

    def doDirtyJob(self, model):
        # create time checker
        timeCh = TimeChecker()
        timeCh.start()

        # do work
        deps = model.getDeps()

        for dep, repos in deps.items():
            outLog(self.__class__.__name__, dep)
            for repo in repos:
                link = repo.getLink()
                outLog(self.__class__.__name__, "Work with repo: " + link)
                # try go to dir link
                self.goToDir(link)
                if self.isDirExist(link):
                    # check branch
                    self.checkBranch()

                    # update if need
                    if self.update:
                        self.updateRepo()

                    # do dirty work
                    tags = self.getTags()

                    if tags:
                        for tag in tags.split("\n"):
                            if self.isTagValid(tag):
                                outLog(self.__class__.__name__, "Work with tag: " + tag)
                                note = self.genNoteByTag(tag)

                                if note.valid:
                                    if not note.name in repo.getDevices():
                                        dev = Device()
                                        dev.addToHistory(note)
                                        dev.setName(note.name)
                                        dev.setTrName(model.getMappedDevName(note.name))
                                        repo.addDeviceByName(note.name, dev)
                                    else:
                                        repo.addToDevice(note.name, note)

                        # sort notes for devices and separate last updates
                        for name, dev in repo.getDevices().items():
                            outLog(self.__class__.__name__, "Sort history for: " + name)
                            dev.sortHistory()
                            outLog(self.__class__.__name__, "Separate last notes for: " + name)
                            dev.fillLast()

                    # return last branch if need
                    if self.needReturnBranch:
                        self.returnBackBranch()

        timeCh.stop()

        outLog(self.__class__.__name__, timeCh.howMuchStr())