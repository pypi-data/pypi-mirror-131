# -*- coding: utf-8 -*-
# ----------------------------------------------
# purpose: 广告垃圾检测
# author : 
# create_time : 2020/6/29 15:32
# update_time : 2020/6/29 15:32
# copyright : Lavector
# ----------------------------------------------
"""
广告清洗
"""
import re
import codecs
import numpy as np

from lavda.util.mysql_util import *
from lavda.analysis.da_clean.clean_interface import *


class SpamInterface(object):
    def predict(self, text, params=None):
        """
        :param text:
        :param params:
        :return: bool
        """
        pass


class OrdinaryWays(object):
    @staticmethod
    def get_from2mysql(c_type="adword"):
        sql = """
        select keyword from %s
        """ % c_type
        result = np.array(LavwikiReader.execute_all(sql)[0])
        result = [i[0] for i in result]
        return result

    @staticmethod
    def get_clean(c_type):
        """
        type:mysql数据库表名，处理weibo垃圾、水军时的词

        """
        clean = OrdinaryWays.get_from2mysql(c_type)
        clean = [str(i).lower().strip() for i in clean if len(str(i).strip()) > 0]
        return clean

    @staticmethod
    def read_by_line(file_path):
        """
        按行读取数据
        :param file_path:
        :return:
        """
        data_list = list()
        with codecs.open(file_path, 'r', encoding="utf-8") as fp:
            for line in fp:
                line = line.strip()
                if len(line) > 0:
                    data_list.append(line)

        return data_list

    @staticmethod
    def has_chinese_count(text):
        """
        判断中文字符数量
        :param self:
        :param text:
        :return:
        """
        count = 0
        tmp_text = text
        if isinstance(tmp_text, str):
            tmp_text = str(tmp_text)
        for ch in tmp_text:
            if '\u4e00' <= ch <= '\u9fff':
                count += 1
        return count

    @staticmethod
    def is_num(text):
        """
        判断是否为数字，包括整数和浮点数
        :param text:
        :return:
        """
        # return text.isdigit()

        # pattern = re.compile(r'^[-+]?[-0-9]\d*\.\d*|[-+]?\.?[0-9]\d*$')
        # result = pattern.match(text)
        # if result:
        #     return True
        # else:
        #     return False

        if text.replace('.', '', 1).isdigit():
            return True
        return False

    @staticmethod
    def get_spam_dict(dict_file_path):
        word_set = set()
        # 1.加载广告词
        word_list = OrdinaryWays.read_by_line(dict_file_path)
        for word in word_list:
            tmp_word = word.strip()
            if tmp_word:
                # TODO 全部转小写
                word_set.add(tmp_word.lower())

        return word_set


class SpamPatternRule(SpamInterface):
    """
    基于正则规则判断，检查是否包含特定的正则表达式
    """
    def __init__(self):
        self.ads_item_rule_list = list()
        self._load()

    def _load(self):
        tmp_rule_set = OrdinaryWays.get_clean('weibo_ads_pattern_rule')
        for tmp_rule in tmp_rule_set:
            tmp_rule_pattern = re.compile(tmp_rule, re.S)
            self.ads_item_rule_list.append(tmp_rule_pattern)

    def predict(self, text, params=None):
        for re_rule_pattern in self.ads_item_rule_list:
            result = re_rule_pattern.search(text)
            if result and result.group() is not None:
                return True
        return False


class SpamHastagRule(SpamInterface):
    """
    基于 Hasttag 中的内容进行判断
    处理类型同pattern rule
    """

    def __init__(self, other_rule_list=None):
        """
        :param dict_file_path:
        :param other_rule_list: 其他自定义的规则
        """
        self.item_rule_list = list()
        self.other_rule_list = other_rule_list

        self._load()

    def _load(self):
        tmp_rule_set = OrdinaryWays.get_clean('weibo_ads_hastag_rule')

        for tmp_rule in tmp_rule_set:
            tmp_rule_pattern = re.compile(tmp_rule, re.S)
            self.item_rule_list.append(tmp_rule_pattern)

    def is_match(self, text, params=None):
        for re_rule_pattern in self.item_rule_list:
            result = re_rule_pattern.search(text)
            if result and result.group() is not None:
                return True
        return False

    def predict(self, text, params=None):
        r2_list = self._get_bracket(text, (u'【', u'】'))
        bracket_list = r2_list

        for item in bracket_list:
            tmp_item = item.strip()
            if self.other_rule_list:
                for other_rule in self.other_rule_list:
                    if other_rule.predict(tmp_item):
                        return True

            if self.is_match(tmp_item):
                return True
        return False

    def _get_bracket(self, text, bracket, drop_bracket=True):
        tmp_text = text
        re_string = u"[{}].*?[{}]".format(bracket[0], bracket[1])
        p1 = re.compile(re_string, re.S)  # 最小匹配
        find_list = re.findall(p1, tmp_text)

        result_list = list()
        if find_list:
            for item in find_list:
                tmp_item = item
                if drop_bracket:
                    tmp_item = tmp_item.replace(bracket[0], u'')
                    tmp_item = tmp_item.replace(bracket[1], u'')
                # TODO,由于抓取数据解析问题，可能许多符号会显示为？号，因此全替换掉
                tmp_item = tmp_item.replace(u'?', u'')
                result_list.append(tmp_item)
        return result_list


