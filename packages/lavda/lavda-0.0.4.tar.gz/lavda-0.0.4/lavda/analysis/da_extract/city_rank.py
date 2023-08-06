# -*- coding: utf-8 -*-
# ----------------------------------------------
# purpose: 城市等级数据提取
# author : 
# create_time : 2020/6/29 15:01
# update_time : 2020/6/29 15:01
# copyright : Lavector
# ----------------------------------------------
import pandas as pd

from lavda.util.panda_tool import PandaTool
from lavda.util.mysql_util import LavwikiReader
from lavda.backexcutor.analysis_interface import RowInterface
from lavda.analysis.da_extract.area import *


class AreaDictTool(object):
    def _load_main_area_from_db(self, mysql_table_name, integer_column):
        """
        从数据库加载词典信息
        :return:
        """
        df_input = LavwikiReader.get_as_df(mysql_table_name)

        column_list = PandaTool.get_column(df_input)
        column_list = [column for column in column_list if "unname" not in column]

        area_list = list()
        for index, row in df_input.iterrows():
            area_item = dict()
            for column in column_list:
                if column in integer_column:
                    area_item[column] = int(row[column])
                else:
                    area_item[column] = str(row[column])

            area_list.append(area_item)

        return area_list

    def _load_from_excel(self, input_file_path, integer_column):
        df_input = PandaTool.read(input_file_path)

        column_list = PandaTool.get_column(df_input)
        column_list = [column for column in column_list if "unname" not in column]

        area_list = list()
        for index, row in df_input.iterrows():
            area_item = dict()
            for column in column_list:
                if column in integer_column:
                    area_item[column] = int(row[column])
                else:
                    area_item[column] = str(row[column])

            area_list.append(area_item)

        return area_list

    def _save_to_excel(self, area_list, integer_column, result_file_path):
        columns = list(area_list[0].keys())

        result_list = list()
        for item in area_list:
            item_list = [item[column] for column in columns]
            result_list.append(item_list)

        df_result = pd.DataFrame(result_list, columns=columns)
        for column in integer_column:
            df_result[column] = df_result[column].astype("int")

        PandaTool.save(result_file_path, df_result)

    def load_main_area_from_excel(self, input_file_path):
        """
        适用于各种词典
        :param input_file_path:
        :return:
        """
        integer_column = {'id', "level"}

        area_list = self._load_from_excel(input_file_path, integer_column)
        # area_list = self._load_main_area_from_db(mysql_table_name, integer_column)
        dict_object = MainAreaDict(area_list)

        return dict_object

    def load_main_area_from_db(self, mysql_table_name):
        """
        适用于各种词典
        :param input_file_path:
        :return:
        """
        integer_column = {'id', "level"}

        area_list = self._load_main_area_from_db(mysql_table_name, integer_column)
        dict_object = MainAreaDict(area_list)

        return dict_object

    def save_main_area_to_excel(self, main_area_dict_object, result_file_path):
        """
        将词典保存为excel文件
        :param main_area_dict_object:
        :param result_file_path:
        :return:
        """
        area_list = main_area_dict_object.get()
        self._save_to_excel(area_list, ['id', 'level'], result_file_path)

    def load_city_rank_from_excel(self, input_file_path):
        """
        适用于各种词典
        :param input_file_path:
        :return:
        """
        integer_column = {'id', 'rankLevel', "level"}
        area_list = self._load_from_excel(input_file_path, integer_column)

        dict_object = CityRankDict(area_list)

        return dict_object

    def save_city_rank_to_excel(self, city_rank_dict_object, result_file_path):
        area_list = city_rank_dict_object.get()
        self._save_to_excel(area_list, ['id', 'level', 'rankLevel'], result_file_path)

    def load_custom_city_rank_from_excel(self, input_file_path,
                                         sheet_name=None,
                                         city_column='city',
                                         rank_column='cityRank'):
        """
        加载自定义城市级别词典
        :param input_file_path: string,文件路径
        :param city_column: string, 表示城市的列名
        :param rank_column: string, 表示城市级别的列名
        :return:
        """
        if sheet_name:
            df_input = PandaTool.read_more(input_file_path, sheet_name=sheet_name)
        else:
            df_input = PandaTool.read_more(input_file_path)

        custom_rank_dict = dict()
        for index, row in df_input.iterrows():
            city_name = row[city_column]
            city_rank = row[rank_column]

            if pd.isna(city_name) or pd.isna(city_rank):
                continue
            city_name = str(city_name).strip()
            city_rank = city_rank

            custom_rank_dict[city_name] = city_rank

        return custom_rank_dict

    def load_custom_city_rank_from_db(self, mysql_table_name,
                                         sheet_name=None,
                                         city_column='city',
                                         rank_column='cityRank'):
        """
        加载自定义城市级别词典
        :param input_file_path: string,文件路径
        :param city_column: string, 表示城市的列名
        :param rank_column: string, 表示城市级别的列名
        :return:
        """
        df_input = LavwikiReader.get_as_df(mysql_table_name)

        custom_rank_dict = dict()
        for index, row in df_input.iterrows():
            city_name = row[city_column]
            city_rank = row[rank_column]

            if pd.isna(city_name) or pd.isna(city_rank):
                continue
            city_name = str(city_name).strip()
            city_rank = city_rank

            custom_rank_dict[city_name] = city_rank

        return custom_rank_dict


