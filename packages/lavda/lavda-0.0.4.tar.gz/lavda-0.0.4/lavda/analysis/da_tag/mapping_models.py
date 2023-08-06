# -*- coding: utf-8 -*-
# ----------------------------------------------
# purpose : 
# author : 
# create_time : 2020/7/1 16:13
# update_time : 2020/7/1 16:13
# copyright : Lavector
# ----------------------------------------------
import sys
import pickle
import pandas as pd
import contextlib
from lavda.analysis.da_tag.tree_like import au_get_tree, au_get_line


@contextlib.contextmanager
def pickle_context(filepath,obj,mode='wb'):
    pass



class _MappingCollect:

    def __init__(self, path):
        """
        mapping表的集合,相当于整个标签词表数据集
        :param path:
        """

        df_sheet = pd.read_excel(path, None)
        sheets = list(df_sheet.keys())
        self.__length = len(sheets)
        self._mapping = [Mapping(path, sheet) for sheet in sheets]
        self.relation = False

    def filter_by(self,name):
        """用于查找某一个sheet对象"""
        pass



class MappingCollect(_MappingCollect):
    def filter_by(self, **kwargs):
        """用于查找某一个sheet对象"""
        name = kwargs.get("name")
        filter_mappings = list(filter(lambda mapping:mapping.sheetname==name,self._mapping))
        if len(filter_mappings) > 0:
            filter_mapping = filter_mappings[0]
        else:
            filter_mapping = None
        return filter_mapping

    def add_sen_sheet(self,sheet_list):
        sheet_list = format_max_xml_kwargs(sheet_list)
        if sheet_list:
            for sheet_name in sheet_list:
                sen_result = self.filter_by(name=sheet_name)
                if sen_result is None:
                    print("情感预设失败,标签词表不含{}sheet".format(sheet_name))
                else:
                    sen_result.sentment =True

    def add_length_sheet(self, sheet_dic):
        sheet_dic = format_max_xml_kwargs(sheet_dic)
        if sheet_dic:
            for sheet_name, tag_length in sheet_dic.items():
                sen_result = self.filter_by(name=sheet_name)
                if sen_result is None:
                    print("距离设置失败,标签词表不含{}sheet".format(sheet_name))
                else:
                    sen_result.length = tag_length

    def __getitem__(self, item):
        return self._mapping[item]

    def to_pickle(self, param):
        save_pickle = open(param,'wb')
        pickle.dump(self,save_pickle)
        save_pickle.close()



class _Mapping:
    """
    对单个mapping表的数据结构进行封装,相当于单一sheet
    """
    def __init__(self, path, sheet):
        tree_line_tup = self.with_draw(path,sheet)
        self.mapping_list = tree_line_tup[1]
        self.mapping_df = tree_line_tup[0]
        self.sheetname = tree_line_tup[-1]
        self.sentment = True
        self.length = 0
        self.relation = None

    def with_draw(self,path,sheet):
        if "-" in sheet:
            sheet_name = sheet.split('-')[0]
            sheet_level = int(sheet.split('-')[-1])
            tree_tup = au_get_tree(path, sheet, sheet_level, sheet_name)
            return tree_tup
        else:
            line_tup = au_get_line(path, sheet)
            return line_tup

    @property
    def mapping_values(self):
        mapping_df = self.mapping_df.astype(str)
        maping_values = mapping_df[self.mapping_list].values
        return maping_values

    @property
    def choice(self):
        return 'content'



class Mapping(_Mapping):

    def __init__(self,path,sheet):
        super(Mapping, self).__init__(path,sheet)
        self.verifi = self.verification()


    def verification(self):
        datapram = {
            'code': 0,
            'msg': "词表正常",
            'sheetname': self.sheetname
        }
        before_verifi_list = self.mapping_values
        verifi_list = [verifi[-1] for verifi in before_verifi_list]
        for veri in verifi_list:
            if str(veri) in ["","||"]:
                datapram['code'] = -1
                datapram['msg'] = "词表异常"
                # print("异常码:{},异常提示:{},词表名:{}".format(datapram['code'],datapram['msg'],datapram['sheetname']))
                return datapram
            if str(veri)[0] == "|" or str(veri[-1]) == "|":
                datapram['code'] = -2
                datapram['msg'] = "词表异常"
                # print("异常码:{},异常提示:{},词表名:{}".format(datapram['code'], datapram['msg'], datapram['sheetname']))


        return datapram




class _Relation_Mapping_collect(MappingCollect):
    def __init__(self,path):
        super(_Relation_Mapping_collect, self).__init__(path)
        self._mapping = [self.add_primary_id(relation_mapping) for relation_mapping in self._mapping]
        self.relation = True

    def add_primary_id(self, mapping):
        name = mapping.sheetname
        df = mapping.mapping_df
        df['{}-id'.format(name)] = range(df.shape[0])
        mapping.mapping_df = df
        return mapping



class Relation_Mapping_collect(_Relation_Mapping_collect):
    def get_map_name_collect(self):
        map_name_collect = [_name.sheetname for _name in self]
        return map_name_collect



def format_max_xml_kwargs(value):
    value = eval(value) if value else value
    return value
