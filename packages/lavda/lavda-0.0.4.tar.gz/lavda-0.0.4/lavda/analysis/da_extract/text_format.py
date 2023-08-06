# -*- coding: utf-8 -*-
# ----------------------------------------------
# author : 
# create_time : 2020/6/29 15:27
# update_time : 2020/6/29 15:27
# copyright : Lavector
# ----------------------------------------------
from lavda.util.lang.langconv import Converter
from lavda.backexcutor.analysis_interface import *


class LangTool(object):
    @staticmethod
    def simple2tradition(text):
        # 将简体转换成繁体
        result = Converter('zh-hant').convert(text)
        return result

    @staticmethod
    def tradition2simple(text):
        # 将繁体转换成简体
        result = Converter('zh-hans').convert(text)
        return result


class Simple2Tradition(RowInterface):
    """
    简体转繁体
    """
    def __init__(self):
        super(Simple2Tradition, self).__init__(None)

    def process(self, data, **params):
        if data is None:
            return None

        if isinstance(data, dict):
            result = dict()
            for key in data:
                result[key] = Converter('zh-hant').convert(str(data[key]))
        else:
            result = Converter('zh-hant').convert(str(data))

        return result


class Tradition2Simple(RowInterface):
    """
    繁体转简体
    """
    def __init__(self):
        super(Tradition2Simple, self).__init__(None)

    def process(self, data, **params):
        if data is None:
            return None

        if isinstance(data, dict):
            result = dict()
            for key in data:
                result[key] = Converter('zh-hans').convert(str(data[key]))
        else:
            result = Converter('zh-hans').convert(str(data))

        return result


if __name__ == '__main__':
    text = "中国好"
    s = Simple2Tradition()
    result1 = s.process(text)
    print(result1)

    t = Tradition2Simple()
    result2 = t.process(result1)
    print(result2)