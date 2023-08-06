# -*- coding: utf-8 -*-
import os

import pandas as pd
from lavda.util.panda_tool import PandaTool
from lavda.util.file_tool import FileTool

from lavda.backexcutor.analysis_interface import *
from lavda.analysis.da_clean.df_distinct import DfDistinct

from lavda.backexcutor.task import TaskBuilder


class BaseExecutor(object):
    def __init__(self, channel_col="channel", max_lines=700000):
        self._task_meta = None
        self._max_lines = max_lines
        self._channel_col = channel_col

    @property
    def task_meta(self):
        return self._task_meta

    @task_meta.setter
    def task_meta(self, value):
        self._task_meta = value

    @property
    def max_lines(self):
        return self._max_lines

    @max_lines.setter
    def max_lines(self, value):
        self._max_lines = value

    @property
    def channel_col(self):
        return self._channel_col

    @channel_col.setter
    def channel_col(self, value):
        self._channel_col = value

    def run_flow(self,
                 config_flow,
                 input_source,
                 config_data_path,
                 output_source=None,
                 statis_output_path=None,
                 clean_result_prefix="tag_clean_"):
        """
        运行数据处理任务流
        :param config_flow: string or dict,配置文件或配置数据
                            (1) string:任务流配置文件
                            (2) dict：基于配置文件解析出来的任务流数据
        :param input_source: string, 输入数据, 可选值:
                                （1）文件目录： 此目录中所有的以suffix为后缀的文件都作为输入数据
                                 (2) 文件（須包含完整的路径）：单个文件作为数据
                                 (3) 文件列表（须包含完整的路径）：list/tuple(文件)
                                 （4） HiveSource
        :param config_path: string, 配置数据目录, 必须是已经存在的目录
                             此目录用以存放各个Task所需要的资源，
        :param output_source: 数据输出
                          (1)string,数据处理结果文件名,必须是包含完整路径的文件名
                            当最后处理结果一个文件存不下时，必自动存储为多个文件
                            以输入的文件名作为前缀
                                eg: /Download/output.xlsx, 实际结果可以为 output_1.xlsx, output_2.xlsx
                          （2）HiveSource
        :param statis_output_path: 统计类结果存储目录，目录不存在则自动构建
        :param clean_result_prefix:  string or None
                                   string: 是否对所有行处理功能(不包括清洗功能、创建过些功能)过虑清洗掉的数据
                                   None: 不过虑清洗的数据
        """

        # 1.校验输出目录
        if statis_output_path is not None:
            FileTool.make_dir(statis_output_path)
        run_params_dict = dict()
        run_params_dict['userCleanFilter'] = clean_result_prefix

        # 2.构建task
        task_builder = TaskBuilder()
        task_merge_object, task_other_list, task_meta = task_builder.build(config_flow, config_data_path, run_params_dict)
        self.task_meta = task_meta
        # 3.加载数据
        df_input = input_source
        # df_input = self.load_data(input_source, merge_task_object=task_merge_object, suffix='.xlsx',
        #                           task_meta=self.task_meta)

        # 4.运行任务、处理数据
        df_result = self.run_process(df_input, task_other_list, task_meta, statis_output_path)
        # todo 直接返回一个dataframe
        return df_result
        # 5.保存结果数据
        # 当只有统计类结果时，不需要再保存原始数据，因此没有数据更改
        # self.save_result(df_result, task_meta, output_source)
        # return True

    def load_data(self, input_path, merge_task_object, suffix, task_meta):
        """
        加载要处理的数据
        :param input_path: object
        :param merge_task_object: object，数据合并功能类
        :param suffix: string，文件后缀
        :param task_meta: dict，文件后缀
        :return:
        """
        raise NotImplemented

    def run_process(self, df_input, task_param_list, task_meta, static_output_path, params=None):
        """
        核心运行代码
        :param df_input: DataFrame,待处理数据
        :param task_param_list: list(TaskParam),任务列表
        :param task_meta: dict, 任务元数据
        :param static_output_path: string,统计类Task结果输出目录
        :param params: dict,其他运行参数
        :return:
        """
        raise NotImplemented

    def save_result(self, df_result, task_meta, output_path):
        """
        保存处理结果
        :param df_result: object，数据处理结果
        :param task_meta: dict，元数据
        :param output_path: string，结果输出文件路径/数据库表名
        :return:
        """
        raise NotImplemented

    def process_df_task(self, df_input, task_param_object, statis_out_path):
        """
        处理一些基于DataFrame的处理功能
        :param df_input: DataFrame，处理数据
        :param task_param_object: TaskParam，任务参数
        :param statis_out_path: string，统计结果输出目录
        :return: DataFrame，处理后的结果
        """
        if isinstance(task_param_object.processor, DfProcessInterface):
            # 基于DataFrame处理数据，单独处理
            df_input = task_param_object.processor.process(df_input)
        elif isinstance(task_param_object.processor, DfStatisInterface):
            # 统计功能，不改变原数据
            # todo 现有统计功能可能会修改原数据，因此要复制一份，这里得改！！！！！！！
            df_statis_input = df_input.copy(deep=True)
            df_statis_result = task_param_object.processor.process(df_statis_input)
            del df_statis_input

            s_output_file = task_param_object.output_file
            # 有分隔符代表可能是全路径，没有的只是文件名
            if statis_out_path is not None:
                if os.sep not in s_output_file:
                    s_output_file = os.path.join(statis_out_path, s_output_file)
                if isinstance(df_statis_result, dict):
                    PandaTool.save_many(s_output_file, df_statis_result, index=True)
                else:
                    PandaTool.save(s_output_file, df_statis_result, max_line=self.max_lines, index=True)
        return df_input

def gl_process_line_fun(task_param_object, line_data, task_meta):
    """
    全局通用处理函数，处理一行数据
    :param task_param_object:
    :param line_data: dict, 一行数据
    :return:
    """
    # 1.filter 检查
    if task_param_object.filters:
        for filter_object in task_param_object.filters:
            if filter_object.process((line_data, task_meta)):
                return task_param_object.processor.get_default_value()

    # 2.筛选需要的数据
    # TODO 不指定输入列时返回全部
    if task_param_object.input_column is None or len(task_param_object.input_column) <= 0:
        sel_line_data = line_data
    elif len(task_param_object.input_column) == 1:
        # TODO 只有一个字段时，返回非集合数据
        sel_line_data = line_data[task_param_object.input_column[0]]
    else:
        sel_line_data = {key: line_data[key] for key in task_param_object.input_column}

    # 3.处理数据
    result = task_param_object.processor.process(sel_line_data)

    return result


def gl_clean_line_dict(line_dict):
    """
    主要是清理空数据
    :param line_dict:
    :return:
    """
    line_dict = {key: line_dict[key] if not pd.isna(line_dict[key]) else None for key in line_dict}

    return line_dict