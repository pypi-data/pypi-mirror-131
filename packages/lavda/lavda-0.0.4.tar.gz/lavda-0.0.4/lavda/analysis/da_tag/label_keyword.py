# -*- coding: utf-8 -*-
# ----------------------------------------------
# purpose : 关键词规则匹配
# author : LGD
# create_time : 2021/2/2 09:57
# update_time : 2021/2/2 09:57
# copyright : Lavector
# ----------------------------------------------
import ahocorasick
from typing import List, Optional


class KeywordMark(object):
    """
    keyword rule中定义的特殊标记
    """
    # TODO 加减号可以一起使用，加减号没有方向，是双向的
    # 1个加号限制距离为7个字符，>1个加号则没有距离限制
    # 减号没有距离限制
    PLUS = "+"
    MINUS = "-"
    # 否定词标记可以出现在任何词前面，但也只能用在词前面，不能是词的组合，如小括号等
    # 否定词距离为5，没有方向限制
    NEG_YES = "@"  # 要否定词
    NEG_NO = "#"   # 不要否定词

    AND = "|"
    # 括号前面必须是加号、减号或空（即开头或结尾）
    BRACKET_LEFT = "("
    BRACKET_RIGHT = ")"


class KElem(object):
    def __init__(self, need_neg):
        self._need_neg = need_neg

    @property
    def need_neg(self):
        return self._need_neg


class KItem(KElem):
    def __init__(self, k_str):
        if k_str.startswith(KeywordMark.NEG_YES):
            k_str = k_str.replace(KeywordMark.NEG_YES, "")
            self._neg_mark = KeywordMark.NEG_YES
        elif k_str.startswith(KeywordMark.NEG_NO):
            k_str = k_str.replace(KeywordMark.NEG_NO, "")
            self._neg_mark = KeywordMark.NEG_NO
        else:
            self._neg_mark = None
        self._k_str = k_str
        super(KItem, self).__init__(True if self._neg_mark is not None else False)

    @property
    def k_str(self):
        return self._k_str

    @property
    def neg_mark(self):
        return self._neg_mark

    @property
    def to_string(self):
        return self._k_str


class KRule(KElem):
    def __init__(self, master, p_slave, m_slave, rule_str=None):
        """

        :param master: string or KRule， 主索引词
        :param p_slave: list(KItem or KRule), 条件词
        :param m_slave: list(KItem or KRule), 条件词
        :param rule_str: string, 规则字符串

        """
        if KeywordMark.NEG_YES in rule_str or KeywordMark.NEG_NO in rule_str:
            need_neg = True
        else:
            need_neg = False
        super(KRule, self).__init__(need_neg)

        self._master = master
        self._p_slave = p_slave
        self._m_slave = m_slave

        # 规则所对应的keyword id
        self._k_id = None

        # 规则id
        self._rule_id = None

        self._rule_str = rule_str

    @property
    def to_string(self):
        return self._rule_str

    @property
    def rule_str(self):
        return self._rule_str

    @property
    def rule_id(self):
        return self._rule_id

    @rule_id.setter
    def rule_id(self, value):
        self._rule_id = value

    @property
    def k_id(self):
        return self._k_id

    @k_id.setter
    def k_id(self, value):
        self._k_id = value

    def get_master_words(self):
        """
        获取master 的所有词
        :return:
        """
        return KRule.get_word(self._master)

    def get_slave_words(self):
        w_list = list()
        for item in self._p_slave:
            t_list = KRule.get_word(item)
            w_list.extend(t_list)
        for item in self._m_slave:
            t_list = KRule.get_word(item)
            w_list.extend(t_list)
        return w_list

    @staticmethod
    def get_word(rule_item):
        """

        :param rule_item: KItem or KRule
        :return:
        """
        if isinstance(rule_item, KItem):
            return [rule_item.k_str]
        else:
            # 由于只有两层构造，因此所有节点都是KItem
            w_list = list()
            w_list.append(rule_item.master.k_str)
            for item in rule_item.p_slave:
                w_list.extend(KRule.get_word(item))
            for item in rule_item.m_slave:
                w_list.extend(KRule.get_word(item))

            return w_list

    @property
    def master(self):
        return self._master

    @property
    def p_slave(self):
        return self._p_slave

    @property
    def m_slave(self):
        return self._m_slave


