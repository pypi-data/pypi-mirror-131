# -*- coding:utf-8 -*-
from datetime import datetime

from lavda.util.panda_tool import PandaTool
from lavda.util.file_tool import FileTool
from lavda.util.time_util import TimeTool

from lavda.backexcutor.analysis_interface import *
from lavda.backexcutor.my_base_executor import *
from lavda.backexcutor.task import *
from lavda.backexcutor.my_data_loader import *


class DfExecutor(BaseExecutor):
    """
    基于DataFrame的数据处理框架
    """

    def __init__(self, max_lines=700000, jobs=1, mode=0, job_batch_size=1000, channel_col="channel"):
        """

        :param max_lines:int 单个文件保存的最大数据量（行数）
        :param jobs:int 并行数量
        :param mode:int 并行工作模式 ，jobs大于1时有作用 多线程貌似没啥用
                    0：joblib 多进程
                    1：joblib 多线程
                    3：threading 多线程
        :param job_batch_size:int mode=0时，单个job单批处理的最大数据量
        :param channel_col:string channel字段名
        """
        super(DfExecutor, self).__init__(channel_col, max_lines)

        self.max_lines = max_lines
        self.jobs = jobs
        self.mode = mode
        self.job_batch_size = job_batch_size

    def run_process(self, df_input, task_param_list, task_meta, statis_output_path, params=None):
        """
        核心运行代码
        :param df_input: DataFrame，待处理数据
        :param task_param_list: list(TaskParam)，任务列表
        :param task_meta:
        :param statis_output_path: string，统计类Task结果输出目录
        :param params: dict，运行参数
        :return:
        """
        task_time_list = list()
        for task_param_object in task_param_list:
            # todo 统计各任务执行时间
            begin_time = datetime.now()
            # 行接口可以并行处理
            if isinstance(task_param_object.processor, RowInterface):
                # todo 校验输入，输入字段不存在则不执行此任务
                skip = False
                if task_param_object.input_column:
                    cur_column = set(PandaTool.get_column(df_input))
                    for col in task_param_object.input_column:
                        if col not in cur_column:
                            skip = True
                            break
                if skip:
                    continue
                # 处理行功能
                df_input = self.run_row_task(df_input, task_param_object, task_meta)
                # todo 清洗类规则处理完后直接把清洗掉
                if task_param_object.output_column:
                    for clean_column in task_param_object.output_column:
                        if 'tag_clean' in clean_column:
                            df_input = df_input[df_input[clean_column] == 0]
                            df_input.drop(columns=[clean_column], inplace=True)
            else:
                df_input = self.process_df_task(df_input, task_param_object, statis_output_path)
                # todo 清洗类规则处理完后直接把清洗掉
                if task_param_object.output_column:
                    for clean_column in task_param_object.output_column:
                        if 'tag_clean' in clean_column:
                            df_input = df_input[df_input[clean_column] == 0]
                            df_input.drop(columns=[clean_column], inplace=True)

            end_time = datetime.now()
            run_time = TimeTool.epoch_seconds(begin_time, end_time)
            one_task_time = dict()
            one_task_time['start'] = begin_time.strftime('%Y-%m-%d %H:%M:%S')
            one_task_time['end'] = end_time.strftime('%Y-%m-%d %H:%M:%S')
            one_task_time['runTime'] = round(float(run_time), 3)
            one_task_time['class'] = task_param_object.name
            one_task_time['inputColumn'] = task_param_object.input_column

            task_time_list.append(one_task_time)

        task_meta['taskTime'] = task_param_list
        return df_input

    def count_data_meta(self, df_input):
        """
        统计输入数据相关内容
        :param df_input:
        :return:
        """
        data_meta = dict()
        data_meta['count'] = df_input.shape[0]
        data_meta['fieldCount'] = df_input.shape[1]

        return data_meta

    def load_data(self, data_source, merge_task_object, suffix, task_meta):
        """
        数据源
            如果是数据库，就是一个表名，类型是字符串，
            如果是文件，就是一个文件夹，类型是字符串，获取文件夹下所有文件作为数据源
            {'type': 'db','name':'table'}
            {'type': 'file','name':'folder'}
        :param data_source:
        :param merge_task_object:
        :param suffix:
        :param task_meta:
        :return:
        """
        # TODO 原来这里写的是从文件里面加载数据，添加个从数据库里家在数据
        # TODO 文件夹返回的dataframe，数据库加载数据返回的是字典，看要不要都改了
        data_source_type = data_source['type']
        input_path = data_source['name']
        if data_source_type == 'db':
            df_input = DaDataLoader.load_from_db(input_path, merge_task_object)
        else:
            df_input = DaDataLoader.load_from_file(input_path, merge_task_object, suffix)
            task_meta['data'] = self.count_data_meta(df_input)

        return df_input

    def save_result(self, df_result, task_meta, output_source):
        # TODO 原来这里写的是往文件里面写数据，添加个往数据库里写数据
        # todo 这里可以就把结果放在表里，把写入文件单独列个功能
        print("***********************************************************")
        print("***********************************************************")
        print("***********************************************************")
        print("***********************************************************")
        print("***********************************************************")
        print('df_result', df_result)
        if output_source is not None:

            data_source_type = output_source['type']
            output_path = output_source['name']
            if data_source_type == 'file':
                # 返回存储结果的状态
                status = DaDataSave.save_to_file(output_path, df_result, task_meta)
                return status
            elif data_source_type == 'db':
                status = DaDataSave.save_to_db(output_path, df_result)
                return status

    def run_row_task(self, df_input, task_param_object, task_meta):
        # print('df_input',df_input)
        # print('task_meta',task_meta)
        # print('task_param_object',task_param_object)
        # 实际执行处理任务
        if self.jobs > 1:
            all_line_result = self._parallel_row_process(df_input, task_param_object, task_meta, self.jobs)
        else:
            all_line_result = self._single_row_process(df_input, task_param_object, task_meta)

        # 处理结果添加到原有数据集上
        output_column = task_param_object.output_column
        if len(output_column) == 1:
            df_input[output_column[0]] = all_line_result
        else:
            for i, one_column in enumerate(output_column):
                one_column_result = [item[i] for item in all_line_result]
                df_input[one_column] = one_column_result
        return df_input

    def _single_row_process(self, df_input, task_param_object, task_meta):
        """
        串行处理数据
        :param df_input: DataFrame，待处理数据
        :param task_param_object: list(TaskParam)，任务列表
        :param task_meta: dict,任务元数据
        :return:
        """
        # 将数据转换为列表
        # print('df_input', df_input)
        data_list = gl_format_df_data(df_input)
        all_line_result = [gl_process_line_fun(task_param_object, line_data, task_meta) for line_data in data_list]

        return all_line_result

    def _parallel_row_process(self, df_input, task_param_object, task_meta, jobs):
        """
        并行数据处理，感觉没必要
        :param df_input: DataFrame，待处理数据
        :param task_param_object:list(TaskParam)，任务列表
        :param jobs: int，并发数量
        :return:
        """
        # 将数据转换为列表
        data_list = gl_format_df_data(df_input)
        return


def gl_format_df_data(df_input):
    """
    格式化dataframe 数据为python list
    因为DataFrame的遍历操作不如list快
    :param df_input:
    :return:
    """
    data_list = df_input.to_dict(orient="records")
    data_list = [gl_clean_line_dict(item) for item in data_list]

    return data_list
