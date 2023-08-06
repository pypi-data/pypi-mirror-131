# -*- coding: utf-8 -*-
# ----------------------------------------------
# purpose : 打标签核心功能
# author : 
# create_time : 2020/7/1 16:33
# update_time : 2020/7/1 16:33
# copyright : Lavector
# ----------------------------------------------
import numpy as np
from lavda.util.text_util import *
from lavda.backexcutor.analysis_interface import *
from lavda.analysis.da_extract.text_format import Tradition2Simple
from lavda.analysis.da_tag.mapping_models import *
from lavda.analysis.da_tag.diatance_tag import *
from lavda.analysis.da_tag.tag_config import tag_choice_dic
from lavda.analysis.da_clean.water_spam import WaterOrdinaryWays
from lavda.config.maxda_config import *

class TextMatch(object):
    def __init__(self):
        desc = """
        ## 匹配模式
        # 	1对1，  one_match_one 词的完全匹配
        # 	1对多， one_match_multi_or 多词或者匹配
        # 	1对多， one_match_multi_and_and 多词并且包含匹配
        # 	1对多， one_match_multi_and_or  多词并且不包含匹配
        # 	1对多， one_match_multi_mix 多词并且or或者匹配

        并且 & 或者 |
        """
        print(desc)

    @staticmethod
    def one_match_one(content, line):
        content = get_Text2Formal(content)
        da_tag = get_Text2Formal(line["da_tag"])
        return da_tag if content == da_tag else False

    @staticmethod
    def one_match_multi_or(content, da_tag):
        """
        目前好像还没有需求
        """
        words = set([i for i in da_tag.split("|") if len(i) > 0])
        return True if re.search("|".join(words), content) else False
    @staticmethod
    def one_match_multi_or_clause(content, da_tag):
        """
        ”修改为了分句的一个需求
        """
        l = []
        words = set([i for i in da_tag.split("|") if len(i) > 0])
        for i in words:
            if i in content:
                l.append(i)
        return l
    @staticmethod
    def one_match_multi_and_or(content, da_tag):
        # 包含 tag1 但不包含 tag2
        tag = da_tag.split("-")
        status = various(content, tag,default_len=7)
        return status

    @staticmethod
    def one_match_multi_and_and(content, da_tag):
        # 包含 tag1 并且包含 tag2
        tag = da_tag.split("+")
        status = exclude(content, tag)
        return status

    @classmethod
    def one_match_multi_mix(cls, line, mapping, Sentment=False, choice="content"):
        """
        line: 表示每一行的数据
        mapping: 表示这个mapping文件的内容
        """
        content = get_Text2Formal(line[choice])
        channel = line['channel']
        The_Other = []
        Tag_Sen_Keword = []

        for k_map in mapping:

            Be_Label_List = []

            tag = 0

            da_tag = str(k_map[-1])
            if "-" not in da_tag and "+" not in da_tag:
                tag += cls.one_match_multi_or(content, da_tag)
                result1 = set(re.findall(da_tag, content))
                list1 = list(result1)
                Be_Label_List.extend(list1)
            else:
                for i in da_tag.split("|"):
                    if "-" in i:
                        if cls.one_match_multi_and_or(content, i):
                            if '(' in i or '（' in i:
                                i = i.split('-')[0][1:-1].split('+')
                                Be_Label_List.extend(i)
                            else:
                                Be_Label_List.append(i.split("-")[0])

                    elif "+" in i:
                        if cls.one_match_multi_and_and(content, i):
                            Be_Label_List.append(i.split("+")[0])

                    else:
                        if cls.one_match_multi_or(content, i):
                            Be_Label_List.append(i)

            if len(Be_Label_List) > 0:
                if Sentment == True:
                    # TODO 暂时注释掉
                    Sen_Collect = None  # run_aspect_sentiment(line['content'], channel, Be_Label_List)
                    Sen = Match_Sentiment(Sen_Collect)
                    print(Sen)
                    k_json = {"tag_product_1": k_map[0], "product_keyword": k_map[1], "brand_Positivity":
                        Sen['Positivity'], "brand_Neutral": Sen['Neutral'], "brand_Bad": Sen['Bad']}


                else:
                    k_json = {"tag_product_1": k_map[0], "product_keyword": k_map[1]}

                Tag_Sen_Keword.append(k_json)

        return Tag_Sen_Keword, The_Other


def Match_Sentiment(dic):
    Positivity = 0
    Neutral = 0
    Bad = 0
    for i, j in dic.items():
        Positivity += j['正向']
        Neutral += j['中性']
        Bad += j['负向']
    return {'Positivity': Positivity, 'Neutral': Neutral, 'Bad': Bad}


