# *-* coding:utf-8 *-*
'''
@author: han
@date:   2020-08-24
'''
import os
import sys
import pandas as pd
from lavda.util.panda_tool import PandaTool
from lavda.util.file_tool import FileTool


global path_root, path_project
path_root = os.getcwd()
path_project = os.path.join(path_root, "data/run_project")
input_data_path = os.path.join(path_project, "1_log")
output_data_path = os.path.join(path_project, "2_merge/result_口红_品牌.xlsx")


def get_file_list(dir, filelist):
    newDir = dir
    if os.path.isfile(dir):
        filelist.append(dir)
    elif os.path.isdir(dir):
        for s in os.listdir(dir):
            # 如果需要忽略某些文件夹，使用以下代码
            if s == ".DS_Store":
                continue
            newDir = os.path.join(dir, s)
            get_file_list(newDir, filelist)
    # 默认顺序排列
    return sorted(filelist, reverse=False)

def save(all_df_result_dict, result_file_path):
    writer = pd.ExcelWriter(result_file_path)
    for label_name in all_df_result_dict:
        df_one_label = all_df_result_dict[label_name]
        df_one_label.to_excel(writer, sheet_name=label_name, index=True)
    writer.save()

# def main():

#     # file_path_friend = FileTool
#     # file_path_all = file_path_friend.get_file_path("C:/Users/zhang/Desktop/口红项目/3、打标结果")
#     file_path_all = get_file_list(input_data_path,filelist=[])
#     dict_df = {}
#     sheetname = 0
#     for file_path in file_path_all:
#         df_statis = PandaTool.read(file_path)
#         dict_df[str(sheetname)] = df_statis
#         sheetname += 1
#     save(dict_df,output_data_path)

class MoreSheetSave():
    def __init__(self):
        pass

    def sheet_save(self,input_data_path,output_data_path):
        file_path_all = get_file_list(input_data_path,filelist=[])
        dict_df = {}
        sheetname = 0
        for file_path in file_path_all:
            df_statis = PandaTool.read(file_path)
            dict_df[str(sheetname)] = df_statis
            sheetname += 1
        save(dict_df,output_data_path)

def main():
    test_friend = MoreSheetSave()
    test_friend.sheet_save(input_data_path,output_data_path)

if __name__ == '__main__':
    main()
