# -*- coding: utf-8 -*-
# ----------------------------------------------
# purpose : 
# author : 
# create_time : 2020/7/1 16:19
# update_time : 2020/7/1 16:19
# copyright : Lavector
# ----------------------------------------------
import pandas as pd
import collections
import os
import xlrd
import pickle
import contextlib


class PandaLabelDictTool(object):
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

        label_dict_object = TreeLabelDict(label_id_dict, total_label_level, label_name)

        return label_dict_object


class LabelDictInterface(object):
    def set_data_column(self, data_column):
        """

        :param data_column: list   标签所对应的数据列名
        :return:
        """
        pass

    def get_data_column(self):
        pass

    def get_label_name(self):
        """
        标签名称
        :return:
        """
        pass

    def set_label_name(self, label_name):
        pass

    def get_label_id_dict(self):
        pass

    def get_item_by_id(self, label_id):
        pass

    def get_label_text_by_id(self, label_id):
        pass

    def get_last_labels_item(self):
        """
        获取最后一级label 信息,即实际用于打标签的内容
        :return:
        """
        pass

    def get_parent_label_text(self, label_id, include_me=True):
        pass

    def get_label_detail_column(self, include_label_id=True):
        """
        标签详细信息列名
        :param include_label_id:  是否包含最后一级label id
        :return:
        """

    def get_label_detail(self, label_id, include_label_id=True):
        """
        标签详细信息
        :param label_id:
        :param include_label_id:
        :return:
        """
        pass

    def get_column_prefix(self):
        """
        列名前缀，用于作为统计汇总使用
        :return:
        """
        return "la_"

    def print_all(self):
        pass

    def print_detail(self):
        pass

    def get_processor(self, processor):
        pass

    def set_processor(self):
        pass


class TreeLabelDict(LabelDictInterface):
    def __init__(self, label_id_dict, level_count, label_name=None):
        self.label_id_dict = label_id_dict
        self.level_count = level_count
        self.label_name = label_name

        # TODO 用于打标签的数据列名,暂时放在这里吧
        self.data_column = None
        # TODO 标签处理类，暂时放这里吧
        self.processor = None

    def set_processor(self, processor):
        self.processor = processor

    def get_processor(self):
        return self.processor

    def set_data_column(self, data_column):
        self.data_column = data_column

    def get_data_column(self):
        return self.data_column

    def get_label_name(self):
        return self.label_name

    def set_label_name(self, label_name):
        self.label_name = label_name

    def get_label_id_dict(self):
        return self.label_id_dict

    def get_level_count(self):
        return self.level_count

    def get_item_by_id(self, label_id):
        return self.label_id_dict[label_id]

    def get_label_text_by_id(self, label_id):
        return self.label_id_dict[label_id]['text']

    def get_parent_by_level(self, current_label_id, parent_level):
        """
        查找相应级别的父类标签
        :param current_label_id:
        :param parent_level:
        :return:
        """
        parent_id = self.label_id_dict[current_label_id]['parent']
        while parent_id >= 0:
            parent_item = self.label_id_dict[parent_id]
            if parent_item['level'] == parent_level:
                return parent_item
            parent_id = parent_item['parent']

        return None

    def get_last_labels_item(self):
        """
        获取最后一级label 信息,即实际用于打标签的内容
        :return:
        """
        label_item_list = list()
        for label_id in self.label_id_dict:
            label_item = self.label_id_dict[label_id]
            if label_item['level'] == self.level_count:
                label_item_list.append(label_item)

        return label_item_list

    def get_label_detail_column(self, include_label_id=True):
        column_list = list()
        label_level = self.get_level_count()
        for i in range(label_level):
            column_list.append(self.get_column_prefix() + self.label_name + "_" + str(i + 1))
        if include_label_id:
            column_list.append(self.get_column_prefix() + self.label_name + "_" + "id")

        return column_list

    def get_label_detail(self, label_id, include_label_id=True):
        detail_list = self.get_all_parent_label_text(label_id)
        if include_label_id:
            detail_list.append(label_id)

        return detail_list

    def get_all_parent_label_text(self, current_label_id, include_me=True):
        parent_list = list()
        parent_id = self.label_id_dict[current_label_id]['parent']
        while parent_id >= 0:
            parent_list.insert(0, self.label_id_dict[parent_id]['text'])
            parent_id = self.label_id_dict[parent_id]['parent']
        if include_me:
            parent_list.append(self.get_item_by_id(current_label_id)['text'])

        return parent_list

    def print_all(self):
        level_count_dict = {level + 1: 0 for level in range(self.level_count)}
        for label_id in self.label_id_dict:
            level_count_dict[self.label_id_dict[label_id]['level']] += 1
        print(level_count_dict)

    def print_detail(self):
        for label_id in self.label_id_dict:
            print(self.label_id_dict[label_id])

    def get_dict(self):
        return self.label_id_dict


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


