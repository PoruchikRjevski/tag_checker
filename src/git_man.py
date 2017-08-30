import os

import common
from tag_model import TagModel, Repo, Note, Device
from cmd_wrap import run_cmd
from logger import out_log, out_err
from time_checker import TimeChecker


class GitMan:
    def __init__(self):
        out_log(self.__class__.__name__, "init")
        self.update = False
        self.chDev = False
        self.lastBr = " "
        self.needReturnBranch = False

    def set_update_flag(self, update):
        self.update = update

    def set_ch_develop_flag(self, chDev):
        self.chDev = chDev

    def update_repo(self):
        (_, err) = run_cmd(common.UPD_REPO)

        out_log(self.__class__.__name__, "update repo")

        if err:
            out_err(self.__class__.__name__, err)

    def checkout_branch(self):
        branch = self.get_current_branch()
        out_log(self.__class__.__name__, "cur branch: " + branch)

        if branch != common.BR_DEV:
            self.lastBr = branch
            self.needReturnBranch = True
            self.switch_to_branch(common.BR_DEV)
            out_log(self.__class__.__name__, "cur branch: " + self.get_current_branch())

    def get_current_branch(self):
        (branch, _) = run_cmd(common.CUR_BRANCH)
        return branch

    def switch_to_branch(self, branch):
        out_log(self.__class__.__name__, "switch to branch: " + branch)
        run_cmd(common.SW_BRANCH.format(branch))

    def switch_back_branch(self):
        out_log(self.__class__.__name__, "return branch")
        out_log(self.__class__.__name__, "cur branch: " + self.get_current_branch())
        self.switch_to_branch(self.lastBr)
        self.needReturnBranch = False
        out_log(self.__class__.__name__, "cur branch: " + self.get_current_branch())

    # use module os for multiplatform
    def go_to_dir(self, link):
        out_log(self.__class__.__name__, "go to dir: " + link)
        os.chdir(link)

    def is_dir_exist(self, link):
        #curDir = os.getcwd()

        #if link[-1:] == "/" and not curDir[-1:] == "/":
        #    curDir = curDir + "/"
        #if not link[-1:] == "/" and curDir[-1:] == "/":
        #    curDir = curDir[:-1]

        #out_log(self.__class__.__name__, "cur dir: " + link)

        #if curDir != link:
        if not os.path.isdir(link):
            out_err(self.__class__.__name__, "can't find dir of repo: " + link)
            return False
        return True

    def get_tags(self):
        out_log(self.__class__.__name__, "get tags")

        (out, err) = run_cmd(common.GET_TAGS)

        if err:
            out_err(self.__class__.__name__, err)

        return out

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

    def is_tag_valid(self, tag):
        for inc in common.PROD:
            if inc in tag:
                return True

        return False

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
                note.num = int(prenum)
            else:
                out_err(self.__class__.__name__, "Bad tag item num: " + tag)

            date = self.do_repair_date(parts[3])

        if not date:
            out_err(self.__class__.__name__, "Bad tag: " + tag)
            return note
        elif date:
            note.date = date

        out_log(self.__class__.__name__, "Note type: " + note.type)
        out_log(self.__class__.__name__, "Note num: " + str(note.num))
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
        bs_sHash = self.get_branches_by_hash(note.sHash)
        out_log(self.__class__.__name__, "note's branches: " + bs_sHash)
        pHashes = self.get_parents_commmit_hash(note.commDate)
        out_log(self.__class__.__name__, "parents hashes: " + pHashes)

        for hash in pHashes.split('\n'):
            curBranches = self.get_branches_by_hash(hash)
            if bs_sHash in curBranches:
                note.pHash = hash
                break

        if note.pHash == -1:
            note.pHash = note.sHash

        #note.pHash = self.get_parents_commmit_hash(note.commDate)

        out_log(self.__class__.__name__, "Note pHash: " + str(note.pHash))

        note.valid = True

        return note

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

        # out_log(self.__class__.__name__, "date: " + date)
        # out_log(self.__class__.__name__, "cmd: " + cmd)
        #
        # (out, err) = run_cmd(cmd)
        #
        # out_log(self.__class__.__name__, out)
        #
        # if out:
        #     out = out.split('\n')[:-1][0]

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

    def scanning(self, model):
        out_log(self.__class__.__name__, "start scanning")

        # create time checker
        timeCh = TimeChecker()
        timeCh.start()

        # do work
        deps = model.get_departments()

        for dep, repos in deps.items():
            out_log(self.__class__.__name__, "department: " + dep)
            for repo in repos:
                link = repo.get_link()
                out_log(self.__class__.__name__, "repo: " + link)
                # try go to dir link
                self.go_to_dir(link)
                if self.is_dir_exist(link):
                    # check branch if need
                    if self.chDev:
                        self.checkout_branch()

                    # update if need
                    if self.update:
                        self.update_repo()

                    # do dirty work
                    tags = self.get_tags()

                    if tags:
                        for tag in tags.split("\n"):
                            if self.is_tag_valid(tag):
                                out_log(self.__class__.__name__, "tag: " + tag)
                                note = self.gen_note_by_tag(tag)

                                if note.valid:
                                    if not note.name in repo.get_devices():
                                        dev = Device()
                                        dev.add_item(note)
                                        dev.set_name(note.name)
                                        dev.set_mapped_name(model.get_mapped_device_name(note.name))
                                        repo.add_device_by_name(note.name, dev)
                                    else:
                                        repo.add_to_device(note.name, note)

                        # sort notes for devices and separate last updates
                        for name, dev in repo.get_devices().items():
                            out_log(self.__class__.__name__, "Sort history for: " + name)
                            dev.sort_items()
                            out_log(self.__class__.__name__, "Separate last notes for: " + name)
                            dev.fill_last()
                            out_log(self.__class__.__name__, "Count all items include for: " + name)
                            dev.count_items()
                    else:
                        out_err(self.__class__.__name__, "no tags")

                    # return last branch if need
                    if self.needReturnBranch:
                        self.switch_back_branch()

        timeCh.stop()

        out_log(self.__class__.__name__, timeCh.passed_time_str())