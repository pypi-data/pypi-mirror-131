# -*- coding: utf-8 -*-
# ----------------------------------------------
# purpose: weibo水军类垃圾检测
# author : 
# create_time : 2020/6/29 15:40
# update_time : 2020/6/29 15:40
# copyright : Lavector
# ----------------------------------------------
import re
import emoji
import codecs
import numpy as np
from lavda.analysis.da_clean.clean_interface import *
from lavda.util.mysql_util import *


class WaterRuleInterface(object):
    def predict(self, text, params=None):
        """
        :param text:
        :param params:
        :return:
        """
        pass


class WaterOrdinaryWays(object):
    """
    抽取的普通方法
    """

    @staticmethod
    def get_from2mysql(c_type="adword"):
        sql = """
        select keyword from %s
        """ % c_type
        # print(sql)
        result = np.array(LavwikiReader.execute_all(sql)[0])
        result = [i[0] for i in result]
        return result

    @staticmethod
    def get_clean(c_type):
        """
        type:mysql数据库表名，处理weibo垃圾、水军时的词

        """
        clean = WaterOrdinaryWays.get_from2mysql(c_type)
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
    def get_weibo_topic(text):
        tmp_text = text
        p1 = re.compile('#.*?#', re.S)  # 最小匹配
        result_list = re.findall(p1, tmp_text)
        return result_list

    @staticmethod
    def get_weibo_user_tag(text):
        r_user_end = re.compile('@[\S]+')
        result = r_user_end.findall(text)
        return result


class WaterWordRule(WaterRuleInterface):
    """
    根据是否包括特定词来判断
    这些广告词必须有很强的代表性，即当出现此广告词时，这条文本几乎肯定是广告
    """

    def __init__(self):
        self.word_set = set()
        self._load()

    def _load(self):
        # 1.加载广告词
        word_list = WaterOrdinaryWays.get_clean('weibo_water_word')
        for word in word_list:
            tmp_word = word.strip()
            if tmp_word and len(tmp_word) > 0:
                self.word_set.add(tmp_word)

    def predict(self, text, params=None):
        for word in self.word_set:
            if word in text:
                return True
        return False


