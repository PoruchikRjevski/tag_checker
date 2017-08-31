import os

import common
import git_defs
from cmd_wrap import *


from tag_model import TagModel, Repo, Note, Device
from logger import out_log, out_err
from time_checker import TimeChecker


class GitMan:
    def __init__(self):
        out_log(self.__class__.__name__, "init")
        self.__update = False
        self.__swDevelop = False
        self.__lastBranch = None
        self.__needReturnBranch = False

    def __is_dir_exist(self, link):
        if not os.path.isdir(link):
            out_err(self.__class__.__name__, "can't find dir of repo: " + link)
            return False
        return True

    def __go_to_dir(self, link):
        os.chdir(link)
        out_log(self.__class__.__name__, "go to dir: " + link)

    def __get_current_branch(self):
        branch = run_cmd(common.CUR_BRANCH)

        out_log(self.__class__.__name__, "cur branch: " + branch)

        return branch

    def __switch_to_branch(self, branch):
        out_log(self.__class__.__name__, "switch to branch: " + branch)
        run_cmd(common.SW_BRANCH.format(branch))

    def __checkout_branch(self):
        branch = self.__get_current_branch()

        if branch != common.BR_DEV:
            self.lastBranch = branch
            self.needReturnBranch = True
            self.__switch_to_branch(common.BR_DEV)
            out_log(self.__class__.__name__, "cur branch: " + self.__get_current_branch())

    def __update_repo(self):
        out_log(self.__class__.__name__, "update repo")
        run_cmd(common.UPD_REPO)

    def __get_tags(self):
        out_log(self.__class__.__name__, "get tags")

        return run_cmd(common.GET_TAGS)

    def __is_tag_valid(self, tag):
        for inc in common.PROD:
            if inc in tag:
                return True

        return False

    def __switch_back_branch(self):
        out_log(self.__class__.__name__, "return branch")
        out_log(self.__class__.__name__, "cur branch: " + self.__get_current_branch())

        self.__switch_to_branch(self.__lastBranch)
        self.__needReturnBranch = False

        out_log(self.__class__.__name__, "cur branch: " + self.__get_current_branch())

    @property
    def update(self):
        return self.__update

    @update.setter
    def update(self, update):
        self.__update = update

    @property
    def swDevelop(self):
        return self.__swDevelop

    @swDevelop.setter
    def swDevelop(self, develop):
        self.__swDevelop = develop

    @property
    def lastBranch(self):
        return self.__lastBranch

    @lastBranch.setter
    def lastBranch(self, last_branch):
        self.__lastBranch = last_branch

    @property
    def needReturnBranch(self):
        return self.__needReturnBranch

    @needReturnBranch.setter
    def needReturnBranch(self, flag):
        self.__needReturnBranch = flag










    def get_short_hash(self, tagStr):
        (out, err) = run_cmd(common.GET_TAG_SSHA.format(tagStr))

        if err:
            out_err(self.__class__.__name__, err)

        return out

    def get_commit_date_by_short_hash(self, hash):
        (out, err) = run_cmd(common.GET_COMM_DATE.format(hash))

        if err:
            out_err(self.__class__.__name__, err)

        return out


    def gen_note_by_tag(self, tag):
        out_log(self.__class__.__name__, "Gen note")
        parts = tag.split("/")

        note = Note()

        if len(parts) < 3:
            return note

        note.name = parts[1]

        out_log(self.__class__.__name__, "Note name: " + note.name)

        date = ""
        if len(parts) == 3:
            date = self.do_repair_date(parts[2])
        elif len(parts) == 4:
            prenum = parts[2].split("-")[-1:][0]

            out_log(self.__class__.__name__, "prenum: " + prenum)

            if prenum not in common.WRONG_NUM:
                note.type = parts[2].split("-")[:-1][0]
                note.cnt = int(prenum)
            else:
                out_err(self.__class__.__name__, "Bad tag item num: " + tag)

            date = self.do_repair_date(parts[3])

        if not date:
            out_err(self.__class__.__name__, "Bad tag: " + tag)
            return note
        elif date:
            note.date = date

        out_log(self.__class__.__name__, "Note type: " + note.type)
        out_log(self.__class__.__name__, "Note num: " + str(note.cnt))
        out_log(self.__class__.__name__, "Note date: " + note.date)

        note.sHash = self.get_short_hash(tag)

        out_log(self.__class__.__name__, "Note short hash: " + note.sHash)

        note.commDate = self.get_commit_date_by_short_hash(note.sHash)

        out_log(self.__class__.__name__, "Note commit date: " + note.commDate)

        note.tag = tag

        note.author = self.get_commit_author_by_short_hash(note.sHash)

        out_log(self.__class__.__name__, "Note author: " + note.author)

        note.commMsg = self.get_commit_msg_by_short_hash(note.sHash)
        commSz = len(note.commMsg)
        note.commMsg = note.commMsg[:common.COMMIT_MSG_SIZE]
        if commSz > common.COMMIT_MSG_SIZE:
            note.commMsg == " ..."

        out_log(self.__class__.__name__, "Note commMsg: " + note.commMsg)

        # get pHash
        note.pHash = self.get_parent_hash(note.sHash)
        if note.pHash == -1:
            note.pHash = note.sHash

        out_log(self.__class__.__name__, "Note pHash: " + str(note.pHash))

        note.valid = True

        return note

    def get_parent_hash(self, noteHash):
        branch = self.get_dev_branch_by_hash(noteHash)
        if not branch:
            return -1

        lastCommHash = self.get_last_commit_on_branch(branch)
        if not lastCommHash:
            return -1

        parent = self.get_parent_commit_hash(noteHash, lastCommHash)

        if not parent:
            return -1;
        else:
            return parent

    def get_parent_commit_hash(self, noteHash, lastCommHash):
        cmd = common.GIT_CMD.format(common.GIT_REV_LIST.format(common.ABBREV_COMM
                                                               + noteHash + "..."
                                                               + lastCommHash
                                                               + " |"
                                                               + common.FORM_TAIL.format(str(common.GIT_PAR_SH_NEST))))

        out_log(self.__class__.__name__, "cmd: " + cmd)

        (out, err) = run_cmd(cmd)

        out_log(self.__class__.__name__, "out: " + out)

        if out:
            out = out.split("\n")[0]

        out_log(self.__class__.__name__, "res: " + out)

        if err:
            out_err(self.__class__.__name__, err)

        return out

    def get_last_commit_on_branch(self, branch):
        cmd = common.GET_LAST_COMM.format(common.FORM_SHORT_HASH,
                                          branch)

        out_log(self.__class__.__name__, "cmd: " + cmd)

        (out, err) = run_cmd(cmd)

        out_log(self.__class__.__name__, "out: " + out)

        if err:
            out_err(self.__class__.__name__, err)

        return out

    def get_dev_branch_by_hash(self, hash):
        cmd = common.GET_B_CONT.format(hash)

        out_log(self.__class__.__name__, "cmd: " + cmd)

        (out, err) = run_cmd(cmd)

        out_log(self.__class__.__name__, "out: " + out)

        res = ""

        for br in [out]:
            if common.BR_DEV in br:
                res = br
                if "* " in res:
                    res = res.replace("* ", "")

                break

        out = res

        out_log(self.__class__.__name__, "res: " + out)

        if err:
            out_err(self.__class__.__name__, err)

        return out

    def get_branches_by_hash(self, hash):
        cmd = common.GET_B_CONT.format(hash)

        out_log(self.__class__.__name__, "cmd: " + cmd)

        (out, err) = run_cmd(cmd)

        if err:
            out_err(self.__class__.__name__, err)

        return out

    def get_parents_commmit_hash(self, date):
        cmd = common.GET_PAR_COMM_H.format(common.FORM_SHORT_HASH,
                                           common.FORM_SINCE.format(date)
                                           + common.NO_MERGES
                                           + " | "
                                           + common.FORM_TAIL.format(str(common.GIT_PAR_SH_NEST)))

        (out, err) = run_cmd(cmd)

        if err:
            out_err(self.__class__.__name__, err)

        return out

    def get_commit_author_by_short_hash(self, hash):
        (out, err) = run_cmd(common.GET_COMM_INFO.format("",
                                                         str(common.GIT_AUTHOR_NEST),
                                                         common.FORM_AUTHOR,
                                                         hash))

        if err:
            out_err(self.__class__.__name__, err)

        return out

    def get_commit_msg_by_short_hash(self, hash):
        (out, err) = run_cmd(common.GET_COMM_INFO.format("",
                                                         str(common.GIT_AUTHOR_NEST),
                                                         common.FORM_PAR_SUBJ,
                                                         hash))

        if err:
            out_err(self.__class__.__name__, err)

        return out

    def do_repair_date(self, date):
        temp = date.split("-")

        res = ""

        try:
            res += temp[0] + "-" + temp[1] + "-" + temp[2] + " "
            res += temp[3][0] + temp[3][1] + ":" + temp[3][2] + temp[3][3]
        except Exception:
            out_err(self.__class__.__name__, "Bad date: " + date)

        return res

    def check_git_installed(self):
        out = run_cmd(git_defs.GIT_CMD.format(git_defs.A_VERSION))

        if "version" in str(out):
            return True

        return False

    def scanning(self, model):
        out_log(self.__class__.__name__, "start scanning")

        # create time checker
        time_ch = TimeChecker()
        time_ch.start

        # do work
        deps = model.departments

        for name, repos in deps.items():
            out_log(self.__class__.__name__, "department: " + name)

            for repo in repos:
                link = repo.link
                out_log(self.__class__.__name__, "repo: " + link)

                # try go to dir link
                self.__go_to_dir(link)

                if self.__is_dir_exist(link):
                    # check branch if need
                    if self.swDevelop:
                        self.__checkout_branch()

                    # update if need
                    if self.update:
                        self.__update_repo()

                    # do dirty work
                    tags = self.__get_tags()

                    if tags:
                        for tag in tags.split("\n"):
                            if self.__is_tag_valid(tag):
                                out_log(self.__class__.__name__, "tag: " + tag)
                                note = self.gen_note_by_tag(tag)

                                if note.valid:
                                    if note.name not in repo.devices:
                                        dev = Device()
                                        dev.add_order(note)
                                        dev.name = note.name
                                        dev.trName = model.get_mappedDevName(note.name)

                                        repo.add_device(note.name, dev)
                                    else:
                                        repo.add_to_device(note.name, note)

                        # sort notes for devices and separate last updates
                        for dev_name, dev in repo.devices.items():
                            out_log(self.__class__.__name__, "Sort history for: " + dev_name)
                            dev.sort_orders()
                            out_log(self.__class__.__name__, "Separate last notes for: " + dev_name)
                            dev.fill_last()
                    else:
                        out_err(self.__class__.__name__, "no tags")

                    # return last branch if need
                    if self.needReturnBranch:
                        self.__switch_back_branch()

        time_ch.stop

        out_log(self.__class__.__name__, time_ch.passed_time_str)