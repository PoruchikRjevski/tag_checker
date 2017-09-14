import multiprocessing
import os
from multiprocessing.dummy import Pool as ThreadPool

import common_defs as c_d
import global_vars as g_v
import version as s_v
from cmd_wrap import *
from git_manager import git_defs as g_d
from logger import *
from tag_model import *
from time_profiler.time_checker import *

# parce state machine environment
W_START, W_DEV, W_OFFSET, W_ITEM, W_DATE, W_DOMEN, W_BREAK = range(7)
P_PROD, P_DEV, P_ITEM, P_DATE, P_PLATFORM = range(5)
# true tag seq: P_PROD/P_DEV/P_ITEM(?)/P_DATE/P_PLATFORM(?)

__all__ = ['GitMan']


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

    def __parce_tag_sm(self, tag_part, pos, item_out, state):
        # offset
        if state[0] == W_OFFSET:
            parts = tag_part.split("-")
            if len(parts) == 2 and pos == P_ITEM:
                state[0] = W_ITEM
            elif len(parts) >= 3 and pos >= P_ITEM:
                state[0] = W_DATE
            else:
                out_err("Parce error. Bad item num or date.")
                state[0] = W_BREAK

        # main
        # W_START
        if state[0] == W_START:
            if self.__is_tag_valid(item_out.tag):
                if g_v.DEBUG: out_log("tag is valid")
                state[0] = W_DEV
            else:
                if g_v.DEBUG: out_log("tag is not valid")
                state[0] = W_BREAK
        # W_DEV
        elif state[0] == W_DEV:
            item_out.dev_name = tag_part
            state[0] = W_OFFSET
            if g_v.DEBUG: out_log("name: " + item_out.dev_name)
        # W_ITEM
        elif state[0] == W_ITEM:
            parts = tag_part.split("-")
            item_out.item_type = parts[0]

            try:
                item_out.item_num = int(parts[1])
            except ValueError:
                out_err("EXCEPT Bad item num: " + parts[1])
                state[0] = W_BREAK
            else:
                if item_out.item_type not in c_d.TYPES_L:
                    out_err("Bad item type: " + item_out.item_type)
                    state[0] = W_BREAK
                else:
                    if g_v.DEBUG:
                        out_log("type: " + item_out.item_type)
                        out_log("num: " + str(item_out.item_num))
                state[0] = W_DATE
        # W_DATE
        elif state[0] == W_DATE:
            item_out.tag_date = self.__repair_tag_date(tag_part)
            if g_v.DEBUG: out_log("date: " + item_out.tag_date)

            state[0] = W_DOMEN
        # W_DOMEN
        elif state[0] == W_DOMEN:
            item_out.platform = tag_part
            if g_v.DEBUG: out_log("platform: " + item_out.platform)

        # end
        if state[0] == W_BREAK:
            return False
        else:
            return True

    def __parce_tag(self, items_out):
        parce_t = -1
        if g_v.DEBUG:
            parce_t = start()
            out_log("start parce tag")

        tag_parts = items_out.tag.split("/")

        if len(tag_parts) < 3:
            out_err("bad tag size: {:s}".format(str(len(tag_parts))))
            return False

        state = [W_START]
        for part in tag_parts:
            if not self.__parce_tag_sm(part, tag_parts.index(part), items_out, state):
                return False

        if g_v.DEBUG:
            stop(parce_t)
            out_log("parce tag time: {:s}".format(get_pass_time(parce_t)))

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
        items = []

        for tag in tag_list:
            items.append(self.__gen_note_by_tag(tag))

        return items

    def __gen_note_by_tag(self, tag):
        res_flag = True
        gen_t = -1

        if g_v.DEBUG:
            gen_t = start()
            out_log("Gen item for tag: " + tag)

        item = Item()
        item.tag = tag

        if self.__parce_tag(item):
            item.cm_hash = self.__get_short_hash(tag)
            if g_v.DEBUG: out_log("item short hash: " + item.cm_hash)

            item.cm_date = self.__repair_commit_date(self.__get_commit_date_by_short_hash(item.cm_hash))
            if g_v.DEBUG: out_log("item commit date: " + item.cm_date)

            item.cm_auth = self.__get_commit_author_by_short_hash(item.cm_hash)
            if g_v.DEBUG: out_log("item author: " + item.cm_auth)

            msg = self.__get_commit_msg_by_short_hash(item.cm_hash)
            item.cm_msg = self.__repair_commit_msg(msg)
            if g_v.DEBUG: out_log("item commMsg: " + item.cm_msg)

            # get pHash
            item.p_hash = self.__get_parents_short_hash(item.cm_hash)
            if item.p_hash == -1:
                item.p_hash = item.cm_hash
            if g_v.DEBUG: out_log("item pHash: " + str(item.p_hash))

            item.valid = True
        else:
            out_err("Bad tag: " + tag)
            res_flag = False

        if g_v.DEBUG:
            stop(gen_t)
            out_log("gen item time: {:s}".format(get_pass_time(gen_t)))

        if res_flag:
            return (res_flag, item)
        else:
            return (res_flag, None)

    def __is_numeric(self, part):
        try:
            int(part)
            return True
        except ValueError:
            return False

    def __repair_tag_date(self, date):
        temp = date.split("-")

        res = ""

        date = {0 : "1992", 1 : "06", 2 : "10", 3 : "00", 4 : "00"}

        time_exist = False

        if len(temp) >= 3:
            for p in temp:
                if temp.index(p) == 3:
                    break

                if self.__is_numeric(p):
                    date[temp.index(p)] = p
                else:
                    return c_d.BAD_DATE
            if len(temp) == 4:
                if len(temp[3]) == 4:
                    date[3] = temp[3][0:2]
                    date[4] = temp[3][2:4]
                    time_exist = True

            try:
                res = "{:s}-{:s}-{:s}".format(date[0],
                                               date[1],
                                               date[2])
                if time_exist:
                    res += " {:s}:{:s}".format(date[3],
                                               date[4])

            except Exception:
                out_err("Bad date: " + date)
                return c_d.BAD_DATE

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

    def __do_work(self, tags_list):
        items_out = []
        if g_v.MULTITH:
            cpu_ths = multiprocessing.cpu_count()
            if g_v.DEBUG: out_log("cpu count: " + str(cpu_ths))

            pool = ThreadPool(cpu_ths)

            items_out = pool.map(self.__gen_note_by_tag, tags_list)

            pool.close()
            pool.join()
        else:
            items_out = self.__gen_notes_by_tag_list(tags_list)

        return items_out

    @property
    def check_git_installed(self):
        out = run_cmd(g_d.GIT_CMD.format(g_d.A_VERSION))

        if c_d.GIT_VER in str(out):
            return True

        return False

    def scanning(self, model):
        if g_v.DEBUG: out_log("start scanning")

        for dep_name, dep_obj in model.departments.items():
            if g_v.DEBUG: out_log("department: \"{:s}\"".format(dep_name))
            for repo in dep_obj.repos:
                if g_v.DEBUG:
                    out_log("repo: \"{:s}\"".format(repo.name))
                    out_log("repo-link: \"{:s}\"".format(repo.link))
                    out_log("repo-soft-type: \"{:s}\"".format(repo.soft_type))

                if self.__is_dir_exist(repo.link):
                    self.__go_to_dir(repo.link)

                tags = self.__get_tags()

                if tags:
                    tags_list = tags.split("\n")

                    if g_v.DEBUG:
                        out_log("Tags number: " + str(len(tags_list)))
                        out_log("Tags: " + str(tags_list))

                    items_list = self.__do_work(tags_list)

                    # add items
                    for item_t in items_list:
                        (flag, item) = item_t
                        if flag and item.valid:
                            item.repo_i = dep_obj.repos.index(repo)
                            dep_obj.items.append(item)
                            if item.dev_name not in dep_obj.devices:
                                dep_obj.devices.append(item.dev_name)

        if g_v.DEBUG: out_log("stop scanning")

    def try_get_build_ver(self):
        cmd = g_d.GIT_CMD.format(g_d.A_REV_LIST
                                 + g_d.A_ALL
                                 + g_d.A_COUNT)

        out = run_cmd(cmd)

        try:
            out_int = int(out)
        except ValueError:
            s_v.V_BUILD = s_v.CURRENT
        else:
            s_v.V_BUILD = out
            out_log("change build version: {:s}".format(out))

        return