class TextMatch2():
    negative_word_list = WaterOrdinaryWays.get_clean('negative_word_judgment')
    goumai_list = WaterOrdinaryWays.get_clean('goumai_word_judgment')
    def __init__(self):
        self.name = None

    @staticmethod
    def is_negative_judgment(tag):
        if '@' in tag or '#' in tag:
            return True
        return False

    @staticmethod
    def negative_word_judgment(text, tag, default_length=5):
        '''
        对单个词进行否定判断
        :param text: 文本内容
        :param tag_label: 标签 @ 要否定词  #不要否定词
        :param tag: 需要判断的否定词
        :param default_length:
        :return:
        '''
        # TODO 否定词判断 就是一个最简单的否定词判断 只看前后是否有否定词然后返回
        # 否定词举例      ['莫', '未', '不怎么', '忽视', '绝无', '别说', '未必', '忘记', '放弃', '并非', '没', '从未', '不是',
        #                       '杜绝', '忌', '毫无', '绝不', '无须', '难以', '非', '无', '从来不', '不要', '从不', '不再', '绝不能',
        #                       '木有', '防止', '无法', '不会', '未尝', '永不', '切勿', '从没', '别', '决不', '不曾', '勿', '不用']
        tag_label = tag[0]
        _tag = tag[1:]
        main_index_list = index_list(text, _tag)
        for _ in main_index_list:
            status = list(filter(
                lambda x: x in text[_ - default_length if _ - default_length >= 0 else 0:_ + default_length],
                TextMatch2.negative_word_list))
            if tag_label == '@':  # 要否定词      @吸收 ---> 不吸收
                if status:
                    return True
            elif tag_label == '#':  # 不要否定词   #滋润  ---> 滋润-不滋润
                if not status:
                    return True
        return False

    @staticmethod
    def one_match_multi_or_clause(content, da_tag):
        """
        ”修改为了分句的一个需求
        """
        l = []
        words = set([i for i in da_tag.split("|") if len(i) > 0])
        for i in words:
            if TextMatch2.is_negative_judgment(i):
                if TextMatch2.negative_word_judgment(content, i):
                    l.append(i)
            elif i in content:
                l.append(i)
        return l

    # @staticmethod
    # def one_match_one(content, line):
    #     content = get_Text2Formal(content)
    #     da_tag = get_Text2Formal(line["da_tag"])
    #     return da_tag if content == da_tag else False

    @staticmethod
    def one_match_multi_or(content, da_tag):
        """
        修改增加否定词判断
        """
        words = set([i for i in da_tag.split("|") if len(i) > 0])
        for i in words:
            if TextMatch2.is_negative_judgment(i):
                if TextMatch2.negative_word_judgment(content, i):
                    return True
            else:
                # if re.search(i, content):
                if i in content:
                    return True
        return False

    @staticmethod
    def one_match_multi_and_or(content, da_tag, default_len):
        # 包含 tag1 但不包含 tag2
        tag = da_tag.split("-")
        status = various(content, tag, default_len)
        return status

    @staticmethod
    def one_match_multi_and_and(content, da_tag, default_len):
        # 包含 tag1 并且包含 tag2
        tag_list = da_tag.split("+")
        if len(tag_list) == 2:
            status = parentheses_continuous_addition_negative(content, da_tag, default_len)
        else:
            status = new_exclude(content, tag_list)
        return status

    @classmethod
    def one_match_multi_mix(cls, line, mapping, merge_obj,default_len):
        """
        line: 表示每一条记录
        mapping: 表示这个mapping文件的内容
        """
        merge_channel_list = merge_obj.channel_list

        length = mapping.length
        choice = mapping.choice
        Sentment = mapping.sentment
        Layer_number = len(mapping.mapping_list)
        sheetname = mapping.sheetname
        channel = line['channel']
        content = line['content']
        if channel in merge_channel_list:
            content = merge_format_content(line, merge_obj.filter_by(channel_name=channel), sheetname)
        content = get_Text2Formal(content)
        The_Other = []
        Tag_Sen_Keword = []

        for k_map in mapping.mapping_values:

            Be_Label_List = []

            da_tag = get_Text2Formal_keyword(k_map[-1])
            if "-" not in da_tag and "+" not in da_tag:
                Re_list = []
                words = set([i for i in da_tag.split("|") if len(i) > 0])
                for i in words:
                    if cls.is_negative_judgment(i):
                        if cls.negative_word_judgment(content, i):
                            Re_list.extend(negative_word_aspect(content,i))
                    elif i in content:
                        Re_list.append(i)
                Be_Label_List.extend(Re_list)
            else:
                for i in da_tag.split("|"):
                    if "-" in i:
                        if cls.one_match_multi_and_or(content, i,default_len):
                            tag_word = i.split("-")[0]
                            if '(' in tag_word or '（' in tag_word:
                                _ = tag_word[1:-1].split('+')
                                for j in _:
                                    if cls.is_negative_judgment(j):
                                        Be_Label_List.extend(negative_word_aspect(content, j))
                                    else:
                                        Be_Label_List.append(j)
                            else:
                                if cls.is_negative_judgment(tag_word):
                                    Be_Label_List.extend(negative_word_aspect(content, tag_word))
                                else:
                                    Be_Label_List.append(tag_word)

                    elif "+" in i and "(" not in i and "（" not in i:
                        if cls.one_match_multi_and_and(content, i,default_len):
                            for j in i.split("+"):
                                if cls.is_negative_judgment(j):
                                    Be_Label_List.extend(negative_word_aspect(content, j))
                                else:
                                    Be_Label_List.append(j)
                    else:
                        if cls.is_negative_judgment(i):
                            if cls.negative_word_judgment(content, i):
                                Be_Label_List.extend(negative_word_aspect(content, i))
                        elif i in content:
                            Be_Label_List.append(i)


            if len(Be_Label_List) > 0:

                corpora = ",".join(Be_Label_List)

                phr = Phrase()

                phr.keyword = Layer_number
                keyword = eval(phr.keyword)

                if Sentment == True:
                    str_res = keyword + "*" + corpora
                else:
                    str_res = keyword

                The_Other.append(str_res)

        return "噜".join(The_Other)
