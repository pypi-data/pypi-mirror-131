# -*- coding: utf-8 -*-
# ----------------------------------------------
# author : 
# create_time : 2020/6/29 14:10
# update_time : 2020/6/29 14:10
# file : time_format.py
# copyright : Lavector
# ----------------------------------------------
"""
提取时间并格式化
"""
import datetime
import collections

from lavda.backexcutor.analysis_interface import RowInterface


class DateTimeFormat(RowInterface):
    """
    从文本中提取时间数据并格式化
    """

    def __init__(self, format_str="%Y-%m-%d", default_value=None):
        """

        :param format_str: str, 时间格式
        :param default_value: 任何值, 默认值
        """
        super(DateTimeFormat, self).__init__(default_value)

        self.default_value = default_value
        self.format_str = format_str
        # TODO '十'要特殊处理，其他处就要全部删掉
        data_map_list = [('十月', '10月'), ('二十日', "20日"), ('三十日', '30日'), ('十日', '10日'), ('十', ''),
                         ('〇', '0'), ('○', '0'), ('一', '1'), ('二', '2'), ('三', '3'), ('四', '4'),
                         ('五', '5'), ('六', '6'), ('七', '7'), ('八', '8'), ('九', '9'),
                         ('+', ''), ('/', '-'), ('.', '-'), ('年', '-'), ('月', '-'), ('日', '')
                         ]
        self.data_map = collections.OrderedDict(data_map_list)

        self.effective_char = set([' ', ':', '-'] + list('0123456789'))

    def is_all_effective_char(self, datetime_string):
        for ch in list(datetime_string):
            if ch in self.effective_char:
                continue
            return False
        return True

    def parse(self, data, **params):
        """

        :param data: string
        :param params:
        :return: datetime:
        """
        if data is None:
            return self.default_value
        datetime_string = str(data).strip()
        if not datetime_string:
            return self.default_value

        # TODO 包括毫秒的情况，要去掉，不处理秒以下的数据
        if "." in datetime_string:
            t_index = datetime_string.index(".")
            datetime_string = datetime_string[:t_index]

        empty_char_count = datetime_string.count(" ")
        if empty_char_count > 1:
            datetime_string = data.replace(" ", "", empty_char_count - 1)

        # 无效字符替换
        for key in self.data_map:
            if key in datetime_string:
                datetime_string = datetime_string.replace(key, self.data_map[key])

        # TODO 再一次进行校验
        if len(datetime_string) > 20:
            return self.default_value
        if not self.is_all_effective_char(datetime_string):
            return self.default_value

        # TODO 没有日期数据时，会给一个默认的日期 1900-01-01
        # TODO 没有时间数据时，会给一个默认的时间 00:00:00
        result_date = self.default_value
        if len(datetime_string) <= 10:
            if datetime_string.count("-") == 2:
                # 只包含日期
                result_date = datetime.datetime.strptime(datetime_string, u"%Y-%m-%d")
            elif 6 <= len(datetime_string) <= 8:
                result_date = datetime.datetime.strptime(datetime_string, u"%Y%m%d")
        elif len(datetime_string) > 10 and ":" in datetime_string:
            datetime_string = datetime_string.replace(" ", "")
            # 包含 日期 + 时间
            if ("-" in datetime_string):
                if datetime_string.count(":") == 1:
                    # 时间包含年，月
                    result_date = datetime.datetime.strptime(datetime_string, u"%Y-%m-%d%H:%M")
                elif datetime_string.count(":") == 2:
                    # 时间包含年，月，日
                    result_date = datetime.datetime.strptime(datetime_string, u"%Y-%m-%d%H:%M:%S")
            else:
                if datetime_string.count(":") == 1:
                    # 时间包含年，月
                    result_date = datetime.datetime.strptime(datetime_string, u"%Y%m%d%H:%M")
                elif datetime_string.count(":") == 2:
                    # 时间包含年，月，日
                    result_date = datetime.datetime.strptime(datetime_string, u"%Y%m%d%H:%M:%S")

        return result_date

    def process(self, data, **params):
        if not data:
            return self.default_value
        result_date = self.parse(data, **params)
        if not result_date:
            return self.default_value
        result = result_date.strftime(self.format_str)

        return result


if __name__ == '__main__':
    datetime_format = DateTimeFormat()

    # 1.测试提取时间
    # datetime_string = "2019年4月5日 18:21"
    datetime_string = "2019年06月02日22:50"
    # datetime_string = "2019/06/02 22:50:00.000"
    # datetime_string = "二○一七年六月二十日"
    datetime_string = "2019-10-11 22:13:00"
    result1 = datetime_format.process(datetime_string)
    print(result1)