class WaterHastagRule(WaterRuleInterface):
    """
    基于Hasttag判断是否为广告
    """
    def __init__(self):
        self.item_rule_list = list()
        self._load()

    def _load(self):
        # 2.加载广告item规则
        rule_list = WaterOrdinaryWays.get_clean('weibo_water_hastag_rule')
        tmp_rule_set = set()
        for rule in rule_list:
            tmp_rule = rule.strip()
            if tmp_rule:
                tmp_rule_set.add(tmp_rule)

        for tmp_rule in tmp_rule_set:
            tmp_rule_pattern = re.compile(tmp_rule, re.S)
            self.item_rule_list.append(tmp_rule_pattern)

    def _get_bracket(self, text, bracket, drop_bracket=True):
        """
        找出原文中带【】的字符串。result_list
        :param text:
        :param bracket:
        :param drop_bracket:
        :return:
        """
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
                result_list.append(tmp_item)
        return result_list

    def is_match_item(self, text, params=None):
        """
        原文把找出的词的【】去掉，和词库中的词比较，词在库中就返回true;
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
        r2_list = self._get_bracket(text, (u'【', u'】'))
        bracket_list = r2_list

        for item in bracket_list:
            tmp_item = item.strip()
            if self.is_match_item(tmp_item):
                return True
        return False


class WaterRepeatPrefix(WaterRuleInterface):
    """
    根据连续出现的前缀进行判断，这些前缀可能就是明星名字
    """
    # 注意最后一个是空格
    SPLIT_CHAR = u'！， |  '
    MAX_REPEAT_COUNT = 5
    EXCEPTION_WORD = [u'比如']

    def predict(self, text, params=None):

        # 1.根据前缀进行分析
        topic_text_list = self._divide_by_hastag_topic(text)
        if self._has_prefix(topic_text_list):
            return True
        user_tag_text_list = self._divide_by_hastag_user_tag(text)
        if self._has_prefix(user_tag_text_list):
            return True
        punc_text_list = self._divide_by_punc(text)
        if self._has_prefix(punc_text_list):
            return True
        emoji_text_list = self._divide_by_emoji(text)
        if self._has_prefix(emoji_text_list):
            return True

        # 2. user tag和topic中出现同名
        user_tag_set = set(user_tag_text_list)
        topic_set = set(topic_text_list)
        for user in user_tag_set:
            for topic in topic_set:
                if user in topic:
                    return True

        return False

    def _has_prefix(self, text_list, ngram=True):
        if ngram:
            max_count = self._get_max_ngram(text_list, 2)
            if max_count >= self.MAX_REPEAT_COUNT:
                return True
            max_count = self._get_max_ngram(text_list, 3)
            if max_count >= self.MAX_REPEAT_COUNT:
                return True
        else:
            max_count = 0
            gram_dict = dict()
            for item in text_list:
                if item in gram_dict:
                    gram_dict[item] += 1
                else:
                    gram_dict[item] = 1
                if gram_dict[item] > max_count:
                    max_count = gram_dict[item]

            if max_count >= self.MAX_REPEAT_COUNT:
                return True

        return False

    def _get_max_ngram(self, text_list, n):
        ngram_dict = dict()
        max_count = 0
        for item in text_list:
            sub_item = item[:n]
            if sub_item in self.EXCEPTION_WORD:
                continue
            # TODO 止前gram必须全是汉字
            if len(sub_item) != n:
                continue
            if WaterOrdinaryWays.has_chinese_count(sub_item) != n:
                continue
            if not sub_item:
                continue
            if sub_item in ngram_dict:
                ngram_dict[sub_item] += 1
            else:
                ngram_dict[sub_item] = 1
            if ngram_dict[sub_item] > max_count:
                max_count = ngram_dict[sub_item]

        return max_count

    def _divide_by_hastag_topic(self, text):
        tmp_text_list = WaterOrdinaryWays.get_weibo_topic(text)
        text_list = list()
        for item in tmp_text_list:
            item = item.replace(u'#', u'').strip()
            if not item:
                continue
            text_list.append(item)

        return text_list

    def _divide_by_hastag_user_tag(self, text):
        tmp_text_list = WaterOrdinaryWays.get_weibo_user_tag(text)
        text_list = list()
        for item in tmp_text_list:
            item = item.replace(u'@', u'').strip()
            if not item:
                continue
            text_list.append(item)

        return text_list

    def _divide_by_punc(self, text):
        """
        根据标点符号切分
        :param text:
        :return:
        """
        re_string = u'[{}]'.format(self.SPLIT_CHAR)
        text_list = re.split(re_string, text)
        text_list = [item.strip() for item in text_list if item.strip()]

        return text_list

    def _divide_by_emoji(self, text):
        """
        根据表情符号切分
        :param text:
        :return:
        """
        emoji_text = emoji.demojize(text)

        # 找到所有表情符
        p1 = re.compile(':.*?:', re.S)  # 最小匹配
        result_list = re.findall(p1, emoji_text)
        emoji_set = set()
        for item in result_list:
            item = item.replace(u':', u'')
            emoji_set.add(item)

        # 按表情拆分
        sub_text_list = re.split('[:.*?:]', emoji_text)

        # 去掉表情符
        text_list = list()
        for item in sub_text_list:
            if item in emoji_set:
                continue
            text_list.append(item)

        return text_list


class WaterForwardMicroblogRule(WaterRuleInterface):
    """
    以  转发微博  或 report  开头的都算水军
    明星名字出现6次以上都算水军
    """
    def __init__(self):
        sql = "select name from lav2bgc_star where channel='weibo' and classify='personal';"
        self.weibo_star_list = [i[0] for i in np.array(LavwikiReader.execute_all(sql)[0])]
    def predict(self, text, params=None):
        if re.match(r"^转发微博", text) or re.match(r"^report", text.lower()):
            return True
        for i in self.weibo_star_list:
            text_list = text.split(i)
            text_list_len = len(text_list)
            if text_list_len > 6:
                return True
        return False


class WeiboWaterRuleModel(RowInterface, CleanInterface):
    """
    将以上三种规则整合在一起判断
    """
    def __init__(self, **params):
        super(WeiboWaterRuleModel, self).__init__(CleanFlag.NO)

        self.rule_list = list()
        self.rule_list.append(WaterWordRule())
        self.rule_list.append(WaterRepeatPrefix())
        self.rule_list.append(WaterHastagRule())
        self.rule_list.append(WaterForwardMicroblogRule())

    def process(self, data, **params):
        clean_text = str(data).lower()
        for rule in self.rule_list:
            if rule.predict(clean_text):
                return CleanFlag.YES
        return CleanFlag.NO


def main():

    sub_model_water = WeiboWaterRuleModel()

    # content = u'【19.9】宝丽康美 核桃黑芝麻黑豆代餐粉'
    content = u'活粉@助力,@助力,@助力,@助力,@助力,@助力,@助力,@助力,@助力4hd44,'
    channel = u"weibo"
    # df = PandaTool.read(r'C:\Users\zhang\Desktop\test.xlsx')

    # result = df.apply(lambda line: sub_model_water.process(line["content"], line["channel"]), axis=1).astype(int)
    result = sub_model_water.process(content)
    print(result)


if __name__ == '__main__':
    main()
