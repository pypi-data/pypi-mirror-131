# -*- coding: utf-8 -*-
# ----------------------------------------------
# purpose : 标签extract的业务层
# author : LGD
# create_time : 2021/2/5 10:56
# update_time : 2021/2/5 10:56
# copyright : Lavector
# ----------------------------------------------
import itertools
import pandas as pd

from lavda.util.panda_tool import PandaTool
from lavda.util.mysql_util import CommonLavDbReader
from lavda.util.dict_trie import DictTrie
from lavda.backexcutor.analysis_interface import RowInterface
from lavda.analysis.da_tag.label_dict import PandaLabelDictTool
from lavda.analysis.da_tag.label_keyword import KRuleParser
from lavda.analysis.da_tag.label_util import LabelUtil
from lavda.config.maxda_config import LAV_AI_DB_CONFIG


LABEL_CONTENT_DICT = {
    "redbook": {
        "default": ['content', 'title'],
    },
    "zhihu": {
        "default": ['content', 'title'],
    },
    "xinyang": {
        "default": ['content', 'title'],
    },
    "tiktok": {
        "default": ['content', 'title'],
    },
    "bilibili": {
        "default": ['content', 'title'],
    },
    "boqi": {
        "default": ['content', 'title'],
    },
    "tmall": {
        "品牌": ['content', 'title'],
        "default": ['content'],
    },
    "jd": {
        "品牌": ['content', 'title'],
        "default": ['content'],
    },
    "nosetime": {
        "品牌": ['content', 'title'],
    },

    "default":  ['content']
}


class PurchaseFilter(object):
    """
    购买标签的过虑规则
    """
    def __init__(self):
        df_word = CommonLavDbReader.get_as_df("pro_label_dict", db_config=LAV_AI_DB_CONFIG)
        word_list = df_word.to_dict(orient="records")
        purchase_must_word_set = set([item["term"] for item in word_list if item['category'] == '购买'])
        # purchase_must_word_set = {'做过', '做了', '完成', '术后', '做的', '复购', '买了', '打完', '打了', '买的', '囤的', '囤了', '坚持做', '定期',
        #                           '有用', '第二次', '第三次', '体验了'}

        trie = DictTrie()
        for word in purchase_must_word_set:
            trie.insert(list(word), word)

        self.trie = trie

    def is_skip(self, input_text):
        start = 0
        # result_list = list()

        value_list = list(input_text)
        while start < len(value_list):
            search_text = value_list[start:]
            r_result = self.trie.search_path(search_text)
            if r_result is None or r_result[1] is None:
                start += 1
            else:
                return False
                # find_item = dict()
                # find_item['value'] = r_result[0]
                # find_item['meta'] = r_result[1]
                # find_item['start'] = start
                # find_item['end'] = start + len(find_item['value'])
                # result_list.append(find_item)
                #
                # t_text = find_item['value']
                # start += len(t_text)

        return True


