#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from lavda.analysis.da_clean.clean_interface import *
from lavda.backexcutor.analysis_interface import RowInterface
from lavda.util.panda_tool import PandaTool


class CleanUnincludedKeyword(RowInterface, CleanFlag):
    
    def __init__(self):
        super(CleanUnincludedKeyword, self).__init__(CleanFlag.NO)

        self.keyword_list = None

    def load_config_data(self, **config):

        keyword_path = config['KeywordExcelPath']
        # 读取配置文件中抓取关键词
        keyword_df = PandaTool.read(keyword_path)
        keyword_list = keyword_df.iloc[:, 0].values.tolist()
        self.keyword_list = keyword_list

    def process(self, data, **params):

        for keyword_i in self.keyword_list:
            if str(keyword_i).strip().lower() in str(data).lower():
                return CleanFlag.NO
        return CleanFlag.YES
