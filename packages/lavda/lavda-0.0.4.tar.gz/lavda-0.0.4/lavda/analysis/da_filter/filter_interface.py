# -*- coding: utf-8 -*-
# ----------------------------------------------
# purpose : 
# author : 
# create_time : 2020/7/2 14:34
# update_time : 2020/7/2 14:34
# copyright : Lavector
# ----------------------------------------------


class RowFilterInterface(object):
    def process(self, data, **params):
        """
        高层接口
        行数据过虑接口，配置行数据处理功能
        :param data:list(line, task_meta)
                line: dict, 当前行数据
                task_meta: dict, 运行任务的元数据
        :param params: dict, 输入参数
        :return: bool
        """
        pass
