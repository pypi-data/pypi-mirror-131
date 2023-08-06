# -*- coding: utf-8 -*-
# ----------------------------------------------
# purpose : 核心配置功能
# author : 
# create_time : 2020/7/2 13:37
# update_time : 2020/7/2 13:37
# copyright : Lavector
# ----------------------------------------------
import os

# 数据分析数据库
CONF_DB_LAVWIKI = {'host': "111.207.114.228",
                   'port': 13306,
                   'user': "data_analysis",
                   'password': "data_analysis_root_0715",
                   'database': "lavwiki",
                   'charset': "utf8",
                  }

#分句符号配置

split_sign = '[.。!！\n]'

# AI 数据库
LAV_AI_DB_CONFIG = {"host": "192.168.50.129",
                    "port": 3306,
                    "user": "lavdata2019",
                    "password": "lav_data_20190905",
                    "database": "lav_ai",
                    }

# NLP 模型配置
def get_nlp_model_path():
    """
    获取nlp 模型根目录
    :return:
    """
    can_model_paths = ['/data/share/nlp', 'C:\\jh\\share\\nlp', 'E:\\data\\share\\nlp']

    for model_path in can_model_paths:
        if os.path.exists(model_path):
            return model_path

    raise Exception("can not find nlp model path")
