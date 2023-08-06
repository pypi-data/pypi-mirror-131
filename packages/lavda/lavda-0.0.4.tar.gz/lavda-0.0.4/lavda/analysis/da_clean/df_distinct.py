# -*- coding: utf-8 -*-
# ----------------------------------------------
# purpose : 去重
# author : 
# create_time : 2020/6/30 14:43
# update_time : 2020/6/30 14:43
# copyright : Lavector
# ----------------------------------------------
from lavda.analysis.common import parse_multi_column
from lavda.analysis.da_clean.clean_interface import *
from lavda.backexcutor.analysis_interface import *


class DfDistinct(DfProcessInterface, CleanInterface):
    def __init__(self, input_column=None, output_column=None):
        """

        :param input_column: string, 去重字段
        :param output_column: string, 去重字段
        """
        self.result_column = output_column
        self.input_column_list = parse_multi_column(input_column)

    def process(self, data, **params):
        drop_dup_tags = data.duplicated(self.input_column_list, keep='first').astype(int)
        data[self.result_column] = drop_dup_tags

        return data