class ItemPriceRule(SpamInterface):
    """
    判断是否表示价格
    """
    def __init__(self):
        price_rule_str_list = [u'(￥|\$)\d+(\.\d+)?',
                               u'\d+(\.\d+)?(元|入)']
        rule_str = u'|'.join(price_rule_str_list)
        rule_str = u'(' + rule_str + u')'

        self.price_rule_pattern = re.compile(rule_str, re.S)

    def predict(self, text, params=None):
        """
        判断是否表示价格,只是表示可能是价格
        :param text:
        :return:
        """
        tmp_text = text
        # 1.根据正则查找
        tmp_text = tmp_text.replace(u' ', u'')

        result = self.price_rule_pattern.search(tmp_text)
        if result and result.group() is not None:
            return True

        # 2.是否为【】包起来的数字
        if u'【' in tmp_text or u'】' in tmp_text:
            tmp_item = tmp_text.replace(u'【', u'')
            tmp_item = tmp_item.replace(u'】', u'')
            if OrdinaryWays.is_num(tmp_item):
                return True

        return False

class ItemNumRule(SpamInterface):
    """
    判断是否为数字
    """
    def predict(self, text, params=None):
        if OrdinaryWays.is_num(text):
            return True

        return False


class SpamWordRule(SpamInterface):
    """
    根据是否包含特定的词来判断
    """

    def __init__(self,use_re=False):
        """

        :param dict_file_path:
        :param use_re: 是否使用正则表达式
        """
        self.word_set = set()
        self.rule_pattern = None

        self._load()

        self.use_re = use_re

    def _load(self):
        self.word_set = OrdinaryWays.get_clean('weibo_ads_word')
        self.rule_pattern = re.compile(u'|'.join(self.word_set), re.S)

    def _do_by_re(self, text, params=None):
        result = self.rule_pattern.search(text)
        if result and result.group() is not None:
            return True

        return False

    def _do(self, text, params=None):
        for word in self.word_set:
            if word in text:
                return True

        return False

    def predict(self, text, params=None):
        if self.use_re:
            return self._do_by_re(text)
        return self._do(text)


class AdsDelimiter(SpamInterface):
    """
    按照分隔符，来判断是否为广告
    """
    # 注意 最后一个是空格符
    SPLIT_CHAR = u'， '
    MAX_WORD_LEN = 30

    def __init__(self, rule_price):
        self.rule_price = rule_price

        self.item_rule_list = list()

        rule_str_set = OrdinaryWays.get_clean("weibo_ads_delimiter_rule")
        for tmp_rule in rule_str_set:
            tmp_rule_pattern = re.compile(tmp_rule, re.S)
            self.item_rule_list.append(tmp_rule_pattern)

    def match_by_pattern(self, text, params=None):
        """
        根据正则匹配查找
        :param text:
        :param params:
        :return:
        """
        for re_rule_pattern in self.item_rule_list:
            result = re_rule_pattern.search(text)
            if result and result.group() is not None:
                return True
        return False

    def predict(self, text, params=None):
        chinese_char_count = OrdinaryWays.has_chinese_count(text)
        if chinese_char_count > self.MAX_WORD_LEN:
            return False

        # 拆分数据，进行处理
        re_string = u'[{}]'.format(self.SPLIT_CHAR)
        text_list = re.split(re_string, text)
        text_list = [item.strip() for item in text_list if item.strip()]

        if len(text_list) < 2:
            return False

        # 根据广告词判断
        if self.match_by_pattern(text):
            return True

        # 根据是否有价格标识
        for item in text_list:
            # 几乎一定是价格
            if self.rule_price.predict(item) and len(item) < 6:
                return True
            # 是数字，但可能是价格
            if OrdinaryWays.is_num(item.strip()) and len(text_list) < 6:
                return True
            # 英文 off,eg:Burberry vip 50% off 只有355/36 ?
            if u'off' in item:
                return True

        return False


class AdsLineRule(SpamInterface):
    """
    以行为单位判断是否为广告
    """

    def __init__(self, rule_list):
        self.rule_list = rule_list

    def predict(self, text, params=None):
        sub_lines = text.split(u'\n')
        sub_lines = [item.strip() for item in sub_lines if item.strip()]
        for line in sub_lines:
            for rule in self.rule_list:
                if rule.predict(line):
                    return True
        return False


class AdsSpecialRule(SpamInterface):
    """
    特别规则，只针对几个特殊字符
    放一些不成熟的规则，后期有很大概率要调整的
    """
    SPECIAL_CHAR = [u'💰', u'💵', u'$']

    def predict(self, text, params=None):
        for item in self.SPECIAL_CHAR:
            if item in text:
                return True

        # 格式不全
        if u'【' in text and u'】' not in text:
            return True
        if u'【' not in text and u'】' in text:
            return True

        return False