class KeywordBaseExtractor(RowInterface):
    """
    关键词提取、匹配基础功能
    """
    COL_TITLE = 'title'
    COL_CONTENT = 'content'

    def __init__(self, default_value=None):
        super(KeywordBaseExtractor, self).__init__(default_value)
        # TODO 定义打标签功能输出格式

        self._mc = None
        self._map_rules = list()

        self.purchase_filter = None

    @property
    def mc(self):
        return self._mc

    def load_base_config_data(self, **config):
        dict_tool = PandaLabelDictTool()

        label_dict_path = config['mappingDictPath']
        mc = dict_tool.load_all_from_file(label_dict_path)
        for mapping in mc.mappings:
            k_rule = KRuleParser(mapping.id2keyword)
            self._map_rules.append((mapping, k_rule))
        self._mc = mc

        mc_names = [item.label_name for item in mc.mappings]
        if '购买' in mc_names:
            self.purchase_filter = PurchaseFilter()

        return mc

    def load_config_data(self, **config):
        """
        加载词表
        :param config:
        :return:
        """
        self.load_base_config_data(**config)

    def clean_text(self, content):
        clean_data = LabelUtil.clean_text(content)
        return clean_data

    def build_task_params(self, data):
        """
        构建提取任务参数,主要是确定各个标签、各个平台打标所需要对应的字段
        :param data:
        :return:
        """
        channel = data['channel']

        # 1. 提取内容列
        input_task_list = list()
        input_columns_set = set()
        for i, mapping_rule in enumerate(self._map_rules):
            mapping, k_rule = mapping_rule
            label_name = mapping.label_name
            input_columns = None
            if channel in LABEL_CONTENT_DICT:
                if label_name in LABEL_CONTENT_DICT[channel]:
                    input_columns = LABEL_CONTENT_DICT[channel][label_name]
                elif 'default' in LABEL_CONTENT_DICT[channel]:
                    input_columns = LABEL_CONTENT_DICT[channel]['default']
            if input_columns is None:
                input_columns = LABEL_CONTENT_DICT['default']
            input_columns_set.update(input_columns)

            input_task_list.append((mapping, k_rule, input_columns))

        return input_task_list, input_columns_set

    def build_texts(self, data, input_columns_set):
        """
        构建并格式化输入文本,主要是数据清洗并格式化
        :param data: dict
        :param input_columns_set:
        :return:
        """
        input_data_dict = dict()
        for col in input_columns_set:
            col_data = self.clean_text(data[col])
            input_data_dict[col] = col_data

        return input_data_dict

    def parse_keywords(self, data, return_all=False):
        """
        从文本中提取标签关键词
        :param data:
        :param return_all: bool，是否提取所有关键词
        :return:
                tuple(input_data_dict, keyword_result)
                input_data_dict:格式化的内容
                keyword_result: 匹配结果

                eg:
                input_data_dict:{'content': [{'index': 0, 'content': '跟tf80对比，它是有点雾面感，不滋润，比较干，膏体是像蜡笔一样的感觉，个人更喜欢滋润的唇膏', 'start': 0, 'end': 46}]}

                keyword_result(每个元素是一个词表的结果):
                [{'content': [{'aspect': '不滋润', 'start': 16, 'end': 19, 'keyword': '不+滋润|有点干|太干|无敌干|拔干-不拔干', 'kid': 47, 'index': 0},
                             {'aspect': '不滋润', 'start': 16, 'end': 19, 'keyword': '不+滋润|有点干|太干|无敌干|拔干-不拔干', 'kid': 250, 'index': 0},
                             {'aspect': '滋润', 'start': 17, 'end': 19, 'keyword': '保湿|滋润|补水|缓解干燥|不起皮', 'kid': 49, 'index': 0},
                             {'aspect': '喜欢', 'start': 39, 'end': 41, 'keyword': '喜欢|心水|感兴趣', 'kid': 282, 'index': 0},
                             {'aspect': '滋润', 'start': 41, 'end': 43, 'keyword': '滋润-不滋润|不拔干|特别润|不干涩|非常润', 'kid': 50, 'index': 0}
                             ]
                }]
        """

        # 1.构建任务参数
        input_task_list, input_columns_set = self.build_task_params(data)

        # 2.构建所需要的数据格式
        input_data_dict = self.build_texts(data, input_columns_set)

        # 3.实际提取匹配
        keyword_result = [{col: list() for col in input_data_dict} for _ in range(len(input_task_list))]
        for one_col in input_data_dict:
            for i, task_item in enumerate(input_task_list):
                mapping, k_rule, input_columns = task_item
                if one_col not in input_columns:
                    continue

                # TODO 单独给购买添加的一个过虑，临时写法，而且是使用原始数据，而非清洗后的数据
                if mapping.label_name == "购买" and self.purchase_filter is not None:
                    if self.purchase_filter.is_skip(data[one_col]):
                        continue
                if one_col == self.COL_TITLE:
                    one_result_dict = self.parse_from_title(mapping, k_rule, input_data_dict[one_col],
                                                            return_all=return_all, original_data=data)
                elif one_col == self.COL_CONTENT:
                    one_result_dict = self.parse_from_content(mapping, k_rule, input_data_dict[one_col],
                                                              return_all=return_all, original_data=data)
                else:
                    raise Exception("unknown col for parser=" + str(one_col))

                if one_result_dict is None:
                    continue
                keyword_result[i][one_col].extend(one_result_dict)

        # 暂时不返回具体的匹配信息
        input_data_dict = self.format_input_data(input_data_dict)
        return input_data_dict, keyword_result

    def is_skip_match(self, mapping, one_col, data):
        """
        正式使用规则匹配前的一些校验、过虑、检查，以确定是否需要进入下一下该步，
        TODO 这些功能，放这里实在是不优雅
        :return:
        """




    def format_input_data(self, input_data_dict):
        """
        格式化/标准化输入数据，主要是分句时使用
        :param input_data_dict:
        :return:
        """
        return input_data_dict

    def parse_from_text(self, mapping, k_rule, content, return_all=False, original_data=None, rule_param=None):
        total_params = {'content': content,
                        'return_all': return_all}
        if rule_param is not None:
            total_params.update(rule_param)
        # one_result = k_rule.parse(content=content, return_all=return_all)
        one_result = k_rule.parse(**total_params)

        return one_result

    def build_title_rule_param(self, original_data):
        # TODO 业务级约定：jd、tmall title作特殊处理,不限制距离
        if original_data is not None and 'channel' in original_data and original_data['channel'] in {"tmall", 'jd'}:
            rule_param = dict()
            rule_param['plus_max_len'] = 100
            return rule_param
        else:
            return None

    def parse_from_title(self, mapping, k_rule, content, return_all=False, original_data=None):
        """
        从title字段提取关键词
        :param mapping:
        :param content:
        :param k_rule:
        :param return_all:
        :return:
        """
        rule_param = self.build_title_rule_param(original_data)
        one_result = self.parse_from_text(mapping, k_rule, content, return_all, rule_param=rule_param)

        return one_result

    def parse_from_content(self, mapping, k_rule, content, return_all=False, original_data=None):
        """
        从content字段提取关键词
        :param mapping:
        :param content:
        :param k_rule:
        :param return_all:
        :return:
        """
        one_result = self.parse_from_text(mapping, k_rule, content, return_all)
        return one_result

    def process(self, data, **params):
        """

        :param data: dict
                    eg: {'channel': 'nosetime', 'content': '也是秋冬必备的颜色之一', 'title': '纪梵希绝美新色，颜色漂亮呀'}
        :param params:
        :return:
                eg:
                []
        """
        return_all = False
        merge_and_format = False
        if params is not None:
            if 'return_all' in params:
                return_all = params['return_all']
            if 'merge_and_format' in params:
                merge_and_format = params['merge_and_format']

        # result_dict: tuple(dict, list), dict是各字段内容，list是各标签打上的结果
        #    ( {'title': '纪梵希绝美新色，颜色漂亮呀', 'content': '也是秋冬必备的颜色之一'},
        #      [{'title': [{'aspect': '纪梵希', 'start': 0, 'end': 3, 'keyword': '纪梵希|givenchy', 'kid': 391}],  'content': []},
        #       {'title': [], 'content': [{'aspect': '秋冬必备的颜色', 'start': 2, 'end': 9, 'keyword': '颜色+秋冬', 'kid': 289}]}]
        #      )
        #
        result_dict = self.parse_keywords(data, return_all)

        if not merge_and_format:
            return result_dict
        else:
            merge_data = self.merge_and_format(result_dict[-1])
            last_result = self.build_result_format(result_dict[-1], merge_data)
            return last_result

    def merge_and_format(self, keyword_result, input_data_dict=None, default_value=None):
        """
        合并不同字段抽取结果并格式化
        :param keyword_result: list, 来处parse_keywords函数的结果
        :return:
            eg: 两个词表，每一列，表示一个词表
                [(30, 283),
                (30, 67)]
        """
        kid_result = list()
        for one_dict in keyword_result:
            one_kid_list = list()
            # TODO 不同字段关键词结果进行合并
            for col in one_dict:
                one_kid_list.extend(one_dict[col])

            one_kids = list(set([kk_item['kid'] for kk_item in one_kid_list]))
            kid_result.append(one_kids)

        # 直接迪卡尔积扩展
        merge_data = KeywordExtractUtil.expand_and_product(*kid_result, default_value=default_value)

        return merge_data

    def build_result_format(self, keyword_result, merge_data):
        """
        构建输出格式，3个字段
        :param keyword_result:
        :param merge_data:
        :return:
        """
        tag_keyword_set = set()
        tag_aspect_list = list()
        for one_dict in keyword_result:
            # TODO 不同字段关键词结果进行合并
            kid_aspect = dict()
            for col in one_dict:
                col_result = one_dict[col]
                for item in col_result:
                    kid = item['kid']
                    if kid not in kid_aspect:
                        kid_aspect[kid] = set()
                    kid_aspect[kid].add(item['aspect'])

                tag_keyword_set.update([item['keyword'] for item in col_result])
            tag_aspect_list.append(kid_aspect)

        tag_keyword_set = list(tag_keyword_set)
        tag_aspect_set = tag_aspect_list

        return merge_data, tag_keyword_set, tag_aspect_set


