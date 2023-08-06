# -*- coding: utf-8 -*-
# ----------------------------------------------
# purpose : 
# author : LGD
# create_time : 2021/2/22 18:15
# update_time : 2021/2/22 18:15
# copyright : Lavector
# ----------------------------------------------
import os
import xml.etree.ElementTree as ET


class PyConfigParser(object):

    def get_default_config_dir(self):
        cur_cwd = os.getcwd()
        if os.path.exists(u'configs/'):
            return os.path.join(cur_cwd, u'configs/')
        elif os.path.exists(u'../config/'):
            return os.path.join(cur_cwd, u'../configs/')
        elif os.path.exists(u'../../configs/'):
            return os.path.join(cur_cwd, u'../../configs/')
        elif os.path.exists(u'../../../configs/'):
            return os.path.join(cur_cwd, u'../../../configs/')

        raise Exception("can not find confir root path!")

    def _clean_string(self, data):
        return data.strip()

    def parse_xml(self, file_name, file_dir=None):
        """

        :param file_name: 配置文件名，不带后缀
        :param file_dir: 配置文件所在的目录，相对路径和绝对路径均可以，
                         为None时，使用默认路径: ./configs/
        :return:
        """
        if file_dir:
            file_path = os.path.join(file_dir, file_name + u'.xml')
        else:
            default_dir = self.get_default_config_dir()
            file_path = os.path.join(default_dir, file_name + u'.xml')

        tree = ET.parse(file_path)
        root_node = tree.getroot()
        config_dict = dict()

        for section_child in root_node:
            tag_name = section_child.attrib[u'name']
            tag_name = self._clean_string(tag_name)
            config_dict[tag_name] = dict()
            if len(section_child) <= 0:
                continue

            for item_node in section_child:
                item_key = self._clean_string(item_node.attrib[u'name'])
                item_value = self._clean_string(item_node.text)
                config_dict[tag_name][item_key] = item_value

        return config_dict