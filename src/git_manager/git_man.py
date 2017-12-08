import multiprocessing
import os
import datetime
from multiprocessing.dummy import Pool as ThreadPool
import logging

import common_defs as c_d
import global_vars as g_v
import version as s_v
from cmd_executor.cmd_executor import *
from git_manager import git_defs as g_d
from tag_model import *
from time_profiler.time_checker import *
from logger import log_func_name

# parse state machine environment
W_START, W_DEVICE_CLASS, W_DEVICE_SELECTOR_TYPE_DETECTION, W_DEVICE_SELECTOR_TYPE, W_TIMESTAMP, W_DOMAIN, W_BREAK = range(7)
POS_TAG_CLASS, POS_DEVICE_CLASS, POS_DEVICE_SELECTOR_TYPE, POS_TIMESTAMP, POS_DOMAIN = range(5)
# true tag naming seq: P_TAG_CLASS/P_DEVICE_CLASS[/P_DEVICE_ITEM]/P_TIMESTAMP[/P_DOMAIN]

__all__ = ['GitMan']


logger = logging.getLogger("{:s}.GitMan".format(c_d.SOLUTION))


class GitMan:
    def __init__(self):
        self.__lastBranch = None
        self.__needReturnBranch = False
        self.__cpus = 1
        self.__m_tasks = 1

    def __get_cpus(self):
        self.__cpus = multiprocessing.cpu_count()
        self.__m_tasks = self.__cpus

    @staticmethod
    def __is_dir_exist(link):
        if not os.path.isdir(link):
            logger.error("can't find dir of repo: {:s}".format(link))
            return False
        return True

    @staticmethod
    def __go_to_dir(link):
        os.chdir(link)

    @staticmethod
    def __get_tags_with_fhash():
        cmd = g_d.GIT_CMD.format(g_d.A_SHOW_REF
                                 + g_d.A_TAGS)

        return run_cmd(cmd)

    @staticmethod
    def __is_tag_classified(tag):
        for inc in c_d.TAG_CLASSES:
            if inc in tag:
                return True

        return False

    @staticmethod
    def __get_tag_datetime_object(tag_date):
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

    @staticmethod
    def __parse_tag_state_machine(tag_part, pos, item_out, state):
        """Process one sub-item of tag, update state and return success or not.

        Keyword arguments:
        tag_part  -- [i]  tag sub-item
        pos       -- [i]  position of sub-item in tag name sequence
        item_out  -- [io] Item instance to hold parsed meta data
        state     -- [io] finite state machine state
        """
        if state[0] == W_DEVICE_SELECTOR_TYPE_DETECTION:   # must be resolved separately and in one step with next state
            parts = tag_part.split("-")
            if len(parts) == 2 and pos == POS_DEVICE_SELECTOR_TYPE:
                state[0] = W_DEVICE_SELECTOR_TYPE
            elif len(parts) >= 3 and pos >= POS_DEVICE_SELECTOR_TYPE:
                state[0] = W_TIMESTAMP
            else:
                logger.error("Parse error. Bad item num or date.")
                state[0] = W_BREAK

        # main processing
        if state[0] == W_START:
            if GitMan.__is_tag_classified(item_out.tag):
                item_out.tag_class = tag_part
                logger.info("tag class: {:s}".format(item_out.tag_class))
                state[0] = W_DEVICE_CLASS
            else:
                logger.info("tag is not classified => bypass")
                state[0] = W_BREAK
        elif state[0] == W_DEVICE_CLASS:
            item_out.device_class = tag_part
            state[0] = W_DEVICE_SELECTOR_TYPE_DETECTION
            logger.info("device class: {:s}".format(item_out.device_class))
        elif state[0] == W_DEVICE_SELECTOR_TYPE:
            parts = tag_part.split("-")
            item_out.device_selector_type = parts[0]

            try:
                item_out.device_selector_id = int(parts[1])
            except ValueError:
                logger.error("EXCEPT Bad device item num: {:s}".format(parts[1]))
                state[0] = W_BREAK
            else:
                if item_out.device_selector_type not in c_d.TAG_DEVICE_SELECTORS:
                    logger.error("Bad device selector type: {:s}".format(item_out.device_selector_type))
                    state[0] = W_BREAK
                else:
                    if g_v.DEBUG:
                        logger.info("type: {:s}".format(item_out.device_selector_type))
                        logger.info("num: {:s}".format(str(item_out.device_selector_id)))
                state[0] = W_TIMESTAMP
        elif state[0] == W_TIMESTAMP:
            item_out.tag_date = GitMan.__repair_tag_date(tag_part)

            logger.info("date: {:s}".format(item_out.tag_date))

            if item_out.tag_date == c_d.BAD_DATE:
                state[0] = W_BREAK
            else:
                state[0] = W_DOMAIN
                item_out.solution_domain = ""
                item_out.tag_date_obj = GitMan.__get_tag_datetime_object(item_out.tag_date)
                item_out.tag_date_ord = item_out.tag_date_obj.toordinal()
        # W_DOMAIN
        elif state[0] == W_DOMAIN:
            item_out.solution_domain = item_out.solution_domain + "." + tag_part
            logger.info("solution domain: {:s}".format(item_out.solution_domain))

        # end
        return state[0] != W_BREAK

    @staticmethod
    def __try_parse_tag(item):
        """Parse item tag to meta info.

        :param item: Item instance to hold all parsed tag data
        :return:     success or not
        """
        parse_t = start()
        logger.info("start parse tag")

        tag_parts = item.tag.split("/")

        if len(tag_parts) < 3:
            logger.error("tag size mismatch: {:s} => bypass".format(str(len(tag_parts))))
            return False

        state = [W_START]
        for part in tag_parts:
            if not GitMan.__parse_tag_state_machine(part, tag_parts.index(part), item, state):
                return False

        stop(parse_t)
        logger.info("parse tag time: {:s}".format(get_pass_time(parse_t)))

        return True

    @staticmethod
    def __get_short_hash(tag):
        cmd = g_d.GIT_CMD.format(g_d.A_REV_PARSE
                                 + g_d.A_SHORT
                                 + " " + tag)

        return tag, run_cmd(cmd)

    @staticmethod
    def __repair_commit_msg(msg):
        size = len(msg)
        msg = msg[:c_d.COMMIT_MSG_SIZE]
        if size > c_d.COMMIT_MSG_SIZE:
            msg += " ..."
        return msg

    @staticmethod
    def __find_develop_branch(branches):
        res = None

        if not isinstance(branches, list):
            b_tmp = [branches]
        else:
            b_tmp = branches

        for branch in b_tmp:
            if "HEAD" not in branch:
                if g_d.BRANCH_DEVELOP in branch:
                    res = branch
                    break
                else:
                    if not res:
                            res = branch

        if "* " in res:
            res = res.replace("* ", "")

        return res

    @staticmethod
    def __get_develop_branch_by_hash(hash):
        cmd = g_d.GIT_CMD.format(g_d.A_BRANCH
                                 + g_d.A_CONTAINS.format(hash) + " --all")

        out = run_cmd(cmd)

        out = GitMan.__find_develop_branch(out.split('\n'))

        return out

    @staticmethod
    def __get_last_commit_on_branch(branch):
        cmd = g_d.GIT_CMD.format(g_d.A_LOG
                                 + g_d.A_NN.format(str(c_d.GIT_AUTHOR_DEEP))
                                 + g_d.A_FORMAT.format(g_d.AA_FHASH)
                                 + " " + branch)

        return run_cmd(cmd).strip('"')

    @staticmethod
    def __get_parent_commit_hash(note_hash, last_commit_hash):
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

    @staticmethod
    def __get_parent_commit_hash_in_dev_branch(note_hash, branch, date):
        cmd = g_d.GIT_CMD.format(g_d.A_LOG
                                 + g_d.A_FORMAT.format(g_d.AA_SHASH)
                                 + " " + note_hash + "..." + branch
                                 + g_d.A_TAIL.format(str(c_d.GIT_PAR_SH_NEST))
                                 + g_d.A_HEAD.format(str(c_d.GIT_AUTHOR_DEEP)))

        out = run_cmd(cmd)

        return out

    @staticmethod
    def __get_parents_short_hash(note_hash, date):
        branch = GitMan.__get_develop_branch_by_hash(note_hash)
        logger.info("finded branch: {:s}".format(str(branch)))
        if branch is None:
            return -1

        last_commit_s_hash = GitMan.__get_last_commit_on_branch(branch)
        logger.info("last commit short hash: {:s}".format(str(last_commit_s_hash)))
        if last_commit_s_hash is None:
            return -1

        parents_hash = GitMan.__get_parent_commit_hash(note_hash, last_commit_s_hash)
        logger.info("parent's hash: {:s}".format(str(parents_hash)))
        if parents_hash is None or not parents_hash:
            return -1
        else:
            parents_hash = parents_hash.strip()
            if parents_hash:
                return parents_hash
            else:
                return -1

    @staticmethod
    def __get_dict_of_jumps_between_commits(hash_a, hashes):
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
                logger.error("EXCEPT Bad jumps between: {:s} and {:s} out: {:s}".format(hash_a,
                                                                                        hash,
                                                                                        out))
                jumps = -1

            res_dict[hash] = jumps

        return res_dict

    @staticmethod
    def __get_commit_info_by_hash(hash):
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

    @staticmethod
    def __get_commit_info_for_all_tags():
        cmd = g_d.GIT_CMD.format(g_d.A_LOG
                                 + g_d.A_PRETTY.format(g_d.A_P_FORMAT.format(g_d.AA_FHASH + "&|"
                                                                             + g_d.AA_COMMIT_DATE + "&|"
                                                                             + g_d.AA_AUTHOR + "&|"
                                                                             + g_d.AA_COMMIT_MSG))
                                 + g_d.A_DATE.format(g_d.A_D_ISO)
                                 + g_d.A_TAGS
                                 + g_d.A_NO_WALK)

        return run_cmd(cmd)

    @staticmethod
    def __is_numeric(part):
        try:
            int(part)
            return True
        except ValueError:
            return False

    @staticmethod
    def __repair_tag_date(date):
        temp = date.split("-")

        res = ""

        date = {0 : "1992", 1 : "06", 2 : "10", 3 : "00", 4 : "00"}

        time_exist = False

        if len(temp) >= 3:
            for p in temp:
                if temp.index(p) == 3:
                    break

                if GitMan.__is_numeric(p):
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
                logger.error("Bad date: {:s}".format(date))
                return c_d.BAD_DATE

        return res

    @staticmethod
    def __repair_commit_date(date):
        date_temp = date.split(" ")
        time_temp = date_temp[1].split(":")

        sh_res = ""
        full_res = ""

        try:
            sh_res = "{:s} {:s}:{:s}".format(date_temp[0],
                                             time_temp[0],
                                             time_temp[1])

            full_res = "{:s}-{:s}{:s}{:s}".format(date_temp[0],
                                                  time_temp[0],
                                                  time_temp[1],
                                                  time_temp[2])
        except Exception:
            logger.error("Bad date: {:s}".format(date))

        return sh_res, full_res

    @staticmethod
    def __repair_tag_info(tag_info):
        if g_d.REFS_TAGS not in tag_info:
            return None, None

        temp = tag_info.split(" {:s}".format(g_d.REFS_TAGS))
        commit_hash_full = temp[0] if len(temp) >= 1 else None
        tag = temp[1] if len(temp) >= 2 else None

        return tag, commit_hash_full

    @staticmethod
    def __strict_f_hash(commit_hash_full):
        return commit_hash_full[:g_d.SHORT_HASH_SIZE] if len(commit_hash_full) >= g_d.SHORT_HASH_SIZE else commit_hash_full

    @staticmethod
    def __gen_item(tag_info):
        logger.info("Gen item for tag: {:s}".format(tag_info))

        item = Item()
        tag, commit_hash_full = GitMan.__repair_tag_info(tag_info)

        if tag is None or commit_hash_full is None:
            return item

        item.tag = tag
        item.commit_hash_full = commit_hash_full

        if not GitMan.__try_parse_tag(item):
            logger.error("Tag is not classified: " + tag)
            return item

        item.valid = True

        return item

    def __gen_items(self, tags_list, repo_index):
        items_out = []

        if g_v.MULTITH and len(tags_list) >= self.__m_tasks:
            pool = ThreadPool(self.__cpus)

            items_out = pool.map(GitMan.__gen_item, tags_list)

            pool.close()
            pool.join()
        else:
            for tag in tags_list:
                items_out.append(GitMan.__gen_item(tag))

        items_out = [item for item in items_out if item.valid]

        for item in items_out:
            item.repo_index = repo_index

        return items_out

    @staticmethod
    def __get_commits_info(unic_hashes, repo_index):
        commits_out = []

        cm_tags_info = GitMan.__get_commit_info_for_all_tags().split("\n")
        for i in range(len(cm_tags_info)):
            cm_tags_info[i] = cm_tags_info[i].strip('"')
        cm_tags_info_true = [cm_tag_info for cm_tag_info in cm_tags_info if cm_tag_info.split("&|")[0].strip('"') in unic_hashes]

        for cm_tag_info in cm_tags_info_true:
            logger.info("Gen commit for: {:s}".format(cm_tag_info))

            separated = cm_tag_info.split("&|")
            raw_hash = separated[0] if len(separated) >= 1 else ""
            raw_date = separated[1] if len(separated) >= 2 else ""
            cm_auth = separated[2] if len(separated) >= 3 else ""
            raw_msg = separated[3] if len(separated) >= 4 else ""

            commit = CommitInfo()

            if not raw_hash or not raw_date or not cm_auth or not raw_msg:
                return commit

            commit.hash = GitMan.__strict_f_hash(raw_hash)

            date = raw_date
            (sh_date, full_date) = GitMan.__repair_commit_date(date)
            commit.date = sh_date
            commit.date_full = full_date
            commit.date_obj = datetime.datetime.strptime(sh_date, "%Y-%m-%d %H:%M")
            logger.info("item commit date: {:s}".format(commit.date))

            commit.auth = cm_auth
            logger.info("item author: {:s}".format(commit.auth))

            msg = raw_msg
            commit.msg = GitMan.__repair_commit_msg(msg)
            logger.info("item commMsg: {:s}".format(commit.msg))

            commit.repo_index = repo_index

            # get pHash
            commit.p_hash = GitMan.__get_parents_short_hash(commit.hash, commit.date)
            if commit.p_hash == -1:
                commit.p_hash = commit.hash
            else:
                commit.p_hash = GitMan.__strict_f_hash(commit.p_hash)
            logger.info("item pHash: {:s}".format(str(commit.p_hash)))

            commit.valid = True

            commits_out.append(commit)

        return commits_out

    @log_func_name(logger)
    def __do_main_work(self, tags_list, commits, repo_index, full_update):
        self.__get_cpus()

        items_out = []

        # parse tags and gen items
        work_t = start()
        items_out = self.__gen_items(tags_list, repo_index)
        stop(work_t)
        logger.info("Gen {:s} items by {:s} tags time: {:s}".format(str(len(items_out)),
                                                                                 str(len(tags_list)),
                                                                                 get_pass_time(work_t)))

        # strict commits hashes from
        for item in items_out:
            item.commit_hash_short = GitMan.__strict_f_hash(item.commit_hash_full)

        if full_update:
            # create helper lists
            work_t = start()
            unic_hashes = list(set([item.commit_hash_full for item in items_out]))
            stop(work_t)
            logger.info("Create helpers lists: {:s}".format(get_pass_time(work_t)))

            # get commits info
            work_t = start()
            commits_out = GitMan.__get_commits_info(unic_hashes, repo_index)

            for commit in commits_out:
                commits.append(commit)

            stop(work_t)
            logger.info("Get commits info: {:s}".format(get_pass_time(work_t)))

        return items_out

    @staticmethod
    def __get_base_items_list(items):
        if items:
            return [item for item in items if item.is_base_prod()]

        return []

    @staticmethod
    def __get_test_items_list(items):
        if items:
            return [item for item in items if item.is_base_test()]

        return []

    @staticmethod
    def __get_max_item_by_tag_date(items):
        if items:
            return max(items, key=lambda item: item.tag_date_obj)

        return None

    @staticmethod
    def __get_min_item_by_tag_date(items):
        if items:
            return min(items, key=lambda item: item.tag_date_obj)

        return None

    @staticmethod
    def __get_steps_for_color_intensity(newer_date_obj, older_date_obj, def_color_steps):
        diff = newer_date_obj - older_date_obj

        if diff.days < def_color_steps:
            return def_color_steps
        else:
            return round((diff.days / def_color_steps) + 0.5)

    @log_func_name(logger)
    def __do_get_metrics(self, items, dep_obj):
        for dev_name, dev_updated in dep_obj.devices.items():
            for soft_t in dep_obj.soft_types:
                dev_s_items = [item for item in items if (item.device_class == dev_name
                                                          and dep_obj.repos[item.repo_index][REPO_OBJECT].soft_type == soft_t
                                                          and item.commit_index < len(dep_obj.commits))]

                if not dev_s_items:
                    continue

                newer_base_item = GitMan.__get_max_item_by_tag_date(GitMan.__get_base_items_list(dev_s_items))
                newer_of_all_item = GitMan.__get_max_item_by_tag_date(dev_s_items)
                older_item = GitMan.__get_min_item_by_tag_date(dev_s_items)

                if not newer_base_item:
                    newer_base_item = newer_of_all_item

                if not newer_base_item:
                    continue

                newer_version_date = dep_obj.commits[newer_base_item.commit_index].date_obj

                red_intense_steps = GitMan.__get_steps_for_color_intensity(newer_base_item.tag_date_obj,
                                                                         older_item.tag_date_obj,
                                                                         c_d.CLR_RED_STEPS)
                blue_intense_steps = GitMan.__get_steps_for_color_intensity(newer_of_all_item.tag_date_obj,
                                                                          newer_base_item.tag_date_obj,
                                                                          c_d.CLR_BLUE_STEPS)

                # get jumps
                unic_hashes_list = list(set([item.commit_hash_short for item in dev_s_items]))
                unic_jumps_by_commit_hash = GitMan.__get_dict_of_jumps_between_commits(newer_base_item.commit_hash_short,
                                                                                 unic_hashes_list)

                for item in dev_s_items:
                    item_i = dep_obj.items.index(item)
                    item_version_date = dep_obj.commits[item.commit_index].date_obj

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

                    dep_obj.items[item_i].metric.jumps = unic_jumps_by_commit_hash[item.commit_hash_short]

    @log_func_name(logger)
    def scanning(self, model):
        for dep_name, dep_obj in model.departments.items():
            logger.info("department: \"{:s}\"".format(dep_name))

            g_v.REPOS_NUM = g_v.REPOS_NUM + len(dep_obj.repos)

            for repo in dep_obj.repos:
                repo_obj = repo[REPO_OBJECT]
                repo_update_flag = repo[UPDATE_FLAG]

                logger.info("repo: \"{:s}\"".format(repo_obj.name))
                logger.info("repo-link: \"{:s}\"".format(repo_obj.link))
                logger.info("repo-soft-type: \"{:s}\"".format(repo_obj.soft_type))

                if not GitMan.__is_dir_exist(repo_obj.link):
                    logger.error("repo not exits: \"{:s}\"".format(repo_obj.link))
                    continue

                GitMan.__go_to_dir(repo_obj.link)

                tags = GitMan.__get_tags_with_fhash()

                if tags:
                    tags_list = tags.split("\n")

                    g_v.TAGS_NUM = g_v.TAGS_NUM + len(tags_list)

                    logger.info("Tags number: {:s}".format(str(len(tags_list))))

                    items_list = self.__do_main_work(tags_list,
                                                     dep_obj.commits,
                                                     dep_obj.repos.index(repo),
                                                     repo_update_flag)

                    g_v.PROC_TAGS_NUM += len(items_list)

                    for commit in dep_obj.commits:
                        for item in items_list:
                            if commit.repo_index == item.repo_index and commit.hash == item.commit_hash_short:
                                item.commit_index = dep_obj.commits.index(commit)

                    for item in items_list:
                        dep_obj.items.append(item)
                        if item.device_class not in dep_obj.devices.keys():
                            dep_obj.devices[item.device_class] = repo_update_flag

                    # do get metrics
                    if repo_update_flag:
                        metr_t = start()
                        self.__do_get_metrics(items_list, dep_obj)
                        stop(metr_t)
                        logger.info("Metrics time: {:s}".format(get_pass_time(metr_t)))