def negative_word_aspect(content,word):
    '''
    不分句打标方法用来提取否定词的aspect
    :param content: 文本
    :param word: 打标词
    :return:
    '''
    if '#' in word:
        return [word[1:]]
    elif '@' in word:
        text_list = [content[tag_index - 5 if tag_index - 5 >= 0 else 0:tag_index + len(word[1:]) + 5] for tag_index in
                     index_list(content, word[1:])]
        for _ in text_list:
            for foudingci in TextMatch2.negative_word_list:
                if foudingci in _:
                    return [foudingci, word[1:]]

class Phrase():
    @property
    def keyword(self):
        # print(self.phr)
        return self.phr

    @keyword.setter
    def keyword(self, raw):
        self.phr = phr_setter(raw)


def phr_setter(key):
    lnital = "k_map[0]"
    if key > 1:
        for i in range(1, key):
            lnital += "+'*'+k_map[{}]".format(i)
    return lnital


def new_exclude(content, tag_list):
    for tag in tag_list:
        if TextMatch2.is_negative_judgment(tag):
            if TextMatch2.negative_word_judgment(content, tag):
                tag = tag[1:]
            else:
                return False  #
        if tag not in content:
            return False
    return True


def index_list(text, word):
    return [i.start() for i in re.finditer(word, text)]


def exclude(content, tag):
    if len(tag) == 2:
        return True if re.search("(?=.*{})(?=.*{})^.*$".format(tag[0], tag[1]), content) else False
    elif len(tag) == 3:
        return True if re.search("(?=.*{})(?=.*{})(?=.*{})^.*$".format(tag[0], tag[1], tag[2]), content) else False
    elif len(tag) == 4:
        return True if re.search("(?=.*{})(?=.*{})(?=.*{})(?=.*{})^.*$".format(tag[0], tag[1], tag[2], tag[3]),
                                 content) else False
    elif len(tag) == 5:
        return True if re.search(
            "(?=.*{})(?=.*{})(?=.*{})(?=.*{})(?=.*{})^.*$".format(tag[0], tag[1], tag[2], tag[3], tag[4]),
            content) else False
    elif len(tag) == 6:
        return True if re.search(
            "(?=.*{})(?=.*{})(?=.*{})(?=.*{})(?=.*{})(?=.*{})^.*$".format(tag[0], tag[1], tag[2], tag[3], tag[4],
                                                                          tag[5]),
            content) else False
    elif len(tag) == 7:
        return True if re.search(
            "(?=.*{})(?=.*{})(?=.*{})(?=.*{})(?=.*{})(?=.*{})(?=.*{})^.*$".format(tag[0], tag[1], tag[2], tag[3],
                                                                                  tag[4], tag[5], tag[6]),
            content) else False
    elif len(tag) == 8:
        return True if re.search(
            "(?=.*{})(?=.*{})(?=.*{})(?=.*{})(?=.*{})(?=.*{})(?=.*{})(?=.*{})^.*$".format(tag[0], tag[1], tag[2],
                                                                                          tag[3], tag[4], tag[5],
                                                                                          tag[6], tag[7]),
            content) else False