class AdsPrefixRule(SpamInterface):
    """
    基于文本前缀判断
    """

    def __init__(self):
        self.base_rule = SpamPrefixRule()

    def predict(self, text, params=None):
        lines = params
        if len(lines) < 0:
            return False
        # 第一行
        if self.base_rule.predict(lines[0].strip()):
            return True

        # 第二行
        if self.base_rule.predict(lines[-1].strip()):
            return True

        return False


class SpamPrefixRule(SpamInterface):
    """
    基于文本前缀判断
    """
    def __init__(self, user_re=False):
        self.word_set = set()
        self.rule_pattern = None

        self._load()

        self.use_re = user_re

    def _load(self):
        # 1.加载广告词
        self.word_set = OrdinaryWays.get_clean('weibo_ads_prefix_word')

        rule_str = u"^" + u"(" + u'|'.join(self.word_set) + u')'
        self.rule_pattern = re.compile(rule_str, re.I | re.S)

    def _do_by_re(self, text, params=None):
        result = self.rule_pattern.search(text)
        if result and result.group() is not None:
            return True

        return False

    def _do(self, text, params=None):
        for word in self.word_set:
            if text.startswith(word):
                return True

        return False

    def predict(self, text, params=None):
        if self.use_re:
            return self._do_by_re(text)
        return self._do(text)


class AdsSuffixRule(SpamInterface):
    """
    基于文本后缀判断
    """

    def __init__(self):
        self.base_rule = SpamSuffixRule()

    def predict(self, text, params=None):
        """
        该文本是否为客观描述类
        :param text:
        :param params:
        :return:
        """
        lines = params
        if len(lines) < 0:
            return False

        # 第一行
        if self.base_rule.predict(lines[0]):
            return True

        # 最后一行
        if self.base_rule.predict(lines[-1]):
            return True

        return False


class SpamSuffixRule(SpamInterface):
    """
    基于文本前缀判断
    """

    def __init__(self, use_re=False):
        self.word_set = set()
        self.rule_pattern = None

        self._load()

        self.use_re = use_re

    def _load(self):
        self.word_set = OrdinaryWays.get_clean('weibo_ads_suffix_word')

        rule_str = u"(" + u'|'.join(self.word_set) + u')' + u"$"
        self.rule_pattern = re.compile(rule_str, re.I | re.S)

    def _do_by_re(self, text, params=None):
        result = self.rule_pattern.search(text)
        if result and result.group() is not None:
            return True

        return False

    def _do(self, text, params=None):
        for word in self.word_set:
            if text.endswith(word):
                return True

        return False

    def predict(self, text, params=None):
        if self.use_re:
            return self._do_by_re(text)
        return self._do(text)


class WeiboAdsRuleModel(RowInterface, CleanInterface):
    def __init__(self, **params):
        super(WeiboAdsRuleModel, self).__init__(CleanFlag.NO)

        self.rule_pattern = SpamPatternRule()
        self.rule_hastag = SpamHastagRule([ItemPriceRule(), ItemNumRule()])
        self.rule_word = SpamWordRule()
        self.rule_delimiter = AdsDelimiter(ItemPriceRule())

        sub_rule_list = list()
        sub_rule_list.append(self.rule_word)
        sub_rule_list.append(self.rule_pattern)
        sub_rule_list.append(self.rule_delimiter)
        sub_rule_list.append(self.rule_hastag)

        self.rule_list = list()
        self.rule_list.append(AdsLineRule(sub_rule_list))
        self.rule_list.append(AdsSpecialRule())
        self.rule_list.append(AdsPrefixRule())
        self.rule_list.append(AdsSuffixRule())

    def _clean(self, text):
        tmp_text = text
        # 去掉特殊的结尾符(html格式中包含)
        ch = chr(8203)
        tmp_text = tmp_text.replace(ch, u'')
        tmp_text = tmp_text.replace(u'\r\n', u'\n')

        # TODO 去掉多余的问号,有好些问号是解析或抓取时产生的，不是原文自带的
        tmp_text = tmp_text.replace(u'?', u'')

        return tmp_text

    def process(self, data, **params):
        """
        预测
        :param data: 文本
        :param params: 参数
        :return:
        """
        clean_text = str(data).lower()
        lines = clean_text.split(u'\n')
        lines = [line.strip() for line in lines]
        for rule in self.rule_list:
            if rule.predict(clean_text, lines):
                return CleanFlag.YES

        return CleanFlag.NO


def run_spam():
    sub_model_ads = WeiboAdsRuleModel()

    content = u'【19.9】宝丽康美 核桃黑芝麻黑豆代餐粉'
    # content = u'桃黑芝麻黑豆代餐粉'
    channel = u"weibo"
    result = sub_model_ads.process(content)
    print(result)


if __name__ == '__main__':
    run_spam()


