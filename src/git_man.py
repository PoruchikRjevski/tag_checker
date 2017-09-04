import os

import multiprocessing
from threading import Thread
from queue import Queue

import common
import git_defs
from cmd_wrap import *
from tag_model import *
from logger import *
from time_checker import *


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
        cmd = git_defs.GIT_CMD.format(git_defs.A_REV_PARSE
                                      + git_defs.A_ABBREV.format(git_defs.A_RP_REF)
                                      + git_defs.REV_HEAD)
        out_log(self.__class__.__name__, "cmd: " + cmd)
        branch = run_cmd(cmd)

        out_log(self.__class__.__name__, "cur branch: " + branch)

        return branch

    def __switch_to_branch(self, branch):
        cmd = git_defs.GIT_CMD.format(git_defs.A_CHECKOUT.format(branch))

        out_log(self.__class__.__name__, "cmd: " + cmd)

        run_cmd(cmd)

    def __checkout_branch(self):
        branch = self.__get_current_branch()

        if branch != common.BR_DEV:
            self.lastBranch = branch
            self.needReturnBranch = True
            self.__switch_to_branch(common.BR_DEV)
            out_log(self.__class__.__name__, "cur branch: " + self.__get_current_branch())

    def __update_repo(self):
        cmd = git_defs.GIT_CMD.format(git_defs.A_PULL)

        out_log(self.__class__.__name__, "cmd: " + cmd)

        run_cmd(cmd)

    def __get_tags(self):
        cmd = git_defs.GIT_CMD.format(git_defs.A_TAG)

        out_log(self.__class__.__name__, "cmd: " + cmd)

        return run_cmd(cmd)

    def __is_tag_valid(self, tag):
        for inc in common.PROD:
            if inc in tag:
                return True

        return False

    def __switch_back_branch(self):
        out_log(self.__class__.__name__, "cur branch: " + self.__get_current_branch())

        self.__switch_to_branch(self.__lastBranch)
        self.__needReturnBranch = False

        out_log(self.__class__.__name__, "cur branch: " + self.__get_current_branch())

    def __parce_tag(self, note_out, t_logs, t_errs):
        tag_parts = note_out.tag.split("/")

        if len(tag_parts) < 3:
            return False

        note_out.name = tag_parts[1]

        t_logs.append(out_log_def(self.__class__.__name__, "Note name: " + note_out.name))

        date = ""
        if len(tag_parts) == 3:
            date = self.__repair_tag_date(tag_parts[2])
        elif len(tag_parts) == 4:
            prenum = tag_parts[2].split("-")[-1:][0]

            t_logs.append(out_log_def(self.__class__.__name__, "prenum: " + prenum))

            note_out.type = tag_parts[2].split("-")[:-1][0]

            if note_out.type not in common.TYPES_L:
                t_errs.append(out_err_def(self.__class__.__name__, "Bad item type: " + note_out.type))
                return False

            try:
                note_out.num = int(prenum)
            except ValueError:
                t_errs.append(out_err_def(self.__class__.__name__, "EXCEPT Bad item num: " + prenum))
                return False

            date = self.__repair_tag_date(tag_parts[3])

        if not date:
            return False
        elif date:
            note_out.date = date

        t_logs.append(out_log_def(self.__class__.__name__, "Note type: " + note_out.type))
        t_logs.append(out_log_def(self.__class__.__name__, "Note num: " + str(note_out.num)))
        t_logs.append(out_log_def(self.__class__.__name__, "Note date: " + note_out.date))

        return True

    def __get_short_hash(self, tag):
        cmd = git_defs.GIT_CMD.format(git_defs.A_REV_PARSE
                                      + git_defs.A_SHORT
                                      + " " + tag)

        # out_log(self.__class__.__name__, "cmd: " + cmd)

        return run_cmd(cmd)

    def __get_commit_date_by_short_hash(self, hash):
        cmd = git_defs.GIT_CMD.format(git_defs.A_LOG
                                      + git_defs.A_NN.format(str(1))
                                      + git_defs.A_PRETTY.format(git_defs.A_P_FORMAT.format(git_defs.AA_COMMIT_DATE))
                                      + git_defs.A_DATE.format(git_defs.A_D_ISO)
                                      + " " + hash)

        out_log(self.__class__.__name__, "cmd: " + cmd)

        return run_cmd(cmd)

    def __get_commit_author_by_short_hash(self, hash):
        cmd = git_defs.GIT_CMD.format(git_defs.A_LOG
                                      + git_defs.A_NN.format(str(common.GIT_AUTHOR_DEEP))
                                      + git_defs.A_FORMAT.format(git_defs.AA_AUTHOR)
                                      + " " + hash)

        # out_log(self.__class__.__name__, "cmd: " + cmd)

        return run_cmd(cmd)

    def __repair_commit_msg(self, msg):
        size = len(msg)
        msg = msg[:common.COMMIT_MSG_SIZE]
        if size > common.COMMIT_MSG_SIZE:
            msg == " ..."
        return msg

    def __get_commit_msg_by_short_hash(self, hash):
        cmd = git_defs.GIT_CMD.format(git_defs.A_LOG
                                      + git_defs.A_NN.format(str(common.GIT_AUTHOR_DEEP))
                                      + git_defs.A_FORMAT.format(git_defs.AA_COMMIT_MSG)
                                      + " " + hash)

        # out_log(self.__class__.__name__, "cmd: " + cmd)

        return run_cmd(cmd)

    def __find_develop_branche(self, branches):
        res = None

        for branch in [branches]:
            if git_defs.BRANCH_DEVELOP in branch:
                res = branch
                if "* " in res:
                    res = res.replace("* ", "")

                break

        return res

    def __get_develop_branch_by_hash(self, hash, t_logs):
        cmd = git_defs.GIT_CMD.format(git_defs.A_BRANCH
                                      + git_defs.A_CONTAINS.format(hash))

        t_logs.append(out_log_def(self.__class__.__name__, "cmd: " + cmd))

        out = run_cmd(cmd)

        out = self.__find_develop_branche(out)

        return out

    def __get_last_commit_on_branch(self, branch, t_logs):
        cmd = git_defs.GIT_CMD.format(git_defs.A_LOG
                                      + git_defs.A_NN.format(str(common.GIT_AUTHOR_DEEP))
                                      + git_defs.A_FORMAT.format(git_defs.AA_SHASH)
                                      + " " + branch)

        t_logs.append(out_log_def(self.__class__.__name__, "cmd: " + cmd))

        return run_cmd(cmd)

    def __get_parent_commit_hash(self, noteHash, lastCommHash, t_logs):
        cmd = common.GIT_CMD.format(common.GIT_REV_LIST.format(common.ABBREV_COMM
                                                               + noteHash + "..."
                                                               + lastCommHash
                                                               + " |"
                                                               + common.FORM_TAIL.format(str(common.GIT_PAR_SH_NEST))))

        t_logs.append(out_log_def(self.__class__.__name__, "cmd: " + cmd))

        out = run_cmd(cmd)

        if out is None:
            return None
        else:
            out = out.split("\n")[0]

        return out

    def __get_parents_short_hash(self, note_hash, t_logs):
        branch = self.__get_develop_branch_by_hash(note_hash, t_logs)
        # out_log(self.__class__.__name__, "finded branch: " + str(branch))
        if branch is None:
            return -1

        last_commit_s_hash = self.__get_last_commit_on_branch(branch, t_logs)
        # out_log(self.__class__.__name__, "last commit short hash: " + str(last_commit_s_hash))
        if last_commit_s_hash is None:
            return -1

        parents_hash = self.__get_parent_commit_hash(note_hash, last_commit_s_hash, t_logs)
        # out_log(self.__class__.__name__, "parent's hash: " + str(parents_hash))
        if parents_hash is None:
            return -1
        else:
            return parents_hash

    def __gen_notes_by_tag_list(self, tag_list, out_queue):
        for tag in tag_list:
            self.__gen_note_by_tag(tag, out_queue)

    def __gen_note_by_tag(self, tag, out_queue):
        t_logs = []
        t_errs = []

        t_logs.append(out_log_def(self.__class__.__name__, "Gen note for tag: " + tag))

        note = Note()
        note.tag = tag

        if not self.__parce_tag(note, t_logs, t_errs):
            t_errs.append(out_err_def(self.__class__.__name__, "Bad tag: " + tag))
            return False

        note.sHash = self.__get_short_hash(tag)
        t_logs.append(out_log_def(self.__class__.__name__, "Note short hash: " + note.sHash))

        note.commDate = self.__repair_commit_date(self.__get_commit_date_by_short_hash(note.sHash))
        # out_log(self.__class__.__name__, "Note commit date: " + note.commDate)
        t_logs.append(out_log_def(self.__class__.__name__, "Note commit date: " + note.commDate))

        note.author = self.__get_commit_author_by_short_hash(note.sHash)
        t_logs.append(out_log_def(self.__class__.__name__, "Note author: " + note.author))

        msg = self.__get_commit_msg_by_short_hash(note.sHash)
        note.commMsg = self.__repair_commit_msg(msg)
        t_logs.append(out_log_def(self.__class__.__name__, "Note commMsg: " + note.commMsg))

        # get pHash
        note.pHash = self.__get_parents_short_hash(note.sHash, t_logs)
        if note.pHash == -1:
            note.pHash = note.sHash
        t_logs.append(out_log_def(self.__class__.__name__, "Note pHash: " + str(note.pHash)))

        note.valid = True

        out_queue.logs = t_logs
        out_queue.errs = t_errs
        out_queue.notes.put(note)
        return True

    def __repair_tag_date(self, date):
        temp = date.split("-")

        res = ""

        try:
            res += temp[0] + "-" + temp[1] + "-" + temp[2] + " "
            res += temp[3][0] + temp[3][1] + ":" + temp[3][2] + temp[3][3]
        except Exception:
            out_err(self.__class__.__name__, "Bad date: " + date)

        return res

    def __repair_commit_date(self, date):
        temp = date.split(" ")
        timeT = temp[1].split(":")

        res = ""

        try:
            res += temp[0] + " " + timeT[0] + ":" + timeT[1]

            print(res)
        except Exception:
            out_err(self.__class__.__name__, "Bad date: " + date)

        return res

    def __add_note(self, model, repo, note):
        if note.name not in repo.devices:
            dev = Device()
            dev.add_order(note)
            dev.name = note.name
            dev.trName = model.get_mappedDevName(note.name)

            repo.add_device(note.name, dev)
        else:
            repo.add_to_device(note.name, note)

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

    @property
    def check_git_installed(self):
        out = run_cmd(git_defs.GIT_CMD.format(git_defs.A_VERSION))

        if "version" in str(out):
            return True

        return False

    def scanning(self, model):
        out_log(self.__class__.__name__, "start scanning")

        # create time checker
        time_ch = TimeChecker()
        int_time_ch = TimeChecker()
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
                    int_time_ch.start
                    tags = self.__get_tags()
                    int_time_ch.stop
                    out_log(self.__class__.__name__, "get all tags " + int_time_ch.passed_time_str)
                    out_log(self.__class__.__name__, "Tags number: " + str(len(tags.split("\n"))))

                    if tags:
                        tags_list = tags.split("\n")
                        n_queue = ThreadQueue()

                        if common.MULTITH:
                            cpu_s = multiprocessing.cpu_count()
                            out_log(self.__class__.__name__, "cpu count: " + str(cpu_s))

                            threads = []

                            if common.FETCH_C_MT:
                                len_tl = len(tags_list)
                                avg = len_tl/cpu_s
                                pos = 0
                                out_log(self.__class__.__name__, "avg: " + str(avg))
                                for n_t in range(cpu_s):
                                    len_tl -= avg
                                    last = len_tl/avg
                                    out_log(self.__class__.__name__, "last: " + str(last))
                                    out_log(self.__class__.__name__, "pos: " + str(pos))
                                    if last > 1:
                                        thread = Thread(target=self.__gen_notes_by_tag_list,
                                                        args=[tags_list[int(pos):int(pos+avg)],
                                                              n_queue])
                                        thread.start()
                                        threads.append(thread)
                                        # self.__gen_notes_by_tag_list(tags_list[int(pos):int(pos+avg)], n_queue)
                                        pos += avg
                                    else:
                                        thread = Thread(target=self.__gen_notes_by_tag_list,
                                                        args=[tags_list[int(pos):],
                                                              n_queue])
                                        thread.start()
                                        threads.append(thread)
                                        # self.__gen_notes_by_tag_list(tags_list[int(pos):], n_queue)
                            else:
                                for tag in tags.split("\n"):
                                    if self.__is_tag_valid(tag):
                                        thread = Thread(target=self.__gen_note_by_tag, args=[tag, n_queue])
                                        thread.start()
                                        threads.append(thread)

                            for res in threads:
                                res.join()
                                threads.remove(res)
                        else:
                            self.__gen_notes_by_tag_list(tags_list, n_queue)

                        n_queue.logs
                        n_queue.errs
                        while not n_queue.notes.empty():
                            note = n_queue.notes.get()

                            if note.valid:
                                self.__add_note(model, repo, note)

                        # sort notes for devices and separate last updates
                        int_time_ch.start
                        for dev_name, dev in repo.devices.items():
                            out_log(self.__class__.__name__, "Sort history for: " + dev_name)
                            dev.sort_orders()
                            out_log(self.__class__.__name__, "Separate last notes for: " + dev_name)
                            dev.fill_last()
                        int_time_ch.stop
                        out_log(self.__class__.__name__, "sort " + int_time_ch.passed_time_str)
                    else:
                        out_err(self.__class__.__name__, "no tags")

                    # return last branch if need
                    if self.needReturnBranch:
                        self.__switch_back_branch()

        time_ch.stop

        out_log(self.__class__.__name__, time_ch.passed_time_str)