def update_various_first_word(content, word, default_len):
    if "(" in word or "（" in word:
        if deal_parentheses_tag(content, word, default_len):
            return True
    else:
        if TextMatch2.is_negative_judgment(word) and TextMatch2.negative_word_judgment(content, word):
            return True
        # elif re.search(word, content):
        elif word in content:
            return True


def replace_parentheses(words):
    rep = {'(': '', ')': '', '（': "", '）': ''}
    rep = dict((re.escape(k), v) for k, v in rep.items())
    pattern = re.compile("|".join(rep.keys()))
    my_str = pattern.sub(lambda m: rep[re.escape(m.group(0))], words)
    return my_str

def parentheses_continuous_addition_negative(content, tag, preset_length=7):
    '''
    重写的 A+B 的判断规则 增加了否定词的判断
    :param content:
    :param tag:
    :param preset_length:
    :return:
    '''
    assert type(preset_length) == int, "长度不符合规范"
    tag_list = tag.split("+")
    assert len(tag_list) == 2, "关键词长度不符合规范"
    first_word = tag_list[0]
    end_word = tag_list[1]
    _first_word = _end_word = ''
    if TextMatch2.is_negative_judgment(first_word):
        if TextMatch2.negative_word_judgment(content, first_word):
            _first_word = first_word[1:]
        else:
            return False
    if TextMatch2.is_negative_judgment(end_word):
        if TextMatch2.negative_word_judgment(content, end_word):
            _end_word = end_word[1:]
        else:
            return False
    a = first_word if not _first_word else _first_word
    b = end_word if not _end_word else _end_word
    # if not re.search("(?=.*{})(?=.*{})^.*$".format(a, b), content):
    ab = a in content and b in content
    if not ab:
        return False
    first_length = len(a)
    second_length = len(b)
    first_index = index_list(content, a)
    second_index = index_list(content, b)
    for first in first_index:
        for second in second_index:
            if first < second:
                length = second - (first + first_length)
            else:
                length = first - (second + second_length)
            if length < preset_length:
                return True
    return False


def parentheses_continuous_addition(content, tag, preset_length=7):
    assert type(preset_length) == int, "长度不符合规范"
    tag_list = tag.split("+")
    if not re.search("(?=.*{})(?=.*{})^.*$".format(tag_list[0], tag_list[1]), content):
        return False
    first_word = tag_list[0]
    end_word = tag_list[1]
    first_length = len(first_word)
    second_length = len(end_word)
    first_index = indexMany(content, first_word)
    second_index = indexMany(content, end_word)
    for first in first_index:
        for second in second_index:
            if first < second:
                length = second - (first + first_length)
            else:
                length = first - (second + second_length)
            if length < preset_length:
                return True
    return False


def deal_parentheses_tag(content, tag_words, default_len):
    parentheses_words = replace_parentheses(tag_words)
    return parentheses_continuous_addition_negative(content, parentheses_words, default_len)


def various(content, tag, default_len):
    count = 0
    if update_various_first_word(content, tag[0], default_len):
        for i in tag[1:]:
            if "(" in i or "（" in i:

                if deal_parentheses_tag(content, i, default_len):
                    count += 1
            else:
                if i in content:
                    count += 1
        if count == 0:
            return True
        else:
            return False
    else:
        return False


def merge_content(line):
    content = "" if not line['content'] else line['content']
    title = "" if not line['title'] else line['title']
    result = str(content) + str(title)
    return result


def get_Text2Formal(line):
    """
    1. 将繁体转换成简体
    2. 删除表情
    3. \n 转化为空
    4. !！?？#,，@… ~～。. 全部用空格替换
    5. 将2个或者以上空格转化为空
    6. 将 字母+空格(一个或多个)+字母 的空格转化为_，并将字母转化为小写
    """
    line = str(line)
    # t2s = Tradition2Simple()
    # line = t2s.process(line)
    line = remove_emoji(line)
    line = re.sub(r"[\n]+", "", line.strip())
    line = re.sub(r"[!！?？#,，@… ~～。.`、'‘]+", " ", line)
    line = re.sub(r"( ){2,}", "", line)
    while 1:
        result = re.sub(r'(.*[A-Za-z])( )+([A-Za-z].*)', r'\1_\3', line)
        if result == line:
            break
        line = result
    return line.lower().strip()
