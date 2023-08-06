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

from lavda.analysis.da_tag.tag_dict import PandaLabelDictTool


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
    text, parent  = ps["text"], ps["parent"]
    result.append(text)
    if parent in r_dict:
        recursion(r_dict, result, parent)


def au_get_tree2dict(filename,sheet_name,level):
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
    columns = ["level_%s" % i for i in range(1, max_len+1)]
    columns[-2] = "keytag"
    columns[-1] = "keyword"
    df.columns = columns
    return df


def au_get_tree(infile, sheet,level,sheet_name):
    r_dict = au_get_tree2dict(infile,sheet,level)
    r_list = format_dict2list(r_dict)
    df = format_list2df(r_list)
    df = df.drop(["keytag"], axis=1)
    df["keyword"] = df["keyword"].apply(lambda line: str(line).replace(" ", "").lower())
    df = df.sort_values(by=list(df.columns), ascending=True)
    columns_dict = au_get_new_columns(level,sheet_name)
    df.rename(columns=columns_dict, inplace=True)
    tree_list = [tree for line,tree in columns_dict.items() ]
    return df,tree_list,sheet_name



def au_get_line(path,sheet):
    df = pd.read_excel(path, sheet, error_bad_lines=False, encoding="utf_8_sig")
    line_new_list = []
    line_list = list(df.columns)
    columns_dict = {}
    the_pop1 = 'keyword'    # 后续代码中用的都是keyword，所以我这儿就不改了
    the_pop2 = [i for i in line_list if 'keyword' in i.replace(" ", "").lower()][0]     # 这儿是给的词表里keyword这列的字段名
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




def au_get_new_columns(level,sheet_name):
    columns_dict = collections.OrderedDict()
    level -= 1
    for col in range(level):
        str_col = str(col+1)
        columns_dict['level_{}'.format(str_col)] = '{}(level{})'.format(sheet_name,str_col)
    columns_dict['keyword'] = "{}(keyword)".format(sheet_name)
    return columns_dict