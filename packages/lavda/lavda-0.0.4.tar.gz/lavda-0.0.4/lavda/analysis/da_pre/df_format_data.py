# -*- coding:utf-8 -*-
"""
DataFrame 文件数据合并相差功能
"""
import os
import pandas as pd

from lavda.backexcutor.analysis_interface import *
from lavda.analysis.da_pre.create_data_index import *
from lavda.util.panda_tool import PandaTool
from lavda.util.mysql_util import LavwikiDfReader


class DfFormatData(DfMergeInterface):
    """
    根据channel将不同数据合并，同时设置索引
    """
    def __init__(self, index_column="", channel_column="channel"):
        self.index_column = index_column
        if channel_column:
            self.channel_column = channel_column
        else:
            self.channel_column = None
        self.merge_dict = dict()
        self.merge_st_names = list()

        # 从数据库加载映射表
        self.load_from_mysql()

    def load_from_mysql(self):
        """
        从数据库加载映射表
        :return:
        """
        df_input = LavwikiDfReader.read_table("config_merge")

        self._parse_from_df(df_input)

    def load_config_data(self, **config):
        """
        从文件加载映射表
        :param config:
        :return:
        """
        if not config:
            return
        if "mergeDictPath" not in config:
            return

        merge_dict_path = config['mergeDictPath']
        # TODO 输入的资源文件是可选的，主要还是使用数据库文件
        if not os.path.exists(merge_dict_path):
            return

        df_input = PandaTool.read(merge_dict_path)
        self._parse_from_df(df_input)

    def _parse_from_df(self, df_input):
        df_input = PandaTool.drop_unnamed_column(df_input)
        column_list = PandaTool.get_column(df_input)

        # TODO 第1列表示channel，其他列为各数据源字段
        channel_column = column_list[0]
        other_column = column_list[1:]
        result_dict = dict()
        for index, row in df_input.iterrows():
            channel_name = row[channel_column]
            if pd.isna(channel_name):
                # raise Exception("channel name is none, index =" + str(index))
                continue
            format_channel_name = channel_name

            result_dict[format_channel_name] = dict()

            for column_name in other_column:
                field_name = row[column_name]
                if pd.isna(field_name):
                    continue

                field_name = str(field_name).strip()
                if not field_name:
                    continue

                # TODO 对齐后标准名要去空格
                result_dict[format_channel_name][field_name] = str(column_name).strip()

        # 合并结果数据
        self.merge_dict.update(result_dict)
        for col in other_column:
            if col in self.merge_st_names:
                continue
            self.merge_st_names.append(col)

    def process(self, input_path, **params):
        """
        
        :param input_path: list(file_path), 必须是完整路径
        :return: 
        """
        file_params_list = input_path

        df_list = list()
        may_data_count = 0
        for file_path in file_params_list:
            parent_file_path, temp_file_name = os.path.split(file_path)
            file_name, extension = os.path.splitext(temp_file_name)

            channel = file_name.split("_")[1].strip().lower()
            # TODO 没有映射词表的不处理，不合并
            if channel not in self.merge_dict:
                raise Exception("can not merge data for channel = " + str(channel))
            # 保留标签类数据
            one_channel_dict = self.merge_dict[channel]
            df_input = PandaTool.read(file_path)
            # print("sub file path = ", file_path)
            # print("sub file shape = ", df_input.shape)
            may_data_count += df_input.shape[0]

            all_df_column = PandaTool.get_column(df_input)
            exist_map_dict = dict()
            not_exist_column = list()
            for col in all_df_column:
                if col in one_channel_dict:
                    exist_map_dict[col] = one_channel_dict[col]
                elif col in self.merge_st_names:
                    # TODO 已经是标准化的名字，也添加到里面，以保留
                    exist_map_dict[col] = col
                else:
                    not_exist_column.append(col)

            df_input.rename(columns=exist_map_dict, inplace=True)

            # TODO 筛选指定的数据列，不在词典中的列一律删掉
            df_input = df_input[list(exist_map_dict.values())]
            df_list.append(df_input)

            # 填充channel
            if self.channel_column:
                df_input[self.channel_column] = channel

        df_result = pd.concat(df_list, sort=False)
        # print("label result shape:", df_result.shape)
        real_data_count = df_result.shape[0]
        if real_data_count != may_data_count:
            raise Exception("data merge error, last total count error")

        # TODO 对于存在于词表中，但不存在于数据中的列，填充空数据
        new_column = PandaTool.get_column(df_result)
        fill_columns = [col for col in self.merge_st_names if col not in new_column]
        for column in fill_columns:
            df_result[column] = None

        # TODO 生成数据id
        data_index_object = CreateDataIndex()
        if self.index_column:
            df_result[self.index_column] = [data_index_object.process() for _ in range(real_data_count)]

        df_result = df_result[self.merge_st_names]

        return df_result


if __name__ == "__main__":
    DfFormatData()
    DfFormatData.load_config_data(None)