def get_Text2Formal_keyword(line):
    """
    只是针对于关键词  与 get_Text2Formal 相比  去除了将 @，# 变为空格的规则，其他不变
    1. 将繁体转换成简体
    2. 删除表情
    3. \n 转化为空
    4. !！?？,，… ~～。. 全部用空格替换
    5. 将2个或者以上空格转化为空
    6. 将 字母+空格(一个或多个)+字母 的空格转化为_，并将字母转化为小写
    """
    line = str(line)
    # t2s = Tradition2Simple()
    # line = t2s.process(line)
    line = remove_emoji(line)
    line = re.sub(r"[\n]+", "", line.strip())
    line = re.sub(r"[!！?？,，… ~～。.`、'‘]+", " ", line)
    line = re.sub(r"( ){2,}", "", line)
    while 1:
        result = re.sub(r'(.*[A-Za-z])( )+([A-Za-z].*)', r'\1_\3', line)
        if result == line:
            break
        line = result
    return line.lower().strip()


def conduct_relation_tag_tree(data, mapping):
    data['merge_tag'] = data.apply(lambda line: deal_sentence_tag(line, mapping), axis=1)
    data['merge_index'] = range(data.shape[0])
    split_merge_index = data.groupby('merge_index')
    df_list = [related_word_mapping(the_data, mapping) for name, the_data in split_merge_index]
    df_data = pd.concat(df_list, join="inner")
    df_data.drop(['merge_index', 'merge_tag'], axis=1, inplace=True)
    return df_data


def related_word_mapping(intermediate, line, mapping):
    merge_series = line[intermediate]
    if str(merge_series.values[0]) in ["nan", "", "NaN", "null", "Null", "None"]:
        return line
    merge_series_values = eval(merge_series.values[0])
    contrast_list = merge_series_values[0]
    the_now_list = [re.findall("(?<=\()\S+(?=\))", contra)[0] for contra in contrast_list]

    merge_list = np.array(merge_series_values)

    # the_mapping_list = mapping.get_map_name_collect()
    inner_name = [name + "-id" for name in the_now_list]

    total_merge_df = pd.DataFrame(merge_list, columns=inner_name)
    for _sheet in the_now_list:
        sheet_name = _sheet
        sheet_df = mapping.filter_by(name=_sheet).mapping_df
        total_merge_df["{}-id".format(sheet_name)] = total_merge_df["{}-id".format(
            sheet_name)].apply(lambda line: -1 if line == "({})".format(sheet_name) else int(line.split("(")[0]))
        total_merge_df = pd.merge(total_merge_df, sheet_df, on="{}-id".format(sheet_name), how="left")
    total_merge_df = total_merge_df.drop(inner_name, axis=1)
    line.insert(1, 'related_index', [1])
    total_merge_df['related_index'] = 1
    inner_line = pd.merge(line, total_merge_df, on="related_index", how='left')
    line = inner_line.drop(columns=['related_index'])
    return line


def deal_sentence_tag(line, mapping, map_1=None, map_0=None):
    # content = "1葡萄牙和中国是芯动的感觉！2葡萄牙和中国是芯动的感觉，韩硕和韩松林端午一起去了长城。3京东618限时定制一款兰博基尼！4京东618限时定制一款兰博基尼，然后韩硕和韩松林和韩翱键盘端午一起去了长城！5京东618限时定制一款怀旧版得兰博基尼，将由葡萄牙和中国一起生产，然后韩硕和韩松林和韩翱键盘端午一起去了长城！"
    test_tag = SplitSentenceTag()
    result = test_tag.process(line, mapping, map_1, map_0)
    result1 = result[0]  # 之前的打标
    result2 = result[-1]  # 新加的中间结果
    return result1, result2