def eval_result_list(input_str):
    """
    可能由于excel保存时丢失一些内容,因此要校验
    :param input_str:
    :return:
    """
    tmp_list = list(input_str)
    if tmp_list[-1] == ']':
        eval_result = eval(input_str)
        return eval_result
    pos = len(tmp_list) - 1
    while pos >= 0:
        if tmp_list[pos] == ')':
            break
        pos -= 1

    select_list = tmp_list[:pos+1]
    select_list += ']'
    result_str = "".join(select_list)
    eval_result = eval(result_str)

    # TODO 因为结果数据太多时，一般是有问题的，因此象征性的只取一个结果吧
    if len(eval_result) > 0:
        eval_result = eval_result[: 1]
    return eval_result


class KeywordExtractUtil(object):
    @staticmethod
    def expand_and_format(label_result,
                          mc,
                          tag_result_col="tag_result",
                          tag_aspect_col='tag_aspect',
                          tag_keyword_col="tag_keyword",
                          tmp_index_col="tmp_merge_index",
                          result_prefix="tag_format_"):
        """
        将标签的结果进行格式化展开，以方便分析师分析
        :param label_result: string(结果文件) or dataframe
        :param mc: MappingCollect
        :param tag_result_col: string, 打标签的中间结果字段名
        :param tag_aspect_col: string, 存储标签aspect信息的字段
        :param tag_keyword_col: string, 存储keyword信息的列，这里只是用于删除的，没别的用处
        :param tmp_index_col: string,展开时使用的临时索引字段名
        :param result_prefix: string,展开后结果字段前缀
        :return:
        """
        mappings = mc.mappings
        total_columns = list()
        mapping_col_dict = dict()
        for i, mapping in enumerate(mappings):
            tmp_cols = [result_prefix + col for col in mapping.columns]
            # TODO 加一个aspect列
            tmp_cols.append(result_prefix + mapping.label_name + "(aspect)")
            mapping_col_dict[i] = tmp_cols
            total_columns.extend(tmp_cols)

        df_input = PandaTool.read_more(label_result)
        df_input[tmp_index_col] = range(df_input.shape[0])

        split_lines = df_input.groupby(tmp_index_col)
        # df_sub_list = list()
        line_result = list()
        for split_index, df_line in split_lines:
            label_kid_list = df_line[tag_result_col]
            tmp_label_id_value = label_kid_list.values[0]
            if isinstance(tmp_label_id_value, str):
                label_kid_list = eval_result_list(tmp_label_id_value)
            else:
                label_kid_list = tmp_label_id_value

            label_aspect_df = df_line[tag_aspect_col]
            if isinstance(tmp_label_id_value, str):
                label_aspect_list = eval(label_aspect_df.values[0])
            else:
                label_aspect_list = label_aspect_df.values[0]

            for line_kids in label_kid_list:
                line_keyword_result = list()
                # 处理一行所有的标签信息
                for i, one_kid in enumerate(line_kids):
                    if one_kid is not None:
                        id2relation = mappings[i].id2relation
                        # TODO 添加aspect结果数据
                        keyword_aspect = ",".join(label_aspect_list[i][one_kid])
                        keyword_line = id2relation[one_kid].copy()
                        keyword_line.append(keyword_aspect)
                        # print(i, len(keyword_line), len(id2relation[one_kid]))
                    else:
                        # TODO 空标签用空值填充
                        keyword_line = [None for _ in range(len(mapping_col_dict[i]))]

                    line_keyword_result.extend(keyword_line)
                # TODO 最后一个元素即tmp_index_col作为和原始数据关联使用
                line_keyword_result = line_keyword_result + [split_index]
                line_result.append(line_keyword_result)
        # 纯标签信息
        db_only_label = pd.DataFrame(line_result, columns=total_columns+ [tmp_index_col])

        inner_line = pd.merge(df_input, db_only_label, on=tmp_index_col, how='left')
        df_data = inner_line.drop(columns=[tmp_index_col, tag_result_col, tag_aspect_col, tag_keyword_col])

        return df_data

    @staticmethod
    def old_expand_and_format(label_result,
                          mc,
                          tag_result_col="tag_result",
                          tag_aspect_col='tag_aspect',
                          tag_keyword_col="tag_keyword",
                          tmp_index_col="tmp_merge_index",
                          result_prefix="tag_format_"):
        """
        将标签的结果进行格式化展开，以方便分析师分析
        旧的方法，仿照达达写的，效率有些低，因此废弃了
        :param label_result: string(结果文件) or dataframe
        :param mc: MappingCollect
        :param tag_result_col: string, 打标签的中间结果字段名
        :param tag_aspect_col: string, 存储标签aspect信息的字段
        :param tag_keyword_col: string, 存储keyword信息的列，这里只是用于删除的，没别的用处
        :param tmp_index_col: string,展开时使用的临时索引字段名
        :param result_prefix: string,展开后结果字段前缀
        :return:
        """
        mappings = mc.mappings
        total_columns = list()
        mapping_col_dict = dict()
        for i, mapping in enumerate(mappings):
            tmp_cols = [result_prefix + col for col in mapping.columns]
            # TODO 加一个aspect列
            tmp_cols.append(result_prefix + mapping.label_name + "(aspect)")
            mapping_col_dict[i] = tmp_cols
            total_columns.extend(tmp_cols)

        df_input = PandaTool.read_more(label_result)
        df_input[tmp_index_col] = range(df_input.shape[0])

        split_lines = df_input.groupby(tmp_index_col)
        df_sub_list = list()
        for split_index, df_line in split_lines:
            label_kid_list = df_line[tag_result_col]
            tmp_label_id_value = label_kid_list.values[0]
            if isinstance(tmp_label_id_value, str):
                label_kid_list = eval(tmp_label_id_value)
            else:
                label_kid_list = tmp_label_id_value

            label_aspect_df = df_line[tag_aspect_col]
            if isinstance(tmp_label_id_value, str):
                label_aspect_list = eval(label_aspect_df.values[0])
            else:
                label_aspect_list = label_aspect_df.values[0]

            line_result = list()
            for line_kids in label_kid_list:
                line_keyword_result = list()
                for i, one_kid in enumerate(line_kids):
                    if one_kid is not None:
                        id2relation = mappings[i].id2relation
                        # TODO 添加aspect结果数据
                        keyword_aspect = ",".join(label_aspect_list[i][one_kid])
                        keyword_line = id2relation[one_kid].copy()
                        keyword_line.append(keyword_aspect)
                        # print(i, len(keyword_line), len(id2relation[one_kid]))
                    else:
                        # TODO 空标签用空值填充
                        keyword_line = [None for _ in range(len(mapping_col_dict[i]))]

                    line_keyword_result.extend(keyword_line)
                line_result.append(line_keyword_result)

            db_only_label = pd.DataFrame(line_result, columns=total_columns)
            db_only_label[tmp_index_col] = split_index

            inner_line = pd.merge(df_line, db_only_label, on=tmp_index_col, how='left')
            line = inner_line.drop(columns=[tmp_index_col, tag_result_col, tag_aspect_col, tag_keyword_col])

            df_sub_list.append(line)

        # 合并所有
        df_data = pd.concat(df_sub_list, sort=False)

        return df_data

    @staticmethod
    def expand_and_product(*input_list, default_value=None):
        """
        迪卡尔积（只是添加一些扩展功能）
        :param input_list:
        :param default_value:
        :return:
        """
        for one_list in input_list:
            if len(one_list) == 0:
                one_list.append(default_value)

        data = list(itertools.product(*input_list))
        return data

    @staticmethod
    def distinct_keywords_kid(input_list):
        """
        二维数组去重，业务级的去重
        保留关系内容最全面的
        # TODO 空值用None 表示
        eg:(k1, None, k2), (k1, None, None) 去重后 => (k1, None, k2)
        :param input_list:
        :return:
        """
        if len(input_list) <= 1:
            return input_list

        # 提取非空元素数据
        elem_list = [set() for _ in range(len(input_list))]
        for i, line in enumerate(input_list):
            for j, value in enumerate(line):
                # TODO 空值用None来表示
                if value is None:
                    continue
                # TODO 因为不同行的值可能是唯一的，因此加一个索引前缀，以产生唯一的值
                u_elem = str(j) + "-" + str(value)
                elem_list[i].add(u_elem)

        # 合并交集部分
        flag_list = [True for _ in range(len(input_list))]
        for i in range(len(input_list) - 1):
            for j in range(i+1, len(input_list)):
                if not flag_list[i] or not flag_list[j]:
                    continue
                ei = elem_list[i]
                ei_count = len(ei)
                if ei_count <= 0:
                    flag_list[i] = False
                    continue

                ej = elem_list[j]
                ej_count = len(ej)
                if ej_count <= 0:
                    flag_list[j] = False
                    continue

                e_tmp_set = ei.intersection(ej)
                e_tmp_count = len(e_tmp_set)

                if e_tmp_count == ei_count:
                    flag_list[i] = False
                elif e_tmp_count == ej_count:
                    flag_list[j] = False
                else:
                    continue

        # 返回最终结果
        result_list = [one_item for i, one_item in enumerate(input_list) if flag_list[i]]

        return result_list


