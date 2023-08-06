# -*- coding: utf-8 -*-
# ----------------------------------------------
# purpose : 打标签功能入口
# author : LGD
# create_time : 2021/2/22 09:54
# update_time : 2021/2/22 09:54
# copyright : Lavector
# ----------------------------------------------
import os

from lavda.config.maxda_config import get_nlp_model_path
from lavda.backexcutor.analysis_interface import DfProcessInterface, RowInterface
from lavda.analysis.da_tag.label_extract import KeywordBaseExtractor, KeywordSegmentExtractor, KeywordExtractUtil
from lavda.analysis.da_tag.label_dict import PandaLabelDictTool, LineLabelDict
from lavda.analysis.da_tag.label_verify import VerifyLabelDict
from lavda.analysis.da_tag.label_core import LabelComponentChecker


class LabelBase(RowInterface):
    def __init__(self, extractor, use_model=False,
                 model_root_path=None,
                 default_value=None):
        super(LabelBase, self).__init__((default_value, default_value, default_value))
        self.extractor = extractor
        self.use_model = eval(use_model) if isinstance(use_model, str) else use_model
        if self.use_model:

            if model_root_path is None:
                model_root_path = get_nlp_model_path()

            self.com_checker = LabelComponentChecker(root_model_path=model_root_path)

            self.com_mapping_kid = dict()
        else:
            self.com_checker = None
            self.com_mapping_kid = dict()

    @property
    def mc(self):
        return self.extractor.mc

    def load_config_data(self, **config):
        # todo 计划取消打标前词表验证，改为上传时词表验证
        # tag_config_path = configs['mappingDictPath']
        # ver = VerifyLabelDict(tag_config_path)
        # analyze_result = ver.analyze()
        # if len(analyze_result) > 0:
        #     raise Exception("mapping dict has error")

        self.extractor.load_config_data(**config)

        # 确定模型需要处理的keyword
        # mapping 索引 => kid
        if self.use_model:
            self.com_mapping_kid = dict()
            for i, cur_mapping in enumerate(self.extractor.mc.mappings):
                if isinstance(self.mc, LineLabelDict):
                    # TODO 成分之类不可能在标准词表中出现
                    continue

                id2relation = cur_mapping.id2relation
                sel_kid_set = set()
                for one_kid in id2relation:
                    # 最后两位分别为keyword，和kid，因此要排除掉
                    cur_relation = id2relation[one_kid][:-2]
                    if '成分' in cur_relation:
                        sel_kid_set.add(one_kid)
                if len(sel_kid_set) <= 0:
                    continue
                self.com_mapping_kid[i] = sel_kid_set

    def analyze_semantics(self, input_data_dict, keyword_result):
        """
        语义级标签识别
        :param input_data_dict:
        :param keyword_result:
        :return:
        """
        # 2.语义级判断
        for i, one_result in enumerate(keyword_result):
            # cur_mapping = self.mc.mappings[i]
            if i not in self.com_mapping_kid:
                continue

            # mapping_name = cur_mapping.label_name
            # id2relation = cur_mapping.id2relation
            for col in input_data_dict:
                select_one_result = list()
                non_select_one_result = list()
                for one_item in one_result[col]:
                    # TODO 判断是否为成分

                    if one_item['kid'] in self.com_mapping_kid[i]:
                        select_one_result.append(one_item)
                    else:
                        non_select_one_result.append(one_item)

                last_col_result = non_select_one_result
                if len(select_one_result) > 0:
                    col_content = input_data_dict[col]
                    predict_result = self.com_checker.predict(col_content, select_one_result)
                    predict_one_result = list()
                    for k, k_result in enumerate(predict_result):
                        if k_result:
                            predict_one_result.append(select_one_result[k])

                    last_col_result.extend(predict_one_result)

                one_result[col] = last_col_result

        return keyword_result

    def do_label(self, data, **params):
        # 1.初步提取
        input_data_dict, keyword_result = self.extractor.process(data, **{"merge_and_format": False,
                                                                          "return_all": True})

        # 2.语义级标签识别
        if self.use_model:
            keyword_result = self.analyze_semantics(input_data_dict, keyword_result)

        # 3.结果合并并格式化
        merge_data = self.extractor.merge_and_format(keyword_result, input_data_dict=input_data_dict)
        last_result = self.extractor.build_result_format(keyword_result, merge_data)

        return last_result

    def process(self, data, **params):

        return self.do_label(data, **params)


class LabelDealSimple(LabelBase):
    def __init__(self, use_model=False,
                 model_root_path=None,
                 default_value=None):
        extractor = KeywordBaseExtractor()
        super(LabelDealSimple, self).__init__(extractor, use_model, model_root_path, default_value=default_value)


class LabelDealRelation(LabelBase):
    def __init__(self, use_model=False,
                 model_root_path=None,
                 default_value=None):
        extractor = KeywordSegmentExtractor()
        super(LabelDealRelation, self).__init__(extractor, use_model, model_root_path, default_value=default_value)


class LabelResultFormat(DfProcessInterface):
    def __init__(self, intermediate='tag_result', add_head_text='tag_format_'):
        """

        :param intermediate: string,打标签中间结果字段名
        :param add_head_text: string，格式化后结果字段名前缀
        """
        self.intermediate = intermediate
        self.add_head_text = add_head_text
        self._mc = None

    def load_config_data(self, **config):
        dict_tool = PandaLabelDictTool()

        label_dict_path = config['mappingDictPath']
        self._mc = dict_tool.load_all_from_file(label_dict_path)

    def process(self, data, **params):
        df_format = KeywordExtractUtil.expand_and_format(data, self._mc, tag_result_col=self.intermediate,
                                                         result_prefix=self.add_head_text)


        return df_format






