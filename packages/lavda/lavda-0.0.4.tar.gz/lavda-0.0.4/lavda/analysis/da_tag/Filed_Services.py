#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Author : dada
# @time   : 2020/7/31 11:05
import functools
import pandas as pd
from openpyxl import load_workbook
import xlrd
import re
from lavda.analysis.da_tag.mapping_models import MappingCollect


def filed_services(func):
    @functools.wraps(func)
    def filed(*args,**kwargs):
        data = kwargs.get("df")
        add_head_text = kwargs.get("add_head_text")
        old_columns = list(data.columns)
        data = func(*args,**kwargs)
        new_columns_list = list(data.columns)
        filter_column_list = list(filter(lambda column: column not in old_columns, new_columns_list))
        new_cloumns_dict = {old_name: "{}{}".format(add_head_text, old_name) for old_name in filter_column_list}
        data.rename(columns=new_cloumns_dict, inplace=True)
        return data
    return filed



class VerMappingCollect():
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
        check_code = 0
        check_msg = '有隐藏表'
        xb = pd.ExcelFile(self.path)
        s = xb.book.sheets()
        for i in s:
            if i.visibility == 1:
                check_code = '有隐藏表'

        return {check_msg: check_code}


    @property
    def check_hide_line(self):
        check_code = 0
        check_msg = '有隐藏行或列'
        wb = load_workbook(self.path)
        for sheet in wb:
            # name = re.findall(r'"(.*?)"', str(sheet))[0]  # sheet name
            for colLetter, colDimension in sheet.column_dimensions.items():
                if colDimension.hidden == True:
                    check_code = '有隐藏行或列'

            for colLetter, colDimension in sheet.row_dimensions.items():
                if colDimension.hidden == True:
                    check_code = '有隐藏行或列'

        return {check_msg: check_code}

    @property
    def check_null(self):
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
                    df.iloc[rl:rh, cl:ch] = base_value
                for k in list(df.isnull().any()):
                    if k:
                        check_code = '有空单元格'

        return {check_msg: check_code}

    @property
    def verification(self):

        check_msg = []
        self.ver_map = MappingCollect(self.path)
        for i in self.ver_map:
            j = i.mapping_values
            for veri in [verifi[-1] for verifi in j]:
                if "||" in str(veri):
                    check_msg.append({'有||在里面': veri})
                if '｜' in str(veri):
                    check_msg.append({'有特殊的竖线(｜)在里面': veri})
                if str(veri)[0] == "|" or str(veri[-1]) == "|":
                    check_msg.append({'以|开头或结尾': veri})
                if '(' in veri or ')' in veri or '（' in veri or '）' in veri:
                    veri = veri.replace('）', ')').replace('（', '(')
                    brackets_content = re.findall(r'\((.*?)\)', veri)
                    for e in brackets_content:
                        if '-' in e:
                            check_msg.append({'括号内不能出现减号': veri})
                        if len(e.split('+')) != 2:
                            check_msg.append({'括号里没有加号或加号超过两个': veri})

        error_a = '单元格错误-标签词错误'
        error_a_list = []
        for j in check_msg:
            error_a_list.append(list(j.values())[0])
        check_msg = ','.join(list(set(error_a_list)))
        return {error_a: check_msg}

    @property
    def ver_status(self):
        status = 0
        dic = {}
        if list(self.check_hide_sheet.values())[0] == 0 and list(self.check_null.values())[0] == 0:
            for i in [self.check_hide_sheet, self.check_hide_line, self.check_null, self.verification]:
                if type(i) == dict:
                    dic[list(i.keys())[0]] = list(i.values())[0]
        else:
            for i in [self.check_hide_sheet, self.check_hide_line, self.check_null]:
                if type(i) == dict:
                    dic[list(i.keys())[0]] = list(i.values())[0]
        for key, values in dic.items():
            # if values != 0 and values != '':
            if values not in [0, '']:
                status = 1
                return {status: dic}
        return {status: dic}
