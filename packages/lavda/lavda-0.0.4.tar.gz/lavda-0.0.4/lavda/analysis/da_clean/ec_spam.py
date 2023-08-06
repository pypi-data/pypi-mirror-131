# -*- coding: utf-8 -*-
# ----------------------------------------------
# purpose: 电商类垃圾检测
# author : 
# create_time : 2020/6/29 15:46
# update_time : 2020/6/29 15:46
# copyright : Lavector
# ----------------------------------------------
import numpy as np

from lavda.analysis.da_clean.clean_interface import *
from lavda.backexcutor.analysis_interface import RowInterface
from lavda.util.mysql_util import *


class EcSpam(RowInterface, CleanInterface):
    """
    电商垃圾的处理
    """
    def __init__(self, **params):
        super(EcSpam, self).__init__(CleanFlag.NO)

        # 加载数据
        sql = """
        select keyword from %s
        """ % "ec_des_word"
        result = np.array(LavwikiReader.execute_all(sql))[0]
        result = [item[0] for item in result]
        clean = [str(i).lower().strip() for i in result if len(str(i).strip()) > 0]

        self.clean_list = clean

    def process(self, data, **params):
        """
        电商垃圾的标记
        """
        data = str(data).replace(" ", "").lower()
        for i in self.clean_list:
            if i in data:
                return CleanFlag.YES
        return CleanFlag.NO


if __name__ == '__main__':
    spam = EcSpam()
    print(spam.process("救积分"))
    print(spam.process("你好呀"))