class SplitSentenceTag(object):
    def __init__(self, params=None):
        pass

    def process(self, line, mapping, map_1=None, map_0=None):
        '''
        原来的话在这设了个列表用来接收，现在计划返回一个列表
        :param line:    一行数据
        :param mapping:    关键词表对象
        :return:
        '''
        sentences = extract_content(line, mapping)
        # print(sentences)
        list_all_sentences_tag = []
        list_all_data = []  # 存放新增需求信息：
        for content_i in sentences:
            # 对每个分句进行打标
            result = get_relation_tag(line,content_i, mapping, map_1, map_0)  # 打标返回结果的要求：
            # 对打标结果进行拆分
            list_tag_int = tag_split(result[0])
            list_all_sentences_tag.extend(list_tag_int)
            list_all_data.extend(result[-1])

        # 对一句话中的标签进行去重。 下面的双重循环去不掉重复的数据。k != i
        new_list_all_sentences_tag = []
        for list_i in list_all_sentences_tag:
            if list_i not in new_list_all_sentences_tag:
                new_list_all_sentences_tag.append(list_i)

        # 将list放入一个新list地址中， 避免删除new_list_all_sentences_tag第一个数据时，遍历不到第二个数据得问题。
        new_list_all_sentences_tag_last = []
        new_list_all_sentences_tag_last = new_list_all_sentences_tag_last + new_list_all_sentences_tag
        for i in new_list_all_sentences_tag:
            # 当打标表为一个词表时 新加的 处理翱建遗留的bug
            if type(i) == str:
                continue
            for str_j in [k for k in new_list_all_sentences_tag if k != i]:
                if (len(i) == 2) and (i[0] in str_j) and (i[1] in str_j) and (i in new_list_all_sentences_tag_last):
                    new_list_all_sentences_tag_last.remove(i)
                elif (len(i) == 3) and (i[0] in str_j) and (i[1] in str_j) and (i[2] in str_j) and (
                        i in new_list_all_sentences_tag_last):
                    new_list_all_sentences_tag_last.remove(i)
                elif (len(i) == 4) and (i[0] in str_j) and (i[1] in str_j) and (i[2] in str_j) and (i[3] in str_j) and (
                        i in new_list_all_sentences_tag_last):
                    new_list_all_sentences_tag_last.remove(i)
                elif (len(i) == 5) and (i[0] in str_j) and (i[1] in str_j) and (i[2] in str_j) and (i[3] in str_j) and (
                        i[4] in str_j) and (i in new_list_all_sentences_tag_last):
                    new_list_all_sentences_tag_last.remove(i)
                elif (len(i) == 6) and (i[0] in str_j) and (i[1] in str_j) and (i[2] in str_j) and (i[3] in str_j) and (
                        i[4] in str_j) and (i[5] in str_j) and (i in new_list_all_sentences_tag_last):
                    new_list_all_sentences_tag_last.remove(i)
                elif (len(i) == 7) and (i[0] in str_j) and (i[1] in str_j) and (i[2] in str_j) and (i[3] in str_j) and (
                        i[4] in str_j) and (i[5] in str_j) and (i[6] in str_j) and (
                        i in new_list_all_sentences_tag_last):
                    new_list_all_sentences_tag_last.remove(i)

        # 如果长度大于2 ,里面是空的去掉。
        # if len(new_list_all_sentences_tag_last) >= 2:
        #     for list_small in new_list_all_sentences_tag_last:
        #         if set(list_small) == set(['']):
        #             new_list_all_sentences_tag_last.remove(list_small)

        if len(new_list_all_sentences_tag_last) >= 2:
            for list_small in new_list_all_sentences_tag_last:
                str_j = "".join(list_small).strip()
                if not bool(re.search(r'\d', str_j)):
                    new_list_all_sentences_tag_last.remove(list_small)

        return new_list_all_sentences_tag_last, list_all_data


def tag_split(tag_dict):
    dict_to_list = list(tag_dict.values())
    dict_count = len(tag_dict)
    tag_all_list = []
    if dict_count == 1:
        tag_all_list = dict_to_list[0]
    elif dict_count == 2:
        for i in dict_to_list[0]:
            for j in dict_to_list[1]:
                tag_all_list.append([i, j])
    elif dict_count == 3:
        for i in dict_to_list[0]:
            for j in dict_to_list[1]:
                for k in dict_to_list[2]:
                    tag_all_list.append([i, j, k])
    elif dict_count == 4:
        for i in dict_to_list[0]:
            for j in dict_to_list[1]:
                for k in dict_to_list[2]:
                    for l in dict_to_list[3]:
                        tag_all_list.append([i, j, k, l])
    elif dict_count == 5:
        for i in dict_to_list[0]:
            for j in dict_to_list[1]:
                for k in dict_to_list[2]:
                    for l in dict_to_list[3]:
                        for m in dict_to_list[4]:
                            tag_all_list.append([i, j, k, l, m])
    elif dict_count == 6:
        for i in dict_to_list[0]:
            for j in dict_to_list[1]:
                for k in dict_to_list[2]:
                    for l in dict_to_list[3]:
                        for m in dict_to_list[4]:
                            for n in dict_to_list[5]:
                                tag_all_list.append([i, j, k, l, m, n])
    elif dict_count == 7:
        for i in dict_to_list[0]:
            for j in dict_to_list[1]:
                for k in dict_to_list[2]:
                    for l in dict_to_list[3]:
                        for m in dict_to_list[4]:
                            for n in dict_to_list[5]:
                                for o in dict_to_list[6]:
                                    tag_all_list.append([i, j, k, l, m, n, o])

    return tag_all_list

