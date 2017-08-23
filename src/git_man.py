import os

import common
from tag_model import TagModel
from tag_model import Tag
from tag_model import Repo
from tag_model import Note
from tag_model import Device
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

    def createTag(self, tagStr):
        outLog(self.__class__.__name__, "cur tag create from: " + tagStr)

        tag = Tag()

        parts = tagStr.split("/")

        if len(parts) >= 4:
            tag.setOrderNum(parts[0])
            tag.setItemName(parts[1])
            tag.setItemNum(parts[2])
            tag.setDate(parts[3])
            tag.setValid(True)

        tag.setShortHash(self.getSHash(tagStr))

        return tag

    def getSHash(self, tagStr):
        outLog(self.__class__.__name__, "get short hash")

        (out, err) = runCmd(common.GET_TAG_SSHA + tagStr)

        if err:
            outErr(self.__class__.__name__, err)

        return out

    def getCommDateBySHash(self, hash):
        outLog(self.__class__.__name__, "get comm date")

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
            date = self.repairDate(parts[2])
        elif len(parts) == 4:
            note.type = parts[2].split("-")[:-1]
            note.num = int(parts[2].split("-")[-1:][0])
            date = self.repairDate(parts[3])

        if not date:
            outErr(self.__class__.__name__, "Bad tag: " + tag)
            return note
        elif date:
            note.date = date

        note.sHash = self.getSHash(tag)

        note.commDate = self.getCommDateBySHash(note.sHash)

        note.valid = True

        return note

    def repairDate(self, date):
        temp = date.split("-")

        res = ""

        try:
            res += temp[2] + "-" + temp[1] + "-" + temp[0] + " "
            res += temp[3][0] + temp[3][1] + ":" + temp[3][2] + temp[3][3]
        except Exception:
            outErr(self.__class__.__name__, "Bad date: " + date)

        return res

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
                    tags = self.getTags()

                    if tags:
                        for tag in tags.split("\n"):
                            if self.isTagValid(tag):
                                note = self.genNoteByTag(tag)

                                if note.valid:
                                    if not note.name in repo.devices:
                                        dev = Device()
                                        dev.history.append(note)
                                        repo.devices[note.name] = dev
                                    else:
                                        repo.devices[note.name].addNote(note)

                        # sort notes for devices and separate last updates
                        for name, dev in repo.devices.items():
                            dev.history = sorted(dev.history, key=lambda note: note.date, reverse=True)

                            lastDate = dev.history[0].date
                            for note in dev.history:
                                if note.date == lastDate:
                                    dev.last.append(note)



                    # if tags:
                    #     for tag in tags.split("\n"):
                    #         tagN = self.createTag(tag)
                    #         if tagN.valid:
                    #             repo.history.append(tagN)
                    #
                    #     repo.history = sorted(repo.history, key=lambda tag: tag.date, reverse=True)
                    #
                    #     # separate last tags
                    #     lastDate = repo.history[0].date
                    #     for tag in repo.history:
                    #         if tag.date == lastDate:
                    #             repo.last.append(tag)

                    # return last branch if need
                    if self.needReturnBranch:
                        self.returnBranch()