# -*- coding: utf-8 -*-
# ----------------------------------------------
# purpose : 业务级标签/基于算法的打标签功能
# author : LGD
# create_time : 2021/2/22 16:32
# update_time : 2021/2/22 16:32
# copyright : Lavector
# ----------------------------------------------
import os

from lavda.util.mysql_util import CommonLavDbReader
from lavda.config.maxda_config import LAV_AI_DB_CONFIG
from lavda.analysis.da_tag.label_model import LabelComponentModel


class LabelResult(object):
    YES = 1
    UN_CERTAIN = 0
    NO = -1


class LabelCheckInterface(object):
    def predict(self, content, aspect, start, end):
        """

        :param content: string, 文本内容
        :param aspect: string, 需要判断的aspect词
        :param start: int, aspect的开始位置
        :param end: int, aspect的结束位置
        :return: bool
        """
        pass

    def predict_list(self, content, aspect_list):
        """

        :param content:
        :param aspect_list: list(dict)
        :return:
        """
        # 添加id字段
        id_aspect_list = list()

        id_i = 0
        for item in aspect_list:
            id_aspect_list.append([id_i, item])
            id_i += 1

        # 排序
        sort_aspect = sorted(id_aspect_list, key=lambda x: x[-1]['start'])

        # 1.分组
        i = 0
        id_group_dict = dict()
        while i < len(sort_aspect):
            if i == 0:
                # group id 从0开始
                id_group_dict[sort_aspect[i][0]] = 0
            else:
                last_item = sort_aspect[i-1][-1]
                last_item_id = sort_aspect[i-1][0]
                cur_item = sort_aspect[i][-1]
                cur_item_id = sort_aspect[i][0]

                last_end = last_item['end']
                cur_start = cur_item['start']
                if cur_start - last_end <= 1 and content[last_end] in {"+", '和', '、', "与"}:
                    id_group_dict[cur_item_id] = id_group_dict[last_item_id]
                else:
                    # 开启新的id
                    id_group_dict[cur_item_id] = id_group_dict[last_item_id] + 1
            i += 1

        # 2.预测结果
        group_result_dict = dict()
        for cur_id, item in sort_aspect:
            one_result = self.predict(content, item['aspect'], item['start'], item['end'])
            item['aspectCategory'] = one_result
            # if one_result:
            #     item['aspectCategory'] = True
            # else:
            #     item['aspectCategory'] = False

            cur_group_id = id_group_dict[cur_id]
            if cur_group_id not in group_result_dict:
                group_result_dict[cur_group_id] = LabelResult.UN_CERTAIN

            if item['aspectCategory'] != LabelResult.UN_CERTAIN:
                group_result_dict[cur_group_id] = item['aspectCategory']

        # 3.根据同组的
        for cur_id, item in sort_aspect:
            cur_group_id = id_group_dict[cur_id]

            cur_group_result = group_result_dict[cur_group_id]
            if item['aspectCategory'] != cur_group_result:
                item['aspectCategory'] = cur_group_result

        result = [item[-1] for item in sort_aspect]

        return result


class LabelComponentChecker(object):
    """
    成分标签检测
    """
    def __init__(self, root_model_path='/data/share/nlp',
                 use_dict=True):
        """

        :param root_model_path: string,模型根路径
        :param use_dict: bool, 是否使用词典判断
        """
        self.model = LabelComponentModel(os.path.join(root_model_path, *['label', "component"]))

        if use_dict:
            df_word = CommonLavDbReader.get_as_df("pro_label_dict", db_config=LAV_AI_DB_CONFIG)
            word_list = df_word.to_dict(orient="records")
            self.must_word_set = set([item["term"] for item in word_list if item['category'] == '成分'])
        else:
            self.must_word_set = set()

    def predict(self, content, aspect_list):
        """

        :param content: string,
        :param aspect_list: list(item)
                eg: [{'aspect': '中国', 'start': 0, 'end': 3}]
        :return:
        """
        index2result = [False] * len(aspect_list)

        # 1.基于词典匹配
        tmp_list = list()
        tmp_index_list = list()
        for i, item in enumerate(aspect_list):
            if item['aspect'] in self.must_word_set:
                index2result[i] = True
            else:
                tmp_list.append(item)
                tmp_index_list.append(i)

        # 2.基于模型进行判断
        format_input = [[content, ii_item['aspect'], ii_item['start'], ii_item['end']] for ii_item in
                        tmp_list]
        if len(format_input) > 0:
            predict_result = self.model.predict_batch(format_input)
            for i, one_result in enumerate(predict_result):
                old_index = tmp_index_list[i]
                index2result[old_index] = one_result

        # 3.检查并处理并列结构
        if False in set(index2result):
            index2result = self.merge_by_group(content, aspect_list, index2result)

        return index2result

    def merge_by_group(self, content, aspect_list, index2result):
        """
        检查并列结构的数据，并将其保持一致
        :param aspect_list:
        :param index2result:
        :return:
        """
        # 添加id，id和index保持一致
        id_aspect_list = list()

        for i, item in enumerate(aspect_list):
            id_aspect_list.append([i, item])

        # 排序
        sort_aspect = sorted(id_aspect_list, key=lambda x: x[-1]['start'])

        # 1.分组
        i = 0
        # item id => group id
        id_group_dict = dict()
        while i < len(sort_aspect):
            if i == 0:
                # group id 从0开始
                id_group_dict[sort_aspect[i][0]] = 0
            else:
                last_item = sort_aspect[i - 1][-1]
                last_item_id = sort_aspect[i - 1][0]
                cur_item = sort_aspect[i][-1]
                cur_item_id = sort_aspect[i][0]

                last_end = last_item['end']
                cur_start = cur_item['start']
                if 0 < cur_start - last_end <= 1 and content[last_end] in {"+", '和', '、', "与"}:
                    id_group_dict[cur_item_id] = id_group_dict[last_item_id]
                else:
                    # 开启新的id
                    id_group_dict[cur_item_id] = id_group_dict[last_item_id] + 1
            i += 1

        # 2.预测结果
        group_result_dict = dict()
        for cur_id, item in sort_aspect:
            cur_group_id = id_group_dict[cur_id]
            if cur_group_id not in group_result_dict:
                group_result_dict[cur_group_id] = False

            # TODO 如果该组为True 即表示为标签，则不再处理了
            if group_result_dict[cur_group_id]:
                continue
            group_result_dict[cur_group_id] = index2result[cur_id]

        # 3.根据同组的
        for cur_id, item in sort_aspect:
            cur_group_id = id_group_dict[cur_id]

            # TODO 如果为True 即表示为标签，则不再处理了
            if index2result[cur_id]:
                continue

            index2result[cur_id] = group_result_dict[cur_group_id]

        return index2result


if __name__ == '__main__':
    com_checker = LabelComponentChecker(use_dict=False)
    content = """细腻，维E和透明质酸钠等成分有效保湿及养护唇部肌肤。丝滑细腻，维E和透明质酸钠等成分有效保湿及养护唇部肌肤。"""
    aspect_list = [{'aspect': '维E', 'start': 3, 'end': 5},
                   {'aspect': '透明质酸钠', 'start': 6, 'end': 11},
                   {'aspect': '维E', 'start': 31, 'end': 33},
                   {'aspect': '透明质酸钠', 'start': 34, 'end': 39},
                   ]

    # print(content[3: 5], content[6: 11], content[31: 33], content[34: 39])
    result = com_checker.predict(content, aspect_list)
    print(result)

