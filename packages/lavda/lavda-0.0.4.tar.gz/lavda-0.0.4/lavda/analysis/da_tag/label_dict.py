# -*- coding: utf-8 -*-
# ----------------------------------------------
# purpose : 
# author : LGD
# create_time : 2021/2/1 16:37
# update_time : 2021/2/1 16:37
# copyright : Lavector
# ----------------------------------------------
import os
import pandas as pd
import xlrd
from typing import List, Optional

from lavda.util.panda_tool import PandaTool
from lavda.analysis.da_tag.label_util import LabelUtil


class LabelExcelMerge(object):
    def process(self, input_file_path, sheet_name=None):
        workbook = xlrd.open_workbook(input_file_path)

        # 获取所有sheet
        # print('打印所有sheet:', workbook.sheet_names())
        if not sheet_name:
            target_sheet = workbook.sheet_by_index(0)  # sheet索引从0开始
        else:
            target_sheet = workbook.sheet_by_name(sheet_name)
        rows_num = target_sheet.nrows
        cols_num = target_sheet.ncols

        # print(target_sheet.merged_cells)
        total_data_list = list()
        for r in range(rows_num):
            line_data_list = list()
            for c in range(cols_num):
                cell_value = target_sheet.row_values(r)[c]
                # print('第%d行第%d列的值：[%s]' % (r, c, sheet2.row_values(r)[c]))
                if cell_value is None or cell_value == '':
                    cell_value = (self.get_merged_cells_value(target_sheet, r, c))
                line_data_list.append(cell_value)

            total_data_list.append(line_data_list)

        return total_data_list

    def get_merged_cells(self, sheet):
        """
        获取所有的合并单元格，格式如下：
        [(4, 5, 2, 4), (5, 6, 2, 4), (1, 4, 3, 4)]
        (4, 5, 2, 4) 的含义为：行 从下标4开始，到下标5（不包含）  列 从下标2开始，到下标4（不包含），为合并单元格
        :param sheet:
        :return:
        """
        return sheet.merged_cells

    def get_merged_cells_value(self, sheet, row_index, col_index):
        """
        先判断给定的单元格，是否属于合并单元格；
        如果是合并单元格，就返回合并单元格的内容
        :return:
        """
        merged = self.get_merged_cells(sheet)
        for rlow, rhigh, clow, chigh in merged:
            if row_index >= rlow and row_index < rhigh:
                if col_index >= clow and col_index < chigh:
                    cell_value = sheet.cell_value(rlow, clow)
                    # print('该单元格[%d,%d]属于合并单元格，值为[%s]' % (row_index, col_index, cell_value))
                    return cell_value
                    break
        return None


MULTI_LABEL_SEPARATOR = "|"


class LabelDictBase(object):
    def __init__(self, id2keyword, id2line, format_data, label_name):
        """
        :param id2keyword: dict, keyword id => keyword 文本
        :param id2line: dict, keyword id => keyword 关联信息，如父类等
        :param format_data: dataframe，标准化的、结构化的词典数据
        :param label_name: string,标签名
        """
        self._id2keyword = id2keyword
        self._id2line = id2line
        self._format_data = format_data
        self._label_name = label_name

        self._columns = list(format_data.columns)

        id2relation = dict()
        for kid in id2line:
            line = [id2line[kid][col] for col in self._columns]
            id2relation[kid] = line
        self._id2relation = id2relation

    @property
    def id2relation(self):
        return self._id2relation

    @property
    def columns(self):
        return self._columns

    @property
    def id2keyword(self):
        return self._id2keyword

    @property
    def id2line(self):
        return self._id2line

    @property
    def label_name(self):
        return self._label_name

    @property
    def format_data(self):
        return self._format_data


class TreeLabelDict(LabelDictBase):
    """
    树形结构词表
    """

    def __init__(self, id2keyword,
                 id2line,
                 format_data,
                 label_name,
                 level_count):
        super(TreeLabelDict, self).__init__(id2keyword, id2line, format_data, label_name)
        self.level_count = level_count


class MappingCollect(object):
    def __init__(self, mappings: List[LabelDictBase]):
        self._mappings = mappings

    @property
    def mappings(self):
        return self._mappings


class LineLabelDict(LabelDictBase):
    """
    以行为单位的标签词表
    """

    def __init__(self, id2keyword,
                 id2line,
                 format_data,
                 label_name):
        super(LineLabelDict, self).__init__(id2keyword, id2line, format_data, label_name)