def format_dict2list(r_dict):
    l_tup = sorted(r_dict.items(), key=lambda item: item[0], reverse=True)
    r_list = []
    max_num = 0
    for k, v in l_tup:
        if v["level"] > max_num:
            max_num = v["level"]
        result = []
        if v["level"] == max_num:
            result.append(v["text"])
            recursion(r_dict, result, v["parent"])
            r_list.append(result[::-1])
    return r_list


def recursion(r_dict, result, id):
    ps = r_dict[id]
    text, parent = ps["text"], ps["parent"]
    result.append(text)
    if parent in r_dict:
        recursion(r_dict, result, parent)


def au_get_tree2dict(filename, sheet_name, level):
    """
    返回数据库标准存储结构
    """
    dict_tool = PandaLabelDictTool()
    label_dict_object = dict_tool.load_tree_dict(
        filename,
        sheet_name=sheet_name,
        header=False,
        tree_format=0,
        total_label_level=level,
        label_name='beauty',
        split_text=False)
    r_dict = label_dict_object.get_dict()
    return r_dict


def format_list2df(result):
    max_len = 0
    for i in result:
        if len(i) > max_len:
            max_len = len(i)

    data = []
    for i in result:
        loss = max_len - len(i)
        tmp_data = i[:-1] + ["" for _ in range(loss)] + [i[-1].split("|")[0], i[-1]]
        data.append(tmp_data)

    max_len += 1
    df = pd.DataFrame(data)
    columns = ["level_%s" % i for i in range(1, max_len + 1)]
    columns[-2] = "keytag"
    columns[-1] = "keyword"
    df.columns = columns
    return df


def au_get_tree(infile, sheet, level, sheet_name):
    r_dict = au_get_tree2dict(infile, sheet, level)
    r_list = format_dict2list(r_dict)
    df = format_list2df(r_list)
    df = df.drop(["keytag"], axis=1)
    df["keyword"] = df["keyword"].apply(lambda line: str(line).replace(" ", "").lower())
    df = df.sort_values(by=list(df.columns), ascending=True)
    columns_dict = au_get_new_columns(level, sheet_name)
    df.rename(columns=columns_dict, inplace=True)
    tree_list = [tree for line, tree in columns_dict.items()]
    return df, tree_list, sheet_name


def au_get_line(path, sheet):
    df = pd.read_excel(path, sheet, error_bad_lines=False, encoding="utf_8_sig")
    line_new_list = []
    line_list = list(df.columns)
    columns_dict = {}
    the_pop1 = 'keyword'  # 后续代码中用的都是keyword，所以我这儿就不改了
    the_pop2 = [i for i in line_list if 'keyword' in i.replace(" ", "").lower()][0]  # 这儿是给的词表里keyword这列的字段名
    for line in line_list:
        new_line = "{}({})".format(sheet, line)
        columns_dict[line] = new_line
        line_new_list.append(new_line)
    new_keyword1 = "{}({})".format(sheet, the_pop1)
    new_keyword2 = "{}({})".format(sheet, the_pop2)
    columns_dict[the_pop1] = new_keyword1
    line_new_list.append(new_keyword1)
    line_new_list.remove(new_keyword2)
    df.rename(columns=columns_dict, inplace=True)
    df[new_keyword1] = df[new_keyword2].apply(lambda line: str(line).replace(" ", "").lower())
    if the_pop2 != the_pop1:
        df.drop(new_keyword2, axis=1, inplace=True)
    return df, line_new_list, sheet


def au_get_new_columns(level, sheet_name):
    columns_dict = collections.OrderedDict()
    level -= 1
    for col in range(level):
        str_col = str(col + 1)
        columns_dict['level_{}'.format(str_col)] = '{}(level{})'.format(sheet_name, str_col)
    columns_dict['keyword'] = "{}(keyword)".format(sheet_name)
    return columns_dict


@contextlib.contextmanager
def pickle_context(filepath, obj, mode='wb'):
    pass


class _MappingCollect:

    def __init__(self, path):
        """
        mapping表的集合,相当于整个标签词表数据集
        :param path:
        """

        df_sheet = pd.read_excel(path, None)
        sheets = list(df_sheet.keys())
        self.__length = len(sheets)
        self._mapping = [Mapping(path, sheet) for sheet in sheets]
        self.relation = False

    def filter_by(self, name):
        """用于查找某一个sheet对象"""
        pass


class MappingCollect(_MappingCollect):
    def filter_by(self, **kwargs):
        """用于查找某一个sheet对象"""
        name = kwargs.get("name")
        filter_mappings = list(filter(lambda mapping: mapping.sheetname == name, self._mapping))
        if len(filter_mappings) > 0:
            filter_mapping = filter_mappings[0]
        else:
            filter_mapping = None
        return filter_mapping

    def add_sen_sheet(self, sheet_list):
        sheet_list = format_max_xml_kwargs(sheet_list)
        if sheet_list:
            for sheet_name in sheet_list:
                sen_result = self.filter_by(name=sheet_name)
                if sen_result is None:
                    print("情感预设失败,标签词表不含{}sheet".format(sheet_name))
                else:
                    sen_result.sentment = True

    def add_length_sheet(self, sheet_dic):
        sheet_dic = format_max_xml_kwargs(sheet_dic)
        if sheet_dic:
            for sheet_name, tag_length in sheet_dic.items():
                sen_result = self.filter_by(name=sheet_name)
                if sen_result is None:
                    print("距离设置失败,标签词表不含{}sheet".format(sheet_name))
                else:
                    sen_result.length = tag_length

    def __getitem__(self, item):
        return self._mapping[item]

    def to_pickle(self, param):
        save_pickle = open(param, 'wb')
        pickle.dump(self, save_pickle)
        save_pickle.close()