def segment_text(text, split_char_set):
    """
    分句
    :param text:
    :param split_char_set:
    :return:
    """
    result_list = list()

    tmp_sub_list = list()
    text_len = len(text)
    sub_text_start = 0
    cur_char_pos = 0

    for i, ch in enumerate(text):

        # 检查到分隔符
        if ch in split_char_set:
            # TODO 分隔符也是需要保留的
            tmp_sub_list.append(ch)
            sub_text = "".join(tmp_sub_list)
            text_index = len(result_list)
            sub_text_term = {'index': text_index, 'content': sub_text, "start": sub_text_start, 'end': sub_text_start + len(sub_text)}
            result_list.append(sub_text_term)

            sub_text_start = sub_text_term['end']
            tmp_sub_list = list()
            continue
        else:
            tmp_sub_list.append(ch)

        # 最后一个字符
        if text_len - 1 == i:
            if tmp_sub_list:
                sub_text = "".join(tmp_sub_list)
                text_index = len(result_list)
                sub_text_term = {'index': text_index, 'content': sub_text, "start": sub_text_start,
                                 'end': sub_text_start + len(sub_text)}
                result_list.append(sub_text_term)

        cur_char_pos += len(ch)

    return result_list


class KeywordSegmentExtractor(KeywordBaseExtractor):
    """
    基于分句的关键词提取、匹配方法
    """
    def __init__(self, default_value=None):
        super(KeywordSegmentExtractor, self).__init__(default_value)
        # 分句打标功能

        self.split_char = {'.', '。', '!', '！', '\n'}

        # 品牌、消费者需要标签向后扩展
        self.brand_exclude_kids = set()
        self.brand_index = None
        self.need_index = None
        self.expand_need = False

    def load_config_data(self, **config):
        """
        加载词表
        :param config:
        :return:
        """
        mc = self.load_base_config_data(**config)

        # TODO 特殊处理
        flag_col = None
        for i, mapping in enumerate(mc.mappings):
            name = mapping.label_name
            if name == '品牌':

                columns = mapping.columns
                id_col = None
                for col in columns:
                    if '(flag)' in col:
                        flag_col = col
                    if '(id)' in col:
                        id_col = col
                if flag_col is not None:
                    id2line = mapping.id2line
                    for one_line in list(id2line.values()):
                        line_kid = int(one_line[id_col])
                        if int(one_line[flag_col]) == 0:
                            self.brand_exclude_kids.add(line_kid)

                self.brand_index = i
            if name == '消费者需求':
                self.need_index = i

            if flag_col is not None and self.need_index is not None and self.brand_index is not None:
                self.expand_need = True

    def build_texts(self, data, input_columns_set):
        input_data_dict = dict()
        for col in input_columns_set:
            # TODO 要先清洗，再分句，否则分句的结果，不容易对应到主句(主要是指aspect的位置信息)
            # TODO 清洗时，不能将分隔符给清洗掉
            col_data = self.clean_text(data[col])

            col_data = segment_text(col_data, self.split_char)

            input_data_dict[col] = col_data

        return input_data_dict

    def format_input_data(self, input_data_dict):
        """
        分句的内容，再合成一个完整的句子
        :param input_data_dict:
        :return:
        """
        format_data = dict()
        for col in input_data_dict:
            sub_text = "".join(item['content'] for item in input_data_dict[col])
            format_data[col] = sub_text

        return format_data

    def parse_by_segment(self, mapping, k_rule, content, return_all=False, original_data=None, rule_param=None):
        """

        :param mapping:
        :param k_rule:
        :param content: segment_text 拆分后的结果
        :param return_all:
        :return:
        """
        result_list = list()
        for text_item in content:
            sub_content = text_item['content']

            one_result = self.parse_from_text(mapping, k_rule, sub_content, return_all=return_all, original_data=original_data, rule_param=rule_param)

            # TODO 添加分句索引字段，同时将aspect的分句位置替换为在整句的位置
            for r_item in one_result:
                r_item["index"] = text_item['index']
                r_item["start"] = text_item['start'] + r_item['start']
                r_item["end"] = text_item['start'] + r_item['end']
            result_list.extend(one_result)

        return result_list

    def parse_from_content(self, mapping, k_rule, content, return_all=False, original_data=None):
        result_list = self.parse_by_segment(mapping, k_rule, content, return_all=return_all, original_data=original_data)

        return result_list

    def parse_from_title(self, mapping, k_rule, content, return_all=False, original_data=None):
        rule_param = self.build_title_rule_param(original_data)

        result_list = self.parse_by_segment(mapping, k_rule, content, return_all=return_all,
                                            original_data=original_data, rule_param=rule_param)

        return result_list

    def build_result_format(self, keyword_result, merge_data):
        """
        构建输出格式，3个字段
        :param keyword_result:
        :param merge_data:
        :return:
        """
        tag_keyword_set = set()
        tag_aspect_list = list()
        for one_dict in keyword_result:
            # TODO 不同字段关键词结果进行合并
            kid_aspect = dict()
            for col in one_dict:
                col_result = one_dict[col]
                for item in col_result:
                    kid = item['kid']
                    if kid not in kid_aspect:
                        kid_aspect[kid] = set()
                    kid_aspect[kid].add(item['aspect'])

                tag_keyword_set.update([item['keyword'] for item in col_result])
            tag_aspect_list.append(kid_aspect)

        tag_keyword_set = list(tag_keyword_set)
        tag_aspect_set = tag_aspect_list


        # TODO 排除不需要的品牌aspect
        if len(self.brand_exclude_kids) > 0:
            t_brand_dict = dict()
            for o_kid in tag_aspect_set[self.brand_index]:
                if o_kid in self.brand_exclude_kids:
                    continue
                t_brand_dict[o_kid] = tag_aspect_set[self.brand_index][o_kid]
            tag_aspect_set[self.brand_index] = t_brand_dict

        return merge_data, tag_keyword_set, tag_aspect_set

    def merge_and_format(self, keyword_result, input_data_dict=None, default_value=None):
        """
        合并不同字段抽取结果并格式化
        :param keyword_result: list, 来处parse_keywords函数的结果
        :param input_data_dict: list, 来处parse_keywords函数的结果
        :param default_value: list,
        :return:
        """
        # 1.不分句字段的结果
        # TODO 所有字段都分句，因此不存在不分句的字段
        # other_kid_list = list()
        # for one_dict in keyword_result:
        #     one_kid_list = list()
        #     for col in one_dict:
        #         if col == self.COL_CONTENT:
        #             continue
        #         one_kid_list.extend(one_dict[col])
        #
        #     one_kids = list(set([kk_item['kid'] for kk_item in one_kid_list]))
        #     other_kid_list.append(one_kids)
        #
        # other_result = KeywordExtractUtil.expand_and_product(*other_kid_list, default_value=default_value)
        other_result = list()

        # 2.分句字段的结果
        # 2.1先提取分句索引
        segment_index = dict()
        for i, one_dict in enumerate(keyword_result):

            for one_col in one_dict:
                for item in one_dict[one_col]:
                    one_index = item['index']
                    seg_index = str(one_col) + '-' + str(one_index)
                    if seg_index not in segment_index:
                        segment_index[seg_index] = dict()
                    if i not in segment_index[seg_index]:
                        segment_index[seg_index][i] = set()
                    segment_index[seg_index][i].add(item['kid'])

        # TODO 品牌-消费者向下扩展，暂时只扩展content字段
        if self.expand_need:
            tmp_expand_brand_and_need(self.COL_CONTENT, segment_index, self.brand_index, self.need_index, self.brand_exclude_kids)
            # TODO 清除残存的不需要的品牌标签结果
            for one_index in segment_index:
                if self.brand_index in segment_index[one_index]:
                    tmp_b_index = set()
                    for one_brand_kid in segment_index[one_index][self.brand_index]:
                        if one_brand_kid in self.brand_exclude_kids:
                            continue
                        tmp_b_index.add(one_brand_kid)
                    segment_index[one_index][self.brand_index] = tmp_b_index
        # 2.2 分别提取各分句结果
        segment_result = list()
        # segment_index: 分句索引 => 标签序列索引 => list(kid)
        for one_index in segment_index:
            segment_kid_list = list()
            for i, one_dict in enumerate(keyword_result):
                if i not in segment_index[one_index] or len(segment_index[one_index][i]) <= 0:
                    # TODO 空值用None表示
                    segment_kid_list.append(list())
                else:
                    segment_kid_list.append(segment_index[one_index][i])

            one_segment_result = KeywordExtractUtil.expand_and_product(*segment_kid_list, default_value=default_value)
            segment_result.extend(one_segment_result)

        all_result = other_result + segment_result

        # 3.去重
        # eg:(k1, None, k2), (k1, None, None) 去重后 => (k1, None, k2)
        all_result = KeywordExtractUtil.distinct_keywords_kid(all_result)

        return all_result


