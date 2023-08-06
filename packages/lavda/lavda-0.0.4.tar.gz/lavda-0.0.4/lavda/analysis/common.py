# -*- coding: utf-8 -*-
# ----------------------------------------------
# purpose : 
# author : 
# create_time : 2020/7/15 16:28
# update_time : 2020/7/15 16:28
# copyright : Lavector
# ----------------------------------------------


def parse_multi_column(field_str):
    """
    解析字段名，由于配置文件是字符串，因此要转换成需要的list格式
    :param field_str: string
    :return: list(string)
    """
    if field_str is None:
        return list()
    column_list = field_str.split(",")
    column_list = [item.strip() for item in column_list if item.strip()]

    return column_list
