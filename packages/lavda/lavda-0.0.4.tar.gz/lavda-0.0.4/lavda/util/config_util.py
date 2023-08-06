# -*- coding: utf-8 -*-
# ----------------------------------------------
# purpose : 配置加载/解析功能
# author : 
# create_time : 2020/6/29 16:47
# update_time : 2020/6/29 16:47
# copyright : Lavector
# ----------------------------------------------
import xml.etree.ElementTree as ET


class ConfigUtil(object):
    @staticmethod
    def _clean_string(data, default_value=""):
        if data is None:
            return default_value
        return data.strip()

    @staticmethod
    def get_flow_config(file_path):
        """
        解析任务流配置
        :param file_path: 配置文件名，不带后缀
        :return:
        """
        tree = ET.parse(file_path)
        root_node = tree.getroot()
        config_list = list()

        for section_child in root_node:
            if len(section_child) <= 0:
                continue

            one_config_dict = dict()

            for item_node in section_child:
                item_key = ConfigUtil._clean_string(item_node.attrib[u'name'])
                if len(item_node) > 0:
                    sub_dict = dict()
                    one_config_dict[item_key] = sub_dict
                    for sub_item_node in item_node:
                        sub_item_key = ConfigUtil._clean_string(sub_item_node.attrib[u'name'])
                        sub_item_value = ConfigUtil._clean_string(sub_item_node.text)
                        sub_dict[sub_item_key] = sub_item_value
                else:
                    item_value = ConfigUtil._clean_string(item_node.text)
                    one_config_dict[item_key] = item_value

            if one_config_dict:
                config_list.append(one_config_dict)

        return config_list


if __name__ == '__main__':
    pass