class NegWordFinder(object):
    def __init__(self):
        neg_word = ['不', "过于", '没有', '未必', '木有', '未能', '从未', '无法', '不会', '不怎么']
        neg_auto = ahocorasick.Automaton()
        for word in neg_word:
            neg_auto.add_word(word, word)
            neg_auto.make_automaton()
        self.neg_auto = neg_auto

    def find(self, content):
        """

        :param content:
        :return: 返回否定词位置索引信息
        """
        neg_pos_set = set()
        for item in self.neg_auto.iter(content):
            target_last_index = item[0]
            target_word = item[-1]
            end = target_last_index + 1
            start = end - len(target_word)
            pos_list = list(range(start, end))
            neg_pos_set.update(pos_list)

        return neg_pos_set


class KRuleParser(object):
    """
    keyword 规则解析器
    """
    # 匹配方向
    DIRECTION_RIGHT = 'right'
    DIRECTION_LEFT = "left"
    DIRECTION_BOTH = "both"

    EXCLUDE_CH = {",", '，', '。',  ':', '：', '！', '?', '？'}

    def __init__(self, kid2keyword: dict, build_neg_model=False):
        """

        :param kid2keyword: dict, id -> keyword 字符串
                        eg: {1: "(中国+完成)-(重要+事情)-知道吗|中华"}
        """
        self.kid2keyword = kid2keyword
        # 1.解析规则
        kid2rules = {k_id: None for k_id in kid2keyword}
        rule_id_dict = dict()

        for k_id in kid2keyword:
            rule_list = self.parse_rule_from_keyword(kid2keyword[k_id])
            for i, cur_rule in enumerate(rule_list):
                cur_rule.k_id = k_id
                cur_rule.rule_id = str(k_id) + "-" + str(i+1)
                rule_id_dict[cur_rule.rule_id] = cur_rule
            kid2rules[k_id] = rule_list

        # 2.获取所有的词
        # master词和slave词分开创建也以减少不需要的查找，因为多数标签只有master words或没有master words
        all_master_words = list()
        all_slave_words = list()
        mater_word_rule_dict = dict()
        for k_id in kid2rules:
            k_rules = kid2rules[k_id]
            for one_rule in k_rules:
                master_words = one_rule.get_master_words()
                all_master_words.extend(master_words)

                slave_words = one_rule.get_slave_words()
                all_slave_words.extend(slave_words)
                # TODO 暂时只取master第一个词作为索引词
                if len(master_words) > 1:
                    all_slave_words.extend(master_words[1:])
                master_first_word = master_words[0]
                if master_first_word not in mater_word_rule_dict:
                    mater_word_rule_dict[master_first_word] = set()
                mater_word_rule_dict[master_first_word].add(one_rule.rule_id)

        # 3.构建词典存储结构
        master_auto = ahocorasick.Automaton()
        for word in mater_word_rule_dict:
            word_rules = [rule_id_dict[r_id] for r_id in mater_word_rule_dict[word]]
            master_auto.add_word(word, (word, word_rules))
        master_auto.make_automaton()
        self.master_auto = master_auto

        slave_auto = ahocorasick.Automaton()
        for word in all_slave_words:
            slave_auto.add_word(word, word)
            slave_auto.make_automaton()
        self.slave_auto = slave_auto

        # 4.否定词查找模型
        if build_neg_model:
            self.neg_model = NegWordFinder()
        else:
            self.neg_model = None

    def parse(self, content,
              return_all=False,
              neg_pos_set=None,
              direction="both",
              plus_max_len=7,
              neg_max_len=5,
              minus_max_range=7,
              merge_keyword=True):
        """

        :param content:
        :param return_all: bool， 是否返回所有匹配结果
        :param neg_pos_set: set, 否定词位置序列
        :param direction: string, 搜索匹配方向
        :param plus_max_len: int, 加号控制距离
        :param neg_max_len: int, 否定词控制距离
        :param minus_max_range: int, 减号作用范围，双向控制，分别向目标词左、右各扩展 minux_max_range 的内容
        :param merge_keyword: bool, 是否合并keyword result，因为一个keyword一个位置附近可能匹配到多个asect词
                                True:合并这些keyword，取最长的
                                False：不合并
        :return:
            eg: [{"aspect": "中国", 'start': 0, 'end': 3, 'keyword': 中国, 'kid': 1}]
        """
        if len(content) <= 0:
            return None

        # 1.先查找索引词
        master_search_list = list()
        slave_word_list = list()
        master_search_word_list = list()
        need_neg_flag = False
        for item in self.master_auto.iter(content):
            target_last_index = item[0]
            target_word, target_rules = item[-1]
            end = target_last_index + 1
            start = end - len(target_word)
            master_search_list.append((start, end, target_word, target_rules))
            master_search_word_list.append((start, end, target_word))

            for one_rule in target_rules:
                if not need_neg_flag and one_rule.need_neg:
                    need_neg_flag = True
                slave_words = one_rule.get_slave_words()
                slave_word_list.extend(slave_words)
                master_words = one_rule.get_master_words()
                # TODO 暂时只取第一个词以外的词，第一个词已经作为索引词了
                if len(master_words) > 1:
                    slave_word_list.extend(master_words[1:])
        # 去重
        slave_word_list = list(set(slave_word_list))

        # 2.查找限定词/条件词
        slave_search_word_list = list()
        if len(slave_word_list) > 0:
            # 查找slave word
            tmp_slave_auto = ahocorasick.Automaton()
            for word in slave_word_list:
                tmp_slave_auto.add_word(word, word)
                tmp_slave_auto.make_automaton()
            slave_search_word_list = self.search_from_automaton(tmp_slave_auto, content)
        search_word_list = master_search_word_list + slave_search_word_list

        # 3.生成总的 word->位置 词典
        word_pos_dict = dict()
        for start, end, word in search_word_list:
            if word not in word_pos_dict:
                word_pos_dict[word] = set()
            word_pos_dict[word].add((start, end))

        # 排序
        for word in word_pos_dict:
            # 排序，从左往右
            sort_result = sorted(list(word_pos_dict[word]), key=lambda x: x[0])
            word_pos_dict[word] = sort_result

        # 4.检查是否需要查看否定词
        if need_neg_flag:
            if neg_pos_set is None:
                if self.neg_model is not None:
                    neg_pos_set = self.neg_model.find(content)
        if neg_pos_set is None:
            neg_pos_set = set()

        # 4.匹配
        kid_result_dict = dict()
        for start, end, target_word, target_rules in master_search_list:
            # TODO 不同的rule可能有相同的rule_str，因此需要减少不必要的计算量
            cache_rule_str_dict = dict()
            for one_rule in target_rules:
                kid = one_rule.k_id
                # 不需要查找所有时，只要匹配到一个词即可返回
                if not return_all and kid in kid_result_dict:
                    continue
                cur_rule_str = one_rule.rule_str
                if cur_rule_str in cache_rule_str_dict:
                    one_result = cache_rule_str_dict[cur_rule_str]
                else:
                    if direction == self.DIRECTION_BOTH:
                        # TODO,双向匹配时，优先使用向右匹配，无法命中时，再向左匹配
                        one_result = self.match(content, target_word, start, end, one_rule, word_pos_dict, neg_pos_set, self.DIRECTION_RIGHT, plus_max_len, neg_max_len, minus_max_range)
                        if one_result is None:
                            one_result = self.match(content, target_word, start, end, one_rule, word_pos_dict, neg_pos_set,
                                                    self.DIRECTION_LEFT, plus_max_len, neg_max_len, minus_max_range)

                    else:
                        one_result = self.match(content,target_word, start, end, one_rule, word_pos_dict, neg_pos_set, direction, plus_max_len, neg_max_len, minus_max_range)
                    cache_rule_str_dict[cur_rule_str] = one_result
                if one_result is None:
                    continue

                if kid not in kid_result_dict:
                    kid_result_dict[kid] = list()
                kid_result_dict[kid].append(one_result)

        # 5.消歧（一个Keyword的多个规则可能匹配到了多个词，因此要消歧,将一个keyword的所有数据汇总消歧）
        k_word_result = list()
        for kid in kid_result_dict:
            k_keyword = self.kid2keyword[kid]
            k_pos_list = kid_result_dict[kid]
            if len(k_pos_list) == 1:
                start, end = k_pos_list[0]
                target_content = content[start: end]
                item = {"aspect": target_content, 'start': start, 'end': end, 'keyword': k_keyword, 'kid': kid}
                k_word_result.append(item)
            else:
                # 以最后一们作为消歧依据，挑选最长的匹配
                if merge_keyword:
                    end_dict = dict()
                    for start, end in k_pos_list:
                        if end not in end_dict:
                            end_dict[end] = set()
                        end_dict[end].add(start)

                    for end in end_dict:
                        s_list = end_dict[end]
                        start = min(list(s_list))
                        target_content = content[start: end]
                        item = {"aspect": target_content, 'start': start, 'end': end, 'keyword': k_keyword, 'kid': kid}
                        k_word_result.append(item)
                else:
                    for start, end in k_pos_list:
                        target_content = content[start: end]
                        item = {"aspect": target_content, 'start': start, 'end': end, 'keyword': k_keyword, 'kid': kid}
                        k_word_result.append(item)

        return k_word_result

    def match(self, content: str,
              word: str,
              start: int,
              end: int,
              one_rule: KRule,
              word_pos_dict: dict,
              neg_pos_set: set,
              direction: str,
              plus_max_len: int,
              neg_max_len: int,
              minus_max_range: int) -> tuple:
        """
        :param content:string, 原始内容
        :param word:string,索引词
        :param start:int,索引词起始位置
        :param end:int,索引词起始位置
        :param one_rule:KRule, 目标规则
        :param word_pos_dict:dict, 所有查找词位置信息
        :param neg_pos_set:set, 否定词位置信息
        :param direction:string, 搜索匹配方向
        :param plus_max_len:int, 搜索匹配方向
        :param neg_max_len:int, 搜索匹配方向
        :return:tuple(start, end), 一条规则匹配到的目标词的起始位置信息
        """
        # 1. 检查减号（无方向、无距离(小括号还是有距离的))
        # if self.is_exist_minus_items(one_rule.m_slave, word_pos_dict, neg_pos_set, plus_max_len=plus_max_len, neg_max_len=neg_max_len):
        #     return None

        # 2.检查master 索引词
        select_word_list = list()
        first_word = {"word": word, "start": start, "end": end}
        select_word_list.append(first_word)

        # print(first_word, one_rule.rule_str)

        master = one_rule.master
        # 检查并判断master的索引词
        if isinstance(master, KItem):
            if not self.is_match_word_list([(start, end)], neg_pos_set, master.neg_mark, neg_max_len):
                return None
        else:
            first_kitem = master.master
            if not self.is_match_word_list([(start, end)], neg_pos_set, first_kitem.neg_mark, neg_max_len):
                return None

        # 3. 查找匹配其他词，如其他加号词，master索引词之外的词
        left_result = None
        right_result = None
        if direction == self.DIRECTION_RIGHT or direction == self.DIRECTION_BOTH:
            right_result = self.search_one_direction(start, end, one_rule, word_pos_dict, neg_pos_set, self.DIRECTION_RIGHT, plus_max_len, neg_max_len)

        if direction == self.DIRECTION_LEFT or direction == self.DIRECTION_BOTH:
            left_result = self.search_one_direction(start, end, one_rule, word_pos_dict, neg_pos_set, self.DIRECTION_LEFT, plus_max_len, neg_max_len)

        # TODO 结果可以为空，但不能为None
        if right_result is None and left_result is None:
            return None
        if right_result is not None:
            select_word_list.extend(right_result)
        if left_result is not None:
            select_word_list.extend(left_result)

        # 4.合并所有词找到最大组合范围
        target_pos_list = list()
        for item in select_word_list:
            target_pos_list.append(item['start'])
            target_pos_list.append(item['end'])

        target_start = min(target_pos_list)
        target_end = max(target_pos_list)

        # 5.减号距离判断
        if len(one_rule.m_slave) > 0:
            # m_left = target_start - minus_max_range
            # m_right = target_end + minus_max_range
            m_word_pos_dict = dict()
            for k_word in word_pos_dict:
                # TODO 构建减号词作用域范围，一般是候选目标词的一小段前后扩展
                if minus_max_range is not None:
                    m_value = [item for item in word_pos_dict[k_word] if self.get_pos_dis(target_start, target_end, item[0], item[1]) <= minus_max_range]
                else:
                    m_value = [item for item in word_pos_dict[k_word]]
                m_word_pos_dict[k_word] = m_value

            if self.is_exist_minus_items(one_rule.m_slave, m_word_pos_dict, neg_pos_set, plus_max_len=plus_max_len, neg_max_len=neg_max_len):
                return None

        # 6.过虑检查
        match_word = content[target_start: target_end]
        if self.is_filter(match_word):
            return None

        return target_start, target_end

    def is_filter(self, match_word):
        for ch in list(match_word):
            if ch in self.EXCLUDE_CH:
                return True
        # 中英点号特殊判断,有些英文字符就是使用点号分开的，如人名之类的，因此要排除的，不能一概作为标点符号进行处理
        return False

    def search_one_direction(self,
                             start: int,
                             end: int,
                             one_rule: KRule,
                             word_pos_dict: dict,
                             neg_pos_set: set,
                             direction: str,
                             plus_max_len: int,
                             neg_max_len: int):
        """
        根据指定的方向查找/匹配一个完整的规则模式
        :param start:
        :param end:
        :param one_rule:
        :param word_pos_dict:
        :param neg_pos_set:
        :param direction:
        :param plus_max_len:
        :param neg_max_len:
        :return:
        """

        # 1.master 为组合词时需要查找另一个词
        master = one_rule.master
        select_word_list = list()
        if isinstance(master, KRule):
            second_kitem = master.p_slave[0]
            # master 是括号组合关系
            other_master_word = second_kitem.k_str
            near_word_result = self.get_near_word(start,
                                                  end,
                                                  other_master_word,
                                                  second_kitem.neg_mark,
                                                  neg_pos_set,
                                                  word_pos_dict,
                                                  direction,
                                                  neg_max_len=neg_max_len,
                                                  max_len=plus_max_len)
            if near_word_result is None:
                return None
            select_word_list.append(near_word_result)

        # 2.检查加号词
        long_max_len = plus_max_len
        for item in one_rule.p_slave:
            if len(select_word_list) > 0:
                # 选用上一个词作为起始查找位置
                source_start = select_word_list[-1]['start']
                source_end = select_word_list[-1]['end']
            else:
                source_start = start
                source_end = end

            if isinstance(item, KItem):
                target_word_item = self.get_near_word(source_start, source_end, item.k_str, item.neg_mark, neg_pos_set, word_pos_dict, direction, neg_max_len=neg_max_len, max_len=long_max_len)
                if target_word_item is None:
                    return None
                select_word_list.append(target_word_item)
            else:
                i_kitem1 = item.master
                i_kitem2 = item.p_slave[0]

                group_result = self.get_near_group(source_start,
                                                   source_end,
                                                   i_kitem1.k_str,
                                                   i_kitem1.neg_mark,
                                                   i_kitem2.k_str,
                                                   i_kitem2.neg_mark,
                                                   neg_pos_set,
                                                   word_pos_dict,
                                                   direction=direction,
                                                   plus_max_len=plus_max_len,
                                                   neg_max_len=neg_max_len,
                                                   max_len=long_max_len)
                if group_result is None:
                    return None
                select_word_list.extend(group_result)

        return select_word_list

    def get_near_word(self, source_start: int,
                      source_end: int,
                      other_word: str,
                      other_word_neg_mark,
                      neg_pos_set,
                      word_pos_dict: dict,
                      direction="right",
                      neg_max_len=None,
                      max_len=None) -> dict:
        """
        根据源词位置找到最近的目标词，可能有方向和距离限制
        :param source_start:
        :param source_end:
        :param other_word:
        :param other_word_neg_mark:
        :param neg_pos_set:
        :param word_pos_dict:
        :param direction:
        :param neg_max_len:
        :param max_len:
        :return: dict
                eg: {"start": 11, "end": 13, 'word': '中国'}
        """
        if other_word not in word_pos_dict:
            return None

        # 3.找词并作距离判断
        may_pos_list = word_pos_dict[other_word]
        target = None
        if direction == self.DIRECTION_RIGHT:
            tmp_list = [item for item in may_pos_list if item[0] > source_start]
            if len(tmp_list) <= 0:
                return None
            # 选第一个
            for one_target in tmp_list:
                if max_len is not None:
                    dis = self.get_pos_dis(source_start, source_end, one_target[0], one_target[1])
                    if dis > max_len:
                        return None
                if not self.is_match_word_list([(one_target[0], one_target[1])], neg_pos_set, other_word_neg_mark, neg_max_len):
                    continue

                target = one_target
                break

        elif direction == self.DIRECTION_LEFT:
            tmp_list = [item for item in may_pos_list if item[0] < source_start]
            if len(tmp_list) <= 0:
                return None
            # 反转，从最后一个开始匹配
            tmp_list.reverse()
            for one_target in tmp_list:
                if max_len is not None:
                    dis = self.get_pos_dis(source_start, source_end, one_target[0], one_target[1])
                    if dis > max_len:
                        return None
                if not self.is_match_word_list([(one_target[0], one_target[1])], neg_pos_set, other_word_neg_mark, neg_max_len):
                    continue

                target = one_target
                break
        else:
            raise Exception("unsupport directionr for get_near_word")

        if target is None:
            return None

        item_result = {"start": target[0], "end": target[1], 'word': other_word}

        return item_result

    def get_near_group(self, source_start: int,
                       source_end: int,
                       word1: str,
                       word1_neg_mark: KeywordMark,
                       word2: str,
                       word2_neg_mark: KeywordMark,
                       neg_pos_set: set,
                       word_pos_dict: dict,
                       direction="right",
                       plus_max_len=None,
                       neg_max_len=None,
                       max_len=None):
        """
        找到距离 source_start, source_end最近的两个词
        TODO 只支持向左或向右查找
        :param source_start:
        :param source_end:
        :param word1:
        :param word1_neg_mark:
        :param word2:
        :param word2_neg_mark:
        :param word_pos_dict:
        :param neg_pos_set:
        :param direction:
        :param plus_max_len:
        :param neg_max_len:
        :param max_len:
        :return:
        """
        # TODO word_pos_dict 中的位置信息必须是排序好的
        if word1 not in word_pos_dict:
            return None
        if word2 not in word_pos_dict:
            return None

        if direction == self.DIRECTION_RIGHT:
            word1_pos_list = [item for item in word_pos_dict[word1] if item[0] >= source_start]

            for s1, e1 in word1_pos_list:
                # 检查否定词语
                if not self.is_match_word_list([(s1, e1)], neg_pos_set, word1_neg_mark, neg_max_len):
                    continue

                # 检查距离
                if max_len is not None:
                    dis = self.get_pos_dis(s1, e1, source_start, source_end)
                    if dis > max_len:
                        return None

                # 括号组内查找总是使用距离限制的
                target2_item = self.get_near_word(s1, e1, word2, word2_neg_mark, neg_pos_set, word_pos_dict, direction=direction, max_len=plus_max_len, neg_max_len=neg_max_len)
                if target2_item is None:
                    return None

                item1 = {"word": word1, "start": s1, 'end': e1}
                return item1, target2_item
        elif direction == self.DIRECTION_LEFT:
            word1_pos_list = [item for item in word_pos_dict[word1] if item[0] < source_start]
            # 要先反转，从最后一个开始向前查找
            word1_pos_list.reverse()
            for s1, e1 in word1_pos_list:
                # 检查否定词语
                if not self.is_match_word_list([(s1, e1)], neg_pos_set, word1_neg_mark, neg_max_len):
                    continue

                # 括号组内查找总是使用距离限制的
                target2_item = self.get_near_word(s1, e1, word2, word2_neg_mark, neg_pos_set, word_pos_dict, direction=direction, max_len=plus_max_len, neg_max_len=neg_max_len)
                if target2_item is None:
                    return None

                # 检查距离
                if max_len is not None:
                    dis = self.get_pos_dis(target2_item['start'], target2_item['end'], source_start, source_end)
                    if dis > max_len:
                        return None

                item1 = {"word": word1, "start": s1, 'end': e1}
                return item1, target2_item
        else:
            raise Exception("unsupport directionr for get_near_group")

        return None

    def get_pos_dis(self, start1, end1, start2, end2) -> int:
        """
        两个词的距离，有重叠时距离为0
        :param start1:
        :param end1:
        :param start2:
        :param end2:
        :return:
        """
        # TODO 这里的两词间距离，实际上是两个两个词间隔字符的数量
        # TODO 一个词的 end位置，其实是该词后面的一位，因此两前后两词的end和start位置相减，正是它们的间隔距离
        if start1 <= start2:
            first = end1
            last = start2
        else:
            first = end2
            last = start1

        # TODO 距离是指两个词的间隔
        dis = max(0, last-first+1)

        return dis

    def is_match_word_list(self, word_pos_list, neg_pos_set, neg_mark=None, neg_max_len=0):
        """
        TODO 匹配词语，否定词判断有问题的，因为可能多个word，有的前面有否定词，有的没有否定词
        :param word_pos_list: [(1, 2), (5, 9)]
        :param neg_pos_set: [3,4,5]
        :param neg_mark:
        :param neg_max_len:
        :return:
        """
        if len(word_pos_list) <= 0:
            return False
        if neg_mark is None:
            return True

        # 检查否定词
        has_neg = False
        for start, end in word_pos_list:
            # TODO 双向匹配
            target_pos = list(range(start-neg_max_len, start)) + list(range(end, end + neg_max_len))

            for i in target_pos:
                if i in neg_pos_set:
                    has_neg = True
                    break
            if has_neg:
                break

        if has_neg:
            if neg_mark == KeywordMark.NEG_YES:
                return True
            else:
                return False
        else:
            if neg_mark == KeywordMark.NEG_YES:
                return False
            else:
                return True

    def is_exist_minus_items(self, m_slave: list,
                             word_pos_dict: dict,
                             neg_pos_set: set,
                             plus_max_len: int,
                             neg_max_len: int):
        """
        检查 减号标记的词是否存在，存在则规则匹配失败
        :param m_slave:
        :param word_pos_dict:
        :param neg_pos_set:
        :param plus_max_len:
        :param neg_max_len:
        :return:
        """
        for item in m_slave:
            if isinstance(item, KItem):
                # TODO 存在即不失败
                if item.k_str in word_pos_dict and self.is_match_word_list(word_pos_dict[item.k_str], neg_pos_set, item.neg_mark, neg_max_len):
                    return True
            else:
                # 组合括号关系，应该只有两个词
                master_word = item.master.k_str
                slave_word = item.p_slave[0].k_str
                group_result = self.is_exist_group(master_word,
                                                   item.master.neg_mark,
                                                   slave_word,
                                                   item.p_slave[0].neg_mark,
                                                   word_pos_dict,
                                                   neg_pos_set,
                                                   neg_max_len,
                                                   plus_max_len)
                if group_result:
                    return True
        return False

    def is_exist_group(self, word1,
                       word1_neg_mark,
                       word2,
                       word2_neg_mark,
                       word_pos_dict,
                       neg_pos_set,
                       neg_max_len,
                       max_len=None) -> bool:
        """
        检查是否存在两个组合词 （小括号包起来的词）,不区分方向，找到一个即可以
        :param word1:
        :param word1_neg_mark:
        :param word2:
        :param word2_neg_mark:
        :param word_pos_dict:
        :param neg_pos_set:
        :param neg_max_len:
        :param max_len:
        :return:
        """
        # 词语是否存在匹配
        if word1 not in word_pos_dict:
            return False
        if word2 not in word_pos_dict:
            return False

        w1_pos_list = word_pos_dict[word1]
        w2_pos_list = word_pos_dict[word2]

        # 距离匹配
        if max_len is None:
            return True
        for s1, e1 in w1_pos_list:
            for s2, e2 in w2_pos_list:
                dis = self.get_pos_dis(s1, e1, s2, e2)

                neg1_result = self.is_match_word_list([(s1, e1)], neg_pos_set, word1_neg_mark, neg_max_len)
                neg2_result = self.is_match_word_list([(s2, e2)], neg_pos_set, word2_neg_mark, neg_max_len)
                if not neg1_result or not neg2_result:
                    continue

                if dis <= max_len:
                    return True

        return False

    def search_from_automaton(self, auto_object, content):
        search_list = list()
        for item in auto_object.iter(content):
            target_last_index = item[0]
            target_word = item[1]
            end = target_last_index + 1
            start = end - len(target_word)
            search_list.append((start, end, target_word))

        return search_list

    @staticmethod
    def second_split(input_str: str) -> list:
        """
        拆分一条规则字符串
        :param input_str: string
                eg: "中国+完成-(重要+事情)-知道吗"
        :return: list
                eg:['中国', '+完成', '-(重要+事情)', '-知道吗']
        """
        sub_list = list()
        tmp_list = list()
        input_str_list = list(input_str)
        i = 0
        while i < len(input_str_list):
            ch = input_str_list[i]
            if ch == KeywordMark.BRACKET_LEFT:
                j = i + 1
                while j < len(input_str_list) and input_str_list[j] != KeywordMark.BRACKET_RIGHT:
                    j += 1

                tmp_list.extend(list(input_str_list[i:j+1]))
                tmp_sub_str = "".join(tmp_list)

                # 递归处理,只有一层递归，不要太复杂了
                sub_list.append(tmp_sub_str)
                # print(input_str_list[j+1])
                i = j + 1
                tmp_list = list()

                continue
            if ch in {KeywordMark.PLUS, KeywordMark.MINUS}:
                if len(tmp_list) > 0:
                    sub_list.append("".join(tmp_list))
                tmp_list = list()
                # 分隔符放在第一位
                tmp_list.append(ch)
            else:
                tmp_list.append(ch)

            i += 1

        if len(tmp_list) > 0:
            sub_list.append("".join(tmp_list))

        return sub_list

    @staticmethod
    def build_rule_item(sub_str: str) -> KRule:
        """
        构建一条规则
        :param sub_str: string, 规则字符串
        :return:
     """
        def build_simple_k_item(k_one_str):
            if k_one_str.startswith(KeywordMark.PLUS):
                k_one_str = k_one_str.replace(KeywordMark.PLUS, "")
                return KeywordMark.PLUS, KItem(k_one_str)
            elif k_one_str.startswith(KeywordMark.MINUS):
                k_one_str = k_one_str.replace(KeywordMark.MINUS, "")
                return KeywordMark.MINUS, KItem(k_one_str)
            else:
                return None, KItem(k_one_str)

        def build_simple_k_rule(k_one_str):
            if k_one_str.startswith(KeywordMark.PLUS):
                k_one_str = k_one_str[len(KeywordMark.PLUS):]
                k_one_str = k_one_str.replace(KeywordMark.BRACKET_LEFT, "")
                k_one_str = k_one_str.replace(KeywordMark.BRACKET_RIGHT, "")
                cur_rule = KRuleParser.build_rule_item(k_one_str)
                return KeywordMark.PLUS,  cur_rule
            elif k_one_str.startswith(KeywordMark.MINUS):
                k_one_str = k_one_str[len(KeywordMark.MINUS):]
                k_one_str = k_one_str.replace(KeywordMark.BRACKET_LEFT, "")
                k_one_str = k_one_str.replace(KeywordMark.BRACKET_RIGHT, "")
                cur_rule = KRuleParser.build_rule_item(k_one_str)
                return KeywordMark.MINUS, cur_rule
            else:
                k_one_str = k_one_str.replace(KeywordMark.BRACKET_LEFT, "")
                k_one_str = k_one_str.replace(KeywordMark.BRACKET_RIGHT, "")
                cur_rule = KRuleParser.build_rule_item(k_one_str)
                return None, cur_rule

        master = None

        rule_str_list = KRuleParser.second_split(sub_str)
        slave_dict = {KeywordMark.PLUS: list(),
                      KeywordMark.MINUS: list()}

        for i, one_str in enumerate(rule_str_list):
            if i == 0:
                if KeywordMark.BRACKET_LEFT in one_str:
                    _, master = build_simple_k_rule(one_str)
                else:
                    _, master = build_simple_k_item(one_str)

            else:
                if KeywordMark.BRACKET_LEFT in one_str:
                    item_type, item = build_simple_k_rule(one_str)
                else:
                    item_type, item = build_simple_k_item(one_str)
                slave_dict[item_type].append(item)

        k_rule = KRule(master, slave_dict[KeywordMark.PLUS], slave_dict[KeywordMark.MINUS], rule_str=sub_str)

        return k_rule

    @staticmethod
    def parse_rule_from_keyword(keyword_str: str) -> List[KRule]:
        """

        :param keyword_str: string, 关键词规则
                    eg: "中国+完成-(重要+事情)-知道吗"|名片夹|卡片夹|护照夹
        :return: list(KRule)
        """
        # 一级拆分
        t_list = keyword_str.split(KeywordMark.AND)

        rule_list = list()
        for sub_str in t_list:
            one_rule = KRuleParser.build_rule_item(sub_str)
            rule_list.append(one_rule)

        return rule_list


if __name__ == "__main__":
    keyword = "(中国+完成)+(想+要)-(重要+事情)-知道吗|#中华"
    # split_result = KRuleParser.second_split(data)
    # print(split_result)
    # rules = KRuleParser.parse_rule_from_keyword(data)
    #
    # for one_rule in rules:
    #     print(one_rule.get_master_words(), one_rule.get_slave_words())
    content = "中国已经完成了最想要12345678知道吗事情，我们还要继续努力人不中华必人胜"
    # content = "我们还要继续努力不中华必胜"
    kid2keyword = {1: keyword}
    parser = KRuleParser(kid2keyword, build_neg_model=True)

    result = parser.parse(content, return_all=True, direction="right")
    print(result)
    # print(KRuleParser.second_split("想+要"))





