# -*- coding: utf-8 -*-
from lavda.analysis.da_clean.clean_interface import *


class AllTextSpam(RowInterface, CleanInterface):
    """
    电商垃圾的处理
    """
    def __init__(self, **params):
        super(AllTextSpam, self).__init__(CleanFlag.NO)

    def process(self, data, **params):
        if str(data) in ["转发微博", "轉發微博", "转发", "666", "好评"]:
            return CleanFlag.YES
        else:
            return CleanFlag.NO


if __name__ == '__main__':
    spam = AllTextSpam()
    print(spam.process("转发微博"))
