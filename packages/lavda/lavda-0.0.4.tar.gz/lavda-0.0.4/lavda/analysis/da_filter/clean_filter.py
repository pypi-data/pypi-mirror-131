# -*- coding: utf-8 -*-
# ----------------------------------------------
# purpose : 过虑清洗数据
# author : 
# create_time : 2020/7/2 14:19
# update_time : 2020/7/2 14:19
# copyright : Lavector
# ----------------------------------------------
from lavda.analysis.da_filter.filter_interface import RowFilterInterface
from lavda.analysis.da_clean.clean_interface import CleanFlag


class CleanFilter(RowFilterInterface):
    def __init__(self, clean_result_prefix):
        """
        清洗功能输出结果字段的前缀，用以判断哪些是清洗的结果
        :param clean_result_prefix:
        """
        self.clean_result_prefix = clean_result_prefix

    def process(self, data, **params):
        """

        :param data: list(dict())
        :param params:
        :return:
        """
        line_dict, task_meta = data

        # 获取清洗结果的字段名
        clean_output_key = [key for key in line_dict.keys() if key.startswith(self.clean_result_prefix)]

        clean_result = [int(line_dict[key]) for key in line_dict if key in clean_output_key and line_dict[key] is not None]
        clean_result = set(clean_result)

        if int(CleanFlag.YES) in clean_result:
            return True

        return False



