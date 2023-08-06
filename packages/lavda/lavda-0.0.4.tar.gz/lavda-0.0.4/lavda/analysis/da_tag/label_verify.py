# -*- coding: utf-8 -*-
# ----------------------------------------------
# purpose : 标签词表校验
# author : LGD
# create_time : 2021/2/22 14:31
# update_time : 2021/2/22 14:31
# copyright : Lavector
# ----------------------------------------------
import re
import pandas as pd
from openpyxl import load_workbook
import xlrd

from lavda.analysis.da_tag.label_dict import PandaLabelDictTool


class VerifyLabelDict(object):
    """
        词表校验
        1.词表，有隐藏sheet，有隐藏字段
        2.词表有空格（非关键词单元格）不能有空格，
        3.连续出现的竖线、单元格开头、结尾不能有坚线、特殊的竖线 如‘｜’就是错误的，比一般的‘|’宽
        :return:
    """

    def __init__(self, path):
        self.path = path

    @property
    def check_hide_sheet(self):
        """
        检查是否有隐藏sheet
        :return:
        """
        error_msg_list = list()
        check_code = 0
        check_msg = '有隐藏表'
        xb = pd.ExcelFile(self.path)
        s = xb.book._sheets
        for i in s:
            if i.sheet_state == 1:
                check_code = '有隐藏表'
                error_msg_list.append(['有隐藏表', ""])
                return error_msg_list

        return error_msg_list

    @property
    def check_hide_line(self):
        """
        检查是否有隐藏行或隐藏列
        :return:
        """
        error_msg_list = list()
        check_code = 0
        check_msg = '有隐藏行或列'
        wb = load_workbook(self.path)
        for sheet in wb:
            # name = re.findall(r'"(.*?)"', str(sheet))[0]  # sheet name
            for colLetter, colDimension in sheet.column_dimensions.items():
                if colDimension.hidden == True:
                    check_code = '有隐藏行或列'
                    error_msg_list.append(['有隐藏行或列', ''])
                    return error_msg_list

            for colLetter, colDimension in sheet.row_dimensions.items():
                if colDimension.hidden == True:
                    check_code = '有隐藏行或列'
                    error_msg_list.append(['有隐藏行或列', ''])
                    return error_msg_list

        return error_msg_list

    @property
    def check_null(self):
        error_msg_list = list()
        check_code = 0
        check_msg = '单元格错误-空单元格'
        excel = xlrd.open_workbook(self.path)
        for n in range(excel.nsheets):
            sheet = excel.sheet_by_index(n)
            sheet_name = excel._sheet_names[n]
            if '-' in sheet_name:
                num = int(sheet_name.split('-')[-1])-1
                df = pd.read_excel(self.path, sheet_name=sheet_name,header=None, nrows=num)
                for e in sheet.merged_cells:
                    rl, rh, cl, ch = e
                    base_value = sheet.cell_value(rl, cl)
                    if rl >= num:
                        error_msg_list.append(['有不合法的合并单元格', base_value])
                    if base_value == '':
                        error_msg_list.append(['合并单元格中有空单元格', ''])
                    df.iloc[rl:rh, cl:ch] = base_value
                for k in list(df.isnull().any()):
                    if k:
                        check_code = '有空单元格'
                        error_msg_list.append(['有空单元格', ''])
                        return error_msg_list

        return error_msg_list

    @staticmethod
    def check_keyword(keyword_str):
        error_msg_list = list()
        if "||" in str(keyword_str):
            error_msg_list.append(['有||在里面', keyword_str])
        if '｜' in str(keyword_str):
            error_msg_list.append(['有特殊的竖线(｜)在里面', keyword_str])
        if str(keyword_str)[0] == "|" or str(keyword_str[-1]) == "|":
            error_msg_list.append(['以|开头或结尾', keyword_str])
        for str_i in str(keyword_str).split('|'):
            if '+' in str_i and '-' in str_i:
                if not ('(' in str_i or ')' in str_i or '（' in str_i or '）' in str_i):
                    error_msg_list.append(['加减号必须用括号隔开', keyword_str])
        if '(' in keyword_str or ')' in keyword_str or '（' in keyword_str or '）' in keyword_str:
            veri = keyword_str.replace('）', ')').replace('（', '(')
            brackets_content = re.finditer(r'\((.*?)\)', veri)
            for e_item in brackets_content:
                e = e_item.group()
                e_start = e_item.start()
                e_end = e_start + len(e)
                left_margin_char = keyword_str[e_start-1] if e_start-1 >=0 else None
                right_margin_char = keyword_str[e_end] if e_end < len(keyword_str) else None
                if left_margin_char is not None and left_margin_char not in {"-", '+', '#', '@', '|'}:
                    error_msg_list.append(['括号左侧有不合法字符:'+str(left_margin_char), keyword_str])
                if right_margin_char is not None and right_margin_char not in {"-", '+', '#', '@', '|'}:
                    error_msg_list.append(['括号右侧有不合法字符:'+str(right_margin_char), keyword_str])

                if '-' in e:
                    error_msg_list.append(['括号内不能出现减号', keyword_str])
                if '|' in e:
                    error_msg_list.append(['括号内不能出现竖线', keyword_str])
                if len(e.split('+')) != 2:
                    error_msg_list.append(['括号里没有加号或加号超过两个', keyword_str])

        return error_msg_list

    @property
    def verification(self):
        """
        检查keyword
        :return:
        """
        error_msg_list = list()
        dict_tool = PandaLabelDictTool()

        mc = dict_tool.load_all_from_file(self.path)
        for mapping in mc.mappings:
            for keyword_str in list(mapping.id2keyword.values()):
                error_msg_list.extend(VerifyLabelDict.check_keyword(keyword_str))

        return error_msg_list

    def analyze(self):
        # 错误信息 list([错误类型， 错误内容]
        total_error_msg = list()
        total_error_msg.extend(self.check_hide_sheet)
        total_error_msg.extend(self.check_null)

        if len(total_error_msg) == 0:
            total_error_msg.extend(self.check_hide_line)
            total_error_msg.extend(self.verification)
        else:
            total_error_msg.extend(self.check_hide_line)

        return total_error_msg


if __name__ == '__main__':
    keyword_str = "精美|精致-(精致-女人)-精致|惊艳"
    msg = VerifyLabelDict.check_keyword(keyword_str)
    print(msg)


