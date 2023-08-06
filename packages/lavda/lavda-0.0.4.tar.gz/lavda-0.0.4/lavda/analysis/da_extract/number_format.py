# -*- coding: utf-8 -*-
# ----------------------------------------------
# author : 
# create_time : 2020/6/29 14:24
# update_time : 2020/6/29 14:24
# copyright : Lavector
# ----------------------------------------------
from lavda.backexcutor.analysis_interface import RowInterface


class IntFormat(RowInterface):
    """"
    整数格式化
    """

    def __init__(self, default_value=""):
        """
        :param default_value: 默认值
        """
        super(IntFormat, self).__init__(default_value)
        self.default_value = default_value

    def process(self, data, **params):
        if data is None:
            return self.default_value
        if isinstance(data, int):
            return data

        data = str(data).strip()
        if not data:
            return self.default_value

        if '千' in data:
            data = data.replace('千', '')
            data = int(float(data) * 1000)
            return data
        elif '万' in data:
            data = data.replace('万', '')
            data = int(float(data) * 10000)
            return data
        elif '亿' in data:
            data = data.replace('亿', '')
            data = int(float(data) * 100000000)
            return data

        # 判断下是不是数字,是数字就保留
        if u'\u0030' <= data <= u'\u0039':
            return int(float(data))
        else:
            return self.default_value


class FloatFormat(RowInterface):
    """
    浮点数格式化
    """
    def __init__(self, n_digits=2, default_value=""):
        """

        :param n_digits: int, 小数点后保留位数
        :param default_value: 默认值
        """
        super(FloatFormat, self).__init__(default_value)

        self.n_digits = n_digits
        self.default_value = default_value

    def process(self, data, **params):
        """
        1：将各个字段的数据进行单位格式化，例如将'万'，'亿'等单位替换成纯数字。
        2：将不是数字的替换成空。
        3: 将price字段处理成保留两位的浮点数。
        :param data: 单个字段的值
        :return: 处理后单个字段的值
        """
        if data is None:
            return self.default_value
        data = str(data).strip()
        if not data:
            return self.default_value

        if '千' in data:
            data = data.replace('千', '')
            data = float(data) * 1000
            return data
        elif '万' in data:
            data = data.replace('万', '')
            data = float(data) * 10000
            return data
        elif '亿' in data:
            data = data.replace('亿', '')
            data = float(data) * 100000000
            return data

        # 判断下是不是数字,是数字就保留
        if u'\u0030' <= data <= u'\u0039':
            return round(float(data), self.n_digits)
        else:
            return self.default_value


if __name__ == '__main__':
    int_format = IntFormat()
    print(int_format.process("23.23"))

    float_format = FloatFormat()
    print(float_format.process("23.2390"))