class PandaLabelDictTool(object):
    LABEL_KEYWORD_COL = "keyword"

    def check_file(self, input_file_path, file_suffix):
        parent_file_path, temp_file_name = os.path.split(input_file_path)
        file_name, extension = os.path.splitext(temp_file_name)
        extension = extension.lower()
        extension = extension.replace(".", "")
        if extension in file_suffix:
            return True
        else:
            raise Exception("unsupport file extension = " + extension)

    def trans(self, total_data_list):
        """
        二维数据置换
        :param total_data_list:
        :return:
        """
        old_max_rows = len(total_data_list)
        old_max_column = 0
        for line in total_data_list:
            current_column = len(line)
            if current_column > old_max_column:
                old_max_column = current_column

        result_data_list = list()
        for i in range(old_max_column):
            sub_data_list = list()
            for j in range(old_max_rows):
                if i < len(total_data_list[j]):
                    sub_data_list.append(total_data_list[j][i])
                else:
                    # TODO 空值填充
                    sub_data_list.append(None)
            result_data_list.append(sub_data_list)

        return result_data_list

    def is_none_value(self, cell_value):
        if pd.isna(cell_value):
            return True
        tmp_cell_value = str(cell_value)
        if not tmp_cell_value:
            return True

        return False

    def drop_none_row(self, total_data_list):
        """
        删除全为None 或空值的行
        :param total_data_list:
        :return:
        """
        result_data_list = list()
        for line in total_data_list:
            is_delete = True
            for cell_value in line:
                if not self.is_none_value(cell_value):
                    is_delete = False
                    break
            if not is_delete:
                result_data_list.append(line)

        return result_data_list

    def drop_none_column(self, total_data_list):
        """
        删除全为None 或空值的行
        :param total_data_list:
        :return:
        """
        delete_column_index = set()
        column_data_list = self.trans(total_data_list)
        for i, line in enumerate(column_data_list):
            is_delete = True
            for cell_value in line:
                if not self.is_none_value(cell_value):
                    is_delete = False
                    break
            if is_delete:
                delete_column_index.add(i)

        result_data_list = list()
        for line in total_data_list:
            sub_list = list()
            for j, cell_value in enumerate(line):
                if j not in delete_column_index:
                    sub_list.append(cell_value)
            result_data_list.append(sub_list)

        return result_data_list

    def check_has_non_value(self, total_data_list):
        for i, line in enumerate(total_data_list):
            for j, cell_value in enumerate(line):
                if self.is_none_value(cell_value):
                    raise Exception("has non value" + ", line=" + str(i) + ", col=" + str(j))

    def drop_end_non_value(self, total_data_list, total_label_level):
        """
        除最后一级标签外， 删除末尾的连续 空值
        :param total_data_list:
        :return:
        """
        result_data = list()
        for i, line in enumerate(total_data_list):
            label_level = i + 1
            if label_level < total_label_level:
                del_list = list()
                data_index = len(line) - 1
                while data_index >= 0:
                    item = line[data_index]
                    if self.is_none_value(item):
                        del_list.append(data_index)
                    else:
                        break
                    data_index -= 1

                if del_list:
                    sub_list = line[0: del_list[len(del_list) - 1]]
                else:
                    sub_list = line
            else:
                sub_list = line
            result_data.append(sub_list)

        return result_data

    def load_all_from_file(self, dict_path) -> MappingCollect:
        """
        加载文件所有的词表
        :param dict_path:
        :return:
        """
        df_sheet = pd.read_excel(dict_path, None)
        sheets = list(df_sheet.keys())

        mapping = list()
        for sheet_name in sheets:
            if "-" in sheet_name:
                tmp_list = sheet_name.split("-")
                tmp_list = [item.strip() for item in tmp_list if item.strip()]
                if len(tmp_list) != 2:
                    raise Exception("unknown sheetname = " + str(sheet_name))
                label_name = tmp_list[0]
                dict_level = int(tmp_list[1])

                label_dict_object = self.load_tree_dict(
                    dict_path,
                    sheet_name=sheet_name,
                    header=False,
                    tree_format=0,
                    total_label_level=dict_level,
                    label_name=label_name,
                    split_text=False)
            else:
                label_name = sheet_name
                label_dict_object = self.load_line_dict(dict_path, label_name=label_name, sheet_name=sheet_name)

            mapping.append(label_dict_object)

        mc = MappingCollect(mapping)

        return mc

    def load_tree_dict(self, input_file_path,
                       sheet_name=None,
                       tree_format=0,
                       header=False,
                       total_label_level=5,
                       label_name=None,
                       split_text=False):
        """

        :param input_file_path: string, 输入文件路径
        :param sheet_name: string, sheet name
        :param tree_format: int, 格式，0：竖形树， 1：横着的树
        :param header: bool, 是否有表头，默认不保留表头信息
        :param total_label_level: int, 标签词典级别
        :param label_name: string, 标签词典级别
        :param split_text: bool, 最后一级是否需要拆分文本
        :return:
        """
        # 1.校验输入文件
        file_suffix = ['xlsx', 'xls']
        self.check_file(input_file_path, file_suffix)

        # 2.处理合并单元格
        excel_merge = LabelExcelMerge()
        dict_array = excel_merge.process(input_file_path, sheet_name=sheet_name)

        # 检查是否有表头
        # TODO 默认不需要表头数据
        if header:
            # 需要去掉表头数据
            dict_array = dict_array[1:]

        # 3.横排的要做转置
        if tree_format == 1:
            # 矩阵转换，横排的要做转换
            dict_array = self.trans(dict_array)

        # 4. 清理
        # 除最后一级外，删除所有行末尾的空值
        dict_array = self.drop_end_non_value(dict_array, total_label_level)
        dict_array = self.drop_none_row(dict_array)
        dict_array = self.drop_none_column(dict_array)

        # 除最后一级外，没能有空值
        if total_label_level > 1:
            self.check_has_non_value(dict_array[0: total_label_level - 1])

        # 以第一行为标准确定完整的列数
        max_column_count = len(dict_array[0])

        # 6. 加载词典信息
        # 全局信息
        cell_pos_dict = dict()
        # 记录最后一级以外的父节点信息
        cell_pos_list = list()

        label_id_dict = dict()
        total_label_id_count = 0

        for i, line in enumerate(dict_array):
            current_level = i + 1
            if current_level > total_label_level:
                current_level = total_label_level
            parent_level = current_level - 1

            sub_pos_list = list()
            cell_pos_list.append(sub_pos_list)
            for j, cell_value in enumerate(line):
                # 超过最大列的不处理
                if j >= max_column_count:
                    continue

                if pd.isna(cell_value):
                    sub_pos_list.append(None)
                    continue
                cell_value = str(cell_value).strip()
                if not cell_value:
                    sub_pos_list.append(None)
                    continue

                if current_level == 1:
                    parent_label_id = -1
                    parent_label_item = None
                else:
                    parent_label_item = cell_pos_list[parent_level - 1][j]
                    if parent_label_item is None:
                        raise Exception("parent is None: line=" + str(i) + ", row" + str(j))
                    parent_label_id = parent_label_item['id']

                # TODO 只对最后一级作拆分
                if current_level == total_label_level and split_text:
                    sub_cell_value_list = cell_value.split("|")
                    sub_cell_value_list = [sub_value.strip() for sub_value in sub_cell_value_list if sub_value.strip()]

                    for sub_cell_value in sub_cell_value_list:
                        pos_value = str(parent_label_id) + "-" + str(current_level) + "-" + sub_cell_value
                        if pos_value in cell_pos_dict:
                            sub_pos_list.append(cell_pos_dict[pos_value])
                            continue

                        new_label_item = dict()
                        new_label_item['id'] = total_label_id_count
                        new_label_item['level'] = current_level
                        new_label_item['parent'] = parent_label_id
                        new_label_item['text'] = sub_cell_value
                        cell_pos_dict[pos_value] = new_label_item
                        sub_pos_list.append(new_label_item)

                        label_id_dict[new_label_item['id']] = new_label_item

                        total_label_id_count += 1

                else:
                    pos_value = str(parent_label_id) + "-" + str(current_level) + "-" + cell_value
                    if pos_value in cell_pos_dict:
                        sub_pos_list.append(cell_pos_dict[pos_value])
                        continue

                    new_label_item = dict()
                    new_label_item['id'] = total_label_id_count
                    new_label_item['level'] = current_level
                    new_label_item['parent'] = parent_label_id
                    new_label_item['text'] = cell_value
                    cell_pos_dict[pos_value] = new_label_item
                    sub_pos_list.append(new_label_item)
                    label_id_dict[new_label_item['id']] = new_label_item

                    total_label_id_count += 1

        # 转在标准格式
        list_data = self._format_dict2list(label_id_dict, total_label_level)
        format_data = self._format_list2df(list_data, label_name, total_label_level)

        format_data = self.clean_keyword(format_data, label_name)
        id2keyword, id2line = self.build_keyword_mapping(format_data, label_name)

        label_dict_object = TreeLabelDict(id2keyword, id2line, format_data, label_name, total_label_level)

        return label_dict_object

    def _format_list2df(self, result, label_name, label_level):
        """

        :param result:
        :param name:
        :param label_level:
                title 格式eg: 消费者(level1) 消费者(level2) 消费者(level3) 消费者(keyword)  消费者(id)
        :return:
        """
        columns = [str(label_name) + "(level%s)" % i for i in range(1, label_level)]
        columns = columns + [PandaLabelDictTool.build_keyword_column(label_name),
                             PandaLabelDictTool.build_id_column(label_name)]
        df = pd.DataFrame(result, columns=columns)

        return df

    def _format_dict2list(self, r_dict, max_level):
        l_tup = sorted(r_dict.items(), key=lambda item: item[0], reverse=True)
        r_list = []

        for k, v in l_tup:
            result = []
            if v["level"] == max_level:
                result.append(v["id"])
                result.append(v["text"])
                self._recursion(r_dict, result, v["parent"])
                r_list.append(result[::-1])
        return r_list

    def _recursion(self, r_dict, result, id):
        ps = r_dict[id]
        text, parent = ps["text"], ps["parent"]
        result.append(text)
        if parent in r_dict:
            self._recursion(r_dict, result, parent)

    def _load_dict_file(self, input_file_path, sheet_name, header=0):
        if isinstance(input_file_path, str):
            parent_file_path, temp_file_name = os.path.split(input_file_path)
            file_name, extension = os.path.splitext(temp_file_name)
            extension = extension.lower()
            if extension.endswith("xlsx") or extension.endswith("xls"):
                df_input = pd.read_excel(input_file_path, header=header, sheet_name=sheet_name)
            elif extension.endswith("csv"):
                df_input = pd.read_csv(input_file_path, header=header)
            else:
                raise Exception("unknown file extension" + input_file_path)
        else:
            # 默认为DataFrame
            df_input = input_file_path

        return df_input

    @staticmethod
    def build_id_column(label_name):
        return str(label_name) + "(id)"

    @staticmethod
    def build_keyword_column(label_name):
        return str(label_name) + "({})".format(PandaLabelDictTool.LABEL_KEYWORD_COL)

    @staticmethod
    def rename_line_dict(df_input, label_name):
        input_columns = df_input.columns
        col_dict = dict()
        for col in input_columns:
            col_dict[col] = str(label_name) + "(" + col + ")"
        df_input.rename(columns=col_dict, inplace=True)
        return df_input

    def load_line_dict(self, input_file_path,
                       sheet_name=None,
                       keyword_column='keyword',
                       label_name=""
                       ):
        """

        :param input_file_path:
        :param label_name: 标签名
        :param keyword_column: 关键词列名

        :param sheet_name: sheet name 列名0000000000000000

        :return:
        """
        df_input = self._load_dict_file(input_file_path, sheet_name)

        df_input = PandaTool.drop_unnamed_column(df_input)

        column_list = PandaTool.get_column(df_input)
        column_list = [i.replace(" ", "").lower() for i in column_list]
        df_input.columns = column_list

        if keyword_column not in column_list:
            raise Exception("can not find {} columns!".format(keyword_column))

        # TODO keyword 再改名
        columns_dict = {keyword_column: PandaLabelDictTool.LABEL_KEYWORD_COL}
        df_input.rename(columns=columns_dict, inplace=True)

        df_input = PandaLabelDictTool.rename_line_dict(df_input, label_name)
        # 生成id
        count = df_input.shape[0]
        id_list = list(range(1, count+1))
        id_column = PandaLabelDictTool.build_id_column(label_name)
        df_input[id_column] = id_list

        df_input = self.clean_keyword(df_input, label_name)
        id2keyword, id2line = self.build_keyword_mapping(df_input, label_name)

        label_dict_object = LineLabelDict(id2keyword, id2line, df_input, label_name)

        return label_dict_object

    def clean_keyword(self, df_format_data, label_name):
        """
        keyword 数据清洗
        :param df_format_data:
        :param label_name:
        :return:
        """
        keyword_column = PandaLabelDictTool.build_keyword_column(label_name)
        # df_format_data[keyword_column] = df_format_data[keyword_column].apply(lambda line: str(line).replace(" ", "").lower())
        df_format_data[keyword_column] = df_format_data[keyword_column].apply(
            LabelUtil.clean_dict_cell)
        return df_format_data

    def build_keyword_mapping(self, df_format_data, label_name):
        """
        构建相关的关联映射关系
        :param df_format_data:
        :param label_name:
        :return:
        """
        dict_data = df_format_data.to_dict(orient="records")
        id_column = PandaLabelDictTool.build_id_column(label_name)
        keyword_column = PandaLabelDictTool.build_keyword_column(label_name)

        id2keyword = dict()
        id2line = dict()
        for line in dict_data:
            id2keyword[line[id_column]] = line[keyword_column]
            id2line[line[id_column]] = line

        return id2keyword, id2line
