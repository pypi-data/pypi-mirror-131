#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Author : dada
# @time   : 2020/7/7 17:00



# class TagDeal():
#     pass
import pickle
from lavda.backexcutor.analysis_interface import DfProcessInterface, RowInterface
from lavda.analysis.da_tag.mapping_models import MappingCollect, Relation_Mapping_collect
from lavda.analysis.da_tag.split_tag import max_split_tag, max_relation_split_tag
from lavda.analysis.da_tag.tag import TextMatch2, deal_sentence_tag, TagContentChoiceCollect
from lavda.analysis.da_tag.tag_config import tag_choice_dic
from lavda.analysis.da_tag.Filed_Services import VerMappingCollect

the_clean_list = ['tag_clean_len','tag_clean_no_chinese_english','tag_clean_weibo_ads','tag_clean_ec_ads','tag_clean_weibo_water']

class TagConfig:
    pass
    # def __init__(self):
    #     self.name = ""



class TagDealSimple(RowInterface,TagConfig):

    def __init__(self, tag_sen_list=None, distance_dict=None,default_value=None):
        super(TagDealSimple, self).__init__(default_value)
        self.tag_sen_list = tag_sen_list
        self.distance_dict = distance_dict

    def load_config_data(self, **config):

        merge_dict_path = config['mappingDictPath']
        check_result = VerMappingCollect(merge_dict_path).ver_status
        assert list(check_result.keys())[0] != 1, "关键词表有错"
        # 合并结果数据
        mapping = MappingCollect(merge_dict_path)
        mapping.add_sen_sheet(self.tag_sen_list)
        mapping.add_length_sheet(self.distance_dict)
        mapping.to_pickle(merge_dict_path.replace("xlsx","pkl"))
        self.mapping = mapping


    def process(self, data, **params):
        merge_content = TagContentChoiceCollect(tag_choice_dic)
        line_column_list = list(data.keys())
        filter_clean_list = list(filter(lambda column: column in the_clean_list, line_column_list))
        filter_clean_list_value = [int(data[value]) for value in filter_clean_list]
        tag_dict = dict()
        for _map in self.mapping:
            # if sum(filter_clean_list_value) > 0:
            #     tag_dict[_map.sheetname] = ""
            # else:
            tag_dict[_map.sheetname] = TextMatch2.one_match_multi_mix(data, _map,merge_content,default_len=7)

        return str(tag_dict)



class ResultTagFormat(DfProcessInterface):
    def __init__(self, intermediate, add_head_text):
        self.intermediate = intermediate
        self.add_head_text = add_head_text

    def load_config_data(self, **config):
        tag_dict_path = config['TagDictPath']
        tag_dict_path = tag_dict_path.replace("xlsx", "pkl")
        tag_dict = open(tag_dict_path, 'rb')
        mapping = pickle.load(tag_dict)
        self.mapping = mapping

    def process(self, data, **params):
        if self.mapping.relation:
            data = max_relation_split_tag(data,self.mapping,self.intermediate,self.add_head_text)
        else:
            data = max_split_tag(data,self.mapping,self.intermediate,self.add_head_text)
        return data



class TagDealRelationSimple(RowInterface,TagConfig):

    def __init__(self, tag_sen_list=None, distance_dict=None, default_value=None):
        super(TagDealRelationSimple, self).__init__((default_value, default_value, default_value))


    def load_config_data(self, **config):

        merge_dict_path = config['mappingDictPath']
        check_result = VerMappingCollect(merge_dict_path).ver_status
        assert list(check_result.keys())[0] != 1, "关键词表有错"
        # 合并结果数据
        mapping = Relation_Mapping_collect(merge_dict_path)
        mapping.to_pickle(merge_dict_path.replace("xlsx","pkl"))
        self.mapping = mapping
        self._ = 0
        for map_i in self.mapping:
            if map_i.sheetname == '品牌' and '品牌(需求)' in map_i.mapping_df.columns:
                self.map_1 = map_i.mapping_df[map_i.mapping_df['品牌(需求)'] == 1]
                self.map_0 = map_i.mapping_df[map_i.mapping_df['品牌(需求)'] == 0]
                self._ = 1

    def process(self, data, **params):
        if self._:
            result = deal_sentence_tag(data, self.mapping, self.map_1, self.map_0)
        else:
            result = deal_sentence_tag(data, self.mapping)
        # result[-1] 存放的是三列需求的数据：关键词包含父级关系，关键词，打到的词，
        # keyword_list = []
        aspect_list = []
        new_aspect_list = []
        keyword_parents_list = []
        for i in result[-1]:
            keyword_parents_list.append(i.split('*')[0])
            # keyword_list.append(i.split('*')[1])
            aspect_list.append(i.split('*')[2])
        for i in aspect_list:
            if ',' in i:
                new_aspect_list.extend(i.split(','))
            else:
                new_aspect_list.append(i)
        return str(result[0]), str(list(set(keyword_parents_list))), str(list(set(new_aspect_list)))
