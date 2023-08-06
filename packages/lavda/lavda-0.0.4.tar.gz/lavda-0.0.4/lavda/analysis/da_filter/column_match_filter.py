# -*- coding: utf-8 -*-
# ----------------------------------------------
# purpose : 
# author : 
# create_time : 2020/7/2 16:07
# update_time : 2020/7/2 16:07
# copyright : Lavector
# ----------------------------------------------
import re

from lavda.analysis.da_filter.filter_interface import RowFilterInterface


class ColumnNotMatchFilter(RowFilterInterface):
    def __init__(self, input_data):
        tmp_list = input_data.split("=")
        t_key = tmp_list[0]
        t_value_str = tmp_list[1]
        t_value_list = re.split('[,，]', t_value_str)
        t_value_list = [item.strip() for item in t_value_list if item.strip()]

        self.name = t_key
        self.values = set(t_value_list)

    def process(self, data, **params):
        line, _ = data

        if line[self.name] not in self.values:
            return True

        return False
