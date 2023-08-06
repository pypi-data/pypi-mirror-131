# -*- coding: utf-8 -*-
# ----------------------------------------------
# purpose: 全渠道水军类垃圾检测
# author :
# create_time : 2020/11/30 15:40
# update_time : 2020/11/30 15:40
# copyright : Lavector
# ----------------------------------------------
import re
import emoji
import codecs
import numpy as np
from lavda.analysis.da_clean.water_spam import *
from lavda.util.mysql_util import *
from lavda.analysis.da_tag.diatance_tag import continuous_addition


class WaterRuleInterface(object):
    def predict(self, text, params=None):
        """
        :param text:
        :param params:
        :return:
        """
        pass


# 新加的水军判断,作用于所有渠道
class navy_judgment(WaterRuleInterface):

    def __init__(self):
        # TODO 获取水军列表
        self._load()

    def _load(self):
        self.navy_nickname_list = WaterOrdinaryWays.get_clean('nickname_navy_judgment_word')
        self.navy_content_list = WaterOrdinaryWays.get_clean('content_navy_judgment_word')
        self.navy_introduce_list = WaterOrdinaryWays.get_clean('introduce_navy_judgment_word')

    def judgment(self, data):
        if data['nickname']:
            nickname = str(data['nickname']).lower()
            for navy_nickname_word in self.navy_nickname_list:
                if navy_nickname_word in nickname:
                    return True
        if data['introduce']:
            introduce = str(data['introduce']).lower()
            for navy_introduce_word in self.navy_introduce_list:
                if navy_introduce_word in introduce:
                    return True
        if data['content']:
            text_content = str(data['content']).lower()
            # 判断文本内容是否含有水军判断词
            for navy_content_word in self.navy_content_list:
                if navy_content_word in text_content:
                    return True
            # 〖9.9〗 括号里面是价格
            bracket_content_list = re.findall(r"〖(.*?)〗", text_content)
            if bracket_content_list:
                for bracket_content in bracket_content_list:
                    if '.' in bracket_content and bracket_content.split('.')[0].isnumeric() or bracket_content.isnumeric():
                        return True
            # 判断是否有  满+享
            if continuous_addition(text_content, '满+享', 7):
                return True
            # 判断是否有过多话题##
            if text_content.count('##') >= 15:
                return True
        return False

    def predict(self, data, params=None):
        return self.judgment(data)


class WaterRuleModel(RowInterface, CleanInterface):
    """
    将微博的三种规则和全渠道的一种规则整合在一起判断
    """

    def __init__(self, **params):
        super(WaterRuleModel, self).__init__(CleanFlag.NO)

        self.weibo_rule_list = list()
        self.weibo_rule_list.append(WaterWordRule())
        self.weibo_rule_list.append(WaterRepeatPrefix())
        self.weibo_rule_list.append(WaterHastagRule())
        self.weibo_rule_list.append(WaterForwardMicroblogRule())
        # 新增作用于全渠道的水军判断
        self.all_rule_list = list()
        self.all_rule_list.append(navy_judgment())

    def process(self, data, **params):
        column_name_list = ['channel', 'introduce', 'content', 'nickname']
        for column_name in column_name_list:
            if column_name not in data:
                data[column_name] = ''
            if not data[column_name]:
                data[column_name] = ''
        if data['channel'] == 'weibo':
            for rule in self.weibo_rule_list:
                if rule.predict(data['content']):
                    return CleanFlag.YES

        for _rule in self.all_rule_list:
            if _rule.predict(data):
                return CleanFlag.YES
        return CleanFlag.NO

if __name__ == '__main__':
    dic = {'nickname':'daigo','introduce':'vx:sdfsdf'}
    c = WaterRuleModel()
    print(c.process(dic))
