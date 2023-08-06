# -*- coding: utf-8 -*-
# ----------------------------------------------
# author : lgd
# create_time : 2020/6/29 14:04
# update_time : 2020/6/29 14:04
# file : age_format.py
# copyright : Lavector
# ----------------------------------------------
"""
年龄相关处理
"""
import datetime

from lavda.backexcutor.analysis_interface import RowInterface
from lavda.analysis.da_extract.datetime_format import DateTimeFormat


class AgeLevelFormat(RowInterface):
    def __init__(self, default_value=None):
        """
        :param default_value: int, 无数据或非法数据时返回此默认值
        """
        super(AgeLevelFormat, self).__init__(default_value)
        self.default_value = default_value
        self.age_level_list = {'41-50': 7,
                               '31-40': 5,
                               '31-35': 5,
                               '21-30': 3,
                               '21-25': 3,
                               '11-20': 2,
                               }

    def process(self, data, params=None):
        if data is None:
            return self.default_value
        age = str(data).strip()
        if not age:
            return self.default_value
        # 0615新加的规则 ,从简介里面捞取年龄
        if '-' in age:
            return self.age_level_list[age]
        age = int(float(age))
        if age <= 0:
            return self.default_value

        age = int(age)
        if 0 < age < 10:
            return self.default_value
        if 10 <= age <= 15:
            return self.default_value
        if 16 <= age <= 20:
            return 2
        if 21 <= age <= 25:
            return 3
        if 26 <= age <= 30:
            return 4
        if 31 <= age <= 35:
            return 5
        if 36 <= age <= 40:
            return 6
        if 41 <= age <= 45:
            return 7
        if 46 <= age <= 50:
            return 8
        if 51 <= age <= 55:
            return 9
        if 56 <= age <= 60:
            return 10

        return self.default_value


class CalAgeFromBirth(RowInterface):
    def __init__(self, default_value=None):
        """
        从生日时间中提出年龄信息
        :param default_value: 无年龄数据或数据无效时使用此值
        """
        super(CalAgeFromBirth, self).__init__(default_value)
        self.default_value = default_value

    def process(self, data, **params):

        """
        根据时间文本字符串计算年龄
        :param data: datetime or string(时间格式字符串，"%Y-%m-%d %H:%M:%S")
        :param params:
        :return: int, 年龄
        """
        if data is None:
            return self.default_value
        # 数据格式检验
        if isinstance(data, str):
            if data.count("-") != 2 or data.count(":") != 2 or len(data) < 18:
                return self.default_value
            data = datetime.datetime.strptime(data, "%Y-%m-%d %H:%M:%S")

        birth_year = data.year

        if birth_year is None:
            return None

        # 计算年龄
        now_year = datetime.datetime.now().year
        age = now_year - birth_year + 1

        return age


class AgeFormat(RowInterface):
    """
    提取并格式化年龄数据，将不合法的数据使用默认值进行表示
    支持的数据包括两种：1. 数字类 2.年龄格式的字符串
    """

    def __init__(self, default_value=None, min_age=16, max_age=60):
        """
        格式化时间数据
        :param default_value: 无年龄数据或数据无效时使用此值
        :param min_age: int or None, 有效数据最小值, 包含等于 <=
        :param max_age: int or None, 有效数据最大值，包含等于  >=
        """
        super(AgeFormat, self).__init__(default_value)

        self.default_value = default_value
        self.min_age = min_age
        self.max_age = max_age

        self.time_extract_processor = DateTimeFormat()
        self.cal_age_processor = CalAgeFromBirth()

    def process(self, data, **params):
        """

        :param data: int or string，输入数据，整数或日期格式数据(作为初生日期)
        :param params:
        :return:
        """
        if 'age' not in data:
            return self.default_value
        data_age = data['age']
        if data_age == '':
            return self.supplementary_age(data)

        if isinstance(data_age, int):
            age = data_age
        else:
            age_str = str(data_age).strip()
            if age_str.replace('.', '', 1).isdigit():
                age = int(float(age_str))
            else:
                # 按年龄处理
                try:
                    datetime_string = self.time_extract_processor.parse(age_str)
                    age = self.cal_age_processor.process(datetime_string)
                except Exception as e:
                    age = self.default_value

        if age is None:
            return self.default_value

        # 年龄数据校验
        if self.min_age is not None and age < self.min_age:
            return self.default_value
        if self.max_age is not None and age > self.max_age:
            return self.default_value

        return age

    def supplementary_age(self, data, **params):
        '''
        0615新加的规则 ,从简介里面捞取年龄
        如果年龄为空，通过简介，用户标签判断年龄信息
        :param data: 字典类型一行数据
        :param params:
        :return:
        '''
        age_list = {'70后': '41-50',
                    '80后': '31-40',
                    '85后': '31-35',
                    '90后': '21-30',
                    '95后': '21-25',
                    '00后': '11-20',
                    '70後': '41-50',
                    '80後': '31-40',
                    '85後': '31-35',
                    '90後': '21-30',
                    '95後': '21-25',
                    '00後': '11-20',
                    }
        judge_column_name_list = ['introduce', 'user_label', 'nickname']
        for column_name in judge_column_name_list:
            if column_name not in data:
                data[column_name] = ''
        judge_text = '.'.join([str(data[i]) for i in judge_column_name_list if data[i]]).lower()
        for _age in age_list.keys():
            if _age in judge_text:
                return age_list[_age]
        return self.default_value


if __name__ == '__main__':
    age_level = AgeLevelFormat()
    print(age_level.process(19))

    age_format = AgeFormat()
    print(age_format.process("60"))
