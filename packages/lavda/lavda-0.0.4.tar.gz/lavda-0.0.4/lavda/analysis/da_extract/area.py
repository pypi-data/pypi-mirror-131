# -*- coding: utf-8 -*-
# ----------------------------------------------
# purpose: 地理信息相关功能
# author : 
# create_time : 2020/6/29 15:06
# update_time : 2020/6/29 15:06
# copyright : Lavector
# ----------------------------------------------
"""
地理信息处理
"""
import numpy as np
from lavda.util.mysql_util import *


class AreaDictInterface(object):
    def get(self):
        pass

    def get_by_area_code(self, area_code):
        pass

    def find(self, text, level=None):
        pass

    def print_all(self):
        pass


class MainAreaDict(AreaDictInterface):
    """
    中国主要城市信息数据
    """

    def __init__(self, area_list):
        self.area_list = area_list

        self.area_dict = dict()
        self.name_code_dict = dict()
        for item in self.area_list:
            area_code = item['areaCode']
            self.area_dict[area_code] = item

            name = item['name']
            short_name = item['shortName']
            if name not in self.name_code_dict:
                self.name_code_dict[name] = set()
            if short_name not in self.name_code_dict:
                self.name_code_dict[short_name] = set()

            self.name_code_dict[name].add(area_code)
            self.name_code_dict[short_name].add(area_code)

    def get(self):
        return self.area_list

    def get_by_area_code(self, area_code):
        if area_code not in self.area_dict:
            return None
        return self.area_dict[area_code]

    def find(self, text, level=None):
        if isinstance(level, int):
            current_level_set = {level}
        elif isinstance(level, (tuple, list)):
            current_level_set = set(level)
        elif isinstance(level, set):
            current_level_set = level
        else:
            current_level_set = None

        result = list()

        if text in self.name_code_dict:
            area_code_set = self.name_code_dict[text]

            for area_code in area_code_set:
                current_area_item = self.area_dict[area_code]
                if current_level_set:
                    if current_area_item['level'] in current_level_set:
                        result.append(current_area_item)
                else:
                    result.append(current_area_item)

        return result

    def print_all(self):
        print("data count = ", len(self.area_list))


class CityRankDict(AreaDictInterface):
    """
    中国主要级别城市排行
    """

    def __init__(self, area_list):
        self.area_list = area_list

        self.area_dict = dict()
        for item in self.area_list:
            self.area_dict[item['areaCode']] = item

    def get(self):
        return self.area_list

    def get_by_area_code(self, area_code):
        if area_code not in self.area_dict:
            return None
        return self.area_dict[area_code]

    def find(self, text, level=None):
        """
        在指定的level内进行匹配查找
        :param text:
        :return: list(dict)
        """
        if isinstance(level, int):
            current_level_set = {level}
        elif isinstance(level, (tuple, list)):
            current_level_set = set(level)
        elif isinstance(level, set):
            current_level_set = level
        else:
            current_level_set = None

        result = list()
        for item in self.area_list:
            if item['name'] == text or item['shortName'] == text:
                if current_level_set and item['level'] not in current_level_set:
                    continue
                result.append(item)

        return result

    def print_all(self):
        print("data count = ", len(self.area_list))


class CityExtractProcessor(object):
    """
    从文本中提取城市信息
    """
    SPE_CITY = {'北京', '天津', '重庆', '上海', '北京市', '上海市', '重庆市', '天津市'}

    def __init__(self, main_area_object, city_list):
        self.main_area_object = main_area_object
        self.city_list = city_list


    def process(self, data, **params):
        """
        从文本中提取城市信息，提取最低级别城市信息
        支持的格式：
        重庆 铜梁县
        北京
        北京 东城区
        湖北 荆州
        湖北 仙桃
        广东
        沈阳 法库
        :param data:
        :param params:
        :return: list(dict)，返回完整的城市信息
        """
        # TODO 2021.8.13 增加了这里的城市判断
        if type(data) == dict:
            city_column_name_list = ['city', 'introduce']
            for column_name in city_column_name_list:
                if column_name not in data:
                    data[column_name] = ''
            data_city = data['city']
            data_city = str(data_city).strip()
            if not data_city:
                city_judgment_text = ''.join([str(data[i]) for i in city_column_name_list if data[i]])
                data_city = self.city_judgment(city_judgment_text)
                if not data_city:
                    return list()
            text = str(data_city).strip()
        else:
            if data is None:
                return list()
            text = str(data).strip()
            if not text:
                return list()

        # TODO
        tmp_list = text.split(" ")
        tmp_list = [value.strip() for value in tmp_list if value.strip()]

        # 1.直接在city rank词典里面查找
        parent_city_str = None
        if len(tmp_list) == 2:
            if tmp_list[0] in self.SPE_CITY:
                parent_city_str = tmp_list[0]
                cur_city_str = tmp_list[1]
            elif tmp_list[1] in self.SPE_CITY:
                parent_city_str = None
                cur_city_str = tmp_list[1]
            else:
                parent_city_str = tmp_list[0]
                cur_city_str = tmp_list[1]
        elif len(tmp_list) == 1:
            cur_city_str = tmp_list[0]
        else:
            # TODO 未知的格式
            return list()

        # TODO 有些行政区域会有调整，如县改为区，因此可能就无法匹配到
        # TODO 生成多个可能的候选城市,把可能性高的放在前面
        can_cur_city_set = {cur_city_str}
        if cur_city_str.endswith("县"):
            can_cur_city_set.add(cur_city_str.replace("县", "区"))

        # 先查找子类
        tmp_target_result = dict()
        for cur_str in can_cur_city_set:
            one_target_result = self.main_area_object.find(cur_str)
            for one_item in one_target_result:
                tmp_target_result[one_item['areaCode']] = one_item

        # 再查找父类
        # 先查找父类，重复性很低的
        if parent_city_str:
            target_parent_result = self.main_area_object.find(parent_city_str, {1, 2})
            if target_parent_result and len(target_parent_result) >= 1:
                # 只使用第一个
                target_parent_result = target_parent_result[0]

                # 筛选子级
                sub_target_result = dict()
                for tmp_area_code in tmp_target_result:
                    tmp_item = tmp_target_result[tmp_area_code]
                    if tmp_item['parent'] == target_parent_result['areaCode']:
                        sub_target_result[tmp_area_code] = tmp_item

                tmp_target_result = sub_target_result

        target_result = list(tmp_target_result.values())

        return target_result

    def city_judgment(self, text):
        '''
        后来增加的城市判断，判断简介里面  坐标后面有没有城市
        :param text: 简介，用户标签
        :return:
        '''
        if '坐标' in text:
            # 坐标  的index，取坐标和坐标后面10个字
            zb_index = text.index('坐标')
            need_text = text[zb_index:zb_index+10]
            for city_i in self.city_list:
                if city_i in need_text:
                    return city_i
        return
