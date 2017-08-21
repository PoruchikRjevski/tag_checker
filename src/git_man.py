

import common
from tag_model import TagModel
from tag_model import Tag
from tag_model import Repo
from cmd_wrap import runCmd

class GitMan:
    def __init__(self):
        self.update = False
        self.lastBr = " "
        self.needReturnBranch = False

    def setUpdate(self, update):
        self.update = update

    def updateRepo(self, link):
        out = runCmd("git --version")

        if str(out).__contains__("version"):
            return True

    def checkBranch(self):
        branch = self.curBranch()

        if branch != common.BR_DEV:
            self.lastBr = branch
            self.needReturnBranch = True
            self.switchBranch(common.BR_DEV)

    def curBranch(self):
        return runCmd(common.CUR_BRANCH)

    def switchBranch(self, branch):
        runCmd(common.SW_BRANCH + branch)

    def returnBranch(self):
        if self.returnBranch:
            self.switchBranch(self.lastBr)
            self.needReturnBranch = False

    def doDirtyJob(self, model):
        deps = model.getDepsKeys()

        for dep, repos in deps.items():
            for repo in repos:
                link = repo.getLink()
                runCmd(common.CD_TO + link)
                # check branch and try to switch
                self.checkBranch()
                # update branch


                # return last branch if need
                self.returnBranch()

                # find tags
                #if self.update:
                    #self.updateRepo(repo.getLink())




        #if self.update:

        #for dep, repos in deps.items():
        #    for repo in repos:


#                repo.show()

        # for even dep
        # for even repo
        # update or not
        # get all tags
        # fill tags