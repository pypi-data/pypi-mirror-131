# -*- coding: utf-8 -*-
# ----------------------------------------------
# purpose: 其他类垃圾检测
# author : 
# create_time : 2020/6/29 15:49
# update_time : 2020/6/29 15:49
# copyright : Lavector
# ----------------------------------------------
import re

from lavda.analysis.da_clean.clean_interface import *


class NoChineseEnglish(RowInterface, CleanInterface):
    """
    非中英文过滤
    """
    def __init__(self, **params):
        super(NoChineseEnglish, self).__init__(CleanFlag.NO)

    def process(self, data, **params):
        zhPattern = re.compile(u'[\u4e00-\u9fa5]+')
        match1 = zhPattern.search(str(data))
        match2 = re.findall('[a-zA-Z]+', str(data))
        if match1 or len(match2) > 0:
            return CleanFlag.NO
        return CleanFlag.YES


class TextLen(RowInterface, CleanInterface):
    def __init__(self, **params):
        super(TextLen, self).__init__(CleanFlag.NO)

    def process(self, data, **params):
        if len(str(data).strip()) < 2:
            return CleanFlag.YES
        # TODO 原来只是超短文本过滤，20210816将微博超话过滤加入进去
        # 微博超话过滤规则：content 以超话宝石符号开头，整体小于15
        #  宝石符号
        if '' == data.strip()[0] and len(str(data).strip()) <= 15:
            return CleanFlag.YES
        return CleanFlag.NO


if __name__ == '__main__':
    no_ce = NoChineseEnglish()
    print(no_ce.process("234###"))

    text_len = TextLen()
    print(text_len.process("khhh"))