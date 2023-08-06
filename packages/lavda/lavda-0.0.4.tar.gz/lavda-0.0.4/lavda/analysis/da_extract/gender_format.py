# -*- coding: utf-8 -*-
# ----------------------------------------------
# author : 
# create_time : 2020/6/29 14:20
# update_time : 2020/6/29 14:20
# file : gender_format.py
# copyright : Lavector
# ----------------------------------------------
from lavda.backexcutor.analysis_interface import RowInterface
from lavda.util.mysql_util import *
import numpy as np
class GenderFormat(RowInterface):
    """
    提取并格式化性别数据

    """
    def __init__(self, data_dict=None,
                 default_value=None):
        """
        :param data_dict: dict, 映射数据
        :param default_value: int, 无数据或非法数据时返回此默认值
        """
        super(GenderFormat, self).__init__(default_value)

        if data_dict is None:
            self.data_dict = {'男': {'1', '1.0', '男'}, '女': {'2', '2.0', '女'}}
        else:
            self.data_dict = data_dict

        self.default_value = default_value
        self.boy_list = ['直男', '宅男', '阳光男', '眼镜男', '型男', '天蝎男', '天枰男', '天平男', '水瓶男', '双子男', '双鱼男',
                         '熟男', '狮子男', '射手男', '山羊男', '瓶子男', '暖男', '男子汉', '男子', '男纸', '男同学', '男生', '男神经', '男神',
                         '男模', '男护士', '男孩', '男闺蜜', '男高中生', '男粉', '男的', '男博主', '牧羊男', '摩羯男', '猛男', '美男', '理工男', '巨蟹男',
                         '金牛男', '肌肉男', '机车男', '工科男', '奋斗男', '草食男', '白羊男']
        self.girl_list = ['直女', '宅女', '眼镜女', '仙女', '天蝎女', '天枰女', '天平女', '水瓶女', '双子女', '双鱼女', '熟女',
                          '狮子女', '射手女', '少女', '山羊女', '瓶子女', '女子', '女纸', '女友粉', '女同学', '女生', '女神经', '女神', '女模', '女护士',
                          '女汉子', '女孩', '女高中生', '女粉', '女的', '女博主', '牧羊女', '摩羯女', '美女', '巨蟹女', '金牛女',
                          '机车女', '白羊女']
        self.boy_other_list = ['boy', '校草', '小哥哥', '帅哥', '少年']
        self.girl_other_list = ['girl', '公主', '富婆', '妈粉', '校花', '小姐姐', '小姑凉']

    def gender_judgment(self, text):
        '''
        后加的通过简介，用户标签等去判断性别
        :param text:
        :return:
        '''

        if '男' in text:
            boy_index = text.index('男')
            for boy_i in self.boy_list:
                if boy_i in text[boy_index - 2 if boy_index - 2 >= 0 else 0:boy_index + 4]:
                    return '男'
        elif '女' in text:
            girl_index = text.index('女')
            for girl_i in self.girl_list:
                if girl_i in text[girl_index - 2 if girl_index - 2 >= 0 else 0:girl_index + 4]:
                    return '女'
        else:
            for girl_i in self.girl_other_list:
                if girl_i in text:
                    return '女'
            for boy_i in self.boy_other_list:
                if boy_i in text:
                    return '男'
        return

    def process(self, data, params=None):
        column_name_list = ['gender', 'introduce', 'user_label', 'nickname']
        for column_name in column_name_list:
            if column_name not in data:
                data[column_name] = ''
        data_gender = data['gender']

        data_str = str(data_gender).strip()
        result_value = None
        for key in self.data_dict:
            if data_str in self.data_dict[key]:
                result_value = key
                break

        # TODO 2021.8.13 增加了这里的性别判断
        if result_value is None:
            gender_judgment_text = ''.join([str(data[i]) for i in ['introduce', 'user_label', 'nickname'] if data[i]])
            result_value = self.gender_judgment(gender_judgment_text)
            result_value = self.default_value if result_value is None else result_value
        return result_value


if __name__ == '__main__':
    gender_format = GenderFormat()
    print(gender_format.process({'gender':'','nickname':'宅男'}))