def remove_topic(content):
    '''
    去除文本中的话题，@后的内容
    :param content: 文本内容
    :return:
    '''
    if '@' in content:
        # 正常的@用户
        li = re.findall(r'@(.*?) ', content)
        _ = ['@' + i for i in li]
        for i in _:
            if len(i) > 17:
                i = i[:17]
            content = content.replace(i, '')
        # 不正常的@用户
        aite_index = index_list(content, '@')
        _ = [content[i:i + 8] for i in aite_index]
        for i in _:
            content = content.replace(i, '')
    if '#' in content:
        a = re.findall(r'#(.*?)#', content)
        _ = ['#' + i + '#' for i in a]
        for i in _:
            content = content.replace(i, '')
    return content


def extract_content(line, mapping):
    '''
    判断是否需要合并字段，返回要打标的内容
    :param line: 一行数据
    :return:
    '''
    max_list = []
    content_list = []  # 存放要打标的内容
    default_value = 'content'
    for map_i in mapping:
        if line['channel'] in tag_choice_dic and '*' in tag_choice_dic[line['channel']].keys():
            max_list.extend(tag_choice_dic[line['channel']]['*'])
        elif line['channel'] in tag_choice_dic and map_i.sheetname in tag_choice_dic[line['channel']]:
            max_list.extend(tag_choice_dic[line['channel']][map_i.sheetname])
    max_list = list(set(max_list))

    if max_list:
        for i in max_list:
            sentences = re.split(split_sign, remove_topic(line[i]))
            for j in sentences:
                content_dict = {}    # 存放要合并的内容
                content_dict[i] = get_Text2Formal(j)
                content_list.append(content_dict)
        return content_list
    else:
        sentences = re.split(split_sign, remove_topic(line[default_value]))
        for j in sentences:
            content_dict = {}    # 存放要合并的内容
            content_dict[default_value] = get_Text2Formal(j)
            content_list.append(content_dict)
        return content_list


def dabiaofunc(name, map_i, map_values, value, result_list, map_list, default_len=7):
    # TODO 打标规则 -------------------
    # 后来加的购买 ，不太合适
    if name == '购买' and len(list(filter(lambda x: x in value, TextMatch2.goumai_list))) == 0:
        return result_list, map_list

    for map_res in map_values:
        map_ = map_res[-1]
        tag = 0
        if "-" not in map_ and "+" not in map_:
            if TextMatch2.one_match_multi_or(value, map_):
                tag += 1
                d = map_i.mapping_df[
                    map_i.mapping_df['{}(keyword)'.format(name)] == map_].values  # 包含父级关系的数据 列表
                dd = '~'.join(map(str, d[0][:-1]))
                result = TextMatch2.one_match_multi_or_clause(value, map_)
                result_list.append(dd + '*' + map_ + '*' + ','.join(result))
        else:
            for i in map_.split("|"):
                if "-" in i:
                    if TextMatch2.one_match_multi_and_or(value, i, default_len):
                        tag += 1
                        d = map_i.mapping_df[map_i.mapping_df['{}(keyword)'.format(name)] == map_].values
                        dd = '~'.join(map(str, d[0][:-1]))
                        if "(" not in i and "（" not in i:
                            result_list.append(dd + '*' + map_ + '*' + i.split('-')[0])
                        else:
                            result = replace_parentheses(i.split('-')[0])
                            result_list.append(dd + '*' + map_ + '*' + ','.join(result.split('+')))

                elif "+" in i and "(" not in i and "（" not in i:
                    if TextMatch2.one_match_multi_and_and(value, i, default_len):
                        tag += 1
                        d = map_i.mapping_df[map_i.mapping_df['{}(keyword)'.format(name)] == map_].values
                        dd = '~'.join(map(str, d[0][:-1]))
                        result_list.append(dd + '*' + map_ + '*' + ','.join(i.split('+')))
                else:
                    if TextMatch2.one_match_multi_or(value, i):
                        tag += 1
                        d = map_i.mapping_df[map_i.mapping_df['{}(keyword)'.format(name)] == map_].values
                        dd = '~'.join(map(str, d[0][:-1]))
                        result_list.append(dd + '*' + map_ + '*' + i)
        if tag > 0:
            map_list.append("{}({})".format(str(map_res[0]), name))
    return result_list, map_list