class _Mapping:
    """
    对单个mapping表的数据结构进行封装,相当于单一sheet
    """

    def __init__(self, path, sheet):
        tree_line_tup = self.with_draw(path, sheet)
        self.mapping_list = tree_line_tup[1]
        self.mapping_df = tree_line_tup[0]
        self.sheetname = tree_line_tup[-1]
        self.sentment = True
        self.length = 0
        self.relation = None

    def with_draw(self, path, sheet):
        if "-" in sheet:
            sheet_name = sheet.split('-')[0]
            sheet_level = int(sheet.split('-')[-1])
            tree_tup = au_get_tree(path, sheet, sheet_level, sheet_name)
            return tree_tup
        else:
            line_tup = au_get_line(path, sheet)
            return line_tup

    @property
    def mapping_values(self):
        mapping_df = self.mapping_df.astype(str)
        maping_values = mapping_df[self.mapping_list].values
        return maping_values

    @property
    def choice(self):
        return 'content'


class Mapping(_Mapping):

    def __init__(self, path, sheet):
        super(Mapping, self).__init__(path, sheet)
        self.verifi = self.verification()

    def verification(self):
        datapram = {
            'code': 0,
            'msg': "词表正常",
            'sheetname': self.sheetname
        }
        before_verifi_list = self.mapping_values
        verifi_list = [verifi[-1] for verifi in before_verifi_list]
        for veri in verifi_list:
            if str(veri) in ["", "||"]:
                datapram['code'] = -1
                datapram['msg'] = "词表异常"
                # print("异常码:{},异常提示:{},词表名:{}".format(datapram['code'],datapram['msg'],datapram['sheetname']))
                return datapram
            if str(veri)[0] == "|" or str(veri[-1]) == "|":
                datapram['code'] = -2
                datapram['msg'] = "词表异常"
                # print("异常码:{},异常提示:{},词表名:{}".format(datapram['code'], datapram['msg'], datapram['sheetname']))

        return datapram


class _Relation_Mapping_collect(MappingCollect):
    def __init__(self, path):
        super(_Relation_Mapping_collect, self).__init__(path)
        self._mapping = [self.add_primary_id(relation_mapping) for relation_mapping in self._mapping]
        self.relation = True

    def add_primary_id(self, mapping):
        name = mapping.sheetname
        df = mapping.mapping_df
        df['{}-id'.format(name)] = range(df.shape[0])
        mapping.mapping_df = df
        return mapping


class Relation_Mapping_collect(_Relation_Mapping_collect):
    def get_map_name_collect(self):
        map_name_collect = [_name.sheetname for _name in self]
        return map_name_collect


def format_max_xml_kwargs(value):
    value = eval(value) if value else value
    return value


def extract_context(path, keyword):
    mapping = MappingCollect(path)
    data_list = []
    for i in mapping:
        for j in i.mapping_list:
            data = i.mapping_df[i.mapping_df[j] == keyword].values
            if len(data) > 0:
                data_list.append(list(data))
    return data_list


def viewLevel(path, keyword, level_=0):
    data_list = []
    data = extract_context(path, keyword)
    for i in data[0]:
        i = i.tolist()
        data_list.append(i)
    shangji_all_list = []
    xiaji_all_list = []
    for i in data_list:
        if level_:
            if i[level_ - 1] == keyword:
                shangji_all = i[:level_ - 1]
                xiaji_all = i[level_:]
                for j in shangji_all:
                    shangji_x = (i.index(j) + 1, j)
                    shangji_all_list.append(shangji_x)
                for j in xiaji_all:
                    xiaji_x = (i.index(j) + 1, j)
                    xiaji_all_list.append(xiaji_x)
        else:
            shangji_all = i[:i.index(x)]
            xiaji_all = i[i.index(x) + 1:]
            shangji_all_list.extend(shangji_all)
            xiaji_all_list.extend(xiaji_all)

    return list(set(shangji_all_list)), list(set(xiaji_all_list))


if __name__ == '__main__':
    file_path = 'config_tag_mapping.xlsx'  # 文件路径
    x = '美白'  # 要查看的词
    # x = '美白祛斑'
    # level = 0
    level = 4  # 级别，默认为0, 如果传0返回值没有级别
    result = viewLevel(file_path, x, level)
    print('{}    的上级是：'.format(x), result[0])
    print('{}    的下级是：'.format(x), result[1])