def gl_city_rank_filter(find_city_item):
    """
    城市级别查找时，增加一些过虑规则
    :return:
    """
    if len(find_city_item) > 1:
        # 1.1 检查并缩小范围
        tmp_dict_count_dict = dict()
        for item in find_city_item:
            current_level = item['level']
            if current_level not in tmp_dict_count_dict:
                tmp_dict_count_dict[current_level] = 0
            tmp_dict_count_dict[current_level] += 1

        if 1 in tmp_dict_count_dict and 2 in tmp_dict_count_dict:
            # TODO 同时存在1级、2级行政区域的，无法处理，
            return None
        if 1 in tmp_dict_count_dict and 3 in tmp_dict_count_dict:
            # TODO 同时存在1级、2级行政区域的，无法处理，
            return None
        if 2 in tmp_dict_count_dict and 3 in tmp_dict_count_dict:
            # TODO 同时存在2级、3级行政区域的，挑选第2级
            find_city_item = [item for item in find_city_item if item['level'] == 2]

    return find_city_item


class CustomCityRank(RowInterface):
    """
    根据自定义城市级别信息，提取地级城市、直辖市，然后分级、分类
    """

    def __init__(self,
                 default_value=None):
        self.default_value = default_value, default_value
        super(CustomCityRank, self).__init__(self.default_value)

        dict_tool = AreaDictTool()
        custom_rank_dict = dict_tool.load_custom_city_rank_from_db('lav2_custom_city_rank')
        self.main_area_object = dict_tool.load_main_area_from_db("lav2_china_area")

        # 20210819新加的，判断城市用
        self.city_list = list(custom_rank_dict.keys())

        self.custom_rank_detail_dict = dict()

        extract_processor = CityExtractProcessor(self.main_area_object, self.city_list)
        for name in custom_rank_dict:
            # TODO 应该只有1、2级城市，不应该会有县级城市，一级只会是直辖市，不会有省名
            find_city_item = extract_processor.process(name)
            if find_city_item is None or len(find_city_item) <= 0:
                # print("unknown city------==", str(name))
                continue
            if len(find_city_item) > 1:
                # TODO 有多个行政区域，且重名的，挑选2级区域，一级只会是直辖市，不会有省名
                find_city_item = [item for item in find_city_item if item['level'] == 2]
            if len(find_city_item) != 1:
                # print(find_city_item)
                # print("can not find city, may have many, name =", name)
                continue
            find_city_item = find_city_item[0]

            item = dict()
            item['areaCode'] = find_city_item['areaCode']
            item['shortName'] = find_city_item['shortName']
            item['level'] = find_city_item['level']
            item['name'] = find_city_item['name']
            item['oldName'] = name
            item['rankLevel'] = custom_rank_dict[name]

            self.custom_rank_detail_dict[item['areaCode']] = item

    def process(self, data, params=None):
        """

        :param data: string
        :param params:
        :return:
        """
        extract_processor = CityExtractProcessor(self.main_area_object, self.city_list)
        find_city_item = extract_processor.process(data)

        default_result = self.default_value

        # 1.查找城市、并确定范围
        if find_city_item is None or len(find_city_item) <= 0:
            return default_result

        find_city_item = gl_city_rank_filter(find_city_item)
        if find_city_item is None:
            return default_result

        target_rank_item = None
        for city_item in find_city_item:
            # 1、2级城市直接返回信息信息
            city_area_code = city_item['areaCode']
            if city_area_code in self.custom_rank_detail_dict:
                target_rank_item = self.custom_rank_detail_dict[city_area_code]
                break
            # 3级城市返回它的父类
            parent_area_code = city_item['parent']
            if parent_area_code in self.custom_rank_detail_dict:
                target_rank_item = self.custom_rank_detail_dict[parent_area_code]
                break

        if target_rank_item is None:
            return default_result

        result = dict()
        result['city'] = str(target_rank_item['shortName'])
        result['city_rank'] = str(target_rank_item["rankLevel"])

        return result['city'], result['city_rank']


if __name__ == '__main__':
    city_rank = CustomCityRank()
    print(city_rank.process("重庆 铜梁县"))