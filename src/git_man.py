import os

import multiprocessing
from multiprocessing.dummy import Pool as ThreadPool
from threading import Thread
from queue import Queue

import common_defs as c_d
import global_vars as g_v
import git_defs as g_d
from cmd_wrap import *
from tag_model import *
from logger import *
from time_checker import *

# parce state machine environment
W_START, W_DEV, W_OFFSET, W_ITEM, W_DATE, W_DOMEN, W_BREAK = range(7)
P_PROD, P_DEV, P_ITEM, P_DATE, P_PLATFORM = range(5)
# true tag seq: P_PROD/P_DEV/P_ITEM(?)/P_DATE/P_PLATFORM(?)


class GitMan:
    def __init__(self):
        if g_v.DEBUG: out_log("init")
        self.__lastBranch = None
        self.__needReturnBranch = False

    def __is_dir_exist(self, link):
        if not os.path.isdir(link):
            out_err("can't find dir of repo: " + link)
            return False
        return True

    def __go_to_dir(self, link):
        os.chdir(link)

    def __get_tags(self):
        cmd = g_d.GIT_CMD.format(g_d.A_TAG)

        return run_cmd(cmd)

    def __is_tag_valid(self, tag):
        for inc in c_d.PROD:
            if inc in tag:
                return True

        return False

    def __parce_tag_sm(self, tag_part, pos, note_out, state):
        # offset
        if state[0] == W_OFFSET:
            parts = tag_part.split("-")
            if len(parts) == 2 and pos == P_ITEM:
                state[0] = W_ITEM
            elif len(parts) == 4 and pos >= P_ITEM:
                state[0] = W_DATE
            else:
                state[0] = W_BREAK

        # main
        if state[0] == W_START:
            if self.__is_tag_valid(note_out.tag):
                if g_v.DEBUG: out_log("tag is valid")
                state[0] = W_DEV
            else:
                if g_v.DEBUG: out_log("tag is not valid")
                state[0] = W_BREAK
        elif state[0] == W_DEV:
            note_out.name = tag_part
            state[0] = W_OFFSET
            if g_v.DEBUG: out_log("name: " + note_out.name)
        elif state[0] == W_ITEM:
            parts = tag_part.split("-")
            note_out.type = parts[0]

            try:
                note_out.num = int(parts[1])
            except ValueError:
                out_err("EXCEPT Bad item num: " + parts[1])
                state[0] = W_BREAK
            else:
                if note_out.type not in c_d.TYPES_L:
                    out_err("Bad item type: " + note_out.type)
                    state[0] = W_BREAK
                else:
                    if g_v.DEBUG:
                        out_log("type: " + note_out.type)
                        out_log("num: " + str(note_out.num))

            state[0] = W_DATE
        elif state[0] == W_DATE:
            note_out.date = self.__repair_tag_date(tag_part)
            if g_v.DEBUG: out_log("date: " + note_out.date)

            state[0] = W_DOMEN
        elif state[0] == W_DOMEN:
            note_out.platform = tag_part
            if g_v.DEBUG: out_log("platform: " + note_out.platform)

        # end
        if state[0] == W_BREAK:
            return False
        else:
            return True

    def __parce_tag(self, note_out):
        timer = TimeChecker()
        timer.start

        if g_v.DEBUG: out_log("start parce tag")

        tag_parts = note_out.tag.split("/")

        if len(tag_parts) < 3:
            return False

        state = [W_START]
        for part in tag_parts:
            if not self.__parce_tag_sm(part, tag_parts.index(part), note_out, state):
                return False

        timer.stop
        if g_v.DEBUG: out_log("finish parce tag - " + timer.passed_time_str)

        return True

    def __get_short_hash(self, tag):
        cmd = g_d.GIT_CMD.format(g_d.A_REV_PARSE
                                 + g_d.A_SHORT
                                 + " " + tag)

        return run_cmd(cmd)

    def __get_commit_date_by_short_hash(self, hash):
        cmd = g_d.GIT_CMD.format(g_d.A_LOG
                                 + g_d.A_NN.format(str(1))
                                 + g_d.A_PRETTY.format(g_d.A_P_FORMAT.format(g_d.AA_COMMIT_DATE))
                                 + g_d.A_DATE.format(g_d.A_D_ISO)
                                 + " " + hash)

        return run_cmd(cmd)

    def __get_commit_author_by_short_hash(self, hash):
        cmd = g_d.GIT_CMD.format(g_d.A_LOG
                                 + g_d.A_NN.format(str(c_d.GIT_AUTHOR_DEEP))
                                 + g_d.A_FORMAT.format(g_d.AA_AUTHOR)
                                 + " " + hash)

        return run_cmd(cmd)

    def __repair_commit_msg(self, msg):
        size = len(msg)
        msg = msg[:c_d.COMMIT_MSG_SIZE]
        if size > c_d.COMMIT_MSG_SIZE:
            msg += " ..."
        return msg

    def __get_commit_msg_by_short_hash(self, hash):
        cmd = g_d.GIT_CMD.format(g_d.A_LOG
                                 + g_d.A_NN.format(str(c_d.GIT_AUTHOR_DEEP))
                                 + g_d.A_FORMAT.format(g_d.AA_COMMIT_MSG)
                                 + " " + hash)

        return run_cmd(cmd)

    def __find_develop_branche(self, branches):
        res = None

        b_tmp = None

        if not isinstance(branches, list):
            b_tmp = [branches]
        else:
            b_tmp = branches

        for branch in b_tmp:
            if g_d.BRANCH_DEVELOP in branch:
                res = branch
                if "* " in res:
                    res = res.replace("* ", "")

                break

        return res

    def __get_develop_branch_by_hash(self, hash):
        cmd = g_d.GIT_CMD.format(g_d.A_BRANCH
                                 + g_d.A_CONTAINS.format(hash))

        out = run_cmd(cmd)

        out = self.__find_develop_branche(out.split('\n'))

        return out

    def __get_last_commit_on_branch(self, branch):
        cmd = g_d.GIT_CMD.format(g_d.A_LOG
                                 + g_d.A_NN.format(str(c_d.GIT_AUTHOR_DEEP))
                                 + g_d.A_FORMAT.format(g_d.AA_SHASH)
                                 + " " + branch)

        return run_cmd(cmd)

    def __get_parent_commit_hash(self, note_hash, last_commit_hash):
        cmd = g_d.GIT_CMD.format(g_d.A_REV_LIST
                                 + g_d.A_ABBREV.format(g_d.A_AB_COMMIT)
                                 + " " + note_hash + "..." + last_commit_hash
                                 + g_d.A_TAIL.format(str(c_d.GIT_PAR_SH_NEST)))

        out = run_cmd(cmd)

        if out is None:
            return None
        else:
            out = out.split("\n")[0]

        return out

    def __get_parents_short_hash(self, note_hash):
        branch = self.__get_develop_branch_by_hash(note_hash)
        if g_v.DEBUG: out_log("finded branch: " + str(branch))
        if branch is None:
            return -1

        last_commit_s_hash = self.__get_last_commit_on_branch(branch)
        if g_v.DEBUG: out_log("last commit short hash: " + str(last_commit_s_hash))
        if last_commit_s_hash is None:
            return -1

        parents_hash = self.__get_parent_commit_hash(note_hash, last_commit_s_hash)
        if g_v.DEBUG: out_log("parent's hash: " + str(parents_hash))
        if parents_hash is None:
            return -1
        else:
            parents_hash = parents_hash.strip()
            if parents_hash:
                return parents_hash
            else:
                return -1

    def __gen_notes_by_tag_list(self, tag_list):
        notes = []

        for tag in tag_list:
            notes.append(self.__gen_note_by_tag(tag))

        return notes

    def __gen_note_by_tag(self, tag):
        timer = TimeChecker()
        timer.start

        res_flag = True

        if g_v.DEBUG: out_log("Gen note for tag: " + tag)

        note = Note()
        note.tag = tag

        if self.__parce_tag(note):
            note.sHash = self.__get_short_hash(tag)
            if g_v.DEBUG: out_log("Note short hash: " + note.sHash)

            note.commDate = self.__repair_commit_date(self.__get_commit_date_by_short_hash(note.sHash))
            if g_v.DEBUG: out_log("Note commit date: " + note.commDate)

            note.author = self.__get_commit_author_by_short_hash(note.sHash)
            if g_v.DEBUG: out_log("Note author: " + note.author)

            msg = self.__get_commit_msg_by_short_hash(note.sHash)
            note.commMsg = self.__repair_commit_msg(msg)
            if g_v.DEBUG: out_log("Note commMsg: " + note.commMsg)

            # get pHash
            note.pHash = self.__get_parents_short_hash(note.sHash)
            if note.pHash == -1:
                note.pHash = note.sHash
            if g_v.DEBUG: out_log("Note pHash: " + str(note.pHash))

            note.valid = True
        else:
            out_err("Bad tag: " + tag)
            res_flag = False

        timer.stop
        if g_v.DEBUG: out_log("Tag time: {:s}".format(timer.passed_time_str))

        if res_flag:
            return (res_flag, note)
        else:
            return (res_flag, None)

    def __repair_tag_date(self, date):
        temp = date.split("-")

        res = ""

        try:
            res = "{:s}-{:s}-{:s} {:s}:{:s}".format(temp[0],
                                                    temp[1],
                                                    temp[2],
                                                    temp[3][0:2],
                                                    temp[3][2:4])
        except Exception:
            out_err("Bad date: " + date)

        return res

    def __repair_commit_date(self, date):
        date_temp = date.split(" ")
        time_temp = date_temp[1].split(":")

        res = ""

        try:
            res = "{:s} {:s}:{:s}".format(date_temp[0],
                                          time_temp[0],
                                          time_temp[1])
        except Exception:
            out_err("Bad date: " + date)

        return res

    def __add_note(self, model, repo, note):
        if note.name not in repo.devices:
            dev = Device()
            dev.add_order(note)
            dev.name = note.name
            dev.trName = model.get_trDevName(note.name)

            repo.add_device(note.name, dev)
        else:
            repo.add_to_device(note.name, note)

    @property
    def check_git_installed(self):
        out = run_cmd(g_d.GIT_CMD.format(g_d.A_VERSION))

        if c_d.GIT_VER in str(out):
            return True

        return False

    def scanning(self, model):
        if g_v.DEBUG: out_log("start scanning")

        # create time checker
        time_ch = TimeChecker()
        int_time_ch = TimeChecker()
        time_ch.start

        # do work
        deps = model.departments

        for name, repos in deps.items():
            if g_v.DEBUG: out_log("department: " + name)

            for repo in repos:
                link = repo.link

                if g_v.DEBUG: out_log("repo: " + link)

                # try go to dir link
                self.__go_to_dir(link)

                if self.__is_dir_exist(link):
                    # do dirty work
                    int_time_ch.start
                    tags = self.__get_tags()
                    int_time_ch.stop

                    if g_v.DEBUG: out_log("get all tags " + int_time_ch.passed_time_str)

                    if tags:
                        tags_list = tags.split("\n")

                        if g_v.DEBUG:
                            if g_v.DEBUG:
                                out_log("Tags number: " + str(len(tags_list)))
                                out_log("Tags: " + str(tags_list))

                        notes_list = []

                        if g_v.MULTITH:
                            cpu_ths = multiprocessing.cpu_count()
                            if g_v.DEBUG: out_log("cpu count: " + str(cpu_ths))

                            pool = ThreadPool(cpu_ths)

                            notes_list = pool.map(self.__gen_note_by_tag, tags_list)

                            pool.close()
                            pool.join()
                        else:
                            notes_list = self.__gen_notes_by_tag_list(tags_list)

                        # add notes
                        for note_t in notes_list:
                            (flag, note) = note_t
                            if flag and note.valid:
                                self.__add_note(model, repo, note)

                        # sort notes for devices and separate last updates
                        int_time_ch.start
                        for dev_name, dev in repo.devices.items():
                            if g_v.DEBUG: out_log("Sort history for: " + dev_name)

                            dev.sort_orders()

                            if g_v.DEBUG: out_log("Separate last notes for: " + dev_name)

                            dev.fill_last()
                        int_time_ch.stop

                        if g_v.DEBUG: out_log("sort " + int_time_ch.passed_time_str)
                    else:
                        out_err("no tags")

        time_ch.stop

        out_log("finish scanning - " + time_ch.passed_time_str)