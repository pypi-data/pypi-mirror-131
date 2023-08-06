# -*- coding:utf-8 -*-
"""
文件相关操作
"""
from __future__ import print_function
from __future__ import absolute_import

import os
import shutil
import json
import pickle
import codecs
import pandas as pd
# import csv


class FileTool(object):
    @staticmethod
    def get_parent_dir(entire_path):
        return os.path.dirname(entire_path)

    @staticmethod
    def get_base_name(entire_path):
        """
        提取完整路径的文件名或目录名
        :param entire_path:
        :return:
        """
        return os.path.basename(entire_path)

    @staticmethod
    def rm_file(path):
        """
        删除文件或目录
        :param path:
        :return:
        """
        if not os.path.exists(path):
            return
        if os.path.isfile(path):
            os.remove(path)
        elif os.path.isdir(path):
            # os.rmdir(path)
            shutil.rmtree(path)

    @staticmethod
    def make_dir(path):
        """
        创建目录，可以递归
        :param path:
        :return:
        """
        if os.path.exists(path):
            return
        os.makedirs(path)

    @staticmethod
    def is_spam_file_name(file_name):
        """

        :param file_name: string,是否为垃圾文件名，不是完整路径，只是文件名
        :return:
        """
        if file_name.startswith(u'.') or file_name.startswith(u'~'):
            return True

        return False

    @staticmethod
    def get_all_file(dir_name, suffix=None, filter_file_name=True, recursion=True):
        """
        从文件夹或目录获取全部文件名(完整路径),不包含子目录
        :param dir_name:
        :param suffix: string or list 后缀名，如".txt"
        :param filter_file_name: bool,是否过虑隐形文件等
        :param recursion: bool,是否递归遍历
        :return: list(string)
        """
        suffix_list = None
        if suffix:
            if isinstance(suffix, (list, tuple, set)):
                suffix_list = suffix
            else:
                suffix_list = [suffix]

        fn_list = []
        for root, dirs, fns in os.walk(dir_name):
            if not recursion and root != dir_name:
                continue
            for fn in fns:
                # 校验后缀
                if suffix_list:
                    satisfy_suffix = False
                    for sub_suffix in suffix_list:
                        if fn.endswith(sub_suffix):
                            satisfy_suffix = True
                            break
                    if not satisfy_suffix:
                        continue
                # 过虑文件名
                if filter_file_name:
                    if FileTool.is_spam_file_name(fn):
                        continue
                temp_fn = os.path.join(root, fn)
                fn_list.append(temp_fn)

        return fn_list

    @staticmethod
    def get_file_path(input_path, suffix=None, recursion=False):
        """
        在指定目录获取指定文件名或以此文件名开头的文件的路径
        file_name 为空时，获取所有文件路径
        :param input_path: 目录名/文件名
        :param suffix: 文件后缀,输入为目录时有效
        :param recursion: 是否递归遍历,输入为目录时有效
        :return:
        """
        if os.path.isdir(input_path):
            all_file_path = FileTool.get_all_file(input_path, suffix=suffix, recursion=recursion)
            return all_file_path
        elif os.path.isfile(input_path):
            return [input_path]
        else:
            parent_file_path, temp_file_name = os.path.split(input_path)
            if not os.path.isdir(parent_file_path):
                raise Exception("invalid input = " + input_path)
            file_name_no_suffix, suffix = os.path.splitext(temp_file_name)

            # file_name_no_suffix, suffix = os.path.splitext(temp_file_name)
            if not suffix:
                return list()
            all_file_path = FileTool.get_all_file(parent_file_path, suffix=suffix, recursion=recursion)

            all_file_path = [item for item in all_file_path if os.path.isfile(item)]
            all_file_name_dict = {FileTool.get_base_name(item): item for item in all_file_path}

            # 根据前缀匹配
            result_list = list()
            for name in all_file_name_dict:
                tmp_name = name.replace(suffix, "")
                tmp_name = tmp_name.replace(file_name_no_suffix, "")
                tmp_name = tmp_name.replace("_", "")
                if tmp_name.isdigit():
                    result_list.append(all_file_name_dict[name])
            return result_list

    @staticmethod
    def get_all_dir(dir_name):
        """
        从文件夹或目录获取全部子目录(完整路径),不包含子目录
        :param dir_name:
        :param suffix: 后缀名，如".txt"
        :return: list(string)
        """
        fn_list = []
        for root, dirs, fns in os.walk(dir_name):
            for d in dirs:
                temp_fn = os.path.join(root, d)
                fn_list.append(temp_fn)

        return fn_list

    @staticmethod
    def write(file_path, data, binary=False):
        """
        保存数据到文件
        :param file_path: 文件名
        :param data: 任意类型
        :param binary: 是否保存为二进制文件
        :return:
        """
        option = 'wb' if binary else 'w'
        with open(file_path, option) as fp:
            pickle.dump(data, fp)

    @staticmethod
    def read(file_path, binary=False):
        """
        加载模型
        :param file_path: 模型文件
        :param binary: 是否为二进制文件
        :return:
        """
        option = 'rb' if binary else 'r'
        with open(file_path, option) as fp:
            data = pickle.load(fp)

        return data

    @staticmethod
    def write_json(file_path, data):
        """
        保存页面信息
        :param file_path:
        :param data:
        :return:
        """
        path = open(file_path, u'w')
        json.dump(data, path)

    @staticmethod
    def read_json(file_path):
        """
        读取json数据
        :param file_path:
        :return:
        """
        if os.path.exists(file_path):
            path = open(file_path, 'r')
            return json.load(path)
        return None

    @staticmethod
    def read_by_line(file_path):
        """
        按行读取数据
        :param file_path:
        :return:
        """
        data_list = list()
        with codecs.open(file_path, 'r', encoding="utf-8") as fp:
            for line in fp:
                line = line.strip()
                if len(line) > 0:
                    data_list.append(line)

        return data_list

    @staticmethod
    def write_by_line(file_path, data):
        """
        按行读取数据
        :param file_path:
        :param data:
        :return:
        """
        data_len = len(data)  #
        with codecs.open(file_path, 'w', encoding="utf-8") as fp:
            for i, item in enumerate(data):
                fp.write(item)
                if i < data_len - 1:
                    fp.write(u"\n")

    @staticmethod
    def write_str(file_path, data):
        with codecs.open(file_path, 'w', encoding="utf-8") as fp:
            fp.write(data)

    @staticmethod
    def read_str(file_path):
        data = u""
        with codecs.open(file_path, 'r', encoding="utf-8") as fp:
            for line in fp:
                data += line

        return data

    @staticmethod
    def read_by_delimiter(file_path, delimiter):
        """
        读取通过分隔符分开的数据，每行一条，且不能重复
        如nam=davic
        :param file_path:
        :param delimiter:
        :return:
        """
        data_dict = dict()
        data = u""
        with codecs.open(file_path, 'r', encoding="utf-8") as fp:
            for line in fp:
                items = line.split(delimiter)
                if items is None:
                    continue
                if len(items) != 2:
                    continue
                key = items[0].strip()
                value = items[1].strip()
                data_dict[key] = value

        return data_dict

    @staticmethod
    def read_csv(file_path, has_header=False, user_columns=None, real_columns=None):
        # file_data = open(file_path)
        if has_header:
            # 默认使用第一行 encoding="utf8",
            excel_data = pd.read_csv(file_path)
        else:
            excel_data = pd.read_csv(file_path, header=None)
        if user_columns:
            excel_data.columns = user_columns
        if real_columns is not None:
            cols = excel_data.columns
            for key in cols:
                real_columns.append(key)
        for index, row in excel_data.iterrows():
            yield index, row

    @staticmethod
    def read_excel(file_path, sheet_name=None, has_header=False, user_columns=None, real_columns=None):
        """
        读取excel数据，有表头时(即has_header为True)，会跳过第一行，直接返回数据，不会返回表头信息
        :param file_path:
        :param sheet_name:  sheet
        :param has_header:  是否有列名, True时：
        :param user_columns: 是否使用自定义列名
        :param real_columns: 实际列名， list ，输出数据
        :return:
        """
        file_data = open(file_path)
        if has_header:
            # 默认使用第一行
            excel_data = pd.read_excel(file_data, sheet_name=sheet_name)
        else:
            excel_data = pd.read_excel(file_data, sheet_name=sheet_name, header=None)
        if user_columns:
            excel_data.columns = user_columns
        if real_columns is not None:
            cols = excel_data.columns
            for key in cols:
                real_columns.append(key)
        for index, row in excel_data.iterrows():
            yield index, row

    @staticmethod
    def write_to_excel(file_path, data_list, columns, sheet=None, index=False):
        """

        :param file_path: string
        :param data_list: list(list)
        :param columns: list
        :param sheet: string
        :param index: bool ，是否添加左侧第一列作为索引
        :return:
        """
        df = pd.DataFrame(data_list, columns=columns)
        excel_writer = pd.ExcelWriter(file_path)

        df.to_excel(excel_writer=excel_writer, sheet_name=sheet, index=index)
        excel_writer.save()


if __name__ == '__main__':
    result = FileTool.get_file_path("/Users/yuantian/Downloads/PyTorch中文手册/README.md")
    print(result)
    print(len(result))