def tmp_expand_brand_and_need(target_col, segment_index, brand_index, need_index, brand_exclude_kids):
    """
    临时处理功能，用于临时扩展品牌-消费者需求关系组合
    :return:
    """

    def split_brand(input_brand_sets):
        t_include_set = set()
        t_exclude_set = set()
        for t_brand_kid in input_brand_sets:
            if t_brand_kid in brand_exclude_kids:
                t_exclude_set.add(t_brand_kid)
            else:
                t_include_set.add(t_brand_kid)
        return t_include_set, t_exclude_set

    max_expand_count = 7

    seg_index_list = list(segment_index.keys())
    # TODO 只选择指定的列的结果
    seg_index_list = [item for item in seg_index_list if target_col in item]
    # 分句索引按顺序排列，从开头到时结尾
    seg_index_list = sorted(seg_index_list, key=lambda x: x)

    start = 0
    while start < len(seg_index_list):
        cur_seg_index = seg_index_list[start]
        cur_brand_sets = segment_index[cur_seg_index][brand_index] if brand_index in segment_index[cur_seg_index] else set()
        cur_include_set, cur_exclude_set = split_brand(cur_brand_sets)
        # segment_index[cur_seg_index][brand_index] = cur_include_set
        # TODO 为了不至于扩展太多数据，因此随机选一个进行扩展，其他不选择
        if len(cur_include_set) <= 0:
            start += 1
            continue
        cur_expand_brand_kid = list(cur_include_set)[0]

        next_index = start + 1
        cur_expand_count = 0
        # TODO 防止最后一句陷入死循环
        if next_index >= len(seg_index_list):
            break
        while next_index < len(seg_index_list) and cur_expand_count <= max_expand_count:
            next_seg_index = seg_index_list[next_index]
            next_brand_sets = segment_index[next_seg_index][brand_index] if brand_index in segment_index[next_seg_index] else set()
            next_need_sets = segment_index[next_seg_index][need_index] if need_index in segment_index[next_seg_index] else set()

            next_include_set, next_exclude_set = split_brand(next_brand_sets)
            # segment_index[next_seg_index][brand_index] = next_include_set

            # TODO 到达下一个合法的品牌标签，要退出
            if len(next_include_set) > 0:
                start = next_index
                break
            if len(next_exclude_set) > 0:
                start = next_index + 1
                break
            # 当前句没有消费者需求标签
            if len(next_need_sets) <= 0:
                next_index += 1
                start = next_index
                continue

            # TODO 当前不包含任何品牌标签，只包含消费者需求标签，因此可以扩展，即将上面的brand kid 加入到当前分句中
            if brand_index not in segment_index[next_seg_index]:
                segment_index[next_seg_index][brand_index] = set()
            #
            segment_index[next_seg_index][brand_index].add(cur_expand_brand_kid)
            cur_expand_count += 1
            next_index += 1
            start = next_index


if __name__ == "__main__":
    # 1.测试分句
    text = "中国来.肿。脸.四月份轸!！wolwe"
    split_char = {'.', '。', '!', '！', '\n'}
    # result = segment_text(text, split_char)

    # 2.测试去重
    data = [(1, None, None), (None, None, 2), (1, None, 2), (18, 19, None)]
    result = KeywordExtractUtil.distinct_keywords_kid(data)
    print(result)