def get_relation_tag(line, content, relation_mapping, map_1=None, map_0=None,):
    mappings = relation_mapping
    result_dic = {}
    result_list = []  # 存放关键词和实际打到的词
    # 我给的content是： {content or title:'要打标的文本内容'}
    key = list(content.keys())[0]
    value = list(content.values())[0]
    for map_i in mappings:
        map_list = []
        name = map_i.sheetname
        # 因为只有品牌有title要求，其他都没有。
        if name == '品牌':
            if '品牌(需求)' in map_i.mapping_list:  # 填充情况下的词表
                map_values_jh = map_1[['{}-id'.format(name), '{}(keyword)'.format(name)]].values
                if key == 'title' and line['channel'] in ['tmall', 'jd']:
                    result_list, map_list = dabiaofunc(name, map_i, map_values_jh, value, result_list, map_list,
                                                       default_len=100)
                else:
                    result_list, map_list = dabiaofunc(name, map_i, map_values_jh, value, result_list, map_list)
                if len(map_list) == 0:
                    map_values_jh = map_0[['{}-id'.format(name), '{}(keyword)'.format(name)]].values
                    result_list, map_list = dabiaofunc(name, map_i, map_values_jh, value, result_list, map_list)
            else:  # 正常情况下的词表
                map_values_jh = map_i.mapping_df[['{}-id'.format(name), '{}(keyword)'.format(name)]].values
                if key == 'title' and line['channel'] in ['tmall', 'jd']:
                    result_list, map_list = dabiaofunc(name, map_i, map_values_jh, value, result_list, map_list,
                                                       default_len=100)
                else:
                    result_list, map_list = dabiaofunc(name, map_i, map_values_jh, value, result_list, map_list)
        else:
            if line['channel'] in tag_choice_dic and '*' in tag_choice_dic[line['channel']].keys() and key in \
                    tag_choice_dic[line['channel']]['*']:
                map_values_jh = map_i.mapping_df[['{}-id'.format(name), '{}(keyword)'.format(name)]].values
                result_list, map_list = dabiaofunc(name, map_i, map_values_jh, value, result_list, map_list)
            elif key == 'content':
                map_values_jh = map_i.mapping_df[['{}-id'.format(name), '{}(keyword)'.format(name)]].values
                result_list, map_list = dabiaofunc(name, map_i, map_values_jh, value, result_list, map_list)
        if len(map_list) > 0:
            result_dic[name] = map_list
        else:
            result_dic[name] = ['({})'.format(name)]
    return result_dic, result_list


class TagContentChoiceCollect:
    tag_content_choice_list = []

    def __init__(self, choice_dict_collect):
        self.tag_content_choice_list = [TagContentChoice({channel: choice})
                                        for channel, choice in choice_dict_collect.items()]

    @property
    def channel_list(self):
        return [tag_content_choice.channel for tag_content_choice in self.tag_content_choice_list]

    def filter_by(self, **kwargs):
        channel_name = kwargs.get('channel_name')
        filter_tag_choice = list(filter(lambda tag_content_choice: tag_content_choice.channel == channel_name,
                                        self.tag_content_choice_list))
        if len(filter_tag_choice) > 0:
            result = filter_tag_choice[0]
        else:
            result = None
        return result


class TagContentChoice:
    def __init__(self, choice_dict):
        self.channel = list(choice_dict.keys())[0]
        self.choice = choice_dict.get(self.channel)

    @property
    def deal_sheet(self):
        return list(self.choice.keys())

    def merge_content_list(self, sheet):
        # 这个if判断是贾浩后来加上的
        if None == self.choice.get(sheet):
            return self.choice['*']
        return self.choice.get(sheet)


def merge_format_content(line, merge_obj, sheetname):
    # 第一个if判断是贾浩后来加上的
    if '*' in merge_obj.deal_sheet:
        merge_list = merge_obj.merge_content_list(sheetname)
        merge_text_list = [deal_format_nan_text(line[text]) for text in merge_list]
        result = "".join(merge_text_list)
    elif sheetname in merge_obj.deal_sheet:
        merge_list = merge_obj.merge_content_list(sheetname)
        merge_text_list = [deal_format_nan_text(line[text]) for text in merge_list]
        result = "".join(merge_text_list)
    else:
        result = str(line['content'])
    return result


def deal_format_nan_text(text):
    text = "" if not text else str(text)
    return text