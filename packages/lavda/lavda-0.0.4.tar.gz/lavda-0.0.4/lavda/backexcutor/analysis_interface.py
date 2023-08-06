# -*- coding:utf-8 -*-
"""
分析处理任务能用接口
"""


class TaskInterface(object):
    def process(self, data, **params):
        """
        高层接口
        任务处理接口
        :param data:任意数据，由底层接口定义
        :param params: dict, 输入参数
        :return: 由底层接口定义
        """
        pass

    def load_config_data(self, **config):
        """
        加载配置文件数据
        :param config:
            格式：配置资源名=> 资源文件名/资源文件完整路径
        :return:
        """
        pass


class RowInterface(TaskInterface):
    """
    核心接口

    """
    def __init__(self, default_value=None):
        self.default_value = default_value

    def get_default_value(self):
        return self.default_value

    def process(self, data, **params):
        """
        以行为单位的数据处理接口
        核心功能接口
        :param data: python基础数据类型，如int, str, dict, 输入数据
        :param params: dict, 输入参数
        :return: 返回数据依赖具体功能
        """
        pass


class DfInterface(TaskInterface):
    """
    高层接口
    实体功能类不要继承此接口
    """
    pass


class DfProcessInterface(DfInterface, TaskInterface):
    def process(self, data, **params):
        """
        核心接口
        基于DataFrame的数据处理接口
        :param data: DataFrame, 输入数据
        :param params: dict, 输入参数
        :return: DataFrame
        """
        pass


class DfStatisInterface(DfInterface, TaskInterface):
    def process(self, data, **params):
        """
        核心接口
        基于DataFrame的数据统计类接口
        不会修改输入数据，只会生成新的统计数据
        :param data: DataFrame
        :param params: dict, 输入参数
        :return: DataFrame 或 dict(name==> DataFrame)， 输出统计结果
        """
        pass


class DfMergeInterface(DfInterface, TaskInterface):
    """
    核心接口
    只有数据合并类才继承此接口
    """
    def process(self, data, **params):
        """

        :param data: 目录/文件名
        :param params:
        :return: DataFrame，合并结果
        """
        pass
