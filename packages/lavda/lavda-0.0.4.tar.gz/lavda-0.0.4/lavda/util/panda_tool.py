# -*- coding:utf-8 -*-
"""
pandas 相关操作
"""
from __future__ import print_function
from __future__ import absolute_import

import pandas as pd
import os
import xlsxwriter
from lavda.util.file_tool import FileTool


class PandaTool(object):
    @staticmethod
    def read_more(input_data, sheet_name=0, header=0, dtype="str"):
        if isinstance(input_data, str):
            df_input = PandaTool.read(input_data, sheet_name=sheet_name, header=header, dtype=dtype)
        else:
            # 默认为DataFrame
            df_input = input_data

        return df_input

    @staticmethod
    def read(input_file_path, sheet_name=0, header=0, dtype="str", file_match_mode="one"):
        """

        :param input_file_path: string，文件名
        :param sheet_name: string，sheet名
        :param header: int，header是否为title
        :param dtype: string or None
        :param file_match_mode: string,文本匹配模式
                    one:完全匹配一个文件名
                    many-sheet:一个文件的多个sheet,合并为一个dataframe
                    many-sheet-list: 不合并
                    many-file:多个文件，多个dataframe合并为一个dataframe, 使用一个input_file_path作为前缀，
                            例如：input_file_path="test.xlx", 无法完全匹配时，test_1.xlsx, test_2.xlsx文件都会被加载使用
                    many-file-list:不合并
        :return:
        """
        # TODO pd.ExcelFile还不知怎么使用dtype
        if file_match_mode == "one":
            df_result = PandaTool.load_one_file(input_file_path, sheet_name, header, dtype)
        elif file_match_mode == "many-sheet":
            # 多sheet模式
            excel_reader = pd.ExcelFile(input_file_path)  # 指定文件
            sheet_names = excel_reader.sheet_names  # 读取文件的所有表单名，得到列表

            df_list = list()
            # TODO 以第一个sheet为基准，只有columns全都一样的才会加载到一起
            first_columns = None
            for i, sheet_name in enumerate(sheet_names):
                if sheet_name.startswith("Sheet"):
                    continue
                df_data = excel_reader.parse(
                    sheet_name=i, header=header)
                if df_data.shape[0] <= 0:
                    continue
                if i == 0:
                    first_columns = set(df_data.columns)
                else:
                    if first_columns is None:
                        continue
                    # TODO 判断列名是否是一样的
                    cur_columns = set(df_data.columns)
                    if len(first_columns) != len(cur_columns):
                        continue
                    same_count = [1 if i_key in first_columns else 0 for i_key in cur_columns]
                    if sum(same_count) != len(first_columns):
                        continue
                df_list.append(df_data)

            # 合并数据
            df_result = pd.concat(df_list, sort=False)

        elif file_match_mode == "many-file":
            # 多文件模式
            file_params_list = FileTool.get_file_path(input_file_path, suffix=[".xlsx", ".csv"])
            df_list = list()
            for file_path in file_params_list:
                df_one = PandaTool.load_one_file(file_path, sheet_name, header, dtype)
                df_list.append(df_one)

            df_result = pd.concat(df_list, sort=False)
        else:
            df_result = None

        return df_result

    @staticmethod
    def load_one_file(input_file_path, sheet_name=0, header=0, dtype="str"):
        parent_file_path, temp_file_name = os.path.split(input_file_path)
        file_name, extension = os.path.splitext(temp_file_name)
        extension = extension.lower()
        if extension.endswith("xlsx") or extension.endswith("xls"):
            df = pd.read_excel(input_file_path, header=header, sheet_name=sheet_name, dtype=dtype)
            # TODO 按字符串类型时，全部全值转为字符串
            if dtype is not None and dtype == "str":
                df.fillna(value="", inplace=True)

        elif extension.endswith("csv"):
            df = pd.read_csv(input_file_path, header=header, encoding='utf_8_sig')
        else:
            raise Exception("unknown file extension" + input_file_path)

        return df

    @staticmethod
    def save(output_file_path, df_content, max_line=1000000, index=False, file_match_mode="many-file"):
        """

        :param output_file_path: 输出文件路径
        :param df_content: DataFrame
        :param max_line: 最大行数据
        :param index: bool
        :param file_match_mode: string,文本匹配模式
                    many-sheet:一个文件的多个sheet
                    many-file:多个文件，使用一个input_file_path作为前缀，
                            例如：input_file_path="test.xlx", 无法完全匹配时，test_1.xlsx, test_2.xlsx文件都会被加载使用
        :return:
        """
        def get_batch_index(length, batch_size):
            index_list = list()
            start = 0
            while start < length:
                end = start + batch_size
                if end > length:
                    end = length
                index_list.append((start, end))
                start = end
            return index_list

        # 保存csv
        if output_file_path.endswith("csv"):
            df_content.to_csv(output_file_path, encoding='utf_8_sig', index=index)
        elif output_file_path.endswith("xlsx"):
            # 保存xlsx
            # TODO xlsx有行数限制，因此大数据文件要拆分
            line_count = df_content.shape[0]
            MAX_BATCH = max_line
            df_result_list = list()
            if line_count > MAX_BATCH:
                batch_list = get_batch_index(line_count, MAX_BATCH)
                parent_file_path, temp_file_name = os.path.split(output_file_path)
                file_name, extension = os.path.splitext(temp_file_name)
                for i, one_batch in enumerate(batch_list):
                    df_sub_content = df_content.iloc[one_batch[0]: one_batch[1]]
                    df_result_list.append(df_sub_content)

                if file_match_mode == "many-sheet":
                    t_df_list = [(str(ti), df_t_one) for ti, df_t_one in enumerate(df_result_list)]
                    PandaTool.save_many(output_file_path, t_df_list)
                else:
                    for i, df_sub_content in enumerate(df_result_list):
                        sub_output_file_path = os.path.join(parent_file_path, file_name + "_" + str(i) + extension)

                        writer = pd.ExcelWriter(sub_output_file_path, engine='xlsxwriter',
                                                options={'strings_to_urls': False})
                        df_sub_content.to_excel(writer, engine='xlsxwriter', index=index)
                        writer.save()

            else:
                writer = pd.ExcelWriter(output_file_path, engine='xlsxwriter',
                                        options={'strings_to_urls': False})
                df_content.to_excel(writer, engine='xlsxwriter', index=index)
                writer.save()
        else:
            raise Exception("unknown file extension" + output_file_path)

    @staticmethod
    def get_column(df):
        real_columns = list()
        cols = df.columns
        for key in cols:
            real_columns.append(str(key))

        return real_columns

    @staticmethod
    def drop_unnamed_column(df):
        real_column = PandaTool.get_column(df)
        select_column = [column for column in real_column if "Unname" not in column]
        df = df[select_column]

        return df

    @staticmethod
    def add_index(df, index_name):
        index_list = list()
        for index, row in df.iterrows():
            index_list.append(index)

        df[index_name] = index_list
        return df

    @staticmethod
    def save_many(output_file_path, df_many_data, index=False):
        """
        注意不能处理超行的问题
        :param output_file_path:
        :param df_many_data:
        :param index:
        :return:
        """
        writer = pd.ExcelWriter(output_file_path,
                                engine='xlsxwriter',
                                options={'strings_to_urls': False})
        if isinstance(df_many_data, (list, tuple)):
            for sheet_name, df in df_many_data:
                df.to_excel(writer, sheet_name=sheet_name, index=index)
        elif isinstance(df_many_data, dict):
            for sheet_name in df_many_data:
                df_many_data[sheet_name].to_excel(writer, sheet_name=sheet_name, index=index)
        else:
            raise Exception("unknown data type")
        writer.save()

    @staticmethod
    def drop_column(df, column_list):
        real_column = PandaTool.get_column(df)
        for column in column_list:
            real_column.remove(column)
        df = df[real_column]

        return df
