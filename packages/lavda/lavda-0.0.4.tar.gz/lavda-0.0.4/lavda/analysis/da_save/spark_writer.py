# -*- coding:utf-8 -*-
import findspark

import os
from pyspark import SparkContext
from pyspark import SparkConf
from pyspark.sql import HiveContext, SparkSession
import pandas as pd
# from middleware.utils import get_dir_files

input_path = "/home/wac/hanaojian/maxda-dev/data"
project_id = 'kh_2020-02-30'

global path_root, path_project
path_root = os.getcwd()
path_project = os.path.join(path_root, "data/run_project")
input_data_path = os.path.join(path_project, "1_log")


def get_dir_files(dir, filelist=[], status=0, str1=""):
    """
    dir: 目录地址
    filelist: 变量地址
    status: 表示是包含 1，取消 0，还是不包含 -1
    str1: 过滤词
    """
    newDir = dir
    if os.path.isfile(dir):
        filelist.append(dir)
    elif os.path.isdir(dir):
        for s in os.listdir(dir):
            # 如果需要忽略某些文件夹，使用以下代码
            if status == 1:
                # 如果不包含改字符串就跳过
                if str1 not in s:
                    continue
            elif status == -1:
                # 如果包含改字符串就跳过
                if str1 in s:
                    continue
            newDir = os.path.join(dir, s)
            get_dir_files(newDir, filelist, status, str1)
    # 默认顺序排列
    return sorted(filelist, reverse=False)


def mergefile(input_path_1, project_id):
    files_path = get_dir_files(input_path_1, [], status=-1, str1=".DS_Store")
    print(files_path)
    df_list = []
    for infile in files_path:
        df = pd.read_excel(infile, header=0, error_bad_lines=False, encoding="utf_8_sig",dtype='str').fillna("")
        df_list.append(df)
    data_pd = pd.concat(df_list)
    data_pd['project_id'] = project_id

    return data_pd


def main():
    findspark.init()
    conf = SparkConf().setAppName('savepyspark').setMaster('local[*]')
    sc = SparkContext(conf = conf)
    sqlContext = HiveContext(sc)

    data_pd = mergefile(input_path,project_id)
    df_1 = sqlContext.createDataFrame(data_pd)

    df_1.write.saveAsTable('test.write_test10', mode='append', partitionBy=['project_id'])

    sc.stop()


if __name__ == '__main__':
    main()