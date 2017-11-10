import multiprocessing
import os
import datetime
from multiprocessing.dummy import Pool as ThreadPool

import common_defs as c_d
import global_vars as g_v
import version as s_v
from cmd_executor.cmd_executor import *
from git_manager import git_defs as g_d
from logger_depr import *
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
        self.__cpus = 1
        self.__m_tasks = 1

    def __get_cpus(self):
        self.__cpus = multiprocessing.cpu_count()
        self.__m_tasks = self.__cpus

    def __is_dir_exist(self, link):
        if not os.path.isdir(link):
            out_err("can't find dir of repo: {:s}".format(link))
            return False
        return True

    def __go_to_dir(self, link):
        os.chdir(link)

    def __get_tags_with_fhash(self):
        cmd = g_d.GIT_CMD.format(g_d.A_SHOW_REF
                                 + g_d.A_TAGS)

        return run_cmd(cmd)

    def __is_tag_valid(self, tag):
        for inc in c_d.PROD:
            if inc in tag:
                return True

        return False

    def __get_tag_datetime_object(self, tag_date):
        splitted = tag_date.split(" ")

        cur_date_str = splitted[0].split("-")
        cur_time_str = None
        if len(splitted) > 1:
            cur_time_str = splitted[1].split(":")

        cur_datetime = None

        year = int(cur_date_str[0])
        month = int(cur_date_str[1])
        day = 1 if int(cur_date_str[2]) == 0 else int(cur_date_str[2])

        hour = 0
        minute = 0

        if not cur_time_str is None:
            hour = int(cur_time_str[0])
            minute = int(cur_time_str[1])

        cur_datetime = datetime.datetime(year, month, day, hour, minute)

        return cur_datetime

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
            if g_v.DEBUG: out_log("name: {:s}".format(item_out.dev_name))
        # W_ITEM
        elif state[0] == W_ITEM:
            parts = tag_part.split("-")
            item_out.item_type = parts[0]

            try:
                item_out.item_num = int(parts[1])
            except ValueError:
                out_err("EXCEPT Bad item num: {:s}".format(parts[1]))
                state[0] = W_BREAK
            else:
                if item_out.item_type not in c_d.TYPES_L:
                    out_err("Bad item type: {:s}".format(item_out.item_type))
                    state[0] = W_BREAK
                else:
                    if g_v.DEBUG:
                        out_log("type: {:s}".format(item_out.item_type))
                        out_log("num: {:s}".format(str(item_out.item_num)))
                state[0] = W_DATE
        # W_DATE
        elif state[0] == W_DATE:
            item_out.tag_date = self.__repair_tag_date(tag_part)

            if g_v.DEBUG: out_log("date: {:s}".format(item_out.tag_date))

            if item_out.tag_date == c_d.BAD_DATE:
                state[0] = W_BREAK
            else:
                state[0] = W_DOMEN
                item_out.tag_date_obj = self.__get_tag_datetime_object(item_out.tag_date)
                item_out.tag_date_ord = item_out.tag_date_obj.toordinal()
        # W_DOMEN
        elif state[0] == W_DOMEN:
            item_out.platform = tag_part
            if g_v.DEBUG: out_log("platform: {:s}".format(item_out.platform))

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

        return tag, run_cmd(cmd)

    def __repair_commit_msg(self, msg):
        size = len(msg)
        msg = msg[:c_d.COMMIT_MSG_SIZE]
        if size > c_d.COMMIT_MSG_SIZE:
            msg += " ..."
        return msg

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
                                 + g_d.A_FORMAT.format(g_d.AA_FHASH)
                                 + " " + branch)

        return run_cmd(cmd)

    def __get_parent_commit_hash(self, note_hash, last_commit_hash):
        cmd = g_d.GIT_CMD.format(g_d.A_LOG
                                 + g_d.A_FORMAT.format(g_d.AA_FHASH)
                                 + " " + note_hash + "..." + last_commit_hash
                                 + g_d.A_TAIL.format(str(c_d.GIT_PAR_SH_NEST)))

        out = run_cmd(cmd)

        if out is None:
            return None
        else:
            out = out.split("\n")[0]

        return out

    def __get_parent_commit_hash_in_dev_branch(self, note_hash, branch, date):
        cmd = g_d.GIT_CMD.format(g_d.A_LOG
                                 + g_d.A_FORMAT.format(g_d.AA_SHASH)
                                 + " " + note_hash + "..." + branch
                                 + g_d.A_TAIL.format(str(c_d.GIT_PAR_SH_NEST))
                                 + g_d.A_HEAD.format(str(c_d.GIT_AUTHOR_DEEP)))

        out = run_cmd(cmd)

        return out

    def __get_parents_short_hash(self, note_hash, date):
        branch = self.__get_develop_branch_by_hash(note_hash)
        if g_v.DEBUG: out_log("finded branch: {:s}".format(str(branch)))
        if branch is None:
            return -1

        last_commit_s_hash = self.__get_last_commit_on_branch(branch)
        if g_v.DEBUG: out_log("last commit short hash: {:s}".format(str(last_commit_s_hash)))
        if last_commit_s_hash is None:
            return -1

        parents_hash = self.__get_parent_commit_hash(note_hash, last_commit_s_hash)
        # parents_hash = self.__get_parent_commit_hash_in_dev_branch(note_hash, branch, date)
        if g_v.DEBUG: out_log("parent's hash: {:s}".format(str(parents_hash)))
        if parents_hash is None or not parents_hash:
            return -1
        else:
            parents_hash = parents_hash.strip()
            if parents_hash:
                return parents_hash
            else:
                return -1

    def __get_dict_of_jumps_between_commits(self, hash_a, hashes):
        res_dict = {}

        for hash in hashes:
            cmd = g_d.GIT_CMD.format(g_d.A_REV_LIST
                                     + g_d.A_COUNT
                                     + " {:s}...{:s}".format(hash_a,
                                                             hash))

            out = run_cmd(cmd)

            jumps = 0
            try:
                jumps = int(out)
            except ValueError:
                out_err("EXCEPT Bad jumps between: {:s} and {:s} out: {:s}".format(hash_a,
                                                                                   hash,
                                                                                   out))
                jumps = -1

            res_dict[hash] = jumps

        return res_dict

    def __get_commit_info_by_hash(self, hash):
        cmd = g_d.GIT_CMD.format(g_d.A_LOG
                                 + g_d.A_NN.format(str(c_d.GIT_AUTHOR_DEEP))
                                 + g_d.A_PRETTY.format(g_d.A_P_FORMAT.format(g_d.AA_COMMIT_DATE + "&|"
                                                                             + g_d.AA_AUTHOR + "&|"
                                                                             + g_d.AA_COMMIT_MSG))
                                 + g_d.A_DATE.format(g_d.A_D_ISO)
                                 + " " + hash)

        answ = run_cmd(cmd).split("&|")

        cm_date = answ[0] if len(answ) >= 1 else ""
        cm_auth = answ[1] if len(answ) >= 2 else ""
        cm_mess = answ[2] if len(answ) >= 3 else ""

        return cm_date, cm_auth, cm_mess

    def __get_commit_info_for_all_tags(self):
        cmd = g_d.GIT_CMD.format(g_d.A_LOG
                                 + g_d.A_PRETTY.format(g_d.A_P_FORMAT.format(g_d.AA_FHASH + "&|"
                                                                             + g_d.AA_COMMIT_DATE + "&|"
                                                                             + g_d.AA_AUTHOR + "&|"
                                                                             + g_d.AA_COMMIT_MSG))
                                 + g_d.A_DATE.format(g_d.A_D_ISO)
                                 + g_d.A_TAGS
                                 + g_d.A_NO_WALK)

        return run_cmd(cmd)

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
                out_err("Bad date: {:s}".format(date))
                return c_d.BAD_DATE

        return res

    def __repair_commit_date(self, date):
        date_temp = date.split(" ")
        time_temp = date_temp[1].split(":")

        sh_res = ""

        try:
            sh_res = "{:s} {:s}:{:s}".format(date_temp[0],
                                             time_temp[0],
                                             time_temp[1])

            full_res = "{:s}-{:s}{:s}{:s}".format(date_temp[0],
                                                    time_temp[0],
                                                    time_temp[1],
                                                    time_temp[2])
        except Exception:
            out_err("Bad date: {:s}".format(date))

        return (sh_res, full_res)

    def __repair_tag_info(self, tag_info):
        if g_d.REFS_TAGS not in tag_info:
            return None, None

        temp = tag_info.split(" {:s}".format(g_d.REFS_TAGS))
        f_hash = temp[0] if len(temp) >= 1 else None
        tag = temp[1] if len(temp) >= 2 else None

        return tag, f_hash

    def __strict_f_hash(self, f_hash):
        return f_hash[:g_d.SHORT_HASH_SIZE] if len(f_hash) >= g_d.SHORT_HASH_SIZE else f_hash

    def __gen_item(self, tag_info):
        if g_v.DEBUG:
            out_log("Gen item for tag: {:s}".format(tag_info))

        item = Item()
        tag, f_hash = self.__repair_tag_info(tag_info)

        if tag is None or f_hash is None:
            return item

        item.tag = tag
        item.f_hash = f_hash

        if not self.__parce_tag(item):
            out_err("Bad tag: " + tag)
            return item

        item.valid = True

        return item

    def __gen_items(self, tags_list, repo_i):
        items_out = []

        if g_v.MULTITH and len(tags_list) >= self.__m_tasks:
            pool = ThreadPool(self.__cpus)

            items_out = pool.map(self.__gen_item, tags_list)

            pool.close()
            pool.join()
        else:
            for tag in tags_list:
                items_out.append(self.__gen_item(tag))

        items_out = [item for item in items_out if item.valid]

        for item in items_out:
            item.repo_i = repo_i

        return items_out

    def __get_commits_info(self, unic_hashes, repo_i):
        commits_out = []

        cm_tags_info = self.__get_commit_info_for_all_tags().split("\n")
        cm_tags_info_true = [cm_tag_info for cm_tag_info in cm_tags_info if cm_tag_info.split("&|")[0] in unic_hashes]

        for cm_tag_info in cm_tags_info_true:
            if g_v.DEBUG:
                out_log("Gen commit for: {:s}".format(cm_tag_info))

            separated = cm_tag_info.split("&|")
            raw_hash = separated[0] if len(separated) >= 1 else ""
            raw_date = separated[1] if len(separated) >= 2 else ""
            cm_auth = separated[2] if len(separated) >= 3 else ""
            raw_msg = separated[3] if len(separated) >= 4 else ""

            commit = CommitInfo()

            if not raw_hash or not raw_date or not cm_auth or not raw_msg:
                return commit

            commit.hash = self.__strict_f_hash(raw_hash)

            date = raw_date
            (sh_date, full_date) = self.__repair_commit_date(date)
            commit.date = sh_date
            commit.date_full = full_date
            commit.date_obj = datetime.datetime.strptime(sh_date, "%Y-%m-%d %H:%M")
            if g_v.DEBUG: out_log("item commit date: {:s}".format(commit.date))

            commit.auth = cm_auth
            if g_v.DEBUG: out_log("item author: {:s}".format(commit.auth))

            msg = raw_msg
            commit.msg = self.__repair_commit_msg(msg)
            if g_v.DEBUG: out_log("item commMsg: {:s}".format(commit.msg))

            commit.repo_i = repo_i

            # get pHash
            commit.p_hash = self.__get_parents_short_hash(commit.hash, commit.date)
            if commit.p_hash == -1:
                commit.p_hash = commit.hash
            else:
                commit.p_hash = self.__strict_f_hash(commit.p_hash)
            if g_v.DEBUG: out_log("item pHash: {:s}".format(str(commit.p_hash)))

            commit.valid = True

            commits_out.append(commit)

        return commits_out

    def __do_main_work(self, tags_list, commits, repo_i, full_update):
        self.__get_cpus()

        items_out = []

        # parce tags and gen items
        work_t = start()
        items_out = self.__gen_items(tags_list, repo_i)
        stop(work_t)
        if g_v.TIMEOUTS: out_log("Gen {:s} items by {:s} tags time: {:s}".format(str(len(items_out)),
                                                                                 str(len(tags_list)),
                                                                                 get_pass_time(work_t)))

        # strict commits hashes from
        for item in items_out:
            item.cm_hash = self.__strict_f_hash(item.f_hash)

        if full_update:
            # create helper lists
            work_t = start()
            unic_hashes = list(set([item.f_hash for item in items_out]))
            stop(work_t)
            if g_v.TIMEOUTS: out_log("Create helpers lists: {:s}".format(get_pass_time(work_t)))

            # get commits info
            work_t = start()
            commits_out = self.__get_commits_info(unic_hashes, repo_i)

            for commit in commits_out:
                commits.append(commit)

            stop(work_t)
            if g_v.TIMEOUTS: out_log("Get commits info: {:s}".format(get_pass_time(work_t)))

        return items_out

    def __get_base_items_list(self, items):
        if items:
            return [item for item in items if item.item_type == c_d.TYPE_ALL]

        return []

    def __get_max_item_by_tag_date(self, items):
        if items:
            return max(items, key=lambda item: item.tag_date_obj)

        return None

    def __get_min_item_by_tag_date(self, items):
        if items:
            return min(items, key=lambda item: item.tag_date_obj)

        return None

    def __get_steps_for_color_intensity(self, newer_date_obj, older_date_obj, def_color_steps):
        diff = newer_date_obj - older_date_obj

        if diff.days < def_color_steps:
            return def_color_steps
        else:
            return round((diff.days / def_color_steps) + 0.5)

    def __do_get_metrics(self, items, dep_obj):
        for dev_name, dev_updated in dep_obj.devices.items():
            for soft_t in dep_obj.soft_types:
                dev_s_items = [item for item in items if (item.dev_name == dev_name
                                                          and dep_obj.repos[item.repo_i][REPO_OBJECT].soft_type == soft_t
                                                          and item.cm_i < len(dep_obj.commits))]

                if not dev_s_items:
                    continue

                base_items = self.__get_base_items_list(dev_s_items)
                newer_base_item = self.__get_max_item_by_tag_date(self.__get_base_items_list(dev_s_items))
                newer_of_all_item = self.__get_max_item_by_tag_date(dev_s_items)
                older_item = self.__get_min_item_by_tag_date(dev_s_items)
                newer_version_date = None

                red_intense_steps = 1
                blue_intense_steps = 1

                unic_jumps_by_cm_hash = {}

                if not newer_base_item:
                    newer_base_item = newer_of_all_item

                if not newer_base_item:
                    continue

                newer_version_date = dep_obj.commits[newer_base_item.cm_i].date_obj

                red_intense_steps = self.__get_steps_for_color_intensity(newer_base_item.tag_date_obj,
                                                                         older_item.tag_date_obj,
                                                                         c_d.CLR_RED_STEPS)
                blue_intense_steps = self.__get_steps_for_color_intensity(newer_of_all_item.tag_date_obj,
                                                                          newer_base_item.tag_date_obj,
                                                                          c_d.CLR_BLUE_STEPS)

                # get jumps
                unic_hashes_list = list(set([item.cm_hash for item in dev_s_items]))
                unic_jumps_by_cm_hash = self.__get_dict_of_jumps_between_commits(newer_base_item.cm_hash,
                                                                                 unic_hashes_list)

                for item in dev_s_items:
                    item_i = dep_obj.items.index(item)
                    item_version_date = dep_obj.commits[item.cm_i].date_obj

                    if item.tag_date_obj < newer_base_item.tag_date_obj:
                        dep_obj.items[item_i].metric.old = True
                        dep_obj.items[item_i].metric.color_intensity = round(
                            ((newer_base_item.tag_date_obj - item.tag_date_obj).days / red_intense_steps) + 0.5)
                    elif item.tag_date_obj > newer_base_item.tag_date_obj:
                        if item_version_date > newer_version_date:
                            dep_obj.items[item_i].metric.exp = True
                            dep_obj.items[item_i].metric.color_intensity = round(
                                ((item.tag_date_obj - newer_base_item.tag_date_obj).days / blue_intense_steps) + 0.5)
                        elif item_version_date < newer_version_date:
                            dep_obj.items[item_i].metric.forced = True
                        else:
                            dep_obj.items[item_i].metric.last = True
                    else:
                        dep_obj.items[item_i].metric.last = True

                    if dep_obj.items[item_i].metric.exp:
                        dep_obj.items[item_i].metric.diff_d = item.tag_date_obj - newer_base_item.tag_date_obj
                    else:
                        dep_obj.items[item_i].metric.diff_d = newer_base_item.tag_date_obj - item.tag_date_obj

                    dep_obj.items[item_i].metric.jumps = unic_jumps_by_cm_hash[item.cm_hash]

    def scanning(self, model):
        if g_v.DEBUG: out_log("start scanning")

        for dep_name, dep_obj in model.departments.items():
            if g_v.DEBUG: out_log("department: \"{:s}\"".format(dep_name))

            g_v.REPOS_NUM = g_v.REPOS_NUM + len(dep_obj.repos)

            for repo in dep_obj.repos:
                repo_obj = repo[REPO_OBJECT]
                repo_update_flag = repo[UPDATE_FLAG]

                if g_v.DEBUG:
                    out_log("repo: \"{:s}\"".format(repo_obj.name))
                    out_log("repo-link: \"{:s}\"".format(repo_obj.link))
                    out_log("repo-soft-type: \"{:s}\"".format(repo_obj.soft_type))

                if self.__is_dir_exist(repo_obj.link):
                    self.__go_to_dir(repo_obj.link)

                tags = self.__get_tags_with_fhash()

                if tags:
                    tags_list = tags.split("\n")

                    g_v.TAGS_NUM = g_v.TAGS_NUM + len(tags_list)

                    if g_v.DEBUG:
                        out_log("Tags number: {:s}".format(str(len(tags_list))))

                    items_list = self.__do_main_work(tags_list,
                                                     dep_obj.commits,
                                                     dep_obj.repos.index(repo),
                                                     repo_update_flag)

                    g_v.PROC_TAGS_NUM += len(items_list)

                    for commit in dep_obj.commits:
                        for item in items_list:
                            if commit.repo_i == item.repo_i and commit.hash == item.cm_hash:
                                item.cm_i = dep_obj.commits.index(commit)

                    for item in items_list:
                        dep_obj.items.append(item)
                        if item.dev_name not in dep_obj.devices.keys():
                        # if not any(item.dev_name in d.keys() for d in dep_obj.devices):
                            dep_obj.devices[item.dev_name] = repo_update_flag
                            # dep_obj.devices.append({item.dev_name: repo_update_flag})

                    # do get metrics
                    if repo_update_flag:
                        metr_t = start()
                        self.__do_get_metrics(items_list, dep_obj)
                        stop(metr_t)
                        if g_v.TIMEOUTS: out_log("Metrics time: {:s}".format(get_pass_time(metr_t)))

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